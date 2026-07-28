// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vmilan_datapath.h for the primary calling header

#include "Vmilan_datapath__pch.h"

void Vmilan_datapath___024root___nba_sequent__TOP__2(Vmilan_datapath___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vmilan_datapath___024root___nba_sequent__TOP__2\n"); );
    Vmilan_datapath__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    CData/*4:0*/ milan_datapath__DOT__pkt_slot_w;
    milan_datapath__DOT__pkt_slot_w = 0;
    CData/*6:0*/ milan_datapath__DOT__csr_tctx_rd_addr_w;
    milan_datapath__DOT__csr_tctx_rd_addr_w = 0;
    QData/*63:0*/ milan_datapath__DOT__i2s_feed_tdata_w;
    milan_datapath__DOT__i2s_feed_tdata_w = 0;
    QData/*47:0*/ milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__4__KET____DOT__u_cbs__DOT__eng_quo_r;
    milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__4__KET____DOT__u_cbs__DOT__eng_quo_r = 0;
    QData/*47:0*/ milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__3__KET____DOT__u_cbs__DOT__eng_quo_r;
    milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__3__KET____DOT__u_cbs__DOT__eng_quo_r = 0;
    QData/*47:0*/ milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__2__KET____DOT__u_cbs__DOT__eng_quo_r;
    milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__2__KET____DOT__u_cbs__DOT__eng_quo_r = 0;
    QData/*47:0*/ milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__1__KET____DOT__u_cbs__DOT__eng_quo_r;
    milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__1__KET____DOT__u_cbs__DOT__eng_quo_r = 0;
    QData/*47:0*/ milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__0__KET____DOT__u_cbs__DOT__eng_quo_r;
    milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__0__KET____DOT__u_cbs__DOT__eng_quo_r = 0;
    CData/*3:0*/ milan_datapath__DOT__chan_map_render__DOT__chans_raw_w;
    milan_datapath__DOT__chan_map_render__DOT__chans_raw_w = 0;
    CData/*0:0*/ milan_datapath__DOT__chan_map_render__DOT__avb_ok_w;
    milan_datapath__DOT__chan_map_render__DOT__avb_ok_w = 0;
    IData/*31:0*/ milan_datapath__DOT__aaf_packetizer__DOT__rr_pick__DOT__unnamedblk3__DOT__unnamedblk4__DOT__t;
    milan_datapath__DOT__aaf_packetizer__DOT__rr_pick__DOT__unnamedblk3__DOT__unnamedblk4__DOT__t = 0;
    CData/*0:0*/ milan_datapath__DOT__chan_map_capture__DOT__lb_sel_ok_w;
    milan_datapath__DOT__chan_map_capture__DOT__lb_sel_ok_w = 0;
    QData/*63:0*/ __Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__123__w;
    __Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__123__w = 0;
    QData/*63:0*/ __Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__124__w;
    __Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__124__w = 0;
    QData/*63:0*/ __Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__125__w;
    __Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__125__w = 0;
    QData/*63:0*/ __Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__126__w;
    __Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__126__w = 0;
    QData/*63:0*/ __Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__127__w;
    __Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__127__w = 0;
    QData/*63:0*/ __Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__128__w;
    __Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__128__w = 0;
    QData/*63:0*/ __Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__129__w;
    __Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__129__w = 0;
    QData/*63:0*/ __Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__130__w;
    __Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__130__w = 0;
    QData/*63:0*/ __Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__131__w;
    __Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__131__w = 0;
    QData/*63:0*/ __Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__132__w;
    __Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__132__w = 0;
    QData/*63:0*/ __Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__133__w;
    __Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__133__w = 0;
    QData/*63:0*/ __Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__134__w;
    __Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__134__w = 0;
    QData/*63:0*/ __Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__135__w;
    __Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__135__w = 0;
    QData/*63:0*/ __Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__136__w;
    __Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__136__w = 0;
    QData/*63:0*/ __Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__137__w;
    __Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__137__w = 0;
    QData/*63:0*/ __Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__138__w;
    __Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__138__w = 0;
    QData/*63:0*/ __Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__139__w;
    __Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__139__w = 0;
    QData/*63:0*/ __Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__140__w;
    __Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__140__w = 0;
    QData/*63:0*/ __Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__141__w;
    __Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__141__w = 0;
    QData/*63:0*/ __Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__142__w;
    __Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__142__w = 0;
    QData/*63:0*/ __Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__143__w;
    __Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__143__w = 0;
    QData/*63:0*/ __Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__144__w;
    __Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__144__w = 0;
    IData/*23:0*/ __Vfunc_milan_datapath__DOT__chan_map_render__DOT__src_rd__181__Vfuncout;
    __Vfunc_milan_datapath__DOT__chan_map_render__DOT__src_rd__181__Vfuncout = 0;
    CData/*6:0*/ __Vfunc_milan_datapath__DOT__chan_map_render__DOT__src_rd__181__a;
    __Vfunc_milan_datapath__DOT__chan_map_render__DOT__src_rd__181__a = 0;
    CData/*6:0*/ __Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__274__Vfuncout;
    __Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__274__Vfuncout = 0;
    CData/*2:0*/ __Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__274__t;
    __Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__274__t = 0;
    CData/*4:0*/ __VdfgRegularize_h6e95ff9d_0_93;
    __VdfgRegularize_h6e95ff9d_0_93 = 0;
    VlWide<3>/*73:0*/ __VdlyVal__milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__mem__v0;
    VL_ZERO_W(74, __VdlyVal__milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__mem__v0);
    CData/*7:0*/ __VdlyDim0__milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__mem__v0;
    __VdlyDim0__milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__mem__v0 = 0;
    // Body
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_17 = ((0x8100U 
                                                  == 
                                                  (vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__hdr_eff[2U] 
                                                   >> 0x00000010U))
                                                  ? 
                                                 (((QData)((IData)(
                                                                   (vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__hdr_eff[1U] 
                                                                    >> 0x00000010U))) 
                                                   << 0x00000020U) 
                                                  | (QData)((IData)(vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__hdr_eff[2U])))
                                                  : 
                                                 ((QData)((IData)(
                                                                  (vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__hdr_eff[2U] 
                                                                   >> 0x00000010U))) 
                                                  << 0x00000020U));
    vlSelfRef.milan_datapath__DOT__pair_zero_fill__DOT__fed_now_c 
        = vlSelfRef.milan_datapath__DOT__pair_zero_fill__DOT__fed_now_r;
    if (vlSelfRef.milan_datapath__DOT__aafcap_pv_w) {
        vlSelfRef.milan_datapath__DOT__pair_zero_fill__DOT__fed_now_c 
            = (vlSelfRef.milan_datapath__DOT__pair_zero_fill__DOT__fed_now_c 
               | (0x00000000ffffffffULL & ((IData)(1U) 
                                           << (0x0000000fU 
                                               & (IData)(
                                                         (vlSelfRef.milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__cap_pair_w 
                                                          >> 0x00000030U))))));
    }
    vlSelfRef.milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__cap_rempty_w 
        = ((1U & (~ (IData)(vlSelfRef.axis_resetn))) 
           || ((IData)(vlSelfRef.milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__u_tcdc__DOT__rptr_gray_n) 
               == (IData)(vlSelfRef.milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__u_tcdc__DOT__wgray_r2_r)));
    vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__loop_mapped_w = 0U;
    if (((vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[0U] 
          >> 7U) & (5U == (7U & (vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[0U] 
                                 >> 4U))))) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[1U] 
          >> 7U) & (5U == (7U & (vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[1U] 
                                 >> 4U))))) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[2U] 
          >> 7U) & (5U == (7U & (vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[2U] 
                                 >> 4U))))) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[3U] 
          >> 7U) & (5U == (7U & (vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[3U] 
                                 >> 4U))))) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[4U] 
          >> 7U) & (5U == (7U & (vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[4U] 
                                 >> 4U))))) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[5U] 
          >> 7U) & (5U == (7U & (vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[5U] 
                                 >> 4U))))) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[6U] 
          >> 7U) & (5U == (7U & (vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[6U] 
                                 >> 4U))))) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[7U] 
          >> 7U) & (5U == (7U & (vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[7U] 
                                 >> 4U))))) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[8U] 
          >> 7U) & (5U == (7U & (vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[8U] 
                                 >> 4U))))) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[9U] 
          >> 7U) & (5U == (7U & (vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[9U] 
                                 >> 4U))))) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[10U] 
          >> 7U) & (5U == (7U & (vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[10U] 
                                 >> 4U))))) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[11U] 
          >> 7U) & (5U == (7U & (vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[11U] 
                                 >> 4U))))) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[12U] 
          >> 7U) & (5U == (7U & (vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[12U] 
                                 >> 4U))))) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[13U] 
          >> 7U) & (5U == (7U & (vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[13U] 
                                 >> 4U))))) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[14U] 
          >> 7U) & (5U == (7U & (vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[14U] 
                                 >> 4U))))) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[15U] 
          >> 7U) & (5U == (7U & (vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[15U] 
                                 >> 4U))))) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[16U] 
          >> 7U) & (5U == (7U & (vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[16U] 
                                 >> 4U))))) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[17U] 
          >> 7U) & (5U == (7U & (vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[17U] 
                                 >> 4U))))) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[18U] 
          >> 7U) & (5U == (7U & (vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[18U] 
                                 >> 4U))))) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[19U] 
          >> 7U) & (5U == (7U & (vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[19U] 
                                 >> 4U))))) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[20U] 
          >> 7U) & (5U == (7U & (vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[20U] 
                                 >> 4U))))) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[21U] 
          >> 7U) & (5U == (7U & (vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[21U] 
                                 >> 4U))))) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[22U] 
          >> 7U) & (5U == (7U & (vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[22U] 
                                 >> 4U))))) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[23U] 
          >> 7U) & (5U == (7U & (vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[23U] 
                                 >> 4U))))) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[24U] 
          >> 7U) & (5U == (7U & (vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[24U] 
                                 >> 4U))))) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[25U] 
          >> 7U) & (5U == (7U & (vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[25U] 
                                 >> 4U))))) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[26U] 
          >> 7U) & (5U == (7U & (vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[26U] 
                                 >> 4U))))) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[27U] 
          >> 7U) & (5U == (7U & (vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[27U] 
                                 >> 4U))))) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[28U] 
          >> 7U) & (5U == (7U & (vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[28U] 
                                 >> 4U))))) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[29U] 
          >> 7U) & (5U == (7U & (vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[29U] 
                                 >> 4U))))) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[30U] 
          >> 7U) & (5U == (7U & (vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[30U] 
                                 >> 4U))))) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__loop_mapped_w = 1U;
    }
    if (((vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[31U] 
          >> 7U) & (5U == (7U & (vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r[31U] 
                                 >> 4U))))) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__loop_mapped_w = 1U;
    }
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_2 = (7U 
                                                & (vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r
                                                   [vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__slot_r] 
                                                   >> 4U));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_10 = (0x0000000fU 
                                                 & vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r
                                                 [vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__slot_r]);
    vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lfsr_next_w 
        = ((0x0000fffeU & ((IData)(vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lfsr_r) 
                           << 1U)) | (1U & VL_REDXOR_16(
                                                        (0xd008U 
                                                         & (IData)(vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lfsr_r)))));
    vlSelfRef.milan_datapath__DOT__adp_tx_tlast = (
                                                   (1U 
                                                    == (IData)(vlSelfRef.milan_datapath__DOT__adp_adv__DOT__state_r)) 
                                                   & (0x0aU 
                                                      == (IData)(vlSelfRef.milan_datapath__DOT__adp_adv__DOT__beat_r)));
    vlSelfRef.milan_datapath__DOT__csr__DOT__live_hit = 1U;
    if ((0x00008000U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
        if ((1U & (~ ((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                      & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
            if ((1U & (~ ((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                          & (0x08b4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                if ((1U & (~ ((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                              & (0x08c8U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                    if ((1U & (~ ((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                  & (0x08d4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                        if ((1U & (~ ((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                      & (0x0940U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_hit = 0U;
                        }
                    }
                }
            }
        }
    } else if ((0x00004000U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
        if ((1U & (~ ((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                      & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
            if ((1U & (~ ((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                          & (0x08b4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                if ((1U & (~ ((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                              & (0x08c8U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                    if ((1U & (~ ((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                  & (0x08d4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                        if ((1U & (~ ((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                      & (0x0940U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_hit = 0U;
                        }
                    }
                }
            }
        }
    } else if ((0x00002000U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
        if ((1U & (~ ((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                      & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
            if ((1U & (~ ((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                          & (0x08b4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                if ((1U & (~ ((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                              & (0x08c8U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                    if ((1U & (~ ((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                  & (0x08d4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                        if ((1U & (~ ((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                      & (0x0940U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_hit = 0U;
                        }
                    }
                }
            }
        }
    } else if ((0x00001000U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
        if ((1U & (~ ((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                      & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
            if ((1U & (~ ((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                          & (0x08b4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                if ((1U & (~ ((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                              & (0x08c8U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                    if ((1U & (~ ((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                  & (0x08d4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                        if ((1U & (~ ((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                      & (0x0940U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_hit = 0U;
                        }
                    }
                }
            }
        }
    } else if ((0x00000800U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
        if ((0x00000400U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
            if ((1U & (~ ((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                          & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                if ((1U & (~ ((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                              & (0x08b4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                    if ((1U & (~ ((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                  & (0x08c8U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                        if ((1U & (~ ((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                      & (0x08d4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                            if ((1U & (~ ((0x0900U 
                                           <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                          & (0x0940U 
                                             > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_hit = 0U;
                            }
                        }
                    }
                }
            }
        } else if ((0x00000200U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
            if ((1U & (~ ((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                          & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                if ((1U & (~ ((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                              & (0x08b4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                    if ((1U & (~ ((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                  & (0x08c8U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                        if ((1U & (~ ((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                      & (0x08d4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                            if ((1U & (~ ((0x0900U 
                                           <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                          & (0x0940U 
                                             > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_hit = 0U;
                            }
                        }
                    }
                }
            }
        } else if ((0x00000100U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
            if ((0x00000080U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                if ((1U & (~ ((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                              & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                    if ((1U & (~ ((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                  & (0x08b4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                        if ((1U & (~ ((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                      & (0x08c8U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                            if ((1U & (~ ((0x08c8U 
                                           <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                          & (0x08d4U 
                                             > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                if ((1U & (~ ((0x0900U 
                                               <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                              & (0x0940U 
                                                 > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_hit = 0U;
                                }
                            }
                        }
                    }
                }
            } else if ((0x00000040U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                if ((1U & (~ ((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                              & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                    if ((1U & (~ ((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                  & (0x08b4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                        if ((1U & (~ ((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                      & (0x08c8U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                            if ((1U & (~ ((0x08c8U 
                                           <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                          & (0x08d4U 
                                             > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                if ((1U & (~ ((0x0900U 
                                               <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                              & (0x0940U 
                                                 > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_hit = 0U;
                                }
                            }
                        }
                    }
                }
            } else if ((0x00000020U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                if ((1U & (~ ((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                              & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                    if ((1U & (~ ((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                  & (0x08b4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                        if ((1U & (~ ((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                      & (0x08c8U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                            if ((1U & (~ ((0x08c8U 
                                           <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                          & (0x08d4U 
                                             > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                if ((1U & (~ ((0x0900U 
                                               <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                              & (0x0940U 
                                                 > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_hit = 0U;
                                }
                            }
                        }
                    }
                }
            } else if ((0x00000010U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                if ((8U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                    if ((1U & (~ ((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                  & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                        if ((1U & (~ ((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                      & (0x08b4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                            if ((1U & (~ ((0x08b4U 
                                           <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                          & (0x08c8U 
                                             > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                if ((1U & (~ ((0x08c8U 
                                               <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                              & (0x08d4U 
                                                 > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                    if ((1U & (~ ((0x0900U 
                                                   <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                  & (0x0940U 
                                                     > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_hit = 0U;
                                    }
                                }
                            }
                        }
                    }
                } else if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                    if ((1U & (~ ((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                  & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                        if ((1U & (~ ((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                      & (0x08b4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                            if ((1U & (~ ((0x08b4U 
                                           <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                          & (0x08c8U 
                                             > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                if ((1U & (~ ((0x08c8U 
                                               <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                              & (0x08d4U 
                                                 > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                    if ((1U & (~ ((0x0900U 
                                                   <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                  & (0x0940U 
                                                     > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_hit = 0U;
                                    }
                                }
                            }
                        }
                    }
                } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                    if ((1U & (~ ((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                  & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                        if ((1U & (~ ((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                      & (0x08b4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                            if ((1U & (~ ((0x08b4U 
                                           <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                          & (0x08c8U 
                                             > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                if ((1U & (~ ((0x08c8U 
                                               <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                              & (0x08d4U 
                                                 > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                    if ((1U & (~ ((0x0900U 
                                                   <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                  & (0x0940U 
                                                     > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_hit = 0U;
                                    }
                                }
                            }
                        }
                    }
                }
            } else if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                if ((1U & (~ ((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                              & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                    if ((1U & (~ ((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                  & (0x08b4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                        if ((1U & (~ ((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                      & (0x08c8U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                            if ((1U & (~ ((0x08c8U 
                                           <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                          & (0x08d4U 
                                             > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                if ((1U & (~ ((0x0900U 
                                               <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                              & (0x0940U 
                                                 > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_hit = 0U;
                                }
                            }
                        }
                    }
                }
            } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                if ((1U & (~ ((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                              & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                    if ((1U & (~ ((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                  & (0x08b4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                        if ((1U & (~ ((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                      & (0x08c8U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                            if ((1U & (~ ((0x08c8U 
                                           <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                          & (0x08d4U 
                                             > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                if ((1U & (~ ((0x0900U 
                                               <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                              & (0x0940U 
                                                 > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_hit = 0U;
                                }
                            }
                        }
                    }
                }
            }
        } else if ((0x00000080U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
            if ((0x00000040U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                if ((0x00000020U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                    if ((0x00000010U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                        if ((8U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                            if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                                if ((1U & (~ ((0x0210U 
                                               <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                              & (0x0234U 
                                                 > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                    if ((1U & (~ ((0x0874U 
                                                   <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                  & (0x08b4U 
                                                     > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                        if ((1U & (~ 
                                                   ((0x08b4U 
                                                     <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                    & (0x08c8U 
                                                       > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                            if ((1U 
                                                 & (~ 
                                                    ((0x08c8U 
                                                      <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                     & (0x08d4U 
                                                        > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                                if (
                                                    (1U 
                                                     & (~ 
                                                        ((0x0900U 
                                                          <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                         & (0x0940U 
                                                            > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_hit = 0U;
                                                }
                                            }
                                        }
                                    }
                                }
                            } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                                if ((1U & (~ ((0x0210U 
                                               <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                              & (0x0234U 
                                                 > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                    if ((1U & (~ ((0x0874U 
                                                   <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                  & (0x08b4U 
                                                     > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                        if ((1U & (~ 
                                                   ((0x08b4U 
                                                     <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                    & (0x08c8U 
                                                       > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                            if ((1U 
                                                 & (~ 
                                                    ((0x08c8U 
                                                      <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                     & (0x08d4U 
                                                        > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                                if (
                                                    (1U 
                                                     & (~ 
                                                        ((0x0900U 
                                                          <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                         & (0x0940U 
                                                            > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_hit = 0U;
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        } else if ((1U & (~ ((0x0210U 
                                              <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                             & (0x0234U 
                                                > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                            if ((1U & (~ ((0x0874U 
                                           <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                          & (0x08b4U 
                                             > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                if ((1U & (~ ((0x08b4U 
                                               <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                              & (0x08c8U 
                                                 > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                    if ((1U & (~ ((0x08c8U 
                                                   <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                  & (0x08d4U 
                                                     > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                        if ((1U & (~ 
                                                   ((0x0900U 
                                                     <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                    & (0x0940U 
                                                       > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_hit = 0U;
                                        }
                                    }
                                }
                            }
                        }
                    } else if ((1U & (~ ((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                         & (0x0234U 
                                            > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                        if ((1U & (~ ((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                      & (0x08b4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                            if ((1U & (~ ((0x08b4U 
                                           <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                          & (0x08c8U 
                                             > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                if ((1U & (~ ((0x08c8U 
                                               <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                              & (0x08d4U 
                                                 > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                    if ((1U & (~ ((0x0900U 
                                                   <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                  & (0x0940U 
                                                     > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_hit = 0U;
                                    }
                                }
                            }
                        }
                    }
                } else if ((1U & (~ ((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                     & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                    if ((1U & (~ ((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                  & (0x08b4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                        if ((1U & (~ ((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                      & (0x08c8U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                            if ((1U & (~ ((0x08c8U 
                                           <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                          & (0x08d4U 
                                             > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                if ((1U & (~ ((0x0900U 
                                               <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                              & (0x0940U 
                                                 > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_hit = 0U;
                                }
                            }
                        }
                    }
                }
            } else if ((1U & (~ ((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                 & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                if ((1U & (~ ((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                              & (0x08b4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                    if ((1U & (~ ((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                  & (0x08c8U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                        if ((1U & (~ ((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                      & (0x08d4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                            if ((1U & (~ ((0x0900U 
                                           <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                          & (0x0940U 
                                             > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_hit = 0U;
                            }
                        }
                    }
                }
            }
        } else if ((0x00000040U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
            if ((0x00000020U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                if ((0x00000010U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                    if ((8U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                        if ((1U & (~ ((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                      & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                            if ((1U & (~ ((0x0874U 
                                           <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                          & (0x08b4U 
                                             > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                if ((1U & (~ ((0x08b4U 
                                               <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                              & (0x08c8U 
                                                 > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                    if ((1U & (~ ((0x08c8U 
                                                   <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                  & (0x08d4U 
                                                     > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                        if ((1U & (~ 
                                                   ((0x0900U 
                                                     <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                    & (0x0940U 
                                                       > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_hit = 0U;
                                        }
                                    }
                                }
                            }
                        }
                    } else if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                        if ((1U & (~ ((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                      & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                            if ((1U & (~ ((0x0874U 
                                           <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                          & (0x08b4U 
                                             > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                if ((1U & (~ ((0x08b4U 
                                               <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                              & (0x08c8U 
                                                 > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                    if ((1U & (~ ((0x08c8U 
                                                   <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                  & (0x08d4U 
                                                     > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                        if ((1U & (~ 
                                                   ((0x0900U 
                                                     <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                    & (0x0940U 
                                                       > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_hit = 0U;
                                        }
                                    }
                                }
                            }
                        }
                    } else if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                        if ((1U & (~ ((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                      & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                            if ((1U & (~ ((0x0874U 
                                           <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                          & (0x08b4U 
                                             > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                if ((1U & (~ ((0x08b4U 
                                               <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                              & (0x08c8U 
                                                 > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                    if ((1U & (~ ((0x08c8U 
                                                   <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                  & (0x08d4U 
                                                     > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                        if ((1U & (~ 
                                                   ((0x0900U 
                                                     <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                    & (0x0940U 
                                                       > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_hit = 0U;
                                        }
                                    }
                                }
                            }
                        }
                    } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                        if ((1U & (~ ((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                      & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                            if ((1U & (~ ((0x0874U 
                                           <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                          & (0x08b4U 
                                             > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                if ((1U & (~ ((0x08b4U 
                                               <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                              & (0x08c8U 
                                                 > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                    if ((1U & (~ ((0x08c8U 
                                                   <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                  & (0x08d4U 
                                                     > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                        if ((1U & (~ 
                                                   ((0x0900U 
                                                     <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                    & (0x0940U 
                                                       > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_hit = 0U;
                                        }
                                    }
                                }
                            }
                        }
                    }
                } else if ((1U & (~ ((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                     & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                    if ((1U & (~ ((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                  & (0x08b4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                        if ((1U & (~ ((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                      & (0x08c8U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                            if ((1U & (~ ((0x08c8U 
                                           <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                          & (0x08d4U 
                                             > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                if ((1U & (~ ((0x0900U 
                                               <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                              & (0x0940U 
                                                 > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_hit = 0U;
                                }
                            }
                        }
                    }
                }
            } else if ((1U & (~ ((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                 & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                if ((1U & (~ ((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                              & (0x08b4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                    if ((1U & (~ ((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                  & (0x08c8U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                        if ((1U & (~ ((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                      & (0x08d4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                            if ((1U & (~ ((0x0900U 
                                           <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                          & (0x0940U 
                                             > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_hit = 0U;
                            }
                        }
                    }
                }
            }
        } else if ((1U & (~ ((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                             & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
            if ((1U & (~ ((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                          & (0x08b4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                if ((1U & (~ ((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                              & (0x08c8U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                    if ((1U & (~ ((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                  & (0x08d4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                        if ((1U & (~ ((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                      & (0x0940U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_hit = 0U;
                        }
                    }
                }
            }
        }
    } else if ((0x00000400U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
        if ((0x00000200U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
            if ((0x00000100U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                if ((0x00000080U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                    if ((0x00000040U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                        if ((1U & (~ ((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                      & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                            if ((1U & (~ ((0x0874U 
                                           <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                          & (0x08b4U 
                                             > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                if ((1U & (~ ((0x08b4U 
                                               <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                              & (0x08c8U 
                                                 > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                    if ((1U & (~ ((0x08c8U 
                                                   <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                  & (0x08d4U 
                                                     > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                        if ((1U & (~ 
                                                   ((0x0900U 
                                                     <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                    & (0x0940U 
                                                       > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_hit = 0U;
                                        }
                                    }
                                }
                            }
                        }
                    } else if ((0x00000020U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                        if ((0x00000010U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                            if ((8U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                                if ((1U & (~ ((0x0210U 
                                               <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                              & (0x0234U 
                                                 > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                    if ((1U & (~ ((0x0874U 
                                                   <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                  & (0x08b4U 
                                                     > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                        if ((1U & (~ 
                                                   ((0x08b4U 
                                                     <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                    & (0x08c8U 
                                                       > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                            if ((1U 
                                                 & (~ 
                                                    ((0x08c8U 
                                                      <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                     & (0x08d4U 
                                                        > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                                if (
                                                    (1U 
                                                     & (~ 
                                                        ((0x0900U 
                                                          <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                         & (0x0940U 
                                                            > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_hit = 0U;
                                                }
                                            }
                                        }
                                    }
                                }
                            } else if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                                if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                                    if ((1U & (~ ((0x0210U 
                                                   <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                  & (0x0234U 
                                                     > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                        if ((1U & (~ 
                                                   ((0x0874U 
                                                     <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                    & (0x08b4U 
                                                       > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                            if ((1U 
                                                 & (~ 
                                                    ((0x08b4U 
                                                      <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                     & (0x08c8U 
                                                        > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                                if (
                                                    (1U 
                                                     & (~ 
                                                        ((0x08c8U 
                                                          <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                         & (0x08d4U 
                                                            > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                                    if (
                                                        (1U 
                                                         & (~ 
                                                            ((0x0900U 
                                                              <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                             & (0x0940U 
                                                                > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_hit = 0U;
                                                    }
                                                }
                                            }
                                        }
                                    }
                                } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                                    if ((1U & (~ ((0x0210U 
                                                   <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                  & (0x0234U 
                                                     > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                        if ((1U & (~ 
                                                   ((0x0874U 
                                                     <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                    & (0x08b4U 
                                                       > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                            if ((1U 
                                                 & (~ 
                                                    ((0x08b4U 
                                                      <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                     & (0x08c8U 
                                                        > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                                if (
                                                    (1U 
                                                     & (~ 
                                                        ((0x08c8U 
                                                          <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                         & (0x08d4U 
                                                            > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                                    if (
                                                        (1U 
                                                         & (~ 
                                                            ((0x0900U 
                                                              <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                             & (0x0940U 
                                                                > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_hit = 0U;
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            } else if ((1U & (~ ((0x0210U 
                                                  <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                 & (0x0234U 
                                                    > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                if ((1U & (~ ((0x0874U 
                                               <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                              & (0x08b4U 
                                                 > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                    if ((1U & (~ ((0x08b4U 
                                                   <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                  & (0x08c8U 
                                                     > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                        if ((1U & (~ 
                                                   ((0x08c8U 
                                                     <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                    & (0x08d4U 
                                                       > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                            if ((1U 
                                                 & (~ 
                                                    ((0x0900U 
                                                      <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                     & (0x0940U 
                                                        > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_hit = 0U;
                                            }
                                        }
                                    }
                                }
                            }
                        } else if ((1U & (~ ((0x0210U 
                                              <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                             & (0x0234U 
                                                > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                            if ((1U & (~ ((0x0874U 
                                           <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                          & (0x08b4U 
                                             > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                if ((1U & (~ ((0x08b4U 
                                               <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                              & (0x08c8U 
                                                 > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                    if ((1U & (~ ((0x08c8U 
                                                   <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                  & (0x08d4U 
                                                     > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                        if ((1U & (~ 
                                                   ((0x0900U 
                                                     <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                    & (0x0940U 
                                                       > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_hit = 0U;
                                        }
                                    }
                                }
                            }
                        }
                    } else if ((0x00000010U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                        if ((1U & (~ ((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                      & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                            if ((1U & (~ ((0x0874U 
                                           <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                          & (0x08b4U 
                                             > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                if ((1U & (~ ((0x08b4U 
                                               <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                              & (0x08c8U 
                                                 > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                    if ((1U & (~ ((0x08c8U 
                                                   <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                  & (0x08d4U 
                                                     > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                        if ((1U & (~ 
                                                   ((0x0900U 
                                                     <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                    & (0x0940U 
                                                       > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_hit = 0U;
                                        }
                                    }
                                }
                            }
                        }
                    } else if ((8U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                        if ((1U & (~ ((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                      & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                            if ((1U & (~ ((0x0874U 
                                           <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                          & (0x08b4U 
                                             > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                if ((1U & (~ ((0x08b4U 
                                               <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                              & (0x08c8U 
                                                 > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                    if ((1U & (~ ((0x08c8U 
                                                   <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                  & (0x08d4U 
                                                     > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                        if ((1U & (~ 
                                                   ((0x0900U 
                                                     <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                    & (0x0940U 
                                                       > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_hit = 0U;
                                        }
                                    }
                                }
                            }
                        }
                    } else if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                        if ((1U & (~ ((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                      & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                            if ((1U & (~ ((0x0874U 
                                           <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                          & (0x08b4U 
                                             > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                if ((1U & (~ ((0x08b4U 
                                               <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                              & (0x08c8U 
                                                 > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                    if ((1U & (~ ((0x08c8U 
                                                   <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                  & (0x08d4U 
                                                     > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                        if ((1U & (~ 
                                                   ((0x0900U 
                                                     <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                    & (0x0940U 
                                                       > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_hit = 0U;
                                        }
                                    }
                                }
                            }
                        }
                    } else if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                        if ((1U & (~ ((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                      & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                            if ((1U & (~ ((0x0874U 
                                           <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                          & (0x08b4U 
                                             > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                if ((1U & (~ ((0x08b4U 
                                               <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                              & (0x08c8U 
                                                 > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                    if ((1U & (~ ((0x08c8U 
                                                   <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                  & (0x08d4U 
                                                     > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                        if ((1U & (~ 
                                                   ((0x0900U 
                                                     <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                    & (0x0940U 
                                                       > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_hit = 0U;
                                        }
                                    }
                                }
                            }
                        }
                    } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                        if ((1U & (~ ((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                      & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                            if ((1U & (~ ((0x0874U 
                                           <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                          & (0x08b4U 
                                             > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                if ((1U & (~ ((0x08b4U 
                                               <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                              & (0x08c8U 
                                                 > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                    if ((1U & (~ ((0x08c8U 
                                                   <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                  & (0x08d4U 
                                                     > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                        if ((1U & (~ 
                                                   ((0x0900U 
                                                     <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                    & (0x0940U 
                                                       > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_hit = 0U;
                                        }
                                    }
                                }
                            }
                        }
                    }
                } else if ((0x00000040U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                    if ((0x00000020U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                        if ((0x00000010U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                            if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                                if ((1U & (~ ((0x0210U 
                                               <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                              & (0x0234U 
                                                 > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                    if ((1U & (~ ((0x0874U 
                                                   <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                  & (0x08b4U 
                                                     > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                        if ((1U & (~ 
                                                   ((0x08b4U 
                                                     <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                    & (0x08c8U 
                                                       > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                            if ((1U 
                                                 & (~ 
                                                    ((0x08c8U 
                                                      <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                     & (0x08d4U 
                                                        > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                                if (
                                                    (1U 
                                                     & (~ 
                                                        ((0x0900U 
                                                          <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                         & (0x0940U 
                                                            > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_hit = 0U;
                                                }
                                            }
                                        }
                                    }
                                }
                            } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                                if ((1U & (~ ((0x0210U 
                                               <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                              & (0x0234U 
                                                 > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                    if ((1U & (~ ((0x0874U 
                                                   <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                  & (0x08b4U 
                                                     > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                        if ((1U & (~ 
                                                   ((0x08b4U 
                                                     <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                    & (0x08c8U 
                                                       > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                            if ((1U 
                                                 & (~ 
                                                    ((0x08c8U 
                                                      <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                     & (0x08d4U 
                                                        > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                                if (
                                                    (1U 
                                                     & (~ 
                                                        ((0x0900U 
                                                          <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                         & (0x0940U 
                                                            > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_hit = 0U;
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        } else if ((8U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                            if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                                if ((1U & (~ ((0x0210U 
                                               <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                              & (0x0234U 
                                                 > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                    if ((1U & (~ ((0x0874U 
                                                   <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                  & (0x08b4U 
                                                     > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                        if ((1U & (~ 
                                                   ((0x08b4U 
                                                     <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                    & (0x08c8U 
                                                       > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                            if ((1U 
                                                 & (~ 
                                                    ((0x08c8U 
                                                      <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                     & (0x08d4U 
                                                        > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                                if (
                                                    (1U 
                                                     & (~ 
                                                        ((0x0900U 
                                                          <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                         & (0x0940U 
                                                            > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_hit = 0U;
                                                }
                                            }
                                        }
                                    }
                                }
                            } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                                if ((1U & (~ ((0x0210U 
                                               <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                              & (0x0234U 
                                                 > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                    if ((1U & (~ ((0x0874U 
                                                   <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                  & (0x08b4U 
                                                     > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                        if ((1U & (~ 
                                                   ((0x08b4U 
                                                     <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                    & (0x08c8U 
                                                       > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                            if ((1U 
                                                 & (~ 
                                                    ((0x08c8U 
                                                      <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                     & (0x08d4U 
                                                        > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                                if (
                                                    (1U 
                                                     & (~ 
                                                        ((0x0900U 
                                                          <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                         & (0x0940U 
                                                            > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_hit = 0U;
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        } else if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                            if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                                if ((1U & (~ ((0x0210U 
                                               <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                              & (0x0234U 
                                                 > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                    if ((1U & (~ ((0x0874U 
                                                   <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                  & (0x08b4U 
                                                     > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                        if ((1U & (~ 
                                                   ((0x08b4U 
                                                     <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                    & (0x08c8U 
                                                       > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                            if ((1U 
                                                 & (~ 
                                                    ((0x08c8U 
                                                      <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                     & (0x08d4U 
                                                        > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                                if (
                                                    (1U 
                                                     & (~ 
                                                        ((0x0900U 
                                                          <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                         & (0x0940U 
                                                            > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_hit = 0U;
                                                }
                                            }
                                        }
                                    }
                                }
                            } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                                if ((1U & (~ ((0x0210U 
                                               <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                              & (0x0234U 
                                                 > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                    if ((1U & (~ ((0x0874U 
                                                   <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                  & (0x08b4U 
                                                     > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                        if ((1U & (~ 
                                                   ((0x08b4U 
                                                     <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                    & (0x08c8U 
                                                       > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                            if ((1U 
                                                 & (~ 
                                                    ((0x08c8U 
                                                      <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                     & (0x08d4U 
                                                        > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                                if (
                                                    (1U 
                                                     & (~ 
                                                        ((0x0900U 
                                                          <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                         & (0x0940U 
                                                            > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_hit = 0U;
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        } else if ((1U & (~ ((0x0210U 
                                              <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                             & (0x0234U 
                                                > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                            if ((1U & (~ ((0x0874U 
                                           <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                          & (0x08b4U 
                                             > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                if ((1U & (~ ((0x08b4U 
                                               <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                              & (0x08c8U 
                                                 > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                    if ((1U & (~ ((0x08c8U 
                                                   <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                  & (0x08d4U 
                                                     > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                        if ((1U & (~ 
                                                   ((0x0900U 
                                                     <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                    & (0x0940U 
                                                       > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_hit = 0U;
                                        }
                                    }
                                }
                            }
                        }
                    } else if ((0x00000010U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                        if ((8U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                            if ((1U & (~ ((0x0210U 
                                           <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                          & (0x0234U 
                                             > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                if ((1U & (~ ((0x0874U 
                                               <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                              & (0x08b4U 
                                                 > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                    if ((1U & (~ ((0x08b4U 
                                                   <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                  & (0x08c8U 
                                                     > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                        if ((1U & (~ 
                                                   ((0x08c8U 
                                                     <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                    & (0x08d4U 
                                                       > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                            if ((1U 
                                                 & (~ 
                                                    ((0x0900U 
                                                      <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                     & (0x0940U 
                                                        > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_hit = 0U;
                                            }
                                        }
                                    }
                                }
                            }
                        } else if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                            if ((1U & (~ ((0x0210U 
                                           <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                          & (0x0234U 
                                             > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                if ((1U & (~ ((0x0874U 
                                               <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                              & (0x08b4U 
                                                 > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                    if ((1U & (~ ((0x08b4U 
                                                   <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                  & (0x08c8U 
                                                     > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                        if ((1U & (~ 
                                                   ((0x08c8U 
                                                     <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                    & (0x08d4U 
                                                       > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                            if ((1U 
                                                 & (~ 
                                                    ((0x0900U 
                                                      <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                     & (0x0940U 
                                                        > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_hit = 0U;
                                            }
                                        }
                                    }
                                }
                            }
                        } else if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                            if ((1U & (~ ((0x0210U 
                                           <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                          & (0x0234U 
                                             > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                if ((1U & (~ ((0x0874U 
                                               <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                              & (0x08b4U 
                                                 > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                    if ((1U & (~ ((0x08b4U 
                                                   <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                  & (0x08c8U 
                                                     > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                        if ((1U & (~ 
                                                   ((0x08c8U 
                                                     <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                    & (0x08d4U 
                                                       > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                            if ((1U 
                                                 & (~ 
                                                    ((0x0900U 
                                                      <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                     & (0x0940U 
                                                        > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_hit = 0U;
                                            }
                                        }
                                    }
                                }
                            }
                        } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                            if ((1U & (~ ((0x0210U 
                                           <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                          & (0x0234U 
                                             > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                if ((1U & (~ ((0x0874U 
                                               <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                              & (0x08b4U 
                                                 > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                    if ((1U & (~ ((0x08b4U 
                                                   <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                  & (0x08c8U 
                                                     > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                        if ((1U & (~ 
                                                   ((0x08c8U 
                                                     <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                    & (0x08d4U 
                                                       > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                            if ((1U 
                                                 & (~ 
                                                    ((0x0900U 
                                                      <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                     & (0x0940U 
                                                        > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_hit = 0U;
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    } else if ((8U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                        if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                            if ((1U & (~ ((0x0210U 
                                           <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                          & (0x0234U 
                                             > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                if ((1U & (~ ((0x0874U 
                                               <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                              & (0x08b4U 
                                                 > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                    if ((1U & (~ ((0x08b4U 
                                                   <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                  & (0x08c8U 
                                                     > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                        if ((1U & (~ 
                                                   ((0x08c8U 
                                                     <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                    & (0x08d4U 
                                                       > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                            if ((1U 
                                                 & (~ 
                                                    ((0x0900U 
                                                      <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                     & (0x0940U 
                                                        > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_hit = 0U;
                                            }
                                        }
                                    }
                                }
                            }
                        } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                            if ((1U & (~ ((0x0210U 
                                           <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                          & (0x0234U 
                                             > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                if ((1U & (~ ((0x0874U 
                                               <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                              & (0x08b4U 
                                                 > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                    if ((1U & (~ ((0x08b4U 
                                                   <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                  & (0x08c8U 
                                                     > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                        if ((1U & (~ 
                                                   ((0x08c8U 
                                                     <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                    & (0x08d4U 
                                                       > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                            if ((1U 
                                                 & (~ 
                                                    ((0x0900U 
                                                      <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                     & (0x0940U 
                                                        > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_hit = 0U;
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    } else if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                        if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                            if ((1U & (~ ((0x0210U 
                                           <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                          & (0x0234U 
                                             > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                if ((1U & (~ ((0x0874U 
                                               <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                              & (0x08b4U 
                                                 > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                    if ((1U & (~ ((0x08b4U 
                                                   <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                  & (0x08c8U 
                                                     > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                        if ((1U & (~ 
                                                   ((0x08c8U 
                                                     <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                    & (0x08d4U 
                                                       > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                            if ((1U 
                                                 & (~ 
                                                    ((0x0900U 
                                                      <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                     & (0x0940U 
                                                        > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_hit = 0U;
                                            }
                                        }
                                    }
                                }
                            }
                        } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                            if ((1U & (~ ((0x0210U 
                                           <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                          & (0x0234U 
                                             > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                if ((1U & (~ ((0x0874U 
                                               <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                              & (0x08b4U 
                                                 > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                    if ((1U & (~ ((0x08b4U 
                                                   <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                  & (0x08c8U 
                                                     > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                        if ((1U & (~ 
                                                   ((0x08c8U 
                                                     <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                    & (0x08d4U 
                                                       > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                            if ((1U 
                                                 & (~ 
                                                    ((0x0900U 
                                                      <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                     & (0x0940U 
                                                        > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_hit = 0U;
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    } else if ((1U & (~ ((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                         & (0x0234U 
                                            > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                        if ((1U & (~ ((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                      & (0x08b4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                            if ((1U & (~ ((0x08b4U 
                                           <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                          & (0x08c8U 
                                             > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                if ((1U & (~ ((0x08c8U 
                                               <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                              & (0x08d4U 
                                                 > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                    if ((1U & (~ ((0x0900U 
                                                   <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                  & (0x0940U 
                                                     > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_hit = 0U;
                                    }
                                }
                            }
                        }
                    }
                } else if ((0x00000020U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                    if ((0x00000010U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                        if ((8U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                            if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                                if ((1U & (~ ((0x0210U 
                                               <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                              & (0x0234U 
                                                 > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                    if ((1U & (~ ((0x0874U 
                                                   <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                  & (0x08b4U 
                                                     > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                        if ((1U & (~ 
                                                   ((0x08b4U 
                                                     <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                    & (0x08c8U 
                                                       > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                            if ((1U 
                                                 & (~ 
                                                    ((0x08c8U 
                                                      <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                     & (0x08d4U 
                                                        > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                                if (
                                                    (1U 
                                                     & (~ 
                                                        ((0x0900U 
                                                          <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                         & (0x0940U 
                                                            > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_hit = 0U;
                                                }
                                            }
                                        }
                                    }
                                }
                            } else if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                                if ((1U & (~ ((0x0210U 
                                               <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                              & (0x0234U 
                                                 > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                    if ((1U & (~ ((0x0874U 
                                                   <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                  & (0x08b4U 
                                                     > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                        if ((1U & (~ 
                                                   ((0x08b4U 
                                                     <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                    & (0x08c8U 
                                                       > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                            if ((1U 
                                                 & (~ 
                                                    ((0x08c8U 
                                                      <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                     & (0x08d4U 
                                                        > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                                if (
                                                    (1U 
                                                     & (~ 
                                                        ((0x0900U 
                                                          <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                         & (0x0940U 
                                                            > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_hit = 0U;
                                                }
                                            }
                                        }
                                    }
                                }
                            } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                                if ((1U & (~ ((0x0210U 
                                               <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                              & (0x0234U 
                                                 > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                    if ((1U & (~ ((0x0874U 
                                                   <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                  & (0x08b4U 
                                                     > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                        if ((1U & (~ 
                                                   ((0x08b4U 
                                                     <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                    & (0x08c8U 
                                                       > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                            if ((1U 
                                                 & (~ 
                                                    ((0x08c8U 
                                                      <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                     & (0x08d4U 
                                                        > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                                if (
                                                    (1U 
                                                     & (~ 
                                                        ((0x0900U 
                                                          <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                         & (0x0940U 
                                                            > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_hit = 0U;
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        } else if ((1U & (~ ((0x0210U 
                                              <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                             & (0x0234U 
                                                > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                            if ((1U & (~ ((0x0874U 
                                           <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                          & (0x08b4U 
                                             > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                if ((1U & (~ ((0x08b4U 
                                               <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                              & (0x08c8U 
                                                 > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                    if ((1U & (~ ((0x08c8U 
                                                   <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                  & (0x08d4U 
                                                     > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                        if ((1U & (~ 
                                                   ((0x0900U 
                                                     <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                    & (0x0940U 
                                                       > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_hit = 0U;
                                        }
                                    }
                                }
                            }
                        }
                    } else if ((8U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                        if ((1U & (~ ((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                      & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                            if ((1U & (~ ((0x0874U 
                                           <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                          & (0x08b4U 
                                             > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                if ((1U & (~ ((0x08b4U 
                                               <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                              & (0x08c8U 
                                                 > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                    if ((1U & (~ ((0x08c8U 
                                                   <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                  & (0x08d4U 
                                                     > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                        if ((1U & (~ 
                                                   ((0x0900U 
                                                     <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                    & (0x0940U 
                                                       > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_hit = 0U;
                                        }
                                    }
                                }
                            }
                        }
                    } else if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                        if ((1U & (~ ((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                      & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                            if ((1U & (~ ((0x0874U 
                                           <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                          & (0x08b4U 
                                             > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                if ((1U & (~ ((0x08b4U 
                                               <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                              & (0x08c8U 
                                                 > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                    if ((1U & (~ ((0x08c8U 
                                                   <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                  & (0x08d4U 
                                                     > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                        if ((1U & (~ 
                                                   ((0x0900U 
                                                     <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                    & (0x0940U 
                                                       > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_hit = 0U;
                                        }
                                    }
                                }
                            }
                        }
                    } else if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                        if ((1U & (~ ((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                      & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                            if ((1U & (~ ((0x0874U 
                                           <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                          & (0x08b4U 
                                             > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                if ((1U & (~ ((0x08b4U 
                                               <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                              & (0x08c8U 
                                                 > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                    if ((1U & (~ ((0x08c8U 
                                                   <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                  & (0x08d4U 
                                                     > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                        if ((1U & (~ 
                                                   ((0x0900U 
                                                     <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                    & (0x0940U 
                                                       > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_hit = 0U;
                                        }
                                    }
                                }
                            }
                        }
                    } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                        if ((1U & (~ ((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                      & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                            if ((1U & (~ ((0x0874U 
                                           <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                          & (0x08b4U 
                                             > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                if ((1U & (~ ((0x08b4U 
                                               <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                              & (0x08c8U 
                                                 > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                    if ((1U & (~ ((0x08c8U 
                                                   <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                  & (0x08d4U 
                                                     > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                        if ((1U & (~ 
                                                   ((0x0900U 
                                                     <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                    & (0x0940U 
                                                       > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_hit = 0U;
                                        }
                                    }
                                }
                            }
                        }
                    }
                } else if ((1U & (~ ((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                     & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                    if ((1U & (~ ((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                  & (0x08b4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                        if ((1U & (~ ((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                      & (0x08c8U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                            if ((1U & (~ ((0x08c8U 
                                           <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                          & (0x08d4U 
                                             > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                if ((1U & (~ ((0x0900U 
                                               <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                              & (0x0940U 
                                                 > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_hit = 0U;
                                }
                            }
                        }
                    }
                }
            } else if ((0x00000080U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                if ((0x00000040U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                    if ((0x00000020U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                        if ((0x00000010U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                            if ((8U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                                if ((1U & (~ ((0x0210U 
                                               <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                              & (0x0234U 
                                                 > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                    if ((1U & (~ ((0x0874U 
                                                   <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                  & (0x08b4U 
                                                     > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                        if ((1U & (~ 
                                                   ((0x08b4U 
                                                     <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                    & (0x08c8U 
                                                       > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                            if ((1U 
                                                 & (~ 
                                                    ((0x08c8U 
                                                      <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                     & (0x08d4U 
                                                        > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                                if (
                                                    (1U 
                                                     & (~ 
                                                        ((0x0900U 
                                                          <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                         & (0x0940U 
                                                            > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_hit = 0U;
                                                }
                                            }
                                        }
                                    }
                                }
                            } else if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                                if ((1U & (~ ((0x0210U 
                                               <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                              & (0x0234U 
                                                 > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                    if ((1U & (~ ((0x0874U 
                                                   <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                  & (0x08b4U 
                                                     > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                        if ((1U & (~ 
                                                   ((0x08b4U 
                                                     <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                    & (0x08c8U 
                                                       > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                            if ((1U 
                                                 & (~ 
                                                    ((0x08c8U 
                                                      <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                     & (0x08d4U 
                                                        > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                                if (
                                                    (1U 
                                                     & (~ 
                                                        ((0x0900U 
                                                          <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                         & (0x0940U 
                                                            > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_hit = 0U;
                                                }
                                            }
                                        }
                                    }
                                }
                            } else if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                                if ((1U & (~ ((0x0210U 
                                               <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                              & (0x0234U 
                                                 > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                    if ((1U & (~ ((0x0874U 
                                                   <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                  & (0x08b4U 
                                                     > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                        if ((1U & (~ 
                                                   ((0x08b4U 
                                                     <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                    & (0x08c8U 
                                                       > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                            if ((1U 
                                                 & (~ 
                                                    ((0x08c8U 
                                                      <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                     & (0x08d4U 
                                                        > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                                if (
                                                    (1U 
                                                     & (~ 
                                                        ((0x0900U 
                                                          <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                         & (0x0940U 
                                                            > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_hit = 0U;
                                                }
                                            }
                                        }
                                    }
                                }
                            } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                                if ((1U & (~ ((0x0210U 
                                               <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                              & (0x0234U 
                                                 > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                    if ((1U & (~ ((0x0874U 
                                                   <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                  & (0x08b4U 
                                                     > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                        if ((1U & (~ 
                                                   ((0x08b4U 
                                                     <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                    & (0x08c8U 
                                                       > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                            if ((1U 
                                                 & (~ 
                                                    ((0x08c8U 
                                                      <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                     & (0x08d4U 
                                                        > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                                if (
                                                    (1U 
                                                     & (~ 
                                                        ((0x0900U 
                                                          <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                         & (0x0940U 
                                                            > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_hit = 0U;
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        } else if ((8U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                            if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                                if ((1U & (~ ((0x0210U 
                                               <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                              & (0x0234U 
                                                 > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                    if ((1U & (~ ((0x0874U 
                                                   <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                  & (0x08b4U 
                                                     > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                        if ((1U & (~ 
                                                   ((0x08b4U 
                                                     <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                    & (0x08c8U 
                                                       > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                            if ((1U 
                                                 & (~ 
                                                    ((0x08c8U 
                                                      <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                     & (0x08d4U 
                                                        > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                                if (
                                                    (1U 
                                                     & (~ 
                                                        ((0x0900U 
                                                          <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                         & (0x0940U 
                                                            > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_hit = 0U;
                                                }
                                            }
                                        }
                                    }
                                }
                            } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                                if ((1U & (~ ((0x0210U 
                                               <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                              & (0x0234U 
                                                 > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                    if ((1U & (~ ((0x0874U 
                                                   <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                  & (0x08b4U 
                                                     > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                        if ((1U & (~ 
                                                   ((0x08b4U 
                                                     <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                    & (0x08c8U 
                                                       > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                            if ((1U 
                                                 & (~ 
                                                    ((0x08c8U 
                                                      <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                     & (0x08d4U 
                                                        > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                                if (
                                                    (1U 
                                                     & (~ 
                                                        ((0x0900U 
                                                          <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                         & (0x0940U 
                                                            > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_hit = 0U;
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        } else if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                            if ((1U & (~ ((0x0210U 
                                           <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                          & (0x0234U 
                                             > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                if ((1U & (~ ((0x0874U 
                                               <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                              & (0x08b4U 
                                                 > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                    if ((1U & (~ ((0x08b4U 
                                                   <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                  & (0x08c8U 
                                                     > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                        if ((1U & (~ 
                                                   ((0x08c8U 
                                                     <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                    & (0x08d4U 
                                                       > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                            if ((1U 
                                                 & (~ 
                                                    ((0x0900U 
                                                      <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                     & (0x0940U 
                                                        > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_hit = 0U;
                                            }
                                        }
                                    }
                                }
                            }
                        } else if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                            if ((1U & (~ ((0x0210U 
                                           <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                          & (0x0234U 
                                             > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                if ((1U & (~ ((0x0874U 
                                               <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                              & (0x08b4U 
                                                 > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                    if ((1U & (~ ((0x08b4U 
                                                   <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                  & (0x08c8U 
                                                     > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                        if ((1U & (~ 
                                                   ((0x08c8U 
                                                     <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                    & (0x08d4U 
                                                       > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                            if ((1U 
                                                 & (~ 
                                                    ((0x0900U 
                                                      <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                     & (0x0940U 
                                                        > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_hit = 0U;
                                            }
                                        }
                                    }
                                }
                            }
                        } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                            if ((1U & (~ ((0x0210U 
                                           <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                          & (0x0234U 
                                             > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                if ((1U & (~ ((0x0874U 
                                               <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                              & (0x08b4U 
                                                 > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                    if ((1U & (~ ((0x08b4U 
                                                   <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                  & (0x08c8U 
                                                     > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                        if ((1U & (~ 
                                                   ((0x08c8U 
                                                     <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                    & (0x08d4U 
                                                       > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                            if ((1U 
                                                 & (~ 
                                                    ((0x0900U 
                                                      <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                     & (0x0940U 
                                                        > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_hit = 0U;
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    } else if ((8U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                        if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                            if ((1U & (~ ((0x0210U 
                                           <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                          & (0x0234U 
                                             > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                if ((1U & (~ ((0x0874U 
                                               <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                              & (0x08b4U 
                                                 > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                    if ((1U & (~ ((0x08b4U 
                                                   <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                  & (0x08c8U 
                                                     > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                        if ((1U & (~ 
                                                   ((0x08c8U 
                                                     <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                    & (0x08d4U 
                                                       > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                            if ((1U 
                                                 & (~ 
                                                    ((0x0900U 
                                                      <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                     & (0x0940U 
                                                        > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_hit = 0U;
                                            }
                                        }
                                    }
                                }
                            }
                        } else if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                            if ((1U & (~ ((0x0210U 
                                           <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                          & (0x0234U 
                                             > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                if ((1U & (~ ((0x0874U 
                                               <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                              & (0x08b4U 
                                                 > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                    if ((1U & (~ ((0x08b4U 
                                                   <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                  & (0x08c8U 
                                                     > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                        if ((1U & (~ 
                                                   ((0x08c8U 
                                                     <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                    & (0x08d4U 
                                                       > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                            if ((1U 
                                                 & (~ 
                                                    ((0x0900U 
                                                      <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                     & (0x0940U 
                                                        > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_hit = 0U;
                                            }
                                        }
                                    }
                                }
                            }
                        } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                            if ((1U & (~ ((0x0210U 
                                           <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                          & (0x0234U 
                                             > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                if ((1U & (~ ((0x0874U 
                                               <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                              & (0x08b4U 
                                                 > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                    if ((1U & (~ ((0x08b4U 
                                                   <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                  & (0x08c8U 
                                                     > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                        if ((1U & (~ 
                                                   ((0x08c8U 
                                                     <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                    & (0x08d4U 
                                                       > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                            if ((1U 
                                                 & (~ 
                                                    ((0x0900U 
                                                      <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                     & (0x0940U 
                                                        > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_hit = 0U;
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    } else if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                        if ((1U & (~ ((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                      & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                            if ((1U & (~ ((0x0874U 
                                           <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                          & (0x08b4U 
                                             > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                if ((1U & (~ ((0x08b4U 
                                               <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                              & (0x08c8U 
                                                 > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                    if ((1U & (~ ((0x08c8U 
                                                   <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                  & (0x08d4U 
                                                     > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                        if ((1U & (~ 
                                                   ((0x0900U 
                                                     <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                    & (0x0940U 
                                                       > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_hit = 0U;
                                        }
                                    }
                                }
                            }
                        }
                    } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                        if ((1U & (~ ((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                      & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                            if ((1U & (~ ((0x0874U 
                                           <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                          & (0x08b4U 
                                             > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                if ((1U & (~ ((0x08b4U 
                                               <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                              & (0x08c8U 
                                                 > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                    if ((1U & (~ ((0x08c8U 
                                                   <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                  & (0x08d4U 
                                                     > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                        if ((1U & (~ 
                                                   ((0x0900U 
                                                     <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                    & (0x0940U 
                                                       > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_hit = 0U;
                                        }
                                    }
                                }
                            }
                        }
                    }
                } else if ((0x00000020U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                    if ((0x00000010U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                        if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                            if ((1U & (~ ((0x0210U 
                                           <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                          & (0x0234U 
                                             > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                if ((1U & (~ ((0x0874U 
                                               <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                              & (0x08b4U 
                                                 > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                    if ((1U & (~ ((0x08b4U 
                                                   <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                  & (0x08c8U 
                                                     > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                        if ((1U & (~ 
                                                   ((0x08c8U 
                                                     <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                    & (0x08d4U 
                                                       > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                            if ((1U 
                                                 & (~ 
                                                    ((0x0900U 
                                                      <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                     & (0x0940U 
                                                        > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_hit = 0U;
                                            }
                                        }
                                    }
                                }
                            }
                        } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                            if ((1U & (~ ((0x0210U 
                                           <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                          & (0x0234U 
                                             > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                if ((1U & (~ ((0x0874U 
                                               <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                              & (0x08b4U 
                                                 > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                    if ((1U & (~ ((0x08b4U 
                                                   <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                  & (0x08c8U 
                                                     > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                        if ((1U & (~ 
                                                   ((0x08c8U 
                                                     <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                    & (0x08d4U 
                                                       > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                            if ((1U 
                                                 & (~ 
                                                    ((0x0900U 
                                                      <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                     & (0x0940U 
                                                        > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_hit = 0U;
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    } else if ((8U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                        if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                            if ((1U & (~ ((0x0210U 
                                           <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                          & (0x0234U 
                                             > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                if ((1U & (~ ((0x0874U 
                                               <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                              & (0x08b4U 
                                                 > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                    if ((1U & (~ ((0x08b4U 
                                                   <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                  & (0x08c8U 
                                                     > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                        if ((1U & (~ 
                                                   ((0x08c8U 
                                                     <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                    & (0x08d4U 
                                                       > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                            if ((1U 
                                                 & (~ 
                                                    ((0x0900U 
                                                      <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                     & (0x0940U 
                                                        > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_hit = 0U;
                                            }
                                        }
                                    }
                                }
                            }
                        } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                            if ((1U & (~ ((0x0210U 
                                           <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                          & (0x0234U 
                                             > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                if ((1U & (~ ((0x0874U 
                                               <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                              & (0x08b4U 
                                                 > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                    if ((1U & (~ ((0x08b4U 
                                                   <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                  & (0x08c8U 
                                                     > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                        if ((1U & (~ 
                                                   ((0x08c8U 
                                                     <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                    & (0x08d4U 
                                                       > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                            if ((1U 
                                                 & (~ 
                                                    ((0x0900U 
                                                      <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                     & (0x0940U 
                                                        > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_hit = 0U;
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    } else if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                        if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                            if ((1U & (~ ((0x0210U 
                                           <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                          & (0x0234U 
                                             > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                if ((1U & (~ ((0x0874U 
                                               <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                              & (0x08b4U 
                                                 > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                    if ((1U & (~ ((0x08b4U 
                                                   <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                  & (0x08c8U 
                                                     > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                        if ((1U & (~ 
                                                   ((0x08c8U 
                                                     <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                    & (0x08d4U 
                                                       > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                            if ((1U 
                                                 & (~ 
                                                    ((0x0900U 
                                                      <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                     & (0x0940U 
                                                        > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_hit = 0U;
                                            }
                                        }
                                    }
                                }
                            }
                        } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                            if ((1U & (~ ((0x0210U 
                                           <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                          & (0x0234U 
                                             > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                if ((1U & (~ ((0x0874U 
                                               <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                              & (0x08b4U 
                                                 > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                    if ((1U & (~ ((0x08b4U 
                                                   <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                  & (0x08c8U 
                                                     > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                        if ((1U & (~ 
                                                   ((0x08c8U 
                                                     <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                    & (0x08d4U 
                                                       > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                            if ((1U 
                                                 & (~ 
                                                    ((0x0900U 
                                                      <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                     & (0x0940U 
                                                        > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_hit = 0U;
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    } else if ((1U & (~ ((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                         & (0x0234U 
                                            > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                        if ((1U & (~ ((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                      & (0x08b4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                            if ((1U & (~ ((0x08b4U 
                                           <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                          & (0x08c8U 
                                             > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                if ((1U & (~ ((0x08c8U 
                                               <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                              & (0x08d4U 
                                                 > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                    if ((1U & (~ ((0x0900U 
                                                   <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                  & (0x0940U 
                                                     > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_hit = 0U;
                                    }
                                }
                            }
                        }
                    }
                } else if ((0x00000010U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                    if ((8U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                        if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                            if ((1U & (~ ((0x0210U 
                                           <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                          & (0x0234U 
                                             > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                if ((1U & (~ ((0x0874U 
                                               <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                              & (0x08b4U 
                                                 > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                    if ((1U & (~ ((0x08b4U 
                                                   <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                  & (0x08c8U 
                                                     > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                        if ((1U & (~ 
                                                   ((0x08c8U 
                                                     <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                    & (0x08d4U 
                                                       > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                            if ((1U 
                                                 & (~ 
                                                    ((0x0900U 
                                                      <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                     & (0x0940U 
                                                        > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_hit = 0U;
                                            }
                                        }
                                    }
                                }
                            }
                        } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                            if ((1U & (~ ((0x0210U 
                                           <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                          & (0x0234U 
                                             > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                if ((1U & (~ ((0x0874U 
                                               <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                              & (0x08b4U 
                                                 > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                    if ((1U & (~ ((0x08b4U 
                                                   <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                  & (0x08c8U 
                                                     > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                        if ((1U & (~ 
                                                   ((0x08c8U 
                                                     <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                    & (0x08d4U 
                                                       > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                            if ((1U 
                                                 & (~ 
                                                    ((0x0900U 
                                                      <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                     & (0x0940U 
                                                        > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_hit = 0U;
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    } else if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                        if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                            if ((1U & (~ ((0x0210U 
                                           <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                          & (0x0234U 
                                             > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                if ((1U & (~ ((0x0874U 
                                               <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                              & (0x08b4U 
                                                 > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                    if ((1U & (~ ((0x08b4U 
                                                   <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                  & (0x08c8U 
                                                     > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                        if ((1U & (~ 
                                                   ((0x08c8U 
                                                     <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                    & (0x08d4U 
                                                       > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                            if ((1U 
                                                 & (~ 
                                                    ((0x0900U 
                                                      <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                     & (0x0940U 
                                                        > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_hit = 0U;
                                            }
                                        }
                                    }
                                }
                            }
                        } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                            if ((1U & (~ ((0x0210U 
                                           <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                          & (0x0234U 
                                             > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                if ((1U & (~ ((0x0874U 
                                               <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                              & (0x08b4U 
                                                 > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                    if ((1U & (~ ((0x08b4U 
                                                   <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                  & (0x08c8U 
                                                     > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                        if ((1U & (~ 
                                                   ((0x08c8U 
                                                     <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                    & (0x08d4U 
                                                       > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                            if ((1U 
                                                 & (~ 
                                                    ((0x0900U 
                                                      <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                     & (0x0940U 
                                                        > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_hit = 0U;
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    } else if ((1U & (~ ((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                         & (0x0234U 
                                            > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                        if ((1U & (~ ((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                      & (0x08b4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                            if ((1U & (~ ((0x08b4U 
                                           <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                          & (0x08c8U 
                                             > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                if ((1U & (~ ((0x08c8U 
                                               <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                              & (0x08d4U 
                                                 > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                    if ((1U & (~ ((0x0900U 
                                                   <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                  & (0x0940U 
                                                     > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_hit = 0U;
                                    }
                                }
                            }
                        }
                    }
                } else if ((1U & (~ ((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                     & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                    if ((1U & (~ ((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                  & (0x08b4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                        if ((1U & (~ ((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                      & (0x08c8U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                            if ((1U & (~ ((0x08c8U 
                                           <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                          & (0x08d4U 
                                             > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                if ((1U & (~ ((0x0900U 
                                               <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                              & (0x0940U 
                                                 > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_hit = 0U;
                                }
                            }
                        }
                    }
                }
            } else if ((0x00000040U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                if ((0x00000020U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                    if ((0x00000010U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                        if ((1U & (~ ((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                      & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                            if ((1U & (~ ((0x0874U 
                                           <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                          & (0x08b4U 
                                             > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                if ((1U & (~ ((0x08b4U 
                                               <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                              & (0x08c8U 
                                                 > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                    if ((1U & (~ ((0x08c8U 
                                                   <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                  & (0x08d4U 
                                                     > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                        if ((1U & (~ 
                                                   ((0x0900U 
                                                     <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                    & (0x0940U 
                                                       > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_hit = 0U;
                                        }
                                    }
                                }
                            }
                        }
                    } else if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                        if ((1U & (~ ((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                      & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                            if ((1U & (~ ((0x0874U 
                                           <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                          & (0x08b4U 
                                             > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                if ((1U & (~ ((0x08b4U 
                                               <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                              & (0x08c8U 
                                                 > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                    if ((1U & (~ ((0x08c8U 
                                                   <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                  & (0x08d4U 
                                                     > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                        if ((1U & (~ 
                                                   ((0x0900U 
                                                     <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                    & (0x0940U 
                                                       > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_hit = 0U;
                                        }
                                    }
                                }
                            }
                        }
                    } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                        if ((1U & (~ ((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                      & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                            if ((1U & (~ ((0x0874U 
                                           <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                          & (0x08b4U 
                                             > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                if ((1U & (~ ((0x08b4U 
                                               <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                              & (0x08c8U 
                                                 > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                    if ((1U & (~ ((0x08c8U 
                                                   <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                  & (0x08d4U 
                                                     > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                        if ((1U & (~ 
                                                   ((0x0900U 
                                                     <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                    & (0x0940U 
                                                       > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_hit = 0U;
                                        }
                                    }
                                }
                            }
                        }
                    }
                } else if ((0x00000010U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                    if ((8U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                        if ((1U & (~ ((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                      & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                            if ((1U & (~ ((0x0874U 
                                           <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                          & (0x08b4U 
                                             > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                if ((1U & (~ ((0x08b4U 
                                               <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                              & (0x08c8U 
                                                 > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                    if ((1U & (~ ((0x08c8U 
                                                   <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                  & (0x08d4U 
                                                     > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                        if ((1U & (~ 
                                                   ((0x0900U 
                                                     <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                    & (0x0940U 
                                                       > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_hit = 0U;
                                        }
                                    }
                                }
                            }
                        }
                    } else if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                        if ((1U & (~ ((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                      & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                            if ((1U & (~ ((0x0874U 
                                           <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                          & (0x08b4U 
                                             > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                if ((1U & (~ ((0x08b4U 
                                               <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                              & (0x08c8U 
                                                 > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                    if ((1U & (~ ((0x08c8U 
                                                   <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                  & (0x08d4U 
                                                     > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                        if ((1U & (~ 
                                                   ((0x0900U 
                                                     <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                    & (0x0940U 
                                                       > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_hit = 0U;
                                        }
                                    }
                                }
                            }
                        }
                    } else if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                        if ((1U & (~ ((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                      & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                            if ((1U & (~ ((0x0874U 
                                           <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                          & (0x08b4U 
                                             > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                if ((1U & (~ ((0x08b4U 
                                               <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                              & (0x08c8U 
                                                 > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                    if ((1U & (~ ((0x08c8U 
                                                   <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                  & (0x08d4U 
                                                     > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                        if ((1U & (~ 
                                                   ((0x0900U 
                                                     <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                    & (0x0940U 
                                                       > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_hit = 0U;
                                        }
                                    }
                                }
                            }
                        }
                    } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                        if ((1U & (~ ((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                      & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                            if ((1U & (~ ((0x0874U 
                                           <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                          & (0x08b4U 
                                             > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                if ((1U & (~ ((0x08b4U 
                                               <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                              & (0x08c8U 
                                                 > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                    if ((1U & (~ ((0x08c8U 
                                                   <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                  & (0x08d4U 
                                                     > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                        if ((1U & (~ 
                                                   ((0x0900U 
                                                     <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                    & (0x0940U 
                                                       > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_hit = 0U;
                                        }
                                    }
                                }
                            }
                        }
                    }
                } else if ((8U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                    if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                        if ((1U & (~ ((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                      & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                            if ((1U & (~ ((0x0874U 
                                           <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                          & (0x08b4U 
                                             > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                if ((1U & (~ ((0x08b4U 
                                               <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                              & (0x08c8U 
                                                 > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                    if ((1U & (~ ((0x08c8U 
                                                   <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                  & (0x08d4U 
                                                     > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                        if ((1U & (~ 
                                                   ((0x0900U 
                                                     <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                    & (0x0940U 
                                                       > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_hit = 0U;
                                        }
                                    }
                                }
                            }
                        }
                    } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                        if ((1U & (~ ((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                      & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                            if ((1U & (~ ((0x0874U 
                                           <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                          & (0x08b4U 
                                             > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                if ((1U & (~ ((0x08b4U 
                                               <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                              & (0x08c8U 
                                                 > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                    if ((1U & (~ ((0x08c8U 
                                                   <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                  & (0x08d4U 
                                                     > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                        if ((1U & (~ 
                                                   ((0x0900U 
                                                     <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                    & (0x0940U 
                                                       > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_hit = 0U;
                                        }
                                    }
                                }
                            }
                        }
                    }
                } else if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                    if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                        if ((1U & (~ ((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                      & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                            if ((1U & (~ ((0x0874U 
                                           <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                          & (0x08b4U 
                                             > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                if ((1U & (~ ((0x08b4U 
                                               <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                              & (0x08c8U 
                                                 > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                    if ((1U & (~ ((0x08c8U 
                                                   <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                  & (0x08d4U 
                                                     > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                        if ((1U & (~ 
                                                   ((0x0900U 
                                                     <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                    & (0x0940U 
                                                       > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_hit = 0U;
                                        }
                                    }
                                }
                            }
                        }
                    } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                        if ((1U & (~ ((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                      & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                            if ((1U & (~ ((0x0874U 
                                           <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                          & (0x08b4U 
                                             > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                if ((1U & (~ ((0x08b4U 
                                               <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                              & (0x08c8U 
                                                 > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                    if ((1U & (~ ((0x08c8U 
                                                   <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                  & (0x08d4U 
                                                     > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                        if ((1U & (~ 
                                                   ((0x0900U 
                                                     <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                    & (0x0940U 
                                                       > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_hit = 0U;
                                        }
                                    }
                                }
                            }
                        }
                    }
                } else if ((1U & (~ ((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                     & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                    if ((1U & (~ ((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                  & (0x08b4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                        if ((1U & (~ ((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                      & (0x08c8U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                            if ((1U & (~ ((0x08c8U 
                                           <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                          & (0x08d4U 
                                             > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                if ((1U & (~ ((0x0900U 
                                               <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                              & (0x0940U 
                                                 > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_hit = 0U;
                                }
                            }
                        }
                    }
                }
            } else if ((1U & (~ ((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                 & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                if ((1U & (~ ((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                              & (0x08b4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                    if ((1U & (~ ((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                  & (0x08c8U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                        if ((1U & (~ ((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                      & (0x08d4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                            if ((1U & (~ ((0x0900U 
                                           <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                          & (0x0940U 
                                             > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_hit = 0U;
                            }
                        }
                    }
                }
            }
        } else if ((0x00000100U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
            if ((0x00000080U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                if ((1U & (~ ((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                              & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                    if ((1U & (~ ((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                  & (0x08b4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                        if ((1U & (~ ((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                      & (0x08c8U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                            if ((1U & (~ ((0x08c8U 
                                           <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                          & (0x08d4U 
                                             > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                if ((1U & (~ ((0x0900U 
                                               <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                              & (0x0940U 
                                                 > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_hit = 0U;
                                }
                            }
                        }
                    }
                }
            } else if ((0x00000040U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                if ((1U & (~ ((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                              & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                    if ((1U & (~ ((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                  & (0x08b4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                        if ((1U & (~ ((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                      & (0x08c8U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                            if ((1U & (~ ((0x08c8U 
                                           <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                          & (0x08d4U 
                                             > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                if ((1U & (~ ((0x0900U 
                                               <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                              & (0x0940U 
                                                 > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_hit = 0U;
                                }
                            }
                        }
                    }
                }
            } else if ((0x00000020U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                if ((0x00000010U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                    if ((8U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                        if ((1U & (~ ((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                      & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                            if ((1U & (~ ((0x0874U 
                                           <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                          & (0x08b4U 
                                             > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                if ((1U & (~ ((0x08b4U 
                                               <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                              & (0x08c8U 
                                                 > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                    if ((1U & (~ ((0x08c8U 
                                                   <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                  & (0x08d4U 
                                                     > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                        if ((1U & (~ 
                                                   ((0x0900U 
                                                     <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                    & (0x0940U 
                                                       > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_hit = 0U;
                                        }
                                    }
                                }
                            }
                        }
                    } else if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                        if ((1U & (~ ((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                      & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                            if ((1U & (~ ((0x0874U 
                                           <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                          & (0x08b4U 
                                             > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                if ((1U & (~ ((0x08b4U 
                                               <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                              & (0x08c8U 
                                                 > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                    if ((1U & (~ ((0x08c8U 
                                                   <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                  & (0x08d4U 
                                                     > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                        if ((1U & (~ 
                                                   ((0x0900U 
                                                     <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                    & (0x0940U 
                                                       > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_hit = 0U;
                                        }
                                    }
                                }
                            }
                        }
                    } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                        if ((1U & (~ ((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                      & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                            if ((1U & (~ ((0x0874U 
                                           <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                          & (0x08b4U 
                                             > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                if ((1U & (~ ((0x08b4U 
                                               <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                              & (0x08c8U 
                                                 > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                    if ((1U & (~ ((0x08c8U 
                                                   <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                  & (0x08d4U 
                                                     > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                        if ((1U & (~ 
                                                   ((0x0900U 
                                                     <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                    & (0x0940U 
                                                       > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_hit = 0U;
                                        }
                                    }
                                }
                            }
                        }
                    }
                } else if ((1U & (~ ((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                     & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                    if ((1U & (~ ((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                  & (0x08b4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                        if ((1U & (~ ((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                      & (0x08c8U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                            if ((1U & (~ ((0x08c8U 
                                           <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                          & (0x08d4U 
                                             > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                if ((1U & (~ ((0x0900U 
                                               <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                              & (0x0940U 
                                                 > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_hit = 0U;
                                }
                            }
                        }
                    }
                }
            } else if ((1U & (~ ((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                 & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                if ((1U & (~ ((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                              & (0x08b4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                    if ((1U & (~ ((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                  & (0x08c8U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                        if ((1U & (~ ((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                      & (0x08d4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                            if ((1U & (~ ((0x0900U 
                                           <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                          & (0x0940U 
                                             > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_hit = 0U;
                            }
                        }
                    }
                }
            }
        } else if ((1U & (~ ((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                             & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
            if ((1U & (~ ((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                          & (0x08b4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                if ((1U & (~ ((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                              & (0x08c8U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                    if ((1U & (~ ((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                  & (0x08d4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                        if ((1U & (~ ((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                      & (0x0940U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_hit = 0U;
                        }
                    }
                }
            }
        }
    } else if ((0x00000200U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
        if ((0x00000100U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
            if ((1U & (~ ((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                          & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                if ((1U & (~ ((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                              & (0x08b4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                    if ((1U & (~ ((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                  & (0x08c8U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                        if ((1U & (~ ((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                      & (0x08d4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                            if ((1U & (~ ((0x0900U 
                                           <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                          & (0x0940U 
                                             > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_hit = 0U;
                            }
                        }
                    }
                }
            }
        } else if ((0x00000080U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
            if ((1U & (~ ((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                          & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                if ((1U & (~ ((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                              & (0x08b4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                    if ((1U & (~ ((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                  & (0x08c8U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                        if ((1U & (~ ((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                      & (0x08d4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                            if ((1U & (~ ((0x0900U 
                                           <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                          & (0x0940U 
                                             > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_hit = 0U;
                            }
                        }
                    }
                }
            }
        } else if ((0x00000040U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
            if ((1U & (~ ((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                          & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                if ((1U & (~ ((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                              & (0x08b4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                    if ((1U & (~ ((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                  & (0x08c8U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                        if ((1U & (~ ((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                      & (0x08d4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                            if ((1U & (~ ((0x0900U 
                                           <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                          & (0x0940U 
                                             > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_hit = 0U;
                            }
                        }
                    }
                }
            }
        } else if ((0x00000020U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
            if ((1U & (~ ((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                          & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                if ((1U & (~ ((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                              & (0x08b4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                    if ((1U & (~ ((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                  & (0x08c8U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                        if ((1U & (~ ((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                      & (0x08d4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                            if ((1U & (~ ((0x0900U 
                                           <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                          & (0x0940U 
                                             > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_hit = 0U;
                            }
                        }
                    }
                }
            }
        } else if ((0x00000010U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
            if ((1U & (~ ((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                          & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                if ((1U & (~ ((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                              & (0x08b4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                    if ((1U & (~ ((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                  & (0x08c8U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                        if ((1U & (~ ((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                      & (0x08d4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                            if ((1U & (~ ((0x0900U 
                                           <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                          & (0x0940U 
                                             > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_hit = 0U;
                            }
                        }
                    }
                }
            }
        } else if ((8U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
            if ((1U & (~ ((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                          & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                if ((1U & (~ ((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                              & (0x08b4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                    if ((1U & (~ ((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                  & (0x08c8U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                        if ((1U & (~ ((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                      & (0x08d4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                            if ((1U & (~ ((0x0900U 
                                           <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                          & (0x0940U 
                                             > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_hit = 0U;
                            }
                        }
                    }
                }
            }
        } else if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
            if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                if ((1U & (~ ((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                              & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                    if ((1U & (~ ((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                  & (0x08b4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                        if ((1U & (~ ((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                      & (0x08c8U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                            if ((1U & (~ ((0x08c8U 
                                           <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                          & (0x08d4U 
                                             > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                if ((1U & (~ ((0x0900U 
                                               <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                              & (0x0940U 
                                                 > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_hit = 0U;
                                }
                            }
                        }
                    }
                }
            } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                if ((1U & (~ ((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                              & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                    if ((1U & (~ ((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                  & (0x08b4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                        if ((1U & (~ ((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                      & (0x08c8U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                            if ((1U & (~ ((0x08c8U 
                                           <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                          & (0x08d4U 
                                             > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                if ((1U & (~ ((0x0900U 
                                               <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                              & (0x0940U 
                                                 > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_hit = 0U;
                                }
                            }
                        }
                    }
                }
            }
        } else if ((1U & (~ ((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                             & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
            if ((1U & (~ ((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                          & (0x08b4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                if ((1U & (~ ((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                              & (0x08c8U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                    if ((1U & (~ ((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                  & (0x08d4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                        if ((1U & (~ ((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                      & (0x0940U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_hit = 0U;
                        }
                    }
                }
            }
        }
    } else if ((0x00000100U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
        if ((0x00000080U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
            if ((1U & (~ ((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                          & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                if ((1U & (~ ((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                              & (0x08b4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                    if ((1U & (~ ((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                  & (0x08c8U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                        if ((1U & (~ ((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                      & (0x08d4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                            if ((1U & (~ ((0x0900U 
                                           <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                          & (0x0940U 
                                             > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_hit = 0U;
                            }
                        }
                    }
                }
            }
        } else if ((0x00000040U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
            if ((1U & (~ ((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                          & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                if ((1U & (~ ((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                              & (0x08b4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                    if ((1U & (~ ((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                  & (0x08c8U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                        if ((1U & (~ ((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                      & (0x08d4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                            if ((1U & (~ ((0x0900U 
                                           <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                          & (0x0940U 
                                             > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_hit = 0U;
                            }
                        }
                    }
                }
            }
        } else if ((0x00000020U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
            if ((1U & (~ ((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                          & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                if ((1U & (~ ((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                              & (0x08b4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                    if ((1U & (~ ((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                  & (0x08c8U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                        if ((1U & (~ ((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                      & (0x08d4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                            if ((1U & (~ ((0x0900U 
                                           <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                          & (0x0940U 
                                             > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_hit = 0U;
                            }
                        }
                    }
                }
            }
        } else if ((0x00000010U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
            if ((8U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                if ((1U & (~ ((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                              & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                    if ((1U & (~ ((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                  & (0x08b4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                        if ((1U & (~ ((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                      & (0x08c8U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                            if ((1U & (~ ((0x08c8U 
                                           <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                          & (0x08d4U 
                                             > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                if ((1U & (~ ((0x0900U 
                                               <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                              & (0x0940U 
                                                 > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_hit = 0U;
                                }
                            }
                        }
                    }
                }
            } else if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                if ((1U & (~ ((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                              & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                    if ((1U & (~ ((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                  & (0x08b4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                        if ((1U & (~ ((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                      & (0x08c8U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                            if ((1U & (~ ((0x08c8U 
                                           <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                          & (0x08d4U 
                                             > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                if ((1U & (~ ((0x0900U 
                                               <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                              & (0x0940U 
                                                 > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_hit = 0U;
                                }
                            }
                        }
                    }
                }
            } else if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                if ((1U & (~ ((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                              & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                    if ((1U & (~ ((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                  & (0x08b4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                        if ((1U & (~ ((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                      & (0x08c8U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                            if ((1U & (~ ((0x08c8U 
                                           <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                          & (0x08d4U 
                                             > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                if ((1U & (~ ((0x0900U 
                                               <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                              & (0x0940U 
                                                 > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_hit = 0U;
                                }
                            }
                        }
                    }
                }
            } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                if ((1U & (~ ((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                              & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                    if ((1U & (~ ((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                  & (0x08b4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                        if ((1U & (~ ((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                      & (0x08c8U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                            if ((1U & (~ ((0x08c8U 
                                           <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                          & (0x08d4U 
                                             > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                if ((1U & (~ ((0x0900U 
                                               <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                              & (0x0940U 
                                                 > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_hit = 0U;
                                }
                            }
                        }
                    }
                }
            }
        } else if ((1U & (~ ((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                             & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
            if ((1U & (~ ((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                          & (0x08b4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                if ((1U & (~ ((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                              & (0x08c8U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                    if ((1U & (~ ((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                  & (0x08d4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                        if ((1U & (~ ((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                      & (0x0940U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_hit = 0U;
                        }
                    }
                }
            }
        }
    } else if ((0x00000080U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
        if ((1U & (~ ((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                      & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
            if ((1U & (~ ((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                          & (0x08b4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                if ((1U & (~ ((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                              & (0x08c8U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                    if ((1U & (~ ((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                  & (0x08d4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                        if ((1U & (~ ((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                      & (0x0940U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_hit = 0U;
                        }
                    }
                }
            }
        }
    } else if ((0x00000040U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
        if ((1U & (~ ((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                      & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
            if ((1U & (~ ((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                          & (0x08b4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                if ((1U & (~ ((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                              & (0x08c8U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                    if ((1U & (~ ((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                  & (0x08d4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                        if ((1U & (~ ((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                      & (0x0940U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_hit = 0U;
                        }
                    }
                }
            }
        }
    } else if ((0x00000020U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
        if ((1U & (~ ((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                      & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
            if ((1U & (~ ((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                          & (0x08b4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                if ((1U & (~ ((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                              & (0x08c8U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                    if ((1U & (~ ((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                  & (0x08d4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                        if ((1U & (~ ((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                      & (0x0940U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_hit = 0U;
                        }
                    }
                }
            }
        }
    } else if ((0x00000010U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
        if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
            if ((1U & (~ ((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                          & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                if ((1U & (~ ((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                              & (0x08b4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                    if ((1U & (~ ((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                  & (0x08c8U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                        if ((1U & (~ ((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                      & (0x08d4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                            if ((1U & (~ ((0x0900U 
                                           <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                          & (0x0940U 
                                             > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_hit = 0U;
                            }
                        }
                    }
                }
            }
        } else if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
            if ((1U & (~ ((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                          & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                if ((1U & (~ ((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                              & (0x08b4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                    if ((1U & (~ ((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                  & (0x08c8U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                        if ((1U & (~ ((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                      & (0x08d4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                            if ((1U & (~ ((0x0900U 
                                           <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                          & (0x0940U 
                                             > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_hit = 0U;
                            }
                        }
                    }
                }
            }
        } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
            if ((1U & (~ ((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                          & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                if ((1U & (~ ((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                              & (0x08b4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                    if ((1U & (~ ((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                  & (0x08c8U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                        if ((1U & (~ ((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                      & (0x08d4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                            if ((1U & (~ ((0x0900U 
                                           <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                          & (0x0940U 
                                             > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_hit = 0U;
                            }
                        }
                    }
                }
            }
        }
    } else if ((1U & (~ ((0x0210U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                         & (0x0234U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
        if ((1U & (~ ((0x0874U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                      & (0x08b4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
            if ((1U & (~ ((0x08b4U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                          & (0x08c8U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                if ((1U & (~ ((0x08c8U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                              & (0x08d4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                    if ((1U & (~ ((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                  & (0x0940U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))))) {
                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_hit = 0U;
                    }
                }
            }
        }
    }
    milan_datapath__DOT__csr_tctx_rd_addr_w = ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_67)
                                                ? (
                                                   (0x00000070U 
                                                    & ((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__snap_idx_r) 
                                                       << 4U)) 
                                                   | (0x0000000fU 
                                                      & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__snap_word_r)))
                                                : (
                                                   ((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rds_idx_r) 
                                                    << 4U) 
                                                   | (0x0000000fU 
                                                      & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rds_word_r))));
    vlSelfRef.s_axi_arready = ((~ ((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__r_valid) 
                                   | ((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_pend) 
                                      | ((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__sweep_busy) 
                                         | (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rds_busy_r))))) 
                               & (IData)(vlSelfRef.s_axi_arvalid));
    vlSelfRef.milan_datapath__DOT____Vcellinp__talker_diag__frame_idx_i 
        = ((IData)(vlSelfRef.milan_datapath__DOT__aaf_frame_p_w)
            ? (IData)(vlSelfRef.milan_datapath__DOT__aaf_frame_idx_w)
            : 8U);
    vlSelfRef.milan_datapath__DOT__tkd_crf_p_w = ((~ (IData)(vlSelfRef.milan_datapath__DOT__aaf_frame_p_w)) 
                                                  & (IData)(vlSelfRef.milan_datapath__DOT__tkd_crf_pend_r));
    vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__tram_q_r 
        = vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__tctx_r
        [vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__tram_raddr_w];
    vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__grant_v_w = 0U;
    vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__grant_t_w = 0U;
    milan_datapath__DOT__aaf_packetizer__DOT__rr_pick__DOT__unnamedblk3__DOT__unnamedblk4__DOT__t 
        = (7U & ((IData)(8U) + (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__rr_r)));
    if (vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pend_r
        [(7U & milan_datapath__DOT__aaf_packetizer__DOT__rr_pick__DOT__unnamedblk3__DOT__unnamedblk4__DOT__t)]) {
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__grant_v_w = 1U;
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__grant_t_w 
            = (7U & milan_datapath__DOT__aaf_packetizer__DOT__rr_pick__DOT__unnamedblk3__DOT__unnamedblk4__DOT__t);
    }
    milan_datapath__DOT__aaf_packetizer__DOT__rr_pick__DOT__unnamedblk3__DOT__unnamedblk4__DOT__t 
        = (7U & ((IData)(7U) + (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__rr_r)));
    if (vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pend_r
        [(7U & milan_datapath__DOT__aaf_packetizer__DOT__rr_pick__DOT__unnamedblk3__DOT__unnamedblk4__DOT__t)]) {
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__grant_v_w = 1U;
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__grant_t_w 
            = (7U & milan_datapath__DOT__aaf_packetizer__DOT__rr_pick__DOT__unnamedblk3__DOT__unnamedblk4__DOT__t);
    }
    milan_datapath__DOT__aaf_packetizer__DOT__rr_pick__DOT__unnamedblk3__DOT__unnamedblk4__DOT__t 
        = (7U & ((IData)(6U) + (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__rr_r)));
    if (vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pend_r
        [(7U & milan_datapath__DOT__aaf_packetizer__DOT__rr_pick__DOT__unnamedblk3__DOT__unnamedblk4__DOT__t)]) {
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__grant_v_w = 1U;
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__grant_t_w 
            = (7U & milan_datapath__DOT__aaf_packetizer__DOT__rr_pick__DOT__unnamedblk3__DOT__unnamedblk4__DOT__t);
    }
    milan_datapath__DOT__aaf_packetizer__DOT__rr_pick__DOT__unnamedblk3__DOT__unnamedblk4__DOT__t 
        = (7U & ((IData)(5U) + (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__rr_r)));
    if (vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pend_r
        [(7U & milan_datapath__DOT__aaf_packetizer__DOT__rr_pick__DOT__unnamedblk3__DOT__unnamedblk4__DOT__t)]) {
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__grant_v_w = 1U;
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__grant_t_w 
            = (7U & milan_datapath__DOT__aaf_packetizer__DOT__rr_pick__DOT__unnamedblk3__DOT__unnamedblk4__DOT__t);
    }
    milan_datapath__DOT__aaf_packetizer__DOT__rr_pick__DOT__unnamedblk3__DOT__unnamedblk4__DOT__t 
        = (7U & ((IData)(4U) + (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__rr_r)));
    if (vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pend_r
        [(7U & milan_datapath__DOT__aaf_packetizer__DOT__rr_pick__DOT__unnamedblk3__DOT__unnamedblk4__DOT__t)]) {
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__grant_v_w = 1U;
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__grant_t_w 
            = (7U & milan_datapath__DOT__aaf_packetizer__DOT__rr_pick__DOT__unnamedblk3__DOT__unnamedblk4__DOT__t);
    }
    milan_datapath__DOT__aaf_packetizer__DOT__rr_pick__DOT__unnamedblk3__DOT__unnamedblk4__DOT__t 
        = (7U & ((IData)(3U) + (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__rr_r)));
    if (vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pend_r
        [(7U & milan_datapath__DOT__aaf_packetizer__DOT__rr_pick__DOT__unnamedblk3__DOT__unnamedblk4__DOT__t)]) {
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__grant_v_w = 1U;
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__grant_t_w 
            = (7U & milan_datapath__DOT__aaf_packetizer__DOT__rr_pick__DOT__unnamedblk3__DOT__unnamedblk4__DOT__t);
    }
    milan_datapath__DOT__aaf_packetizer__DOT__rr_pick__DOT__unnamedblk3__DOT__unnamedblk4__DOT__t 
        = (7U & ((IData)(2U) + (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__rr_r)));
    if (vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pend_r
        [(7U & milan_datapath__DOT__aaf_packetizer__DOT__rr_pick__DOT__unnamedblk3__DOT__unnamedblk4__DOT__t)]) {
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__grant_v_w = 1U;
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__grant_t_w 
            = (7U & milan_datapath__DOT__aaf_packetizer__DOT__rr_pick__DOT__unnamedblk3__DOT__unnamedblk4__DOT__t);
    }
    milan_datapath__DOT__aaf_packetizer__DOT__rr_pick__DOT__unnamedblk3__DOT__unnamedblk4__DOT__t 
        = (7U & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__rr_r)));
    if (vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pend_r
        [(7U & milan_datapath__DOT__aaf_packetizer__DOT__rr_pick__DOT__unnamedblk3__DOT__unnamedblk4__DOT__t)]) {
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__grant_v_w = 1U;
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__grant_t_w 
            = (7U & milan_datapath__DOT__aaf_packetizer__DOT__rr_pick__DOT__unnamedblk3__DOT__unnamedblk4__DOT__t);
    }
    vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__stg_q_r 
        = vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__stg_r
        [(((IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__et_r) 
           << 6U) | (((IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__ebank_r) 
                      << 5U) | ((((IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__esmp_r) 
                                  << 2U) | (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__eo_r)) 
                                & (- (IData)((2U == (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__est_r)))))))];
    vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__in_acc 
        = ((IData)(vlSelfRef.s_axis_tx_tvalid) & (IData)(vlSelfRef.s_axis_tx_tready));
    vlSelfRef.milan_datapath__DOT__chan_tdm_render__DOT__u_fcdc__DOT__wptr_bin_n 
        = (7U & ((IData)(vlSelfRef.milan_datapath__DOT__chan_tdm_render__DOT__u_fcdc__DOT__wptr_bin_r) 
                 + (IData)(vlSelfRef.milan_datapath__DOT__chan_tdm_render__DOT__fifo_wen_w)));
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_render__DOT__sel_r__v0) {
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__sel_r[0U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__sel_r__v0;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_render__DOT__sel_r__v1) {
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__sel_r[0U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__sel_r__v1;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_render__DOT__sel_r__v2) {
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__sel_r[0U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__sel_r__v2;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_render__DOT__sel_r__v3) {
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__sel_r[1U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__sel_r__v3;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_render__DOT__sel_r__v4) {
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__sel_r[1U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__sel_r__v4;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_render__DOT__sel_r__v5) {
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__sel_r[1U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__sel_r__v5;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_render__DOT__sel_r__v6) {
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__sel_r[2U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__sel_r__v6;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_render__DOT__sel_r__v7) {
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__sel_r[2U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__sel_r__v7;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_render__DOT__sel_r__v8) {
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__sel_r[2U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__sel_r__v8;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_render__DOT__sel_r__v9) {
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__sel_r[3U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__sel_r__v9;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_render__DOT__sel_r__v10) {
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__sel_r[3U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__sel_r__v10;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_render__DOT__sel_r__v11) {
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__sel_r[3U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__sel_r__v11;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_render__DOT__sel_r__v12) {
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__sel_r[4U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__sel_r__v12;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_render__DOT__sel_r__v13) {
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__sel_r[4U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__sel_r__v13;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_render__DOT__sel_r__v14) {
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__sel_r[4U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__sel_r__v14;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_render__DOT__sel_r__v15) {
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__sel_r[5U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__sel_r__v15;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_render__DOT__sel_r__v16) {
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__sel_r[5U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__sel_r__v16;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_render__DOT__sel_r__v17) {
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__sel_r[5U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__sel_r__v17;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_render__DOT__sel_r__v18) {
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__sel_r[6U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__sel_r__v18;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_render__DOT__sel_r__v19) {
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__sel_r[6U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__sel_r__v19;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_render__DOT__sel_r__v20) {
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__sel_r[6U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__sel_r__v20;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_render__DOT__sel_r__v21) {
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__sel_r[7U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__sel_r__v21;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_render__DOT__sel_r__v22) {
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__sel_r[7U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__sel_r__v22;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_render__DOT__sel_r__v23) {
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__sel_r[7U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__sel_r__v23;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_render__DOT__sel_r__v24) {
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__sel_r[8U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__sel_r__v24;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_render__DOT__sel_r__v25) {
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__sel_r[8U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__sel_r__v25;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_render__DOT__sel_r__v26) {
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__sel_r[8U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__sel_r__v26;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_render__DOT__sel_r__v27) {
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__sel_r[9U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__sel_r__v27;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_render__DOT__sel_r__v28) {
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__sel_r[9U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__sel_r__v28;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_render__DOT__sel_r__v29) {
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__sel_r[9U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__sel_r__v29;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_render__DOT__sel_r__v30) {
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__sel_r[0U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__sel_r[1U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__sel_r[2U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__sel_r[3U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__sel_r[4U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__sel_r[5U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__sel_r[6U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__sel_r[7U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__sel_r[8U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__sel_r[9U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_render__DOT__map_r__v0) {
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__map_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__chan_map_render__DOT__map_r__v0] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__map_r__v0;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_render__DOT__map_r__v1) {
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__map_r[0U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__map_r[1U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__map_r[2U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__map_r[3U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__map_r[4U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__map_r[5U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__map_r[6U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__map_r[7U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__map_r[8U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__map_r[9U] = 0U;
    }
    vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__4__KET____DOT__u_cbs__DOT__eng_q1 
        = vlSelfRef.__Vdly__milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__4__KET____DOT__u_cbs__DOT__eng_q1;
    vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__4__KET____DOT__u_cbs__DOT__eng_cnt 
        = vlSelfRef.__Vdly__milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__4__KET____DOT__u_cbs__DOT__eng_cnt;
    vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__4__KET____DOT__u_cbs__DOT__eng_is1g_s 
        = vlSelfRef.__Vdly__milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__4__KET____DOT__u_cbs__DOT__eng_is1g_s;
    vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__4__KET____DOT__u_cbs__DOT__eng_num 
        = vlSelfRef.__Vdly__milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__4__KET____DOT__u_cbs__DOT__eng_num;
    vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__4__KET____DOT__u_cbs__DOT__eng_quo 
        = vlSelfRef.__Vdly__milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__4__KET____DOT__u_cbs__DOT__eng_quo;
    vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__4__KET____DOT__u_cbs__DOT__eng_den 
        = vlSelfRef.__Vdly__milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__4__KET____DOT__u_cbs__DOT__eng_den;
    vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__3__KET____DOT__u_cbs__DOT__eng_q1 
        = vlSelfRef.__Vdly__milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__3__KET____DOT__u_cbs__DOT__eng_q1;
    vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__3__KET____DOT__u_cbs__DOT__eng_cnt 
        = vlSelfRef.__Vdly__milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__3__KET____DOT__u_cbs__DOT__eng_cnt;
    vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__3__KET____DOT__u_cbs__DOT__eng_is1g_s 
        = vlSelfRef.__Vdly__milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__3__KET____DOT__u_cbs__DOT__eng_is1g_s;
    vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__3__KET____DOT__u_cbs__DOT__eng_num 
        = vlSelfRef.__Vdly__milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__3__KET____DOT__u_cbs__DOT__eng_num;
    vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__3__KET____DOT__u_cbs__DOT__eng_quo 
        = vlSelfRef.__Vdly__milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__3__KET____DOT__u_cbs__DOT__eng_quo;
    vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__3__KET____DOT__u_cbs__DOT__eng_den 
        = vlSelfRef.__Vdly__milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__3__KET____DOT__u_cbs__DOT__eng_den;
    vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__2__KET____DOT__u_cbs__DOT__eng_q1 
        = vlSelfRef.__Vdly__milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__2__KET____DOT__u_cbs__DOT__eng_q1;
    vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__2__KET____DOT__u_cbs__DOT__eng_cnt 
        = vlSelfRef.__Vdly__milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__2__KET____DOT__u_cbs__DOT__eng_cnt;
    vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__2__KET____DOT__u_cbs__DOT__eng_is1g_s 
        = vlSelfRef.__Vdly__milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__2__KET____DOT__u_cbs__DOT__eng_is1g_s;
    vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__2__KET____DOT__u_cbs__DOT__eng_num 
        = vlSelfRef.__Vdly__milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__2__KET____DOT__u_cbs__DOT__eng_num;
    vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__2__KET____DOT__u_cbs__DOT__eng_quo 
        = vlSelfRef.__Vdly__milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__2__KET____DOT__u_cbs__DOT__eng_quo;
    vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__2__KET____DOT__u_cbs__DOT__eng_den 
        = vlSelfRef.__Vdly__milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__2__KET____DOT__u_cbs__DOT__eng_den;
    vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__1__KET____DOT__u_cbs__DOT__eng_q1 
        = vlSelfRef.__Vdly__milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__1__KET____DOT__u_cbs__DOT__eng_q1;
    vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__1__KET____DOT__u_cbs__DOT__eng_cnt 
        = vlSelfRef.__Vdly__milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__1__KET____DOT__u_cbs__DOT__eng_cnt;
    vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__1__KET____DOT__u_cbs__DOT__eng_is1g_s 
        = vlSelfRef.__Vdly__milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__1__KET____DOT__u_cbs__DOT__eng_is1g_s;
    vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__1__KET____DOT__u_cbs__DOT__eng_num 
        = vlSelfRef.__Vdly__milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__1__KET____DOT__u_cbs__DOT__eng_num;
    vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__1__KET____DOT__u_cbs__DOT__eng_quo 
        = vlSelfRef.__Vdly__milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__1__KET____DOT__u_cbs__DOT__eng_quo;
    vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__1__KET____DOT__u_cbs__DOT__eng_den 
        = vlSelfRef.__Vdly__milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__1__KET____DOT__u_cbs__DOT__eng_den;
    vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__0__KET____DOT__u_cbs__DOT__eng_q1 
        = vlSelfRef.__Vdly__milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__0__KET____DOT__u_cbs__DOT__eng_q1;
    vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__0__KET____DOT__u_cbs__DOT__eng_cnt 
        = vlSelfRef.__Vdly__milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__0__KET____DOT__u_cbs__DOT__eng_cnt;
    vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__0__KET____DOT__u_cbs__DOT__eng_is1g_s 
        = vlSelfRef.__Vdly__milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__0__KET____DOT__u_cbs__DOT__eng_is1g_s;
    vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__0__KET____DOT__u_cbs__DOT__eng_num 
        = vlSelfRef.__Vdly__milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__0__KET____DOT__u_cbs__DOT__eng_num;
    vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__0__KET____DOT__u_cbs__DOT__eng_quo 
        = vlSelfRef.__Vdly__milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__0__KET____DOT__u_cbs__DOT__eng_quo;
    vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__0__KET____DOT__u_cbs__DOT__eng_den 
        = vlSelfRef.__Vdly__milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__0__KET____DOT__u_cbs__DOT__eng_den;
    __Vfunc_milan_datapath__DOT__chan_map_render__DOT__src_rd__181__a 
        = (0x0000007fU & (IData)(vlSelfRef.milan_datapath__DOT____Vcellinp__chan_map_render__map_wr_data_i));
    __Vfunc_milan_datapath__DOT__chan_map_render__DOT__src_rd__181__Vfuncout 
        = ((0x00000040U & (IData)(__Vfunc_milan_datapath__DOT__chan_map_render__DOT__src_rd__181__a))
            ? ((0x10U > (0x0000003fU & (IData)(__Vfunc_milan_datapath__DOT__chan_map_render__DOT__src_rd__181__a)))
                ? vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__pbcur_r
               [(0x0000000fU & (IData)(__Vfunc_milan_datapath__DOT__chan_map_render__DOT__src_rd__181__a))]
                : 0U) : vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__cur_r
           [(7U & ((IData)(__Vfunc_milan_datapath__DOT__chan_map_render__DOT__src_rd__181__a) 
                   >> 3U))][(7U & (IData)(__Vfunc_milan_datapath__DOT__chan_map_render__DOT__src_rd__181__a))]);
    vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__map_seed_w 
        = __Vfunc_milan_datapath__DOT__chan_map_render__DOT__src_rd__181__Vfuncout;
    vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__dm_tready 
        = ((((IData)(vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT____Vcellout__fifo_gen__BRA__4__KET____DOT__eth_packet_buffer__s_axis_tready) 
             << 4U) | (((IData)(vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT____Vcellout__fifo_gen__BRA__3__KET____DOT__eth_packet_buffer__s_axis_tready) 
                        << 3U) | ((IData)(vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT____Vcellout__fifo_gen__BRA__2__KET____DOT__eth_packet_buffer__s_axis_tready) 
                                  << 2U))) | (((IData)(vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT____Vcellout__fifo_gen__BRA__1__KET____DOT__eth_packet_buffer__s_axis_tready) 
                                               << 1U) 
                                              | (IData)(vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT____Vcellout__fifo_gen__BRA__0__KET____DOT__eth_packet_buffer__s_axis_tready)));
    vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_rx__DOT__ts_state 
        = vlSelfRef.__Vdly__milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_rx__DOT__ts_state;
    vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_tx__DOT__ts_state 
        = vlSelfRef.__Vdly__milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_tx__DOT__ts_state;
    vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__tl_idx_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__aaf_rx_depkt__DOT__tl_idx_r;
    vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__locked_sh_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__locked_sh_r;
    vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__zero_idx_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__zero_idx_r;
    vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__bind_pend_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__bind_pend_r;
    vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__sil_pend_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__sil_pend_r;
    vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__servo_pend_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__servo_pend_r;
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r__v0) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r[0U][0U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r__v0[0U];
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r[0U][1U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r__v0[1U];
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r[0U][2U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r__v0[2U];
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r[0U][3U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r__v0[3U];
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r[0U][4U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r__v0[4U];
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r__v1) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r__v1][0U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r__v1[0U];
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r__v1][1U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r__v1[1U];
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r__v1][2U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r__v1[2U];
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r__v1][3U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r__v1[3U];
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r__v1][4U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r__v1[4U];
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r__v2) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r[0U][0U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r__v2[0U];
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r[0U][1U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r__v2[1U];
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r[0U][2U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r__v2[2U];
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r[0U][3U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r__v2[3U];
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r[0U][4U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r__v2[4U];
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r__v3) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r[0U][0U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r__v3[0U];
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r[0U][1U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r__v3[1U];
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r[0U][2U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r__v3[2U];
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r[0U][3U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r__v3[3U];
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r[0U][4U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r__v3[4U];
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r[1U][0U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r__v4[0U];
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r[1U][1U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r__v4[1U];
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r[1U][2U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r__v4[2U];
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r[1U][3U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r__v4[3U];
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r[1U][4U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r__v4[4U];
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r__v5) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r[0U][0U] = 0U;
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r[0U][1U] = 0U;
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r[0U][2U] = 0U;
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r[0U][3U] = 0U;
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r[0U][4U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r__v6) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r[1U][0U] = 0U;
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r[1U][1U] = 0U;
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r[1U][2U] = 0U;
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r[1U][3U] = 0U;
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r[1U][4U] = 0U;
    }
    vlSelfRef.milan_datapath__DOT__route_render_sel_w = 0U;
    if ((2U & vlSelfRef.milan_datapath__DOT__pcm_route__DOT__route_r[7U])) {
        vlSelfRef.milan_datapath__DOT__route_render_sel_w = 7U;
    }
    if ((2U & vlSelfRef.milan_datapath__DOT__pcm_route__DOT__route_r[6U])) {
        vlSelfRef.milan_datapath__DOT__route_render_sel_w = 6U;
    }
    if ((2U & vlSelfRef.milan_datapath__DOT__pcm_route__DOT__route_r[5U])) {
        vlSelfRef.milan_datapath__DOT__route_render_sel_w = 5U;
    }
    if ((2U & vlSelfRef.milan_datapath__DOT__pcm_route__DOT__route_r[4U])) {
        vlSelfRef.milan_datapath__DOT__route_render_sel_w = 4U;
    }
    if ((2U & vlSelfRef.milan_datapath__DOT__pcm_route__DOT__route_r[3U])) {
        vlSelfRef.milan_datapath__DOT__route_render_sel_w = 3U;
    }
    if ((2U & vlSelfRef.milan_datapath__DOT__pcm_route__DOT__route_r[2U])) {
        vlSelfRef.milan_datapath__DOT__route_render_sel_w = 2U;
    }
    if ((2U & vlSelfRef.milan_datapath__DOT__pcm_route__DOT__route_r[1U])) {
        vlSelfRef.milan_datapath__DOT__route_render_sel_w = 1U;
    }
    if ((2U & vlSelfRef.milan_datapath__DOT__pcm_route__DOT__route_r[0U])) {
        vlSelfRef.milan_datapath__DOT__route_render_sel_w = 0U;
    }
    vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__bind_zero_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__bind_zero_r;
    vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__inc_rd_q_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__inc_rd_q_r;
    vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__wrph_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__wrph_r;
    vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__pq_cnt_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__pq_cnt_r;
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__chans_sh_r__v0) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__chans_sh_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__avtp_rx_monitor__DOT__chans_sh_r__v0] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__chans_sh_r__v0;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r__v0) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r[0U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r__v1) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r[0U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r__v1;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r__v2) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r[1U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r__v3) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r[1U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r__v3;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r__v4) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r[2U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r__v5) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r[2U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r__v5;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r__v6) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r[3U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r__v7) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r[3U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r__v7;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r__v8) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r[4U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r__v9) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r[4U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r__v9;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r__v10) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r[5U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r__v11) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r[5U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r__v11;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r__v12) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r[6U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r__v13) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r[6U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r__v13;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r__v14) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r[7U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r__v15) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r[7U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r__v15;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r__v16) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r__v16] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r__v17) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r__v17] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__chans_sh_r__v0) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r__v18] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__mreset_pend_r__v0) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__mreset_pend_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__avtp_rx_monitor__DOT__mreset_pend_r__v0] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__mreset_pend_r__v0;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__mreset_pend_r__v1) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__mreset_pend_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__avtp_rx_monitor__DOT__mreset_pend_r__v1] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__mreset_pend_r__v1;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_pend_r__v0) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_pend_r[0U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_pend_r__v0;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_pend_r__v1) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_pend_r[1U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_pend_r__v1;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_pend_r__v2) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_pend_r[2U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_pend_r__v2;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_pend_r__v3) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_pend_r[3U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_pend_r__v3;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_pend_r__v4) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_pend_r[4U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_pend_r__v4;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_pend_r__v5) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_pend_r[5U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_pend_r__v5;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_pend_r__v6) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_pend_r[6U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_pend_r__v6;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_pend_r__v7) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_pend_r[7U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_pend_r__v7;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_pend_r__v8) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_pend_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_pend_r__v8] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_pend_r__v8;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__chans_sh_r__v1) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__chans_sh_r[0U] = 0U;
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r[0U] = 0U;
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__mreset_pend_r[0U] = 0U;
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_pend_r[0U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__ddrop_pend_r__v0) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ddrop_pend_r[0U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__ddrop_pend_r__v0;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__ddrop_pend_r__v1) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ddrop_pend_r[1U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__ddrop_pend_r__v1;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__ddrop_pend_r__v2) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ddrop_pend_r[2U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__ddrop_pend_r__v2;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__ddrop_pend_r__v3) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ddrop_pend_r[3U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__ddrop_pend_r__v3;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__ddrop_pend_r__v4) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ddrop_pend_r[4U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__ddrop_pend_r__v4;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__ddrop_pend_r__v5) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ddrop_pend_r[5U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__ddrop_pend_r__v5;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__ddrop_pend_r__v6) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ddrop_pend_r[6U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__ddrop_pend_r__v6;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__ddrop_pend_r__v7) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ddrop_pend_r[7U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__ddrop_pend_r__v7;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_pend_r__v8) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ddrop_pend_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__avtp_rx_monitor__DOT__ddrop_pend_r__v8] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__ddrop_pend_r__v8;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__chans_sh_r__v1) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ddrop_pend_r[0U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__chans_sh_r__v2) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__chans_sh_r[1U] = 0U;
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__chans_sh_r[2U] = 0U;
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__chans_sh_r[3U] = 0U;
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__chans_sh_r[4U] = 0U;
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__chans_sh_r[5U] = 0U;
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__chans_sh_r[6U] = 0U;
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__chans_sh_r[7U] = 0U;
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r[1U] = 0U;
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r[2U] = 0U;
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r[3U] = 0U;
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r[4U] = 0U;
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r[5U] = 0U;
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r[6U] = 0U;
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r[7U] = 0U;
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__mreset_pend_r[1U] = 0U;
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__mreset_pend_r[2U] = 0U;
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__mreset_pend_r[3U] = 0U;
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__mreset_pend_r[4U] = 0U;
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__mreset_pend_r[5U] = 0U;
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__mreset_pend_r[6U] = 0U;
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__mreset_pend_r[7U] = 0U;
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_pend_r[1U] = 0U;
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_pend_r[2U] = 0U;
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_pend_r[3U] = 0U;
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_pend_r[4U] = 0U;
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_pend_r[5U] = 0U;
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_pend_r[6U] = 0U;
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_pend_r[7U] = 0U;
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ddrop_pend_r[1U] = 0U;
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ddrop_pend_r[2U] = 0U;
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ddrop_pend_r[3U] = 0U;
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ddrop_pend_r[4U] = 0U;
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ddrop_pend_r[5U] = 0U;
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ddrop_pend_r[6U] = 0U;
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ddrop_pend_r[7U] = 0U;
    }
    vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__mst_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__mst_r;
    vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__class_map__DOT__gptp_frame 
        = (IData)(((0x000088f700000000ULL == (0x0000ffff00000000ULL 
                                              & vlSelfRef.__VdfgRegularize_h6e95ff9d_0_17)) 
                   & ((~ (vlSelfRef.milan_datapath__DOT__csr__DOT__cls_ctrl 
                          >> 1U)) | (0x00000180c200000eULL 
                                     == (0x0000ffffffffffffULL 
                                         & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__hdr_eff[5U])) 
                                             << 0x00000010U) 
                                            | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__hdr_eff[4U])) 
                                               >> 0x00000010U)))))));
    __VdfgRegularize_h6e95ff9d_0_93 = (0x0000001fU 
                                       & ((IData)(3U) 
                                          * (7U & (
                                                   (0x8100U 
                                                    == 
                                                    (0x0000ffffU 
                                                     & (IData)(
                                                               (vlSelfRef.__VdfgRegularize_h6e95ff9d_0_17 
                                                                >> 0x00000010U))))
                                                    ? (IData)(
                                                              (vlSelfRef.__VdfgRegularize_h6e95ff9d_0_17 
                                                               >> 0x0000000dU))
                                                    : vlSelfRef.milan_datapath__DOT__csr__DOT__cls_dpcp))));
    milan_datapath__DOT__chan_map_capture__DOT__lb_sel_ok_w 
        = ((8U > (0x0000000fU & (vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r
                                 [vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__slot_r] 
                                 >> 8U))) & (4U > (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_10)));
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__aaf_packetizer__DOT__tctx_r__v0) {
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__tctx_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__aaf_packetizer__DOT__tctx_r__v0] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__aaf_packetizer__DOT__tctx_r__v0;
    }
    vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__ebank_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__aaf_packetizer__DOT__ebank_r;
    vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__esmp_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__aaf_packetizer__DOT__esmp_r;
    vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__eo_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__aaf_packetizer__DOT__eo_r;
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__aaf_packetizer__DOT__stg_r__v0) {
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__stg_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__aaf_packetizer__DOT__stg_r__v0] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__aaf_packetizer__DOT__stg_r__v0;
    }
    vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__et_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__aaf_packetizer__DOT__et_r;
    vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__est_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__aaf_packetizer__DOT__est_r;
    vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__do_push 
        = ((IData)(vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__in_acc) 
           & ((~ (IData)(vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__tq_pushed)) 
              & ((IData)(vlSelfRef.s_axis_tx_tlast) 
                 | ((0x12U > (IData)(vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__byte_counter)) 
                    & (0x00000012U <= ((IData)(8U) 
                                       + (IData)(vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__byte_counter)))))));
    vlSelfRef.milan_datapath__DOT____Vcellinp__i2s_feed_mux__phys_armed_i 
        = (1U & ((vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__map_r[0U] 
                  | vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__map_r[1U]) 
                 >> 7U));
    vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__4__KET____DOT__u_cbs__DOT__eng_ldval 
        = (0x0000ffffffffffffULL & ((1U == (IData)(vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__4__KET____DOT__u_cbs__DOT__eng_cnt))
                                     ? (vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__4__KET____DOT__u_cbs__DOT__eng_idle_s 
                                        << 0x00000010U)
                                     : ((vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__4__KET____DOT__u_cbs__DOT__eng_idle_s 
                                         - ((IData)(vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__4__KET____DOT__u_cbs__DOT__eng_is1g_s)
                                             ? 0x000000003b9aca00ULL
                                             : 0x0000000005f5e100ULL)) 
                                        << 0x00000010U)));
    vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__4__KET____DOT__u_cbs__DOT__eng_trial 
        = ((vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__4__KET____DOT__u_cbs__DOT__eng_rem 
            << 1U) | (1U & (IData)((vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__4__KET____DOT__u_cbs__DOT__eng_num 
                                    >> 0x0000002fU))));
    milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__4__KET____DOT__u_cbs__DOT__eng_quo_r 
        = (0x0000ffffffffffffULL & (vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__4__KET____DOT__u_cbs__DOT__eng_quo 
                                    + (QData)((IData)(
                                                      ((vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__4__KET____DOT__u_cbs__DOT__eng_rem 
                                                        << 1U) 
                                                       >= vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__4__KET____DOT__u_cbs__DOT__eng_den)))));
    vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__3__KET____DOT__u_cbs__DOT__eng_ldval 
        = (0x0000ffffffffffffULL & ((1U == (IData)(vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__3__KET____DOT__u_cbs__DOT__eng_cnt))
                                     ? (vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__3__KET____DOT__u_cbs__DOT__eng_idle_s 
                                        << 0x00000010U)
                                     : ((vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__3__KET____DOT__u_cbs__DOT__eng_idle_s 
                                         - ((IData)(vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__3__KET____DOT__u_cbs__DOT__eng_is1g_s)
                                             ? 0x000000003b9aca00ULL
                                             : 0x0000000005f5e100ULL)) 
                                        << 0x00000010U)));
    vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__3__KET____DOT__u_cbs__DOT__eng_trial 
        = ((vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__3__KET____DOT__u_cbs__DOT__eng_rem 
            << 1U) | (1U & (IData)((vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__3__KET____DOT__u_cbs__DOT__eng_num 
                                    >> 0x0000002fU))));
    milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__3__KET____DOT__u_cbs__DOT__eng_quo_r 
        = (0x0000ffffffffffffULL & (vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__3__KET____DOT__u_cbs__DOT__eng_quo 
                                    + (QData)((IData)(
                                                      ((vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__3__KET____DOT__u_cbs__DOT__eng_rem 
                                                        << 1U) 
                                                       >= vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__3__KET____DOT__u_cbs__DOT__eng_den)))));
    vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__2__KET____DOT__u_cbs__DOT__eng_ldval 
        = (0x0000ffffffffffffULL & ((1U == (IData)(vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__2__KET____DOT__u_cbs__DOT__eng_cnt))
                                     ? (vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__2__KET____DOT__u_cbs__DOT__eng_idle_s 
                                        << 0x00000010U)
                                     : ((vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__2__KET____DOT__u_cbs__DOT__eng_idle_s 
                                         - ((IData)(vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__2__KET____DOT__u_cbs__DOT__eng_is1g_s)
                                             ? 0x000000003b9aca00ULL
                                             : 0x0000000005f5e100ULL)) 
                                        << 0x00000010U)));
    vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__2__KET____DOT__u_cbs__DOT__eng_trial 
        = ((vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__2__KET____DOT__u_cbs__DOT__eng_rem 
            << 1U) | (1U & (IData)((vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__2__KET____DOT__u_cbs__DOT__eng_num 
                                    >> 0x0000002fU))));
    milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__2__KET____DOT__u_cbs__DOT__eng_quo_r 
        = (0x0000ffffffffffffULL & (vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__2__KET____DOT__u_cbs__DOT__eng_quo 
                                    + (QData)((IData)(
                                                      ((vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__2__KET____DOT__u_cbs__DOT__eng_rem 
                                                        << 1U) 
                                                       >= vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__2__KET____DOT__u_cbs__DOT__eng_den)))));
    vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__1__KET____DOT__u_cbs__DOT__eng_ldval 
        = (0x0000ffffffffffffULL & ((1U == (IData)(vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__1__KET____DOT__u_cbs__DOT__eng_cnt))
                                     ? (vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__1__KET____DOT__u_cbs__DOT__eng_idle_s 
                                        << 0x00000010U)
                                     : ((vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__1__KET____DOT__u_cbs__DOT__eng_idle_s 
                                         - ((IData)(vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__1__KET____DOT__u_cbs__DOT__eng_is1g_s)
                                             ? 0x000000003b9aca00ULL
                                             : 0x0000000005f5e100ULL)) 
                                        << 0x00000010U)));
    vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__1__KET____DOT__u_cbs__DOT__eng_trial 
        = ((vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__1__KET____DOT__u_cbs__DOT__eng_rem 
            << 1U) | (1U & (IData)((vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__1__KET____DOT__u_cbs__DOT__eng_num 
                                    >> 0x0000002fU))));
    milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__1__KET____DOT__u_cbs__DOT__eng_quo_r 
        = (0x0000ffffffffffffULL & (vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__1__KET____DOT__u_cbs__DOT__eng_quo 
                                    + (QData)((IData)(
                                                      ((vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__1__KET____DOT__u_cbs__DOT__eng_rem 
                                                        << 1U) 
                                                       >= vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__1__KET____DOT__u_cbs__DOT__eng_den)))));
    vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__0__KET____DOT__u_cbs__DOT__eng_ldval 
        = (0x0000ffffffffffffULL & ((1U == (IData)(vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__0__KET____DOT__u_cbs__DOT__eng_cnt))
                                     ? (vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__0__KET____DOT__u_cbs__DOT__eng_idle_s 
                                        << 0x00000010U)
                                     : ((vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__0__KET____DOT__u_cbs__DOT__eng_idle_s 
                                         - ((IData)(vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__0__KET____DOT__u_cbs__DOT__eng_is1g_s)
                                             ? 0x000000003b9aca00ULL
                                             : 0x0000000005f5e100ULL)) 
                                        << 0x00000010U)));
    vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__0__KET____DOT__u_cbs__DOT__eng_trial 
        = ((vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__0__KET____DOT__u_cbs__DOT__eng_rem 
            << 1U) | (1U & (IData)((vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__0__KET____DOT__u_cbs__DOT__eng_num 
                                    >> 0x0000002fU))));
    milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__0__KET____DOT__u_cbs__DOT__eng_quo_r 
        = (0x0000ffffffffffffULL & (vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__0__KET____DOT__u_cbs__DOT__eng_quo 
                                    + (QData)((IData)(
                                                      ((vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__0__KET____DOT__u_cbs__DOT__eng_rem 
                                                        << 1U) 
                                                       >= vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__0__KET____DOT__u_cbs__DOT__eng_den)))));
    if (vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__mux_queues__DOT__store_axis_int_to_temp) {
        vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__mux_queues__DOT__temp_m_axis_tlast_reg 
            = (1U & (vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__eth_packet_buffer__DOT__m_axis_pipe_reg[1U][2U] 
                     >> 8U));
    }
    vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__mux_queues__DOT__store_axis_int_to_output = 0U;
    vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__mux_queues__DOT__store_axis_temp_to_output = 0U;
    if ((1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__mux_queues__DOT__m_axis_tready_int_reg)))) {
        if ((0U != ((IData)(vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__dm_tready) 
                    & (IData)(vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__mux_queues__DOT__m_axis_tvalid_reg)))) {
            vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__mux_queues__DOT__store_axis_temp_to_output = 1U;
        }
    }
    vlSelfRef.milan_datapath__DOT__csr__DOT__rds_valid_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rds_dir_r)
            ? (IData)(vlSelfRef.milan_datapath__DOT__tctx_rd_valid_w)
            : (IData)(vlSelfRef.milan_datapath__DOT__lctx_rd_valid_w));
    vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ram_q_r 
        = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__lctx_r
        [vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ram_raddr_w];
    vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__inc_next_w = 0x0fU;
    if ((0x00000200U & (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__inc_list_r))) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__inc_next_w = 9U;
    }
    if ((0x00000100U & (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__inc_list_r))) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__inc_next_w = 8U;
    }
    if ((0x00000080U & (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__inc_list_r))) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__inc_next_w = 7U;
    }
    if ((0x00000040U & (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__inc_list_r))) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__inc_next_w = 6U;
    }
    if ((0x00000020U & (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__inc_list_r))) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__inc_next_w = 5U;
    }
    if ((0x00000010U & (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__inc_list_r))) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__inc_next_w = 4U;
    }
    if ((8U & (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__inc_list_r))) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__inc_next_w = 3U;
    }
    if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__inc_list_r))) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__inc_next_w = 2U;
    }
    if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__inc_list_r))) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__inc_next_w = 1U;
    }
    if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__inc_list_r))) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__inc_next_w = 0U;
    }
    vlSelfRef.milan_datapath__DOT__mon_wire_chans_all_w 
        = (((((0x000000f0U & ((vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__chans_sh_r[7U] 
                               | (- (IData)((0x0fU 
                                             < vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__chans_sh_r[7U])))) 
                              << 4U)) | (0x0000000fU 
                                         & (vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__chans_sh_r[6U] 
                                            | (- (IData)(
                                                         (0x0fU 
                                                          < vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__chans_sh_r[6U])))))) 
             << 0x00000018U) | (((0x000000f0U & ((vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__chans_sh_r[5U] 
                                                  | (- (IData)(
                                                               (0x0fU 
                                                                < vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__chans_sh_r[5U])))) 
                                                 << 4U)) 
                                 | (0x0000000fU & (vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__chans_sh_r[4U] 
                                                   | (- (IData)(
                                                                (0x0fU 
                                                                 < vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__chans_sh_r[4U])))))) 
                                << 0x00000010U)) | 
           ((((0x000000f0U & ((vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__chans_sh_r[3U] 
                               | (- (IData)((0x0fU 
                                             < vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__chans_sh_r[3U])))) 
                              << 4U)) | (0x0000000fU 
                                         & (vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__chans_sh_r[2U] 
                                            | (- (IData)(
                                                         (0x0fU 
                                                          < vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__chans_sh_r[2U])))))) 
             << 8U) | ((0x000000f0U & ((vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__chans_sh_r[1U] 
                                        | (- (IData)(
                                                     (0x0fU 
                                                      < vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__chans_sh_r[1U])))) 
                                       << 4U)) | (0x0000000fU 
                                                  & (vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__chans_sh_r[0U] 
                                                     | (- (IData)(
                                                                  (0x0fU 
                                                                   < vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__chans_sh_r[0U]))))))));
    vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__mreset_any_w = 0U;
    if ((0U != vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__mreset_pend_r[0U])) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__mreset_any_w = 1U;
    }
    if ((0U != vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__mreset_pend_r[1U])) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__mreset_any_w = 1U;
    }
    if ((0U != vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__mreset_pend_r[2U])) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__mreset_any_w = 1U;
    }
    if ((0U != vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__mreset_pend_r[3U])) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__mreset_any_w = 1U;
    }
    if ((0U != vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__mreset_pend_r[4U])) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__mreset_any_w = 1U;
    }
    if ((0U != vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__mreset_pend_r[5U])) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__mreset_any_w = 1U;
    }
    if ((0U != vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__mreset_pend_r[6U])) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__mreset_any_w = 1U;
    }
    if ((0U != vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__mreset_pend_r[7U])) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__mreset_any_w = 1U;
    }
    vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__depkt_any_w = 0U;
    if (((0U != vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_pend_r[0U]) 
         | (0U != vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ddrop_pend_r[0U]))) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__depkt_any_w = 1U;
    }
    if (((0U != vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_pend_r[1U]) 
         | (0U != vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ddrop_pend_r[1U]))) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__depkt_any_w = 1U;
    }
    if (((0U != vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_pend_r[2U]) 
         | (0U != vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ddrop_pend_r[2U]))) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__depkt_any_w = 1U;
    }
    if (((0U != vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_pend_r[3U]) 
         | (0U != vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ddrop_pend_r[3U]))) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__depkt_any_w = 1U;
    }
    if (((0U != vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_pend_r[4U]) 
         | (0U != vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ddrop_pend_r[4U]))) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__depkt_any_w = 1U;
    }
    if (((0U != vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_pend_r[5U]) 
         | (0U != vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ddrop_pend_r[5U]))) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__depkt_any_w = 1U;
    }
    if (((0U != vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_pend_r[6U]) 
         | (0U != vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ddrop_pend_r[6U]))) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__depkt_any_w = 1U;
    }
    if (((0U != vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_pend_r[7U]) 
         | (0U != vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ddrop_pend_r[7U]))) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__depkt_any_w = 1U;
    }
    vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__pdisp_w 
        = ((0U == (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__mst_r)) 
           & (0U != (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__pq_cnt_r)));
    vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__eng_we_w = 0U;
    vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__overflow_reg = 0U;
    vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__good_frame_reg = 0U;
    if (vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_rx__DOT__beat_acc) {
        if (((((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__wr_ptr_reg) 
               == (0x0100U ^ (IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__rd_ptr_reg))) 
              | ((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__wr_ptr_reg) 
                 == (0x0100U ^ (IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__wr_ptr_commit_reg)))) 
             | (IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__drop_frame_reg))) {
            vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__drop_frame_reg = 1U;
            if (vlSelfRef.s_axis_mac_rx_tlast) {
                vlSelfRef.__Vdly__milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__wr_ptr_reg 
                    = vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__wr_ptr_commit_reg;
                vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__drop_frame_reg = 0U;
                vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__overflow_reg = 1U;
            }
        } else {
            __VdlyVal__milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__mem__v0[0U] 
                = (IData)(vlSelfRef.s_axis_mac_rx_tdata);
            __VdlyVal__milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__mem__v0[1U] 
                = (IData)((vlSelfRef.s_axis_mac_rx_tdata 
                           >> 0x00000020U));
            __VdlyVal__milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__mem__v0[2U] 
                = (0x000003ffU & ((((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__fw_user) 
                                    | (IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__mark_frame_reg)) 
                                   << 9U) | ((((IData)(vlSelfRef.s_axis_mac_rx_tlast) 
                                               | (IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__mark_frame_reg)) 
                                              << 8U) 
                                             | (IData)(vlSelfRef.s_axis_mac_rx_tkeep))));
            __VdlyDim0__milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__mem__v0 
                = (0x000000ffU & (IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__wr_ptr_reg));
            vlSelfRef.__VdlySet__milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__mem__v0 = 1U;
            vlSelfRef.__Vdly__milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__wr_ptr_reg 
                = (0x000001ffU & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__wr_ptr_reg)));
            if (vlSelfRef.s_axis_mac_rx_tlast) {
                if (((IData)(vlSelfRef.s_axis_mac_rx_tlast) 
                     & (IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__fw_user))) {
                    vlSelfRef.__Vdly__milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__wr_ptr_reg 
                        = vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__wr_ptr_commit_reg;
                } else {
                    vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__wr_ptr_commit_reg 
                        = (0x000001ffU & ((IData)(1U) 
                                          + (IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__wr_ptr_reg)));
                    vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__good_frame_reg 
                        = vlSelfRef.s_axis_mac_rx_tlast;
                }
            }
        }
    }
    if ((1U & (~ (IData)(vlSelfRef.axis_resetn)))) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__loop_fed_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__wr_ptr_reg = 0U;
        vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__wr_ptr_commit_reg = 0U;
        vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__drop_frame_reg = 0U;
        vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__overflow_reg = 0U;
        vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__good_frame_reg = 0U;
        vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__mark_frame_reg = 0U;
    }
    if ((1U & (~ VL_ONEHOT_I((((IData)(((0x000022f000000000ULL 
                                         == (0x0000ffff00000000ULL 
                                             & vlSelfRef.__VdfgRegularize_h6e95ff9d_0_17)) 
                                        & (0x8100U 
                                           != (0x0000ffffU 
                                               & (IData)(
                                                         (vlSelfRef.__VdfgRegularize_h6e95ff9d_0_17 
                                                          >> 0x00000010U)))))) 
                               << 2U) | (((IData)((0x000022f081000000ULL 
                                                   == 
                                                   (0x0000ffffffff0000ULL 
                                                    & vlSelfRef.__VdfgRegularize_h6e95ff9d_0_17))) 
                                          << 1U) | (IData)(vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__class_map__DOT__gptp_frame))))))) {
        if ((0U != (((IData)(((0x000022f000000000ULL 
                               == (0x0000ffff00000000ULL 
                                   & vlSelfRef.__VdfgRegularize_h6e95ff9d_0_17)) 
                              & (0x8100U != (0x0000ffffU 
                                             & (IData)(
                                                       (vlSelfRef.__VdfgRegularize_h6e95ff9d_0_17 
                                                        >> 0x00000010U)))))) 
                     << 2U) | (((IData)((0x000022f081000000ULL 
                                         == (0x0000ffffffff0000ULL 
                                             & vlSelfRef.__VdfgRegularize_h6e95ff9d_0_17))) 
                                << 1U) | (IData)(vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__class_map__DOT__gptp_frame))))) {
            if (VL_UNLIKELY((vlSymsp->_vm_contextp__->assertOn()))) {
                VL_WRITEF_NX("[%0t] %%Error: traffic_class_map.sv:229: Assertion failed in %m: unique case, but multiple matches found for '1'h1'\n",3, 'M',vlSymsp->name(),"milan_datapath.traffic_controller.classifier.class_map.classify", 'T',-9
                             , '#',64,VL_TIME_UNITED_Q(1000));
                VL_STOP_MT("../../../configs/generated/endstation_ax7101_8x8/../../../hdl/ieee8021q/ts/traffic_class_map.sv", 229, "");
            }
        }
    }
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_95 = (0x0000001fU 
                                                 & (((IData)(3U) 
                                                     * 
                                                     (7U 
                                                      & (vlSelfRef.milan_datapath__DOT__csr__DOT__cls_regen 
                                                         >> (IData)(__VdfgRegularize_h6e95ff9d_0_93)))) 
                                                    & (- (IData)(
                                                                 (0x17U 
                                                                  >= (IData)(__VdfgRegularize_h6e95ff9d_0_93))))));
    if (vlSelfRef.axis_resetn) {
        if (vlSelfRef.s_axi_awready) {
            if ((1U & (~ ((IData)(vlSelfRef.s_axi_awaddr) 
                          >> 0x0000000fU)))) {
                if ((1U & (~ ((IData)(vlSelfRef.s_axi_awaddr) 
                              >> 0x0000000eU)))) {
                    if ((1U & (~ ((IData)(vlSelfRef.s_axi_awaddr) 
                                  >> 0x0000000dU)))) {
                        if ((1U & (~ ((IData)(vlSelfRef.s_axi_awaddr) 
                                      >> 0x0000000cU)))) {
                            if ((1U & (~ ((IData)(vlSelfRef.s_axi_awaddr) 
                                          >> 0x0000000bU)))) {
                                if ((0x00000400U & (IData)(vlSelfRef.s_axi_awaddr))) {
                                    if ((0x00000200U 
                                         & (IData)(vlSelfRef.s_axi_awaddr))) {
                                        if ((0x00000100U 
                                             & (IData)(vlSelfRef.s_axi_awaddr))) {
                                            if ((1U 
                                                 & (~ 
                                                    ((IData)(vlSelfRef.s_axi_awaddr) 
                                                     >> 7U)))) {
                                                if (
                                                    (1U 
                                                     & (~ 
                                                        ((IData)(vlSelfRef.s_axi_awaddr) 
                                                         >> 6U)))) {
                                                    if (
                                                        (1U 
                                                         & (~ 
                                                            ((IData)(vlSelfRef.s_axi_awaddr) 
                                                             >> 5U)))) {
                                                        if (
                                                            (0x00000010U 
                                                             & (IData)(vlSelfRef.s_axi_awaddr))) {
                                                            if (
                                                                (8U 
                                                                 & (IData)(vlSelfRef.s_axi_awaddr))) {
                                                                if (
                                                                    (4U 
                                                                     & (IData)(vlSelfRef.s_axi_awaddr))) {
                                                                    if (
                                                                        (1U 
                                                                         & (~ 
                                                                            ((IData)(vlSelfRef.s_axi_awaddr) 
                                                                             >> 1U)))) {
                                                                        if (
                                                                            (1U 
                                                                             & (~ (IData)(vlSelfRef.s_axi_awaddr)))) {
                                                                            vlSelfRef.milan_datapath__DOT__csr__DOT__link_ctrl 
                                                                                = vlSelfRef.s_axi_wdata;
                                                                        }
                                                                    }
                                                                }
                                                            }
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    } else {
        vlSelfRef.milan_datapath__DOT__csr__DOT__link_ctrl = 1U;
    }
    vlSelfRef.o_mac_reinit = (1U & ((IData)(vlSelfRef.milan_datapath__DOT__link_guard__DOT__guard_rst_r) 
                                    | (vlSelfRef.milan_datapath__DOT__csr__DOT__link_ctrl 
                                       >> 1U)));
    vlSelfRef.milan_datapath__DOT__link_guard__DOT__rx_trans_w 
        = (1U & ((~ (vlSelfRef.milan_datapath__DOT__csr__DOT__link_ctrl 
                     >> 3U)) & VL_REDXOR_32((3U & ((IData)(vlSelfRef.milan_datapath__DOT__link_guard__DOT__rx_sync_r) 
                                                   >> 1U)))));
    vlSelfRef.milan_datapath__DOT__link_guard__DOT__tx_trans_w 
        = (1U & ((~ (vlSelfRef.milan_datapath__DOT__csr__DOT__link_ctrl 
                     >> 3U)) & VL_REDXOR_32((3U & ((IData)(vlSelfRef.milan_datapath__DOT__link_guard__DOT__tx_sync_r) 
                                                   >> 1U)))));
    vlSelfRef.milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__u_tcdc__DOT__rptr_bin_r 
        = ((IData)(vlSelfRef.axis_resetn) ? (IData)(vlSelfRef.milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__u_tcdc__DOT__rptr_bin_n)
            : 0U);
    vlSelfRef.milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__u_tcdc__DOT__rptr_bin_n 
        = (0x0000000fU & ((IData)(vlSelfRef.milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__u_tcdc__DOT__rptr_bin_r) 
                          + ((~ (IData)(vlSelfRef.milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__cap_rempty_w)) 
                             & (IData)(vlSelfRef.milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__cap_ren_r))));
    if (vlSelfRef.axis_resetn) {
        vlSelfRef.milan_datapath__DOT__csr__DOT__stats_rst_p = 0U;
        if (vlSelfRef.s_axi_awready) {
            if ((1U & (~ ((IData)(vlSelfRef.s_axi_awaddr) 
                          >> 0x0000000fU)))) {
                if ((1U & (~ ((IData)(vlSelfRef.s_axi_awaddr) 
                              >> 0x0000000eU)))) {
                    if ((1U & (~ ((IData)(vlSelfRef.s_axi_awaddr) 
                                  >> 0x0000000dU)))) {
                        if ((1U & (~ ((IData)(vlSelfRef.s_axi_awaddr) 
                                      >> 0x0000000cU)))) {
                            if ((1U & (~ ((IData)(vlSelfRef.s_axi_awaddr) 
                                          >> 0x0000000bU)))) {
                                if ((1U & (~ ((IData)(vlSelfRef.s_axi_awaddr) 
                                              >> 0x0000000aU)))) {
                                    if ((0x00000200U 
                                         & (IData)(vlSelfRef.s_axi_awaddr))) {
                                        if ((1U & (~ 
                                                   ((IData)(vlSelfRef.s_axi_awaddr) 
                                                    >> 8U)))) {
                                            if ((1U 
                                                 & (~ 
                                                    ((IData)(vlSelfRef.s_axi_awaddr) 
                                                     >> 7U)))) {
                                                if (
                                                    (1U 
                                                     & (~ 
                                                        ((IData)(vlSelfRef.s_axi_awaddr) 
                                                         >> 6U)))) {
                                                    if (
                                                        (1U 
                                                         & (~ 
                                                            ((IData)(vlSelfRef.s_axi_awaddr) 
                                                             >> 5U)))) {
                                                        if (
                                                            (1U 
                                                             & (~ 
                                                                ((IData)(vlSelfRef.s_axi_awaddr) 
                                                                 >> 4U)))) {
                                                            if (
                                                                (1U 
                                                                 & (~ 
                                                                    ((IData)(vlSelfRef.s_axi_awaddr) 
                                                                     >> 3U)))) {
                                                                if (
                                                                    (1U 
                                                                     & (~ 
                                                                        ((IData)(vlSelfRef.s_axi_awaddr) 
                                                                         >> 2U)))) {
                                                                    if (
                                                                        (1U 
                                                                         & (~ 
                                                                            ((IData)(vlSelfRef.s_axi_awaddr) 
                                                                             >> 1U)))) {
                                                                        if (
                                                                            (1U 
                                                                             & (~ (IData)(vlSelfRef.s_axi_awaddr)))) {
                                                                            if (
                                                                                (2U 
                                                                                & vlSelfRef.s_axi_wdata)) {
                                                                                vlSelfRef.milan_datapath__DOT__csr__DOT__stats_rst_p = 1U;
                                                                            }
                                                                        }
                                                                    }
                                                                }
                                                            }
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
        vlSelfRef.milan_datapath__DOT__speed_q = vlSelfRef.milan_datapath__DOT__speed_sync;
        if (vlSelfRef.milan_datapath__DOT__csr__DOT__cmrd_go_w) {
            vlSelfRef.milan_datapath__DOT__csr__DOT__cmrd_side_r 
                = (1U & (vlSelfRef.milan_datapath__DOT__csr__DOT__chmap_sel 
                         >> 8U));
        }
    } else {
        vlSelfRef.milan_datapath__DOT__speed_q = 2U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__cmrd_side_r = 0U;
    }
    vlSelfRef.milan_datapath__DOT____Vcellinp__chan_map_capture__map_rd_en_i 
        = ((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__cmrd_side_r) 
           & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__cmrd_busy_r));
    vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__lb_sel_w 
        = (vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r
           [(0x0000001fU & ((- (IData)((IData)(milan_datapath__DOT__chan_map_capture__DOT__lb_sel_ok_w))) 
                            & ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_10) 
                               + (0x0000001cU & ((vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r
                                                  [vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__slot_r] 
                                                  >> 8U) 
                                                 << 2U)))))] 
           & (- (QData)((IData)(milan_datapath__DOT__chan_map_capture__DOT__lb_sel_ok_w))));
    vlSelfRef.milan_datapath__DOT__rmap_rd_data_w = 0U;
    if (vlSelfRef.axis_resetn) {
        if (vlSelfRef.milan_datapath__DOT__csr__DOT__cmrd_go_w) {
            vlSelfRef.milan_datapath__DOT__csr__DOT__cmrd_addr_r 
                = (0x0000003fU & vlSelfRef.milan_datapath__DOT__csr__DOT__chmap_sel);
        }
    } else {
        vlSelfRef.milan_datapath__DOT__csr__DOT__cmrd_addr_r = 0U;
    }
    if ((0U == (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__cmrd_addr_r)))) {
        vlSelfRef.milan_datapath__DOT__rmap_rd_data_w 
            = vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__map_r[0U];
    }
    if ((1U == (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__cmrd_addr_r)))) {
        vlSelfRef.milan_datapath__DOT__rmap_rd_data_w 
            = vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__map_r[1U];
    }
    if ((2U == (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__cmrd_addr_r)))) {
        vlSelfRef.milan_datapath__DOT__rmap_rd_data_w 
            = vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__map_r[2U];
    }
    if ((3U == (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__cmrd_addr_r)))) {
        vlSelfRef.milan_datapath__DOT__rmap_rd_data_w 
            = vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__map_r[3U];
    }
    if ((4U == (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__cmrd_addr_r)))) {
        vlSelfRef.milan_datapath__DOT__rmap_rd_data_w 
            = vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__map_r[4U];
    }
    if ((5U == (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__cmrd_addr_r)))) {
        vlSelfRef.milan_datapath__DOT__rmap_rd_data_w 
            = vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__map_r[5U];
    }
    if ((6U == (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__cmrd_addr_r)))) {
        vlSelfRef.milan_datapath__DOT__rmap_rd_data_w 
            = vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__map_r[6U];
    }
    if ((7U == (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__cmrd_addr_r)))) {
        vlSelfRef.milan_datapath__DOT__rmap_rd_data_w 
            = vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__map_r[7U];
    }
    if ((8U == (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__cmrd_addr_r)))) {
        vlSelfRef.milan_datapath__DOT__rmap_rd_data_w 
            = vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__map_r[8U];
    }
    if ((9U == (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__cmrd_addr_r)))) {
        vlSelfRef.milan_datapath__DOT__rmap_rd_data_w 
            = vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__map_r[9U];
    }
    if (vlSelfRef.axis_resetn) {
        if (vlSelfRef.s_axi_awready) {
            if ((1U & (~ ((IData)(vlSelfRef.s_axi_awaddr) 
                          >> 0x0000000fU)))) {
                if ((1U & (~ ((IData)(vlSelfRef.s_axi_awaddr) 
                              >> 0x0000000eU)))) {
                    if ((1U & (~ ((IData)(vlSelfRef.s_axi_awaddr) 
                                  >> 0x0000000dU)))) {
                        if ((1U & (~ ((IData)(vlSelfRef.s_axi_awaddr) 
                                      >> 0x0000000cU)))) {
                            if ((1U & (~ ((IData)(vlSelfRef.s_axi_awaddr) 
                                          >> 0x0000000bU)))) {
                                if ((0x00000400U & (IData)(vlSelfRef.s_axi_awaddr))) {
                                    if ((0x00000200U 
                                         & (IData)(vlSelfRef.s_axi_awaddr))) {
                                        if ((1U & (~ 
                                                   ((IData)(vlSelfRef.s_axi_awaddr) 
                                                    >> 8U)))) {
                                            if ((0x00000080U 
                                                 & (IData)(vlSelfRef.s_axi_awaddr))) {
                                                if (
                                                    (0x00000040U 
                                                     & (IData)(vlSelfRef.s_axi_awaddr))) {
                                                    if (
                                                        (1U 
                                                         & (~ 
                                                            ((IData)(vlSelfRef.s_axi_awaddr) 
                                                             >> 5U)))) {
                                                        if (
                                                            (1U 
                                                             & (~ 
                                                                ((IData)(vlSelfRef.s_axi_awaddr) 
                                                                 >> 4U)))) {
                                                            if (
                                                                (8U 
                                                                 & (IData)(vlSelfRef.s_axi_awaddr))) {
                                                                if (
                                                                    (4U 
                                                                     & (IData)(vlSelfRef.s_axi_awaddr))) {
                                                                    if (
                                                                        (1U 
                                                                         & (~ 
                                                                            ((IData)(vlSelfRef.s_axi_awaddr) 
                                                                             >> 1U)))) {
                                                                        if (
                                                                            (1U 
                                                                             & (~ (IData)(vlSelfRef.s_axi_awaddr)))) {
                                                                            vlSelfRef.milan_datapath__DOT__csr__DOT__maap_ctrl 
                                                                                = vlSelfRef.s_axi_wdata;
                                                                        }
                                                                    }
                                                                }
                                                            }
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    } else {
        vlSelfRef.milan_datapath__DOT__csr__DOT__maap_ctrl = 0x00000800U;
    }
    if ((1U & ((vlSelfRef.milan_datapath__DOT__csr__DOT__maap_ctrl 
                >> 1U) & (~ (IData)(vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__seed_used_r))))) {
        vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT____VlemCall_0__rand_offset 
            = (vlSelfRef.milan_datapath__DOT__csr__DOT__maap_ctrl 
               >> 0x00000010U);
    } else {
        vlSelfRef.__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rand_offset__151__cnt 
            = (0x000000ffU & (vlSelfRef.milan_datapath__DOT__csr__DOT__maap_ctrl 
                              >> 8U));
        vlSelfRef.__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rand_offset__151__rnd 
            = vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lfsr_next_w;
        vlSelfRef.__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rand_offset__151__o 
            = (0x0000ffffU & ((0xfe00U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rand_offset__151__rnd))
                               ? ((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rand_offset__151__rnd) 
                                  - (IData)(0xfe00U))
                               : (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rand_offset__151__rnd)));
        if (((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rand_offset__151__o) 
             > (0x0000ffffU & ((IData)(0xfe00U) - (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rand_offset__151__cnt))))) {
            vlSelfRef.__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rand_offset__151__o 
                = (0x0000ffffU & ((IData)(0xfe00U) 
                                  - (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rand_offset__151__cnt)));
        }
        vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT____VlemCall_0__rand_offset 
            = vlSelfRef.__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rand_offset__151__o;
    }
    vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__new_off_w 
        = vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT____VlemCall_0__rand_offset;
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_7 = (1U 
                                                & ((~ vlSelfRef.milan_datapath__DOT__csr__DOT__maap_ctrl) 
                                                   | (2U 
                                                      == (IData)(vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__state_r))));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_68 = (7U 
                                                 & (vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__chans_r
                                                    [vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__et_r] 
                                                    >> 1U));
    vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__ext_trd_go_w 
        = (((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_67) 
            | ((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rds_busy_r) 
               & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rds_dir_r))) 
           & ((3U == (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__est_r)) 
              | ((~ (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__grant_v_w)) 
                 & (0U == (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__est_r)))));
    vlSelfRef.milan_datapath__DOT__pbk_regs_w[0U] = 
        (((((((3U == (3U & (vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__map_r[9U] 
                            >> 6U))) << 3U) | ((3U 
                                                == 
                                                (3U 
                                                 & (vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__map_r[8U] 
                                                    >> 6U))) 
                                               << 2U)) 
            | (((3U == (3U & (vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__map_r[7U] 
                              >> 6U))) << 1U) | (3U 
                                                 == 
                                                 (3U 
                                                  & (vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__map_r[6U] 
                                                     >> 6U))))) 
           << 0x0000001cU) | (((((3U == (3U & (vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__map_r[5U] 
                                               >> 6U))) 
                                 << 3U) | ((3U == (3U 
                                                   & (vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__map_r[4U] 
                                                      >> 6U))) 
                                           << 2U)) 
                               | (((3U == (3U & (vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__map_r[3U] 
                                                 >> 6U))) 
                                   << 1U) | (3U == 
                                             (3U & 
                                              (vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__map_r[2U] 
                                               >> 6U))))) 
                              << 0x00000018U)) | ((
                                                   ((3U 
                                                     == 
                                                     (3U 
                                                      & (vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__map_r[1U] 
                                                         >> 6U))) 
                                                    << 0x00000017U) 
                                                   | ((3U 
                                                       == 
                                                       (3U 
                                                        & (vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__map_r[0U] 
                                                           >> 6U))) 
                                                      << 0x00000016U)) 
                                                  | (((IData)(vlSelfRef.milan_datapath__DOT____Vcellinp__i2s_feed_mux__phys_armed_i) 
                                                      << 0x00000013U) 
                                                     | (((IData)(vlSelfRef.pb_enable_i) 
                                                         << 0x00000012U) 
                                                        | ((0x00010000U 
                                                            & (vlSelfRef.milan_datapath__DOT__csr__DOT__chmap_ctrl 
                                                               << 0x00000010U)) 
                                                           | (IData)(vlSelfRef.milan_datapath__DOT__pbk_unarmed_w))))));
    vlSelfRef.milan_datapath__DOT__pbk_regs_w[1U] = (IData)((QData)((IData)(vlSelfRef.milan_datapath__DOT__pbk_feeds_w)));
    vlSelfRef.milan_datapath__DOT__pbk_regs_w[2U] = (IData)(
                                                            ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pbk_feeds_w)) 
                                                             >> 0x00000020U));
    if (vlSelfRef.axis_resetn) {
        vlSelfRef.milan_datapath__DOT__csr__DOT__adp_adv_p = 0U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__adp_dep_p = 0U;
        if (vlSelfRef.s_axi_awready) {
            if ((1U & (~ ((IData)(vlSelfRef.s_axi_awaddr) 
                          >> 0x0000000fU)))) {
                if ((1U & (~ ((IData)(vlSelfRef.s_axi_awaddr) 
                              >> 0x0000000eU)))) {
                    if ((1U & (~ ((IData)(vlSelfRef.s_axi_awaddr) 
                                  >> 0x0000000dU)))) {
                        if ((1U & (~ ((IData)(vlSelfRef.s_axi_awaddr) 
                                      >> 0x0000000cU)))) {
                            if ((1U & (~ ((IData)(vlSelfRef.s_axi_awaddr) 
                                          >> 0x0000000bU)))) {
                                if ((0x00000400U & (IData)(vlSelfRef.s_axi_awaddr))) {
                                    if ((0x00000200U 
                                         & (IData)(vlSelfRef.s_axi_awaddr))) {
                                        if ((1U & (~ 
                                                   ((IData)(vlSelfRef.s_axi_awaddr) 
                                                    >> 8U)))) {
                                            if ((1U 
                                                 & (~ 
                                                    ((IData)(vlSelfRef.s_axi_awaddr) 
                                                     >> 7U)))) {
                                                if (
                                                    (0x00000040U 
                                                     & (IData)(vlSelfRef.s_axi_awaddr))) {
                                                    if (
                                                        (1U 
                                                         & (~ 
                                                            ((IData)(vlSelfRef.s_axi_awaddr) 
                                                             >> 5U)))) {
                                                        if (
                                                            (1U 
                                                             & (~ 
                                                                ((IData)(vlSelfRef.s_axi_awaddr) 
                                                                 >> 4U)))) {
                                                            if (
                                                                (1U 
                                                                 & (~ 
                                                                    ((IData)(vlSelfRef.s_axi_awaddr) 
                                                                     >> 3U)))) {
                                                                if (
                                                                    (1U 
                                                                     & (~ 
                                                                        ((IData)(vlSelfRef.s_axi_awaddr) 
                                                                         >> 2U)))) {
                                                                    if (
                                                                        (1U 
                                                                         & (~ 
                                                                            ((IData)(vlSelfRef.s_axi_awaddr) 
                                                                             >> 1U)))) {
                                                                        if (
                                                                            (1U 
                                                                             & (~ (IData)(vlSelfRef.s_axi_awaddr)))) {
                                                                            if (
                                                                                (1U 
                                                                                & vlSelfRef.s_axi_wdata)) {
                                                                                vlSelfRef.milan_datapath__DOT__csr__DOT__adp_adv_p = 1U;
                                                                            }
                                                                            if (
                                                                                (2U 
                                                                                & vlSelfRef.s_axi_wdata)) {
                                                                                vlSelfRef.milan_datapath__DOT__csr__DOT__adp_dep_p = 1U;
                                                                            }
                                                                        }
                                                                    }
                                                                }
                                                            }
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
        if (vlSelfRef.milan_datapath__DOT__adp_adv__DOT__depart_evt_w) {
            vlSelfRef.milan_datapath__DOT__adp_adv__DOT__available_r = 0U;
        } else if ((((IData)(vlSelfRef.milan_datapath__DOT__adp_link_up_p) 
                     & vlSelfRef.milan_datapath__DOT__csr__DOT__adp_ctrl) 
                    | (IData)(vlSelfRef.milan_datapath__DOT__adp_adv__DOT__rearm_fire_w))) {
            vlSelfRef.milan_datapath__DOT__adp_adv__DOT__available_r = 1U;
        }
        vlSelfRef.milan_datapath__DOT__chan_tdm_render__DOT__u_fcdc__DOT__rgray_w1_r 
            = vlSelfRef.milan_datapath__DOT__chan_tdm_render__DOT__u_fcdc__DOT__rptr_gray_r;
        if ((0x0822U == (IData)(vlSelfRef.milan_datapath__DOT__media_tick_cnt_r))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__media_tick_cnt_r = 0U;
            vlSelfRef.milan_datapath__DOT__media_tick_p = 1U;
        } else {
            vlSelfRef.__Vdly__milan_datapath__DOT__media_tick_cnt_r 
                = (0x00000fffU & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__media_tick_cnt_r)));
            vlSelfRef.milan_datapath__DOT__media_tick_p = 0U;
        }
    } else {
        vlSelfRef.milan_datapath__DOT__adp_adv__DOT__available_r = 0U;
        vlSelfRef.milan_datapath__DOT__chan_tdm_render__DOT__u_fcdc__DOT__rgray_w1_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__media_tick_cnt_r = 0U;
        vlSelfRef.milan_datapath__DOT__media_tick_p = 0U;
    }
    vlSelfRef.milan_datapath__DOT__media_tick_cnt_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__media_tick_cnt_r;
    vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__4__KET____DOT__u_cbs__DOT__eng_ge 
        = (vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__4__KET____DOT__u_cbs__DOT__eng_trial 
           >= vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__4__KET____DOT__u_cbs__DOT__eng_den);
    vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__4__KET____DOT__u_cbs__DOT__eng_quo_s 
        = (0x0000ffffffffffffULL & ((IData)(vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__4__KET____DOT__u_cbs__DOT__eng_sign)
                                     ? (- milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__4__KET____DOT__u_cbs__DOT__eng_quo_r)
                                     : milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__4__KET____DOT__u_cbs__DOT__eng_quo_r));
    vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__3__KET____DOT__u_cbs__DOT__eng_ge 
        = (vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__3__KET____DOT__u_cbs__DOT__eng_trial 
           >= vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__3__KET____DOT__u_cbs__DOT__eng_den);
    vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__3__KET____DOT__u_cbs__DOT__eng_quo_s 
        = (0x0000ffffffffffffULL & ((IData)(vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__3__KET____DOT__u_cbs__DOT__eng_sign)
                                     ? (- milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__3__KET____DOT__u_cbs__DOT__eng_quo_r)
                                     : milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__3__KET____DOT__u_cbs__DOT__eng_quo_r));
    vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__2__KET____DOT__u_cbs__DOT__eng_ge 
        = (vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__2__KET____DOT__u_cbs__DOT__eng_trial 
           >= vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__2__KET____DOT__u_cbs__DOT__eng_den);
    vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__2__KET____DOT__u_cbs__DOT__eng_quo_s 
        = (0x0000ffffffffffffULL & ((IData)(vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__2__KET____DOT__u_cbs__DOT__eng_sign)
                                     ? (- milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__2__KET____DOT__u_cbs__DOT__eng_quo_r)
                                     : milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__2__KET____DOT__u_cbs__DOT__eng_quo_r));
    vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__1__KET____DOT__u_cbs__DOT__eng_ge 
        = (vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__1__KET____DOT__u_cbs__DOT__eng_trial 
           >= vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__1__KET____DOT__u_cbs__DOT__eng_den);
    vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__1__KET____DOT__u_cbs__DOT__eng_quo_s 
        = (0x0000ffffffffffffULL & ((IData)(vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__1__KET____DOT__u_cbs__DOT__eng_sign)
                                     ? (- milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__1__KET____DOT__u_cbs__DOT__eng_quo_r)
                                     : milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__1__KET____DOT__u_cbs__DOT__eng_quo_r));
    vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__0__KET____DOT__u_cbs__DOT__eng_ge 
        = (vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__0__KET____DOT__u_cbs__DOT__eng_trial 
           >= vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__0__KET____DOT__u_cbs__DOT__eng_den);
    vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__0__KET____DOT__u_cbs__DOT__eng_quo_s 
        = (0x0000ffffffffffffULL & ((IData)(vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__0__KET____DOT__u_cbs__DOT__eng_sign)
                                     ? (- milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__0__KET____DOT__u_cbs__DOT__eng_quo_r)
                                     : milan_datapath__DOT__traffic_controller__DOT__traffic_shaper__DOT__gen_cbs__BRA__0__KET____DOT__u_cbs__DOT__eng_quo_r));
    vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pown_v_w = 0U;
    milan_datapath__DOT__pkt_slot_w = ((1U & vlSelfRef.milan_datapath__DOT__csr__DOT__chmap_ctrl)
                                        ? (IData)(vlSelfRef.milan_datapath__DOT__cmap_slot_w)
                                        : ((IData)(vlSelfRef.milan_datapath__DOT__aafcap_pv_w)
                                            ? (0x0000000fU 
                                               & (IData)(
                                                         (vlSelfRef.milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__cap_pair_w 
                                                          >> 0x00000030U)))
                                            : (IData)(vlSelfRef.milan_datapath__DOT__pair_zero_fill__DOT__pend_slot_c)));
    if ((((IData)(milan_datapath__DOT__pkt_slot_w) 
          >= vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pbase_w[0U]) 
         & ((IData)(milan_datapath__DOT__pkt_slot_w) 
            < vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pbase_w[1U]))) {
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pown_v_w = 1U;
    }
    if ((((IData)(milan_datapath__DOT__pkt_slot_w) 
          >= vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pbase_w[1U]) 
         & ((IData)(milan_datapath__DOT__pkt_slot_w) 
            < vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pbase_w[2U]))) {
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pown_v_w = 1U;
    }
    if ((((IData)(milan_datapath__DOT__pkt_slot_w) 
          >= vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pbase_w[2U]) 
         & ((IData)(milan_datapath__DOT__pkt_slot_w) 
            < vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pbase_w[3U]))) {
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pown_v_w = 1U;
    }
    if ((((IData)(milan_datapath__DOT__pkt_slot_w) 
          >= vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pbase_w[3U]) 
         & ((IData)(milan_datapath__DOT__pkt_slot_w) 
            < vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pbase_w[4U]))) {
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pown_v_w = 1U;
    }
    if ((((IData)(milan_datapath__DOT__pkt_slot_w) 
          >= vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pbase_w[4U]) 
         & ((IData)(milan_datapath__DOT__pkt_slot_w) 
            < vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pbase_w[5U]))) {
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pown_v_w = 1U;
    }
    if ((((IData)(milan_datapath__DOT__pkt_slot_w) 
          >= vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pbase_w[5U]) 
         & ((IData)(milan_datapath__DOT__pkt_slot_w) 
            < vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pbase_w[6U]))) {
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pown_v_w = 1U;
    }
    vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pown_o_w = 0U;
    if ((((IData)(milan_datapath__DOT__pkt_slot_w) 
          >= vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pbase_w[0U]) 
         & ((IData)(milan_datapath__DOT__pkt_slot_w) 
            < vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pbase_w[1U]))) {
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pown_o_w 
            = (3U & ((IData)(milan_datapath__DOT__pkt_slot_w) 
                     - vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pbase_w[0U]));
    }
    if ((((IData)(milan_datapath__DOT__pkt_slot_w) 
          >= vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pbase_w[1U]) 
         & ((IData)(milan_datapath__DOT__pkt_slot_w) 
            < vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pbase_w[2U]))) {
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pown_o_w 
            = (3U & ((IData)(milan_datapath__DOT__pkt_slot_w) 
                     - vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pbase_w[1U]));
    }
    if ((((IData)(milan_datapath__DOT__pkt_slot_w) 
          >= vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pbase_w[2U]) 
         & ((IData)(milan_datapath__DOT__pkt_slot_w) 
            < vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pbase_w[3U]))) {
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pown_o_w 
            = (3U & ((IData)(milan_datapath__DOT__pkt_slot_w) 
                     - vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pbase_w[2U]));
    }
    if ((((IData)(milan_datapath__DOT__pkt_slot_w) 
          >= vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pbase_w[3U]) 
         & ((IData)(milan_datapath__DOT__pkt_slot_w) 
            < vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pbase_w[4U]))) {
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pown_o_w 
            = (3U & ((IData)(milan_datapath__DOT__pkt_slot_w) 
                     - vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pbase_w[3U]));
    }
    if ((((IData)(milan_datapath__DOT__pkt_slot_w) 
          >= vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pbase_w[4U]) 
         & ((IData)(milan_datapath__DOT__pkt_slot_w) 
            < vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pbase_w[5U]))) {
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pown_o_w 
            = (3U & ((IData)(milan_datapath__DOT__pkt_slot_w) 
                     - vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pbase_w[4U]));
    }
    if ((((IData)(milan_datapath__DOT__pkt_slot_w) 
          >= vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pbase_w[5U]) 
         & ((IData)(milan_datapath__DOT__pkt_slot_w) 
            < vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pbase_w[6U]))) {
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pown_o_w 
            = (3U & ((IData)(milan_datapath__DOT__pkt_slot_w) 
                     - vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pbase_w[5U]));
    }
    if ((((IData)(milan_datapath__DOT__pkt_slot_w) 
          >= vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pbase_w[6U]) 
         & ((IData)(milan_datapath__DOT__pkt_slot_w) 
            < vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pbase_w[7U]))) {
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pown_v_w = 1U;
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pown_o_w 
            = (3U & ((IData)(milan_datapath__DOT__pkt_slot_w) 
                     - vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pbase_w[6U]));
    }
    vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pown_t_w = 0U;
    if ((((IData)(milan_datapath__DOT__pkt_slot_w) 
          >= vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pbase_w[0U]) 
         & ((IData)(milan_datapath__DOT__pkt_slot_w) 
            < vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pbase_w[1U]))) {
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pown_t_w = 0U;
    }
    if ((((IData)(milan_datapath__DOT__pkt_slot_w) 
          >= vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pbase_w[1U]) 
         & ((IData)(milan_datapath__DOT__pkt_slot_w) 
            < vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pbase_w[2U]))) {
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pown_t_w = 1U;
    }
    if ((((IData)(milan_datapath__DOT__pkt_slot_w) 
          >= vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pbase_w[2U]) 
         & ((IData)(milan_datapath__DOT__pkt_slot_w) 
            < vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pbase_w[3U]))) {
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pown_t_w = 2U;
    }
    if ((((IData)(milan_datapath__DOT__pkt_slot_w) 
          >= vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pbase_w[3U]) 
         & ((IData)(milan_datapath__DOT__pkt_slot_w) 
            < vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pbase_w[4U]))) {
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pown_t_w = 3U;
    }
    if ((((IData)(milan_datapath__DOT__pkt_slot_w) 
          >= vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pbase_w[4U]) 
         & ((IData)(milan_datapath__DOT__pkt_slot_w) 
            < vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pbase_w[5U]))) {
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pown_t_w = 4U;
    }
    if ((((IData)(milan_datapath__DOT__pkt_slot_w) 
          >= vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pbase_w[5U]) 
         & ((IData)(milan_datapath__DOT__pkt_slot_w) 
            < vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pbase_w[6U]))) {
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pown_t_w = 5U;
    }
    if ((((IData)(milan_datapath__DOT__pkt_slot_w) 
          >= vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pbase_w[6U]) 
         & ((IData)(milan_datapath__DOT__pkt_slot_w) 
            < vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pbase_w[7U]))) {
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pown_t_w = 6U;
    }
    if ((((IData)(milan_datapath__DOT__pkt_slot_w) 
          >= vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pbase_w[7U]) 
         & ((IData)(milan_datapath__DOT__pkt_slot_w) 
            < vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pbase_w[8U]))) {
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pown_v_w = 1U;
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pown_o_w 
            = (3U & ((IData)(milan_datapath__DOT__pkt_slot_w) 
                     - vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pbase_w[7U]));
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pown_t_w = 7U;
    }
    vlSelfRef.milan_datapath__DOT__i2s_feed_chans_w 
        = ((1U & vlSelfRef.milan_datapath__DOT__csr__DOT__chmap_ctrl)
            ? 2U : (IData)(vlSelfRef.milan_datapath__DOT__mon_wire_chans_w));
    vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__c_eff_w 
        = (((0U == (IData)(vlSelfRef.milan_datapath__DOT__i2s_feed_chans_w)) 
            | (8U < (IData)(vlSelfRef.milan_datapath__DOT__i2s_feed_chans_w)))
            ? 2U : (7U & (IData)(vlSelfRef.milan_datapath__DOT__i2s_feed_chans_w)));
    vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__mux_queues__DOT__store_axis_int_to_temp = 0U;
    if (vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__mux_queues__DOT__m_axis_tready_int_reg) {
        if ((1U & ((0U != ((IData)(vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__dm_tready) 
                           & (IData)(vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__mux_queues__DOT__m_axis_tvalid_reg))) 
                   | (~ (0U != (IData)(vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__mux_queues__DOT__m_axis_tvalid_reg)))))) {
            vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__mux_queues__DOT__store_axis_int_to_output = 1U;
        }
        if ((1U & (~ ((0U != ((IData)(vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__dm_tready) 
                              & (IData)(vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__mux_queues__DOT__m_axis_tvalid_reg))) 
                      | (~ (0U != (IData)(vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__mux_queues__DOT__m_axis_tvalid_reg))))))) {
            vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__mux_queues__DOT__store_axis_int_to_temp = 1U;
        }
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__eth_packet_buffer__DOT__m_axis_pipe_reg__v0) {
        vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__eth_packet_buffer__DOT__m_axis_pipe_reg[1U][0U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__eth_packet_buffer__DOT__m_axis_pipe_reg__v0[0U];
        vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__eth_packet_buffer__DOT__m_axis_pipe_reg[1U][1U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__eth_packet_buffer__DOT__m_axis_pipe_reg__v0[1U];
        vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__eth_packet_buffer__DOT__m_axis_pipe_reg[1U][2U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__eth_packet_buffer__DOT__m_axis_pipe_reg__v0[2U];
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__eth_packet_buffer__DOT__m_axis_pipe_reg__v1) {
        vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__eth_packet_buffer__DOT__m_axis_pipe_reg[0U][0U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__eth_packet_buffer__DOT__m_axis_pipe_reg__v1[0U];
        vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__eth_packet_buffer__DOT__m_axis_pipe_reg[0U][1U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__eth_packet_buffer__DOT__m_axis_pipe_reg__v1[1U];
        vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__eth_packet_buffer__DOT__m_axis_pipe_reg[0U][2U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__eth_packet_buffer__DOT__m_axis_pipe_reg__v1[2U];
    }
    if (vlSelfRef.axis_resetn) {
        if (vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ext_wr_ok_w) {
            vlSelfRef.milan_datapath__DOT__csr__DOT__lctx_wr_p_r = 0U;
        }
        if (vlSelfRef.milan_datapath__DOT__tctx_wr_rdy_w) {
            vlSelfRef.milan_datapath__DOT__csr__DOT__tctx_wr_p_r = 0U;
        }
        if (vlSelfRef.s_axi_awready) {
            if ((1U & (~ ((IData)(vlSelfRef.s_axi_awaddr) 
                          >> 0x0000000fU)))) {
                if ((1U & (~ ((IData)(vlSelfRef.s_axi_awaddr) 
                              >> 0x0000000eU)))) {
                    if ((1U & (~ ((IData)(vlSelfRef.s_axi_awaddr) 
                                  >> 0x0000000dU)))) {
                        if ((1U & (~ ((IData)(vlSelfRef.s_axi_awaddr) 
                                      >> 0x0000000cU)))) {
                            if ((0x00000800U & (IData)(vlSelfRef.s_axi_awaddr))) {
                                if ((1U & (~ ((IData)(vlSelfRef.s_axi_awaddr) 
                                              >> 0x0000000aU)))) {
                                    if ((1U & (~ ((IData)(vlSelfRef.s_axi_awaddr) 
                                                  >> 9U)))) {
                                        if ((1U & (~ 
                                                   ((IData)(vlSelfRef.s_axi_awaddr) 
                                                    >> 8U)))) {
                                            if ((1U 
                                                 & (~ 
                                                    ((IData)(vlSelfRef.s_axi_awaddr) 
                                                     >> 7U)))) {
                                                if (
                                                    (1U 
                                                     & (~ 
                                                        ((IData)(vlSelfRef.s_axi_awaddr) 
                                                         >> 6U)))) {
                                                    if (
                                                        (0x00000020U 
                                                         & (IData)(vlSelfRef.s_axi_awaddr))) {
                                                        if (
                                                            (1U 
                                                             & (~ 
                                                                ((IData)(vlSelfRef.s_axi_awaddr) 
                                                                 >> 4U)))) {
                                                            if (
                                                                (8U 
                                                                 & (IData)(vlSelfRef.s_axi_awaddr))) {
                                                                if (
                                                                    (1U 
                                                                     & (~ 
                                                                        ((IData)(vlSelfRef.s_axi_awaddr) 
                                                                         >> 2U)))) {
                                                                    if (
                                                                        (1U 
                                                                         & (~ 
                                                                            ((IData)(vlSelfRef.s_axi_awaddr) 
                                                                             >> 1U)))) {
                                                                        if (
                                                                            (1U 
                                                                             & (~ (IData)(vlSelfRef.s_axi_awaddr)))) {
                                                                            if (
                                                                                ((8U 
                                                                                > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__strm_idx_r)) 
                                                                                & (~ (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__strm_dir_r)))) {
                                                                                vlSelfRef.milan_datapath__DOT__csr__DOT__lctx_wr_p_r = 1U;
                                                                                vlSelfRef.milan_datapath__DOT__csr__DOT__lctx_wr_addr_r 
                                                                                = 
                                                                                (3U 
                                                                                | (0x000000e0U 
                                                                                & ((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__strm_idx_r) 
                                                                                << 5U)));
                                                                                vlSelfRef.milan_datapath__DOT__csr__DOT__lctx_wr_data_r 
                                                                                = vlSelfRef.s_axi_wdata;
                                                                            }
                                                                        }
                                                                    }
                                                                }
                                                            } else if (
                                                                       (4U 
                                                                        & (IData)(vlSelfRef.s_axi_awaddr))) {
                                                                if (
                                                                    (1U 
                                                                     & (~ 
                                                                        ((IData)(vlSelfRef.s_axi_awaddr) 
                                                                         >> 1U)))) {
                                                                    if (
                                                                        (1U 
                                                                         & (~ (IData)(vlSelfRef.s_axi_awaddr)))) {
                                                                        if (
                                                                            ((8U 
                                                                              > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__strm_idx_r)) 
                                                                             & (~ (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__strm_dir_r)))) {
                                                                            vlSelfRef.milan_datapath__DOT__csr__DOT__lctx_wr_p_r = 1U;
                                                                            vlSelfRef.milan_datapath__DOT__csr__DOT__lctx_wr_addr_r 
                                                                                = 
                                                                                (2U 
                                                                                | (0x000000e0U 
                                                                                & ((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__strm_idx_r) 
                                                                                << 5U)));
                                                                            vlSelfRef.milan_datapath__DOT__csr__DOT__lctx_wr_data_r 
                                                                                = vlSelfRef.s_axi_wdata;
                                                                        }
                                                                    }
                                                                }
                                                            } else if (
                                                                       (1U 
                                                                        & (~ 
                                                                           ((IData)(vlSelfRef.s_axi_awaddr) 
                                                                            >> 1U)))) {
                                                                if (
                                                                    (1U 
                                                                     & (~ (IData)(vlSelfRef.s_axi_awaddr)))) {
                                                                    if (
                                                                        (8U 
                                                                         > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__strm_idx_r))) {
                                                                        if (vlSelfRef.milan_datapath__DOT__csr__DOT__strm_dir_r) {
                                                                            if (
                                                                                (0U 
                                                                                == (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__strm_idx_r))) {
                                                                                vlSelfRef.milan_datapath__DOT__csr__DOT__aaf_dmhi 
                                                                                = vlSelfRef.s_axi_wdata;
                                                                            } else {
                                                                                vlSelfRef.milan_datapath__DOT__csr__DOT__tctx_wr_p_r = 1U;
                                                                                vlSelfRef.milan_datapath__DOT__csr__DOT__tctx_wr_addr_r 
                                                                                = 
                                                                                (2U 
                                                                                | (0x00000070U 
                                                                                & ((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__strm_idx_r) 
                                                                                << 4U)));
                                                                                vlSelfRef.milan_datapath__DOT__csr__DOT__tctx_wr_data_r 
                                                                                = vlSelfRef.s_axi_wdata;
                                                                            }
                                                                        }
                                                                    }
                                                                }
                                                            }
                                                        }
                                                    } else if (
                                                               (0x00000010U 
                                                                & (IData)(vlSelfRef.s_axi_awaddr))) {
                                                        if (
                                                            (8U 
                                                             & (IData)(vlSelfRef.s_axi_awaddr))) {
                                                            if (
                                                                (4U 
                                                                 & (IData)(vlSelfRef.s_axi_awaddr))) {
                                                                if (
                                                                    (1U 
                                                                     & (~ 
                                                                        ((IData)(vlSelfRef.s_axi_awaddr) 
                                                                         >> 1U)))) {
                                                                    if (
                                                                        (1U 
                                                                         & (~ (IData)(vlSelfRef.s_axi_awaddr)))) {
                                                                        if (
                                                                            (8U 
                                                                             > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__strm_idx_r))) {
                                                                            if (vlSelfRef.milan_datapath__DOT__csr__DOT__strm_dir_r) {
                                                                                if (
                                                                                (0U 
                                                                                == (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__strm_idx_r))) {
                                                                                vlSelfRef.milan_datapath__DOT__csr__DOT__aaf_dmlo 
                                                                                = vlSelfRef.s_axi_wdata;
                                                                                } else {
                                                                                vlSelfRef.milan_datapath__DOT__csr__DOT__tctx_wr_p_r = 1U;
                                                                                vlSelfRef.milan_datapath__DOT__csr__DOT__tctx_wr_addr_r 
                                                                                = 
                                                                                (1U 
                                                                                | (0x00000070U 
                                                                                & ((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__strm_idx_r) 
                                                                                << 4U)));
                                                                                vlSelfRef.milan_datapath__DOT__csr__DOT__tctx_wr_data_r 
                                                                                = vlSelfRef.s_axi_wdata;
                                                                                }
                                                                            }
                                                                        }
                                                                    }
                                                                }
                                                            } else if (
                                                                       (1U 
                                                                        & (~ 
                                                                           ((IData)(vlSelfRef.s_axi_awaddr) 
                                                                            >> 1U)))) {
                                                                if (
                                                                    (1U 
                                                                     & (~ (IData)(vlSelfRef.s_axi_awaddr)))) {
                                                                    if (
                                                                        (8U 
                                                                         > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__strm_idx_r))) {
                                                                        if (
                                                                            (1U 
                                                                             & (~ (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__strm_dir_r)))) {
                                                                            vlSelfRef.milan_datapath__DOT__csr__DOT__lctx_wr_p_r = 1U;
                                                                            vlSelfRef.milan_datapath__DOT__csr__DOT__lctx_wr_addr_r 
                                                                                = 
                                                                                (1U 
                                                                                | (0x000000e0U 
                                                                                & ((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__strm_idx_r) 
                                                                                << 5U)));
                                                                            vlSelfRef.milan_datapath__DOT__csr__DOT__lctx_wr_data_r 
                                                                                = vlSelfRef.s_axi_wdata;
                                                                        }
                                                                    }
                                                                }
                                                            }
                                                        } else if (
                                                                   (4U 
                                                                    & (IData)(vlSelfRef.s_axi_awaddr))) {
                                                            if (
                                                                (1U 
                                                                 & (~ 
                                                                    ((IData)(vlSelfRef.s_axi_awaddr) 
                                                                     >> 1U)))) {
                                                                if (
                                                                    (1U 
                                                                     & (~ (IData)(vlSelfRef.s_axi_awaddr)))) {
                                                                    if (
                                                                        (8U 
                                                                         > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__strm_idx_r))) {
                                                                        if (
                                                                            (1U 
                                                                             & (~ (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__strm_dir_r)))) {
                                                                            vlSelfRef.milan_datapath__DOT__csr__DOT__lctx_wr_p_r = 1U;
                                                                            vlSelfRef.milan_datapath__DOT__csr__DOT__lctx_wr_addr_r 
                                                                                = 
                                                                                (0x000000e0U 
                                                                                & ((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__strm_idx_r) 
                                                                                << 5U));
                                                                            vlSelfRef.milan_datapath__DOT__csr__DOT__lctx_wr_data_r 
                                                                                = vlSelfRef.s_axi_wdata;
                                                                        }
                                                                    }
                                                                }
                                                            }
                                                        } else if (
                                                                   (1U 
                                                                    & (~ 
                                                                       ((IData)(vlSelfRef.s_axi_awaddr) 
                                                                        >> 1U)))) {
                                                            if (
                                                                (1U 
                                                                 & (~ (IData)(vlSelfRef.s_axi_awaddr)))) {
                                                                if (
                                                                    (8U 
                                                                     > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__strm_idx_r))) {
                                                                    if (vlSelfRef.milan_datapath__DOT__csr__DOT__strm_dir_r) {
                                                                        if (
                                                                            (0U 
                                                                             == (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__strm_idx_r))) {
                                                                            vlSelfRef.__Vdly__milan_datapath__DOT__csr__DOT__aaf_ctrl 
                                                                                = 
                                                                                ((0xfffffffeU 
                                                                                & vlSelfRef.milan_datapath__DOT__csr__DOT__aaf_ctrl) 
                                                                                | (1U 
                                                                                & vlSelfRef.s_axi_wdata));
                                                                        } else {
                                                                            vlSelfRef.milan_datapath__DOT__csr__DOT__tctx_wr_p_r = 1U;
                                                                            vlSelfRef.milan_datapath__DOT__csr__DOT__tctx_wr_addr_r 
                                                                                = 
                                                                                (0x00000070U 
                                                                                & ((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__strm_idx_r) 
                                                                                << 4U));
                                                                            vlSelfRef.milan_datapath__DOT__csr__DOT__tctx_wr_data_r 
                                                                                = vlSelfRef.s_axi_wdata;
                                                                        }
                                                                    } else {
                                                                        vlSelfRef.milan_datapath__DOT__csr__DOT__lctx_wr_p_r = 1U;
                                                                        vlSelfRef.milan_datapath__DOT__csr__DOT__lctx_wr_addr_r 
                                                                            = 
                                                                            (4U 
                                                                             | (0x000000e0U 
                                                                                & ((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__strm_idx_r) 
                                                                                << 5U)));
                                                                        vlSelfRef.milan_datapath__DOT__csr__DOT__lctx_wr_data_r 
                                                                            = vlSelfRef.s_axi_wdata;
                                                                    }
                                                                }
                                                            }
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            } else if ((0x00000400U 
                                        & (IData)(vlSelfRef.s_axi_awaddr))) {
                                if ((0x00000200U & (IData)(vlSelfRef.s_axi_awaddr))) {
                                    if ((1U & (~ ((IData)(vlSelfRef.s_axi_awaddr) 
                                                  >> 8U)))) {
                                        if ((1U & (~ 
                                                   ((IData)(vlSelfRef.s_axi_awaddr) 
                                                    >> 7U)))) {
                                            if ((0x00000040U 
                                                 & (IData)(vlSelfRef.s_axi_awaddr))) {
                                                if (
                                                    (1U 
                                                     & (~ 
                                                        ((IData)(vlSelfRef.s_axi_awaddr) 
                                                         >> 5U)))) {
                                                    if (
                                                        (0x00000010U 
                                                         & (IData)(vlSelfRef.s_axi_awaddr))) {
                                                        if (
                                                            (8U 
                                                             & (IData)(vlSelfRef.s_axi_awaddr))) {
                                                            if (
                                                                (4U 
                                                                 & (IData)(vlSelfRef.s_axi_awaddr))) {
                                                                if (
                                                                    (1U 
                                                                     & (~ 
                                                                        ((IData)(vlSelfRef.s_axi_awaddr) 
                                                                         >> 1U)))) {
                                                                    if (
                                                                        (1U 
                                                                         & (~ (IData)(vlSelfRef.s_axi_awaddr)))) {
                                                                        vlSelfRef.milan_datapath__DOT__csr__DOT__aaf_dmhi 
                                                                            = vlSelfRef.s_axi_wdata;
                                                                    }
                                                                }
                                                            } else if (
                                                                       (1U 
                                                                        & (~ 
                                                                           ((IData)(vlSelfRef.s_axi_awaddr) 
                                                                            >> 1U)))) {
                                                                if (
                                                                    (1U 
                                                                     & (~ (IData)(vlSelfRef.s_axi_awaddr)))) {
                                                                    vlSelfRef.milan_datapath__DOT__csr__DOT__aaf_dmlo 
                                                                        = vlSelfRef.s_axi_wdata;
                                                                }
                                                            }
                                                        } else if (
                                                                   (4U 
                                                                    & (IData)(vlSelfRef.s_axi_awaddr))) {
                                                            if (
                                                                (1U 
                                                                 & (~ 
                                                                    ((IData)(vlSelfRef.s_axi_awaddr) 
                                                                     >> 1U)))) {
                                                                if (
                                                                    (1U 
                                                                     & (~ (IData)(vlSelfRef.s_axi_awaddr)))) {
                                                                    vlSelfRef.__Vdly__milan_datapath__DOT__csr__DOT__aaf_ctrl 
                                                                        = vlSelfRef.s_axi_wdata;
                                                                }
                                                            }
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
        if ((2U == (((IData)(vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_rx__DOT__rec_push) 
                     << 1U) | (IData)(vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_rx__DOT__pop_r)))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_rx__DOT__rec_lvl 
                = (3U & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_rx__DOT__rec_lvl)));
        } else if ((1U == (((IData)(vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_rx__DOT__rec_push) 
                            << 1U) | (IData)(vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_rx__DOT__pop_r)))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_rx__DOT__rec_lvl 
                = (3U & ((IData)(vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_rx__DOT__rec_lvl) 
                         - (IData)(1U)));
        }
        if (((IData)(vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_rx__DOT__rec_push) 
             & ((0U == (IData)(vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_rx__DOT__rec_lvl)) 
                | ((1U == (IData)(vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_rx__DOT__rec_lvl)) 
                   & (IData)(vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_rx__DOT__pop_r))))) {
            vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_rx__DOT__q0_ts 
                = vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_rx__DOT__ts_sop;
            vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_rx__DOT__q0_seq 
                = vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_rx__DOT__ptp_seq_id;
            vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_rx__DOT__q0_mt 
                = vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_rx__DOT__msg_type;
        } else if (vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_rx__DOT__rec_push) {
            vlSelfRef.__Vdly__milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_rx__DOT__q1_ts 
                = vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_rx__DOT__ts_sop;
            vlSelfRef.__Vdly__milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_rx__DOT__q1_seq 
                = vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_rx__DOT__ptp_seq_id;
            vlSelfRef.__Vdly__milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_rx__DOT__q1_mt 
                = vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_rx__DOT__msg_type;
        } else if (((IData)(vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_rx__DOT__pop_r) 
                    & (2U == (IData)(vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_rx__DOT__rec_lvl)))) {
            vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_rx__DOT__q0_ts 
                = vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_rx__DOT__q1_ts;
            vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_rx__DOT__q0_seq 
                = vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_rx__DOT__q1_seq;
            vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_rx__DOT__q0_mt 
                = vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_rx__DOT__q1_mt;
        }
        vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_rx__DOT__pop_r 
            = vlSelfRef.__Vdly__milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_rx__DOT__pop_r;
        vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_rx__DOT__q1_ts 
            = vlSelfRef.__Vdly__milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_rx__DOT__q1_ts;
        vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_rx__DOT__q1_seq 
            = vlSelfRef.__Vdly__milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_rx__DOT__q1_seq;
        vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_rx__DOT__q1_mt 
            = vlSelfRef.__Vdly__milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_rx__DOT__q1_mt;
        vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_rx__DOT__rec_lvl 
            = vlSelfRef.__Vdly__milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_rx__DOT__rec_lvl;
        if ((2U == (((IData)(vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_tx__DOT__rec_push) 
                     << 1U) | (IData)(vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_tx__DOT__pop_r)))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_tx__DOT__rec_lvl 
                = (3U & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_tx__DOT__rec_lvl)));
        } else if ((1U == (((IData)(vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_tx__DOT__rec_push) 
                            << 1U) | (IData)(vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_tx__DOT__pop_r)))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_tx__DOT__rec_lvl 
                = (3U & ((IData)(vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_tx__DOT__rec_lvl) 
                         - (IData)(1U)));
        }
        if (((IData)(vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_tx__DOT__rec_push) 
             & ((0U == (IData)(vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_tx__DOT__rec_lvl)) 
                | ((1U == (IData)(vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_tx__DOT__rec_lvl)) 
                   & (IData)(vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_tx__DOT__pop_r))))) {
            vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_tx__DOT__q0_ts 
                = vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_tx__DOT__ts_sop;
            vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_tx__DOT__q0_seq 
                = vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_tx__DOT__ptp_seq_id;
            vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_tx__DOT__q0_mt 
                = vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_tx__DOT__msg_type;
        } else if (vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_tx__DOT__rec_push) {
            vlSelfRef.__Vdly__milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_tx__DOT__q1_ts 
                = vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_tx__DOT__ts_sop;
            vlSelfRef.__Vdly__milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_tx__DOT__q1_seq 
                = vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_tx__DOT__ptp_seq_id;
            vlSelfRef.__Vdly__milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_tx__DOT__q1_mt 
                = vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_tx__DOT__msg_type;
        } else if (((IData)(vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_tx__DOT__pop_r) 
                    & (2U == (IData)(vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_tx__DOT__rec_lvl)))) {
            vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_tx__DOT__q0_ts 
                = vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_tx__DOT__q1_ts;
            vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_tx__DOT__q0_seq 
                = vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_tx__DOT__q1_seq;
            vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_tx__DOT__q0_mt 
                = vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_tx__DOT__q1_mt;
        }
    } else {
        vlSelfRef.__Vdly__milan_datapath__DOT__csr__DOT__aaf_ctrl = 0x00020000U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__aaf_dmlo = 0xf000fe01U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__aaf_dmhi = 0x000091e0U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__lctx_wr_p_r = 0U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__lctx_wr_addr_r = 0U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__lctx_wr_data_r = 0U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__tctx_wr_p_r = 0U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__tctx_wr_addr_r = 0U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__tctx_wr_data_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_rx__DOT__rec_lvl = 0U;
        vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_rx__DOT__pop_r 
            = vlSelfRef.__Vdly__milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_rx__DOT__pop_r;
        vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_rx__DOT__q1_ts 
            = vlSelfRef.__Vdly__milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_rx__DOT__q1_ts;
        vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_rx__DOT__q1_seq 
            = vlSelfRef.__Vdly__milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_rx__DOT__q1_seq;
        vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_rx__DOT__q1_mt 
            = vlSelfRef.__Vdly__milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_rx__DOT__q1_mt;
        vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_rx__DOT__rec_lvl 
            = vlSelfRef.__Vdly__milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_rx__DOT__rec_lvl;
        vlSelfRef.__Vdly__milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_tx__DOT__rec_lvl = 0U;
    }
    vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_tx__DOT__pop_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_tx__DOT__pop_r;
    vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_tx__DOT__q1_ts 
        = vlSelfRef.__Vdly__milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_tx__DOT__q1_ts;
    vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_tx__DOT__q1_seq 
        = vlSelfRef.__Vdly__milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_tx__DOT__q1_seq;
    vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_tx__DOT__q1_mt 
        = vlSelfRef.__Vdly__milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_tx__DOT__q1_mt;
    vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_tx__DOT__rec_lvl 
        = vlSelfRef.__Vdly__milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_tx__DOT__rec_lvl;
    vlSelfRef.milan_datapath__DOT__csr__DOT__rds_done_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rds_busy_r) 
           & ((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rds_valid_w) 
              & (0U == (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rds_cyc_r))));
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__lctx_r__v0) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__lctx_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__avtp_rx_monitor__DOT__lctx_r__v0] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__lctx_r__v0;
    }
    vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__eng_waddr_w = 0U;
    if ((4U == (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__mst_r))) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__eng_we_w = 1U;
        if ((0U == (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__wrph_r))) {
            vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__189__s 
                = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ev_s_r;
            vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__189__Vfuncout 
                = (8U | ((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__189__s) 
                         << 5U));
            vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__eng_waddr_w 
                = vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__189__Vfuncout;
        } else if ((1U == (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__wrph_r))) {
            vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__190__s 
                = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ev_s_r;
            vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__190__Vfuncout 
                = (9U | ((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__190__s) 
                         << 5U));
            vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__eng_waddr_w 
                = vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__190__Vfuncout;
        } else {
            vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__191__s 
                = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ev_s_r;
            vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__191__Vfuncout 
                = (0x0aU | ((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__191__s) 
                            << 5U));
            vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__eng_waddr_w 
                = vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__191__Vfuncout;
        }
    } else if ((5U == (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__mst_r))) {
        if (vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__w11_mode_r) {
            if (vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__inc_rd_q_r) {
                vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__eng_we_w = 1U;
                vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__192__s 
                    = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ev_s_r;
                vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__192__Vfuncout 
                    = (0x0bU | ((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__192__s) 
                                << 5U));
                vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__eng_waddr_w 
                    = vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__192__Vfuncout;
            }
        } else if (vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__sil_mode_r) {
            if ((1U == (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__wrph_r))) {
                vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__eng_we_w = 1U;
                vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__193__s 
                    = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ev_s_r;
                vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__193__Vfuncout 
                    = (0x11U | ((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__193__s) 
                                << 5U));
                vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__eng_waddr_w 
                    = vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__193__Vfuncout;
            } else if ((3U == (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__wrph_r))) {
                vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__eng_we_w = 1U;
                vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__194__s 
                    = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ev_s_r;
                vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__194__Vfuncout 
                    = (8U | ((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__194__s) 
                             << 5U));
                vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__eng_waddr_w 
                    = vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__194__Vfuncout;
            }
        } else if (vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__bind_zero_r) {
            vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__eng_we_w = 1U;
            vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__195__w 
                = (0x10U | (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__zero_idx_r));
            vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__195__s 
                = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ev_s_r;
            vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__195__Vfuncout 
                = (((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__195__s) 
                    << 5U) | (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__195__w));
            vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__eng_waddr_w 
                = vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__195__Vfuncout;
        } else if (((0U != (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__inc_list_r)) 
                    & (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__inc_rd_q_r))) {
            vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__eng_we_w = 1U;
            vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__196__w 
                = (0x10U | (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__inc_next_w));
            vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__196__s 
                = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ev_s_r;
            vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__196__Vfuncout 
                = (((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__196__s) 
                    << 5U) | (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__196__w));
            vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__eng_waddr_w 
                = vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__196__Vfuncout;
        }
    } else if ((7U == (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__mst_r))) {
        if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__wrph_r) 
                      >> 3U)))) {
            if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__wrph_r))) {
                if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__wrph_r) 
                              >> 1U)))) {
                    if ((1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__wrph_r)))) {
                        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__eng_we_w = 1U;
                        vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__197__s 
                            = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ev_s_r;
                        vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__197__Vfuncout 
                            = (3U | ((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__197__s) 
                                     << 5U));
                        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__eng_waddr_w 
                            = vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__197__Vfuncout;
                    }
                }
            } else {
                vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__eng_we_w = 1U;
                if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__wrph_r))) {
                    if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__wrph_r))) {
                        vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__198__s 
                            = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ev_s_r;
                        vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__198__Vfuncout 
                            = (2U | ((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__198__s) 
                                     << 5U));
                        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__eng_waddr_w 
                            = vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__198__Vfuncout;
                    } else {
                        vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__199__s 
                            = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ev_s_r;
                        vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__199__Vfuncout 
                            = (1U | ((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__199__s) 
                                     << 5U));
                        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__eng_waddr_w 
                            = vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__199__Vfuncout;
                    }
                } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__wrph_r))) {
                    vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__200__s 
                        = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ev_s_r;
                    vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__200__Vfuncout 
                        = ((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__200__s) 
                           << 5U);
                    vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__eng_waddr_w 
                        = vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__200__Vfuncout;
                } else {
                    vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__201__s 
                        = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ev_s_r;
                    vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__201__Vfuncout 
                        = (8U | ((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__201__s) 
                                 << 5U));
                    vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__eng_waddr_w 
                        = vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__201__Vfuncout;
                }
            }
        }
    }
    if (vlSelfRef.axis_resetn) {
        if ((0x0001869fU <= vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ms_div_r)) {
            vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__ms_div_r = 0U;
            vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ms_tick_r = 1U;
        } else {
            vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__ms_div_r 
                = (0x0001ffffU & ((IData)(1U) + vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ms_div_r));
            vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ms_tick_r = 0U;
        }
    } else {
        vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__ms_div_r = 0U;
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ms_tick_r = 0U;
    }
    vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ms_div_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__ms_div_r;
    vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__rd_ptr_reg 
        = vlSelfRef.__Vdly__milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__rd_ptr_reg;
    vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__wr_ptr_reg 
        = vlSelfRef.__Vdly__milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__wr_ptr_reg;
    vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__fw_user 
        = (1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__avtprx_accept_p_w) 
                    | (IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__good_r))));
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__mem__v0) {
        vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__mem[__VdlyDim0__milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__mem__v0][0U] 
            = __VdlyVal__milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__mem__v0[0U];
        vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__mem[__VdlyDim0__milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__mem__v0][1U] 
            = __VdlyVal__milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__mem__v0[1U];
        vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__mem[__VdlyDim0__milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__mem__v0][2U] 
            = __VdlyVal__milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__mem__v0[2U];
    }
    if (vlSelfRef.axis_resetn) {
        vlSelfRef.milan_datapath__DOT__strtbl_bind_rise_w 
            = ((IData)(vlSelfRef.milan_datapath__DOT__strtbl_en_w) 
               & (~ (IData)(vlSelfRef.milan_datapath__DOT__stream_table__DOT__en_q_r)));
        vlSelfRef.milan_datapath__DOT__pcmrx_pdu_p_w = 0U;
        if ((0U == (IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__rstate_r))) {
            if (vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__pop_w) {
                vlSelfRef.__Vdly__milan_datapath__DOT__aaf_rx_depkt__DOT__rbeat_r 
                    = ((7U == (IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__rbeat_r))
                        ? 7U : (7U & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__rbeat_r))));
                if ((1U == (IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__rbeat_r))) {
                    __Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__123__w 
                        = (((QData)((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg[1U][1U])) 
                            << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg[1U][0U])));
                    vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT____VlemCall_0__fbyte 
                        = (0x000000ffU & (IData)((__Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__123__w 
                                                  >> 0x20U)));
                    __Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__124__w 
                        = (((QData)((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg[1U][1U])) 
                            << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg[1U][0U])));
                    vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT____VlemCall_1__fbyte 
                        = (0x000000ffU & (IData)((__Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__124__w 
                                                  >> 0x28U)));
                    vlSelfRef.__Vdly__milan_datapath__DOT__aaf_rx_depkt__DOT__vlan_r 
                        = ((0x81U == (IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT____VlemCall_0__fbyte)) 
                           & (0U == (IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT____VlemCall_1__fbyte)));
                }
                if ((4U == (IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__rbeat_r))) {
                    if (vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__vlan_r) {
                        __Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__125__w 
                            = (((QData)((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg[1U][1U])) 
                                << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg[1U][0U])));
                        vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT____VlemCall_2__fbyte 
                            = (0x000000ffU & (IData)(
                                                     (__Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__125__w 
                                                      >> 0x30U)));
                        __Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__126__w 
                            = (((QData)((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg[1U][1U])) 
                                << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg[1U][0U])));
                        vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT____VlemCall_3__fbyte 
                            = (0x000000ffU & (IData)(
                                                     (__Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__126__w 
                                                      >> 0x38U)));
                        vlSelfRef.__Vdly__milan_datapath__DOT__aaf_rx_depkt__DOT__remain_r 
                            = (((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT____VlemCall_2__fbyte) 
                                << 8U) | (IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT____VlemCall_3__fbyte));
                    } else {
                        __Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__127__w 
                            = (((QData)((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg[1U][1U])) 
                                << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg[1U][0U])));
                        __Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__129__w 
                            = (((QData)((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg[1U][1U])) 
                                << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg[1U][0U])));
                        vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT____VlemCall_4__fbyte 
                            = (0x000000ffU & (IData)(
                                                     (__Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__127__w 
                                                      >> 0x10U)));
                        vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT____VlemCall_6__fbyte 
                            = (0x000000ffU & (IData)(
                                                     (__Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__129__w 
                                                      >> 0x38U)));
                        __Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__128__w 
                            = (((QData)((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg[1U][1U])) 
                                << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg[1U][0U])));
                        __Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__130__w 
                            = (((QData)((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg[1U][1U])) 
                                << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg[1U][0U])));
                        vlSelfRef.__Vdly__milan_datapath__DOT__aaf_rx_depkt__DOT__rstate_r = 1U;
                        vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT____VlemCall_5__fbyte 
                            = (0x000000ffU & (IData)(
                                                     (__Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__128__w 
                                                      >> 0x18U)));
                        vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT____VlemCall_7__fbyte 
                            = (0x000000ffU & (IData)(
                                                     (__Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__130__w 
                                                      >> 0x30U)));
                        vlSelfRef.__Vdly__milan_datapath__DOT__aaf_rx_depkt__DOT__remain_r 
                            = (((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT____VlemCall_4__fbyte) 
                                << 8U) | (IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT____VlemCall_5__fbyte));
                        vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__hold_r 
                            = (((QData)((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT____VlemCall_6__fbyte)) 
                                << 8U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT____VlemCall_7__fbyte)));
                    }
                }
                if (((5U == (IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__rbeat_r)) 
                     & (IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__vlan_r))) {
                    __Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__131__w 
                        = (((QData)((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg[1U][1U])) 
                            << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg[1U][0U])));
                    vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT____VlemCall_8__fbyte 
                        = (0x000000ffU & (IData)((__Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__131__w 
                                                  >> 0x38U)));
                    __Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__132__w 
                        = (((QData)((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg[1U][1U])) 
                            << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg[1U][0U])));
                    vlSelfRef.__Vdly__milan_datapath__DOT__aaf_rx_depkt__DOT__rstate_r = 1U;
                    vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT____VlemCall_9__fbyte 
                        = (0x000000ffU & (IData)((__Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__132__w 
                                                  >> 0x30U)));
                    __Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__133__w 
                        = (((QData)((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg[1U][1U])) 
                            << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg[1U][0U])));
                    vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT____VlemCall_10__fbyte 
                        = (0x000000ffU & (IData)((__Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__133__w 
                                                  >> 0x28U)));
                    __Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__134__w 
                        = (((QData)((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg[1U][1U])) 
                            << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg[1U][0U])));
                    vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT____VlemCall_11__fbyte 
                        = (0x000000ffU & (IData)((__Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__134__w 
                                                  >> 0x20U)));
                    __Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__135__w 
                        = (((QData)((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg[1U][1U])) 
                            << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg[1U][0U])));
                    vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT____VlemCall_12__fbyte 
                        = (0x000000ffU & (IData)((__Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__135__w 
                                                  >> 0x18U)));
                    __Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__136__w 
                        = (((QData)((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg[1U][1U])) 
                            << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg[1U][0U])));
                    vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT____VlemCall_13__fbyte 
                        = (0x000000ffU & (IData)((__Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__136__w 
                                                  >> 0x10U)));
                    vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__hold_r 
                        = (((QData)((IData)((((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT____VlemCall_8__fbyte) 
                                              << 8U) 
                                             | (IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT____VlemCall_9__fbyte)))) 
                            << 0x00000020U) | (QData)((IData)(
                                                              ((((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT____VlemCall_10__fbyte) 
                                                                 << 0x00000018U) 
                                                                | ((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT____VlemCall_11__fbyte) 
                                                                   << 0x00000010U)) 
                                                               | (((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT____VlemCall_12__fbyte) 
                                                                   << 8U) 
                                                                  | (IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT____VlemCall_13__fbyte))))));
                }
                if ((0x00000100U & vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg[1U][2U])) {
                    vlSelfRef.__Vdly__milan_datapath__DOT__aaf_rx_depkt__DOT__rstate_r = 0U;
                    vlSelfRef.__Vdly__milan_datapath__DOT__aaf_rx_depkt__DOT__rbeat_r = 0U;
                }
            }
        } else if ((1U == (IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__rstate_r))) {
            if (((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__emit_w) 
                 & (IData)(vlSelfRef.milan_datapath__DOT__dpkt_pcm_tready_w))) {
                if ((1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__hold_only_w)))) {
                    if (vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__vlan_r) {
                        __Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__137__w 
                            = (((QData)((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg[1U][1U])) 
                                << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg[1U][0U])));
                        vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT____VlemCall_14__fbyte 
                            = (0x000000ffU & (IData)(
                                                     (__Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__137__w 
                                                      >> 0x38U)));
                        __Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__138__w 
                            = (((QData)((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg[1U][1U])) 
                                << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg[1U][0U])));
                        vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT____VlemCall_15__fbyte 
                            = (0x000000ffU & (IData)(
                                                     (__Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__138__w 
                                                      >> 0x30U)));
                        __Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__139__w 
                            = (((QData)((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg[1U][1U])) 
                                << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg[1U][0U])));
                        vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT____VlemCall_16__fbyte 
                            = (0x000000ffU & (IData)(
                                                     (__Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__139__w 
                                                      >> 0x28U)));
                        __Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__140__w 
                            = (((QData)((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg[1U][1U])) 
                                << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg[1U][0U])));
                        vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT____VlemCall_17__fbyte 
                            = (0x000000ffU & (IData)(
                                                     (__Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__140__w 
                                                      >> 0x20U)));
                        __Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__141__w 
                            = (((QData)((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg[1U][1U])) 
                                << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg[1U][0U])));
                        vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT____VlemCall_18__fbyte 
                            = (0x000000ffU & (IData)(
                                                     (__Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__141__w 
                                                      >> 0x18U)));
                        __Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__142__w 
                            = (((QData)((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg[1U][1U])) 
                                << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg[1U][0U])));
                        vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT____VlemCall_19__fbyte 
                            = (0x000000ffU & (IData)(
                                                     (__Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__142__w 
                                                      >> 0x10U)));
                        vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT____VlemCond_22 
                            = (((QData)((IData)((((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT____VlemCall_14__fbyte) 
                                                  << 8U) 
                                                 | (IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT____VlemCall_15__fbyte)))) 
                                << 0x00000020U) | (QData)((IData)(
                                                                  ((((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT____VlemCall_16__fbyte) 
                                                                     << 0x00000018U) 
                                                                    | ((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT____VlemCall_17__fbyte) 
                                                                       << 0x00000010U)) 
                                                                   | (((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT____VlemCall_18__fbyte) 
                                                                       << 8U) 
                                                                      | (IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT____VlemCall_19__fbyte))))));
                    } else {
                        __Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__143__w 
                            = (((QData)((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg[1U][1U])) 
                                << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg[1U][0U])));
                        vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT____VlemCall_20__fbyte 
                            = (0x000000ffU & (IData)(
                                                     (__Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__143__w 
                                                      >> 0x38U)));
                        __Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__144__w 
                            = (((QData)((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg[1U][1U])) 
                                << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg[1U][0U])));
                        vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT____VlemCall_21__fbyte 
                            = (0x000000ffU & (IData)(
                                                     (__Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__144__w 
                                                      >> 0x30U)));
                        vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT____VlemCond_22 
                            = (((QData)((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT____VlemCall_20__fbyte)) 
                                << 8U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT____VlemCall_21__fbyte)));
                    }
                    vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__hold_r 
                        = vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT____VlemCond_22;
                }
                if ((8U >= (IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__remain_r))) {
                    vlSelfRef.milan_datapath__DOT__pcmrx_pdus 
                        = (0x0000ffffU & ((IData)(1U) 
                                          + (IData)(vlSelfRef.milan_datapath__DOT__pcmrx_pdus)));
                    vlSelfRef.milan_datapath__DOT__pcmrx_pdu_p_w = 1U;
                    vlSelfRef.milan_datapath__DOT__pcmrx_pdu_idx_w 
                        = vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__idxq_r
                        [vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__idxq_rp_r];
                    vlSelfRef.__Vdly__milan_datapath__DOT__aaf_rx_depkt__DOT__remain_r = 0U;
                    vlSelfRef.__Vdly__milan_datapath__DOT__aaf_rx_depkt__DOT__rbeat_r = 0U;
                    vlSelfRef.__Vdly__milan_datapath__DOT__aaf_rx_depkt__DOT__rstate_r 
                        = ((1U & (((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__hold_only_w) 
                                   | (~ (IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__pop_w))) 
                                  | (~ (vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg[1U][2U] 
                                        >> 8U)))) ? 
                           ((1U & ((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__hold_only_w) 
                                   | (~ (vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg[1U][2U] 
                                         >> 8U)))) ? 2U
                             : 0U) : 0U);
                } else {
                    vlSelfRef.__Vdly__milan_datapath__DOT__aaf_rx_depkt__DOT__remain_r 
                        = (0x0000ffffU & ((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__remain_r) 
                                          - (IData)(8U)));
                }
            }
            if ((((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__pop_w) 
                  & (vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg[1U][2U] 
                     >> 8U)) & (~ (((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__emit_w) 
                                    & (IData)(vlSelfRef.milan_datapath__DOT__dpkt_pcm_tready_w)) 
                                   & (8U >= (IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__remain_r)))))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__aaf_rx_depkt__DOT__rstate_r = 0U;
                vlSelfRef.__Vdly__milan_datapath__DOT__aaf_rx_depkt__DOT__rbeat_r = 0U;
                vlSelfRef.__Vdly__milan_datapath__DOT__aaf_rx_depkt__DOT__remain_r = 0U;
            }
        } else if ((2U == (IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__rstate_r))) {
            if (((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__pop_w) 
                 & (vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg[1U][2U] 
                    >> 8U))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__aaf_rx_depkt__DOT__rstate_r = 0U;
                vlSelfRef.__Vdly__milan_datapath__DOT__aaf_rx_depkt__DOT__rbeat_r = 0U;
            }
        } else {
            vlSelfRef.__Vdly__milan_datapath__DOT__aaf_rx_depkt__DOT__rstate_r = 0U;
        }
    } else {
        vlSelfRef.milan_datapath__DOT__strtbl_bind_rise_w = 0U;
        vlSelfRef.milan_datapath__DOT__pcmrx_pdus = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__aaf_rx_depkt__DOT__rstate_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__aaf_rx_depkt__DOT__rbeat_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__aaf_rx_depkt__DOT__vlan_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__aaf_rx_depkt__DOT__remain_r = 0U;
        vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__hold_r = 0ULL;
        vlSelfRef.milan_datapath__DOT__pcmrx_pdu_p_w = 0U;
        vlSelfRef.milan_datapath__DOT__pcmrx_pdu_idx_w = 0U;
    }
    vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__rbeat_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__aaf_rx_depkt__DOT__rbeat_r;
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg__v0) {
        vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg[1U][0U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg__v0[0U];
        vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg[1U][1U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg__v0[1U];
        vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg[1U][2U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg__v0[2U];
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg__v1) {
        vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg[0U][0U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg__v1[0U];
        vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg[0U][1U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg__v1[1U];
        vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg[0U][2U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg__v1[2U];
    }
    vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__idxq_rp_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__aaf_rx_depkt__DOT__idxq_rp_r;
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__aaf_rx_depkt__DOT__idxq_r__v0) {
        vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__idxq_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__aaf_rx_depkt__DOT__idxq_r__v0] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__aaf_rx_depkt__DOT__idxq_r__v0;
    }
    vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__vlan_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__aaf_rx_depkt__DOT__vlan_r;
    vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__remain_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__aaf_rx_depkt__DOT__remain_r;
    vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__rstate_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__aaf_rx_depkt__DOT__rstate_r;
    if (vlSelfRef.axis_resetn) {
        vlSelfRef.milan_datapath__DOT__i2spb_reset_p = 0U;
        if (vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__stg_drop_w) {
            vlSelfRef.milan_datapath__DOT__i2spb_reset_p 
                = vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__was_filled_r;
            vlSelfRef.__Vdly__milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__was_filled_r = 0U;
        }
        if ((0U != (IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__fill_w))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__was_filled_r = 1U;
        }
        if ((((~ (IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__prefill_r)) 
              & (0U == (IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__fill_w))) 
             & (IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__was_filled_r))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__prefill_r = 1U;
            vlSelfRef.milan_datapath__DOT__i2spb_reset_p = 1U;
            vlSelfRef.__Vdly__milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__was_filled_r = 0U;
        } else if (((IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__prefill_r) 
                    & (0x0100U <= (IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__fill_w)))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__prefill_r = 0U;
        }
        vlSelfRef.__Vdly__milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__cdc_wen_r = 0U;
        if (((((0U != (IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__fill_w)) 
               & (~ (IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__prefill_r))) 
              & (~ (IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__cdc_wfull_w))) 
             & (~ (IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__cdc_wen_r)))) {
            vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__cdc_wdata_r 
                = vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__fifo_r
                [(0x000001ffU & (IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__rptr_r))];
            vlSelfRef.__Vdly__milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__cdc_wen_r = 1U;
            vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__rptr_r 
                = (0x000003ffU & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__rptr_r)));
        }
    } else {
        vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__rptr_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__cdc_wen_r = 0U;
        vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__cdc_wdata_r = 0ULL;
        vlSelfRef.milan_datapath__DOT__i2spb_reset_p = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__was_filled_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__prefill_r = 1U;
    }
    vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__was_filled_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__was_filled_r;
    vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__prefill_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__prefill_r;
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__fifo_r__v0) {
        vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__fifo_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__fifo_r__v0] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__fifo_r__v0;
    }
    vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__cdc_wen_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__cdc_wen_r;
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_94 = (7U 
                                                 & (vlSelfRef.milan_datapath__DOT__csr__DOT__cls_tcq 
                                                    >> 
                                                    (0x0000001fU 
                                                     & (((IData)(3U) 
                                                         * 
                                                         (7U 
                                                          & (vlSelfRef.milan_datapath__DOT__csr__DOT__cls_map 
                                                             >> (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_95)))) 
                                                        & (- (IData)(
                                                                     (0x17U 
                                                                      >= (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_95))))))));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_76 = ((IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__beat_r) 
                                                 == 
                                                 (0x0000001fU 
                                                  & ((IData)(5U) 
                                                     + 
                                                     ((IData)(6U) 
                                                      * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_68)))));
    __Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__274__t 
        = vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__et_r;
    __Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__274__Vfuncout 
        = (3U | ((IData)(__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__274__t) 
                 << 4U));
    vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__tram_raddr_w 
        = __Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__274__Vfuncout;
    if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__est_r))) {
        if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__est_r))) {
            if (vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__ext_trd_go_w) {
                vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT____VlemCall_0__taddr 
                    = milan_datapath__DOT__csr_tctx_rd_addr_w;
            } else {
                vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__275__w 
                    = ((0U == (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__grant_t_w))
                        ? 3U : 0U);
                vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__275__t 
                    = vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__grant_t_w;
                vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT____VlemCall_0__taddr 
                    = (((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__275__t) 
                        << 4U) | (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__275__w));
            }
            vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__tram_raddr_w 
                = vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT____VlemCall_0__taddr;
        } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__est_r))) {
            vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__276__t 
                = vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__et_r;
            vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__276__Vfuncout 
                = (5U | ((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__276__t) 
                         << 4U));
            vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__tram_raddr_w 
                = vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__276__Vfuncout;
        } else {
            vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__277__t 
                = vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__et_r;
            vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__277__Vfuncout 
                = (5U | ((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__277__t) 
                         << 4U));
            vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__tram_raddr_w 
                = vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__277__Vfuncout;
        }
    } else if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__est_r))) {
        if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__est_r))) {
            if (vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__ext_trd_go_w) {
                vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT____VlemCall_0__taddr 
                    = milan_datapath__DOT__csr_tctx_rd_addr_w;
            } else {
                vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__278__w 
                    = ((0U == (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__grant_t_w))
                        ? 3U : 0U);
                vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__278__t 
                    = vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__grant_t_w;
                vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT____VlemCall_0__taddr 
                    = (((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__278__t) 
                        << 4U) | (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__278__w));
            }
            vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__tram_raddr_w 
                = vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT____VlemCall_0__taddr;
        } else {
            vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__279__w 
                = ((0U == (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fph_r))
                    ? 4U : 3U);
            vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__279__t 
                = vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__et_r;
            vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__279__Vfuncout 
                = (((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__279__t) 
                    << 4U) | (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__279__w));
            vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__tram_raddr_w 
                = vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__279__Vfuncout;
        }
    } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__est_r))) {
        vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__280__w 
            = ((0U == (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fph_r))
                ? 1U : ((1U == (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fph_r))
                         ? 2U : 3U));
        vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__280__t 
            = vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__et_r;
        vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__280__Vfuncout 
            = (((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__280__t) 
                << 4U) | (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__280__w));
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__tram_raddr_w 
            = vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__280__Vfuncout;
    } else {
        if (vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__ext_trd_go_w) {
            vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT____VlemCall_0__taddr 
                = milan_datapath__DOT__csr_tctx_rd_addr_w;
        } else {
            vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__281__w 
                = ((0U == (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__grant_t_w))
                    ? 3U : 0U);
            vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__281__t 
                = vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__grant_t_w;
            vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT____VlemCall_0__taddr 
                = (((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__281__t) 
                    << 4U) | (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__281__w));
        }
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__tram_raddr_w 
            = vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT____VlemCall_0__taddr;
    }
    vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__own_last_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pown_o_w) 
           == (3U & ((vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__chans_r
                      [vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pown_t_w] 
                      >> 1U) - (IData)(1U))));
    vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__p1_w 
        = (7U & (((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__pos_r)) 
                 & (- (IData)(((IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__c_eff_w) 
                               != (7U & ((IData)(1U) 
                                         + (IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__pos_r))))))));
    vlSelfRef.milan_datapath__DOT__wing_stg_hit_w = 
        ((IData)(vlSelfRef.milan_datapath__DOT__wing_stg_vld_r) 
         & ((IData)(vlSelfRef.milan_datapath__DOT__wing_stg_idx_r) 
            == (7U & ((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__lctx_wr_addr_r) 
                      >> 5U))));
    vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ext_wr_ok_w 
        = ((~ (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__eng_we_w)) 
           & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__lctx_wr_p_r));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_8 = ((2U 
                                                 > 
                                                 (0x0000000fU 
                                                  & (vlSelfRef.milan_datapath__DOT__csr__DOT__tctx_wr_data_r 
                                                     >> 1U)))
                                                 ? 2U
                                                 : 
                                                ((8U 
                                                  <= 
                                                  (0x0000000fU 
                                                   & (vlSelfRef.milan_datapath__DOT__csr__DOT__tctx_wr_data_r 
                                                      >> 1U)))
                                                  ? 8U
                                                  : 
                                                 (0x0000000fU 
                                                  & ((vlSelfRef.milan_datapath__DOT__csr__DOT__tctx_wr_data_r 
                                                      >> 1U) 
                                                     + 
                                                     (1U 
                                                      & (vlSelfRef.milan_datapath__DOT__csr__DOT__tctx_wr_data_r 
                                                         >> 1U))))));
    vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__tram_we_w = 0U;
    vlSelfRef.milan_datapath__DOT__tctx_wr_rdy_w = 0U;
    if ((1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__tsw_pend_r)))) {
        if ((4U != (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__est_r))) {
            if ((5U != (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__est_r))) {
                if (vlSelfRef.milan_datapath__DOT__csr__DOT__tctx_wr_p_r) {
                    vlSelfRef.milan_datapath__DOT__tctx_wr_rdy_w = 1U;
                }
            }
        }
    }
    vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__tram_wdata_w = 0U;
    vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__tram_waddr_w = 0U;
    if (vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__tsw_pend_r) {
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__tram_we_w = 1U;
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__tram_wdata_w 
            = vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__tsw_val_r;
        vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__271__t 
            = vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__tsw_t_r;
        vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__271__Vfuncout 
            = (4U | ((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__271__t) 
                     << 4U));
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__tram_waddr_w 
            = vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__271__Vfuncout;
    } else if ((4U == (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__est_r))) {
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__tram_we_w = 1U;
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__tram_wdata_w 
            = (0x000000ffU & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__eseq_r)));
        vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__272__t 
            = vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__et_r;
        vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__272__Vfuncout 
            = (3U | ((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__272__t) 
                     << 4U));
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__tram_waddr_w 
            = vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__272__Vfuncout;
    } else if ((5U == (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__est_r))) {
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__tram_we_w = 1U;
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__tram_wdata_w 
            = ((IData)(1U) + vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__tram_q_r);
        vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__273__t 
            = vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__et_r;
        vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__273__Vfuncout 
            = (5U | ((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__273__t) 
                     << 4U));
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__tram_waddr_w 
            = vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__273__Vfuncout;
    } else if (vlSelfRef.milan_datapath__DOT__csr__DOT__tctx_wr_p_r) {
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__tram_we_w = 1U;
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__tram_wdata_w 
            = vlSelfRef.milan_datapath__DOT__csr__DOT__tctx_wr_data_r;
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__tram_waddr_w 
            = vlSelfRef.milan_datapath__DOT__csr__DOT__tctx_wr_addr_r;
    }
    vlSelfRef.milan_datapath__DOT__tctx_w0_wr_w = ((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__tctx_wr_p_r) 
                                                   & (0U 
                                                      == 
                                                      (0x0000000fU 
                                                       & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__tctx_wr_addr_r))));
    vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__seq_mm_w 
        = (IData)(((0x00001000U == (0x00001f00U & vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ram_q_r)) 
                   & ((0x000000ffU & ((IData)(1U) + vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ram_q_r)) 
                      != (0x000000ffU & (vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__cur_r[4U] 
                                         >> 3U)))));
    vlSelfRef.milan_datapath__DOT____Vcellinp__csr__i_pcmrx_cnt 
        = (((IData)(vlSelfRef.milan_datapath__DOT__pcmrx_drops) 
            << 0x00000010U) | (IData)(vlSelfRef.milan_datapath__DOT__pcmrx_pdus));
    vlSelfRef.m_axis_pcm_tuser = vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__idxq_r
        [vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__idxq_rp_r];
    if ((0U < ((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__vlan_r)
                ? 6U : 2U))) {
        vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__out_assemble__DOT__unnamedblk1__DOT__unnamedblk2__DOT__b 
            = (0x000000ffU & (IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__hold_r));
    } else {
        vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__122__j 
            = (7U & (- ((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__vlan_r)
                         ? 6U : 2U)));
        vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__122__w 
            = (((QData)((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg[1U][1U])) 
                << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg[1U][0U])));
        vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__122__Vfuncout 
            = (0x000000ffU & (IData)((vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__122__w 
                                      >> (0x0000003fU 
                                          & ((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__122__j) 
                                             << 3U)))));
        vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__out_assemble__DOT__unnamedblk1__DOT__unnamedblk2__DOT__b 
            = vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__122__Vfuncout;
    }
    vlSelfRef.milan_datapath__DOT__dpkt_pcm_tdata_w 
        = ((0xffffffffffffff00ULL & vlSelfRef.milan_datapath__DOT__dpkt_pcm_tdata_w) 
           | (IData)((IData)(((0U < (IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__remain_r))
                               ? (IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__out_assemble__DOT__unnamedblk1__DOT__unnamedblk2__DOT__b)
                               : 0U))));
    if ((1U < ((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__vlan_r)
                ? 6U : 2U))) {
        vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__out_assemble__DOT__unnamedblk1__DOT__unnamedblk2__DOT__b 
            = (0x000000ffU & (IData)((vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__hold_r 
                                      >> 8U)));
    } else {
        vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__122__j 
            = (7U & ((IData)(1U) - ((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__vlan_r)
                                     ? 6U : 2U)));
        vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__122__w 
            = (((QData)((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg[1U][1U])) 
                << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg[1U][0U])));
        vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__122__Vfuncout 
            = (0x000000ffU & (IData)((vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__122__w 
                                      >> (0x0000003fU 
                                          & ((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__122__j) 
                                             << 3U)))));
        vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__out_assemble__DOT__unnamedblk1__DOT__unnamedblk2__DOT__b 
            = vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__122__Vfuncout;
    }
    vlSelfRef.milan_datapath__DOT__dpkt_pcm_tdata_w 
        = ((0xffffffffffff00ffULL & vlSelfRef.milan_datapath__DOT__dpkt_pcm_tdata_w) 
           | ((QData)((IData)(((1U < (IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__remain_r))
                                ? (IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__out_assemble__DOT__unnamedblk1__DOT__unnamedblk2__DOT__b)
                                : 0U))) << 8U));
    if ((2U < ((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__vlan_r)
                ? 6U : 2U))) {
        vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__out_assemble__DOT__unnamedblk1__DOT__unnamedblk2__DOT__b 
            = (0x000000ffU & (IData)((vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__hold_r 
                                      >> 0x10U)));
    } else {
        vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__122__j 
            = (7U & ((IData)(2U) - ((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__vlan_r)
                                     ? 6U : 2U)));
        vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__122__w 
            = (((QData)((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg[1U][1U])) 
                << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg[1U][0U])));
        vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__122__Vfuncout 
            = (0x000000ffU & (IData)((vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__122__w 
                                      >> (0x0000003fU 
                                          & ((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__122__j) 
                                             << 3U)))));
        vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__out_assemble__DOT__unnamedblk1__DOT__unnamedblk2__DOT__b 
            = vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__122__Vfuncout;
    }
    vlSelfRef.milan_datapath__DOT__dpkt_pcm_tdata_w 
        = ((0xffffffffff00ffffULL & vlSelfRef.milan_datapath__DOT__dpkt_pcm_tdata_w) 
           | ((QData)((IData)(((2U < (IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__remain_r))
                                ? (IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__out_assemble__DOT__unnamedblk1__DOT__unnamedblk2__DOT__b)
                                : 0U))) << 0x00000010U));
    if ((3U < ((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__vlan_r)
                ? 6U : 2U))) {
        vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__out_assemble__DOT__unnamedblk1__DOT__unnamedblk2__DOT__b 
            = (0x000000ffU & (IData)((vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__hold_r 
                                      >> 0x18U)));
    } else {
        vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__122__j 
            = (7U & ((IData)(3U) - ((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__vlan_r)
                                     ? 6U : 2U)));
        vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__122__w 
            = (((QData)((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg[1U][1U])) 
                << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg[1U][0U])));
        vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__122__Vfuncout 
            = (0x000000ffU & (IData)((vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__122__w 
                                      >> (0x0000003fU 
                                          & ((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__122__j) 
                                             << 3U)))));
        vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__out_assemble__DOT__unnamedblk1__DOT__unnamedblk2__DOT__b 
            = vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__122__Vfuncout;
    }
    vlSelfRef.milan_datapath__DOT__dpkt_pcm_tdata_w 
        = ((0xffffffff00ffffffULL & vlSelfRef.milan_datapath__DOT__dpkt_pcm_tdata_w) 
           | ((QData)((IData)(((3U < (IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__remain_r))
                                ? (IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__out_assemble__DOT__unnamedblk1__DOT__unnamedblk2__DOT__b)
                                : 0U))) << 0x00000018U));
    if ((4U < ((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__vlan_r)
                ? 6U : 2U))) {
        vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__out_assemble__DOT__unnamedblk1__DOT__unnamedblk2__DOT__b 
            = (0x000000ffU & (IData)((vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__hold_r 
                                      >> 0x20U)));
    } else {
        vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__122__j 
            = (7U & ((IData)(4U) - ((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__vlan_r)
                                     ? 6U : 2U)));
        vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__122__w 
            = (((QData)((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg[1U][1U])) 
                << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg[1U][0U])));
        vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__122__Vfuncout 
            = (0x000000ffU & (IData)((vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__122__w 
                                      >> (0x0000003fU 
                                          & ((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__122__j) 
                                             << 3U)))));
        vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__out_assemble__DOT__unnamedblk1__DOT__unnamedblk2__DOT__b 
            = vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__122__Vfuncout;
    }
    vlSelfRef.milan_datapath__DOT__dpkt_pcm_tdata_w 
        = ((0xffffff00ffffffffULL & vlSelfRef.milan_datapath__DOT__dpkt_pcm_tdata_w) 
           | ((QData)((IData)(((4U < (IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__remain_r))
                                ? (IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__out_assemble__DOT__unnamedblk1__DOT__unnamedblk2__DOT__b)
                                : 0U))) << 0x00000020U));
    if ((5U < ((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__vlan_r)
                ? 6U : 2U))) {
        vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__out_assemble__DOT__unnamedblk1__DOT__unnamedblk2__DOT__b 
            = (0x000000ffU & (IData)((vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__hold_r 
                                      >> 0x28U)));
    } else {
        vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__122__j 
            = (7U & ((IData)(5U) - ((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__vlan_r)
                                     ? 6U : 2U)));
        vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__122__w 
            = (((QData)((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg[1U][1U])) 
                << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg[1U][0U])));
        vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__122__Vfuncout 
            = (0x000000ffU & (IData)((vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__122__w 
                                      >> (0x0000003fU 
                                          & ((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__122__j) 
                                             << 3U)))));
        vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__out_assemble__DOT__unnamedblk1__DOT__unnamedblk2__DOT__b 
            = vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__122__Vfuncout;
    }
    vlSelfRef.milan_datapath__DOT__dpkt_pcm_tdata_w 
        = ((0xffff00ffffffffffULL & vlSelfRef.milan_datapath__DOT__dpkt_pcm_tdata_w) 
           | ((QData)((IData)(((5U < (IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__remain_r))
                                ? (IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__out_assemble__DOT__unnamedblk1__DOT__unnamedblk2__DOT__b)
                                : 0U))) << 0x00000028U));
    if ((6U < ((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__vlan_r)
                ? 6U : 2U))) {
        vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__out_assemble__DOT__unnamedblk1__DOT__unnamedblk2__DOT__b 
            = (0x000000ffU & (IData)((vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__hold_r 
                                      >> 0x30U)));
    } else {
        vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__122__j 
            = (7U & ((IData)(6U) - ((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__vlan_r)
                                     ? 6U : 2U)));
        vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__122__w 
            = (((QData)((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg[1U][1U])) 
                << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg[1U][0U])));
        vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__122__Vfuncout 
            = (0x000000ffU & (IData)((vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__122__w 
                                      >> (0x0000003fU 
                                          & ((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__122__j) 
                                             << 3U)))));
        vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__out_assemble__DOT__unnamedblk1__DOT__unnamedblk2__DOT__b 
            = vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__122__Vfuncout;
    }
    vlSelfRef.milan_datapath__DOT__dpkt_pcm_tdata_w 
        = ((0xff00ffffffffffffULL & vlSelfRef.milan_datapath__DOT__dpkt_pcm_tdata_w) 
           | ((QData)((IData)(((6U < (IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__remain_r))
                                ? (IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__out_assemble__DOT__unnamedblk1__DOT__unnamedblk2__DOT__b)
                                : 0U))) << 0x00000030U));
    vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__122__j 
        = (7U & ((IData)(7U) - ((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__vlan_r)
                                 ? 6U : 2U)));
    vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__122__w 
        = (((QData)((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg[1U][1U])) 
            << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg[1U][0U])));
    vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__122__Vfuncout 
        = (0x000000ffU & (IData)((vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__122__w 
                                  >> (0x0000003fU & 
                                      ((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__122__j) 
                                       << 3U)))));
    vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__out_assemble__DOT__unnamedblk1__DOT__unnamedblk2__DOT__b 
        = vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__122__Vfuncout;
    vlSelfRef.milan_datapath__DOT__dpkt_pcm_tdata_w 
        = ((0x00ffffffffffffffULL & vlSelfRef.milan_datapath__DOT__dpkt_pcm_tdata_w) 
           | ((QData)((IData)(((7U < (IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__remain_r))
                                ? (IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__out_assemble__DOT__unnamedblk1__DOT__unnamedblk2__DOT__b)
                                : 0U))) << 0x00000038U));
    milan_datapath__DOT__i2s_feed_tdata_w = ((1U & vlSelfRef.milan_datapath__DOT__csr__DOT__chmap_ctrl)
                                              ? (((QData)((IData)(
                                                                  ((0x00ff0000U 
                                                                    & (vlSelfRef.milan_datapath__DOT__chmap_phys_w[0U] 
                                                                       >> 8U)) 
                                                                   | ((0x0000ff00U 
                                                                       & (vlSelfRef.milan_datapath__DOT__chmap_phys_w[1U] 
                                                                          << 8U)) 
                                                                      | (0x000000ffU 
                                                                         & (vlSelfRef.milan_datapath__DOT__chmap_phys_w[1U] 
                                                                            >> 8U)))))) 
                                                  << 0x00000020U) 
                                                 | (QData)((IData)(
                                                                   ((0x00ff0000U 
                                                                     & (vlSelfRef.milan_datapath__DOT__chmap_phys_w[0U] 
                                                                        << 0x00000010U)) 
                                                                    | ((0x0000ff00U 
                                                                        & vlSelfRef.milan_datapath__DOT__chmap_phys_w[0U]) 
                                                                       | (0x000000ffU 
                                                                          & (vlSelfRef.milan_datapath__DOT__chmap_phys_w[0U] 
                                                                             >> 0x00000010U)))))))
                                              : vlSelfRef.milan_datapath__DOT__dpkt_pcm_tdata_w);
    vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__hold_only_w 
        = ((1U == (IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__rstate_r)) 
           & ((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__remain_r) 
              <= ((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__vlan_r)
                   ? 6U : 2U)));
    vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__fill_w 
        = (0x000003ffU & ((IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__wptr_r) 
                          - (IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__rptr_r)));
    vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__cdc_wfull_w 
        = ((IData)(vlSelfRef.axis_resetn) && ((IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__u_cdc__DOT__wptr_gray_n) 
                                              == ((0x00000018U 
                                                   & ((~ 
                                                       ((IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__u_cdc__DOT__rgray_w2_r) 
                                                        >> 3U)) 
                                                      << 3U)) 
                                                  | (7U 
                                                     & (IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__u_cdc__DOT__rgray_w2_r)))));
    if (vlSelfRef.axis_resetn) {
        vlSelfRef.milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__u_tcdc__DOT__wgray_r2_r 
            = vlSelfRef.milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__u_tcdc__DOT__wgray_r1_r;
        vlSelfRef.milan_datapath__DOT__speed_sync = vlSelfRef.milan_datapath__DOT__speed_meta;
        vlSelfRef.milan_datapath__DOT__adp_link_up_p 
            = (((IData)(vlSelfRef.i_link_up) & (~ (IData)(vlSelfRef.milan_datapath__DOT__link_up_q))) 
               | ((vlSelfRef.milan_datapath__DOT__csr__DOT__adp_ctrl 
                   & (~ (IData)(vlSelfRef.milan_datapath__DOT__adp_en_q))) 
                  & (IData)(vlSelfRef.i_link_up)));
        vlSelfRef.milan_datapath__DOT__adp_link_down_p 
            = ((~ (IData)(vlSelfRef.i_link_up)) & (IData)(vlSelfRef.milan_datapath__DOT__link_up_q));
        if (vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_rx__DOT__beat_acc) {
            if (vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_rx__DOT__start_packet) {
                vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_rx__DOT__ts_sop 
                    = ((((QData)((IData)(vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ts_counter__DOT__acc[2U])) 
                         << 0x00000028U) | (((QData)((IData)(vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ts_counter__DOT__acc[1U])) 
                                             << 8U) 
                                            | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ts_counter__DOT__acc[0U])) 
                                               >> 0x00000018U))) 
                       - (QData)((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__ptp_ilat)));
            }
            if (((~ (IData)(vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_rx__DOT__start_packet)) 
                 & (8U == (IData)(vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_rx__DOT__byte_counter)))) {
                if ((0x8100U != ((0x0000ff00U & ((IData)(
                                                         (vlSelfRef.s_axis_mac_rx_tdata 
                                                          >> 0x00000020U)) 
                                                 << 8U)) 
                                 | (0x000000ffU & (IData)(
                                                          (vlSelfRef.s_axis_mac_rx_tdata 
                                                           >> 0x00000028U)))))) {
                    vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_rx__DOT__eth_match 
                        = (0x88f7U == ((0x0000ff00U 
                                        & ((IData)(
                                                   (vlSelfRef.s_axis_mac_rx_tdata 
                                                    >> 0x00000020U)) 
                                           << 8U)) 
                                       | (0x000000ffU 
                                          & (IData)(
                                                    (vlSelfRef.s_axis_mac_rx_tdata 
                                                     >> 0x00000028U)))));
                    vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_rx__DOT__msg_type 
                        = (0x0000000fU & (IData)((vlSelfRef.s_axis_mac_rx_tdata 
                                                  >> 0x00000030U)));
                    vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_rx__DOT__eth_type_valid = 1U;
                }
            }
            if ((((~ (IData)(vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_rx__DOT__start_packet)) 
                  & (IData)(vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_rx__DOT__vlan_tagged)) 
                 & (0x10U == (IData)(vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_rx__DOT__byte_counter)))) {
                vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_rx__DOT__eth_match 
                    = (0x88f7U == ((0x0000ff00U & ((IData)(vlSelfRef.s_axis_mac_rx_tdata) 
                                                   << 8U)) 
                                   | (0x000000ffU & (IData)(
                                                            (vlSelfRef.s_axis_mac_rx_tdata 
                                                             >> 8U)))));
                vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_rx__DOT__msg_type 
                    = (0x0000000fU & (IData)((vlSelfRef.s_axis_mac_rx_tdata 
                                              >> 0x00000010U)));
                vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_rx__DOT__eth_type_valid = 1U;
            }
            if ((((~ (IData)(vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_rx__DOT__start_packet)) 
                  & (~ (IData)(vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_rx__DOT__vlan_tagged))) 
                 & (0x28U == (IData)(vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_rx__DOT__byte_counter)))) {
                vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_rx__DOT__ptp_seq_id 
                    = ((0x0000ff00U & ((IData)((vlSelfRef.s_axis_mac_rx_tdata 
                                                >> 0x00000020U)) 
                                       << 8U)) | (0x000000ffU 
                                                  & (IData)(
                                                            (vlSelfRef.s_axis_mac_rx_tdata 
                                                             >> 0x00000028U))));
                vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_rx__DOT__ptp_seq_id_valid = 1U;
            }
            if ((((~ (IData)(vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_rx__DOT__start_packet)) 
                  & (IData)(vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_rx__DOT__vlan_tagged)) 
                 & (0x30U == (IData)(vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_rx__DOT__byte_counter)))) {
                vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_rx__DOT__ptp_seq_id 
                    = ((0x0000ff00U & ((IData)(vlSelfRef.s_axis_mac_rx_tdata) 
                                       << 8U)) | (0x000000ffU 
                                                  & (IData)(
                                                            (vlSelfRef.s_axis_mac_rx_tdata 
                                                             >> 8U))));
                vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_rx__DOT__ptp_seq_id_valid = 1U;
            }
            if (((~ (IData)(vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_rx__DOT__start_packet)) 
                 & (8U == (IData)(vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_rx__DOT__byte_counter)))) {
                vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_rx__DOT__vlan_tagged 
                    = (0x8100U == ((0x0000ff00U & ((IData)(
                                                           (vlSelfRef.s_axis_mac_rx_tdata 
                                                            >> 0x00000020U)) 
                                                   << 8U)) 
                                   | (0x000000ffU & (IData)(
                                                            (vlSelfRef.s_axis_mac_rx_tdata 
                                                             >> 0x00000028U)))));
            }
            if (vlSelfRef.s_axis_mac_rx_tlast) {
                vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_rx__DOT__eth_type_valid = 0U;
                vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_rx__DOT__eth_match = 0U;
                vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_rx__DOT__ptp_seq_id_valid = 0U;
                vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_rx__DOT__vlan_tagged = 0U;
            }
            vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_rx__DOT__start_packet 
                = vlSelfRef.s_axis_mac_rx_tlast;
        }
        if (vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_tx__DOT__beat_acc) {
            if (vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_tx__DOT__start_packet) {
                vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_tx__DOT__ts_sop 
                    = ((((QData)((IData)(vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ts_counter__DOT__acc[2U])) 
                         << 0x00000028U) | (((QData)((IData)(vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ts_counter__DOT__acc[1U])) 
                                             << 8U) 
                                            | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ts_counter__DOT__acc[0U])) 
                                               >> 0x00000018U))) 
                       + (QData)((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__ptp_elat)));
            }
        }
        if (vlSelfRef.s_axi_awready) {
            if ((1U & (~ ((IData)(vlSelfRef.s_axi_awaddr) 
                          >> 0x0000000fU)))) {
                if ((1U & (~ ((IData)(vlSelfRef.s_axi_awaddr) 
                              >> 0x0000000eU)))) {
                    if ((1U & (~ ((IData)(vlSelfRef.s_axi_awaddr) 
                                  >> 0x0000000dU)))) {
                        if ((1U & (~ ((IData)(vlSelfRef.s_axi_awaddr) 
                                      >> 0x0000000cU)))) {
                            if ((0x00000800U & (IData)(vlSelfRef.s_axi_awaddr))) {
                                if ((1U & (~ ((IData)(vlSelfRef.s_axi_awaddr) 
                                              >> 0x0000000aU)))) {
                                    if ((1U & (~ ((IData)(vlSelfRef.s_axi_awaddr) 
                                                  >> 9U)))) {
                                        if ((0x00000100U 
                                             & (IData)(vlSelfRef.s_axi_awaddr))) {
                                            if ((1U 
                                                 & (~ 
                                                    ((IData)(vlSelfRef.s_axi_awaddr) 
                                                     >> 7U)))) {
                                                if (
                                                    (1U 
                                                     & (~ 
                                                        ((IData)(vlSelfRef.s_axi_awaddr) 
                                                         >> 6U)))) {
                                                    if (
                                                        (1U 
                                                         & (~ 
                                                            ((IData)(vlSelfRef.s_axi_awaddr) 
                                                             >> 5U)))) {
                                                        if (
                                                            (1U 
                                                             & (~ 
                                                                ((IData)(vlSelfRef.s_axi_awaddr) 
                                                                 >> 4U)))) {
                                                            if (
                                                                (1U 
                                                                 & (~ 
                                                                    ((IData)(vlSelfRef.s_axi_awaddr) 
                                                                     >> 3U)))) {
                                                                if (
                                                                    (4U 
                                                                     & (IData)(vlSelfRef.s_axi_awaddr))) {
                                                                    if (
                                                                        (1U 
                                                                         & (~ 
                                                                            ((IData)(vlSelfRef.s_axi_awaddr) 
                                                                             >> 1U)))) {
                                                                        if (
                                                                            (1U 
                                                                             & (~ (IData)(vlSelfRef.s_axi_awaddr)))) {
                                                                            vlSelfRef.milan_datapath__DOT__csr__DOT__chmap_sel 
                                                                                = vlSelfRef.s_axi_wdata;
                                                                        }
                                                                    }
                                                                }
                                                            }
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                        if ((1U & (~ 
                                                   ((IData)(vlSelfRef.s_axi_awaddr) 
                                                    >> 8U)))) {
                                            if ((1U 
                                                 & (~ 
                                                    ((IData)(vlSelfRef.s_axi_awaddr) 
                                                     >> 7U)))) {
                                                if (
                                                    (1U 
                                                     & (~ 
                                                        ((IData)(vlSelfRef.s_axi_awaddr) 
                                                         >> 6U)))) {
                                                    if (
                                                        (1U 
                                                         & (~ 
                                                            ((IData)(vlSelfRef.s_axi_awaddr) 
                                                             >> 5U)))) {
                                                        if (
                                                            (1U 
                                                             & (~ 
                                                                ((IData)(vlSelfRef.s_axi_awaddr) 
                                                                 >> 4U)))) {
                                                            if (
                                                                (1U 
                                                                 & (~ 
                                                                    ((IData)(vlSelfRef.s_axi_awaddr) 
                                                                     >> 3U)))) {
                                                                if (
                                                                    (1U 
                                                                     & (~ 
                                                                        ((IData)(vlSelfRef.s_axi_awaddr) 
                                                                         >> 2U)))) {
                                                                    if (
                                                                        (1U 
                                                                         & (~ 
                                                                            ((IData)(vlSelfRef.s_axi_awaddr) 
                                                                             >> 1U)))) {
                                                                        if (
                                                                            (1U 
                                                                             & (~ (IData)(vlSelfRef.s_axi_awaddr)))) {
                                                                            vlSelfRef.milan_datapath__DOT__csr__DOT__strm_dir_r 
                                                                                = 
                                                                                (1U 
                                                                                & (vlSelfRef.s_axi_wdata 
                                                                                >> 8U));
                                                                        }
                                                                    }
                                                                }
                                                            }
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                            if ((1U & (~ ((IData)(vlSelfRef.s_axi_awaddr) 
                                          >> 0x0000000bU)))) {
                                if ((0x00000400U & (IData)(vlSelfRef.s_axi_awaddr))) {
                                    if ((1U & (~ ((IData)(vlSelfRef.s_axi_awaddr) 
                                                  >> 9U)))) {
                                        if ((0x00000100U 
                                             & (IData)(vlSelfRef.s_axi_awaddr))) {
                                            if ((1U 
                                                 & (~ 
                                                    ((IData)(vlSelfRef.s_axi_awaddr) 
                                                     >> 7U)))) {
                                                if (
                                                    (0x00000040U 
                                                     & (IData)(vlSelfRef.s_axi_awaddr))) {
                                                    if (
                                                        (1U 
                                                         & (~ 
                                                            ((IData)(vlSelfRef.s_axi_awaddr) 
                                                             >> 5U)))) {
                                                        if (
                                                            (1U 
                                                             & (~ 
                                                                ((IData)(vlSelfRef.s_axi_awaddr) 
                                                                 >> 4U)))) {
                                                            if (
                                                                (1U 
                                                                 & (~ 
                                                                    ((IData)(vlSelfRef.s_axi_awaddr) 
                                                                     >> 3U)))) {
                                                                if (
                                                                    (1U 
                                                                     & (~ 
                                                                        ((IData)(vlSelfRef.s_axi_awaddr) 
                                                                         >> 2U)))) {
                                                                    if (
                                                                        (1U 
                                                                         & (~ 
                                                                            ((IData)(vlSelfRef.s_axi_awaddr) 
                                                                             >> 1U)))) {
                                                                        if (
                                                                            (1U 
                                                                             & (~ (IData)(vlSelfRef.s_axi_awaddr)))) {
                                                                            vlSelfRef.milan_datapath__DOT__csr__DOT__ptp_ilat 
                                                                                = vlSelfRef.s_axi_wdata;
                                                                        }
                                                                    }
                                                                }
                                                                if (
                                                                    (4U 
                                                                     & (IData)(vlSelfRef.s_axi_awaddr))) {
                                                                    if (
                                                                        (1U 
                                                                         & (~ 
                                                                            ((IData)(vlSelfRef.s_axi_awaddr) 
                                                                             >> 1U)))) {
                                                                        if (
                                                                            (1U 
                                                                             & (~ (IData)(vlSelfRef.s_axi_awaddr)))) {
                                                                            vlSelfRef.milan_datapath__DOT__csr__DOT__ptp_elat 
                                                                                = vlSelfRef.s_axi_wdata;
                                                                        }
                                                                    }
                                                                }
                                                            }
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
        if (vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_tx__DOT__beat_acc) {
            if (((~ (IData)(vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_tx__DOT__start_packet)) 
                 & (8U == (IData)(vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_tx__DOT__byte_counter)))) {
                if ((0x8100U != ((0x0000ff00U & ((IData)(
                                                         (vlSymsp->TOP__milan_datapath__DOT__ptp_timestamp__DOT__m_axis_tx.tdata 
                                                          >> 0x00000020U)) 
                                                 << 8U)) 
                                 | (0x000000ffU & (IData)(
                                                          (vlSymsp->TOP__milan_datapath__DOT__ptp_timestamp__DOT__m_axis_tx.tdata 
                                                           >> 0x00000028U)))))) {
                    vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_tx__DOT__eth_match 
                        = (0x88f7U == ((0x0000ff00U 
                                        & ((IData)(
                                                   (vlSymsp->TOP__milan_datapath__DOT__ptp_timestamp__DOT__m_axis_tx.tdata 
                                                    >> 0x00000020U)) 
                                           << 8U)) 
                                       | (0x000000ffU 
                                          & (IData)(
                                                    (vlSymsp->TOP__milan_datapath__DOT__ptp_timestamp__DOT__m_axis_tx.tdata 
                                                     >> 0x00000028U)))));
                    vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_tx__DOT__msg_type 
                        = (0x0000000fU & (IData)((vlSymsp->TOP__milan_datapath__DOT__ptp_timestamp__DOT__m_axis_tx.tdata 
                                                  >> 0x00000030U)));
                    vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_tx__DOT__eth_type_valid = 1U;
                }
            }
            if ((((~ (IData)(vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_tx__DOT__start_packet)) 
                  & (IData)(vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_tx__DOT__vlan_tagged)) 
                 & (0x10U == (IData)(vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_tx__DOT__byte_counter)))) {
                vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_tx__DOT__eth_match 
                    = (0x88f7U == ((0x0000ff00U & ((IData)(vlSymsp->TOP__milan_datapath__DOT__ptp_timestamp__DOT__m_axis_tx.tdata) 
                                                   << 8U)) 
                                   | (0x000000ffU & (IData)(
                                                            (vlSymsp->TOP__milan_datapath__DOT__ptp_timestamp__DOT__m_axis_tx.tdata 
                                                             >> 8U)))));
                vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_tx__DOT__msg_type 
                    = (0x0000000fU & (IData)((vlSymsp->TOP__milan_datapath__DOT__ptp_timestamp__DOT__m_axis_tx.tdata 
                                              >> 0x00000010U)));
                vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_tx__DOT__eth_type_valid = 1U;
            }
            if ((((~ (IData)(vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_tx__DOT__start_packet)) 
                  & (~ (IData)(vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_tx__DOT__vlan_tagged))) 
                 & (0x28U == (IData)(vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_tx__DOT__byte_counter)))) {
                vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_tx__DOT__ptp_seq_id 
                    = ((0x0000ff00U & ((IData)((vlSymsp->TOP__milan_datapath__DOT__ptp_timestamp__DOT__m_axis_tx.tdata 
                                                >> 0x00000020U)) 
                                       << 8U)) | (0x000000ffU 
                                                  & (IData)(
                                                            (vlSymsp->TOP__milan_datapath__DOT__ptp_timestamp__DOT__m_axis_tx.tdata 
                                                             >> 0x00000028U))));
                vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_tx__DOT__ptp_seq_id_valid = 1U;
            }
            if ((((~ (IData)(vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_tx__DOT__start_packet)) 
                  & (IData)(vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_tx__DOT__vlan_tagged)) 
                 & (0x30U == (IData)(vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_tx__DOT__byte_counter)))) {
                vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_tx__DOT__ptp_seq_id 
                    = ((0x0000ff00U & ((IData)(vlSymsp->TOP__milan_datapath__DOT__ptp_timestamp__DOT__m_axis_tx.tdata) 
                                       << 8U)) | (0x000000ffU 
                                                  & (IData)(
                                                            (vlSymsp->TOP__milan_datapath__DOT__ptp_timestamp__DOT__m_axis_tx.tdata 
                                                             >> 8U))));
                vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_tx__DOT__ptp_seq_id_valid = 1U;
            }
            if (((~ (IData)(vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_tx__DOT__start_packet)) 
                 & (8U == (IData)(vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_tx__DOT__byte_counter)))) {
                vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_tx__DOT__vlan_tagged 
                    = (0x8100U == ((0x0000ff00U & ((IData)(
                                                           (vlSymsp->TOP__milan_datapath__DOT__ptp_timestamp__DOT__m_axis_tx.tdata 
                                                            >> 0x00000020U)) 
                                                   << 8U)) 
                                   | (0x000000ffU & (IData)(
                                                            (vlSymsp->TOP__milan_datapath__DOT__ptp_timestamp__DOT__m_axis_tx.tdata 
                                                             >> 0x00000028U)))));
            }
            if (vlSymsp->TOP__milan_datapath__DOT__ptp_timestamp__DOT__m_axis_tx.tlast) {
                vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_tx__DOT__eth_type_valid = 0U;
                vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_tx__DOT__eth_match = 0U;
                vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_tx__DOT__ptp_seq_id_valid = 0U;
                vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_tx__DOT__vlan_tagged = 0U;
            }
            vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_tx__DOT__start_packet 
                = vlSymsp->TOP__milan_datapath__DOT__ptp_timestamp__DOT__m_axis_tx.tlast;
        }
        vlSelfRef.milan_datapath__DOT__stream_table__DOT__en_q_r 
            = vlSelfRef.milan_datapath__DOT__strtbl_en_w;
        vlSelfRef.milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__u_tcdc__DOT__wgray_r1_r 
            = vlSelfRef.milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__u_tcdc__DOT__wptr_gray_r;
        vlSelfRef.milan_datapath__DOT__speed_meta = vlSelfRef.i_mac_speed;
        vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__u_cdc__DOT__rgray_w2_r 
            = vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__u_cdc__DOT__rgray_w1_r;
        vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__u_cdc__DOT__rgray_w1_r 
            = vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__u_cdc__DOT__rptr_gray_r;
    } else {
        vlSelfRef.milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__u_tcdc__DOT__wgray_r2_r = 0U;
        vlSelfRef.milan_datapath__DOT__speed_sync = 2U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__chmap_sel = 0U;
        vlSelfRef.milan_datapath__DOT__adp_link_up_p = 0U;
        vlSelfRef.milan_datapath__DOT__adp_link_down_p = 0U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__strm_dir_r = 0U;
        vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_rx__DOT__eth_match = 0U;
        vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_rx__DOT__msg_type = 0U;
        vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_rx__DOT__ptp_seq_id = 0U;
        vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_rx__DOT__eth_type_valid = 0U;
        vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_rx__DOT__ptp_seq_id_valid = 0U;
        vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_tx__DOT__eth_match = 0U;
        vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_tx__DOT__msg_type = 0U;
        vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_tx__DOT__ptp_seq_id = 0U;
        vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_tx__DOT__eth_type_valid = 0U;
        vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_tx__DOT__ptp_seq_id_valid = 0U;
        vlSelfRef.milan_datapath__DOT__stream_table__DOT__en_q_r = 0U;
        vlSelfRef.milan_datapath__DOT__g_aif_tdm_master__DOT__g_solo__DOT__aaf_capture__DOT__u_tcdc__DOT__wgray_r1_r = 0U;
        vlSelfRef.milan_datapath__DOT__speed_meta = 2U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__ptp_ilat = 0U;
        vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_rx__DOT__vlan_tagged = 0U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__ptp_elat = 0U;
        vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_tx__DOT__vlan_tagged = 0U;
        vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__u_cdc__DOT__rgray_w2_r = 0U;
        vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_rx__DOT__start_packet = 1U;
        vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_tx__DOT__start_packet = 1U;
        vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__u_cdc__DOT__rgray_w1_r = 0U;
    }
    vlSelfRef.o_mac_is_1g = (1U & ((0x00000020U & vlSelfRef.milan_datapath__DOT__csr__DOT__mac_ctrl)
                                    ? (vlSelfRef.milan_datapath__DOT__csr__DOT__mac_ctrl 
                                       >> 4U) : (2U 
                                                 == (IData)(vlSelfRef.milan_datapath__DOT__speed_sync))));
    vlSelfRef.milan_datapath__DOT____Vcellinp__chan_map_render__map_wr_en_i 
        = ((~ (vlSelfRef.milan_datapath__DOT__csr__DOT__chmap_sel 
               >> 8U)) & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__chmap_wr_p));
    vlSelfRef.milan_datapath__DOT__adp_adv__DOT__depart_evt_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__adp_link_down_p) 
           | (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__adp_dep_p));
    vlSelfRef.milan_datapath__DOT__link_up_q = ((IData)(vlSelfRef.axis_resetn) 
                                                && (IData)(vlSelfRef.i_link_up));
    vlSelfRef.milan_datapath__DOT__adp_en_q = ((IData)(vlSelfRef.axis_resetn) 
                                               && (1U 
                                                   & vlSelfRef.milan_datapath__DOT__csr__DOT__adp_ctrl));
    vlSelfRef.milan_datapath__DOT__aaf_tx_tlast = (
                                                   (3U 
                                                    == (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__est_r)) 
                                                   & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_76));
    vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ram_we_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__eng_we_w) 
           | (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ext_wr_ok_w));
    vlSelfRef.milan_datapath__DOT__tctx_maxf_w[0U] 
        = (0x0000ffffU & ((IData)(0x0018U) + ((IData)(0x0018U) 
                                              * ((IData)(
                                                         ((0U 
                                                           == 
                                                           (0x70U 
                                                            & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__tctx_wr_addr_r))) 
                                                          & (IData)(vlSelfRef.milan_datapath__DOT__tctx_w0_wr_w)))
                                                  ? (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_8)
                                                  : vlSelfRef.milan_datapath__DOT__tctx_chans_r[0U]))));
    vlSelfRef.milan_datapath__DOT__tctx_maxf_w[1U] 
        = (0x0000ffffU & ((IData)(0x0018U) + ((IData)(0x0018U) 
                                              * ((IData)(
                                                         ((0x10U 
                                                           == 
                                                           (0x70U 
                                                            & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__tctx_wr_addr_r))) 
                                                          & (IData)(vlSelfRef.milan_datapath__DOT__tctx_w0_wr_w)))
                                                  ? (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_8)
                                                  : vlSelfRef.milan_datapath__DOT__tctx_chans_r[1U]))));
    vlSelfRef.milan_datapath__DOT__tctx_maxf_w[2U] 
        = (0x0000ffffU & ((IData)(0x0018U) + ((IData)(0x0018U) 
                                              * ((IData)(
                                                         ((0x20U 
                                                           == 
                                                           (0x70U 
                                                            & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__tctx_wr_addr_r))) 
                                                          & (IData)(vlSelfRef.milan_datapath__DOT__tctx_w0_wr_w)))
                                                  ? (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_8)
                                                  : vlSelfRef.milan_datapath__DOT__tctx_chans_r[2U]))));
    vlSelfRef.milan_datapath__DOT__tctx_maxf_w[3U] 
        = (0x0000ffffU & ((IData)(0x0018U) + ((IData)(0x0018U) 
                                              * ((IData)(
                                                         ((0x30U 
                                                           == 
                                                           (0x70U 
                                                            & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__tctx_wr_addr_r))) 
                                                          & (IData)(vlSelfRef.milan_datapath__DOT__tctx_w0_wr_w)))
                                                  ? (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_8)
                                                  : vlSelfRef.milan_datapath__DOT__tctx_chans_r[3U]))));
    vlSelfRef.milan_datapath__DOT__tctx_maxf_w[4U] 
        = (0x0000ffffU & ((IData)(0x0018U) + ((IData)(0x0018U) 
                                              * ((IData)(
                                                         ((0x40U 
                                                           == 
                                                           (0x70U 
                                                            & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__tctx_wr_addr_r))) 
                                                          & (IData)(vlSelfRef.milan_datapath__DOT__tctx_w0_wr_w)))
                                                  ? (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_8)
                                                  : vlSelfRef.milan_datapath__DOT__tctx_chans_r[4U]))));
    vlSelfRef.milan_datapath__DOT__tctx_maxf_w[5U] 
        = (0x0000ffffU & ((IData)(0x0018U) + ((IData)(0x0018U) 
                                              * ((IData)(
                                                         ((0x50U 
                                                           == 
                                                           (0x70U 
                                                            & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__tctx_wr_addr_r))) 
                                                          & (IData)(vlSelfRef.milan_datapath__DOT__tctx_w0_wr_w)))
                                                  ? (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_8)
                                                  : vlSelfRef.milan_datapath__DOT__tctx_chans_r[5U]))));
    vlSelfRef.milan_datapath__DOT__tctx_maxf_w[6U] 
        = (0x0000ffffU & ((IData)(0x0018U) + ((IData)(0x0018U) 
                                              * ((IData)(
                                                         ((0x60U 
                                                           == 
                                                           (0x70U 
                                                            & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__tctx_wr_addr_r))) 
                                                          & (IData)(vlSelfRef.milan_datapath__DOT__tctx_w0_wr_w)))
                                                  ? (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_8)
                                                  : vlSelfRef.milan_datapath__DOT__tctx_chans_r[6U]))));
    vlSelfRef.milan_datapath__DOT__tctx_maxf_w[7U] 
        = (0x0000ffffU & ((IData)(0x0018U) + ((IData)(0x0018U) 
                                              * ((IData)(
                                                         ((0x70U 
                                                           == 
                                                           (0x70U 
                                                            & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__tctx_wr_addr_r))) 
                                                          & (IData)(vlSelfRef.milan_datapath__DOT__tctx_w0_wr_w)))
                                                  ? (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_8)
                                                  : vlSelfRef.milan_datapath__DOT__tctx_chans_r[7U]))));
    vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__w0_addr_w 
        = ((0x00000038U & ((IData)(vlSelfRef.m_axis_pcm_tuser) 
                           << 3U)) | (7U & (IData)(vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__chpos_r)));
    milan_datapath__DOT__chan_map_render__DOT__chans_raw_w = 0U;
    if ((0U == (IData)(vlSelfRef.m_axis_pcm_tuser))) {
        milan_datapath__DOT__chan_map_render__DOT__chans_raw_w 
            = (0x0000000fU & vlSelfRef.milan_datapath__DOT__mon_wire_chans_all_w);
    }
    if ((1U == (IData)(vlSelfRef.m_axis_pcm_tuser))) {
        milan_datapath__DOT__chan_map_render__DOT__chans_raw_w 
            = (0x0000000fU & (vlSelfRef.milan_datapath__DOT__mon_wire_chans_all_w 
                              >> 4U));
    }
    if ((2U == (IData)(vlSelfRef.m_axis_pcm_tuser))) {
        milan_datapath__DOT__chan_map_render__DOT__chans_raw_w 
            = (0x0000000fU & (vlSelfRef.milan_datapath__DOT__mon_wire_chans_all_w 
                              >> 8U));
    }
    if ((3U == (IData)(vlSelfRef.m_axis_pcm_tuser))) {
        milan_datapath__DOT__chan_map_render__DOT__chans_raw_w 
            = (0x0000000fU & (vlSelfRef.milan_datapath__DOT__mon_wire_chans_all_w 
                              >> 0x0cU));
    }
    if ((4U == (IData)(vlSelfRef.m_axis_pcm_tuser))) {
        milan_datapath__DOT__chan_map_render__DOT__chans_raw_w 
            = (0x0000000fU & (vlSelfRef.milan_datapath__DOT__mon_wire_chans_all_w 
                              >> 0x10U));
    }
    if ((5U == (IData)(vlSelfRef.m_axis_pcm_tuser))) {
        milan_datapath__DOT__chan_map_render__DOT__chans_raw_w 
            = (0x0000000fU & (vlSelfRef.milan_datapath__DOT__mon_wire_chans_all_w 
                              >> 0x14U));
    }
    if ((6U == (IData)(vlSelfRef.m_axis_pcm_tuser))) {
        milan_datapath__DOT__chan_map_render__DOT__chans_raw_w 
            = (0x0000000fU & (vlSelfRef.milan_datapath__DOT__mon_wire_chans_all_w 
                              >> 0x18U));
    }
    vlSelfRef.milan_datapath__DOT__pcm_route__DOT__cur_route_w = 0U;
    if ((0U == (IData)(vlSelfRef.m_axis_pcm_tuser))) {
        vlSelfRef.milan_datapath__DOT__pcm_route__DOT__cur_route_w 
            = vlSelfRef.milan_datapath__DOT__pcm_route__DOT__route_r[0U];
    }
    if ((1U == (IData)(vlSelfRef.m_axis_pcm_tuser))) {
        vlSelfRef.milan_datapath__DOT__pcm_route__DOT__cur_route_w 
            = vlSelfRef.milan_datapath__DOT__pcm_route__DOT__route_r[1U];
    }
    if ((2U == (IData)(vlSelfRef.m_axis_pcm_tuser))) {
        vlSelfRef.milan_datapath__DOT__pcm_route__DOT__cur_route_w 
            = vlSelfRef.milan_datapath__DOT__pcm_route__DOT__route_r[2U];
    }
    if ((3U == (IData)(vlSelfRef.m_axis_pcm_tuser))) {
        vlSelfRef.milan_datapath__DOT__pcm_route__DOT__cur_route_w 
            = vlSelfRef.milan_datapath__DOT__pcm_route__DOT__route_r[3U];
    }
    if ((4U == (IData)(vlSelfRef.m_axis_pcm_tuser))) {
        vlSelfRef.milan_datapath__DOT__pcm_route__DOT__cur_route_w 
            = vlSelfRef.milan_datapath__DOT__pcm_route__DOT__route_r[4U];
    }
    if ((5U == (IData)(vlSelfRef.m_axis_pcm_tuser))) {
        vlSelfRef.milan_datapath__DOT__pcm_route__DOT__cur_route_w 
            = vlSelfRef.milan_datapath__DOT__pcm_route__DOT__route_r[5U];
    }
    if ((6U == (IData)(vlSelfRef.m_axis_pcm_tuser))) {
        vlSelfRef.milan_datapath__DOT__pcm_route__DOT__cur_route_w 
            = vlSelfRef.milan_datapath__DOT__pcm_route__DOT__route_r[6U];
    }
    if ((7U == (IData)(vlSelfRef.m_axis_pcm_tuser))) {
        milan_datapath__DOT__chan_map_render__DOT__chans_raw_w 
            = (vlSelfRef.milan_datapath__DOT__mon_wire_chans_all_w 
               >> 0x1cU);
        vlSelfRef.milan_datapath__DOT__pcm_route__DOT__cur_route_w 
            = vlSelfRef.milan_datapath__DOT__pcm_route__DOT__route_r[7U];
    }
    vlSelfRef.m_axis_pcm_tdata = vlSelfRef.milan_datapath__DOT__dpkt_pcm_tdata_w;
    vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__emit_w 
        = ((1U == (IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__rstate_r)) 
           & ((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__hold_only_w) 
              | ((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_tvalid_pipe_reg) 
                 >> 1U)));
    vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__stg_drain_w 
        = (1U & (~ (((IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__fill_w) 
                     >> 9U) | (0U == (IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__stg_cnt_r)))));
    vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__map_wr_ok_w 
        = ((0x0aU > (0x0000000fU & vlSelfRef.milan_datapath__DOT__csr__DOT__chmap_sel)) 
           & (IData)(vlSelfRef.milan_datapath__DOT____Vcellinp__chan_map_render__map_wr_en_i));
    vlSelfRef.milan_datapath__DOT__csr_srp_ctx_dir 
        = (1U & ((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__srp_wr_pend_r)
                  ? (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__srp_wr_dir_r)
                  : (~ (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__strm_dir_r))));
    vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__eff_chans_w 
        = ((0U == (IData)(milan_datapath__DOT__chan_map_render__DOT__chans_raw_w))
            ? 2U : (IData)(milan_datapath__DOT__chan_map_render__DOT__chans_raw_w));
    vlSelfRef.milan_datapath__DOT__dpkt_pcm_tready_w 
        = (1U & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pcm_route__DOT__cur_route_w)) 
                 | (IData)(vlSelfRef.m_axis_pcm_tready)));
    vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__s0_w 
        = ((0x00ff0000U & ((IData)(milan_datapath__DOT__i2s_feed_tdata_w) 
                           << 0x00000010U)) | ((0x0000ff00U 
                                                & ((IData)(
                                                           (milan_datapath__DOT__i2s_feed_tdata_w 
                                                            >> 8U)) 
                                                   << 8U)) 
                                               | (0x000000ffU 
                                                  & (IData)(
                                                            (milan_datapath__DOT__i2s_feed_tdata_w 
                                                             >> 0x00000010U)))));
    vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__s1_w 
        = ((0x00ff0000U & ((IData)((milan_datapath__DOT__i2s_feed_tdata_w 
                                    >> 0x00000020U)) 
                           << 0x00000010U)) | ((0x0000ff00U 
                                                & ((IData)(
                                                           (milan_datapath__DOT__i2s_feed_tdata_w 
                                                            >> 0x00000028U)) 
                                                   << 8U)) 
                                               | (0x000000ffU 
                                                  & (IData)(
                                                            (milan_datapath__DOT__i2s_feed_tdata_w 
                                                             >> 0x00000030U)))));
    vlSelfRef.m_axis_pcm_tvalid = ((IData)(vlSelfRef.milan_datapath__DOT__pcm_route__DOT__cur_route_w) 
                                   & (IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__emit_w));
    vlSelfRef.m_axis_pcm_tlast = ((8U >= (IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__remain_r)) 
                                  & (IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__emit_w));
    vlSelfRef.milan_datapath__DOT__rend_pcm_tvalid_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__emit_w) 
           & ((IData)(vlSelfRef.milan_datapath__DOT__pcm_route__DOT__render_active_o) 
              & ((IData)(vlSelfRef.milan_datapath__DOT__route_render_sel_w) 
                 == (IData)(vlSelfRef.m_axis_pcm_tuser))));
    vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__stg_space_w 
        = (7U & (((IData)(4U) - (IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__stg_cnt_r)) 
                 + (1U & (- (IData)((IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__stg_drain_w))))));
    vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__u_cdc__DOT__wptr_bin_n 
        = (0x0000001fU & ((IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__u_cdc__DOT__wptr_bin_r) 
                          + ((~ (IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__cdc_wfull_w)) 
                             & (IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__cdc_wen_r))));
    vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_rx__DOT__byte_counter 
        = vlSelfRef.__Vdly__milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_rx__DOT__byte_counter;
    vlSelfRef.milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_tx__DOT__byte_counter 
        = vlSelfRef.__Vdly__milan_datapath__DOT__ptp_timestamp__DOT__ptp_ts_tx__DOT__byte_counter;
    vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__ch1_w 
        = (0x0000000fU & (((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__chpos_r)) 
                          & (- (IData)(((IData)(vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__eff_chans_w) 
                                        != (0x0000000fU 
                                            & ((IData)(1U) 
                                               + (IData)(vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__chpos_r))))))));
    vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_tready_pipe 
        = ((0U == (IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__rstate_r)) 
           | ((2U == (IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__rstate_r)) 
              | ((1U == (IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__rstate_r)) 
                 & ((~ (IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__hold_only_w)) 
                    & (IData)(vlSelfRef.milan_datapath__DOT__dpkt_pcm_tready_w)))));
    vlSelfRef.milan_datapath__DOT__dpkt_acc_w = ((IData)(vlSelfRef.milan_datapath__DOT__dpkt_pcm_tready_w) 
                                                 & (IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__emit_w));
    vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__pcm_acc_w 
        = (((1U & vlSelfRef.milan_datapath__DOT__csr__DOT__chmap_ctrl)
             ? (IData)(vlSelfRef.milan_datapath__DOT__chmap_phys_v_w)
             : (IData)(vlSelfRef.milan_datapath__DOT__rend_pcm_tvalid_w)) 
           & ((IData)(vlSelfRef.m_axis_pcm_tready) 
              | vlSelfRef.milan_datapath__DOT__csr__DOT__chmap_ctrl));
    vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__w1_addr_w 
        = ((0x00000038U & ((IData)(vlSelfRef.m_axis_pcm_tuser) 
                           << 3U)) | (7U & (IData)(vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__ch1_w)));
    vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__pop_w 
        = (((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_tvalid_pipe_reg) 
            >> 1U) & (IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_tready_pipe));
    milan_datapath__DOT__chan_map_render__DOT__avb_ok_w 
        = ((8U > (IData)(vlSelfRef.m_axis_pcm_tuser)) 
           & (IData)(vlSelfRef.milan_datapath__DOT__dpkt_acc_w));
    vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__w0_en_w 
        = ((8U > (IData)(vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__chpos_r)) 
           & (IData)(milan_datapath__DOT__chan_map_render__DOT__avb_ok_w));
    vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__w1_en_w 
        = ((8U > (IData)(vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__ch1_w)) 
           & (IData)(milan_datapath__DOT__chan_map_render__DOT__avb_ok_w));
}
