// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vmilan_datapath.h for the primary calling header

#include "Vmilan_datapath__pch.h"

extern const VlUnpacked<CData/*2:0*/, 512> Vmilan_datapath__ConstPool__TABLE_h08b0e54a_0;
extern const VlUnpacked<CData/*2:0*/, 512> Vmilan_datapath__ConstPool__TABLE_hdb612095_0;
extern const VlUnpacked<CData/*2:0*/, 32> Vmilan_datapath__ConstPool__TABLE_h9a1b00ed_0;
extern const VlWide<10>/*319:0*/ Vmilan_datapath__ConstPool__CONST_h8a04c6be_0;
extern const VlUnpacked<CData/*3:0*/, 512> Vmilan_datapath__ConstPool__TABLE_hc68454f1_0;

VL_ATTR_COLD void Vmilan_datapath___024root___stl_sequent__TOP__1(Vmilan_datapath___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vmilan_datapath___024root___stl_sequent__TOP__1\n"); );
    Vmilan_datapath__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    CData/*4:0*/ milan_datapath__DOT__pkt_slot_w;
    milan_datapath__DOT__pkt_slot_w = 0;
    CData/*6:0*/ milan_datapath__DOT__csr_tctx_rd_addr_w;
    milan_datapath__DOT__csr_tctx_rd_addr_w = 0;
    QData/*63:0*/ milan_datapath__DOT__i2s_feed_tdata_w;
    milan_datapath__DOT__i2s_feed_tdata_w = 0;
    VlWide<3>/*64:0*/ milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__0__KET____DOT__esub_w;
    VL_ZERO_W(65, milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__0__KET____DOT__esub_w);
    VlWide<3>/*64:0*/ milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__1__KET____DOT__esub_w;
    VL_ZERO_W(65, milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__1__KET____DOT__esub_w);
    VlWide<3>/*64:0*/ milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__2__KET____DOT__esub_w;
    VL_ZERO_W(65, milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__2__KET____DOT__esub_w);
    VlWide<3>/*64:0*/ milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__3__KET____DOT__esub_w;
    VL_ZERO_W(65, milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__3__KET____DOT__esub_w);
    VlWide<3>/*64:0*/ milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__4__KET____DOT__esub_w;
    VL_ZERO_W(65, milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__4__KET____DOT__esub_w);
    VlWide<3>/*64:0*/ milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__5__KET____DOT__esub_w;
    VL_ZERO_W(65, milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__5__KET____DOT__esub_w);
    VlWide<3>/*64:0*/ milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__6__KET____DOT__esub_w;
    VL_ZERO_W(65, milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__6__KET____DOT__esub_w);
    VlWide<3>/*64:0*/ milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__7__KET____DOT__esub_w;
    VL_ZERO_W(65, milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__7__KET____DOT__esub_w);
    VlWide<3>/*64:0*/ milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__8__KET____DOT__esub_w;
    VL_ZERO_W(65, milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__8__KET____DOT__esub_w);
    VlWide<3>/*64:0*/ milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__9__KET____DOT__esub_w;
    VL_ZERO_W(65, milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__9__KET____DOT__esub_w);
    VlWide<3>/*64:0*/ milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__10__KET____DOT__esub_w;
    VL_ZERO_W(65, milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__10__KET____DOT__esub_w);
    VlWide<3>/*64:0*/ milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__11__KET____DOT__esub_w;
    VL_ZERO_W(65, milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__11__KET____DOT__esub_w);
    VlWide<3>/*64:0*/ milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__12__KET____DOT__esub_w;
    VL_ZERO_W(65, milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__12__KET____DOT__esub_w);
    VlWide<3>/*64:0*/ milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__13__KET____DOT__esub_w;
    VL_ZERO_W(65, milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__13__KET____DOT__esub_w);
    VlWide<3>/*64:0*/ milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__14__KET____DOT__esub_w;
    VL_ZERO_W(65, milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__14__KET____DOT__esub_w);
    SData/*8:0*/ milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__req_w;
    milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__req_w = 0;
    SData/*15:0*/ milan_datapath__DOT__lwsrp__DOT__tx__DOT__unnamedblk1__DOT__vh;
    milan_datapath__DOT__lwsrp__DOT__tx__DOT__unnamedblk1__DOT__vh = 0;
    IData/*31:0*/ milan_datapath__DOT__lwsrp__DOT__tx__DOT__unnamedblk1__DOT__lb;
    milan_datapath__DOT__lwsrp__DOT__tx__DOT__unnamedblk1__DOT__lb = 0;
    IData/*31:0*/ milan_datapath__DOT__lwsrp__DOT__tx__DOT__unnamedblk1__DOT__unnamedblk2__DOT__k;
    milan_datapath__DOT__lwsrp__DOT__tx__DOT__unnamedblk1__DOT__unnamedblk2__DOT__k = 0;
    CData/*0:0*/ milan_datapath__DOT__aecp_listener__DOT__u_val__DOT__w_type_ok;
    milan_datapath__DOT__aecp_listener__DOT__u_val__DOT__w_type_ok = 0;
    CData/*0:0*/ milan_datapath__DOT__aecp_listener__DOT__u_val__DOT__m_tvalid_l;
    milan_datapath__DOT__aecp_listener__DOT__u_val__DOT__m_tvalid_l = 0;
    SData/*15:0*/ milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__hit;
    milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__hit = 0;
    CData/*0:0*/ milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_probe_resp;
    milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_probe_resp = 0;
    QData/*63:0*/ milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_resp;
    milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_resp = 0;
    CData/*0:0*/ milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_frame_en_w;
    milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_frame_en_w = 0;
    VlWide<10>/*316:0*/ milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_frame_w;
    VL_ZERO_W(317, milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_frame_w);
    CData/*3:0*/ milan_datapath__DOT__chan_map_render__DOT__chans_raw_w;
    milan_datapath__DOT__chan_map_render__DOT__chans_raw_w = 0;
    CData/*0:0*/ milan_datapath__DOT__chan_map_render__DOT__avb_ok_w;
    milan_datapath__DOT__chan_map_render__DOT__avb_ok_w = 0;
    CData/*0:0*/ milan_datapath__DOT__avtp_rx_monitor__DOT____VlemCall_4__ms_locked;
    CData/*0:0*/ milan_datapath__DOT__avtp_rx_monitor__DOT__lock_ok_w;
    milan_datapath__DOT__avtp_rx_monitor__DOT__lock_ok_w = 0;
    IData/*31:0*/ milan_datapath__DOT__avtp_rx_monitor__DOT__eng_wdata_w;
    milan_datapath__DOT__avtp_rx_monitor__DOT__eng_wdata_w = 0;
    CData/*3:0*/ milan_datapath__DOT__acmp_responder__DOT__tmr_rd_idx_w;
    milan_datapath__DOT__acmp_responder__DOT__tmr_rd_idx_w = 0;
    IData/*31:0*/ milan_datapath__DOT__adp_adv__DOT__unnamedblk1__DOT__k;
    milan_datapath__DOT__adp_adv__DOT__unnamedblk1__DOT__k = 0;
    SData/*15:0*/ milan_datapath__DOT__csr__DOT__strm_read_mux__DOT__coff;
    milan_datapath__DOT__csr__DOT__strm_read_mux__DOT__coff = 0;
    QData/*47:0*/ milan_datapath__DOT__aaf_packetizer__DOT__eff_dmac_w;
    milan_datapath__DOT__aaf_packetizer__DOT__eff_dmac_w = 0;
    QData/*63:0*/ milan_datapath__DOT__aaf_packetizer__DOT__stream_id_w;
    milan_datapath__DOT__aaf_packetizer__DOT__stream_id_w = 0;
    IData/*31:0*/ milan_datapath__DOT__aaf_packetizer__DOT__frame_bytes__DOT__unnamedblk5__DOT__k;
    milan_datapath__DOT__aaf_packetizer__DOT__frame_bytes__DOT__unnamedblk5__DOT__k = 0;
    CData/*0:0*/ milan_datapath__DOT__chan_map_capture__DOT__lb_sel_ok_w;
    milan_datapath__DOT__chan_map_capture__DOT__lb_sel_ok_w = 0;
    SData/*15:0*/ __Vfunc_milan_datapath__DOT__lwsrp__DOT__tx__DOT__vech__27__Vfuncout;
    __Vfunc_milan_datapath__DOT__lwsrp__DOT__tx__DOT__vech__27__Vfuncout = 0;
    CData/*0:0*/ __Vfunc_milan_datapath__DOT__lwsrp__DOT__tx__DOT__vech__27__lva;
    __Vfunc_milan_datapath__DOT__lwsrp__DOT__tx__DOT__vech__27__lva = 0;
    QData/*63:0*/ __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__150__Vfuncout;
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__150__Vfuncout = 0;
    CData/*2:0*/ __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__150__b;
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__150__b = 0;
    VlUnpacked<CData/*7:0*/, 64> __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__150__f;
    for (int __Vi0 = 0; __Vi0 < 64; ++__Vi0) {
        __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__150__f[__Vi0] = 0;
    }
    IData/*31:0*/ __Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__ms_locked__186__w;
    __Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__ms_locked__186__w = 0;
    CData/*7:0*/ __Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__202__Vfuncout;
    __Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__202__Vfuncout = 0;
    CData/*2:0*/ __Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__202__s;
    __Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__202__s = 0;
    CData/*6:0*/ __Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__274__Vfuncout;
    __Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__274__Vfuncout = 0;
    CData/*2:0*/ __Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__274__t;
    __Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__274__t = 0;
    SData/*8:0*/ __VdfgRegularize_h6e95ff9d_0_24;
    __VdfgRegularize_h6e95ff9d_0_24 = 0;
    CData/*0:0*/ __VdfgRegularize_h6e95ff9d_0_81;
    __VdfgRegularize_h6e95ff9d_0_81 = 0;
    CData/*0:0*/ __VdfgRegularize_h6e95ff9d_0_88;
    __VdfgRegularize_h6e95ff9d_0_88 = 0;
    CData/*4:0*/ __VdfgRegularize_h6e95ff9d_0_93;
    __VdfgRegularize_h6e95ff9d_0_93 = 0;
    VlWide<3>/*95:0*/ __Vtemp_13;
    VlWide<3>/*95:0*/ __Vtemp_14;
    VlWide<3>/*95:0*/ __Vtemp_16;
    VlWide<3>/*95:0*/ __Vtemp_17;
    VlWide<3>/*95:0*/ __Vtemp_19;
    VlWide<3>/*95:0*/ __Vtemp_20;
    VlWide<3>/*95:0*/ __Vtemp_22;
    VlWide<3>/*95:0*/ __Vtemp_23;
    VlWide<3>/*95:0*/ __Vtemp_25;
    VlWide<3>/*95:0*/ __Vtemp_26;
    VlWide<3>/*95:0*/ __Vtemp_28;
    VlWide<3>/*95:0*/ __Vtemp_29;
    VlWide<3>/*95:0*/ __Vtemp_31;
    VlWide<3>/*95:0*/ __Vtemp_32;
    VlWide<3>/*95:0*/ __Vtemp_34;
    VlWide<3>/*95:0*/ __Vtemp_35;
    VlWide<3>/*95:0*/ __Vtemp_37;
    VlWide<3>/*95:0*/ __Vtemp_38;
    VlWide<3>/*95:0*/ __Vtemp_40;
    VlWide<3>/*95:0*/ __Vtemp_41;
    VlWide<3>/*95:0*/ __Vtemp_43;
    VlWide<3>/*95:0*/ __Vtemp_44;
    VlWide<3>/*95:0*/ __Vtemp_46;
    VlWide<3>/*95:0*/ __Vtemp_47;
    VlWide<3>/*95:0*/ __Vtemp_49;
    VlWide<3>/*95:0*/ __Vtemp_50;
    VlWide<3>/*95:0*/ __Vtemp_52;
    VlWide<3>/*95:0*/ __Vtemp_53;
    VlWide<3>/*95:0*/ __Vtemp_55;
    VlWide<3>/*95:0*/ __Vtemp_56;
    VlWide<3>/*95:0*/ __Vtemp_58;
    VlWide<3>/*95:0*/ __Vtemp_59;
    VlWide<3>/*95:0*/ __Vtemp_61;
    VlWide<3>/*95:0*/ __Vtemp_62;
    IData/*31:0*/ __Vilp1;
    IData/*31:0*/ __Vilp2;
    // Body
    vlSelfRef.milan_datapath__DOT__csr__DOT__shadow_axi_we 
        = vlSelfRef.milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw;
    __VdfgRegularize_h6e95ff9d_0_81 = ((0x0810U == (IData)(vlSelfRef.s_axi_awaddr)) 
                                       & (IData)(vlSelfRef.s_axi_awready));
    vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__hdr_shifted[0U] 
        = (IData)(vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__beat_be);
    vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__hdr_shifted[1U] 
        = (IData)((vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__beat_be 
                   >> 0x00000020U));
    vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__hdr_shifted[2U] 
        = vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__eth_header[0U];
    vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__hdr_shifted[3U] 
        = vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__eth_header[1U];
    vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__hdr_shifted[4U] 
        = vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__eth_header[2U];
    vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__hdr_shifted[5U] 
        = vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__eth_header[3U];
    vlSelfRef.m_axis_pcm_tdata = vlSelfRef.milan_datapath__DOT__dpkt_pcm_tdata_w;
    vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__xl_in 
        = ((0x00ff0000U & ((IData)(vlSelfRef.milan_datapath__DOT__dpkt_pcm_tdata_w) 
                           << 0x00000010U)) | ((0x0000ff00U 
                                                & ((IData)(
                                                           (vlSelfRef.milan_datapath__DOT__dpkt_pcm_tdata_w 
                                                            >> 8U)) 
                                                   << 8U)) 
                                               | (0x000000ffU 
                                                  & (IData)(
                                                            (vlSelfRef.milan_datapath__DOT__dpkt_pcm_tdata_w 
                                                             >> 0x00000010U)))));
    vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__xr_in 
        = ((0x00ff0000U & ((IData)((vlSelfRef.milan_datapath__DOT__dpkt_pcm_tdata_w 
                                    >> 0x00000020U)) 
                           << 0x00000010U)) | ((0x0000ff00U 
                                                & ((IData)(
                                                           (vlSelfRef.milan_datapath__DOT__dpkt_pcm_tdata_w 
                                                            >> 0x00000028U)) 
                                                   << 8U)) 
                                               | (0x000000ffU 
                                                  & (IData)(
                                                            (vlSelfRef.milan_datapath__DOT__dpkt_pcm_tdata_w 
                                                             >> 0x00000030U)))));
    vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__ig_to_val_tlast 
        = ((2U == (IData)(vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_ingress__DOT__rstate_r)) 
           & ((IData)(vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_ingress__DOT__hold_last_r) 
              | (((IData)(vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_ingress__DOT__frame_fifo__DOT__m_axis_tvalid_pipe_reg) 
                  >> 1U) & ((0U == Vmilan_datapath__ConstPool__TABLE_h08b0e54a_0
                             [vlSelfRef.__VdfgRegularize_h6e95ff9d_0_101]) 
                            & (vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_ingress__DOT__frame_fifo__DOT__m_axis_pipe_reg[1U][2U] 
                               >> 8U)))));
    vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_ingress__DOT__w_out = 0ULL;
    if ((0U < (IData)(vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_ingress__DOT__hold_cnt_r))) {
        vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_ingress__DOT__w_out 
            = ((0x00ffffffffffffffULL & vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_ingress__DOT__w_out) 
               | ((QData)((IData)((0x000000ffU & vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_ingress__DOT__hold_r))) 
                  << 0x00000038U));
    }
    if ((1U < (IData)(vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_ingress__DOT__hold_cnt_r))) {
        vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_ingress__DOT__w_out 
            = ((0xff00ffffffffffffULL & vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_ingress__DOT__w_out) 
               | ((QData)((IData)((0x000000ffU & (vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_ingress__DOT__hold_r 
                                                  >> 8U)))) 
                  << 0x00000030U));
    }
    if ((2U < (IData)(vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_ingress__DOT__hold_cnt_r))) {
        vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_ingress__DOT__w_out 
            = ((0xffff00ffffffffffULL & vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_ingress__DOT__w_out) 
               | ((QData)((IData)((0x000000ffU & (vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_ingress__DOT__hold_r 
                                                  >> 0x10U)))) 
                  << 0x00000028U));
    }
    if ((3U < (IData)(vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_ingress__DOT__hold_cnt_r))) {
        vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_ingress__DOT__w_out 
            = ((0xffffff00ffffffffULL & vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_ingress__DOT__w_out) 
               | ((QData)((IData)((vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_ingress__DOT__hold_r 
                                   >> 0x18U))) << 0x00000020U));
    }
    if ((1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_ingress__DOT__hold_last_r)))) {
        if ((0U < Vmilan_datapath__ConstPool__TABLE_hdb612095_0
             [vlSelfRef.__VdfgRegularize_h6e95ff9d_0_101])) {
            vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_ingress__DOT__w_out 
                = ((0xffffffff00ffffffULL & vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_ingress__DOT__w_out) 
                   | ((QData)((IData)((0x000000ffU 
                                       & vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_ingress__DOT__frame_fifo__DOT__m_axis_pipe_reg[1U][0U]))) 
                      << 0x00000018U));
        }
        if ((1U < Vmilan_datapath__ConstPool__TABLE_hdb612095_0
             [vlSelfRef.__VdfgRegularize_h6e95ff9d_0_101])) {
            vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_ingress__DOT__w_out 
                = ((0xffffffffff00ffffULL & vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_ingress__DOT__w_out) 
                   | ((QData)((IData)((0x000000ffU 
                                       & (vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_ingress__DOT__frame_fifo__DOT__m_axis_pipe_reg[1U][0U] 
                                          >> 8U)))) 
                      << 0x00000010U));
        }
        if ((2U < Vmilan_datapath__ConstPool__TABLE_hdb612095_0
             [vlSelfRef.__VdfgRegularize_h6e95ff9d_0_101])) {
            vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_ingress__DOT__w_out 
                = ((0xffffffffffff00ffULL & vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_ingress__DOT__w_out) 
                   | ((QData)((IData)((0x000000ffU 
                                       & (vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_ingress__DOT__frame_fifo__DOT__m_axis_pipe_reg[1U][0U] 
                                          >> 0x00000010U)))) 
                      << 8U));
        }
        if ((3U < Vmilan_datapath__ConstPool__TABLE_hdb612095_0
             [vlSelfRef.__VdfgRegularize_h6e95ff9d_0_101])) {
            vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_ingress__DOT__w_out 
                = ((0xffffffffffffff00ULL & vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_ingress__DOT__w_out) 
                   | (IData)((IData)((vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_ingress__DOT__frame_fifo__DOT__m_axis_pipe_reg[1U][0U] 
                                      >> 0x00000018U))));
        }
    }
    milan_datapath__DOT__chan_map_capture__DOT__lb_sel_ok_w 
        = ((8U > (0x0000000fU & (vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r
                                 [vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__slot_r] 
                                 >> 8U))) & (4U > (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_10)));
    vlSelfRef.milan_datapath__DOT__eff_crft_dmac_w 
        = (0x0000ffffffffffffULL & ((0U != vlSelfRef.milan_datapath__DOT__cfg_crft_dmac)
                                     ? vlSelfRef.milan_datapath__DOT__cfg_crft_dmac
                                     : (8ULL + vlSelfRef.milan_datapath__DOT__eff_aaf_dmac)));
    milan_datapath__DOT__aaf_packetizer__DOT__eff_dmac_w 
        = ((0U == (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__et_r))
            ? vlSelfRef.milan_datapath__DOT__eff_aaf_dmac
            : vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__edmac_r);
    vlSelfRef.milan_datapath__DOT__i2s_feed_lpf_act_w 
        = ((~ vlSelfRef.milan_datapath__DOT__csr__DOT__chmap_ctrl) 
           & (IData)(vlSelfRef.milan_datapath__DOT__pcm_lpf_active));
    vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__c_eff_w 
        = (((0U == (IData)(vlSelfRef.milan_datapath__DOT__i2s_feed_chans_w)) 
            | (8U < (IData)(vlSelfRef.milan_datapath__DOT__i2s_feed_chans_w)))
            ? 2U : (7U & (IData)(vlSelfRef.milan_datapath__DOT__i2s_feed_chans_w)));
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
    vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__ext_trd_go_w 
        = (((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_67) 
            | ((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rds_busy_r) 
               & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rds_dir_r))) 
           & ((3U == (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__est_r)) 
              | ((~ (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__grant_v_w)) 
                 & (0U == (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__est_r)))));
    milan_datapath__DOT__avtp_rx_monitor__DOT__lock_ok_w 
        = (((IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ev_s_r) 
            != (7U & (IData)(vlSelfRef.milan_datapath__DOT__route_render_sel_w))) 
           | (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_82));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_76 = ((IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__beat_r) 
                                                 == 
                                                 (0x0000001fU 
                                                  & ((IData)(5U) 
                                                     + 
                                                     ((IData)(6U) 
                                                      * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_68)))));
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
    vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__is_full3_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__lstn_incl_r) 
           & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__is_full_w));
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
    milan_datapath__DOT__avtp_rx_monitor__DOT__eng_wdata_w = 0U;
    vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__eng_waddr_w = 0U;
    if ((4U == (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__mst_r))) {
        if ((0U == (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__wrph_r))) {
            milan_datapath__DOT__avtp_rx_monitor__DOT__eng_wdata_w 
                = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__monst_r;
            vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__189__s 
                = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ev_s_r;
            vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__189__Vfuncout 
                = (8U | ((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__189__s) 
                         << 5U));
            vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__eng_waddr_w 
                = vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__189__Vfuncout;
        } else if ((1U == (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__wrph_r))) {
            milan_datapath__DOT__avtp_rx_monitor__DOT__eng_wdata_w 
                = ((vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__cur_r[4U] 
                    << 0x0000001eU) | (vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__cur_r[3U] 
                                       >> 2U));
            vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__190__s 
                = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ev_s_r;
            vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__190__Vfuncout 
                = (9U | ((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__190__s) 
                         << 5U));
            vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__eng_waddr_w 
                = vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__190__Vfuncout;
        } else {
            milan_datapath__DOT__avtp_rx_monitor__DOT__eng_wdata_w 
                = ((vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__cur_r[1U] 
                    << 0x0000001eU) | (vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__cur_r[0U] 
                                       >> 2U));
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
                milan_datapath__DOT__avtp_rx_monitor__DOT__eng_wdata_w 
                    = ((((vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ram_q_r 
                          >> 0x10U) + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ddrop_add_r)) 
                        << 0x00000010U) | (0x0000ffffU 
                                           & (vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ram_q_r 
                                              + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_add_r))));
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
                milan_datapath__DOT__avtp_rx_monitor__DOT__eng_wdata_w 
                    = ((IData)(1U) + vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ram_q_r);
                vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__193__s 
                    = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ev_s_r;
                vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__193__Vfuncout 
                    = (0x11U | ((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__193__s) 
                                << 5U));
                vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__eng_waddr_w 
                    = vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__193__Vfuncout;
            } else if ((3U == (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__wrph_r))) {
                milan_datapath__DOT__avtp_rx_monitor__DOT__eng_wdata_w 
                    = (0xffffefffU & vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ram_q_r);
                vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__194__s 
                    = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ev_s_r;
                vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__194__Vfuncout 
                    = (8U | ((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__194__s) 
                             << 5U));
                vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__eng_waddr_w 
                    = vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__194__Vfuncout;
            }
        } else if (vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__bind_zero_r) {
            milan_datapath__DOT__avtp_rx_monitor__DOT__eng_wdata_w = 0U;
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
            milan_datapath__DOT__avtp_rx_monitor__DOT__eng_wdata_w 
                = (vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ram_q_r 
                   + ((4U == (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__inc_next_w))
                       ? (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__mr_add_r)
                       : 1U));
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
                        milan_datapath__DOT__avtp_rx_monitor__DOT__eng_wdata_w 
                            = (IData)((vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__fmt_in0_r 
                                       >> 0x20U));
                        vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__197__s 
                            = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ev_s_r;
                        vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__197__Vfuncout 
                            = (3U | ((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__197__s) 
                                     << 5U));
                        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__eng_waddr_w 
                            = vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__197__Vfuncout;
                    }
                }
            } else if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__wrph_r))) {
                if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__wrph_r))) {
                    milan_datapath__DOT__avtp_rx_monitor__DOT__eng_wdata_w 
                        = (IData)(vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__fmt_in0_r);
                    vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__198__s 
                        = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ev_s_r;
                    vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__198__Vfuncout 
                        = (2U | ((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__198__s) 
                                 << 5U));
                    vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__eng_waddr_w 
                        = vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__198__Vfuncout;
                } else {
                    milan_datapath__DOT__avtp_rx_monitor__DOT__eng_wdata_w 
                        = vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__view0_r[5U];
                    vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__199__s 
                        = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ev_s_r;
                    vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__199__Vfuncout 
                        = (1U | ((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__199__s) 
                                 << 5U));
                    vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__eng_waddr_w 
                        = vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__199__Vfuncout;
                }
            } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__wrph_r))) {
                milan_datapath__DOT__avtp_rx_monitor__DOT__eng_wdata_w 
                    = vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__view0_r[4U];
                vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__200__s 
                    = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ev_s_r;
                vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__200__Vfuncout 
                    = ((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__200__s) 
                       << 5U);
                vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__eng_waddr_w 
                    = vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__200__Vfuncout;
            } else {
                milan_datapath__DOT__avtp_rx_monitor__DOT__eng_wdata_w 
                    = (0xffffc0ffU & vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ram_q_r);
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
    vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__stg_drain_w 
        = (1U & (~ (((IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__fill_w) 
                     >> 9U) | (0U == (IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__stg_cnt_r)))));
    vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__l0_state_w[0U] 
        = (IData)(vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_l0__DOT__locking_controller_id_r);
    vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__l0_state_w[1U] 
        = (IData)((vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_l0__DOT__locking_controller_id_r 
                   >> 0x00000020U));
    vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__l0_state_w[2U] = 0U;
    vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__l0_state_w[3U] = 0U;
    vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__l0_state_w[4U] 
        = ((0xfffc0000U & vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__l0_state_w[4U]) 
           | (((IData)(vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_l0__DOT__current_config_r) 
               << 2U) | ((IData)(vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_l0__DOT__locked_r) 
                         << 1U)));
    vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__l0_state_w[4U] 
        = ((0x0003ffffU & vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__l0_state_w[4U]) 
           | ((IData)(vlSelfRef.milan_datapath__DOT__cfg_adp_entity_id) 
              << 0x00000012U));
    vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__l0_state_w[5U] 
        = (((IData)(vlSelfRef.milan_datapath__DOT__cfg_adp_entity_id) 
            >> 0x0000000eU) | ((IData)((vlSelfRef.milan_datapath__DOT__cfg_adp_entity_id 
                                        >> 0x00000020U)) 
                               << 0x00000012U));
    vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__l0_state_w[6U] 
        = ((IData)((vlSelfRef.milan_datapath__DOT__cfg_adp_entity_id 
                    >> 0x00000020U)) >> 0x0000000eU);
    vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__emit_w 
        = ((1U == (IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__rstate_r)) 
           & ((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__hold_only_w) 
              | ((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_tvalid_pipe_reg) 
                 >> 1U)));
    milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__hit 
        = (((((((vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_valid[15U] 
                 & (0ULL == (vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_mask[15U] 
                             & (vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_key[15U] 
                                ^ vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__dmac)))) 
                << 3U) | ((vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_valid[14U] 
                           & (0ULL == (vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_mask[14U] 
                                       & (vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_key[14U] 
                                          ^ vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__dmac)))) 
                          << 2U)) | (((vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_valid[13U] 
                                       & (0ULL == (vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_mask[13U] 
                                                   & (vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_key[13U] 
                                                      ^ vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__dmac)))) 
                                      << 1U) | (vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_valid[12U] 
                                                & (0ULL 
                                                   == 
                                                   (vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_mask[12U] 
                                                    & (vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_key[12U] 
                                                       ^ vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__dmac)))))) 
             << 0x0000000cU) | (((((vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_valid[11U] 
                                    & (0ULL == (vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_mask[11U] 
                                                & (vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_key[11U] 
                                                   ^ vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__dmac)))) 
                                   << 3U) | ((vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_valid[10U] 
                                              & (0ULL 
                                                 == 
                                                 (vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_mask[10U] 
                                                  & (vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_key[10U] 
                                                     ^ vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__dmac)))) 
                                             << 2U)) 
                                 | (((vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_valid[9U] 
                                      & (0ULL == (vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_mask[9U] 
                                                  & (vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_key[9U] 
                                                     ^ vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__dmac)))) 
                                     << 1U) | (vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_valid[8U] 
                                               & (0ULL 
                                                  == 
                                                  (vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_mask[8U] 
                                                   & (vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_key[8U] 
                                                      ^ vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__dmac)))))) 
                                << 8U)) | ((((((vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_valid[7U] 
                                                & (0ULL 
                                                   == 
                                                   (vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_mask[7U] 
                                                    & (vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_key[7U] 
                                                       ^ vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__dmac)))) 
                                               << 3U) 
                                              | ((vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_valid[6U] 
                                                  & (0ULL 
                                                     == 
                                                     (vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_mask[6U] 
                                                      & (vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_key[6U] 
                                                         ^ vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__dmac)))) 
                                                 << 2U)) 
                                             | (((vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_valid[5U] 
                                                  & (0ULL 
                                                     == 
                                                     (vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_mask[5U] 
                                                      & (vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_key[5U] 
                                                         ^ vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__dmac)))) 
                                                 << 1U) 
                                                | (vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_valid[4U] 
                                                   & (0ULL 
                                                      == 
                                                      (vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_mask[4U] 
                                                       & (vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_key[4U] 
                                                          ^ vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__dmac)))))) 
                                            << 4U) 
                                           | ((((vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_valid[3U] 
                                                 & (0ULL 
                                                    == 
                                                    (vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_mask[3U] 
                                                     & (vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_key[3U] 
                                                        ^ vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__dmac)))) 
                                                << 3U) 
                                               | ((vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_valid[2U] 
                                                   & (0ULL 
                                                      == 
                                                      (vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_mask[2U] 
                                                       & (vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_key[2U] 
                                                          ^ vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__dmac)))) 
                                                  << 2U)) 
                                              | (((vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_valid[1U] 
                                                   & (0ULL 
                                                      == 
                                                      (vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_mask[1U] 
                                                       & (vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_key[1U] 
                                                          ^ vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__dmac)))) 
                                                  << 1U) 
                                                 | (vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_valid[0U] 
                                                    & (0ULL 
                                                       == 
                                                       (vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_mask[0U] 
                                                        & (vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_key[0U] 
                                                           ^ vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__dmac))))))));
    milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_probe_resp 
        = ((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_acmp_base) 
           & ((1U == (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_msg_r)) 
              & ((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_lstnr_us) 
                 & ((9U > (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_luid_r)) 
                    & (((3U == (7U & (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r[9U] 
                                      >> 0x0000001aU))) 
                        | (4U == (7U & (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r[9U] 
                                        >> 0x0000001aU)))) 
                       & (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_sm_en))))));
    vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_lstn_hit 
        = ((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_acmp_base) 
           & ((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_is_lstn_cmd) 
              & (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_lstnr_us)));
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
    vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__eready_w 
        = (((((((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_48) 
                << 3U) | ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_47) 
                          << 2U)) | (((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_46) 
                                      << 1U) | (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_45))) 
             << 0x0000000bU) | (((((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_44) 
                                   << 3U) | ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_43) 
                                             << 2U)) 
                                 | (((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_42) 
                                     << 1U) | (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_41))) 
                                << 7U)) | (((((2U & 
                                               (((0x00000040U 
                                                  & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__dir_r))
                                                  ? 
                                                 ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r) 
                                                  >> 6U)
                                                  : 
                                                 (((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r) 
                                                   >> 6U) 
                                                  & ((2U 
                                                      == 
                                                      (3U 
                                                       & (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r 
                                                          >> 0x0000000cU))) 
                                                     | (3U 
                                                        == 
                                                        (3U 
                                                         & (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r 
                                                            >> 0x0000000cU)))))) 
                                                << 1U)) 
                                              | (1U 
                                                 & ((0x00000020U 
                                                     & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__dir_r))
                                                     ? 
                                                    ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r) 
                                                     >> 5U)
                                                     : 
                                                    (((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r) 
                                                      >> 5U) 
                                                     & ((2U 
                                                         == 
                                                         (3U 
                                                          & (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r 
                                                             >> 0x0000000aU))) 
                                                        | (3U 
                                                           == 
                                                           (3U 
                                                            & (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r 
                                                               >> 0x0000000aU)))))))) 
                                             << 5U) 
                                            | (((2U 
                                                 & (((0x00000010U 
                                                      & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__dir_r))
                                                      ? 
                                                     ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r) 
                                                      >> 4U)
                                                      : 
                                                     (((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r) 
                                                       >> 4U) 
                                                      & ((2U 
                                                          == 
                                                          (3U 
                                                           & (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r 
                                                              >> 8U))) 
                                                         | (3U 
                                                            == 
                                                            (3U 
                                                             & (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r 
                                                                >> 8U)))))) 
                                                    << 1U)) 
                                                | (1U 
                                                   & ((8U 
                                                       & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__dir_r))
                                                       ? 
                                                      ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r) 
                                                       >> 3U)
                                                       : 
                                                      (((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r) 
                                                        >> 3U) 
                                                       & ((2U 
                                                           == 
                                                           (3U 
                                                            & (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r 
                                                               >> 6U))) 
                                                          | (3U 
                                                             == 
                                                             (3U 
                                                              & (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r 
                                                                 >> 6U)))))))) 
                                               << 3U)) 
                                           | ((4U & 
                                               (((4U 
                                                  & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__dir_r))
                                                  ? 
                                                 ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r) 
                                                  >> 2U)
                                                  : 
                                                 (((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r) 
                                                   >> 2U) 
                                                  & ((2U 
                                                      == 
                                                      (3U 
                                                       & (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r 
                                                          >> 4U))) 
                                                     | (3U 
                                                        == 
                                                        (3U 
                                                         & (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r 
                                                            >> 4U)))))) 
                                                << 2U)) 
                                              | ((2U 
                                                  & (((2U 
                                                       & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__dir_r))
                                                       ? 
                                                      ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r) 
                                                       >> 1U)
                                                       : 
                                                      (((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r) 
                                                        >> 1U) 
                                                       & ((2U 
                                                           == 
                                                           (3U 
                                                            & (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r 
                                                               >> 2U))) 
                                                          | (3U 
                                                             == 
                                                             (3U 
                                                              & (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r 
                                                                 >> 2U)))))) 
                                                     << 1U)) 
                                                 | (1U 
                                                    & ((1U 
                                                        & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__dir_r))
                                                        ? (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r)
                                                        : 
                                                       ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__areg_r) 
                                                        & ((2U 
                                                            == 
                                                            (3U 
                                                             & vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r)) 
                                                           | (3U 
                                                              == 
                                                              (3U 
                                                               & vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__adecl_r))))))))));
    vlSelfRef.milan_datapath__DOT__aprb_regs_w[0U] 
        = vlSelfRef.milan_datapath__DOT__aprb_parsed_w;
    vlSelfRef.milan_datapath__DOT__aprb_regs_w[1U] 
        = vlSelfRef.milan_datapath__DOT__aprb_matched_w;
    vlSelfRef.milan_datapath__DOT__aprb_regs_w[2U] 
        = (IData)(vlSelfRef.milan_datapath__DOT__aprb_sid_r);
    vlSelfRef.milan_datapath__DOT__aprb_regs_w[3U] 
        = (IData)((vlSelfRef.milan_datapath__DOT__aprb_sid_r 
                   >> 0x00000020U));
    vlSelfRef.milan_datapath__DOT__aprb_regs_w[4U] 
        = ((0x00ff0000U & (VL_COUNTONES_I((IData)(vlSelfRef.milan_datapath__DOT__strtbl_en_w)) 
                           << 0x00000010U)) | ((((IData)(vlSelfRef.milan_datapath__DOT__aprb_idx_r) 
                                                 << 9U) 
                                                | ((IData)(vlSelfRef.milan_datapath__DOT__aprb_hit_r) 
                                                   << 8U)) 
                                               | (IData)(vlSelfRef.milan_datapath__DOT__aprb_subtype_r)));
    vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__penq_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__avtprx_match) 
           & (((IData)(vlSelfRef.milan_datapath__DOT__strtbl_en_w) 
               >> (IData)(vlSelfRef.milan_datapath__DOT__avtprx_idx)) 
              & (2U != (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__pq_cnt_r))));
    vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_cap_hs 
        = (((0U == (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__st_r)) 
            | (1U == (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__st_r))) 
           & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_52));
    vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_frame_latch 
        = ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_52) 
           & ((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rxl_r) 
              & (0U == (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__st_r))));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_1[0U] = (IData)(
                                                           ((8U 
                                                             > (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__fv_idx_r))
                                                             ? 
                                                            ((vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__fv_r 
                                                              << 8U) 
                                                             | (QData)((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__byte_w)))
                                                             : vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__fv_r));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_1[1U] = (IData)(
                                                           (((8U 
                                                              > (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__fv_idx_r))
                                                              ? 
                                                             ((vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__fv_r 
                                                               << 8U) 
                                                              | (QData)((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__byte_w)))
                                                              : vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__fv_r) 
                                                            >> 0x00000020U));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_1[2U] = 0U;
    milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__req_w 
        = (((((((IData)(((~ ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__dir_r) 
                             >> 0x0000000eU)) & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__valid_r) 
                                                 >> 0x0000000eU))) 
                << 4U) | (((2U & (((~ ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__dir_r) 
                                       >> 0x0000000dU)) 
                                   << 1U) & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__valid_r) 
                                             >> 0x0000000cU))) 
                           | (1U & ((~ ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__dir_r) 
                                        >> 0x0000000cU)) 
                                    & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__valid_r) 
                                       >> 0x0000000cU)))) 
                          << 2U)) | ((2U & (((~ ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__dir_r) 
                                                 >> 0x0000000bU)) 
                                             << 1U) 
                                            & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__valid_r) 
                                               >> 0x0000000aU))) 
                                     | (1U & ((~ ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__dir_r) 
                                                  >> 0x0000000aU)) 
                                              & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__valid_r) 
                                                 >> 0x0000000aU))))) 
             << 4U) | ((((2U & (((~ ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__dir_r) 
                                     >> 9U)) << 1U) 
                                & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__valid_r) 
                                   >> 8U))) | (1U & 
                                               ((~ 
                                                 ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__dir_r) 
                                                  >> 8U)) 
                                                & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__valid_r) 
                                                   >> 8U)))) 
                        << 2U) | ((2U & (((~ ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__dir_r) 
                                              >> 7U)) 
                                          << 1U) & 
                                         ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__valid_r) 
                                          >> 6U))) 
                                  | (IData)(vlSelfRef.milan_datapath__DOT__lwsrp_talker_declared)))) 
           & ((- (IData)((1U & ((~ (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__registrar__DOT__boundary_r)) 
                                & vlSelfRef.milan_datapath__DOT__csr__DOT__lwsrp_ctrl)))) 
              & (((((((~ ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__dir_r) 
                          >> 0x0000000eU)) & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_48)) 
                     << 4U) | ((((~ ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__dir_r) 
                                     >> 0x0000000dU)) 
                                 & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_47)) 
                                << 3U) | (((~ ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__dir_r) 
                                               >> 0x0000000cU)) 
                                           & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_46)) 
                                          << 2U))) 
                   | ((((~ ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__dir_r) 
                            >> 0x0000000bU)) & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_45)) 
                       << 1U) | ((~ ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__dir_r) 
                                     >> 0x0000000aU)) 
                                 & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_44)))) 
                  << 4U) | (((((~ ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__dir_r) 
                                   >> 9U)) & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_43)) 
                              << 3U) | (((~ ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__dir_r) 
                                             >> 8U)) 
                                         & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_42)) 
                                        << 2U)) | (
                                                   (((~ 
                                                      ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__dir_r) 
                                                       >> 7U)) 
                                                     & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_41)) 
                                                    << 1U) 
                                                   | (IData)(vlSelfRef.milan_datapath__DOT__lwsrp_listener_ready))))));
    vlSelfRef.milan_datapath__DOT__listener_observed_w 
        = (1U & ((vlSelfRef.milan_datapath__DOT__csr__DOT__lwsrp_ctrl 
                  & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp_listener_ready)) 
                 | vlSelfRef.milan_datapath__DOT__csr__DOT__acmp_lobs));
    vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w 
        = (((QData)((IData)(((0x0000ff00U & (vlSelfRef.milan_datapath__DOT__csr__DOT__mac_alo 
                                             << 8U)) 
                             | (0x000000ffU & (vlSelfRef.milan_datapath__DOT__csr__DOT__mac_alo 
                                               >> 8U))))) 
            << 0x00000020U) | (QData)((IData)(((0xff000000U 
                                                & (vlSelfRef.milan_datapath__DOT__csr__DOT__mac_alo 
                                                   << 8U)) 
                                               | vlSelfRef.__VdfgRegularize_h6e95ff9d_0_77))));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_90 = ((IData)(Vmilan_datapath__ConstPool__TABLE_h9a1b00ed_0
                                                         [vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__queue_grant]) 
                                                 << 6U);
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_89 = ((IData)(Vmilan_datapath__ConstPool__TABLE_h9a1b00ed_0
                                                         [vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__queue_grant]) 
                                                 << 3U);
    vlSelfRef.milan_datapath__DOT__ctl2_tx_tlast = 
        ((IData)(vlSelfRef.milan_datapath__DOT__aecp_acmp_mux__DOT__gsel)
          ? ((2U == (IData)(vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__st_r)) 
             & (8U == (IData)(vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__beat_r)))
          : (IData)(vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__beat_last_r));
    vlSelfRef.milan_datapath__DOT__ctl2_tx_tvalid = 
        (((IData)(vlSelfRef.milan_datapath__DOT__aecp_acmp_mux__DOT__gsel)
           ? (2U == (IData)(vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__st_r))
           : (IData)(vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__beat_pend_r)) 
         & (IData)(vlSelfRef.milan_datapath__DOT__aecp_acmp_mux__DOT__active));
    vlSelfRef.milan_datapath__DOT__chan_tdm_render__DOT__u_fcdc__DOT__wptr_gray_n 
        = ((IData)(vlSelfRef.milan_datapath__DOT__chan_tdm_render__DOT__u_fcdc__DOT__wptr_bin_n) 
           ^ ((IData)(vlSelfRef.milan_datapath__DOT__chan_tdm_render__DOT__u_fcdc__DOT__wptr_bin_n) 
              >> 1U));
    vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__w_bscan_rl 
        = ((0U == (IData)(vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__w_brec_rl))
            ? (IData)(vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__brec_dlen_q)
            : (IData)(vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__w_brec_rl));
    vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__do_push 
        = ((IData)(vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__in_acc) 
           & ((~ (IData)(vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__tq_pushed)) 
              & ((IData)(vlSelfRef.s_axis_tx_tlast) 
                 | ((0x12U > (IData)(vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__byte_counter)) 
                    & (0x00000012U <= ((IData)(8U) 
                                       + (IData)(vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__byte_counter)))))));
    vlSelfRef.milan_datapath__DOT__adp_adv__DOT__rearm_fire_w 
        = (vlSelfRef.milan_datapath__DOT__csr__DOT__adp_ctrl 
           & ((IData)(vlSelfRef.milan_datapath__DOT__eff_link_w) 
              & ((IData)(vlSelfRef.milan_datapath__DOT__adp_tick_1s) 
                 & ((~ (IData)(vlSelfRef.milan_datapath__DOT__adp_adv__DOT__available_r)) 
                    & (1U <= (IData)(vlSelfRef.milan_datapath__DOT__adp_adv__DOT__rearm_tick_r))))));
    vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__st_raddr_w 
        = (0x0000ffffU & ((IData)(vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__w_wb_read)
                           ? ((IData)(vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__wb_addr_q) 
                              + (IData)(vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__wb_cnt_r))
                           : ((IData)(vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__w_soff) 
                              + (IData)(vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__seg_addr_q
                                        [vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__w_seg]))));
    vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__tmr_wr_idx_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__w_arm_wr)
            ? (IData)(vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__w_uid_idx)
            : (IData)(vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__swp_idx_r));
    vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__w_swp_run 
        = ((~ (IData)(vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__w_arm_wr)) 
           & (IData)(vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__swp_active_r));
    vlSelfRef.milan_datapath__DOT____Vcellinp__lwsrp__ctx_idx_i 
        = (0x0000000fU & ((IData)(vlSelfRef.milan_datapath__DOT__csr_srp_ctx_idx) 
                          | (- (IData)((IData)(vlSelfRef.milan_datapath__DOT__crf_srp_gnt_w)))));
    vlSelfRef.milan_datapath__DOT__srp_tk_row_w = ((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__srp_wr_pend_r) 
                                                   & ((~ (IData)(vlSelfRef.milan_datapath__DOT__csr_srp_ctx_dir)) 
                                                      & ((1U 
                                                          <= 
                                                          (0x0000001fU 
                                                           & ((IData)(vlSelfRef.milan_datapath__DOT__csr_srp_ctx_idx) 
                                                              - (IData)(7U)))) 
                                                         & (8U 
                                                            > 
                                                            (0x0000001fU 
                                                             & ((IData)(vlSelfRef.milan_datapath__DOT__csr_srp_ctx_idx) 
                                                                - (IData)(7U)))))));
    vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__fire 
        = ((IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__in_acc) 
           & ((0x38U <= (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__bytes_in)) 
              & ((0x01bfU >= (0x000001ffU & (((IData)(0x01bfU) 
                                              - ((IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__et_off) 
                                                 << 3U)) 
                                             - (IData)(7U)))) 
                 & ((0x22U == (0x000000ffU & (((0U 
                                                == 
                                                (0x0000001fU 
                                                 & (((IData)(0x01bfU) 
                                                     - 
                                                     ((IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__et_off) 
                                                      << 3U)) 
                                                    - (IData)(7U))))
                                                ? 0U
                                                : (vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__hdr
                                                   [
                                                   (((IData)(7U) 
                                                     + 
                                                     (0x000001ffU 
                                                      & (((IData)(0x01bfU) 
                                                          - 
                                                          ((IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__et_off) 
                                                           << 3U)) 
                                                         - (IData)(7U)))) 
                                                    >> 5U)] 
                                                   << 
                                                   ((IData)(0x00000020U) 
                                                    - 
                                                    (0x0000001fU 
                                                     & (((IData)(0x01bfU) 
                                                         - 
                                                         ((IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__et_off) 
                                                          << 3U)) 
                                                        - (IData)(7U)))))) 
                                              | (vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__hdr
                                                 [(0x0000000fU 
                                                   & ((((IData)(0x01bfU) 
                                                        - 
                                                        ((IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__et_off) 
                                                         << 3U)) 
                                                       - (IData)(7U)) 
                                                      >> 5U))] 
                                                 >> 
                                                 (0x0000001fU 
                                                  & (((IData)(0x01bfU) 
                                                      - 
                                                      ((IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__et_off) 
                                                       << 3U)) 
                                                     - (IData)(7U))))))) 
                    & ((0x01bfU >= (0x000001ffU & (
                                                   ((IData)(0x01bfU) 
                                                    - 
                                                    (0x000001f8U 
                                                     & (((IData)(1U) 
                                                         + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__et_off)) 
                                                        << 3U))) 
                                                   - (IData)(7U)))) 
                       & ((0xf0U == (0x000000ffU & 
                                     (((0U == (0x0000001fU 
                                               & (((IData)(0x01bfU) 
                                                   - 
                                                   (0x000001f8U 
                                                    & (((IData)(1U) 
                                                        + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__et_off)) 
                                                       << 3U))) 
                                                  - (IData)(7U))))
                                        ? 0U : (vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__hdr
                                                [(((IData)(7U) 
                                                   + 
                                                   (0x000001ffU 
                                                    & (((IData)(0x01bfU) 
                                                        - 
                                                        (0x000001f8U 
                                                         & (((IData)(1U) 
                                                             + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__et_off)) 
                                                            << 3U))) 
                                                       - (IData)(7U)))) 
                                                  >> 5U)] 
                                                << 
                                                ((IData)(0x00000020U) 
                                                 - 
                                                 (0x0000001fU 
                                                  & (((IData)(0x01bfU) 
                                                      - 
                                                      (0x000001f8U 
                                                       & (((IData)(1U) 
                                                           + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__et_off)) 
                                                          << 3U))) 
                                                     - (IData)(7U)))))) 
                                      | (vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__hdr
                                         [(0x0000000fU 
                                           & ((((IData)(0x01bfU) 
                                                - (0x000001f8U 
                                                   & (((IData)(1U) 
                                                       + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__et_off)) 
                                                      << 3U))) 
                                               - (IData)(7U)) 
                                              >> 5U))] 
                                         >> (0x0000001fU 
                                             & (((IData)(0x01bfU) 
                                                 - 
                                                 (0x000001f8U 
                                                  & (((IData)(1U) 
                                                      + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__et_off)) 
                                                     << 3U))) 
                                                - (IData)(7U))))))) 
                          & ((7U >= (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__subtype)) 
                             & ((~ (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__parsed)) 
                                & ((vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__hdr
                                    [(((IData)(7U) 
                                       + (0x000001ffU 
                                          & (((IData)(0x01bfU) 
                                              - (0x000001f8U 
                                                 & (((IData)(3U) 
                                                     + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__et_off)) 
                                                    << 3U))) 
                                             - (IData)(7U)))) 
                                      >> 5U)] >> (0x0000001fU 
                                                  & ((IData)(7U) 
                                                     + 
                                                     (0x000001ffU 
                                                      & (((IData)(0x01bfU) 
                                                          - 
                                                          (0x000001f8U 
                                                           & (((IData)(3U) 
                                                               + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__et_off)) 
                                                              << 3U))) 
                                                         - (IData)(7U)))))) 
                                   & (0x01bfU >= (0x000001ffU 
                                                  & (((IData)(0x01bfU) 
                                                      - 
                                                      (0x000001f8U 
                                                       & (((IData)(3U) 
                                                           + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__et_off)) 
                                                          << 3U))) 
                                                     - (IData)(7U)))))))))))));
    vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__match_hit = 0U;
    if (((IData)(vlSelfRef.milan_datapath__DOT__strtbl_en_w) 
         & ((((QData)((IData)(vlSelfRef.milan_datapath__DOT__strtbl_sid_w[1U])) 
              << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__strtbl_sid_w[0U]))) 
            == vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__sid))) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__match_hit = 1U;
    }
    if ((((IData)(vlSelfRef.milan_datapath__DOT__strtbl_en_w) 
          >> 1U) & ((((QData)((IData)(vlSelfRef.milan_datapath__DOT__strtbl_sid_w[3U])) 
                      << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__strtbl_sid_w[2U]))) 
                    == vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__sid))) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__match_hit = 1U;
    }
    if ((((IData)(vlSelfRef.milan_datapath__DOT__strtbl_en_w) 
          >> 2U) & ((((QData)((IData)(vlSelfRef.milan_datapath__DOT__strtbl_sid_w[5U])) 
                      << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__strtbl_sid_w[4U]))) 
                    == vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__sid))) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__match_hit = 1U;
    }
    if ((((IData)(vlSelfRef.milan_datapath__DOT__strtbl_en_w) 
          >> 3U) & ((((QData)((IData)(vlSelfRef.milan_datapath__DOT__strtbl_sid_w[7U])) 
                      << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__strtbl_sid_w[6U]))) 
                    == vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__sid))) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__match_hit = 1U;
    }
    if ((((IData)(vlSelfRef.milan_datapath__DOT__strtbl_en_w) 
          >> 4U) & ((((QData)((IData)(vlSelfRef.milan_datapath__DOT__strtbl_sid_w[9U])) 
                      << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__strtbl_sid_w[8U]))) 
                    == vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__sid))) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__match_hit = 1U;
    }
    if ((((IData)(vlSelfRef.milan_datapath__DOT__strtbl_en_w) 
          >> 5U) & ((((QData)((IData)(vlSelfRef.milan_datapath__DOT__strtbl_sid_w[11U])) 
                      << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__strtbl_sid_w[10U]))) 
                    == vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__sid))) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__match_hit = 1U;
    }
    if ((((IData)(vlSelfRef.milan_datapath__DOT__strtbl_en_w) 
          >> 6U) & ((((QData)((IData)(vlSelfRef.milan_datapath__DOT__strtbl_sid_w[13U])) 
                      << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__strtbl_sid_w[12U]))) 
                    == vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__sid))) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__match_hit = 1U;
    }
    vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__match_idx = 0U;
    if (((IData)(vlSelfRef.milan_datapath__DOT__strtbl_en_w) 
         & ((((QData)((IData)(vlSelfRef.milan_datapath__DOT__strtbl_sid_w[1U])) 
              << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__strtbl_sid_w[0U]))) 
            == vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__sid))) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__match_idx = 0U;
    }
    if ((((IData)(vlSelfRef.milan_datapath__DOT__strtbl_en_w) 
          >> 1U) & ((((QData)((IData)(vlSelfRef.milan_datapath__DOT__strtbl_sid_w[3U])) 
                      << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__strtbl_sid_w[2U]))) 
                    == vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__sid))) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__match_idx = 1U;
    }
    if ((((IData)(vlSelfRef.milan_datapath__DOT__strtbl_en_w) 
          >> 2U) & ((((QData)((IData)(vlSelfRef.milan_datapath__DOT__strtbl_sid_w[5U])) 
                      << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__strtbl_sid_w[4U]))) 
                    == vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__sid))) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__match_idx = 2U;
    }
    if ((((IData)(vlSelfRef.milan_datapath__DOT__strtbl_en_w) 
          >> 3U) & ((((QData)((IData)(vlSelfRef.milan_datapath__DOT__strtbl_sid_w[7U])) 
                      << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__strtbl_sid_w[6U]))) 
                    == vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__sid))) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__match_idx = 3U;
    }
    if ((((IData)(vlSelfRef.milan_datapath__DOT__strtbl_en_w) 
          >> 4U) & ((((QData)((IData)(vlSelfRef.milan_datapath__DOT__strtbl_sid_w[9U])) 
                      << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__strtbl_sid_w[8U]))) 
                    == vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__sid))) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__match_idx = 4U;
    }
    if ((((IData)(vlSelfRef.milan_datapath__DOT__strtbl_en_w) 
          >> 5U) & ((((QData)((IData)(vlSelfRef.milan_datapath__DOT__strtbl_sid_w[11U])) 
                      << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__strtbl_sid_w[10U]))) 
                    == vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__sid))) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__match_idx = 5U;
    }
    if ((((IData)(vlSelfRef.milan_datapath__DOT__strtbl_en_w) 
          >> 6U) & ((((QData)((IData)(vlSelfRef.milan_datapath__DOT__strtbl_sid_w[13U])) 
                      << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__strtbl_sid_w[12U]))) 
                    == vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__sid))) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__match_idx = 6U;
    }
    if ((((IData)(vlSelfRef.milan_datapath__DOT__strtbl_en_w) 
          >> 7U) & ((((QData)((IData)(vlSelfRef.milan_datapath__DOT__strtbl_sid_w[15U])) 
                      << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__strtbl_sid_w[14U]))) 
                    == vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__sid))) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__match_hit = 1U;
        vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__match_idx = 7U;
    }
    vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__w_smap_rows 
        = ((0x000fU == (0x0000ffffU & (IData)((vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__cw0_r 
                                               >> 0x00000020U))))
            ? vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__AEM_SMAP_OUT_ROWS_C
           [vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__w_smap_pi_out]
            : vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__AEM_SMAP_IN_ROWS_C
           [vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__w_smap_pi_in]);
    vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ram_we_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__eng_we_w) 
           | (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ext_wr_ok_w));
    vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__ingress__DOT__fw_user 
        = vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__ingress__DOT__kind_r;
    if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__ingress__DOT__hold_v_r) 
                  & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__ingress__DOT__hold_l_r))))) {
        if (((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__ingress__DOT__rxv_r) 
             & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__ingress__DOT__hold_v_r))) {
            if ((1U == (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__ingress__DOT__beat_idx_r))) {
                vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__ingress__DOT__fw_user 
                    = vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__ingress__DOT__match_mvrp_w;
            }
        }
    }
    vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__ingress__DOT__match_w 
        = ((((0x00000180c200000eULL == vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__ingress__DOT__hold_dst_w) 
             & (0x22eaU == (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__ingress__DOT__et_w))) 
            | (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__ingress__DOT__match_mvrp_w)) 
           & vlSelfRef.milan_datapath__DOT__csr__DOT__lwsrp_ctrl);
    vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__mux_queues__DOT__store_axis_int_to_output = 0U;
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
    vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__mux_queues__DOT__store_axis_temp_to_output = 0U;
    if ((1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__mux_queues__DOT__m_axis_tready_int_reg)))) {
        if ((0U != ((IData)(vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__dm_tready) 
                    & (IData)(vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__mux_queues__DOT__m_axis_tvalid_reg)))) {
            vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__buffer_queues__DOT__mux_queues__DOT__store_axis_temp_to_output = 1U;
        }
    }
    vlSelfRef.milan_datapath__DOT__csr__DOT__win_alias_ctrl_w 
        = ((IData)(__VdfgRegularize_h6e95ff9d_0_81) 
           & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_21));
    vlSelfRef.milan_datapath__DOT__csr__DOT__srp_prov_w 
        = ((IData)(__VdfgRegularize_h6e95ff9d_0_81) 
           & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__srp_poll_w));
    if ((0x12U <= (IData)(vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__byte_counter))) {
        vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__hdr_eff[0U] 
            = vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__eth_header[0U];
        vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__hdr_eff[1U] 
            = vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__eth_header[1U];
        vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__hdr_eff[2U] 
            = vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__eth_header[2U];
        vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__hdr_eff[3U] 
            = vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__eth_header[3U];
        vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__hdr_eff[4U] 
            = vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__eth_header[4U];
        vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__hdr_eff[5U] 
            = vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__eth_header[5U];
    } else {
        vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__hdr_eff[0U] 
            = vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__hdr_shifted[0U];
        vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__hdr_eff[1U] 
            = vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__hdr_shifted[1U];
        vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__hdr_eff[2U] 
            = vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__hdr_shifted[2U];
        vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__hdr_eff[3U] 
            = vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__hdr_shifted[3U];
        vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__hdr_eff[4U] 
            = vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__hdr_shifted[4U];
        vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__hdr_eff[5U] 
            = vlSelfRef.milan_datapath__DOT__traffic_controller__DOT__classifier__DOT__hdr_shifted[5U];
    }
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
    milan_datapath__DOT__aecp_listener__DOT__u_val__DOT__w_type_ok 
        = ((0U == (0x0000000fU & (IData)((vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_ingress__DOT__w_out 
                                          >> 0x00000020U)))) 
           | (6U == (0x0000000fU & (IData)((vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_ingress__DOT__w_out 
                                            >> 0x00000020U)))));
    vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__lb_sel_w 
        = (vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r
           [(0x0000001fU & ((- (IData)((IData)(milan_datapath__DOT__chan_map_capture__DOT__lb_sel_ok_w))) 
                            & ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_10) 
                               + (0x0000001cU & ((vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r
                                                  [vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__slot_r] 
                                                  >> 8U) 
                                                 << 2U)))))] 
           & (- (QData)((IData)(milan_datapath__DOT__chan_map_capture__DOT__lb_sel_ok_w))));
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
    vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__p1_w 
        = (7U & (((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__pos_r)) 
                 & (- (IData)(((IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__c_eff_w) 
                               != (7U & ((IData)(1U) 
                                         + (IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__pos_r))))))));
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
    vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__lock_now_w 
        = ((~ (vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ram_q_r 
               >> 0x0000000cU)) & (IData)(milan_datapath__DOT__avtp_rx_monitor__DOT__lock_ok_w));
    vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__monst_next_w 
        = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ram_q_r;
    vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__monst_next_w 
        = ((0xffc03fffU & vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__monst_next_w) 
           | (0x003fc000U & (vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__cur_r[2U] 
                             << 4U)));
    vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__monst_next_w 
        = ((0xffffff00U & vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__monst_next_w) 
           | (0x000000ffU & (vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__cur_r[4U] 
                             >> 3U)));
    __Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__ms_locked__186__w 
        = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ram_q_r;
    milan_datapath__DOT__avtp_rx_monitor__DOT____VlemCall_4__ms_locked 
        = (1U & (__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__ms_locked__186__w 
                 >> 0x0cU));
    if (milan_datapath__DOT__avtp_rx_monitor__DOT____VlemCall_4__ms_locked) {
        vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__ms_settle__187__w 
            = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ram_q_r;
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT____VlemCall_5__ms_settle 
            = (0x0000000fU & (vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__ms_settle__187__w 
                              >> 8U));
        if ((0U != (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT____VlemCall_5__ms_settle))) {
            vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__ms_settle__188__w 
                = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ram_q_r;
            vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT____VlemCall_6__ms_settle 
                = (0x0000000fU & (vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__ms_settle__188__w 
                                  >> 8U));
            vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__monst_next_w 
                = ((0xfffff0ffU & vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__monst_next_w) 
                   | (0x00000f00U & (((IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT____VlemCall_6__ms_settle) 
                                      - (IData)(1U)) 
                                     << 8U)));
        }
    } else {
        if (milan_datapath__DOT__avtp_rx_monitor__DOT__lock_ok_w) {
            vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__monst_next_w 
                = (0x00001000U | vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__monst_next_w);
        }
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__monst_next_w 
            = (0x00000800U | (0xfffff0ffU & vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__monst_next_w));
    }
    vlSelfRef.milan_datapath__DOT__aaf_tx_tlast = (
                                                   (3U 
                                                    == (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__est_r)) 
                                                   & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_76));
    vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx0_tlast_w 
        = ((1U == (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__state_r)) 
           & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__beat_r) 
              == (0x0000000fU & (((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__is_full3_w)
                                   ? 0x0bU : 8U) - (IData)(1U)))));
    if (vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__eng_we_w) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ram_wdata_w 
            = milan_datapath__DOT__avtp_rx_monitor__DOT__eng_wdata_w;
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ram_waddr_w 
            = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__eng_waddr_w;
    } else {
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ram_wdata_w 
            = vlSelfRef.milan_datapath__DOT__csr__DOT__lctx_wr_data_r;
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ram_waddr_w 
            = vlSelfRef.milan_datapath__DOT__csr__DOT__lctx_wr_addr_r;
    }
    vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__stg_space_w 
        = (7U & (((IData)(4U) - (IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__stg_cnt_r)) 
                 + (1U & (- (IData)((IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__stg_drain_w))))));
    vlSelfRef.m_axis_pcm_tlast = ((8U >= (IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__remain_r)) 
                                  & (IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__emit_w));
    vlSelfRef.milan_datapath__DOT__rend_pcm_tvalid_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__emit_w) 
           & ((IData)(vlSelfRef.milan_datapath__DOT__pcm_route__DOT__render_active_o) 
              & ((IData)(vlSelfRef.milan_datapath__DOT__route_render_sel_w) 
                 == (IData)(vlSelfRef.m_axis_pcm_tuser))));
    vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__match_any = 0U;
    if ((0x00008000U & (IData)(milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__hit))) {
        vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__match_any = 1U;
    }
    if ((0x00004000U & (IData)(milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__hit))) {
        vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__match_any = 1U;
    }
    if ((0x00002000U & (IData)(milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__hit))) {
        vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__match_any = 1U;
    }
    if ((0x00001000U & (IData)(milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__hit))) {
        vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__match_any = 1U;
    }
    if ((0x00000800U & (IData)(milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__hit))) {
        vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__match_any = 1U;
    }
    if ((0x00000400U & (IData)(milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__hit))) {
        vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__match_any = 1U;
    }
    if ((0x00000200U & (IData)(milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__hit))) {
        vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__match_any = 1U;
    }
    if ((0x00000100U & (IData)(milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__hit))) {
        vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__match_any = 1U;
    }
    if ((0x00000080U & (IData)(milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__hit))) {
        vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__match_any = 1U;
    }
    if ((0x00000040U & (IData)(milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__hit))) {
        vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__match_any = 1U;
    }
    if ((0x00000020U & (IData)(milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__hit))) {
        vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__match_any = 1U;
    }
    if ((0x00000010U & (IData)(milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__hit))) {
        vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__match_any = 1U;
    }
    if ((8U & (IData)(milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__hit))) {
        vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__match_any = 1U;
    }
    if ((4U & (IData)(milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__hit))) {
        vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__match_any = 1U;
    }
    if ((2U & (IData)(milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__hit))) {
        vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__match_any = 1U;
    }
    vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__match_act = 0U;
    if ((0x00008000U & (IData)(milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__hit))) {
        vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__match_act 
            = vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_action[15U];
    }
    if ((0x00004000U & (IData)(milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__hit))) {
        vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__match_act 
            = vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_action[14U];
    }
    if ((0x00002000U & (IData)(milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__hit))) {
        vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__match_act 
            = vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_action[13U];
    }
    if ((0x00001000U & (IData)(milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__hit))) {
        vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__match_act 
            = vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_action[12U];
    }
    if ((0x00000800U & (IData)(milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__hit))) {
        vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__match_act 
            = vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_action[11U];
    }
    if ((0x00000400U & (IData)(milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__hit))) {
        vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__match_act 
            = vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_action[10U];
    }
    if ((0x00000200U & (IData)(milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__hit))) {
        vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__match_act 
            = vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_action[9U];
    }
    if ((0x00000100U & (IData)(milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__hit))) {
        vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__match_act 
            = vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_action[8U];
    }
    if ((0x00000080U & (IData)(milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__hit))) {
        vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__match_act 
            = vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_action[7U];
    }
    if ((0x00000040U & (IData)(milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__hit))) {
        vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__match_act 
            = vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_action[6U];
    }
    if ((0x00000020U & (IData)(milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__hit))) {
        vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__match_act 
            = vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_action[5U];
    }
    if ((0x00000010U & (IData)(milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__hit))) {
        vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__match_act 
            = vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_action[4U];
    }
    if ((8U & (IData)(milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__hit))) {
        vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__match_act 
            = vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_action[3U];
    }
    if ((4U & (IData)(milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__hit))) {
        vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__match_act 
            = vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_action[2U];
    }
    if ((2U & (IData)(milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__hit))) {
        vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__match_act 
            = vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_action[1U];
    }
    if ((1U & (IData)(milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__hit))) {
        vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__match_any = 1U;
        vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__match_act 
            = vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_action[0U];
    }
    vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_set_w = 0U;
    milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_frame_w[0U] 
        = vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r[0U];
    milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_frame_w[1U] 
        = vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r[1U];
    milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_frame_w[2U] 
        = vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r[2U];
    milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_frame_w[3U] 
        = vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r[3U];
    milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_frame_w[4U] 
        = vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r[4U];
    milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_frame_w[5U] 
        = vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r[5U];
    milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_frame_w[6U] 
        = vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r[6U];
    milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_frame_w[7U] 
        = vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r[7U];
    milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_frame_w[8U] 
        = vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r[8U];
    milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_frame_w[9U] 
        = vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r[9U];
    milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_frame_en_w = 0U;
    if (((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_lstn_hit) 
         & (9U > (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_luid_r)))) {
        if ((6U == (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_msg_r))) {
            if (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_sm_en) {
                if ((1U & (~ (((0U != (7U & (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r[9U] 
                                             >> 0x0000001aU))) 
                               & (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_same_talker)) 
                              & (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_flags_match))))) {
                    vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_set_w = 1U;
                    milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_frame_w[0U] 
                        = (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_ctlr_r);
                    milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_frame_w[1U] 
                        = (IData)((vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_ctlr_r 
                                   >> 0x00000020U));
                    milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_frame_w[2U] 
                        = (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_talker_r);
                    milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_frame_w[3U] 
                        = (IData)((vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_talker_r 
                                   >> 0x00000020U));
                    milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_frame_w[8U] 
                        = ((0xf0000fffU & milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_frame_w[8U]) 
                           | ((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_tuid_r) 
                              << 0x0000000cU));
                    if ((0U == (7U & (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r[9U] 
                                      >> 0x0000001aU)))) {
                        milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_frame_w[7U] 
                            = ((0x0fffffffU & milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_frame_w[7U]) 
                               | ((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_flags_r) 
                                  << 0x0000001cU));
                        milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_frame_w[8U] 
                            = ((0xfffff000U & milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_frame_w[8U]) 
                               | ((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_flags_r) 
                                  >> 4U));
                        milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_frame_w[9U] 
                            = (0x1fc1ffffU & milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_frame_w[9U]);
                    } else {
                        milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_frame_w[7U] 
                            = ((0x0fffffffU & milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_frame_w[7U]) 
                               | (((0xfff7U & ((vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r[8U] 
                                                << 4U) 
                                               | (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r[7U] 
                                                  >> 0x0000001cU))) 
                                   | (8U & (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_flags_r))) 
                                  << 0x0000001cU));
                        milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_frame_w[8U] 
                            = ((0xfffff000U & milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_frame_w[8U]) 
                               | (((0xfff7U & ((vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r[8U] 
                                                << 4U) 
                                               | (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r[7U] 
                                                  >> 0x0000001cU))) 
                                   | (8U & (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_flags_r))) 
                                  >> 4U));
                    }
                    milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_frame_w[9U] 
                        = (0x00800000U | (0x1f3fffffU 
                                          & milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_frame_w[9U]));
                    milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_frame_w[4U] 
                        = (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_bind_sid);
                    milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_frame_w[5U] 
                        = (IData)((vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_bind_sid 
                                   >> 0x00000020U));
                    if (((6U == (7U & (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r[9U] 
                                       >> 0x0000001aU))) 
                         | (7U == (7U & (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r[9U] 
                                         >> 0x0000001aU))))) {
                        milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_frame_w[9U] 
                            = (0x1dffffffU & milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_frame_w[9U]);
                    }
                    milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_frame_w[8U] 
                        = (0x0fffffffU & milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_frame_w[8U]);
                    milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_frame_w[9U] 
                        = (0x1ffffc00U & milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_frame_w[9U]);
                    milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_frame_w[9U] 
                        = (0x0c000000U | (0x03ffffffU 
                                          & milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_frame_w[9U]));
                    milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_frame_en_w = 1U;
                }
            } else {
                VL_ASSIGN_W(317, milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_frame_w, Vmilan_datapath__ConstPool__CONST_h8a04c6be_0);
                milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_frame_w[9U] 
                    = (0x18000000U | (0x03ffffffU & milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_frame_w[9U]));
                milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_frame_w[0U] 
                    = (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_ctlr_r);
                milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_frame_w[1U] 
                    = (IData)((vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_ctlr_r 
                               >> 0x00000020U));
                milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_frame_w[2U] 
                    = (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_talker_r);
                milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_frame_w[3U] 
                    = (IData)((vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_talker_r 
                               >> 0x00000020U));
                milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_frame_w[7U] 
                    = ((0x0fffffffU & milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_frame_w[7U]) 
                       | ((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_flags_r) 
                          << 0x0000001cU));
                milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_frame_w[8U] 
                    = ((0xf0000000U & milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_frame_w[8U]) 
                       | ((0x0ffff000U & ((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_tuid_r) 
                                          << 0x0000000cU)) 
                          | ((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_flags_r) 
                             >> 4U)));
                milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_frame_w[4U] 
                    = (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_bind_sid);
                milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_frame_w[5U] 
                    = (IData)((vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_bind_sid 
                               >> 0x00000020U));
                milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_frame_w[6U] 
                    = (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_dmac_r);
                milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_frame_w[7U] 
                    = ((0xffff0000U & milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_frame_w[7U]) 
                       | (IData)((vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_dmac_r 
                                  >> 0x00000020U)));
                milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_frame_en_w = 1U;
            }
        } else if ((8U == (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_msg_r))) {
            VL_ASSIGN_W(317, milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_frame_w, Vmilan_datapath__ConstPool__CONST_h8a04c6be_0);
            if (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_sm_en) {
                milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_frame_w[9U] 
                    = ((0x1effffffU & milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_frame_w[9U]) 
                       | (0x01000000U & vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r[9U]));
                milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_frame_w[9U] 
                    = ((0x1ffe03ffU & milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_frame_w[9U]) 
                       | (0x0001fc00U & vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r[9U]));
            }
            milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_frame_en_w = 1U;
        }
    } else if (milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_probe_resp) {
        if ((0U == (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_status_r))) {
            milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_frame_w[4U] 
                = (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_sid_r);
            milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_frame_w[5U] 
                = (IData)((vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_sid_r 
                           >> 0x00000020U));
            milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_frame_w[6U] 
                = (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_dmac_r);
            milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_frame_w[7U] 
                = ((0xf0000000U & milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_frame_w[7U]) 
                   | (((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_vlan_r) 
                       << 0x00000010U) | (IData)((vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_dmac_r 
                                                  >> 0x00000020U))));
            milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_frame_w[9U] 
                = (0x02000000U | milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_frame_w[9U]);
            milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_frame_w[9U] 
                = (0x00c00000U | (0x1f01ffffU & milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_frame_w[9U]));
            milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_frame_w[8U] 
                = (0x0fffffffU & milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_frame_w[8U]);
            milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_frame_w[9U] 
                = (0x00000271U | (0x1ffffc00U & milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_frame_w[9U]));
            milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_frame_w[9U] 
                = (0x18000000U | (0x03ffffffU & milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_frame_w[9U]));
        } else {
            milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_frame_w[9U] 
                = ((0x1fc1ffffU & milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_frame_w[9U]) 
                   | (0x1fffffffU & ((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cap_status_r) 
                                     << 0x00000011U)));
            milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_frame_w[8U] 
                = (0x0fffffffU & milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_frame_w[8U]);
            milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_frame_w[9U] 
                = (0x000000faU | (0x1ffffc00U & milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_frame_w[9U]));
            milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_frame_w[9U] 
                = (0x14000000U | (0x03ffffffU & milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_frame_w[9U]));
        }
        milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_frame_en_w = 1U;
    }
    vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__eff_chans_w 
        = ((0U == (IData)(milan_datapath__DOT__chan_map_render__DOT__chans_raw_w))
            ? 2U : (IData)(milan_datapath__DOT__chan_map_render__DOT__chans_raw_w));
    vlSelfRef.m_axis_pcm_tvalid = ((IData)(vlSelfRef.milan_datapath__DOT__pcm_route__DOT__cur_route_w) 
                                   & (IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__emit_w));
    vlSelfRef.milan_datapath__DOT__dpkt_pcm_tready_w 
        = (1U & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pcm_route__DOT__cur_route_w)) 
                 | (IData)(vlSelfRef.m_axis_pcm_tready)));
    vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__pdisp_new_w 
        = ((0U == (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__mst_r)) 
           & ((0U == (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__pq_cnt_r)) 
              & (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__penq_w)));
    vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ext_rd_go_w 
        = ((0U == (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__mst_r)) 
           & ((0U == (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__pq_cnt_r)) 
              & ((((~ (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rds_dir_r)) 
                   & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rds_busy_r)) 
                  | (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_80)) 
                 & ((~ (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__penq_w)) 
                    & ((0U == (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__bind_pend_r)) 
                       & ((0U == (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__sil_pend_r)) 
                          & ((~ ((IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__depkt_any_w) 
                                 | (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__mreset_any_w))) 
                             & (0U == (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__servo_pend_r)))))))));
    vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_swp_run 
        = ((~ ((1U == (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__st_r)) 
               | (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_frame_latch))) 
           & (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__swp_active_r));
    vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_rest_ok 
        = ((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__init_done_r) 
           & ((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_rest_pend) 
              & ((~ ((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_frame_latch) 
                     | ((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__swp_active_r) 
                        | ((1U == (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__st_r)) 
                           | (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_launch_ok))))) 
                 & (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_rest_sm_ok))));
    __Vtemp_13[0U] = (IData)((((QData)((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__view0_r[5U])) 
                               << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__view0_r[4U]))));
    __Vtemp_13[1U] = (IData)(((((QData)((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__view0_r[5U])) 
                                << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__view0_r[4U]))) 
                              >> 0x00000020U));
    __Vtemp_13[2U] = 0U;
    VL_SUB_W(3, __Vtemp_14, __Vtemp_13, vlSelfRef.__VdfgRegularize_h6e95ff9d_0_1);
    vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__lsid_sub_w[0U] 
        = __Vtemp_14[0U];
    vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__lsid_sub_w[1U] 
        = __Vtemp_14[1U];
    vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__lsid_sub_w[2U] 
        = (1U & __Vtemp_14[2U]);
    __Vtemp_16[0U] = (IData)((((QData)((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__sid_r[1U])) 
                               << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__sid_r[0U]))));
    __Vtemp_16[1U] = (IData)(((((QData)((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__sid_r[1U])) 
                                << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__sid_r[0U]))) 
                              >> 0x00000020U));
    __Vtemp_16[2U] = 0U;
    VL_SUB_W(3, __Vtemp_17, __Vtemp_16, vlSelfRef.__VdfgRegularize_h6e95ff9d_0_1);
    milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__0__KET____DOT__esub_w[0U] 
        = __Vtemp_17[0U];
    milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__0__KET____DOT__esub_w[1U] 
        = __Vtemp_17[1U];
    milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__0__KET____DOT__esub_w[2U] 
        = (1U & __Vtemp_17[2U]);
    __Vtemp_19[0U] = (IData)((((QData)((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__sid_r[3U])) 
                               << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__sid_r[2U]))));
    __Vtemp_19[1U] = (IData)(((((QData)((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__sid_r[3U])) 
                                << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__sid_r[2U]))) 
                              >> 0x00000020U));
    __Vtemp_19[2U] = 0U;
    VL_SUB_W(3, __Vtemp_20, __Vtemp_19, vlSelfRef.__VdfgRegularize_h6e95ff9d_0_1);
    milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__1__KET____DOT__esub_w[0U] 
        = __Vtemp_20[0U];
    milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__1__KET____DOT__esub_w[1U] 
        = __Vtemp_20[1U];
    milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__1__KET____DOT__esub_w[2U] 
        = (1U & __Vtemp_20[2U]);
    __Vtemp_22[0U] = (IData)((((QData)((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__sid_r[5U])) 
                               << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__sid_r[4U]))));
    __Vtemp_22[1U] = (IData)(((((QData)((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__sid_r[5U])) 
                                << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__sid_r[4U]))) 
                              >> 0x00000020U));
    __Vtemp_22[2U] = 0U;
    VL_SUB_W(3, __Vtemp_23, __Vtemp_22, vlSelfRef.__VdfgRegularize_h6e95ff9d_0_1);
    milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__2__KET____DOT__esub_w[0U] 
        = __Vtemp_23[0U];
    milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__2__KET____DOT__esub_w[1U] 
        = __Vtemp_23[1U];
    milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__2__KET____DOT__esub_w[2U] 
        = (1U & __Vtemp_23[2U]);
    __Vtemp_25[0U] = (IData)((((QData)((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__sid_r[7U])) 
                               << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__sid_r[6U]))));
    __Vtemp_25[1U] = (IData)(((((QData)((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__sid_r[7U])) 
                                << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__sid_r[6U]))) 
                              >> 0x00000020U));
    __Vtemp_25[2U] = 0U;
    VL_SUB_W(3, __Vtemp_26, __Vtemp_25, vlSelfRef.__VdfgRegularize_h6e95ff9d_0_1);
    milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__3__KET____DOT__esub_w[0U] 
        = __Vtemp_26[0U];
    milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__3__KET____DOT__esub_w[1U] 
        = __Vtemp_26[1U];
    milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__3__KET____DOT__esub_w[2U] 
        = (1U & __Vtemp_26[2U]);
    __Vtemp_28[0U] = (IData)((((QData)((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__sid_r[9U])) 
                               << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__sid_r[8U]))));
    __Vtemp_28[1U] = (IData)(((((QData)((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__sid_r[9U])) 
                                << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__sid_r[8U]))) 
                              >> 0x00000020U));
    __Vtemp_28[2U] = 0U;
    VL_SUB_W(3, __Vtemp_29, __Vtemp_28, vlSelfRef.__VdfgRegularize_h6e95ff9d_0_1);
    milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__4__KET____DOT__esub_w[0U] 
        = __Vtemp_29[0U];
    milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__4__KET____DOT__esub_w[1U] 
        = __Vtemp_29[1U];
    milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__4__KET____DOT__esub_w[2U] 
        = (1U & __Vtemp_29[2U]);
    __Vtemp_31[0U] = (IData)((((QData)((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__sid_r[11U])) 
                               << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__sid_r[10U]))));
    __Vtemp_31[1U] = (IData)(((((QData)((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__sid_r[11U])) 
                                << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__sid_r[10U]))) 
                              >> 0x00000020U));
    __Vtemp_31[2U] = 0U;
    VL_SUB_W(3, __Vtemp_32, __Vtemp_31, vlSelfRef.__VdfgRegularize_h6e95ff9d_0_1);
    milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__5__KET____DOT__esub_w[0U] 
        = __Vtemp_32[0U];
    milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__5__KET____DOT__esub_w[1U] 
        = __Vtemp_32[1U];
    milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__5__KET____DOT__esub_w[2U] 
        = (1U & __Vtemp_32[2U]);
    __Vtemp_34[0U] = (IData)((((QData)((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__sid_r[13U])) 
                               << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__sid_r[12U]))));
    __Vtemp_34[1U] = (IData)(((((QData)((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__sid_r[13U])) 
                                << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__sid_r[12U]))) 
                              >> 0x00000020U));
    __Vtemp_34[2U] = 0U;
    VL_SUB_W(3, __Vtemp_35, __Vtemp_34, vlSelfRef.__VdfgRegularize_h6e95ff9d_0_1);
    milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__6__KET____DOT__esub_w[0U] 
        = __Vtemp_35[0U];
    milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__6__KET____DOT__esub_w[1U] 
        = __Vtemp_35[1U];
    milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__6__KET____DOT__esub_w[2U] 
        = (1U & __Vtemp_35[2U]);
    __Vtemp_37[0U] = (IData)((((QData)((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__sid_r[15U])) 
                               << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__sid_r[14U]))));
    __Vtemp_37[1U] = (IData)(((((QData)((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__sid_r[15U])) 
                                << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__sid_r[14U]))) 
                              >> 0x00000020U));
    __Vtemp_37[2U] = 0U;
    VL_SUB_W(3, __Vtemp_38, __Vtemp_37, vlSelfRef.__VdfgRegularize_h6e95ff9d_0_1);
    milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__7__KET____DOT__esub_w[0U] 
        = __Vtemp_38[0U];
    milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__7__KET____DOT__esub_w[1U] 
        = __Vtemp_38[1U];
    milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__7__KET____DOT__esub_w[2U] 
        = (1U & __Vtemp_38[2U]);
    __Vtemp_40[0U] = (IData)((((QData)((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__sid_r[17U])) 
                               << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__sid_r[16U]))));
    __Vtemp_40[1U] = (IData)(((((QData)((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__sid_r[17U])) 
                                << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__sid_r[16U]))) 
                              >> 0x00000020U));
    __Vtemp_40[2U] = 0U;
    VL_SUB_W(3, __Vtemp_41, __Vtemp_40, vlSelfRef.__VdfgRegularize_h6e95ff9d_0_1);
    milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__8__KET____DOT__esub_w[0U] 
        = __Vtemp_41[0U];
    milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__8__KET____DOT__esub_w[1U] 
        = __Vtemp_41[1U];
    milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__8__KET____DOT__esub_w[2U] 
        = (1U & __Vtemp_41[2U]);
    __Vtemp_43[0U] = (IData)((((QData)((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__sid_r[19U])) 
                               << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__sid_r[18U]))));
    __Vtemp_43[1U] = (IData)(((((QData)((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__sid_r[19U])) 
                                << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__sid_r[18U]))) 
                              >> 0x00000020U));
    __Vtemp_43[2U] = 0U;
    VL_SUB_W(3, __Vtemp_44, __Vtemp_43, vlSelfRef.__VdfgRegularize_h6e95ff9d_0_1);
    milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__9__KET____DOT__esub_w[0U] 
        = __Vtemp_44[0U];
    milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__9__KET____DOT__esub_w[1U] 
        = __Vtemp_44[1U];
    milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__9__KET____DOT__esub_w[2U] 
        = (1U & __Vtemp_44[2U]);
    __Vtemp_46[0U] = (IData)((((QData)((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__sid_r[21U])) 
                               << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__sid_r[20U]))));
    __Vtemp_46[1U] = (IData)(((((QData)((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__sid_r[21U])) 
                                << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__sid_r[20U]))) 
                              >> 0x00000020U));
    __Vtemp_46[2U] = 0U;
    VL_SUB_W(3, __Vtemp_47, __Vtemp_46, vlSelfRef.__VdfgRegularize_h6e95ff9d_0_1);
    milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__10__KET____DOT__esub_w[0U] 
        = __Vtemp_47[0U];
    milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__10__KET____DOT__esub_w[1U] 
        = __Vtemp_47[1U];
    milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__10__KET____DOT__esub_w[2U] 
        = (1U & __Vtemp_47[2U]);
    __Vtemp_49[0U] = (IData)((((QData)((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__sid_r[23U])) 
                               << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__sid_r[22U]))));
    __Vtemp_49[1U] = (IData)(((((QData)((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__sid_r[23U])) 
                                << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__sid_r[22U]))) 
                              >> 0x00000020U));
    __Vtemp_49[2U] = 0U;
    VL_SUB_W(3, __Vtemp_50, __Vtemp_49, vlSelfRef.__VdfgRegularize_h6e95ff9d_0_1);
    milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__11__KET____DOT__esub_w[0U] 
        = __Vtemp_50[0U];
    milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__11__KET____DOT__esub_w[1U] 
        = __Vtemp_50[1U];
    milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__11__KET____DOT__esub_w[2U] 
        = (1U & __Vtemp_50[2U]);
    __Vtemp_52[0U] = (IData)((((QData)((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__sid_r[25U])) 
                               << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__sid_r[24U]))));
    __Vtemp_52[1U] = (IData)(((((QData)((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__sid_r[25U])) 
                                << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__sid_r[24U]))) 
                              >> 0x00000020U));
    __Vtemp_52[2U] = 0U;
    VL_SUB_W(3, __Vtemp_53, __Vtemp_52, vlSelfRef.__VdfgRegularize_h6e95ff9d_0_1);
    milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__12__KET____DOT__esub_w[0U] 
        = __Vtemp_53[0U];
    milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__12__KET____DOT__esub_w[1U] 
        = __Vtemp_53[1U];
    milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__12__KET____DOT__esub_w[2U] 
        = (1U & __Vtemp_53[2U]);
    __Vtemp_55[0U] = (IData)((((QData)((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__sid_r[27U])) 
                               << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__sid_r[26U]))));
    __Vtemp_55[1U] = (IData)(((((QData)((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__sid_r[27U])) 
                                << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__sid_r[26U]))) 
                              >> 0x00000020U));
    __Vtemp_55[2U] = 0U;
    VL_SUB_W(3, __Vtemp_56, __Vtemp_55, vlSelfRef.__VdfgRegularize_h6e95ff9d_0_1);
    milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__13__KET____DOT__esub_w[0U] 
        = __Vtemp_56[0U];
    milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__13__KET____DOT__esub_w[1U] 
        = __Vtemp_56[1U];
    milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__13__KET____DOT__esub_w[2U] 
        = (1U & __Vtemp_56[2U]);
    __Vtemp_58[0U] = (IData)((((QData)((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__sid_r[29U])) 
                               << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__sid_r[28U]))));
    __Vtemp_58[1U] = (IData)(((((QData)((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__sid_r[29U])) 
                                << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__sid_r[28U]))) 
                              >> 0x00000020U));
    __Vtemp_58[2U] = 0U;
    VL_SUB_W(3, __Vtemp_59, __Vtemp_58, vlSelfRef.__VdfgRegularize_h6e95ff9d_0_1);
    milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__14__KET____DOT__esub_w[0U] 
        = __Vtemp_59[0U];
    milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__14__KET____DOT__esub_w[1U] 
        = __Vtemp_59[1U];
    milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__14__KET____DOT__esub_w[2U] 
        = (1U & __Vtemp_59[2U]);
    __VdfgRegularize_h6e95ff9d_0_88 = ((8U >= (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__aidx_r)) 
                                       & ((IData)(milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__req_w) 
                                          >> (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__aidx_r)));
    vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__active_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__grant_r) 
           & (IData)(milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__req_w));
    vlSelfRef.milan_datapath__DOT____Vcellinp__csr__i_tlk_lobs_v 
        = (((((2U & ((vlSelfRef.milan_datapath__DOT__csr__DOT__acmp_lobs 
                      | (((IData)(vlSelfRef.milan_datapath__DOT__lwsrp_stream_gate) 
                          >> 7U) & vlSelfRef.milan_datapath__DOT__csr__DOT__lwsrp_ctrl)) 
                     << 1U)) | (1U & (vlSelfRef.milan_datapath__DOT__csr__DOT__acmp_lobs 
                                      | (((IData)(vlSelfRef.milan_datapath__DOT__lwsrp_stream_gate) 
                                          >> 6U) & vlSelfRef.milan_datapath__DOT__csr__DOT__lwsrp_ctrl)))) 
             << 6U) | (((2U & ((vlSelfRef.milan_datapath__DOT__csr__DOT__acmp_lobs 
                                | (((IData)(vlSelfRef.milan_datapath__DOT__lwsrp_stream_gate) 
                                    >> 5U) & vlSelfRef.milan_datapath__DOT__csr__DOT__lwsrp_ctrl)) 
                               << 1U)) | (1U & (vlSelfRef.milan_datapath__DOT__csr__DOT__acmp_lobs 
                                                | (((IData)(vlSelfRef.milan_datapath__DOT__lwsrp_stream_gate) 
                                                    >> 4U) 
                                                   & vlSelfRef.milan_datapath__DOT__csr__DOT__lwsrp_ctrl)))) 
                       << 4U)) | ((((2U & ((vlSelfRef.milan_datapath__DOT__csr__DOT__acmp_lobs 
                                            | (((IData)(vlSelfRef.milan_datapath__DOT__lwsrp_stream_gate) 
                                                >> 3U) 
                                               & vlSelfRef.milan_datapath__DOT__csr__DOT__lwsrp_ctrl)) 
                                           << 1U)) 
                                    | (1U & (vlSelfRef.milan_datapath__DOT__csr__DOT__acmp_lobs 
                                             | (((IData)(vlSelfRef.milan_datapath__DOT__lwsrp_stream_gate) 
                                                 >> 2U) 
                                                & vlSelfRef.milan_datapath__DOT__csr__DOT__lwsrp_ctrl)))) 
                                   << 2U) | ((2U & 
                                              ((vlSelfRef.milan_datapath__DOT__csr__DOT__acmp_lobs 
                                                | (((IData)(vlSelfRef.milan_datapath__DOT__lwsrp_stream_gate) 
                                                    >> 1U) 
                                                   & vlSelfRef.milan_datapath__DOT__csr__DOT__lwsrp_ctrl)) 
                                               << 1U)) 
                                             | (IData)(vlSelfRef.milan_datapath__DOT__listener_observed_w))));
    __Vtemp_61[0U] = (IData)((vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w 
                              << 0x00000010U));
    __Vtemp_61[1U] = (IData)(((vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w 
                               << 0x00000010U) >> 0x00000020U));
    __Vtemp_61[2U] = 0U;
    VL_SUB_W(3, __Vtemp_62, __Vtemp_61, vlSelfRef.__VdfgRegularize_h6e95ff9d_0_1);
    vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__sid_sub_w[0U] 
        = __Vtemp_62[0U];
    vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__sid_sub_w[1U] 
        = __Vtemp_62[1U];
    vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__sid_sub_w[2U] 
        = (1U & __Vtemp_62[2U]);
    vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__byte_w = 0U;
    if ((8U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__sec_r))) {
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__byte_w = 0U;
    } else if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__sec_r))) {
        if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__sec_r))) {
            vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__byte_w = 0U;
        } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__sec_r))) {
            if ((0x00000010U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__off_r))) {
                vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__byte_w 
                    = ((((0x0eU >= (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__row_r)) 
                         && (1U & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__ready_q_r) 
                                   >> (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__row_r))))
                         ? 2U : 1U) << 6U);
            } else if ((8U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__off_r))) {
                if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__off_r))) {
                    vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__byte_w 
                        = ((((0x0eU >= (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__row_r)) 
                             && (1U & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__ready_q_r) 
                                       >> (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__row_r))))
                             ? 2U : 1U) << 6U);
                } else if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__off_r))) {
                    if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__off_r))) {
                        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__byte_w 
                            = ((((0x0eU >= (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__row_r)) 
                                 && (1U & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__ready_q_r) 
                                           >> (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__row_r))))
                                 ? 2U : 1U) << 6U);
                    } else {
                        vlSelfRef.__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__row_evt__33__row 
                            = vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__row_r;
                        vlSelfRef.__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__row_evt__33__Vfuncout 
                            = ((((0x0eU >= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__row_evt__33__row)) 
                                 && (1U & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__row_lv_w) 
                                           >> (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__row_evt__33__row)))) 
                                | ((0x0eU >= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__row_evt__33__row)) 
                                   && (1U & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctxtx_lv_w) 
                                             >> (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__row_evt__33__row)))))
                                ? 0xb4U : (((0x0eU 
                                             >= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__row_evt__33__row)) 
                                            && (1U 
                                                & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctxtx_fresh_w) 
                                                   >> (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__row_evt__33__row))))
                                            ? 0U : 0x24U));
                        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__byte_w 
                            = vlSelfRef.__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__row_evt__33__Vfuncout;
                    }
                } else {
                    vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__byte_w 
                        = ((0x03bfU >= (0x000003ffU 
                                        & (((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__row_r) 
                                            << 6U) 
                                           + (((IData)(9U) 
                                               - (0x0000000fU 
                                                  & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__off_r))) 
                                              << 3U))))
                            ? (0x000000ffU & (((0U 
                                                == 
                                                (0x0000001fU 
                                                 & (((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__row_r) 
                                                     << 6U) 
                                                    + 
                                                    (((IData)(9U) 
                                                      - 
                                                      (0x0000000fU 
                                                       & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__off_r))) 
                                                     << 3U))))
                                                ? 0U
                                                : (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__sid_r
                                                   [
                                                   (((IData)(7U) 
                                                     + 
                                                     (0x000003ffU 
                                                      & (((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__row_r) 
                                                          << 6U) 
                                                         + 
                                                         (((IData)(9U) 
                                                           - 
                                                           (0x0000000fU 
                                                            & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__off_r))) 
                                                          << 3U)))) 
                                                    >> 5U)] 
                                                   << 
                                                   ((IData)(0x00000020U) 
                                                    - 
                                                    (0x0000001fU 
                                                     & (((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__row_r) 
                                                         << 6U) 
                                                        + 
                                                        (((IData)(9U) 
                                                          - 
                                                          (0x0000000fU 
                                                           & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__off_r))) 
                                                         << 3U)))))) 
                                              | (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__sid_r
                                                 [(0x0000001fU 
                                                   & ((((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__row_r) 
                                                        << 6U) 
                                                       + 
                                                       (((IData)(9U) 
                                                         - 
                                                         (0x0000000fU 
                                                          & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__off_r))) 
                                                        << 3U)) 
                                                      >> 5U))] 
                                                 >> 
                                                 (0x0000001fU 
                                                  & (((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__row_r) 
                                                      << 6U) 
                                                     + 
                                                     (((IData)(9U) 
                                                       - 
                                                       (0x0000000fU 
                                                        & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__off_r))) 
                                                      << 3U))))))
                            : 0U);
                }
            } else {
                vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__byte_w 
                    = (0x000000ffU & ((4U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__off_r))
                                       ? ((0x03bfU 
                                           >= (0x000003ffU 
                                               & (((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__row_r) 
                                                   << 6U) 
                                                  + 
                                                  (((IData)(9U) 
                                                    - 
                                                    (0x0000000fU 
                                                     & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__off_r))) 
                                                   << 3U))))
                                           ? (((0U 
                                                == 
                                                (0x0000001fU 
                                                 & (((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__row_r) 
                                                     << 6U) 
                                                    + 
                                                    (((IData)(9U) 
                                                      - 
                                                      (0x0000000fU 
                                                       & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__off_r))) 
                                                     << 3U))))
                                                ? 0U
                                                : (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__sid_r
                                                   [
                                                   (((IData)(7U) 
                                                     + 
                                                     (0x000003ffU 
                                                      & (((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__row_r) 
                                                          << 6U) 
                                                         + 
                                                         (((IData)(9U) 
                                                           - 
                                                           (0x0000000fU 
                                                            & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__off_r))) 
                                                          << 3U)))) 
                                                    >> 5U)] 
                                                   << 
                                                   ((IData)(0x00000020U) 
                                                    - 
                                                    (0x0000001fU 
                                                     & (((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__row_r) 
                                                         << 6U) 
                                                        + 
                                                        (((IData)(9U) 
                                                          - 
                                                          (0x0000000fU 
                                                           & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__off_r))) 
                                                         << 3U)))))) 
                                              | (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__sid_r
                                                 [(0x0000001fU 
                                                   & ((((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__row_r) 
                                                        << 6U) 
                                                       + 
                                                       (((IData)(9U) 
                                                         - 
                                                         (0x0000000fU 
                                                          & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__off_r))) 
                                                        << 3U)) 
                                                      >> 5U))] 
                                                 >> 
                                                 (0x0000001fU 
                                                  & (((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__row_r) 
                                                      << 6U) 
                                                     + 
                                                     (((IData)(9U) 
                                                       - 
                                                       (0x0000000fU 
                                                        & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__off_r))) 
                                                      << 3U)))))
                                           : 0U) : 
                                      ((2U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__off_r))
                                        ? ((0x03bfU 
                                            >= (0x000003ffU 
                                                & (((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__row_r) 
                                                    << 6U) 
                                                   + 
                                                   (((IData)(9U) 
                                                     - 
                                                     (0x0000000fU 
                                                      & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__off_r))) 
                                                    << 3U))))
                                            ? (((0U 
                                                 == 
                                                 (0x0000001fU 
                                                  & (((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__row_r) 
                                                      << 6U) 
                                                     + 
                                                     (((IData)(9U) 
                                                       - 
                                                       (0x0000000fU 
                                                        & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__off_r))) 
                                                      << 3U))))
                                                 ? 0U
                                                 : 
                                                (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__sid_r
                                                 [(
                                                   ((IData)(7U) 
                                                    + 
                                                    (0x000003ffU 
                                                     & (((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__row_r) 
                                                         << 6U) 
                                                        + 
                                                        (((IData)(9U) 
                                                          - 
                                                          (0x0000000fU 
                                                           & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__off_r))) 
                                                         << 3U)))) 
                                                   >> 5U)] 
                                                 << 
                                                 ((IData)(0x00000020U) 
                                                  - 
                                                  (0x0000001fU 
                                                   & (((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__row_r) 
                                                       << 6U) 
                                                      + 
                                                      (((IData)(9U) 
                                                        - 
                                                        (0x0000000fU 
                                                         & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__off_r))) 
                                                       << 3U)))))) 
                                               | (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__sid_r
                                                  [
                                                  (0x0000001fU 
                                                   & ((((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__row_r) 
                                                        << 6U) 
                                                       + 
                                                       (((IData)(9U) 
                                                         - 
                                                         (0x0000000fU 
                                                          & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__off_r))) 
                                                        << 3U)) 
                                                      >> 5U))] 
                                                  >> 
                                                  (0x0000001fU 
                                                   & (((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__row_r) 
                                                       << 6U) 
                                                      + 
                                                      (((IData)(9U) 
                                                        - 
                                                        (0x0000000fU 
                                                         & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__off_r))) 
                                                       << 3U)))))
                                            : 0U) : 
                                       ((1U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__off_r))
                                         ? 1U : 0U))));
            }
        } else {
            vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__unnamedblk3__DOT__listlen 
                = (0x0000ffffU & ((IData)(2U) + ((IData)(0x000cU) 
                                                 * (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__nl_r))));
            vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__byte_w 
                = ((0U == (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__off_r))
                    ? 3U : ((1U == (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__off_r))
                             ? 8U : (0x000000ffU & 
                                     ((2U == (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__off_r))
                                       ? ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__unnamedblk3__DOT__listlen) 
                                          >> 8U) : (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__unnamedblk3__DOT__listlen)))));
        }
    } else if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__sec_r))) {
        if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__sec_r))) {
            vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__byte_w = 0U;
        } else if ((0x00000010U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__off_r))) {
            if ((8U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__off_r))) {
                if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__off_r))) {
                    vlSelfRef.__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__row_evt__34__row 
                        = vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__row_r;
                    vlSelfRef.__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__row_evt__34__Vfuncout 
                        = ((((0x0eU >= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__row_evt__34__row)) 
                             && (1U & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__row_lv_w) 
                                       >> (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__row_evt__34__row)))) 
                            | ((0x0eU >= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__row_evt__34__row)) 
                               && (1U & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctxtx_lv_w) 
                                         >> (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__row_evt__34__row)))))
                            ? 0xb4U : (((0x0eU >= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__row_evt__34__row)) 
                                        && (1U & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctxtx_fresh_w) 
                                                  >> (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__row_evt__34__row))))
                                        ? 0U : 0x24U));
                    vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__byte_w 
                        = vlSelfRef.__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__row_evt__34__Vfuncout;
                } else if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__off_r))) {
                    if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__off_r))) {
                        vlSelfRef.__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__row_evt__35__row 
                            = vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__row_r;
                        vlSelfRef.__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__row_evt__35__Vfuncout 
                            = ((((0x0eU >= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__row_evt__35__row)) 
                                 && (1U & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__row_lv_w) 
                                           >> (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__row_evt__35__row)))) 
                                | ((0x0eU >= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__row_evt__35__row)) 
                                   && (1U & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctxtx_lv_w) 
                                             >> (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__row_evt__35__row)))))
                                ? 0xb4U : (((0x0eU 
                                             >= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__row_evt__35__row)) 
                                            && (1U 
                                                & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctxtx_fresh_w) 
                                                   >> (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__row_evt__35__row))))
                                            ? 0U : 0x24U));
                        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__byte_w 
                            = vlSelfRef.__Vfunc_milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__row_evt__35__Vfuncout;
                    } else {
                        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__byte_w 
                            = (0x000000ffU & vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__rec_q_r[0U]);
                    }
                } else {
                    vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__byte_w 
                        = (0x000000ffU & ((1U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__off_r))
                                           ? ((vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__rec_q_r[0U] 
                                               << 0x00000018U) 
                                              | (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__rec_q_r[0U] 
                                                 >> 8U))
                                           : ((vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__rec_q_r[0U] 
                                               << 0x00000010U) 
                                              | (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__rec_q_r[0U] 
                                                 >> 0x00000010U))));
                }
            } else {
                vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__byte_w 
                    = (0x000000ffU & ((4U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__off_r))
                                       ? ((2U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__off_r))
                                           ? ((1U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__off_r))
                                               ? ((vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__rec_q_r[0U] 
                                                   << 8U) 
                                                  | (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__rec_q_r[0U] 
                                                     >> 0x00000018U))
                                               : vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__rec_q_r[2U])
                                           : ((1U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__off_r))
                                               ? vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__rec_q_r[1U]
                                               : ((vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__rec_q_r[1U] 
                                                   << 0x00000018U) 
                                                  | (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__rec_q_r[1U] 
                                                     >> 8U))))
                                       : ((2U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__off_r))
                                           ? ((1U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__off_r))
                                               ? ((vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__rec_q_r[1U] 
                                                   << 0x00000010U) 
                                                  | (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__rec_q_r[1U] 
                                                     >> 0x00000010U))
                                               : ((vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__rec_q_r[1U] 
                                                   << 8U) 
                                                  | (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__rec_q_r[1U] 
                                                     >> 0x00000018U)))
                                           : ((1U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__off_r))
                                               ? vlSelfRef.milan_datapath__DOT__csr__DOT__lwsrp_vid
                                               : (0x0000000fU 
                                                  & (vlSelfRef.milan_datapath__DOT__csr__DOT__lwsrp_vid 
                                                     >> 8U))))));
            }
        } else {
            vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__byte_w 
                = (0x000000ffU & ((8U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__off_r))
                                   ? ((4U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__off_r))
                                       ? ((2U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__off_r))
                                           ? ((1U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__off_r))
                                               ? ((vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__rec_q_r[2U] 
                                                   << 0x00000018U) 
                                                  | (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__rec_q_r[2U] 
                                                     >> 8U))
                                               : ((vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__rec_q_r[2U] 
                                                   << 0x00000010U) 
                                                  | (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__rec_q_r[2U] 
                                                     >> 0x00000010U)))
                                           : ((1U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__off_r))
                                               ? ((vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__rec_q_r[2U] 
                                                   << 8U) 
                                                  | (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__rec_q_r[2U] 
                                                     >> 0x00000018U))
                                               : vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__rec_q_r[3U]))
                                       : ((2U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__off_r))
                                           ? ((1U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__off_r))
                                               ? ((vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__rec_q_r[3U] 
                                                   << 0x00000018U) 
                                                  | (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__rec_q_r[3U] 
                                                     >> 8U))
                                               : ((vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__rec_q_r[3U] 
                                                   << 0x00000010U) 
                                                  | (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__rec_q_r[3U] 
                                                     >> 0x00000010U)))
                                           : ((0x03bfU 
                                               >= (0x000003ffU 
                                                   & (((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__row_r) 
                                                       << 6U) 
                                                      + 
                                                      (((IData)(9U) 
                                                        - 
                                                        (0x0000000fU 
                                                         & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__off_r))) 
                                                       << 3U))))
                                               ? ((
                                                   (0U 
                                                    == 
                                                    (0x0000001fU 
                                                     & (((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__row_r) 
                                                         << 6U) 
                                                        + 
                                                        (((IData)(9U) 
                                                          - 
                                                          (0x0000000fU 
                                                           & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__off_r))) 
                                                         << 3U))))
                                                    ? 0U
                                                    : 
                                                   (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__sid_r
                                                    [
                                                    (((IData)(7U) 
                                                      + 
                                                      (0x000003ffU 
                                                       & (((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__row_r) 
                                                           << 6U) 
                                                          + 
                                                          (((IData)(9U) 
                                                            - 
                                                            (0x0000000fU 
                                                             & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__off_r))) 
                                                           << 3U)))) 
                                                     >> 5U)] 
                                                    << 
                                                    ((IData)(0x00000020U) 
                                                     - 
                                                     (0x0000001fU 
                                                      & (((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__row_r) 
                                                          << 6U) 
                                                         + 
                                                         (((IData)(9U) 
                                                           - 
                                                           (0x0000000fU 
                                                            & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__off_r))) 
                                                          << 3U)))))) 
                                                  | (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__sid_r
                                                     [
                                                     (0x0000001fU 
                                                      & ((((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__row_r) 
                                                           << 6U) 
                                                          + 
                                                          (((IData)(9U) 
                                                            - 
                                                            (0x0000000fU 
                                                             & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__off_r))) 
                                                           << 3U)) 
                                                         >> 5U))] 
                                                     >> 
                                                     (0x0000001fU 
                                                      & (((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__row_r) 
                                                          << 6U) 
                                                         + 
                                                         (((IData)(9U) 
                                                           - 
                                                           (0x0000000fU 
                                                            & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__off_r))) 
                                                          << 3U)))))
                                               : 0U)))
                                   : ((4U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__off_r))
                                       ? ((0x03bfU 
                                           >= (0x000003ffU 
                                               & (((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__row_r) 
                                                   << 6U) 
                                                  + 
                                                  (((IData)(9U) 
                                                    - 
                                                    (0x0000000fU 
                                                     & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__off_r))) 
                                                   << 3U))))
                                           ? (((0U 
                                                == 
                                                (0x0000001fU 
                                                 & (((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__row_r) 
                                                     << 6U) 
                                                    + 
                                                    (((IData)(9U) 
                                                      - 
                                                      (0x0000000fU 
                                                       & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__off_r))) 
                                                     << 3U))))
                                                ? 0U
                                                : (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__sid_r
                                                   [
                                                   (((IData)(7U) 
                                                     + 
                                                     (0x000003ffU 
                                                      & (((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__row_r) 
                                                          << 6U) 
                                                         + 
                                                         (((IData)(9U) 
                                                           - 
                                                           (0x0000000fU 
                                                            & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__off_r))) 
                                                          << 3U)))) 
                                                    >> 5U)] 
                                                   << 
                                                   ((IData)(0x00000020U) 
                                                    - 
                                                    (0x0000001fU 
                                                     & (((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__row_r) 
                                                         << 6U) 
                                                        + 
                                                        (((IData)(9U) 
                                                          - 
                                                          (0x0000000fU 
                                                           & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__off_r))) 
                                                         << 3U)))))) 
                                              | (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__sid_r
                                                 [(0x0000001fU 
                                                   & ((((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__row_r) 
                                                        << 6U) 
                                                       + 
                                                       (((IData)(9U) 
                                                         - 
                                                         (0x0000000fU 
                                                          & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__off_r))) 
                                                        << 3U)) 
                                                      >> 5U))] 
                                                 >> 
                                                 (0x0000001fU 
                                                  & (((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__row_r) 
                                                      << 6U) 
                                                     + 
                                                     (((IData)(9U) 
                                                       - 
                                                       (0x0000000fU 
                                                        & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__off_r))) 
                                                      << 3U)))))
                                           : 0U) : 
                                      ((2U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__off_r))
                                        ? ((0x03bfU 
                                            >= (0x000003ffU 
                                                & (((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__row_r) 
                                                    << 6U) 
                                                   + 
                                                   (((IData)(9U) 
                                                     - 
                                                     (0x0000000fU 
                                                      & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__off_r))) 
                                                    << 3U))))
                                            ? (((0U 
                                                 == 
                                                 (0x0000001fU 
                                                  & (((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__row_r) 
                                                      << 6U) 
                                                     + 
                                                     (((IData)(9U) 
                                                       - 
                                                       (0x0000000fU 
                                                        & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__off_r))) 
                                                      << 3U))))
                                                 ? 0U
                                                 : 
                                                (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__sid_r
                                                 [(
                                                   ((IData)(7U) 
                                                    + 
                                                    (0x000003ffU 
                                                     & (((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__row_r) 
                                                         << 6U) 
                                                        + 
                                                        (((IData)(9U) 
                                                          - 
                                                          (0x0000000fU 
                                                           & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__off_r))) 
                                                         << 3U)))) 
                                                   >> 5U)] 
                                                 << 
                                                 ((IData)(0x00000020U) 
                                                  - 
                                                  (0x0000001fU 
                                                   & (((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__row_r) 
                                                       << 6U) 
                                                      + 
                                                      (((IData)(9U) 
                                                        - 
                                                        (0x0000000fU 
                                                         & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__off_r))) 
                                                       << 3U)))))) 
                                               | (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__sid_r
                                                  [
                                                  (0x0000001fU 
                                                   & ((((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__row_r) 
                                                        << 6U) 
                                                       + 
                                                       (((IData)(9U) 
                                                         - 
                                                         (0x0000000fU 
                                                          & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__off_r))) 
                                                        << 3U)) 
                                                      >> 5U))] 
                                                  >> 
                                                  (0x0000001fU 
                                                   & (((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__row_r) 
                                                       << 6U) 
                                                      + 
                                                      (((IData)(9U) 
                                                        - 
                                                        (0x0000000fU 
                                                         & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__off_r))) 
                                                       << 3U)))))
                                            : 0U) : 
                                       ((1U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__off_r))
                                         ? 1U : 0U)))));
        }
    } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__sec_r))) {
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__unnamedblk3__DOT__listlen 
            = (0x0000ffffU & ((IData)(2U) + ((IData)(0x001cU) 
                                             * (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__nt_r))));
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__byte_w 
            = ((0U == (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__off_r))
                ? 1U : ((1U == (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__off_r))
                         ? 0x00000019U : (0x000000ffU 
                                          & ((2U == (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__off_r))
                                              ? ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__unnamedblk3__DOT__listlen) 
                                                 >> 8U)
                                              : (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__unnamedblk3__DOT__listlen)))));
    } else {
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__byte_w 
            = ((0x00000010U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__off_r))
                ? 0U : (0x000000ffU & ((8U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__off_r))
                                        ? ((4U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__off_r))
                                            ? ((2U 
                                                & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__off_r))
                                                ? 0U
                                                : (
                                                   (1U 
                                                    & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__off_r))
                                                    ? 0xeaU
                                                    : 0x22U))
                                            : ((2U 
                                                & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__off_r))
                                                ? (
                                                   (1U 
                                                    & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__off_r))
                                                    ? (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w)
                                                    : (IData)(
                                                              (vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w 
                                                               >> 8U)))
                                                : (
                                                   (1U 
                                                    & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__off_r))
                                                    ? (IData)(
                                                              (vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w 
                                                               >> 0x10U))
                                                    : (IData)(
                                                              (vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w 
                                                               >> 0x18U)))))
                                        : ((4U & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__off_r))
                                            ? ((2U 
                                                & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__off_r))
                                                ? (
                                                   (1U 
                                                    & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__off_r))
                                                    ? (IData)(
                                                              (vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w 
                                                               >> 0x20U))
                                                    : (IData)(
                                                              (vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w 
                                                               >> 0x28U)))
                                                : (
                                                   (1U 
                                                    & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__off_r))
                                                    ? 0x0eU
                                                    : 0U))
                                            : ((2U 
                                                & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__off_r))
                                                ? (
                                                   (1U 
                                                    & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__off_r))
                                                    ? 0U
                                                    : 0xc2U)
                                                : (
                                                   (1U 
                                                    & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__off_r))
                                                    ? 0x80U
                                                    : 1U))))));
    }
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__150__b 
        = vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat_r;
    for (int __Vi0 = 0; __Vi0 < 64; ++__Vi0) {
        __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__150__f[__Vi0] = 0;
    }
    __Vilp1 = 0U;
    while ((__Vilp1 <= 0x0000003fU)) {
        __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__150__f[__Vilp1] = 0U;
        __Vilp1 = ((IData)(1U) + __Vilp1);
    }
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__150__f[0U] = 0x91U;
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__150__f[1U] = 0xe0U;
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__150__f[2U] = 0xf0U;
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__150__f[3U] = 0U;
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__150__f[4U] = 0xffU;
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__150__f[5U] = 0U;
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__150__f[6U] 
        = (0x000000ffU & (IData)((vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w 
                                  >> 0x00000028U)));
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__150__f[7U] 
        = (0x000000ffU & (IData)((vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w 
                                  >> 0x00000020U)));
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__150__f[8U] 
        = (0x000000ffU & (IData)((vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w 
                                  >> 0x00000018U)));
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__150__f[9U] 
        = (0x000000ffU & (IData)((vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w 
                                  >> 0x00000010U)));
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__150__f[10U] 
        = (0x000000ffU & (IData)((vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w 
                                  >> 8U)));
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__150__f[11U] 
        = (0x000000ffU & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w));
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__150__f[12U] = 0x22U;
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__150__f[13U] = 0xf0U;
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__150__f[14U] = 0xfeU;
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__150__f[15U] 
        = vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_msg_r;
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__150__f[16U] = 8U;
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__150__f[17U] = 0x1cU;
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__150__f[26U] = 0x91U;
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__150__f[27U] = 0xe0U;
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__150__f[28U] = 0xf0U;
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__150__f[29U] = 0U;
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__150__f[30U] 
        = (0x000000ffU & ((IData)(vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__offset_r) 
                          >> 8U));
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__150__f[31U] 
        = (0x000000ffU & (IData)(vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__offset_r));
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__150__f[32U] = 0U;
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__150__f[33U] 
        = (0x000000ffU & (vlSelfRef.milan_datapath__DOT__csr__DOT__maap_ctrl 
                          >> 8U));
    if ((2U == (IData)(vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_msg_r))) {
        __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__150__f[34U] = 0x91U;
        __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__150__f[35U] = 0xe0U;
        __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__150__f[36U] = 0xf0U;
        __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__150__f[37U] = 0U;
        __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__150__f[38U] 
            = (0x000000ffU & ((IData)(vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_conf_start_r) 
                              >> 8U));
        __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__150__f[39U] 
            = (0x000000ffU & (IData)(vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_conf_start_r));
        __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__150__f[40U] 
            = (0x000000ffU & ((IData)(vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_conf_cnt_r) 
                              >> 8U));
        __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__150__f[41U] 
            = (0x000000ffU & (IData)(vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_conf_cnt_r));
    }
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__150__Vfuncout 
        = (((QData)((IData)((((((IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__150__f
                                        [(7U | ((IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__150__b) 
                                                << 3U))]) 
                                << 8U) | __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__150__f
                               [(6U | ((IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__150__b) 
                                       << 3U))]) << 0x00000010U) 
                             | (((IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__150__f
                                         [(5U | ((IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__150__b) 
                                                 << 3U))]) 
                                 << 8U) | __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__150__f
                                [(4U | ((IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__150__b) 
                                        << 3U))])))) 
            << 0x00000020U) | (QData)((IData)((((((IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__150__f
                                                          [
                                                          (3U 
                                                           | ((IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__150__b) 
                                                              << 3U))]) 
                                                  << 8U) 
                                                 | __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__150__f
                                                 [(2U 
                                                   | ((IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__150__b) 
                                                      << 3U))]) 
                                                << 0x00000010U) 
                                               | (((IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__150__f
                                                           [
                                                           (1U 
                                                            | ((IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__150__b) 
                                                               << 3U))]) 
                                                   << 8U) 
                                                  | __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__150__f
                                                  [
                                                  ((IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__150__b) 
                                                   << 3U)])))));
    vlSelfRef.milan_datapath__DOT__maap_tx_tdata = __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__150__Vfuncout;
    milan_datapath__DOT__adp_adv__DOT__unnamedblk1__DOT__k = 0U;
    while (VL_GTS_III(32, 0x00000058U, milan_datapath__DOT__adp_adv__DOT__unnamedblk1__DOT__k)) {
        if (VL_LIKELY(((0x57U >= (0x0000007fU & milan_datapath__DOT__adp_adv__DOT__unnamedblk1__DOT__k))))) {
            vlSelfRef.milan_datapath__DOT__adp_adv__DOT__fb[(0x0000007fU 
                                                             & milan_datapath__DOT__adp_adv__DOT__unnamedblk1__DOT__k)] = 0U;
        }
        milan_datapath__DOT__adp_adv__DOT__unnamedblk1__DOT__k 
            = ((IData)(1U) + milan_datapath__DOT__adp_adv__DOT__unnamedblk1__DOT__k);
    }
    vlSelfRef.milan_datapath__DOT__adp_adv__DOT__fb[0U] = 0x91U;
    vlSelfRef.milan_datapath__DOT__adp_adv__DOT__fb[1U] = 0xe0U;
    vlSelfRef.milan_datapath__DOT__adp_adv__DOT__fb[2U] = 0xf0U;
    vlSelfRef.milan_datapath__DOT__adp_adv__DOT__fb[3U] = 1U;
    vlSelfRef.milan_datapath__DOT__adp_adv__DOT__fb[4U] = 0U;
    vlSelfRef.milan_datapath__DOT__adp_adv__DOT__fb[5U] = 0U;
    vlSelfRef.milan_datapath__DOT__adp_adv__DOT__fb[6U] 
        = (0x000000ffU & (IData)((vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w 
                                  >> 0x28U)));
    vlSelfRef.milan_datapath__DOT__adp_adv__DOT__fb[7U] 
        = (0x000000ffU & (IData)((vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w 
                                  >> 0x20U)));
    vlSelfRef.milan_datapath__DOT__adp_adv__DOT__fb[8U] 
        = (0x000000ffU & (IData)((vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w 
                                  >> 0x18U)));
    vlSelfRef.milan_datapath__DOT__adp_adv__DOT__fb[9U] 
        = (0x000000ffU & (IData)((vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w 
                                  >> 0x10U)));
    vlSelfRef.milan_datapath__DOT__adp_adv__DOT__fb[10U] 
        = (0x000000ffU & (IData)((vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w 
                                  >> 8U)));
    vlSelfRef.milan_datapath__DOT__adp_adv__DOT__fb[11U] 
        = (0x000000ffU & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w));
    vlSelfRef.milan_datapath__DOT__adp_adv__DOT__fb[12U] = 0x22U;
    vlSelfRef.milan_datapath__DOT__adp_adv__DOT__fb[13U] = 0xf0U;
    vlSelfRef.milan_datapath__DOT__adp_adv__DOT__fb[14U] = 0xfaU;
    vlSelfRef.milan_datapath__DOT__adp_adv__DOT__fb[15U] 
        = vlSelfRef.milan_datapath__DOT__adp_adv__DOT__tx_msg_r;
    vlSelfRef.milan_datapath__DOT__adp_adv__DOT__fb[16U] 
        = (0x000000f8U & (vlSelfRef.milan_datapath__DOT__csr__DOT__adp_ctrl 
                          >> 5U));
    vlSelfRef.milan_datapath__DOT__adp_adv__DOT__fb[17U] = 0x38U;
    vlSelfRef.milan_datapath__DOT__adp_adv__DOT__fb[18U] 
        = (0x000000ffU & (IData)((vlSelfRef.milan_datapath__DOT__cfg_adp_entity_id 
                                  >> 0x38U)));
    vlSelfRef.milan_datapath__DOT__adp_adv__DOT__fb[19U] 
        = (0x000000ffU & (IData)((vlSelfRef.milan_datapath__DOT__cfg_adp_entity_id 
                                  >> 0x30U)));
    vlSelfRef.milan_datapath__DOT__adp_adv__DOT__fb[20U] 
        = (0x000000ffU & (IData)((vlSelfRef.milan_datapath__DOT__cfg_adp_entity_id 
                                  >> 0x28U)));
    vlSelfRef.milan_datapath__DOT__adp_adv__DOT__fb[21U] 
        = (0x000000ffU & (IData)((vlSelfRef.milan_datapath__DOT__cfg_adp_entity_id 
                                  >> 0x20U)));
    vlSelfRef.milan_datapath__DOT__adp_adv__DOT__fb[22U] 
        = (0x000000ffU & (IData)((vlSelfRef.milan_datapath__DOT__cfg_adp_entity_id 
                                  >> 0x18U)));
    vlSelfRef.milan_datapath__DOT__adp_adv__DOT__fb[23U] 
        = (0x000000ffU & (IData)((vlSelfRef.milan_datapath__DOT__cfg_adp_entity_id 
                                  >> 0x10U)));
    vlSelfRef.milan_datapath__DOT__adp_adv__DOT__fb[24U] 
        = (0x000000ffU & (IData)((vlSelfRef.milan_datapath__DOT__cfg_adp_entity_id 
                                  >> 8U)));
    vlSelfRef.milan_datapath__DOT__adp_adv__DOT__fb[25U] 
        = (0x000000ffU & (IData)(vlSelfRef.milan_datapath__DOT__cfg_adp_entity_id));
    vlSelfRef.milan_datapath__DOT__adp_adv__DOT__fb[26U] 
        = (0x000000ffU & (IData)((vlSelfRef.milan_datapath__DOT__cfg_adp_entity_model_id 
                                  >> 0x38U)));
    vlSelfRef.milan_datapath__DOT__adp_adv__DOT__fb[27U] 
        = (0x000000ffU & (IData)((vlSelfRef.milan_datapath__DOT__cfg_adp_entity_model_id 
                                  >> 0x30U)));
    vlSelfRef.milan_datapath__DOT__adp_adv__DOT__fb[28U] 
        = (0x000000ffU & (IData)((vlSelfRef.milan_datapath__DOT__cfg_adp_entity_model_id 
                                  >> 0x28U)));
    vlSelfRef.milan_datapath__DOT__adp_adv__DOT__fb[29U] 
        = (0x000000ffU & (IData)((vlSelfRef.milan_datapath__DOT__cfg_adp_entity_model_id 
                                  >> 0x20U)));
    vlSelfRef.milan_datapath__DOT__adp_adv__DOT__fb[30U] 
        = (0x000000ffU & (IData)((vlSelfRef.milan_datapath__DOT__cfg_adp_entity_model_id 
                                  >> 0x18U)));
    vlSelfRef.milan_datapath__DOT__adp_adv__DOT__fb[31U] 
        = (0x000000ffU & (IData)((vlSelfRef.milan_datapath__DOT__cfg_adp_entity_model_id 
                                  >> 0x10U)));
    vlSelfRef.milan_datapath__DOT__adp_adv__DOT__fb[32U] 
        = (0x000000ffU & (IData)((vlSelfRef.milan_datapath__DOT__cfg_adp_entity_model_id 
                                  >> 8U)));
    vlSelfRef.milan_datapath__DOT__adp_adv__DOT__fb[33U] 
        = (0x000000ffU & (IData)(vlSelfRef.milan_datapath__DOT__cfg_adp_entity_model_id));
    vlSelfRef.milan_datapath__DOT__adp_adv__DOT__fb[34U] 
        = (vlSelfRef.milan_datapath__DOT__csr__DOT__adp_ecaps 
           >> 0x18U);
    vlSelfRef.milan_datapath__DOT__adp_adv__DOT__fb[35U] 
        = (0x000000ffU & (vlSelfRef.milan_datapath__DOT__csr__DOT__adp_ecaps 
                          >> 0x10U));
    vlSelfRef.milan_datapath__DOT__adp_adv__DOT__fb[36U] 
        = (0x000000ffU & (vlSelfRef.milan_datapath__DOT__csr__DOT__adp_ecaps 
                          >> 8U));
    vlSelfRef.milan_datapath__DOT__adp_adv__DOT__fb[37U] 
        = (0x000000ffU & vlSelfRef.milan_datapath__DOT__csr__DOT__adp_ecaps);
    vlSelfRef.milan_datapath__DOT__adp_adv__DOT__fb[38U] = 0U;
    vlSelfRef.milan_datapath__DOT__adp_adv__DOT__fb[39U] = 9U;
    vlSelfRef.milan_datapath__DOT__adp_adv__DOT__fb[40U] = 0x48U;
    vlSelfRef.milan_datapath__DOT__adp_adv__DOT__fb[41U] = 1U;
    vlSelfRef.milan_datapath__DOT__adp_adv__DOT__fb[42U] = 0U;
    vlSelfRef.milan_datapath__DOT__adp_adv__DOT__fb[43U] = 9U;
    vlSelfRef.milan_datapath__DOT__adp_adv__DOT__fb[44U] = 0x48U;
    vlSelfRef.milan_datapath__DOT__adp_adv__DOT__fb[45U] = 1U;
    vlSelfRef.milan_datapath__DOT__adp_adv__DOT__fb[46U] 
        = (vlSelfRef.milan_datapath__DOT__csr__DOT__adp_ccaps 
           >> 0x18U);
    vlSelfRef.milan_datapath__DOT__adp_adv__DOT__fb[47U] 
        = (0x000000ffU & (vlSelfRef.milan_datapath__DOT__csr__DOT__adp_ccaps 
                          >> 0x10U));
    vlSelfRef.milan_datapath__DOT__adp_adv__DOT__fb[48U] 
        = (0x000000ffU & (vlSelfRef.milan_datapath__DOT__csr__DOT__adp_ccaps 
                          >> 8U));
    vlSelfRef.milan_datapath__DOT__adp_adv__DOT__fb[49U] 
        = (0x000000ffU & vlSelfRef.milan_datapath__DOT__csr__DOT__adp_ccaps);
    vlSelfRef.milan_datapath__DOT__adp_adv__DOT__fb[50U] 
        = (vlSelfRef.milan_datapath__DOT__adp_adv__DOT__tx_index_r 
           >> 0x18U);
    vlSelfRef.milan_datapath__DOT__adp_adv__DOT__fb[51U] 
        = (0x000000ffU & (vlSelfRef.milan_datapath__DOT__adp_adv__DOT__tx_index_r 
                          >> 0x10U));
    vlSelfRef.milan_datapath__DOT__adp_adv__DOT__fb[52U] 
        = (0x000000ffU & (vlSelfRef.milan_datapath__DOT__adp_adv__DOT__tx_index_r 
                          >> 8U));
    vlSelfRef.milan_datapath__DOT__adp_adv__DOT__fb[53U] 
        = (0x000000ffU & vlSelfRef.milan_datapath__DOT__adp_adv__DOT__tx_index_r);
    vlSelfRef.milan_datapath__DOT__adp_adv__DOT__fb[54U] 
        = (0x000000ffU & (IData)((vlSelfRef.milan_datapath__DOT__cfg_adp_gptp_gm 
                                  >> 0x38U)));
    vlSelfRef.milan_datapath__DOT__adp_adv__DOT__fb[55U] 
        = (0x000000ffU & (IData)((vlSelfRef.milan_datapath__DOT__cfg_adp_gptp_gm 
                                  >> 0x30U)));
    vlSelfRef.milan_datapath__DOT__adp_adv__DOT__fb[56U] 
        = (0x000000ffU & (IData)((vlSelfRef.milan_datapath__DOT__cfg_adp_gptp_gm 
                                  >> 0x28U)));
    vlSelfRef.milan_datapath__DOT__adp_adv__DOT__fb[57U] 
        = (0x000000ffU & (IData)((vlSelfRef.milan_datapath__DOT__cfg_adp_gptp_gm 
                                  >> 0x20U)));
    vlSelfRef.milan_datapath__DOT__adp_adv__DOT__fb[58U] 
        = (0x000000ffU & (IData)((vlSelfRef.milan_datapath__DOT__cfg_adp_gptp_gm 
                                  >> 0x18U)));
    vlSelfRef.milan_datapath__DOT__adp_adv__DOT__fb[59U] 
        = (0x000000ffU & (IData)((vlSelfRef.milan_datapath__DOT__cfg_adp_gptp_gm 
                                  >> 0x10U)));
    vlSelfRef.milan_datapath__DOT__adp_adv__DOT__fb[60U] 
        = (0x000000ffU & (IData)((vlSelfRef.milan_datapath__DOT__cfg_adp_gptp_gm 
                                  >> 8U)));
    vlSelfRef.milan_datapath__DOT__adp_adv__DOT__fb[61U] 
        = (0x000000ffU & (IData)(vlSelfRef.milan_datapath__DOT__cfg_adp_gptp_gm));
    vlSelfRef.milan_datapath__DOT__adp_adv__DOT__fb[62U] 
        = (0x000000ffU & vlSelfRef.milan_datapath__DOT__csr__DOT__adp_domain);
    vlSelfRef.milan_datapath__DOT__adp_adv__DOT__fb[63U] = 0U;
    vlSelfRef.milan_datapath__DOT__adp_adv__DOT__fb[64U] 
        = (0x000000ffU & (vlSelfRef.milan_datapath__DOT__csr__DOT__adp_idx0 
                          >> 8U));
    vlSelfRef.milan_datapath__DOT__adp_adv__DOT__fb[65U] 
        = (0x000000ffU & vlSelfRef.milan_datapath__DOT__csr__DOT__adp_idx0);
    vlSelfRef.milan_datapath__DOT__adp_adv__DOT__fb[66U] 
        = (vlSelfRef.milan_datapath__DOT__csr__DOT__adp_idx0 
           >> 0x00000018U);
    vlSelfRef.milan_datapath__DOT__adp_adv__DOT__fb[67U] 
        = (0x000000ffU & (vlSelfRef.milan_datapath__DOT__csr__DOT__adp_idx0 
                          >> 0x00000010U));
    vlSelfRef.milan_datapath__DOT__adp_adv__DOT__fb[68U] 
        = (0x000000ffU & (vlSelfRef.milan_datapath__DOT__csr__DOT__adp_idx1 
                          >> 8U));
    vlSelfRef.milan_datapath__DOT__adp_adv__DOT__fb[69U] 
        = (0x000000ffU & vlSelfRef.milan_datapath__DOT__csr__DOT__adp_idx1);
    vlSelfRef.milan_datapath__DOT__adp_adv__DOT__fb[70U] 
        = (0x000000ffU & (IData)((vlSelfRef.milan_datapath__DOT__cfg_adp_association_id 
                                  >> 0x38U)));
    vlSelfRef.milan_datapath__DOT__adp_adv__DOT__fb[71U] 
        = (0x000000ffU & (IData)((vlSelfRef.milan_datapath__DOT__cfg_adp_association_id 
                                  >> 0x30U)));
    vlSelfRef.milan_datapath__DOT__adp_adv__DOT__fb[72U] 
        = (0x000000ffU & (IData)((vlSelfRef.milan_datapath__DOT__cfg_adp_association_id 
                                  >> 0x28U)));
    vlSelfRef.milan_datapath__DOT__adp_adv__DOT__fb[73U] 
        = (0x000000ffU & (IData)((vlSelfRef.milan_datapath__DOT__cfg_adp_association_id 
                                  >> 0x20U)));
    vlSelfRef.milan_datapath__DOT__adp_adv__DOT__fb[74U] 
        = (0x000000ffU & (IData)((vlSelfRef.milan_datapath__DOT__cfg_adp_association_id 
                                  >> 0x18U)));
    vlSelfRef.milan_datapath__DOT__adp_adv__DOT__fb[75U] 
        = (0x000000ffU & (IData)((vlSelfRef.milan_datapath__DOT__cfg_adp_association_id 
                                  >> 0x10U)));
    vlSelfRef.milan_datapath__DOT__adp_adv__DOT__fb[76U] 
        = (0x000000ffU & (IData)((vlSelfRef.milan_datapath__DOT__cfg_adp_association_id 
                                  >> 8U)));
    vlSelfRef.milan_datapath__DOT__adp_adv__DOT__fb[77U] 
        = (0x000000ffU & (IData)(vlSelfRef.milan_datapath__DOT__cfg_adp_association_id));
    vlSelfRef.milan_datapath__DOT__eff_crft_sid_w = 
        ((0U != vlSelfRef.milan_datapath__DOT__cfg_crft_sid)
          ? vlSelfRef.milan_datapath__DOT__cfg_crft_sid
          : (8ULL | (vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w 
                     << 0x00000010U)));
    milan_datapath__DOT__aaf_packetizer__DOT__stream_id_w 
        = ((vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w 
            << 0x00000010U) | (QData)((IData)(((IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__euid_r) 
                                               & (- (IData)(
                                                            (0U 
                                                             != (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__et_r))))))));
    milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_resp 
        = vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rword_w;
    if ((8U & (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__beat_r))) {
        if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__beat_r) 
                      >> 2U)))) {
            if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__beat_r) 
                          >> 1U)))) {
                if ((1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__beat_r)))) {
                    milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_resp 
                        = ((0xffffffffffff0000ULL & milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_resp) 
                           | (IData)((IData)(((0x0000ff00U 
                                               & ((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_resp_flags) 
                                                  << 8U)) 
                                              | (0x000000ffU 
                                                 & ((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_resp_flags) 
                                                    >> 8U))))));
                    if ((2U != (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__resp_kind_r))) {
                        milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_resp 
                            = (0xffffffff0000ffffULL 
                               & milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_resp);
                    }
                }
            }
        }
    } else if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__beat_r))) {
        if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__beat_r))) {
            if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__beat_r))) {
                milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_resp 
                    = ((0xffffffffff000000ULL & milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_resp) 
                       | (IData)((IData)(((0x00ff0000U 
                                           & ((IData)(
                                                      (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_dmac_echo 
                                                       >> 8U)) 
                                              << 0x00000010U)) 
                                          | ((0x0000ff00U 
                                              & ((IData)(
                                                         (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_dmac_echo 
                                                          >> 0x10U)) 
                                                 << 8U)) 
                                             | (0x000000ffU 
                                                & (IData)(
                                                          (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_dmac_echo 
                                                           >> 0x18U))))))));
                milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_resp 
                    = ((0xffffff0000ffffffULL & milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_resp) 
                       | ((QData)((IData)((0x000000ffU 
                                           & (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_dmac_echo)))) 
                          << 0x00000018U));
                milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_resp 
                    = ((0xffff00ffffffffffULL & milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_resp) 
                       | ((QData)((IData)(((0U == (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__resp_kind_r))
                                            ? 1U : 
                                           (((2U == (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__resp_kind_r)) 
                                             & (0U 
                                                != 
                                                (7U 
                                                 & (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r[9U] 
                                                    >> 0x0000001aU))))
                                             ? 1U : 0U)))) 
                          << 0x00000028U));
            } else {
                if ((0U != (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__resp_kind_r))) {
                    milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_resp 
                        = ((0xffffffff0000ffffULL & milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_resp) 
                           | ((QData)((IData)(((((0U 
                                                  != 
                                                  (7U 
                                                   & (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r[9U] 
                                                      >> 0x0000001aU)))
                                                  ? 
                                                 (0x000000ffU 
                                                  & (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r[8U] 
                                                     >> 0x0000000cU))
                                                  : 0U) 
                                                << 8U) 
                                               | ((0U 
                                                   != 
                                                   (7U 
                                                    & (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r[9U] 
                                                       >> 0x0000001aU)))
                                                   ? 
                                                  (0x000000ffU 
                                                   & (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r[8U] 
                                                      >> 0x00000014U))
                                                   : 0U)))) 
                              << 0x00000010U));
                }
                milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_resp 
                    = ((0x0000ffffffffffffULL & milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_resp) 
                       | ((QData)((IData)(((0x0000ff00U 
                                            & ((IData)(
                                                       (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_dmac_echo 
                                                        >> 0x20U)) 
                                               << 8U)) 
                                           | (0x000000ffU 
                                              & (IData)(
                                                        (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_dmac_echo 
                                                         >> 0x28U)))))) 
                          << 0x00000030U));
            }
        } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__beat_r))) {
            vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__tkb__146__echo 
                = (0x000000ffU & (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rword_w));
            vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT____VlemCall_2__tkb 
                = (0x000000ffU & ((0U == (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__resp_kind_r))
                                   ? (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__tkb__146__echo)
                                   : ((1U == (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__resp_kind_r))
                                       ? 0U : ((0U 
                                                != 
                                                (7U 
                                                 & (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r[9U] 
                                                    >> 0x0000001aU)))
                                                ? (
                                                   (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r[2U] 
                                                    << 0x00000018U) 
                                                   | (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r[2U] 
                                                      >> 8U))
                                                : 0U))));
            milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_resp 
                = ((0xffffffffffffff00ULL & milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_resp) 
                   | (IData)((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT____VlemCall_2__tkb)));
            vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__tkb__147__echo 
                = (0x000000ffU & (IData)((vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rword_w 
                                          >> 8U)));
            vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT____VlemCall_3__tkb 
                = (0x000000ffU & ((0U == (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__resp_kind_r))
                                   ? (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__tkb__147__echo)
                                   : ((1U == (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__resp_kind_r))
                                       ? 0U : ((0U 
                                                != 
                                                (7U 
                                                 & (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r[9U] 
                                                    >> 0x0000001aU)))
                                                ? vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r[2U]
                                                : 0U))));
            milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_resp 
                = ((0xffffffffffff00ffULL & milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_resp) 
                   | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT____VlemCall_3__tkb)) 
                      << 8U));
        } else {
            vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__tkb__148__echo 
                = (0x000000ffU & (IData)((vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rword_w 
                                          >> 0x10U)));
            vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT____VlemCall_1__tkb 
                = (0x000000ffU & ((0U == (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__resp_kind_r))
                                   ? (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__tkb__148__echo)
                                   : ((1U == (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__resp_kind_r))
                                       ? 0U : ((0U 
                                                != 
                                                (7U 
                                                 & (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r[9U] 
                                                    >> 0x0000001aU)))
                                                ? (
                                                   (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r[3U] 
                                                    << 8U) 
                                                   | (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r[3U] 
                                                      >> 0x00000018U))
                                                : 0U))));
            milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_resp 
                = ((0xffffffffff00ffffULL & milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_resp) 
                   | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT____VlemCall_1__tkb)) 
                      << 0x00000010U));
            vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__tkb__148__echo 
                = (0x000000ffU & (IData)((vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rword_w 
                                          >> 0x18U)));
            vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT____VlemCall_1__tkb 
                = (0x000000ffU & ((0U == (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__resp_kind_r))
                                   ? (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__tkb__148__echo)
                                   : ((1U == (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__resp_kind_r))
                                       ? 0U : ((0U 
                                                != 
                                                (7U 
                                                 & (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r[9U] 
                                                    >> 0x0000001aU)))
                                                ? (
                                                   (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r[3U] 
                                                    << 0x00000010U) 
                                                   | (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r[3U] 
                                                      >> 0x00000010U))
                                                : 0U))));
            milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_resp 
                = ((0xffffffff00ffffffULL & milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_resp) 
                   | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT____VlemCall_1__tkb)) 
                      << 0x00000018U));
            vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__tkb__148__echo 
                = (0x000000ffU & (IData)((vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rword_w 
                                          >> 0x20U)));
            vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT____VlemCall_1__tkb 
                = (0x000000ffU & ((0U == (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__resp_kind_r))
                                   ? (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__tkb__148__echo)
                                   : ((1U == (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__resp_kind_r))
                                       ? 0U : ((0U 
                                                != 
                                                (7U 
                                                 & (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r[9U] 
                                                    >> 0x0000001aU)))
                                                ? (
                                                   (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r[3U] 
                                                    << 0x00000018U) 
                                                   | (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r[3U] 
                                                      >> 8U))
                                                : 0U))));
            milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_resp 
                = ((0xffffff00ffffffffULL & milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_resp) 
                   | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT____VlemCall_1__tkb)) 
                      << 0x00000020U));
            vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__tkb__148__echo 
                = (0x000000ffU & (IData)((vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rword_w 
                                          >> 0x28U)));
            vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT____VlemCall_1__tkb 
                = (0x000000ffU & ((0U == (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__resp_kind_r))
                                   ? (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__tkb__148__echo)
                                   : ((1U == (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__resp_kind_r))
                                       ? 0U : ((0U 
                                                != 
                                                (7U 
                                                 & (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r[9U] 
                                                    >> 0x0000001aU)))
                                                ? vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r[3U]
                                                : 0U))));
            milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_resp 
                = ((0xffff00ffffffffffULL & milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_resp) 
                   | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT____VlemCall_1__tkb)) 
                      << 0x00000028U));
            vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__tkb__148__echo 
                = (0x000000ffU & (IData)((vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rword_w 
                                          >> 0x30U)));
            vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT____VlemCall_1__tkb 
                = (0x000000ffU & ((0U == (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__resp_kind_r))
                                   ? (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__tkb__148__echo)
                                   : ((1U == (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__resp_kind_r))
                                       ? 0U : ((0U 
                                                != 
                                                (7U 
                                                 & (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r[9U] 
                                                    >> 0x0000001aU)))
                                                ? (
                                                   (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r[2U] 
                                                    << 8U) 
                                                   | (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r[2U] 
                                                      >> 0x00000018U))
                                                : 0U))));
            milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_resp 
                = ((0xff00ffffffffffffULL & milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_resp) 
                   | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT____VlemCall_1__tkb)) 
                      << 0x00000030U));
            vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__tkb__148__echo 
                = (0x000000ffU & (IData)((vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rword_w 
                                          >> 0x38U)));
            vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT____VlemCall_1__tkb 
                = (0x000000ffU & ((0U == (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__resp_kind_r))
                                   ? (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__tkb__148__echo)
                                   : ((1U == (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__resp_kind_r))
                                       ? 0U : ((0U 
                                                != 
                                                (7U 
                                                 & (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r[9U] 
                                                    >> 0x0000001aU)))
                                                ? (
                                                   (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r[2U] 
                                                    << 0x00000010U) 
                                                   | (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r[2U] 
                                                      >> 0x00000010U))
                                                : 0U))));
            milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_resp 
                = ((0x00ffffffffffffffULL & milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_resp) 
                   | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT____VlemCall_1__tkb)) 
                      << 0x00000038U));
        }
    } else if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__beat_r))) {
        if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__beat_r))) {
            if ((2U != (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__resp_kind_r))) {
                milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_resp 
                    = (0xffffffffffff0000ULL & milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_resp);
            }
        } else {
            milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_resp 
                = ((0xffffffffffff0000ULL & milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_resp) 
                   | (IData)((IData)((0x00002c00U | 
                                      ((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__resp_status_r) 
                                       << 3U)))));
            if ((2U != (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__resp_kind_r))) {
                milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_resp 
                    = (0x000000000000ffffULL & milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_resp);
            }
        }
    } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__beat_r))) {
        milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_resp 
            = ((0xffffffffff000000ULL & milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_resp) 
               | (IData)((IData)(((0x00ff0000U & ((IData)(
                                                          (vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w 
                                                           >> 8U)) 
                                                  << 0x00000010U)) 
                                  | ((0x0000ff00U & 
                                      ((IData)((vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w 
                                                >> 0x10U)) 
                                       << 8U)) | (0x000000ffU 
                                                  & (IData)(
                                                            (vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w 
                                                             >> 0x18U))))))));
        milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_resp 
            = ((0xffffffff00ffffffULL & milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_resp) 
               | ((QData)((IData)((0x000000ffU & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w)))) 
                  << 0x00000018U));
        milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_resp 
            = ((0x00ffffffffffffffULL & milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_resp) 
               | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__resp_msg_r)) 
                  << 0x00000038U));
    } else {
        milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_resp 
            = ((0x0000ffffffffffffULL & milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_resp) 
               | ((QData)((IData)(((0x0000ff00U & ((IData)(
                                                           (vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w 
                                                            >> 0x20U)) 
                                                   << 8U)) 
                                   | (0x000000ffU & (IData)(
                                                            (vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w 
                                                             >> 0x28U)))))) 
                  << 0x00000030U));
    }
    milan_datapath__DOT__lwsrp__DOT__tx__DOT__unnamedblk1__DOT__unnamedblk2__DOT__k = 0U;
    while (VL_GTS_III(32, 0x00000058U, milan_datapath__DOT__lwsrp__DOT__tx__DOT__unnamedblk1__DOT__unnamedblk2__DOT__k)) {
        if (VL_LIKELY(((0x57U >= (0x0000007fU & milan_datapath__DOT__lwsrp__DOT__tx__DOT__unnamedblk1__DOT__unnamedblk2__DOT__k))))) {
            vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__fb[(0x0000007fU 
                                                                    & milan_datapath__DOT__lwsrp__DOT__tx__DOT__unnamedblk1__DOT__unnamedblk2__DOT__k)] = 0U;
        }
        milan_datapath__DOT__lwsrp__DOT__tx__DOT__unnamedblk1__DOT__unnamedblk2__DOT__k 
            = ((IData)(1U) + milan_datapath__DOT__lwsrp__DOT__tx__DOT__unnamedblk1__DOT__unnamedblk2__DOT__k);
    }
    __Vfunc_milan_datapath__DOT__lwsrp__DOT__tx__DOT__vech__27__lva 
        = vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__lva_r;
    __Vfunc_milan_datapath__DOT__lwsrp__DOT__tx__DOT__vech__27__Vfuncout 
        = (1U | (((IData)(__Vfunc_milan_datapath__DOT__lwsrp__DOT__tx__DOT__vech__27__lva)
                   ? 1U : 0U) << 0x0000000dU));
    milan_datapath__DOT__lwsrp__DOT__tx__DOT__unnamedblk1__DOT__vh 
        = __Vfunc_milan_datapath__DOT__lwsrp__DOT__tx__DOT__vech__27__Vfuncout;
    milan_datapath__DOT__lwsrp__DOT__tx__DOT__unnamedblk1__DOT__lb 
        = ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__talker_incl_r)
            ? 0x0000003eU : 0x0000001cU);
    if (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__kind_r) {
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__fb[0U] = 1U;
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__fb[1U] = 0x80U;
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__fb[2U] = 0xc2U;
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__fb[3U] = 0U;
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__fb[4U] = 0U;
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__fb[5U] = 0x21U;
    } else {
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__fb[0U] = 1U;
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__fb[1U] = 0x80U;
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__fb[2U] = 0xc2U;
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__fb[3U] = 0U;
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__fb[4U] = 0U;
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__fb[5U] = 0x0eU;
    }
    vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__fb[6U] 
        = (0x000000ffU & (IData)((vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w 
                                  >> 0x28U)));
    vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__fb[7U] 
        = (0x000000ffU & (IData)((vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w 
                                  >> 0x20U)));
    vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__fb[8U] 
        = (0x000000ffU & (IData)((vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w 
                                  >> 0x18U)));
    vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__fb[9U] 
        = (0x000000ffU & (IData)((vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w 
                                  >> 0x10U)));
    vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__fb[10U] 
        = (0x000000ffU & (IData)((vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w 
                                  >> 8U)));
    vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__fb[11U] 
        = (0x000000ffU & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w));
    if (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__kind_r) {
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__fb[12U] = 0x88U;
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__fb[13U] = 0xf5U;
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__fb[14U] = 0U;
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__fb[15U] = 1U;
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__fb[16U] = 2U;
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__fb[17U] 
            = (0x000000ffU & ((IData)(milan_datapath__DOT__lwsrp__DOT__tx__DOT__unnamedblk1__DOT__vh) 
                              >> 8U));
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__fb[18U] 
            = (0x000000ffU & (IData)(milan_datapath__DOT__lwsrp__DOT__tx__DOT__unnamedblk1__DOT__vh));
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__fb[19U] 
            = (0x0000000fU & (vlSelfRef.milan_datapath__DOT__csr__DOT__lwsrp_vid 
                              >> 8U));
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__fb[20U] 
            = (0x000000ffU & vlSelfRef.milan_datapath__DOT__csr__DOT__lwsrp_vid);
        vlSelfRef.__Vfunc_milan_datapath__DOT__lwsrp__DOT__tx__DOT__pack3__28__e 
            = vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__vid_evt_r;
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT____VlemCall_0__pack3 
            = (0x000000ffU & ((IData)(0x24U) * (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__lwsrp__DOT__tx__DOT__pack3__28__e)));
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__fb[21U] 
            = vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT____VlemCall_0__pack3;
    } else {
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__fb[12U] = 0x22U;
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__fb[13U] = 0xeaU;
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__fb[14U] = 0U;
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__fb[15U] = 4U;
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__fb[16U] = 4U;
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__fb[17U] = 0U;
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__fb[18U] = 9U;
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__fb[19U] 
            = (0x000000ffU & ((IData)(milan_datapath__DOT__lwsrp__DOT__tx__DOT__unnamedblk1__DOT__vh) 
                              >> 8U));
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__fb[20U] 
            = (0x000000ffU & (IData)(milan_datapath__DOT__lwsrp__DOT__tx__DOT__unnamedblk1__DOT__vh));
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__fb[21U] = 6U;
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__fb[22U] = 3U;
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__fb[23U] 
            = (0x0000000fU & (vlSelfRef.milan_datapath__DOT__csr__DOT__lwsrp_vid 
                              >> 8U));
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__fb[24U] 
            = (0x000000ffU & vlSelfRef.milan_datapath__DOT__csr__DOT__lwsrp_vid);
        vlSelfRef.__Vfunc_milan_datapath__DOT__lwsrp__DOT__tx__DOT__pack3__29__e 
            = vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__domain_evt_r;
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT____VlemCall_1__pack3 
            = (0x000000ffU & ((IData)(0x24U) * (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__lwsrp__DOT__tx__DOT__pack3__29__e)));
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__fb[25U] 
            = vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT____VlemCall_1__pack3;
        if (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__talker_incl_r) {
            vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__fb[28U] = 1U;
            vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__fb[29U] = 0x19U;
            vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__fb[30U] = 0U;
            vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__fb[31U] = 0x1eU;
            vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__fb[32U] 
                = (0x000000ffU & ((IData)(milan_datapath__DOT__lwsrp__DOT__tx__DOT__unnamedblk1__DOT__vh) 
                                  >> 8U));
            vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__fb[33U] 
                = (0x000000ffU & (IData)(milan_datapath__DOT__lwsrp__DOT__tx__DOT__unnamedblk1__DOT__vh));
            vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__fb[34U] 
                = (0x000000ffU & (IData)((vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w 
                                          >> 0x28U)));
            vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__fb[35U] 
                = (0x000000ffU & (IData)((vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w 
                                          >> 0x20U)));
            vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__fb[36U] 
                = (0x000000ffU & (IData)((vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w 
                                          >> 0x18U)));
            vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__fb[37U] 
                = (0x000000ffU & (IData)((vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w 
                                          >> 0x10U)));
            vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__fb[38U] 
                = (0x000000ffU & (IData)((vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w 
                                          >> 8U)));
            vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__fb[39U] 
                = (0x000000ffU & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w));
            vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__fb[40U] = 0U;
            vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__fb[41U] = 0U;
            vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__fb[42U] 
                = (0x000000ffU & (IData)((vlSelfRef.milan_datapath__DOT__cfg_lwsrp_dmac 
                                          >> 0x28U)));
            vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__fb[43U] 
                = (0x000000ffU & (IData)((vlSelfRef.milan_datapath__DOT__cfg_lwsrp_dmac 
                                          >> 0x20U)));
            vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__fb[44U] 
                = (0x000000ffU & (IData)((vlSelfRef.milan_datapath__DOT__cfg_lwsrp_dmac 
                                          >> 0x18U)));
            vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__fb[45U] 
                = (0x000000ffU & (IData)((vlSelfRef.milan_datapath__DOT__cfg_lwsrp_dmac 
                                          >> 0x10U)));
            vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__fb[46U] 
                = (0x000000ffU & (IData)((vlSelfRef.milan_datapath__DOT__cfg_lwsrp_dmac 
                                          >> 8U)));
            vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__fb[47U] 
                = (0x000000ffU & (IData)(vlSelfRef.milan_datapath__DOT__cfg_lwsrp_dmac));
            vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__fb[48U] 
                = (0x0000000fU & (vlSelfRef.milan_datapath__DOT__csr__DOT__lwsrp_vid 
                                  >> 8U));
            vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__fb[49U] 
                = (0x000000ffU & vlSelfRef.milan_datapath__DOT__csr__DOT__lwsrp_vid);
            vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__fb[50U] 
                = (0x000000ffU & (vlSelfRef.milan_datapath__DOT__csr__DOT__lwsrp_tspec 
                                  >> 8U));
            vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__fb[51U] 
                = (0x000000ffU & vlSelfRef.milan_datapath__DOT__csr__DOT__lwsrp_tspec);
            vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__fb[52U] 
                = (vlSelfRef.milan_datapath__DOT__csr__DOT__lwsrp_tspec 
                   >> 0x00000018U);
            vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__fb[53U] 
                = (0x000000ffU & (vlSelfRef.milan_datapath__DOT__csr__DOT__lwsrp_tspec 
                                  >> 0x00000010U));
            vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__fb[54U] = 0x70U;
            vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__fb[55U] 
                = (vlSelfRef.milan_datapath__DOT__csr__DOT__lwsrp_lat 
                   >> 0x18U);
            vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__fb[56U] 
                = (0x000000ffU & (vlSelfRef.milan_datapath__DOT__csr__DOT__lwsrp_lat 
                                  >> 0x10U));
            vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__fb[57U] 
                = (0x000000ffU & (vlSelfRef.milan_datapath__DOT__csr__DOT__lwsrp_lat 
                                  >> 8U));
            vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__fb[58U] 
                = (0x000000ffU & vlSelfRef.milan_datapath__DOT__csr__DOT__lwsrp_lat);
            vlSelfRef.__Vfunc_milan_datapath__DOT__lwsrp__DOT__tx__DOT__pack3__30__e 
                = vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__talker_evt_r;
            vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT____VlemCall_2__pack3 
                = (0x000000ffU & ((IData)(0x24U) * (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__lwsrp__DOT__tx__DOT__pack3__30__e)));
            vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__fb[59U] 
                = vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT____VlemCall_2__pack3;
        }
        if (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__lstn_incl_r) {
            if ((0x57U >= (0x0000007fU & milan_datapath__DOT__lwsrp__DOT__tx__DOT__unnamedblk1__DOT__lb))) {
                vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__fb[(0x0000007fU 
                                                                        & milan_datapath__DOT__lwsrp__DOT__tx__DOT__unnamedblk1__DOT__lb)] = 3U;
            }
            if ((0x57U >= (0x0000007fU & ((IData)(1U) 
                                          + milan_datapath__DOT__lwsrp__DOT__tx__DOT__unnamedblk1__DOT__lb)))) {
                vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__fb[(0x0000007fU 
                                                                        & ((IData)(1U) 
                                                                           + milan_datapath__DOT__lwsrp__DOT__tx__DOT__unnamedblk1__DOT__lb))] = 8U;
            }
            if ((0x57U >= (0x0000007fU & ((IData)(2U) 
                                          + milan_datapath__DOT__lwsrp__DOT__tx__DOT__unnamedblk1__DOT__lb)))) {
                vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__fb[(0x0000007fU 
                                                                        & ((IData)(2U) 
                                                                           + milan_datapath__DOT__lwsrp__DOT__tx__DOT__unnamedblk1__DOT__lb))] = 0U;
            }
            if ((0x57U >= (0x0000007fU & ((IData)(3U) 
                                          + milan_datapath__DOT__lwsrp__DOT__tx__DOT__unnamedblk1__DOT__lb)))) {
                vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__fb[(0x0000007fU 
                                                                        & ((IData)(3U) 
                                                                           + milan_datapath__DOT__lwsrp__DOT__tx__DOT__unnamedblk1__DOT__lb))] = 0x0eU;
            }
            if ((0x57U >= (0x0000007fU & ((IData)(4U) 
                                          + milan_datapath__DOT__lwsrp__DOT__tx__DOT__unnamedblk1__DOT__lb)))) {
                vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__fb[(0x0000007fU 
                                                                        & ((IData)(4U) 
                                                                           + milan_datapath__DOT__lwsrp__DOT__tx__DOT__unnamedblk1__DOT__lb))] 
                    = (0x000000ffU & ((IData)(milan_datapath__DOT__lwsrp__DOT__tx__DOT__unnamedblk1__DOT__vh) 
                                      >> 8U));
            }
            if ((0x57U >= (0x0000007fU & ((IData)(5U) 
                                          + milan_datapath__DOT__lwsrp__DOT__tx__DOT__unnamedblk1__DOT__lb)))) {
                vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__fb[(0x0000007fU 
                                                                        & ((IData)(5U) 
                                                                           + milan_datapath__DOT__lwsrp__DOT__tx__DOT__unnamedblk1__DOT__lb))] 
                    = (0x000000ffU & (IData)(milan_datapath__DOT__lwsrp__DOT__tx__DOT__unnamedblk1__DOT__vh));
            }
            if ((0x57U >= (0x0000007fU & ((IData)(6U) 
                                          + milan_datapath__DOT__lwsrp__DOT__tx__DOT__unnamedblk1__DOT__lb)))) {
                vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__fb[(0x0000007fU 
                                                                        & ((IData)(6U) 
                                                                           + milan_datapath__DOT__lwsrp__DOT__tx__DOT__unnamedblk1__DOT__lb))] 
                    = (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__view0_r[5U] 
                       >> 0x00000018U);
            }
            if ((0x57U >= (0x0000007fU & ((IData)(7U) 
                                          + milan_datapath__DOT__lwsrp__DOT__tx__DOT__unnamedblk1__DOT__lb)))) {
                vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__fb[(0x0000007fU 
                                                                        & ((IData)(7U) 
                                                                           + milan_datapath__DOT__lwsrp__DOT__tx__DOT__unnamedblk1__DOT__lb))] 
                    = (0x000000ffU & (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__view0_r[5U] 
                                      >> 0x00000010U));
            }
            if ((0x57U >= (0x0000007fU & ((IData)(8U) 
                                          + milan_datapath__DOT__lwsrp__DOT__tx__DOT__unnamedblk1__DOT__lb)))) {
                vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__fb[(0x0000007fU 
                                                                        & ((IData)(8U) 
                                                                           + milan_datapath__DOT__lwsrp__DOT__tx__DOT__unnamedblk1__DOT__lb))] 
                    = (0x000000ffU & (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__view0_r[5U] 
                                      >> 8U));
            }
            if ((0x57U >= (0x0000007fU & ((IData)(9U) 
                                          + milan_datapath__DOT__lwsrp__DOT__tx__DOT__unnamedblk1__DOT__lb)))) {
                vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__fb[(0x0000007fU 
                                                                        & ((IData)(9U) 
                                                                           + milan_datapath__DOT__lwsrp__DOT__tx__DOT__unnamedblk1__DOT__lb))] 
                    = (0x000000ffU & vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__view0_r[5U]);
            }
            if ((0x57U >= (0x0000007fU & ((IData)(0x0aU) 
                                          + milan_datapath__DOT__lwsrp__DOT__tx__DOT__unnamedblk1__DOT__lb)))) {
                vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__fb[(0x0000007fU 
                                                                        & ((IData)(0x0aU) 
                                                                           + milan_datapath__DOT__lwsrp__DOT__tx__DOT__unnamedblk1__DOT__lb))] 
                    = (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__view0_r[4U] 
                       >> 0x00000018U);
            }
            if ((0x57U >= (0x0000007fU & ((IData)(0x0bU) 
                                          + milan_datapath__DOT__lwsrp__DOT__tx__DOT__unnamedblk1__DOT__lb)))) {
                vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__fb[(0x0000007fU 
                                                                        & ((IData)(0x0bU) 
                                                                           + milan_datapath__DOT__lwsrp__DOT__tx__DOT__unnamedblk1__DOT__lb))] 
                    = (0x000000ffU & (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__view0_r[4U] 
                                      >> 0x00000010U));
            }
            if ((0x57U >= (0x0000007fU & ((IData)(0x0cU) 
                                          + milan_datapath__DOT__lwsrp__DOT__tx__DOT__unnamedblk1__DOT__lb)))) {
                vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__fb[(0x0000007fU 
                                                                        & ((IData)(0x0cU) 
                                                                           + milan_datapath__DOT__lwsrp__DOT__tx__DOT__unnamedblk1__DOT__lb))] 
                    = (0x000000ffU & (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__view0_r[4U] 
                                      >> 8U));
            }
            if ((0x57U >= (0x0000007fU & ((IData)(0x0dU) 
                                          + milan_datapath__DOT__lwsrp__DOT__tx__DOT__unnamedblk1__DOT__lb)))) {
                vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__fb[(0x0000007fU 
                                                                        & ((IData)(0x0dU) 
                                                                           + milan_datapath__DOT__lwsrp__DOT__tx__DOT__unnamedblk1__DOT__lb))] 
                    = (0x000000ffU & vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__view0_r[4U]);
            }
            vlSelfRef.__Vfunc_milan_datapath__DOT__lwsrp__DOT__tx__DOT__pack3__31__e 
                = vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__lstn_evt_r;
            vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT____VlemCall_3__pack3 
                = (0x000000ffU & ((IData)(0x24U) * (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__lwsrp__DOT__tx__DOT__pack3__31__e)));
            if ((0x57U >= (0x0000007fU & ((IData)(0x0eU) 
                                          + milan_datapath__DOT__lwsrp__DOT__tx__DOT__unnamedblk1__DOT__lb)))) {
                vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__fb[(0x0000007fU 
                                                                        & ((IData)(0x0eU) 
                                                                           + milan_datapath__DOT__lwsrp__DOT__tx__DOT__unnamedblk1__DOT__lb))] 
                    = vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT____VlemCall_3__pack3;
            }
            vlSelfRef.__Vfunc_milan_datapath__DOT__lwsrp__DOT__tx__DOT__pack4__32__p 
                = ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp_ta_registered)
                    ? 2U : 1U);
            vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT____VlemCall_4__pack4 
                = ((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__lwsrp__DOT__tx__DOT__pack4__32__p) 
                   << 6U);
            if ((0x57U >= (0x0000007fU & ((IData)(0x0fU) 
                                          + milan_datapath__DOT__lwsrp__DOT__tx__DOT__unnamedblk1__DOT__lb)))) {
                vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT__fb[(0x0000007fU 
                                                                        & ((IData)(0x0fU) 
                                                                           + milan_datapath__DOT__lwsrp__DOT__tx__DOT__unnamedblk1__DOT__lb))] 
                    = vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx__DOT____VlemCall_4__pack4;
            }
        }
    }
    vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_dyn__DOT__w_clock_id 
        = (0x000000fffe000000ULL | (((QData)((IData)(
                                                     (0x00ffffffU 
                                                      & (IData)(
                                                                (vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w 
                                                                 >> 0x00000018U))))) 
                                     << 0x00000028U) 
                                    | (QData)((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_77))));
    vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__w_beat 
        = vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__rword_w;
    if ((8U & (IData)(vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__beat_r))) {
        if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__beat_r) 
                      >> 2U)))) {
            if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__beat_r) 
                          >> 1U)))) {
                if ((1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__beat_r)))) {
                    vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__w_beat 
                        = ((0xffffffffffffff00ULL & vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__w_beat) 
                           | (IData)((IData)((0x000000ffU 
                                              & ((IData)(vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__rword_w) 
                                                 & (~ 
                                                    ((IData)(vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__flag_clr_r) 
                                                     >> 8U)))))));
                    vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__w_beat 
                        = ((0xffffffffffff00ffULL & vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__w_beat) 
                           | ((QData)((IData)((0x000000ffU 
                                               & ((IData)(
                                                          (vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__rword_w 
                                                           >> 8U)) 
                                                  & (~ (IData)(vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__flag_clr_r)))))) 
                              << 8U));
                    vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_responder__DOT__sf__253__echo 
                        = (0x000000ffU & (IData)((vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__rword_w 
                                                  >> 0x10U)));
                    vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_responder__DOT__sf__253__live 
                        = (0x0000000fU & ((IData)(vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__live_vid_r) 
                                          >> 8U));
                    vlSelfRef.milan_datapath__DOT__acmp_responder__DOT____VlemCall_14__sf 
                        = ((2U == (IData)(vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__resp_mode_r))
                            ? (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_responder__DOT__sf__253__live)
                            : ((1U == (IData)(vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__resp_mode_r))
                                ? 0U : (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_responder__DOT__sf__253__echo)));
                    vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__w_beat 
                        = ((0xffffffffff00ffffULL & vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__w_beat) 
                           | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__acmp_responder__DOT____VlemCall_14__sf)) 
                              << 0x00000010U));
                    vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_responder__DOT__sf__254__echo 
                        = (0x000000ffU & (IData)((vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__rword_w 
                                                  >> 0x18U)));
                    vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_responder__DOT__sf__254__live 
                        = (0x000000ffU & (IData)(vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__live_vid_r));
                    vlSelfRef.milan_datapath__DOT__acmp_responder__DOT____VlemCall_15__sf 
                        = ((2U == (IData)(vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__resp_mode_r))
                            ? (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_responder__DOT__sf__254__live)
                            : ((1U == (IData)(vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__resp_mode_r))
                                ? 0U : (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_responder__DOT__sf__254__echo)));
                    vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__w_beat 
                        = ((0xffffffff00ffffffULL & vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__w_beat) 
                           | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__acmp_responder__DOT____VlemCall_15__sf)) 
                              << 0x00000018U));
                }
            }
        }
    } else if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__beat_r))) {
        if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__beat_r))) {
            if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__beat_r))) {
                vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_responder__DOT__sf__255__echo 
                    = (0x000000ffU & (IData)(vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__rword_w));
                vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_responder__DOT__sf__255__live 
                    = (0x000000ffU & (IData)((vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__live_dmac_r 
                                              >> 0x18U)));
                vlSelfRef.milan_datapath__DOT__acmp_responder__DOT____VlemCall_10__sf 
                    = ((2U == (IData)(vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__resp_mode_r))
                        ? (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_responder__DOT__sf__255__live)
                        : ((1U == (IData)(vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__resp_mode_r))
                            ? 0U : (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_responder__DOT__sf__255__echo)));
                vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__w_beat 
                    = ((0xffffffffffffff00ULL & vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__w_beat) 
                       | (IData)((IData)(vlSelfRef.milan_datapath__DOT__acmp_responder__DOT____VlemCall_10__sf)));
                vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_responder__DOT__sf__256__echo 
                    = (0x000000ffU & (IData)((vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__rword_w 
                                              >> 8U)));
                vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_responder__DOT__sf__256__live 
                    = (0x000000ffU & (IData)((vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__live_dmac_r 
                                              >> 0x10U)));
                vlSelfRef.milan_datapath__DOT__acmp_responder__DOT____VlemCall_11__sf 
                    = ((2U == (IData)(vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__resp_mode_r))
                        ? (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_responder__DOT__sf__256__live)
                        : ((1U == (IData)(vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__resp_mode_r))
                            ? 0U : (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_responder__DOT__sf__256__echo)));
                vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__w_beat 
                    = ((0xffffffffffff00ffULL & vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__w_beat) 
                       | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__acmp_responder__DOT____VlemCall_11__sf)) 
                          << 8U));
                vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_responder__DOT__sf__257__echo 
                    = (0x000000ffU & (IData)((vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__rword_w 
                                              >> 0x10U)));
                vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_responder__DOT__sf__257__live 
                    = (0x000000ffU & (IData)((vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__live_dmac_r 
                                              >> 8U)));
                vlSelfRef.milan_datapath__DOT__acmp_responder__DOT____VlemCall_12__sf 
                    = ((2U == (IData)(vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__resp_mode_r))
                        ? (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_responder__DOT__sf__257__live)
                        : ((1U == (IData)(vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__resp_mode_r))
                            ? 0U : (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_responder__DOT__sf__257__echo)));
                vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__w_beat 
                    = ((0xffffffffff00ffffULL & vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__w_beat) 
                       | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__acmp_responder__DOT____VlemCall_12__sf)) 
                          << 0x00000010U));
                vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_responder__DOT__sf__258__echo 
                    = (0x000000ffU & (IData)((vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__rword_w 
                                              >> 0x18U)));
                vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_responder__DOT__sf__258__live 
                    = (0x000000ffU & (IData)(vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__live_dmac_r));
                vlSelfRef.milan_datapath__DOT__acmp_responder__DOT____VlemCall_13__sf 
                    = ((2U == (IData)(vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__resp_mode_r))
                        ? (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_responder__DOT__sf__258__live)
                        : ((1U == (IData)(vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__resp_mode_r))
                            ? 0U : (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_responder__DOT__sf__258__echo)));
                vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__w_beat 
                    = ((0xffffffff00ffffffULL & vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__w_beat) 
                       | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__acmp_responder__DOT____VlemCall_13__sf)) 
                          << 0x00000018U));
                if ((0U != (IData)(vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__resp_mode_r))) {
                    vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__w_beat 
                        = (0xffff0000ffffffffULL & vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__w_beat);
                }
            } else {
                vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_responder__DOT__sf__259__echo 
                    = (0x000000ffU & (IData)((vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__rword_w 
                                              >> 0x30U)));
                vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_responder__DOT__sf__259__live 
                    = (0x000000ffU & (IData)((vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__live_dmac_r 
                                              >> 0x28U)));
                vlSelfRef.milan_datapath__DOT__acmp_responder__DOT____VlemCall_8__sf 
                    = ((2U == (IData)(vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__resp_mode_r))
                        ? (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_responder__DOT__sf__259__live)
                        : ((1U == (IData)(vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__resp_mode_r))
                            ? 0U : (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_responder__DOT__sf__259__echo)));
                vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__w_beat 
                    = ((0xff00ffffffffffffULL & vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__w_beat) 
                       | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__acmp_responder__DOT____VlemCall_8__sf)) 
                          << 0x00000030U));
                vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_responder__DOT__sf__260__echo 
                    = (0x000000ffU & (IData)((vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__rword_w 
                                              >> 0x38U)));
                vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_responder__DOT__sf__260__live 
                    = (0x000000ffU & (IData)((vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__live_dmac_r 
                                              >> 0x20U)));
                vlSelfRef.milan_datapath__DOT__acmp_responder__DOT____VlemCall_9__sf 
                    = ((2U == (IData)(vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__resp_mode_r))
                        ? (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_responder__DOT__sf__260__live)
                        : ((1U == (IData)(vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__resp_mode_r))
                            ? 0U : (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_responder__DOT__sf__260__echo)));
                vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__w_beat 
                    = ((0x00ffffffffffffffULL & vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__w_beat) 
                       | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__acmp_responder__DOT____VlemCall_9__sf)) 
                          << 0x00000038U));
            }
        }
    } else if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__beat_r))) {
        if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__beat_r))) {
            vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_responder__DOT__sf__261__echo 
                = (0x000000ffU & (IData)(vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__rword_w));
            vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_responder__DOT__sf__261__live 
                = (0x000000ffU & ((IData)(vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__tuid_r) 
                                  >> 8U));
            vlSelfRef.milan_datapath__DOT__acmp_responder__DOT____VlemCall_6__sf 
                = ((2U == (IData)(vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__resp_mode_r))
                    ? (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_responder__DOT__sf__261__live)
                    : ((1U == (IData)(vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__resp_mode_r))
                        ? 0U : (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_responder__DOT__sf__261__echo)));
            vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__w_beat 
                = ((0xffffffffffffff00ULL & vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__w_beat) 
                   | (IData)((IData)(vlSelfRef.milan_datapath__DOT__acmp_responder__DOT____VlemCall_6__sf)));
            vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_responder__DOT__sf__262__echo 
                = (0x000000ffU & (IData)((vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__rword_w 
                                          >> 8U)));
            vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_responder__DOT__sf__262__live 
                = (0x000000ffU & (IData)(vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__tuid_r));
            vlSelfRef.milan_datapath__DOT__acmp_responder__DOT____VlemCall_7__sf 
                = ((2U == (IData)(vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__resp_mode_r))
                    ? (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_responder__DOT__sf__262__live)
                    : ((1U == (IData)(vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__resp_mode_r))
                        ? 0U : (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_responder__DOT__sf__262__echo)));
            vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__w_beat 
                = ((0xffffffffffff00ffULL & vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__w_beat) 
                   | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__acmp_responder__DOT____VlemCall_7__sf)) 
                      << 8U));
        } else {
            vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__w_beat 
                = ((0xffffffffffff0000ULL & vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__w_beat) 
                   | (IData)((IData)((0x00002c00U | 
                                      ((IData)(vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__resp_status_r) 
                                       << 3U)))));
            vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_responder__DOT__sf__263__echo 
                = (0x000000ffU & (IData)((vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__rword_w 
                                          >> 0x10U)));
            vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_responder__DOT__sf__263__live 
                = (0x000000ffU & (IData)((vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w 
                                          >> 0x28U)));
            vlSelfRef.milan_datapath__DOT__acmp_responder__DOT____VlemCall_0__sf 
                = ((2U == (IData)(vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__resp_mode_r))
                    ? (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_responder__DOT__sf__263__live)
                    : ((1U == (IData)(vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__resp_mode_r))
                        ? 0U : (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_responder__DOT__sf__263__echo)));
            vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__w_beat 
                = ((0xffffffffff00ffffULL & vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__w_beat) 
                   | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__acmp_responder__DOT____VlemCall_0__sf)) 
                      << 0x00000010U));
            vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_responder__DOT__sf__264__echo 
                = (0x000000ffU & (IData)((vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__rword_w 
                                          >> 0x18U)));
            vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_responder__DOT__sf__264__live 
                = (0x000000ffU & (IData)((vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w 
                                          >> 0x20U)));
            vlSelfRef.milan_datapath__DOT__acmp_responder__DOT____VlemCall_1__sf 
                = ((2U == (IData)(vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__resp_mode_r))
                    ? (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_responder__DOT__sf__264__live)
                    : ((1U == (IData)(vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__resp_mode_r))
                        ? 0U : (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_responder__DOT__sf__264__echo)));
            vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__w_beat 
                = ((0xffffffff00ffffffULL & vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__w_beat) 
                   | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__acmp_responder__DOT____VlemCall_1__sf)) 
                      << 0x00000018U));
            vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_responder__DOT__sf__265__echo 
                = (0x000000ffU & (IData)((vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__rword_w 
                                          >> 0x20U)));
            vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_responder__DOT__sf__265__live 
                = (0x000000ffU & (IData)((vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w 
                                          >> 0x18U)));
            vlSelfRef.milan_datapath__DOT__acmp_responder__DOT____VlemCall_2__sf 
                = ((2U == (IData)(vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__resp_mode_r))
                    ? (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_responder__DOT__sf__265__live)
                    : ((1U == (IData)(vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__resp_mode_r))
                        ? 0U : (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_responder__DOT__sf__265__echo)));
            vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__w_beat 
                = ((0xffffff00ffffffffULL & vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__w_beat) 
                   | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__acmp_responder__DOT____VlemCall_2__sf)) 
                      << 0x00000020U));
            vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_responder__DOT__sf__266__echo 
                = (0x000000ffU & (IData)((vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__rword_w 
                                          >> 0x28U)));
            vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_responder__DOT__sf__266__live 
                = (0x000000ffU & (IData)((vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w 
                                          >> 0x10U)));
            vlSelfRef.milan_datapath__DOT__acmp_responder__DOT____VlemCall_3__sf 
                = ((2U == (IData)(vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__resp_mode_r))
                    ? (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_responder__DOT__sf__266__live)
                    : ((1U == (IData)(vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__resp_mode_r))
                        ? 0U : (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_responder__DOT__sf__266__echo)));
            vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__w_beat 
                = ((0xffff00ffffffffffULL & vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__w_beat) 
                   | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__acmp_responder__DOT____VlemCall_3__sf)) 
                      << 0x00000028U));
            vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_responder__DOT__sf__267__echo 
                = (0x000000ffU & (IData)((vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__rword_w 
                                          >> 0x30U)));
            vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_responder__DOT__sf__267__live 
                = (0x000000ffU & (IData)((vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w 
                                          >> 8U)));
            vlSelfRef.milan_datapath__DOT__acmp_responder__DOT____VlemCall_4__sf 
                = ((2U == (IData)(vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__resp_mode_r))
                    ? (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_responder__DOT__sf__267__live)
                    : ((1U == (IData)(vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__resp_mode_r))
                        ? 0U : (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_responder__DOT__sf__267__echo)));
            vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__w_beat 
                = ((0xff00ffffffffffffULL & vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__w_beat) 
                   | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__acmp_responder__DOT____VlemCall_4__sf)) 
                      << 0x00000030U));
            vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_responder__DOT__sf__268__echo 
                = (0x000000ffU & (IData)((vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__rword_w 
                                          >> 0x38U)));
            vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_responder__DOT__sf__268__live 
                = (0x000000ffU & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w));
            vlSelfRef.milan_datapath__DOT__acmp_responder__DOT____VlemCall_5__sf 
                = ((2U == (IData)(vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__resp_mode_r))
                    ? (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_responder__DOT__sf__268__live)
                    : ((1U == (IData)(vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__resp_mode_r))
                        ? 0U : (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_responder__DOT__sf__268__echo)));
            vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__w_beat 
                = ((0x00ffffffffffffffULL & vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__w_beat) 
                   | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__acmp_responder__DOT____VlemCall_5__sf)) 
                      << 0x00000038U));
        }
    } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__beat_r))) {
        vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__w_beat 
            = ((0xffffffffff000000ULL & vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__w_beat) 
               | (IData)((IData)(((0x00ff0000U & ((IData)(
                                                          (vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w 
                                                           >> 8U)) 
                                                  << 0x00000010U)) 
                                  | ((0x0000ff00U & 
                                      ((IData)((vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w 
                                                >> 0x10U)) 
                                       << 8U)) | (0x000000ffU 
                                                  & (IData)(
                                                            (vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w 
                                                             >> 0x18U))))))));
        vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__w_beat 
            = ((0xffffffff00ffffffULL & vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__w_beat) 
               | ((QData)((IData)((0x000000ffU & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w)))) 
                  << 0x00000018U));
        vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__w_beat 
            = ((0x00ffffffffffffffULL & vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__w_beat) 
               | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__resp_msg_r)) 
                  << 0x00000038U));
    } else {
        vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__w_beat 
            = ((0x0000ffffffffffffULL & vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__w_beat) 
               | ((QData)((IData)(((0x0000ff00U & ((IData)(
                                                           (vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w 
                                                            >> 0x20U)) 
                                                   << 8U)) 
                                   | (0x000000ffU & (IData)(
                                                            (vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w 
                                                             >> 0x28U)))))) 
                  << 0x00000030U));
    }
    vlSelfRef.milan_datapath__DOT__ctl_tx_mux__DOT__active 
        = ((IData)(vlSelfRef.milan_datapath__DOT__ctl_tx_mux__DOT__locked_r) 
           | ((1U == (IData)(vlSelfRef.milan_datapath__DOT__adp_adv__DOT__state_r)) 
              | (IData)(vlSelfRef.milan_datapath__DOT__ctl2_tx_tvalid)));
    vlSelfRef.milan_datapath__DOT__ctl_tx_mux__DOT__gsel 
        = (1U & ((IData)(vlSelfRef.milan_datapath__DOT__ctl_tx_mux__DOT__locked_r)
                  ? (IData)(vlSelfRef.milan_datapath__DOT__ctl_tx_mux__DOT__sel_r)
                  : (((1U == (IData)(vlSelfRef.milan_datapath__DOT__adp_adv__DOT__state_r)) 
                      & (IData)(vlSelfRef.milan_datapath__DOT__ctl2_tx_tvalid))
                      ? (~ (IData)(vlSelfRef.milan_datapath__DOT__ctl_tx_mux__DOT__last_grant_r))
                      : (IData)(vlSelfRef.milan_datapath__DOT__ctl2_tx_tvalid))));
    milan_datapath__DOT__acmp_responder__DOT__tmr_rd_idx_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__w_swp_run)
            ? (IData)(vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__swp_idx_r)
            : (IData)(vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__w_uid_idx));
    vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__rb_row_w 
        = (0x0000000fU & (((IData)(vlSelfRef.milan_datapath__DOT____Vcellinp__lwsrp__ctx_idx_i) 
                           - (IData)(1U)) & (- (IData)(
                                                       (0x0fU 
                                                        > 
                                                        (0x0000000fU 
                                                         & ((IData)(vlSelfRef.milan_datapath__DOT____Vcellinp__lwsrp__ctx_idx_i) 
                                                            - (IData)(1U))))))));
    vlSelfRef.milan_datapath__DOT____Vcellinp__lwsrp__ctx_max_frame_i 
        = ((IData)(vlSelfRef.milan_datapath__DOT__crf_srp_gnt_w)
            ? 0x0000002aU : (0x0000ffffU & ((IData)(vlSelfRef.milan_datapath__DOT__srp_tk_row_w)
                                             ? vlSelfRef.milan_datapath__DOT__tctx_maxf_w
                                            [(7U & 
                                              (((IData)(vlSelfRef.milan_datapath__DOT__csr_srp_ctx_idx) 
                                                - (IData)(7U)) 
                                               & (- (IData)((IData)(vlSelfRef.milan_datapath__DOT__srp_tk_row_w)))))]
                                             : vlSelfRef.milan_datapath__DOT__csr__DOT__lwsrp_tspec)));
    vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__w_smap_milan_ns 
        = ((0U != (IData)(vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__w_smap_rows)) 
           & (IData)(vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__w_smap_out_ok));
    vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__w_smap_has 
        = (((IData)(vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__w_smap_in_ok) 
            | (IData)(vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__w_smap_out_ok)) 
           & (0U != (IData)(vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__w_smap_rows)));
    vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__ingress__DOT__fw_valid = 0U;
    if (((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__ingress__DOT__hold_v_r) 
         & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__ingress__DOT__hold_l_r))) {
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__ingress__DOT__fw_valid = 1U;
    } else if (((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__ingress__DOT__rxv_r) 
                & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__ingress__DOT__hold_v_r))) {
        if ((1U == (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__ingress__DOT__beat_idx_r))) {
            vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__ingress__DOT__fw_valid 
                = vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__ingress__DOT__match_w;
        } else if (vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__ingress__DOT__active_r) {
            vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__ingress__DOT__fw_valid = 1U;
        }
    }
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
    vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_val__DOT__w_ok 
        = ((IData)(milan_datapath__DOT__aecp_listener__DOT__u_val__DOT__w_type_ok) 
           & (0x000cU <= (0x000007ffU & (IData)((vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_ingress__DOT__w_out 
                                                 >> 0x00000010U)))));
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
                = (0x00ffffffU & (IData)((((4U > (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_10))
                                            ? vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__tdm_hold_r
                                           [(3U & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_10))]
                                            : 0ULL) 
                                          >> 0x00000018U)));
            vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__sel_r_w 
                = (0x00ffffffU & (IData)(((4U > (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_10))
                                           ? vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__tdm_hold_r
                                          [(3U & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_10))]
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
    vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__own_last_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pown_o_w) 
           == (3U & ((vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__chans_r
                      [vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pown_t_w] 
                      >> 1U) - (IData)(1U))));
    vlSelfRef.milan_datapath__DOT__lwsrp_tx_tlast = 
        ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__g_txmux__DOT__busy_r) 
         & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__g_txmux__DOT__sel_r)
             ? ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__last_beat_r) 
                & (5U == (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx_tx__DOT__st_r)))
             : (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__tx0_tlast_w)));
    vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__leg_hit_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ram_we_w) 
           & (0U == (0xe0U & (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ram_waddr_w))));
    vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__beat_acc 
        = ((IData)(vlSelfRef.m_axis_pcm_tready) & (IData)(vlSelfRef.milan_datapath__DOT__rend_pcm_tvalid_w));
    vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__pcm_acc_w 
        = (((1U & vlSelfRef.milan_datapath__DOT__csr__DOT__chmap_ctrl)
             ? (IData)(vlSelfRef.milan_datapath__DOT__chmap_phys_v_w)
             : (IData)(vlSelfRef.milan_datapath__DOT__rend_pcm_tvalid_w)) 
           & ((IData)(vlSelfRef.m_axis_pcm_tready) 
              | vlSelfRef.milan_datapath__DOT__csr__DOT__chmap_ctrl));
    vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__pass_sof 
        = (1U & ((~ ((IData)(vlSelfRef.s_axis_mac_rx_tlast) 
                     & (IData)(vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__sof))) 
                 & (((IData)(vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__match_any)
                      ? (~ (IData)(vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__match_act))
                      : ((2U & vlSelfRef.milan_datapath__DOT__csr__DOT__tcam_ctrl)
                          ? ((0x0000ffffffffffffULL 
                              == vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__dmac) 
                             | ((1U & (IData)(vlSelfRef.s_axis_mac_rx_tdata))
                                 ? ((IData)((vlSelfRef.o_mc_hash 
                                             >> (0x0000003fU 
                                                 & ((IData)(
                                                            (vlSelfRef.s_axis_mac_rx_tdata 
                                                             >> 2U)) 
                                                    ^ 
                                                    ((IData)(
                                                             (vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__dmac 
                                                              >> 0x00000024U)) 
                                                     ^ 
                                                     ((IData)(
                                                              (vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__dmac 
                                                               >> 0x0000001eU)) 
                                                      ^ 
                                                      ((IData)(
                                                               (vlSelfRef.s_axis_mac_rx_tdata 
                                                                >> 0x00000010U)) 
                                                       ^ 
                                                       ((IData)(
                                                                (vlSelfRef.s_axis_mac_rx_tdata 
                                                                 >> 0x0000001aU)) 
                                                        ^ 
                                                        ((IData)(
                                                                 (vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__dmac 
                                                                  >> 0x0000000cU)) 
                                                         ^ 
                                                         ((IData)(
                                                                  (vlSelfRef.s_axis_mac_rx_tdata 
                                                                   >> 0x00000028U)) 
                                                          ^ (IData)(
                                                                    (vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__dmac 
                                                                     >> 6U)))))))))))) 
                                    | (IData)(vlSelfRef.o_mac_allmulti))
                                 : (vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__dmac 
                                    == vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w)))
                          : vlSelfRef.milan_datapath__DOT__csr__DOT__tcam_ctrl)) 
                    | (IData)(vlSelfRef.o_mac_promisc))));
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
    vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__disp_s_w 
        = (7U & ((IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__pdisp_new_w)
                  ? (IData)(vlSelfRef.milan_datapath__DOT__avtprx_idx)
                  : ((vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r[0U][4U] 
                      << 0x0000000dU) | (vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r[0U][4U] 
                                         >> 0x00000013U))));
    vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_tbl_ok 
        = ((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__init_done_r) 
           & ((~ (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__strm_dir_r)) 
              & ((~ ((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_frame_latch) 
                     | ((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_launch_ok) 
                        | ((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__swp_active_r) 
                           | ((1U == (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__st_r)) 
                              | (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_rest_ok)))))) 
                 & ((9U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__strm_idx_r)) 
                    & (8U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__strm_idx_r))))));
    vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rd_idx_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_frame_latch)
            ? (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_luid_idx)
            : ((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_launch_ok)
                ? Vmilan_datapath__ConstPool__TABLE_hc68454f1_0
               [vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_pend_r]
                : ((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_swp_run)
                    ? (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__swp_idx_r)
                    : ((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_rest_ok)
                        ? (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rest_idx_r)
                        : (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__strm_idx_r)))));
    vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__ext_kd_w[0U] 
        = (IData)((((QData)((IData)((0x00001fffU & milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__2__KET____DOT__esub_w[0U]))) 
                    << 0x0000001aU) | (QData)((IData)(
                                                      ((0x03ffe000U 
                                                        & (milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__1__KET____DOT__esub_w[0U] 
                                                           << 0x0000000dU)) 
                                                       | (0x00001fffU 
                                                          & milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__0__KET____DOT__esub_w[0U]))))));
    vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__ext_kd_w[1U] 
        = ((0xffffff80U & vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__ext_kd_w[1U]) 
           | (IData)(((((QData)((IData)((0x00001fffU 
                                         & milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__2__KET____DOT__esub_w[0U]))) 
                        << 0x0000001aU) | (QData)((IData)(
                                                          ((0x03ffe000U 
                                                            & (milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__1__KET____DOT__esub_w[0U] 
                                                               << 0x0000000dU)) 
                                                           | (0x00001fffU 
                                                              & milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__0__KET____DOT__esub_w[0U]))))) 
                      >> 0x00000020U)));
    vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__ext_kd_w[1U] 
        = ((0x0000007fU & vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__ext_kd_w[1U]) 
           | ((IData)((((QData)((IData)((0x00001fffU 
                                         & milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__5__KET____DOT__esub_w[0U]))) 
                        << 0x0000001aU) | (QData)((IData)(
                                                          ((0x03ffe000U 
                                                            & (milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__4__KET____DOT__esub_w[0U] 
                                                               << 0x0000000dU)) 
                                                           | (0x00001fffU 
                                                              & milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__3__KET____DOT__esub_w[0U])))))) 
              << 7U));
    vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__ext_kd_w[2U] 
        = ((0xffffc000U & vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__ext_kd_w[2U]) 
           | (((IData)((((QData)((IData)((0x00001fffU 
                                          & milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__5__KET____DOT__esub_w[0U]))) 
                         << 0x0000001aU) | (QData)((IData)(
                                                           ((0x03ffe000U 
                                                             & (milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__4__KET____DOT__esub_w[0U] 
                                                                << 0x0000000dU)) 
                                                            | (0x00001fffU 
                                                               & milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__3__KET____DOT__esub_w[0U])))))) 
               >> 0x00000019U) | ((IData)(((((QData)((IData)(
                                                             (0x00001fffU 
                                                              & milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__5__KET____DOT__esub_w[0U]))) 
                                             << 0x0000001aU) 
                                            | (QData)((IData)(
                                                              ((0x03ffe000U 
                                                                & (milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__4__KET____DOT__esub_w[0U] 
                                                                   << 0x0000000dU)) 
                                                               | (0x00001fffU 
                                                                  & milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__3__KET____DOT__esub_w[0U]))))) 
                                           >> 0x00000020U)) 
                                  << 7U)));
    vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__ext_kd_w[2U] 
        = ((0x00003fffU & vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__ext_kd_w[2U]) 
           | ((IData)((((QData)((IData)((0x00001fffU 
                                         & milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__8__KET____DOT__esub_w[0U]))) 
                        << 0x0000001aU) | (QData)((IData)(
                                                          ((0x03ffe000U 
                                                            & (milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__7__KET____DOT__esub_w[0U] 
                                                               << 0x0000000dU)) 
                                                           | (0x00001fffU 
                                                              & milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__6__KET____DOT__esub_w[0U])))))) 
              << 0x0000000eU));
    vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__ext_kd_w[3U] 
        = ((0xffe00000U & vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__ext_kd_w[3U]) 
           | (((IData)((((QData)((IData)((0x00001fffU 
                                          & milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__8__KET____DOT__esub_w[0U]))) 
                         << 0x0000001aU) | (QData)((IData)(
                                                           ((0x03ffe000U 
                                                             & (milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__7__KET____DOT__esub_w[0U] 
                                                                << 0x0000000dU)) 
                                                            | (0x00001fffU 
                                                               & milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__6__KET____DOT__esub_w[0U])))))) 
               >> 0x00000012U) | ((IData)(((((QData)((IData)(
                                                             (0x00001fffU 
                                                              & milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__8__KET____DOT__esub_w[0U]))) 
                                             << 0x0000001aU) 
                                            | (QData)((IData)(
                                                              ((0x03ffe000U 
                                                                & (milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__7__KET____DOT__esub_w[0U] 
                                                                   << 0x0000000dU)) 
                                                               | (0x00001fffU 
                                                                  & milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__6__KET____DOT__esub_w[0U]))))) 
                                           >> 0x00000020U)) 
                                  << 0x0000000eU)));
    vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__ext_kd_w[3U] 
        = ((0x001fffffU & vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__ext_kd_w[3U]) 
           | ((IData)((((QData)((IData)((0x00001fffU 
                                         & milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__11__KET____DOT__esub_w[0U]))) 
                        << 0x0000001aU) | (QData)((IData)(
                                                          ((0x03ffe000U 
                                                            & (milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__10__KET____DOT__esub_w[0U] 
                                                               << 0x0000000dU)) 
                                                           | (0x00001fffU 
                                                              & milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__9__KET____DOT__esub_w[0U])))))) 
              << 0x00000015U));
    vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__ext_kd_w[4U] 
        = ((0xf0000000U & vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__ext_kd_w[4U]) 
           | (((IData)((((QData)((IData)((0x00001fffU 
                                          & milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__11__KET____DOT__esub_w[0U]))) 
                         << 0x0000001aU) | (QData)((IData)(
                                                           ((0x03ffe000U 
                                                             & (milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__10__KET____DOT__esub_w[0U] 
                                                                << 0x0000000dU)) 
                                                            | (0x00001fffU 
                                                               & milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__9__KET____DOT__esub_w[0U])))))) 
               >> 0x0000000bU) | ((IData)(((((QData)((IData)(
                                                             (0x00001fffU 
                                                              & milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__11__KET____DOT__esub_w[0U]))) 
                                             << 0x0000001aU) 
                                            | (QData)((IData)(
                                                              ((0x03ffe000U 
                                                                & (milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__10__KET____DOT__esub_w[0U] 
                                                                   << 0x0000000dU)) 
                                                               | (0x00001fffU 
                                                                  & milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__9__KET____DOT__esub_w[0U]))))) 
                                           >> 0x00000020U)) 
                                  << 0x00000015U)));
    vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__ext_kd_w[4U] 
        = ((0x0fffffffU & vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__ext_kd_w[4U]) 
           | ((IData)((((QData)((IData)((0x00001fffU 
                                         & milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__14__KET____DOT__esub_w[0U]))) 
                        << 0x0000001aU) | (QData)((IData)(
                                                          ((0x03ffe000U 
                                                            & (milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__13__KET____DOT__esub_w[0U] 
                                                               << 0x0000000dU)) 
                                                           | (0x00001fffU 
                                                              & milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__12__KET____DOT__esub_w[0U])))))) 
              << 0x0000001cU));
    vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__ext_kd_w[5U] 
        = (((IData)((((QData)((IData)((0x00001fffU 
                                       & milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__14__KET____DOT__esub_w[0U]))) 
                      << 0x0000001aU) | (QData)((IData)(
                                                        ((0x03ffe000U 
                                                          & (milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__13__KET____DOT__esub_w[0U] 
                                                             << 0x0000000dU)) 
                                                         | (0x00001fffU 
                                                            & milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__12__KET____DOT__esub_w[0U])))))) 
            >> 4U) | ((IData)(((((QData)((IData)((0x00001fffU 
                                                  & milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__14__KET____DOT__esub_w[0U]))) 
                                 << 0x0000001aU) | (QData)((IData)(
                                                                   ((0x03ffe000U 
                                                                     & (milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__13__KET____DOT__esub_w[0U] 
                                                                        << 0x0000000dU)) 
                                                                    | (0x00001fffU 
                                                                       & milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__12__KET____DOT__esub_w[0U]))))) 
                               >> 0x00000020U)) << 0x0000001cU));
    vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__ext_kd_w[6U] 
        = (7U & ((IData)(((((QData)((IData)((0x00001fffU 
                                             & milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__14__KET____DOT__esub_w[0U]))) 
                            << 0x0000001aU) | (QData)((IData)(
                                                              ((0x03ffe000U 
                                                                & (milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__13__KET____DOT__esub_w[0U] 
                                                                   << 0x0000000dU)) 
                                                               | (0x00001fffU 
                                                                  & milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__12__KET____DOT__esub_w[0U]))))) 
                          >> 0x00000020U)) >> 4U));
    vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__ext_hit_w 
        = (((((((0x0007fffeU & (((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__valid_r) 
                                 >> 0x0000000dU) & 
                                (((0ULL == (0x000fffffffffffffULL 
                                            & (((QData)((IData)(milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__14__KET____DOT__esub_w[2U])) 
                                                << 0x00000033U) 
                                               | (((QData)((IData)(milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__14__KET____DOT__esub_w[1U])) 
                                                   << 0x00000013U) 
                                                  | ((QData)((IData)(milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__14__KET____DOT__esub_w[0U])) 
                                                     >> 0x0000000dU))))) 
                                  & ((0x00001fffU & milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__14__KET____DOT__esub_w[0U]) 
                                     < (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__nv_r))) 
                                 << 1U))) | (((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__valid_r) 
                                              >> 0x0000000dU) 
                                             & ((0ULL 
                                                 == 
                                                 (0x000fffffffffffffULL 
                                                  & (((QData)((IData)(milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__13__KET____DOT__esub_w[2U])) 
                                                      << 0x00000033U) 
                                                     | (((QData)((IData)(milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__13__KET____DOT__esub_w[1U])) 
                                                         << 0x00000013U) 
                                                        | ((QData)((IData)(milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__13__KET____DOT__esub_w[0U])) 
                                                           >> 0x0000000dU))))) 
                                                & ((0x00001fffU 
                                                    & milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__13__KET____DOT__esub_w[0U]) 
                                                   < (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__nv_r))))) 
               << 6U) | (((0x001ffffeU & (((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__valid_r) 
                                           >> 0x0000000bU) 
                                          & (((0ULL 
                                               == (0x000fffffffffffffULL 
                                                   & (((QData)((IData)(milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__12__KET____DOT__esub_w[2U])) 
                                                       << 0x00000033U) 
                                                      | (((QData)((IData)(milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__12__KET____DOT__esub_w[1U])) 
                                                          << 0x00000013U) 
                                                         | ((QData)((IData)(milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__12__KET____DOT__esub_w[0U])) 
                                                            >> 0x0000000dU))))) 
                                              & ((0x00001fffU 
                                                  & milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__12__KET____DOT__esub_w[0U]) 
                                                 < (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__nv_r))) 
                                             << 1U))) 
                          | (((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__valid_r) 
                              >> 0x0000000bU) & ((0ULL 
                                                  == 
                                                  (0x000fffffffffffffULL 
                                                   & (((QData)((IData)(milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__11__KET____DOT__esub_w[2U])) 
                                                       << 0x00000033U) 
                                                      | (((QData)((IData)(milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__11__KET____DOT__esub_w[1U])) 
                                                          << 0x00000013U) 
                                                         | ((QData)((IData)(milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__11__KET____DOT__esub_w[0U])) 
                                                            >> 0x0000000dU))))) 
                                                 & ((0x00001fffU 
                                                     & milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__11__KET____DOT__esub_w[0U]) 
                                                    < (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__nv_r))))) 
                         << 4U)) | ((((0x007ffffeU 
                                       & (((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__valid_r) 
                                           >> 9U) & 
                                          (((0ULL == 
                                             (0x000fffffffffffffULL 
                                              & (((QData)((IData)(milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__10__KET____DOT__esub_w[2U])) 
                                                  << 0x00000033U) 
                                                 | (((QData)((IData)(milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__10__KET____DOT__esub_w[1U])) 
                                                     << 0x00000013U) 
                                                    | ((QData)((IData)(milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__10__KET____DOT__esub_w[0U])) 
                                                       >> 0x0000000dU))))) 
                                            & ((0x00001fffU 
                                                & milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__10__KET____DOT__esub_w[0U]) 
                                               < (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__nv_r))) 
                                           << 1U))) 
                                      | (((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__valid_r) 
                                          >> 9U) & 
                                         ((0ULL == 
                                           (0x000fffffffffffffULL 
                                            & (((QData)((IData)(milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__9__KET____DOT__esub_w[2U])) 
                                                << 0x00000033U) 
                                               | (((QData)((IData)(milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__9__KET____DOT__esub_w[1U])) 
                                                   << 0x00000013U) 
                                                  | ((QData)((IData)(milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__9__KET____DOT__esub_w[0U])) 
                                                     >> 0x0000000dU))))) 
                                          & ((0x00001fffU 
                                              & milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__9__KET____DOT__esub_w[0U]) 
                                             < (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__nv_r))))) 
                                     << 2U) | ((0x01fffffeU 
                                                & (((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__valid_r) 
                                                    >> 7U) 
                                                   & (((0ULL 
                                                        == 
                                                        (0x000fffffffffffffULL 
                                                         & (((QData)((IData)(milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__8__KET____DOT__esub_w[2U])) 
                                                             << 0x00000033U) 
                                                            | (((QData)((IData)(milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__8__KET____DOT__esub_w[1U])) 
                                                                << 0x00000013U) 
                                                               | ((QData)((IData)(milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__8__KET____DOT__esub_w[0U])) 
                                                                  >> 0x0000000dU))))) 
                                                       & ((0x00001fffU 
                                                           & milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__8__KET____DOT__esub_w[0U]) 
                                                          < (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__nv_r))) 
                                                      << 1U))) 
                                               | (((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__valid_r) 
                                                   >> 7U) 
                                                  & ((0ULL 
                                                      == 
                                                      (0x000fffffffffffffULL 
                                                       & (((QData)((IData)(milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__7__KET____DOT__esub_w[2U])) 
                                                           << 0x00000033U) 
                                                          | (((QData)((IData)(milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__7__KET____DOT__esub_w[1U])) 
                                                              << 0x00000013U) 
                                                             | ((QData)((IData)(milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__7__KET____DOT__esub_w[0U])) 
                                                                >> 0x0000000dU))))) 
                                                     & ((0x00001fffU 
                                                         & milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__7__KET____DOT__esub_w[0U]) 
                                                        < (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__nv_r))))))) 
            << 7U) | (((((0x07fffffeU & (((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__valid_r) 
                                          >> 5U) & 
                                         (((0ULL == 
                                            (0x000fffffffffffffULL 
                                             & (((QData)((IData)(milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__6__KET____DOT__esub_w[2U])) 
                                                 << 0x00000033U) 
                                                | (((QData)((IData)(milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__6__KET____DOT__esub_w[1U])) 
                                                    << 0x00000013U) 
                                                   | ((QData)((IData)(milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__6__KET____DOT__esub_w[0U])) 
                                                      >> 0x0000000dU))))) 
                                           & ((0x00001fffU 
                                               & milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__6__KET____DOT__esub_w[0U]) 
                                              < (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__nv_r))) 
                                          << 1U))) 
                         | (((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__valid_r) 
                             >> 5U) & ((0ULL == (0x000fffffffffffffULL 
                                                 & (((QData)((IData)(milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__5__KET____DOT__esub_w[2U])) 
                                                     << 0x00000033U) 
                                                    | (((QData)((IData)(milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__5__KET____DOT__esub_w[1U])) 
                                                        << 0x00000013U) 
                                                       | ((QData)((IData)(milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__5__KET____DOT__esub_w[0U])) 
                                                          >> 0x0000000dU))))) 
                                       & ((0x00001fffU 
                                           & milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__5__KET____DOT__esub_w[0U]) 
                                          < (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__nv_r))))) 
                        << 5U) | (((0x1ffffffeU & (
                                                   ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__valid_r) 
                                                    >> 3U) 
                                                   & (((0ULL 
                                                        == 
                                                        (0x000fffffffffffffULL 
                                                         & (((QData)((IData)(milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__4__KET____DOT__esub_w[2U])) 
                                                             << 0x00000033U) 
                                                            | (((QData)((IData)(milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__4__KET____DOT__esub_w[1U])) 
                                                                << 0x00000013U) 
                                                               | ((QData)((IData)(milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__4__KET____DOT__esub_w[0U])) 
                                                                  >> 0x0000000dU))))) 
                                                       & ((0x00001fffU 
                                                           & milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__4__KET____DOT__esub_w[0U]) 
                                                          < (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__nv_r))) 
                                                      << 1U))) 
                                   | (((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__valid_r) 
                                       >> 3U) & ((0ULL 
                                                  == 
                                                  (0x000fffffffffffffULL 
                                                   & (((QData)((IData)(milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__3__KET____DOT__esub_w[2U])) 
                                                       << 0x00000033U) 
                                                      | (((QData)((IData)(milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__3__KET____DOT__esub_w[1U])) 
                                                          << 0x00000013U) 
                                                         | ((QData)((IData)(milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__3__KET____DOT__esub_w[0U])) 
                                                            >> 0x0000000dU))))) 
                                                 & ((0x00001fffU 
                                                     & milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__3__KET____DOT__esub_w[0U]) 
                                                    < (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__nv_r))))) 
                                  << 3U)) | ((0xfffffffcU 
                                              & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__valid_r) 
                                                 & (((0ULL 
                                                      == 
                                                      (0x000fffffffffffffULL 
                                                       & (((QData)((IData)(milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__2__KET____DOT__esub_w[2U])) 
                                                           << 0x00000033U) 
                                                          | (((QData)((IData)(milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__2__KET____DOT__esub_w[1U])) 
                                                              << 0x00000013U) 
                                                             | ((QData)((IData)(milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__2__KET____DOT__esub_w[0U])) 
                                                                >> 0x0000000dU))))) 
                                                     & ((0x00001fffU 
                                                         & milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__2__KET____DOT__esub_w[0U]) 
                                                        < (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__nv_r))) 
                                                    << 2U))) 
                                             | ((0xfffffffeU 
                                                 & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__valid_r) 
                                                    & (((0ULL 
                                                         == 
                                                         (0x000fffffffffffffULL 
                                                          & (((QData)((IData)(milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__1__KET____DOT__esub_w[2U])) 
                                                              << 0x00000033U) 
                                                             | (((QData)((IData)(milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__1__KET____DOT__esub_w[1U])) 
                                                                 << 0x00000013U) 
                                                                | ((QData)((IData)(milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__1__KET____DOT__esub_w[0U])) 
                                                                   >> 0x0000000dU))))) 
                                                        & ((0x00001fffU 
                                                            & milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__1__KET____DOT__esub_w[0U]) 
                                                           < (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__nv_r))) 
                                                       << 1U))) 
                                                | ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__ctx__DOT__valid_r) 
                                                   & ((0ULL 
                                                       == 
                                                       (0x000fffffffffffffULL 
                                                        & (((QData)((IData)(milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__0__KET____DOT__esub_w[2U])) 
                                                            << 0x00000033U) 
                                                           | (((QData)((IData)(milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__0__KET____DOT__esub_w[1U])) 
                                                               << 0x00000013U) 
                                                              | ((QData)((IData)(milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__0__KET____DOT__esub_w[0U])) 
                                                                 >> 0x0000000dU))))) 
                                                      & ((0x00001fffU 
                                                          & milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__g_extmatch__BRA__0__KET____DOT__esub_w[0U]) 
                                                         < (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__walker__DOT__nv_r))))))));
    vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__fit_w 
        = ((vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__cand_w 
            <= ((IData)(vlSelfRef.o_mac_is_1g) ? 0x2cb41780U
                 : 0x047868c0U)) & (IData)(__VdfgRegularize_h6e95ff9d_0_88));
    __VdfgRegularize_h6e95ff9d_0_24 = (((((4U & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp_stream_gate) 
                                                 << 2U)) 
                                          | (((IData)(vlSelfRef.milan_datapath__DOT__lwsrp_over_limit) 
                                              << 1U) 
                                             | (1U 
                                                & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__active_w)))) 
                                         << 6U) | (
                                                   ((2U 
                                                     & ((~ (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__rx__DOT__registrar__DOT__boundary_r)) 
                                                        << 1U)) 
                                                    | (IData)(vlSelfRef.milan_datapath__DOT__lwsrp_talker_declared)) 
                                                   << 4U)) 
                                       | (((IData)(vlSelfRef.milan_datapath__DOT__lwsrp_listener_ready) 
                                           << 3U) | 
                                          (((IData)(vlSelfRef.milan_datapath__DOT__lwsrp_listener_reg) 
                                            << 2U) 
                                           | (IData)(vlSelfRef.milan_datapath__DOT__lwsrp_listener_decl))));
    vlSelfRef.milan_datapath__DOT__acmp_lobs_v_w = 
        ((0x00000100U & ((vlSelfRef.milan_datapath__DOT__csr__DOT__acmp_lobs 
                          | (((IData)(vlSelfRef.milan_datapath__DOT__lwsrp_stream_gate) 
                              >> 8U) & vlSelfRef.milan_datapath__DOT__csr__DOT__lwsrp_ctrl)) 
                         << 8U)) | (IData)(vlSelfRef.milan_datapath__DOT____Vcellinp__csr__i_tlk_lobs_v));
    vlSelfRef.milan_datapath__DOT__crf_tx__DOT__pdu[0U] = 4U;
    vlSelfRef.milan_datapath__DOT__crf_tx__DOT__pdu[1U] 
        = (0x00000080U | (IData)(vlSelfRef.milan_datapath__DOT__crf_tx__DOT__tu_r));
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
    milan_datapath__DOT__aaf_packetizer__DOT__frame_bytes__DOT__unnamedblk5__DOT__k = 0U;
    while ((0x000000f0U > milan_datapath__DOT__aaf_packetizer__DOT__frame_bytes__DOT__unnamedblk5__DOT__k)) {
        if (VL_LIKELY(((0xefU >= (0x000000ffU & milan_datapath__DOT__aaf_packetizer__DOT__frame_bytes__DOT__unnamedblk5__DOT__k))))) {
            vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[(0x000000ffU 
                                                                    & milan_datapath__DOT__aaf_packetizer__DOT__frame_bytes__DOT__unnamedblk5__DOT__k)] = 0U;
        }
        milan_datapath__DOT__aaf_packetizer__DOT__frame_bytes__DOT__unnamedblk5__DOT__k 
            = ((IData)(1U) + milan_datapath__DOT__aaf_packetizer__DOT__frame_bytes__DOT__unnamedblk5__DOT__k);
    }
    vlSelfRef.milan_datapath__DOT__i2s_feed_mux__DOT__feed_p_w 
        = ((1U & vlSelfRef.milan_datapath__DOT__csr__DOT__chmap_ctrl)
            ? (IData)(vlSelfRef.milan_datapath__DOT__chmap_phys_v_w)
            : (IData)(vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__beat_acc));
    vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[0U] 
        = (0x000000ffU & (IData)((milan_datapath__DOT__aaf_packetizer__DOT__eff_dmac_w 
                                  >> 0x00000028U)));
    vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[1U] 
        = (0x000000ffU & (IData)((milan_datapath__DOT__aaf_packetizer__DOT__eff_dmac_w 
                                  >> 0x00000020U)));
    vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[2U] 
        = (0x000000ffU & (IData)((milan_datapath__DOT__aaf_packetizer__DOT__eff_dmac_w 
                                  >> 0x00000018U)));
    vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[3U] 
        = (0x000000ffU & (IData)((milan_datapath__DOT__aaf_packetizer__DOT__eff_dmac_w 
                                  >> 0x00000010U)));
    vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[4U] 
        = (0x000000ffU & (IData)((milan_datapath__DOT__aaf_packetizer__DOT__eff_dmac_w 
                                  >> 8U)));
    vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[5U] 
        = (0x000000ffU & (IData)(milan_datapath__DOT__aaf_packetizer__DOT__eff_dmac_w));
    vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[6U] 
        = (0x000000ffU & (IData)((vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w 
                                  >> 0x00000028U)));
    vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[7U] 
        = (0x000000ffU & (IData)((vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w 
                                  >> 0x00000020U)));
    vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[8U] 
        = (0x000000ffU & (IData)((vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w 
                                  >> 0x00000018U)));
    vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[9U] 
        = (0x000000ffU & (IData)((vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w 
                                  >> 0x00000010U)));
    vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[10U] 
        = (0x000000ffU & (IData)((vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w 
                                  >> 8U)));
    vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[11U] 
        = (0x000000ffU & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w));
    vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[12U] = 0x81U;
    vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[13U] = 0U;
    vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[14U] 
        = (0x00000060U | (0x0000000fU & ((IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__eff_vid_w) 
                                         >> 8U)));
    vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[15U] 
        = (0x000000ffU & (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__eff_vid_w));
    vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[16U] = 0x22U;
    vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[17U] = 0xf0U;
    vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[18U] = 2U;
    vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[19U] = 0x81U;
    vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[20U] 
        = vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__eseq_r;
    vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[21U] 
        = vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__etu_r;
    vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[22U] 
        = (0x000000ffU & (IData)((milan_datapath__DOT__aaf_packetizer__DOT__stream_id_w 
                                  >> 0x00000038U)));
    vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[23U] 
        = (0x000000ffU & (IData)((milan_datapath__DOT__aaf_packetizer__DOT__stream_id_w 
                                  >> 0x00000030U)));
    vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[24U] 
        = (0x000000ffU & (IData)((milan_datapath__DOT__aaf_packetizer__DOT__stream_id_w 
                                  >> 0x00000028U)));
    vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[25U] 
        = (0x000000ffU & (IData)((milan_datapath__DOT__aaf_packetizer__DOT__stream_id_w 
                                  >> 0x00000020U)));
    vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[26U] 
        = (0x000000ffU & (IData)((milan_datapath__DOT__aaf_packetizer__DOT__stream_id_w 
                                  >> 0x00000018U)));
    vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[27U] 
        = (0x000000ffU & (IData)((milan_datapath__DOT__aaf_packetizer__DOT__stream_id_w 
                                  >> 0x00000010U)));
    vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[28U] 
        = (0x000000ffU & (IData)((milan_datapath__DOT__aaf_packetizer__DOT__stream_id_w 
                                  >> 8U)));
    vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[29U] 
        = (0x000000ffU & (IData)(milan_datapath__DOT__aaf_packetizer__DOT__stream_id_w));
    vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[30U] 
        = (vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__ets_r 
           >> 0x00000018U);
    vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[31U] 
        = (0x000000ffU & (vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__ets_r 
                          >> 0x00000010U));
    vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[32U] 
        = (0x000000ffU & (vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__ets_r 
                          >> 8U));
    vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[33U] 
        = (0x000000ffU & vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__ets_r);
    vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[34U] = 2U;
    vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[35U] = 0x50U;
    vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[36U] 
        = vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__chans_r
        [vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__et_r];
    vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[37U] = 0x20U;
    vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[38U] = 0U;
    vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[39U] 
        = (0x000000f8U & (((IData)(6U) * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_68)) 
                          << 3U));
    vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[40U] = 0U;
    vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[41U] = 0U;
    if ((0U < (0x0000001fU & ((IData)(6U) * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_68))))) {
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[42U] 
            = (0x000000ffU & (vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_l_r[0U] 
                              >> 0x10U));
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[43U] 
            = (0x000000ffU & (vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_l_r[0U] 
                              >> 8U));
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[44U] 
            = (0x000000ffU & vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_l_r[0U]);
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[45U] = 0U;
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[46U] 
            = (0x000000ffU & (vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_r_r[0U] 
                              >> 0x10U));
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[47U] 
            = (0x000000ffU & (vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_r_r[0U] 
                              >> 8U));
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[48U] 
            = (0x000000ffU & vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_r_r[0U]);
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[49U] = 0U;
    }
    if ((1U < (0x0000001fU & ((IData)(6U) * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_68))))) {
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[50U] 
            = (0x000000ffU & (vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_l_r[1U] 
                              >> 0x10U));
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[51U] 
            = (0x000000ffU & (vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_l_r[1U] 
                              >> 8U));
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[52U] 
            = (0x000000ffU & vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_l_r[1U]);
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[53U] = 0U;
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[54U] 
            = (0x000000ffU & (vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_r_r[1U] 
                              >> 0x10U));
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[55U] 
            = (0x000000ffU & (vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_r_r[1U] 
                              >> 8U));
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[56U] 
            = (0x000000ffU & vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_r_r[1U]);
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[57U] = 0U;
    }
    if ((2U < (0x0000001fU & ((IData)(6U) * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_68))))) {
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[58U] 
            = (0x000000ffU & (vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_l_r[2U] 
                              >> 0x10U));
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[59U] 
            = (0x000000ffU & (vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_l_r[2U] 
                              >> 8U));
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[60U] 
            = (0x000000ffU & vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_l_r[2U]);
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[61U] = 0U;
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[62U] 
            = (0x000000ffU & (vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_r_r[2U] 
                              >> 0x10U));
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[63U] 
            = (0x000000ffU & (vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_r_r[2U] 
                              >> 8U));
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[64U] 
            = (0x000000ffU & vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_r_r[2U]);
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[65U] = 0U;
    }
    if ((3U < (0x0000001fU & ((IData)(6U) * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_68))))) {
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[66U] 
            = (0x000000ffU & (vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_l_r[3U] 
                              >> 0x10U));
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[67U] 
            = (0x000000ffU & (vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_l_r[3U] 
                              >> 8U));
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[68U] 
            = (0x000000ffU & vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_l_r[3U]);
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[69U] = 0U;
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[70U] 
            = (0x000000ffU & (vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_r_r[3U] 
                              >> 0x10U));
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[71U] 
            = (0x000000ffU & (vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_r_r[3U] 
                              >> 8U));
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[72U] 
            = (0x000000ffU & vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_r_r[3U]);
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[73U] = 0U;
    }
    if ((4U < (0x0000001fU & ((IData)(6U) * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_68))))) {
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[74U] 
            = (0x000000ffU & (vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_l_r[4U] 
                              >> 0x10U));
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[75U] 
            = (0x000000ffU & (vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_l_r[4U] 
                              >> 8U));
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[76U] 
            = (0x000000ffU & vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_l_r[4U]);
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[77U] = 0U;
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[78U] 
            = (0x000000ffU & (vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_r_r[4U] 
                              >> 0x10U));
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[79U] 
            = (0x000000ffU & (vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_r_r[4U] 
                              >> 8U));
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[80U] 
            = (0x000000ffU & vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_r_r[4U]);
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[81U] = 0U;
    }
    if ((5U < (0x0000001fU & ((IData)(6U) * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_68))))) {
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[82U] 
            = (0x000000ffU & (vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_l_r[5U] 
                              >> 0x10U));
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[83U] 
            = (0x000000ffU & (vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_l_r[5U] 
                              >> 8U));
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[84U] 
            = (0x000000ffU & vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_l_r[5U]);
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[85U] = 0U;
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[86U] 
            = (0x000000ffU & (vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_r_r[5U] 
                              >> 0x10U));
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[87U] 
            = (0x000000ffU & (vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_r_r[5U] 
                              >> 8U));
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[88U] 
            = (0x000000ffU & vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_r_r[5U]);
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[89U] = 0U;
    }
    if ((6U < (0x0000001fU & ((IData)(6U) * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_68))))) {
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[90U] 
            = (0x000000ffU & (vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_l_r[6U] 
                              >> 0x10U));
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[91U] 
            = (0x000000ffU & (vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_l_r[6U] 
                              >> 8U));
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[92U] 
            = (0x000000ffU & vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_l_r[6U]);
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[93U] = 0U;
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[94U] 
            = (0x000000ffU & (vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_r_r[6U] 
                              >> 0x10U));
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[95U] 
            = (0x000000ffU & (vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_r_r[6U] 
                              >> 8U));
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[96U] 
            = (0x000000ffU & vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_r_r[6U]);
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[97U] = 0U;
    }
    if ((7U < (0x0000001fU & ((IData)(6U) * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_68))))) {
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[98U] 
            = (0x000000ffU & (vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_l_r[7U] 
                              >> 0x10U));
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[99U] 
            = (0x000000ffU & (vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_l_r[7U] 
                              >> 8U));
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[100U] 
            = (0x000000ffU & vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_l_r[7U]);
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[101U] = 0U;
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[102U] 
            = (0x000000ffU & (vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_r_r[7U] 
                              >> 0x10U));
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[103U] 
            = (0x000000ffU & (vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_r_r[7U] 
                              >> 8U));
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[104U] 
            = (0x000000ffU & vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_r_r[7U]);
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[105U] = 0U;
    }
    if ((8U < (0x0000001fU & ((IData)(6U) * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_68))))) {
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[106U] 
            = (0x000000ffU & (vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_l_r[8U] 
                              >> 0x10U));
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[107U] 
            = (0x000000ffU & (vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_l_r[8U] 
                              >> 8U));
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[108U] 
            = (0x000000ffU & vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_l_r[8U]);
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[109U] = 0U;
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[110U] 
            = (0x000000ffU & (vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_r_r[8U] 
                              >> 0x10U));
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[111U] 
            = (0x000000ffU & (vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_r_r[8U] 
                              >> 8U));
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[112U] 
            = (0x000000ffU & vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_r_r[8U]);
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[113U] = 0U;
    }
    if ((9U < (0x0000001fU & ((IData)(6U) * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_68))))) {
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[114U] 
            = (0x000000ffU & (vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_l_r[9U] 
                              >> 0x10U));
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[115U] 
            = (0x000000ffU & (vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_l_r[9U] 
                              >> 8U));
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[116U] 
            = (0x000000ffU & vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_l_r[9U]);
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[117U] = 0U;
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[118U] 
            = (0x000000ffU & (vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_r_r[9U] 
                              >> 0x10U));
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[119U] 
            = (0x000000ffU & (vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_r_r[9U] 
                              >> 8U));
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[120U] 
            = (0x000000ffU & vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_r_r[9U]);
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[121U] = 0U;
    }
    if ((0x0aU < (0x0000001fU & ((IData)(6U) * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_68))))) {
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[122U] 
            = (0x000000ffU & (vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_l_r[10U] 
                              >> 0x10U));
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[123U] 
            = (0x000000ffU & (vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_l_r[10U] 
                              >> 8U));
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[124U] 
            = (0x000000ffU & vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_l_r[10U]);
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[125U] = 0U;
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[126U] 
            = (0x000000ffU & (vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_r_r[10U] 
                              >> 0x10U));
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[127U] 
            = (0x000000ffU & (vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_r_r[10U] 
                              >> 8U));
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[128U] 
            = (0x000000ffU & vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_r_r[10U]);
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[129U] = 0U;
    }
    if ((0x0bU < (0x0000001fU & ((IData)(6U) * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_68))))) {
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[130U] 
            = (0x000000ffU & (vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_l_r[11U] 
                              >> 0x10U));
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[131U] 
            = (0x000000ffU & (vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_l_r[11U] 
                              >> 8U));
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[132U] 
            = (0x000000ffU & vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_l_r[11U]);
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[133U] = 0U;
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[134U] 
            = (0x000000ffU & (vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_r_r[11U] 
                              >> 0x10U));
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[135U] 
            = (0x000000ffU & (vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_r_r[11U] 
                              >> 8U));
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[136U] 
            = (0x000000ffU & vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_r_r[11U]);
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[137U] = 0U;
    }
    if ((0x0cU < (0x0000001fU & ((IData)(6U) * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_68))))) {
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[138U] 
            = (0x000000ffU & (vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_l_r[12U] 
                              >> 0x10U));
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[139U] 
            = (0x000000ffU & (vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_l_r[12U] 
                              >> 8U));
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[140U] 
            = (0x000000ffU & vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_l_r[12U]);
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[141U] = 0U;
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[142U] 
            = (0x000000ffU & (vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_r_r[12U] 
                              >> 0x10U));
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[143U] 
            = (0x000000ffU & (vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_r_r[12U] 
                              >> 8U));
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[144U] 
            = (0x000000ffU & vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_r_r[12U]);
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[145U] = 0U;
    }
    if ((0x0dU < (0x0000001fU & ((IData)(6U) * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_68))))) {
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[146U] 
            = (0x000000ffU & (vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_l_r[13U] 
                              >> 0x10U));
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[147U] 
            = (0x000000ffU & (vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_l_r[13U] 
                              >> 8U));
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[148U] 
            = (0x000000ffU & vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_l_r[13U]);
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[149U] = 0U;
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[150U] 
            = (0x000000ffU & (vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_r_r[13U] 
                              >> 0x10U));
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[151U] 
            = (0x000000ffU & (vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_r_r[13U] 
                              >> 8U));
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[152U] 
            = (0x000000ffU & vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_r_r[13U]);
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[153U] = 0U;
    }
    if ((0x0eU < (0x0000001fU & ((IData)(6U) * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_68))))) {
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[154U] 
            = (0x000000ffU & (vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_l_r[14U] 
                              >> 0x10U));
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[155U] 
            = (0x000000ffU & (vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_l_r[14U] 
                              >> 8U));
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[156U] 
            = (0x000000ffU & vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_l_r[14U]);
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[157U] = 0U;
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[158U] 
            = (0x000000ffU & (vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_r_r[14U] 
                              >> 0x10U));
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[159U] 
            = (0x000000ffU & (vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_r_r[14U] 
                              >> 8U));
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[160U] 
            = (0x000000ffU & vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_r_r[14U]);
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[161U] = 0U;
    }
    if ((0x0fU < (0x0000001fU & ((IData)(6U) * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_68))))) {
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[162U] 
            = (0x000000ffU & (vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_l_r[15U] 
                              >> 0x10U));
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[163U] 
            = (0x000000ffU & (vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_l_r[15U] 
                              >> 8U));
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[164U] 
            = (0x000000ffU & vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_l_r[15U]);
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[165U] = 0U;
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[166U] 
            = (0x000000ffU & (vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_r_r[15U] 
                              >> 0x10U));
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[167U] 
            = (0x000000ffU & (vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_r_r[15U] 
                              >> 8U));
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[168U] 
            = (0x000000ffU & vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_r_r[15U]);
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[169U] = 0U;
    }
    if ((0x10U < (0x0000001fU & ((IData)(6U) * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_68))))) {
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[170U] 
            = (0x000000ffU & (vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_l_r[16U] 
                              >> 0x10U));
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[171U] 
            = (0x000000ffU & (vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_l_r[16U] 
                              >> 8U));
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[172U] 
            = (0x000000ffU & vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_l_r[16U]);
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[173U] = 0U;
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[174U] 
            = (0x000000ffU & (vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_r_r[16U] 
                              >> 0x10U));
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[175U] 
            = (0x000000ffU & (vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_r_r[16U] 
                              >> 8U));
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[176U] 
            = (0x000000ffU & vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_r_r[16U]);
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[177U] = 0U;
    }
    if ((0x11U < (0x0000001fU & ((IData)(6U) * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_68))))) {
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[178U] 
            = (0x000000ffU & (vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_l_r[17U] 
                              >> 0x10U));
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[179U] 
            = (0x000000ffU & (vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_l_r[17U] 
                              >> 8U));
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[180U] 
            = (0x000000ffU & vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_l_r[17U]);
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[181U] = 0U;
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[182U] 
            = (0x000000ffU & (vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_r_r[17U] 
                              >> 0x10U));
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[183U] 
            = (0x000000ffU & (vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_r_r[17U] 
                              >> 8U));
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[184U] 
            = (0x000000ffU & vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_r_r[17U]);
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[185U] = 0U;
    }
    if ((0x12U < (0x0000001fU & ((IData)(6U) * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_68))))) {
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[186U] 
            = (0x000000ffU & (vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_l_r[18U] 
                              >> 0x10U));
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[187U] 
            = (0x000000ffU & (vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_l_r[18U] 
                              >> 8U));
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[188U] 
            = (0x000000ffU & vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_l_r[18U]);
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[189U] = 0U;
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[190U] 
            = (0x000000ffU & (vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_r_r[18U] 
                              >> 0x10U));
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[191U] 
            = (0x000000ffU & (vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_r_r[18U] 
                              >> 8U));
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[192U] 
            = (0x000000ffU & vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_r_r[18U]);
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[193U] = 0U;
    }
    if ((0x13U < (0x0000001fU & ((IData)(6U) * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_68))))) {
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[194U] 
            = (0x000000ffU & (vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_l_r[19U] 
                              >> 0x10U));
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[195U] 
            = (0x000000ffU & (vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_l_r[19U] 
                              >> 8U));
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[196U] 
            = (0x000000ffU & vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_l_r[19U]);
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[197U] = 0U;
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[198U] 
            = (0x000000ffU & (vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_r_r[19U] 
                              >> 0x10U));
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[199U] 
            = (0x000000ffU & (vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_r_r[19U] 
                              >> 8U));
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[200U] 
            = (0x000000ffU & vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_r_r[19U]);
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[201U] = 0U;
    }
    if ((0x14U < (0x0000001fU & ((IData)(6U) * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_68))))) {
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[202U] 
            = (0x000000ffU & (vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_l_r[20U] 
                              >> 0x10U));
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[203U] 
            = (0x000000ffU & (vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_l_r[20U] 
                              >> 8U));
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[204U] 
            = (0x000000ffU & vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_l_r[20U]);
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[205U] = 0U;
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[206U] 
            = (0x000000ffU & (vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_r_r[20U] 
                              >> 0x10U));
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[207U] 
            = (0x000000ffU & (vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_r_r[20U] 
                              >> 8U));
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[208U] 
            = (0x000000ffU & vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_r_r[20U]);
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[209U] = 0U;
    }
    if ((0x15U < (0x0000001fU & ((IData)(6U) * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_68))))) {
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[210U] 
            = (0x000000ffU & (vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_l_r[21U] 
                              >> 0x10U));
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[211U] 
            = (0x000000ffU & (vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_l_r[21U] 
                              >> 8U));
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[212U] 
            = (0x000000ffU & vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_l_r[21U]);
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[213U] = 0U;
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[214U] 
            = (0x000000ffU & (vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_r_r[21U] 
                              >> 0x10U));
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[215U] 
            = (0x000000ffU & (vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_r_r[21U] 
                              >> 8U));
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[216U] 
            = (0x000000ffU & vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_r_r[21U]);
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[217U] = 0U;
    }
    if ((0x16U < (0x0000001fU & ((IData)(6U) * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_68))))) {
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[218U] 
            = (0x000000ffU & (vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_l_r[22U] 
                              >> 0x10U));
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[219U] 
            = (0x000000ffU & (vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_l_r[22U] 
                              >> 8U));
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[220U] 
            = (0x000000ffU & vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_l_r[22U]);
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[221U] = 0U;
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[222U] 
            = (0x000000ffU & (vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_r_r[22U] 
                              >> 0x10U));
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[223U] 
            = (0x000000ffU & (vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_r_r[22U] 
                              >> 8U));
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[224U] 
            = (0x000000ffU & vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_r_r[22U]);
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[225U] = 0U;
    }
    if ((0x17U < (0x0000001fU & ((IData)(6U) * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_68))))) {
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[226U] 
            = (0x000000ffU & (vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_l_r[23U] 
                              >> 0x10U));
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[227U] 
            = (0x000000ffU & (vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_l_r[23U] 
                              >> 8U));
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[228U] 
            = (0x000000ffU & vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_l_r[23U]);
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[229U] = 0U;
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[230U] 
            = (0x000000ffU & (vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_r_r[23U] 
                              >> 0x10U));
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[231U] 
            = (0x000000ffU & (vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_r_r[23U] 
                              >> 8U));
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[232U] 
            = (0x000000ffU & vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__buf_r_r[23U]);
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[233U] = 0U;
    }
    if ((3U == (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__st_r))) {
        vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b 
            = ((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__beat_r) 
               << 3U);
        vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT____VlemCall_4__probe_byte 
            = (0x000000ffU & (((((((((0U == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                     | (1U == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                    | (2U == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                   | (3U == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                  | (6U == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                 | (7U == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                | (8U == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                               | (9U == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b))
                               ? ((0U == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                   ? 0x91U : ((1U == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                               ? 0xe0U
                                               : ((2U 
                                                   == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                                   ? 0xf0U
                                                   : 
                                                  ((3U 
                                                    == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                                    ? 1U
                                                    : 
                                                   ((6U 
                                                     == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                                     ? (IData)(
                                                               (vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w 
                                                                >> 0x28U))
                                                     : 
                                                    ((7U 
                                                      == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                                      ? (IData)(
                                                                (vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w 
                                                                 >> 0x20U))
                                                      : 
                                                     ((8U 
                                                       == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                                       ? (IData)(
                                                                 (vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w 
                                                                  >> 0x18U))
                                                       : (IData)(
                                                                 (vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w 
                                                                  >> 0x10U)))))))))
                               : (((((((((0x0000000aU 
                                          == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                         | (0x0000000bU 
                                            == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                        | (0x0000000cU 
                                           == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                       | (0x0000000dU 
                                          == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                      | (0x0000000eU 
                                         == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                     | (0x0000000fU 
                                        == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                    | (0x00000010U 
                                       == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                   | (0x00000011U == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b))
                                   ? ((0x0000000aU 
                                       == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                       ? (IData)((vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w 
                                                  >> 8U))
                                       : ((0x0000000bU 
                                           == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                           ? (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w)
                                           : ((0x0000000cU 
                                               == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                               ? 0x22U
                                               : ((0x0000000dU 
                                                   == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                                   ? 0xf0U
                                                   : 
                                                  ((0x0000000eU 
                                                    == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                                    ? 0xfcU
                                                    : 
                                                   ((0x0000000fU 
                                                     == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                                     ? 0U
                                                     : 
                                                    ((0x00000010U 
                                                      == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                                      ? 0U
                                                      : 0x2cU)))))))
                                   : ((((((((((((((
                                                   ((0x0000001aU 
                                                     == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                    || (0x0000001bU 
                                                        == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                   || (0x0000001cU 
                                                       == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                  || (0x0000001dU 
                                                      == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                 || (0x0000001eU 
                                                     == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                || (0x0000001fU 
                                                    == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                               || (0x00000020U 
                                                   == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                              || (0x00000021U 
                                                  == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                             | ((((((((0x00000022U 
                                                       == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                      || (0x00000023U 
                                                          == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                     || (0x00000024U 
                                                         == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                    || (0x00000025U 
                                                        == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                   || (0x00000026U 
                                                       == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                  || (0x00000027U 
                                                      == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                 || (0x00000028U 
                                                     == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                || (0x00000029U 
                                                    == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b))) 
                                            | ((((((((0x0000002aU 
                                                      == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                     || (0x0000002bU 
                                                         == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                    || (0x0000002cU 
                                                        == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                   || (0x0000002dU 
                                                       == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                  || (0x0000002eU 
                                                      == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                 || (0x0000002fU 
                                                     == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                || (0x00000030U 
                                                    == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                               || (0x00000031U 
                                                   == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b))) 
                                           | (0x00000032U 
                                              == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                          | (0x00000033U 
                                             == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                         | (0x00000034U 
                                            == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                        | (0x00000035U 
                                           == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                       | (0x0000003eU 
                                          == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b))
                                       ? (((((((((0x0000001aU 
                                                  == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                 || (0x0000001bU 
                                                     == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                || (0x0000001cU 
                                                    == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                               || (0x0000001dU 
                                                   == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                              || (0x0000001eU 
                                                  == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                             || (0x0000001fU 
                                                 == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                            || (0x00000020U 
                                                == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                           || (0x00000021U 
                                               == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b))
                                           ? (((0U 
                                                == 
                                                (0x0000001fU 
                                                 & VL_MULS_III(32, (IData)(8U), 
                                                               ((IData)(0x00000021U) 
                                                                - vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b))))
                                                ? 0U
                                                : (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r
                                                   [
                                                   (((IData)(7U) 
                                                     + 
                                                     (0x0000003fU 
                                                      & VL_MULS_III(32, (IData)(8U), 
                                                                    ((IData)(0x00000021U) 
                                                                     - vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)))) 
                                                    >> 5U)] 
                                                   << 
                                                   ((IData)(0x00000020U) 
                                                    - 
                                                    (0x0000001fU 
                                                     & VL_MULS_III(32, (IData)(8U), 
                                                                   ((IData)(0x00000021U) 
                                                                    - vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)))))) 
                                              | (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r
                                                 [(1U 
                                                   & (VL_MULS_III(32, (IData)(8U), 
                                                                  ((IData)(0x00000021U) 
                                                                   - vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                      >> 5U))] 
                                                 >> 
                                                 (0x0000001fU 
                                                  & VL_MULS_III(32, (IData)(8U), 
                                                                ((IData)(0x00000021U) 
                                                                 - vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)))))
                                           : ((((((
                                                   (((0x00000022U 
                                                      == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                     || (0x00000023U 
                                                         == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                    || (0x00000024U 
                                                        == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                   || (0x00000025U 
                                                       == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                  || (0x00000026U 
                                                      == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                 || (0x00000027U 
                                                     == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                || (0x00000028U 
                                                    == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                               || (0x00000029U 
                                                   == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b))
                                               ? ((
                                                   (0U 
                                                    == 
                                                    (0x0000001fU 
                                                     & ((IData)(0x00000040U) 
                                                        + 
                                                        (0x0000003fU 
                                                         & VL_MULS_III(32, (IData)(8U), 
                                                                       ((IData)(0x00000029U) 
                                                                        - vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b))))))
                                                    ? 0U
                                                    : 
                                                   (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r
                                                    [
                                                    (((IData)(0x00000047U) 
                                                      + 
                                                      (0x0000003fU 
                                                       & VL_MULS_III(32, (IData)(8U), 
                                                                     ((IData)(0x00000029U) 
                                                                      - vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)))) 
                                                     >> 5U)] 
                                                    << 
                                                    ((IData)(0x00000020U) 
                                                     - 
                                                     (0x0000001fU 
                                                      & ((IData)(0x00000040U) 
                                                         + 
                                                         (0x0000003fU 
                                                          & VL_MULS_III(32, (IData)(8U), 
                                                                        ((IData)(0x00000029U) 
                                                                         - vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)))))))) 
                                                  | (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r
                                                     [
                                                     (((IData)(0x00000040U) 
                                                       + 
                                                       (0x0000003fU 
                                                        & VL_MULS_III(32, (IData)(8U), 
                                                                      ((IData)(0x00000029U) 
                                                                       - vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)))) 
                                                      >> 5U)] 
                                                     >> 
                                                     (0x0000001fU 
                                                      & ((IData)(0x00000040U) 
                                                         + 
                                                         (0x0000003fU 
                                                          & VL_MULS_III(32, (IData)(8U), 
                                                                        ((IData)(0x00000029U) 
                                                                         - vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)))))))
                                               : ((
                                                   (((((((0x0000002aU 
                                                          == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                         || (0x0000002bU 
                                                             == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                        || (0x0000002cU 
                                                            == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                       || (0x0000002dU 
                                                           == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                      || (0x0000002eU 
                                                          == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                     || (0x0000002fU 
                                                         == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                    || (0x00000030U 
                                                        == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                   || (0x00000031U 
                                                       == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b))
                                                   ? (IData)(
                                                             (vlSelfRef.milan_datapath__DOT__cfg_adp_entity_id 
                                                              >> 
                                                              (0x0000003fU 
                                                               & VL_MULS_III(32, (IData)(8U), 
                                                                             ((IData)(0x00000031U) 
                                                                              - vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)))))
                                                   : 
                                                  ((0x00000032U 
                                                    == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                                    ? 
                                                   ((vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r[8U] 
                                                     << 0x0000000cU) 
                                                    | (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r[8U] 
                                                       >> 0x00000014U))
                                                    : 
                                                   ((0x00000033U 
                                                     == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                                     ? 
                                                    ((vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r[8U] 
                                                      << 0x00000014U) 
                                                     | (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r[8U] 
                                                        >> 0x0000000cU))
                                                     : 
                                                    ((0x00000034U 
                                                      == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                                      ? 0U
                                                      : 
                                                     ((0x00000035U 
                                                       == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                                       ? (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_idx_r)
                                                       : 
                                                      ((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_seq_r) 
                                                       >> 8U))))))))
                                       : ((0x0000003fU 
                                           == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                           ? (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_seq_r)
                                           : ((0x00000040U 
                                               == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                               ? ((vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r[8U] 
                                                   << 0x0000001cU) 
                                                  | (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r[8U] 
                                                     >> 4U))
                                               : ((0x00000041U 
                                                   == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                                   ? 
                                                  (0xb7U 
                                                   & ((vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r[8U] 
                                                       << 4U) 
                                                      | (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r[7U] 
                                                         >> 0x0000001cU)))
                                                   : 0U)))))));
        vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_beat 
            = ((0xffffffffffffff00ULL & vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_beat) 
               | (IData)((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT____VlemCall_4__probe_byte)));
        if ((1U & (~ VL_ONEHOT_I((((((((((0x00000041U 
                                          == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                         << 3U) | (
                                                   (0x00000040U 
                                                    == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                   << 2U)) 
                                       | (((0x0000003fU 
                                            == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                           << 1U) | 
                                          (0x0000003eU 
                                           == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b))) 
                                      << 0x0000000aU) 
                                     | (((0x00000035U 
                                          == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                         << 9U) | (
                                                   ((0x00000034U 
                                                     == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                    << 8U) 
                                                   | ((0x00000033U 
                                                       == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                      << 7U)))) 
                                    | ((((((0x00000032U 
                                            == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                           << 3U) | 
                                          (((0x00000031U 
                                             == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                            | ((0x00000030U 
                                                == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                               | ((0x0000002fU 
                                                   == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                  | ((0x0000002eU 
                                                      == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                     | ((0x0000002dU 
                                                         == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                        | ((0x0000002cU 
                                                            == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                           | ((0x0000002bU 
                                                               == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                              | (0x0000002aU 
                                                                 == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)))))))) 
                                           << 2U)) 
                                         | ((((0x00000029U 
                                               == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                              | ((0x00000028U 
                                                  == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                 | ((0x00000027U 
                                                     == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                    | ((0x00000026U 
                                                        == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                       | ((0x00000025U 
                                                           == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                          | ((0x00000024U 
                                                              == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                             | ((0x00000023U 
                                                                 == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                                | (0x00000022U 
                                                                   == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)))))))) 
                                             << 1U) 
                                            | ((0x00000021U 
                                                == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                               | ((0x00000020U 
                                                   == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                  | ((0x0000001fU 
                                                      == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                     | ((0x0000001eU 
                                                         == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                        | ((0x0000001dU 
                                                            == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                           | ((0x0000001cU 
                                                               == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                              | ((0x0000001bU 
                                                                  == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                                 | (0x0000001aU 
                                                                    == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)))))))))) 
                                        << 3U) | ((
                                                   (0x00000011U 
                                                    == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                   << 2U) 
                                                  | (((0x00000010U 
                                                       == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                      << 1U) 
                                                     | (0x0000000fU 
                                                        == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b))))) 
                                   << 0x0000000dU) 
                                  | (((((((0x0000000eU 
                                           == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                          << 3U) | 
                                         ((0x0000000dU 
                                           == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                          << 2U)) | 
                                        (((0x0000000cU 
                                           == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                          << 1U) | 
                                         (0x0000000bU 
                                          == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b))) 
                                       << 9U) | (((0x0000000aU 
                                                   == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                  << 8U) 
                                                 | (((9U 
                                                      == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                     << 7U) 
                                                    | ((8U 
                                                        == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                       << 6U)))) 
                                     | ((((7U == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                          << 5U) | 
                                         (((6U == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                           << 4U) | 
                                          ((3U == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                           << 3U))) 
                                        | (((2U == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                            << 2U) 
                                           | (((1U 
                                                == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                               << 1U) 
                                              | (0U 
                                                 == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)))))))))) {
            if ((0U != (((((((((0x00000041U == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                               << 3U) | ((0x00000040U 
                                          == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                         << 2U)) | 
                             (((0x0000003fU == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                               << 1U) | (0x0000003eU 
                                         == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b))) 
                            << 0x0000000aU) | (((0x00000035U 
                                                 == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                << 9U) 
                                               | (((0x00000034U 
                                                    == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                   << 8U) 
                                                  | ((0x00000033U 
                                                      == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                     << 7U)))) 
                          | ((((((0x00000032U == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                 << 3U) | (((0x00000031U 
                                             == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                            | ((0x00000030U 
                                                == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                               | ((0x0000002fU 
                                                   == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                  | ((0x0000002eU 
                                                      == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                     | ((0x0000002dU 
                                                         == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                        | ((0x0000002cU 
                                                            == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                           | ((0x0000002bU 
                                                               == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                              | (0x0000002aU 
                                                                 == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)))))))) 
                                           << 2U)) 
                               | ((((0x00000029U == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                    | ((0x00000028U 
                                        == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                       | ((0x00000027U 
                                           == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                          | ((0x00000026U 
                                              == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                             | ((0x00000025U 
                                                 == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                | ((0x00000024U 
                                                    == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                   | ((0x00000023U 
                                                       == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                      | (0x00000022U 
                                                         == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)))))))) 
                                   << 1U) | ((0x00000021U 
                                              == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                             | ((0x00000020U 
                                                 == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                | ((0x0000001fU 
                                                    == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                   | ((0x0000001eU 
                                                       == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                      | ((0x0000001dU 
                                                          == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                         | ((0x0000001cU 
                                                             == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                            | ((0x0000001bU 
                                                                == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                               | (0x0000001aU 
                                                                  == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)))))))))) 
                              << 3U) | (((0x00000011U 
                                          == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                         << 2U) | (
                                                   ((0x00000010U 
                                                     == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                    << 1U) 
                                                   | (0x0000000fU 
                                                      == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b))))) 
                         << 0x0000000dU) | (((((((0x0000000eU 
                                                  == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                 << 3U) 
                                                | ((0x0000000dU 
                                                    == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                   << 2U)) 
                                               | (((0x0000000cU 
                                                    == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                   << 1U) 
                                                  | (0x0000000bU 
                                                     == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b))) 
                                              << 9U) 
                                             | (((0x0000000aU 
                                                  == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                 << 8U) 
                                                | (((9U 
                                                     == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                    << 7U) 
                                                   | ((8U 
                                                       == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                      << 6U)))) 
                                            | ((((7U 
                                                  == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                 << 5U) 
                                                | (((6U 
                                                     == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                    << 4U) 
                                                   | ((3U 
                                                       == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                      << 3U))) 
                                               | (((2U 
                                                    == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                   << 2U) 
                                                  | (((1U 
                                                       == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                      << 1U) 
                                                     | (0U 
                                                        == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)))))))) {
                if (VL_UNLIKELY((vlSymsp->_vm_contextp__->assertOn()))) {
                    VL_WRITEF_NX("[%0t] %%Error: KL_acmp_lstn_ctx.sv:431: Assertion failed in %m: unique case, but multiple matches found for '32'h%X'\n",4, 'M',vlSymsp->name(),"milan_datapath.acmp_listener_sm.u_ctx.probe_byte", 'T',-9
                                 , '#',64,VL_TIME_UNITED_Q(1000)
                                 , '#',32,vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b);
                    VL_STOP_MT("../../../configs/generated/endstation_ax7101_8x8/../../../hdl/ieee17221/acmp/KL_acmp_lstn_ctx.sv", 431, "");
                }
            }
        }
        vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b 
            = ((IData)(1U) + ((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__beat_r) 
                              << 3U));
        vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT____VlemCall_4__probe_byte 
            = (0x000000ffU & (((((((((0U == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                     | (1U == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                    | (2U == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                   | (3U == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                  | (6U == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                 | (7U == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                | (8U == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                               | (9U == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b))
                               ? ((0U == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                   ? 0x91U : ((1U == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                               ? 0xe0U
                                               : ((2U 
                                                   == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                                   ? 0xf0U
                                                   : 
                                                  ((3U 
                                                    == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                                    ? 1U
                                                    : 
                                                   ((6U 
                                                     == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                                     ? (IData)(
                                                               (vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w 
                                                                >> 0x28U))
                                                     : 
                                                    ((7U 
                                                      == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                                      ? (IData)(
                                                                (vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w 
                                                                 >> 0x20U))
                                                      : 
                                                     ((8U 
                                                       == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                                       ? (IData)(
                                                                 (vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w 
                                                                  >> 0x18U))
                                                       : (IData)(
                                                                 (vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w 
                                                                  >> 0x10U)))))))))
                               : (((((((((0x0000000aU 
                                          == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                         | (0x0000000bU 
                                            == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                        | (0x0000000cU 
                                           == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                       | (0x0000000dU 
                                          == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                      | (0x0000000eU 
                                         == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                     | (0x0000000fU 
                                        == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                    | (0x00000010U 
                                       == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                   | (0x00000011U == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b))
                                   ? ((0x0000000aU 
                                       == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                       ? (IData)((vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w 
                                                  >> 8U))
                                       : ((0x0000000bU 
                                           == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                           ? (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w)
                                           : ((0x0000000cU 
                                               == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                               ? 0x22U
                                               : ((0x0000000dU 
                                                   == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                                   ? 0xf0U
                                                   : 
                                                  ((0x0000000eU 
                                                    == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                                    ? 0xfcU
                                                    : 
                                                   ((0x0000000fU 
                                                     == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                                     ? 0U
                                                     : 
                                                    ((0x00000010U 
                                                      == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                                      ? 0U
                                                      : 0x2cU)))))))
                                   : ((((((((((((((
                                                   ((0x0000001aU 
                                                     == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                    || (0x0000001bU 
                                                        == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                   || (0x0000001cU 
                                                       == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                  || (0x0000001dU 
                                                      == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                 || (0x0000001eU 
                                                     == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                || (0x0000001fU 
                                                    == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                               || (0x00000020U 
                                                   == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                              || (0x00000021U 
                                                  == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                             | ((((((((0x00000022U 
                                                       == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                      || (0x00000023U 
                                                          == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                     || (0x00000024U 
                                                         == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                    || (0x00000025U 
                                                        == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                   || (0x00000026U 
                                                       == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                  || (0x00000027U 
                                                      == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                 || (0x00000028U 
                                                     == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                || (0x00000029U 
                                                    == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b))) 
                                            | ((((((((0x0000002aU 
                                                      == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                     || (0x0000002bU 
                                                         == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                    || (0x0000002cU 
                                                        == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                   || (0x0000002dU 
                                                       == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                  || (0x0000002eU 
                                                      == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                 || (0x0000002fU 
                                                     == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                || (0x00000030U 
                                                    == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                               || (0x00000031U 
                                                   == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b))) 
                                           | (0x00000032U 
                                              == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                          | (0x00000033U 
                                             == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                         | (0x00000034U 
                                            == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                        | (0x00000035U 
                                           == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                       | (0x0000003eU 
                                          == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b))
                                       ? (((((((((0x0000001aU 
                                                  == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                 || (0x0000001bU 
                                                     == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                || (0x0000001cU 
                                                    == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                               || (0x0000001dU 
                                                   == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                              || (0x0000001eU 
                                                  == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                             || (0x0000001fU 
                                                 == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                            || (0x00000020U 
                                                == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                           || (0x00000021U 
                                               == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b))
                                           ? (((0U 
                                                == 
                                                (0x0000001fU 
                                                 & VL_MULS_III(32, (IData)(8U), 
                                                               ((IData)(0x00000021U) 
                                                                - vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b))))
                                                ? 0U
                                                : (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r
                                                   [
                                                   (((IData)(7U) 
                                                     + 
                                                     (0x0000003fU 
                                                      & VL_MULS_III(32, (IData)(8U), 
                                                                    ((IData)(0x00000021U) 
                                                                     - vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)))) 
                                                    >> 5U)] 
                                                   << 
                                                   ((IData)(0x00000020U) 
                                                    - 
                                                    (0x0000001fU 
                                                     & VL_MULS_III(32, (IData)(8U), 
                                                                   ((IData)(0x00000021U) 
                                                                    - vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)))))) 
                                              | (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r
                                                 [(1U 
                                                   & (VL_MULS_III(32, (IData)(8U), 
                                                                  ((IData)(0x00000021U) 
                                                                   - vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                      >> 5U))] 
                                                 >> 
                                                 (0x0000001fU 
                                                  & VL_MULS_III(32, (IData)(8U), 
                                                                ((IData)(0x00000021U) 
                                                                 - vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)))))
                                           : ((((((
                                                   (((0x00000022U 
                                                      == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                     || (0x00000023U 
                                                         == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                    || (0x00000024U 
                                                        == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                   || (0x00000025U 
                                                       == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                  || (0x00000026U 
                                                      == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                 || (0x00000027U 
                                                     == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                || (0x00000028U 
                                                    == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                               || (0x00000029U 
                                                   == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b))
                                               ? ((
                                                   (0U 
                                                    == 
                                                    (0x0000001fU 
                                                     & ((IData)(0x00000040U) 
                                                        + 
                                                        (0x0000003fU 
                                                         & VL_MULS_III(32, (IData)(8U), 
                                                                       ((IData)(0x00000029U) 
                                                                        - vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b))))))
                                                    ? 0U
                                                    : 
                                                   (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r
                                                    [
                                                    (((IData)(0x00000047U) 
                                                      + 
                                                      (0x0000003fU 
                                                       & VL_MULS_III(32, (IData)(8U), 
                                                                     ((IData)(0x00000029U) 
                                                                      - vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)))) 
                                                     >> 5U)] 
                                                    << 
                                                    ((IData)(0x00000020U) 
                                                     - 
                                                     (0x0000001fU 
                                                      & ((IData)(0x00000040U) 
                                                         + 
                                                         (0x0000003fU 
                                                          & VL_MULS_III(32, (IData)(8U), 
                                                                        ((IData)(0x00000029U) 
                                                                         - vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)))))))) 
                                                  | (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r
                                                     [
                                                     (((IData)(0x00000040U) 
                                                       + 
                                                       (0x0000003fU 
                                                        & VL_MULS_III(32, (IData)(8U), 
                                                                      ((IData)(0x00000029U) 
                                                                       - vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)))) 
                                                      >> 5U)] 
                                                     >> 
                                                     (0x0000001fU 
                                                      & ((IData)(0x00000040U) 
                                                         + 
                                                         (0x0000003fU 
                                                          & VL_MULS_III(32, (IData)(8U), 
                                                                        ((IData)(0x00000029U) 
                                                                         - vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)))))))
                                               : ((
                                                   (((((((0x0000002aU 
                                                          == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                         || (0x0000002bU 
                                                             == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                        || (0x0000002cU 
                                                            == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                       || (0x0000002dU 
                                                           == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                      || (0x0000002eU 
                                                          == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                     || (0x0000002fU 
                                                         == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                    || (0x00000030U 
                                                        == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                   || (0x00000031U 
                                                       == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b))
                                                   ? (IData)(
                                                             (vlSelfRef.milan_datapath__DOT__cfg_adp_entity_id 
                                                              >> 
                                                              (0x0000003fU 
                                                               & VL_MULS_III(32, (IData)(8U), 
                                                                             ((IData)(0x00000031U) 
                                                                              - vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)))))
                                                   : 
                                                  ((0x00000032U 
                                                    == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                                    ? 
                                                   ((vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r[8U] 
                                                     << 0x0000000cU) 
                                                    | (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r[8U] 
                                                       >> 0x00000014U))
                                                    : 
                                                   ((0x00000033U 
                                                     == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                                     ? 
                                                    ((vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r[8U] 
                                                      << 0x00000014U) 
                                                     | (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r[8U] 
                                                        >> 0x0000000cU))
                                                     : 
                                                    ((0x00000034U 
                                                      == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                                      ? 0U
                                                      : 
                                                     ((0x00000035U 
                                                       == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                                       ? (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_idx_r)
                                                       : 
                                                      ((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_seq_r) 
                                                       >> 8U))))))))
                                       : ((0x0000003fU 
                                           == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                           ? (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_seq_r)
                                           : ((0x00000040U 
                                               == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                               ? ((vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r[8U] 
                                                   << 0x0000001cU) 
                                                  | (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r[8U] 
                                                     >> 4U))
                                               : ((0x00000041U 
                                                   == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                                   ? 
                                                  (0xb7U 
                                                   & ((vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r[8U] 
                                                       << 4U) 
                                                      | (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r[7U] 
                                                         >> 0x0000001cU)))
                                                   : 0U)))))));
        vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_beat 
            = ((0xffffffffffff00ffULL & vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_beat) 
               | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT____VlemCall_4__probe_byte)) 
                  << 8U));
        if ((1U & (~ VL_ONEHOT_I((((((((((0x00000041U 
                                          == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                         << 3U) | (
                                                   (0x00000040U 
                                                    == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                   << 2U)) 
                                       | (((0x0000003fU 
                                            == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                           << 1U) | 
                                          (0x0000003eU 
                                           == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b))) 
                                      << 0x0000000aU) 
                                     | (((0x00000035U 
                                          == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                         << 9U) | (
                                                   ((0x00000034U 
                                                     == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                    << 8U) 
                                                   | ((0x00000033U 
                                                       == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                      << 7U)))) 
                                    | ((((((0x00000032U 
                                            == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                           << 3U) | 
                                          (((0x00000031U 
                                             == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                            | ((0x00000030U 
                                                == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                               | ((0x0000002fU 
                                                   == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                  | ((0x0000002eU 
                                                      == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                     | ((0x0000002dU 
                                                         == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                        | ((0x0000002cU 
                                                            == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                           | ((0x0000002bU 
                                                               == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                              | (0x0000002aU 
                                                                 == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)))))))) 
                                           << 2U)) 
                                         | ((((0x00000029U 
                                               == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                              | ((0x00000028U 
                                                  == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                 | ((0x00000027U 
                                                     == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                    | ((0x00000026U 
                                                        == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                       | ((0x00000025U 
                                                           == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                          | ((0x00000024U 
                                                              == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                             | ((0x00000023U 
                                                                 == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                                | (0x00000022U 
                                                                   == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)))))))) 
                                             << 1U) 
                                            | ((0x00000021U 
                                                == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                               | ((0x00000020U 
                                                   == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                  | ((0x0000001fU 
                                                      == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                     | ((0x0000001eU 
                                                         == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                        | ((0x0000001dU 
                                                            == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                           | ((0x0000001cU 
                                                               == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                              | ((0x0000001bU 
                                                                  == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                                 | (0x0000001aU 
                                                                    == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)))))))))) 
                                        << 3U) | ((
                                                   (0x00000011U 
                                                    == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                   << 2U) 
                                                  | (((0x00000010U 
                                                       == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                      << 1U) 
                                                     | (0x0000000fU 
                                                        == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b))))) 
                                   << 0x0000000dU) 
                                  | (((((((0x0000000eU 
                                           == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                          << 3U) | 
                                         ((0x0000000dU 
                                           == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                          << 2U)) | 
                                        (((0x0000000cU 
                                           == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                          << 1U) | 
                                         (0x0000000bU 
                                          == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b))) 
                                       << 9U) | (((0x0000000aU 
                                                   == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                  << 8U) 
                                                 | (((9U 
                                                      == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                     << 7U) 
                                                    | ((8U 
                                                        == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                       << 6U)))) 
                                     | ((((7U == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                          << 5U) | 
                                         (((6U == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                           << 4U) | 
                                          ((3U == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                           << 3U))) 
                                        | (((2U == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                            << 2U) 
                                           | (((1U 
                                                == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                               << 1U) 
                                              | (0U 
                                                 == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)))))))))) {
            if ((0U != (((((((((0x00000041U == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                               << 3U) | ((0x00000040U 
                                          == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                         << 2U)) | 
                             (((0x0000003fU == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                               << 1U) | (0x0000003eU 
                                         == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b))) 
                            << 0x0000000aU) | (((0x00000035U 
                                                 == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                << 9U) 
                                               | (((0x00000034U 
                                                    == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                   << 8U) 
                                                  | ((0x00000033U 
                                                      == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                     << 7U)))) 
                          | ((((((0x00000032U == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                 << 3U) | (((0x00000031U 
                                             == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                            | ((0x00000030U 
                                                == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                               | ((0x0000002fU 
                                                   == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                  | ((0x0000002eU 
                                                      == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                     | ((0x0000002dU 
                                                         == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                        | ((0x0000002cU 
                                                            == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                           | ((0x0000002bU 
                                                               == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                              | (0x0000002aU 
                                                                 == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)))))))) 
                                           << 2U)) 
                               | ((((0x00000029U == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                    | ((0x00000028U 
                                        == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                       | ((0x00000027U 
                                           == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                          | ((0x00000026U 
                                              == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                             | ((0x00000025U 
                                                 == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                | ((0x00000024U 
                                                    == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                   | ((0x00000023U 
                                                       == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                      | (0x00000022U 
                                                         == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)))))))) 
                                   << 1U) | ((0x00000021U 
                                              == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                             | ((0x00000020U 
                                                 == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                | ((0x0000001fU 
                                                    == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                   | ((0x0000001eU 
                                                       == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                      | ((0x0000001dU 
                                                          == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                         | ((0x0000001cU 
                                                             == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                            | ((0x0000001bU 
                                                                == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                               | (0x0000001aU 
                                                                  == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)))))))))) 
                              << 3U) | (((0x00000011U 
                                          == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                         << 2U) | (
                                                   ((0x00000010U 
                                                     == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                    << 1U) 
                                                   | (0x0000000fU 
                                                      == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b))))) 
                         << 0x0000000dU) | (((((((0x0000000eU 
                                                  == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                 << 3U) 
                                                | ((0x0000000dU 
                                                    == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                   << 2U)) 
                                               | (((0x0000000cU 
                                                    == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                   << 1U) 
                                                  | (0x0000000bU 
                                                     == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b))) 
                                              << 9U) 
                                             | (((0x0000000aU 
                                                  == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                 << 8U) 
                                                | (((9U 
                                                     == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                    << 7U) 
                                                   | ((8U 
                                                       == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                      << 6U)))) 
                                            | ((((7U 
                                                  == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                 << 5U) 
                                                | (((6U 
                                                     == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                    << 4U) 
                                                   | ((3U 
                                                       == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                      << 3U))) 
                                               | (((2U 
                                                    == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                   << 2U) 
                                                  | (((1U 
                                                       == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                      << 1U) 
                                                     | (0U 
                                                        == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)))))))) {
                if (VL_UNLIKELY((vlSymsp->_vm_contextp__->assertOn()))) {
                    VL_WRITEF_NX("[%0t] %%Error: KL_acmp_lstn_ctx.sv:431: Assertion failed in %m: unique case, but multiple matches found for '32'h%X'\n",4, 'M',vlSymsp->name(),"milan_datapath.acmp_listener_sm.u_ctx.probe_byte", 'T',-9
                                 , '#',64,VL_TIME_UNITED_Q(1000)
                                 , '#',32,vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b);
                    VL_STOP_MT("../../../configs/generated/endstation_ax7101_8x8/../../../hdl/ieee17221/acmp/KL_acmp_lstn_ctx.sv", 431, "");
                }
            }
        }
        vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b 
            = ((IData)(2U) + ((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__beat_r) 
                              << 3U));
        vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT____VlemCall_4__probe_byte 
            = (0x000000ffU & (((((((((0U == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                     | (1U == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                    | (2U == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                   | (3U == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                  | (6U == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                 | (7U == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                | (8U == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                               | (9U == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b))
                               ? ((0U == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                   ? 0x91U : ((1U == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                               ? 0xe0U
                                               : ((2U 
                                                   == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                                   ? 0xf0U
                                                   : 
                                                  ((3U 
                                                    == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                                    ? 1U
                                                    : 
                                                   ((6U 
                                                     == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                                     ? (IData)(
                                                               (vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w 
                                                                >> 0x28U))
                                                     : 
                                                    ((7U 
                                                      == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                                      ? (IData)(
                                                                (vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w 
                                                                 >> 0x20U))
                                                      : 
                                                     ((8U 
                                                       == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                                       ? (IData)(
                                                                 (vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w 
                                                                  >> 0x18U))
                                                       : (IData)(
                                                                 (vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w 
                                                                  >> 0x10U)))))))))
                               : (((((((((0x0000000aU 
                                          == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                         | (0x0000000bU 
                                            == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                        | (0x0000000cU 
                                           == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                       | (0x0000000dU 
                                          == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                      | (0x0000000eU 
                                         == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                     | (0x0000000fU 
                                        == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                    | (0x00000010U 
                                       == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                   | (0x00000011U == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b))
                                   ? ((0x0000000aU 
                                       == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                       ? (IData)((vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w 
                                                  >> 8U))
                                       : ((0x0000000bU 
                                           == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                           ? (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w)
                                           : ((0x0000000cU 
                                               == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                               ? 0x22U
                                               : ((0x0000000dU 
                                                   == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                                   ? 0xf0U
                                                   : 
                                                  ((0x0000000eU 
                                                    == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                                    ? 0xfcU
                                                    : 
                                                   ((0x0000000fU 
                                                     == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                                     ? 0U
                                                     : 
                                                    ((0x00000010U 
                                                      == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                                      ? 0U
                                                      : 0x2cU)))))))
                                   : ((((((((((((((
                                                   ((0x0000001aU 
                                                     == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                    || (0x0000001bU 
                                                        == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                   || (0x0000001cU 
                                                       == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                  || (0x0000001dU 
                                                      == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                 || (0x0000001eU 
                                                     == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                || (0x0000001fU 
                                                    == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                               || (0x00000020U 
                                                   == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                              || (0x00000021U 
                                                  == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                             | ((((((((0x00000022U 
                                                       == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                      || (0x00000023U 
                                                          == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                     || (0x00000024U 
                                                         == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                    || (0x00000025U 
                                                        == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                   || (0x00000026U 
                                                       == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                  || (0x00000027U 
                                                      == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                 || (0x00000028U 
                                                     == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                || (0x00000029U 
                                                    == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b))) 
                                            | ((((((((0x0000002aU 
                                                      == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                     || (0x0000002bU 
                                                         == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                    || (0x0000002cU 
                                                        == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                   || (0x0000002dU 
                                                       == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                  || (0x0000002eU 
                                                      == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                 || (0x0000002fU 
                                                     == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                || (0x00000030U 
                                                    == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                               || (0x00000031U 
                                                   == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b))) 
                                           | (0x00000032U 
                                              == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                          | (0x00000033U 
                                             == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                         | (0x00000034U 
                                            == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                        | (0x00000035U 
                                           == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                       | (0x0000003eU 
                                          == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b))
                                       ? (((((((((0x0000001aU 
                                                  == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                 || (0x0000001bU 
                                                     == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                || (0x0000001cU 
                                                    == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                               || (0x0000001dU 
                                                   == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                              || (0x0000001eU 
                                                  == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                             || (0x0000001fU 
                                                 == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                            || (0x00000020U 
                                                == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                           || (0x00000021U 
                                               == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b))
                                           ? (((0U 
                                                == 
                                                (0x0000001fU 
                                                 & VL_MULS_III(32, (IData)(8U), 
                                                               ((IData)(0x00000021U) 
                                                                - vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b))))
                                                ? 0U
                                                : (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r
                                                   [
                                                   (((IData)(7U) 
                                                     + 
                                                     (0x0000003fU 
                                                      & VL_MULS_III(32, (IData)(8U), 
                                                                    ((IData)(0x00000021U) 
                                                                     - vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)))) 
                                                    >> 5U)] 
                                                   << 
                                                   ((IData)(0x00000020U) 
                                                    - 
                                                    (0x0000001fU 
                                                     & VL_MULS_III(32, (IData)(8U), 
                                                                   ((IData)(0x00000021U) 
                                                                    - vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)))))) 
                                              | (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r
                                                 [(1U 
                                                   & (VL_MULS_III(32, (IData)(8U), 
                                                                  ((IData)(0x00000021U) 
                                                                   - vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                      >> 5U))] 
                                                 >> 
                                                 (0x0000001fU 
                                                  & VL_MULS_III(32, (IData)(8U), 
                                                                ((IData)(0x00000021U) 
                                                                 - vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)))))
                                           : ((((((
                                                   (((0x00000022U 
                                                      == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                     || (0x00000023U 
                                                         == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                    || (0x00000024U 
                                                        == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                   || (0x00000025U 
                                                       == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                  || (0x00000026U 
                                                      == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                 || (0x00000027U 
                                                     == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                || (0x00000028U 
                                                    == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                               || (0x00000029U 
                                                   == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b))
                                               ? ((
                                                   (0U 
                                                    == 
                                                    (0x0000001fU 
                                                     & ((IData)(0x00000040U) 
                                                        + 
                                                        (0x0000003fU 
                                                         & VL_MULS_III(32, (IData)(8U), 
                                                                       ((IData)(0x00000029U) 
                                                                        - vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b))))))
                                                    ? 0U
                                                    : 
                                                   (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r
                                                    [
                                                    (((IData)(0x00000047U) 
                                                      + 
                                                      (0x0000003fU 
                                                       & VL_MULS_III(32, (IData)(8U), 
                                                                     ((IData)(0x00000029U) 
                                                                      - vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)))) 
                                                     >> 5U)] 
                                                    << 
                                                    ((IData)(0x00000020U) 
                                                     - 
                                                     (0x0000001fU 
                                                      & ((IData)(0x00000040U) 
                                                         + 
                                                         (0x0000003fU 
                                                          & VL_MULS_III(32, (IData)(8U), 
                                                                        ((IData)(0x00000029U) 
                                                                         - vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)))))))) 
                                                  | (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r
                                                     [
                                                     (((IData)(0x00000040U) 
                                                       + 
                                                       (0x0000003fU 
                                                        & VL_MULS_III(32, (IData)(8U), 
                                                                      ((IData)(0x00000029U) 
                                                                       - vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)))) 
                                                      >> 5U)] 
                                                     >> 
                                                     (0x0000001fU 
                                                      & ((IData)(0x00000040U) 
                                                         + 
                                                         (0x0000003fU 
                                                          & VL_MULS_III(32, (IData)(8U), 
                                                                        ((IData)(0x00000029U) 
                                                                         - vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)))))))
                                               : ((
                                                   (((((((0x0000002aU 
                                                          == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                         || (0x0000002bU 
                                                             == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                        || (0x0000002cU 
                                                            == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                       || (0x0000002dU 
                                                           == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                      || (0x0000002eU 
                                                          == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                     || (0x0000002fU 
                                                         == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                    || (0x00000030U 
                                                        == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                   || (0x00000031U 
                                                       == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b))
                                                   ? (IData)(
                                                             (vlSelfRef.milan_datapath__DOT__cfg_adp_entity_id 
                                                              >> 
                                                              (0x0000003fU 
                                                               & VL_MULS_III(32, (IData)(8U), 
                                                                             ((IData)(0x00000031U) 
                                                                              - vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)))))
                                                   : 
                                                  ((0x00000032U 
                                                    == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                                    ? 
                                                   ((vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r[8U] 
                                                     << 0x0000000cU) 
                                                    | (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r[8U] 
                                                       >> 0x00000014U))
                                                    : 
                                                   ((0x00000033U 
                                                     == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                                     ? 
                                                    ((vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r[8U] 
                                                      << 0x00000014U) 
                                                     | (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r[8U] 
                                                        >> 0x0000000cU))
                                                     : 
                                                    ((0x00000034U 
                                                      == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                                      ? 0U
                                                      : 
                                                     ((0x00000035U 
                                                       == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                                       ? (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_idx_r)
                                                       : 
                                                      ((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_seq_r) 
                                                       >> 8U))))))))
                                       : ((0x0000003fU 
                                           == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                           ? (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_seq_r)
                                           : ((0x00000040U 
                                               == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                               ? ((vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r[8U] 
                                                   << 0x0000001cU) 
                                                  | (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r[8U] 
                                                     >> 4U))
                                               : ((0x00000041U 
                                                   == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                                   ? 
                                                  (0xb7U 
                                                   & ((vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r[8U] 
                                                       << 4U) 
                                                      | (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r[7U] 
                                                         >> 0x0000001cU)))
                                                   : 0U)))))));
        vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_beat 
            = ((0xffffffffff00ffffULL & vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_beat) 
               | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT____VlemCall_4__probe_byte)) 
                  << 0x00000010U));
        if ((1U & (~ VL_ONEHOT_I((((((((((0x00000041U 
                                          == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                         << 3U) | (
                                                   (0x00000040U 
                                                    == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                   << 2U)) 
                                       | (((0x0000003fU 
                                            == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                           << 1U) | 
                                          (0x0000003eU 
                                           == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b))) 
                                      << 0x0000000aU) 
                                     | (((0x00000035U 
                                          == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                         << 9U) | (
                                                   ((0x00000034U 
                                                     == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                    << 8U) 
                                                   | ((0x00000033U 
                                                       == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                      << 7U)))) 
                                    | ((((((0x00000032U 
                                            == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                           << 3U) | 
                                          (((0x00000031U 
                                             == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                            | ((0x00000030U 
                                                == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                               | ((0x0000002fU 
                                                   == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                  | ((0x0000002eU 
                                                      == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                     | ((0x0000002dU 
                                                         == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                        | ((0x0000002cU 
                                                            == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                           | ((0x0000002bU 
                                                               == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                              | (0x0000002aU 
                                                                 == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)))))))) 
                                           << 2U)) 
                                         | ((((0x00000029U 
                                               == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                              | ((0x00000028U 
                                                  == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                 | ((0x00000027U 
                                                     == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                    | ((0x00000026U 
                                                        == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                       | ((0x00000025U 
                                                           == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                          | ((0x00000024U 
                                                              == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                             | ((0x00000023U 
                                                                 == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                                | (0x00000022U 
                                                                   == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)))))))) 
                                             << 1U) 
                                            | ((0x00000021U 
                                                == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                               | ((0x00000020U 
                                                   == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                  | ((0x0000001fU 
                                                      == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                     | ((0x0000001eU 
                                                         == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                        | ((0x0000001dU 
                                                            == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                           | ((0x0000001cU 
                                                               == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                              | ((0x0000001bU 
                                                                  == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                                 | (0x0000001aU 
                                                                    == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)))))))))) 
                                        << 3U) | ((
                                                   (0x00000011U 
                                                    == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                   << 2U) 
                                                  | (((0x00000010U 
                                                       == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                      << 1U) 
                                                     | (0x0000000fU 
                                                        == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b))))) 
                                   << 0x0000000dU) 
                                  | (((((((0x0000000eU 
                                           == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                          << 3U) | 
                                         ((0x0000000dU 
                                           == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                          << 2U)) | 
                                        (((0x0000000cU 
                                           == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                          << 1U) | 
                                         (0x0000000bU 
                                          == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b))) 
                                       << 9U) | (((0x0000000aU 
                                                   == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                  << 8U) 
                                                 | (((9U 
                                                      == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                     << 7U) 
                                                    | ((8U 
                                                        == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                       << 6U)))) 
                                     | ((((7U == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                          << 5U) | 
                                         (((6U == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                           << 4U) | 
                                          ((3U == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                           << 3U))) 
                                        | (((2U == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                            << 2U) 
                                           | (((1U 
                                                == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                               << 1U) 
                                              | (0U 
                                                 == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)))))))))) {
            if ((0U != (((((((((0x00000041U == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                               << 3U) | ((0x00000040U 
                                          == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                         << 2U)) | 
                             (((0x0000003fU == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                               << 1U) | (0x0000003eU 
                                         == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b))) 
                            << 0x0000000aU) | (((0x00000035U 
                                                 == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                << 9U) 
                                               | (((0x00000034U 
                                                    == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                   << 8U) 
                                                  | ((0x00000033U 
                                                      == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                     << 7U)))) 
                          | ((((((0x00000032U == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                 << 3U) | (((0x00000031U 
                                             == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                            | ((0x00000030U 
                                                == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                               | ((0x0000002fU 
                                                   == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                  | ((0x0000002eU 
                                                      == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                     | ((0x0000002dU 
                                                         == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                        | ((0x0000002cU 
                                                            == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                           | ((0x0000002bU 
                                                               == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                              | (0x0000002aU 
                                                                 == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)))))))) 
                                           << 2U)) 
                               | ((((0x00000029U == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                    | ((0x00000028U 
                                        == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                       | ((0x00000027U 
                                           == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                          | ((0x00000026U 
                                              == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                             | ((0x00000025U 
                                                 == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                | ((0x00000024U 
                                                    == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                   | ((0x00000023U 
                                                       == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                      | (0x00000022U 
                                                         == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)))))))) 
                                   << 1U) | ((0x00000021U 
                                              == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                             | ((0x00000020U 
                                                 == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                | ((0x0000001fU 
                                                    == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                   | ((0x0000001eU 
                                                       == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                      | ((0x0000001dU 
                                                          == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                         | ((0x0000001cU 
                                                             == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                            | ((0x0000001bU 
                                                                == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                               | (0x0000001aU 
                                                                  == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)))))))))) 
                              << 3U) | (((0x00000011U 
                                          == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                         << 2U) | (
                                                   ((0x00000010U 
                                                     == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                    << 1U) 
                                                   | (0x0000000fU 
                                                      == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b))))) 
                         << 0x0000000dU) | (((((((0x0000000eU 
                                                  == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                 << 3U) 
                                                | ((0x0000000dU 
                                                    == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                   << 2U)) 
                                               | (((0x0000000cU 
                                                    == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                   << 1U) 
                                                  | (0x0000000bU 
                                                     == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b))) 
                                              << 9U) 
                                             | (((0x0000000aU 
                                                  == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                 << 8U) 
                                                | (((9U 
                                                     == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                    << 7U) 
                                                   | ((8U 
                                                       == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                      << 6U)))) 
                                            | ((((7U 
                                                  == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                 << 5U) 
                                                | (((6U 
                                                     == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                    << 4U) 
                                                   | ((3U 
                                                       == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                      << 3U))) 
                                               | (((2U 
                                                    == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                   << 2U) 
                                                  | (((1U 
                                                       == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                      << 1U) 
                                                     | (0U 
                                                        == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)))))))) {
                if (VL_UNLIKELY((vlSymsp->_vm_contextp__->assertOn()))) {
                    VL_WRITEF_NX("[%0t] %%Error: KL_acmp_lstn_ctx.sv:431: Assertion failed in %m: unique case, but multiple matches found for '32'h%X'\n",4, 'M',vlSymsp->name(),"milan_datapath.acmp_listener_sm.u_ctx.probe_byte", 'T',-9
                                 , '#',64,VL_TIME_UNITED_Q(1000)
                                 , '#',32,vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b);
                    VL_STOP_MT("../../../configs/generated/endstation_ax7101_8x8/../../../hdl/ieee17221/acmp/KL_acmp_lstn_ctx.sv", 431, "");
                }
            }
        }
        vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b 
            = ((IData)(3U) + ((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__beat_r) 
                              << 3U));
        vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT____VlemCall_4__probe_byte 
            = (0x000000ffU & (((((((((0U == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                     | (1U == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                    | (2U == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                   | (3U == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                  | (6U == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                 | (7U == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                | (8U == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                               | (9U == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b))
                               ? ((0U == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                   ? 0x91U : ((1U == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                               ? 0xe0U
                                               : ((2U 
                                                   == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                                   ? 0xf0U
                                                   : 
                                                  ((3U 
                                                    == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                                    ? 1U
                                                    : 
                                                   ((6U 
                                                     == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                                     ? (IData)(
                                                               (vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w 
                                                                >> 0x28U))
                                                     : 
                                                    ((7U 
                                                      == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                                      ? (IData)(
                                                                (vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w 
                                                                 >> 0x20U))
                                                      : 
                                                     ((8U 
                                                       == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                                       ? (IData)(
                                                                 (vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w 
                                                                  >> 0x18U))
                                                       : (IData)(
                                                                 (vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w 
                                                                  >> 0x10U)))))))))
                               : (((((((((0x0000000aU 
                                          == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                         | (0x0000000bU 
                                            == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                        | (0x0000000cU 
                                           == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                       | (0x0000000dU 
                                          == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                      | (0x0000000eU 
                                         == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                     | (0x0000000fU 
                                        == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                    | (0x00000010U 
                                       == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                   | (0x00000011U == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b))
                                   ? ((0x0000000aU 
                                       == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                       ? (IData)((vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w 
                                                  >> 8U))
                                       : ((0x0000000bU 
                                           == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                           ? (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w)
                                           : ((0x0000000cU 
                                               == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                               ? 0x22U
                                               : ((0x0000000dU 
                                                   == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                                   ? 0xf0U
                                                   : 
                                                  ((0x0000000eU 
                                                    == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                                    ? 0xfcU
                                                    : 
                                                   ((0x0000000fU 
                                                     == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                                     ? 0U
                                                     : 
                                                    ((0x00000010U 
                                                      == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                                      ? 0U
                                                      : 0x2cU)))))))
                                   : ((((((((((((((
                                                   ((0x0000001aU 
                                                     == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                    || (0x0000001bU 
                                                        == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                   || (0x0000001cU 
                                                       == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                  || (0x0000001dU 
                                                      == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                 || (0x0000001eU 
                                                     == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                || (0x0000001fU 
                                                    == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                               || (0x00000020U 
                                                   == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                              || (0x00000021U 
                                                  == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                             | ((((((((0x00000022U 
                                                       == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                      || (0x00000023U 
                                                          == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                     || (0x00000024U 
                                                         == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                    || (0x00000025U 
                                                        == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                   || (0x00000026U 
                                                       == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                  || (0x00000027U 
                                                      == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                 || (0x00000028U 
                                                     == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                || (0x00000029U 
                                                    == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b))) 
                                            | ((((((((0x0000002aU 
                                                      == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                     || (0x0000002bU 
                                                         == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                    || (0x0000002cU 
                                                        == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                   || (0x0000002dU 
                                                       == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                  || (0x0000002eU 
                                                      == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                 || (0x0000002fU 
                                                     == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                || (0x00000030U 
                                                    == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                               || (0x00000031U 
                                                   == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b))) 
                                           | (0x00000032U 
                                              == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                          | (0x00000033U 
                                             == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                         | (0x00000034U 
                                            == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                        | (0x00000035U 
                                           == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                       | (0x0000003eU 
                                          == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b))
                                       ? (((((((((0x0000001aU 
                                                  == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                 || (0x0000001bU 
                                                     == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                || (0x0000001cU 
                                                    == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                               || (0x0000001dU 
                                                   == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                              || (0x0000001eU 
                                                  == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                             || (0x0000001fU 
                                                 == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                            || (0x00000020U 
                                                == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                           || (0x00000021U 
                                               == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b))
                                           ? (((0U 
                                                == 
                                                (0x0000001fU 
                                                 & VL_MULS_III(32, (IData)(8U), 
                                                               ((IData)(0x00000021U) 
                                                                - vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b))))
                                                ? 0U
                                                : (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r
                                                   [
                                                   (((IData)(7U) 
                                                     + 
                                                     (0x0000003fU 
                                                      & VL_MULS_III(32, (IData)(8U), 
                                                                    ((IData)(0x00000021U) 
                                                                     - vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)))) 
                                                    >> 5U)] 
                                                   << 
                                                   ((IData)(0x00000020U) 
                                                    - 
                                                    (0x0000001fU 
                                                     & VL_MULS_III(32, (IData)(8U), 
                                                                   ((IData)(0x00000021U) 
                                                                    - vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)))))) 
                                              | (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r
                                                 [(1U 
                                                   & (VL_MULS_III(32, (IData)(8U), 
                                                                  ((IData)(0x00000021U) 
                                                                   - vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                      >> 5U))] 
                                                 >> 
                                                 (0x0000001fU 
                                                  & VL_MULS_III(32, (IData)(8U), 
                                                                ((IData)(0x00000021U) 
                                                                 - vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)))))
                                           : ((((((
                                                   (((0x00000022U 
                                                      == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                     || (0x00000023U 
                                                         == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                    || (0x00000024U 
                                                        == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                   || (0x00000025U 
                                                       == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                  || (0x00000026U 
                                                      == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                 || (0x00000027U 
                                                     == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                || (0x00000028U 
                                                    == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                               || (0x00000029U 
                                                   == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b))
                                               ? ((
                                                   (0U 
                                                    == 
                                                    (0x0000001fU 
                                                     & ((IData)(0x00000040U) 
                                                        + 
                                                        (0x0000003fU 
                                                         & VL_MULS_III(32, (IData)(8U), 
                                                                       ((IData)(0x00000029U) 
                                                                        - vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b))))))
                                                    ? 0U
                                                    : 
                                                   (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r
                                                    [
                                                    (((IData)(0x00000047U) 
                                                      + 
                                                      (0x0000003fU 
                                                       & VL_MULS_III(32, (IData)(8U), 
                                                                     ((IData)(0x00000029U) 
                                                                      - vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)))) 
                                                     >> 5U)] 
                                                    << 
                                                    ((IData)(0x00000020U) 
                                                     - 
                                                     (0x0000001fU 
                                                      & ((IData)(0x00000040U) 
                                                         + 
                                                         (0x0000003fU 
                                                          & VL_MULS_III(32, (IData)(8U), 
                                                                        ((IData)(0x00000029U) 
                                                                         - vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)))))))) 
                                                  | (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r
                                                     [
                                                     (((IData)(0x00000040U) 
                                                       + 
                                                       (0x0000003fU 
                                                        & VL_MULS_III(32, (IData)(8U), 
                                                                      ((IData)(0x00000029U) 
                                                                       - vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)))) 
                                                      >> 5U)] 
                                                     >> 
                                                     (0x0000001fU 
                                                      & ((IData)(0x00000040U) 
                                                         + 
                                                         (0x0000003fU 
                                                          & VL_MULS_III(32, (IData)(8U), 
                                                                        ((IData)(0x00000029U) 
                                                                         - vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)))))))
                                               : ((
                                                   (((((((0x0000002aU 
                                                          == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                         || (0x0000002bU 
                                                             == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                        || (0x0000002cU 
                                                            == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                       || (0x0000002dU 
                                                           == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                      || (0x0000002eU 
                                                          == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                     || (0x0000002fU 
                                                         == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                    || (0x00000030U 
                                                        == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                   || (0x00000031U 
                                                       == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b))
                                                   ? (IData)(
                                                             (vlSelfRef.milan_datapath__DOT__cfg_adp_entity_id 
                                                              >> 
                                                              (0x0000003fU 
                                                               & VL_MULS_III(32, (IData)(8U), 
                                                                             ((IData)(0x00000031U) 
                                                                              - vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)))))
                                                   : 
                                                  ((0x00000032U 
                                                    == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                                    ? 
                                                   ((vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r[8U] 
                                                     << 0x0000000cU) 
                                                    | (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r[8U] 
                                                       >> 0x00000014U))
                                                    : 
                                                   ((0x00000033U 
                                                     == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                                     ? 
                                                    ((vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r[8U] 
                                                      << 0x00000014U) 
                                                     | (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r[8U] 
                                                        >> 0x0000000cU))
                                                     : 
                                                    ((0x00000034U 
                                                      == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                                      ? 0U
                                                      : 
                                                     ((0x00000035U 
                                                       == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                                       ? (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_idx_r)
                                                       : 
                                                      ((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_seq_r) 
                                                       >> 8U))))))))
                                       : ((0x0000003fU 
                                           == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                           ? (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_seq_r)
                                           : ((0x00000040U 
                                               == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                               ? ((vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r[8U] 
                                                   << 0x0000001cU) 
                                                  | (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r[8U] 
                                                     >> 4U))
                                               : ((0x00000041U 
                                                   == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                                   ? 
                                                  (0xb7U 
                                                   & ((vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r[8U] 
                                                       << 4U) 
                                                      | (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r[7U] 
                                                         >> 0x0000001cU)))
                                                   : 0U)))))));
        vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_beat 
            = ((0xffffffff00ffffffULL & vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_beat) 
               | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT____VlemCall_4__probe_byte)) 
                  << 0x00000018U));
        if ((1U & (~ VL_ONEHOT_I((((((((((0x00000041U 
                                          == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                         << 3U) | (
                                                   (0x00000040U 
                                                    == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                   << 2U)) 
                                       | (((0x0000003fU 
                                            == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                           << 1U) | 
                                          (0x0000003eU 
                                           == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b))) 
                                      << 0x0000000aU) 
                                     | (((0x00000035U 
                                          == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                         << 9U) | (
                                                   ((0x00000034U 
                                                     == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                    << 8U) 
                                                   | ((0x00000033U 
                                                       == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                      << 7U)))) 
                                    | ((((((0x00000032U 
                                            == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                           << 3U) | 
                                          (((0x00000031U 
                                             == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                            | ((0x00000030U 
                                                == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                               | ((0x0000002fU 
                                                   == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                  | ((0x0000002eU 
                                                      == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                     | ((0x0000002dU 
                                                         == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                        | ((0x0000002cU 
                                                            == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                           | ((0x0000002bU 
                                                               == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                              | (0x0000002aU 
                                                                 == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)))))))) 
                                           << 2U)) 
                                         | ((((0x00000029U 
                                               == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                              | ((0x00000028U 
                                                  == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                 | ((0x00000027U 
                                                     == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                    | ((0x00000026U 
                                                        == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                       | ((0x00000025U 
                                                           == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                          | ((0x00000024U 
                                                              == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                             | ((0x00000023U 
                                                                 == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                                | (0x00000022U 
                                                                   == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)))))))) 
                                             << 1U) 
                                            | ((0x00000021U 
                                                == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                               | ((0x00000020U 
                                                   == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                  | ((0x0000001fU 
                                                      == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                     | ((0x0000001eU 
                                                         == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                        | ((0x0000001dU 
                                                            == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                           | ((0x0000001cU 
                                                               == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                              | ((0x0000001bU 
                                                                  == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                                 | (0x0000001aU 
                                                                    == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)))))))))) 
                                        << 3U) | ((
                                                   (0x00000011U 
                                                    == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                   << 2U) 
                                                  | (((0x00000010U 
                                                       == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                      << 1U) 
                                                     | (0x0000000fU 
                                                        == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b))))) 
                                   << 0x0000000dU) 
                                  | (((((((0x0000000eU 
                                           == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                          << 3U) | 
                                         ((0x0000000dU 
                                           == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                          << 2U)) | 
                                        (((0x0000000cU 
                                           == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                          << 1U) | 
                                         (0x0000000bU 
                                          == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b))) 
                                       << 9U) | (((0x0000000aU 
                                                   == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                  << 8U) 
                                                 | (((9U 
                                                      == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                     << 7U) 
                                                    | ((8U 
                                                        == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                       << 6U)))) 
                                     | ((((7U == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                          << 5U) | 
                                         (((6U == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                           << 4U) | 
                                          ((3U == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                           << 3U))) 
                                        | (((2U == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                            << 2U) 
                                           | (((1U 
                                                == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                               << 1U) 
                                              | (0U 
                                                 == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)))))))))) {
            if ((0U != (((((((((0x00000041U == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                               << 3U) | ((0x00000040U 
                                          == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                         << 2U)) | 
                             (((0x0000003fU == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                               << 1U) | (0x0000003eU 
                                         == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b))) 
                            << 0x0000000aU) | (((0x00000035U 
                                                 == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                << 9U) 
                                               | (((0x00000034U 
                                                    == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                   << 8U) 
                                                  | ((0x00000033U 
                                                      == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                     << 7U)))) 
                          | ((((((0x00000032U == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                 << 3U) | (((0x00000031U 
                                             == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                            | ((0x00000030U 
                                                == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                               | ((0x0000002fU 
                                                   == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                  | ((0x0000002eU 
                                                      == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                     | ((0x0000002dU 
                                                         == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                        | ((0x0000002cU 
                                                            == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                           | ((0x0000002bU 
                                                               == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                              | (0x0000002aU 
                                                                 == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)))))))) 
                                           << 2U)) 
                               | ((((0x00000029U == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                    | ((0x00000028U 
                                        == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                       | ((0x00000027U 
                                           == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                          | ((0x00000026U 
                                              == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                             | ((0x00000025U 
                                                 == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                | ((0x00000024U 
                                                    == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                   | ((0x00000023U 
                                                       == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                      | (0x00000022U 
                                                         == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)))))))) 
                                   << 1U) | ((0x00000021U 
                                              == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                             | ((0x00000020U 
                                                 == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                | ((0x0000001fU 
                                                    == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                   | ((0x0000001eU 
                                                       == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                      | ((0x0000001dU 
                                                          == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                         | ((0x0000001cU 
                                                             == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                            | ((0x0000001bU 
                                                                == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                               | (0x0000001aU 
                                                                  == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)))))))))) 
                              << 3U) | (((0x00000011U 
                                          == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                         << 2U) | (
                                                   ((0x00000010U 
                                                     == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                    << 1U) 
                                                   | (0x0000000fU 
                                                      == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b))))) 
                         << 0x0000000dU) | (((((((0x0000000eU 
                                                  == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                 << 3U) 
                                                | ((0x0000000dU 
                                                    == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                   << 2U)) 
                                               | (((0x0000000cU 
                                                    == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                   << 1U) 
                                                  | (0x0000000bU 
                                                     == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b))) 
                                              << 9U) 
                                             | (((0x0000000aU 
                                                  == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                 << 8U) 
                                                | (((9U 
                                                     == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                    << 7U) 
                                                   | ((8U 
                                                       == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                      << 6U)))) 
                                            | ((((7U 
                                                  == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                 << 5U) 
                                                | (((6U 
                                                     == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                    << 4U) 
                                                   | ((3U 
                                                       == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                      << 3U))) 
                                               | (((2U 
                                                    == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                   << 2U) 
                                                  | (((1U 
                                                       == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                      << 1U) 
                                                     | (0U 
                                                        == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)))))))) {
                if (VL_UNLIKELY((vlSymsp->_vm_contextp__->assertOn()))) {
                    VL_WRITEF_NX("[%0t] %%Error: KL_acmp_lstn_ctx.sv:431: Assertion failed in %m: unique case, but multiple matches found for '32'h%X'\n",4, 'M',vlSymsp->name(),"milan_datapath.acmp_listener_sm.u_ctx.probe_byte", 'T',-9
                                 , '#',64,VL_TIME_UNITED_Q(1000)
                                 , '#',32,vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b);
                    VL_STOP_MT("../../../configs/generated/endstation_ax7101_8x8/../../../hdl/ieee17221/acmp/KL_acmp_lstn_ctx.sv", 431, "");
                }
            }
        }
        vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b 
            = ((IData)(4U) + ((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__beat_r) 
                              << 3U));
        vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT____VlemCall_4__probe_byte 
            = (0x000000ffU & (((((((((0U == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                     | (1U == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                    | (2U == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                   | (3U == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                  | (6U == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                 | (7U == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                | (8U == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                               | (9U == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b))
                               ? ((0U == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                   ? 0x91U : ((1U == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                               ? 0xe0U
                                               : ((2U 
                                                   == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                                   ? 0xf0U
                                                   : 
                                                  ((3U 
                                                    == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                                    ? 1U
                                                    : 
                                                   ((6U 
                                                     == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                                     ? (IData)(
                                                               (vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w 
                                                                >> 0x28U))
                                                     : 
                                                    ((7U 
                                                      == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                                      ? (IData)(
                                                                (vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w 
                                                                 >> 0x20U))
                                                      : 
                                                     ((8U 
                                                       == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                                       ? (IData)(
                                                                 (vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w 
                                                                  >> 0x18U))
                                                       : (IData)(
                                                                 (vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w 
                                                                  >> 0x10U)))))))))
                               : (((((((((0x0000000aU 
                                          == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                         | (0x0000000bU 
                                            == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                        | (0x0000000cU 
                                           == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                       | (0x0000000dU 
                                          == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                      | (0x0000000eU 
                                         == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                     | (0x0000000fU 
                                        == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                    | (0x00000010U 
                                       == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                   | (0x00000011U == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b))
                                   ? ((0x0000000aU 
                                       == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                       ? (IData)((vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w 
                                                  >> 8U))
                                       : ((0x0000000bU 
                                           == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                           ? (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w)
                                           : ((0x0000000cU 
                                               == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                               ? 0x22U
                                               : ((0x0000000dU 
                                                   == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                                   ? 0xf0U
                                                   : 
                                                  ((0x0000000eU 
                                                    == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                                    ? 0xfcU
                                                    : 
                                                   ((0x0000000fU 
                                                     == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                                     ? 0U
                                                     : 
                                                    ((0x00000010U 
                                                      == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                                      ? 0U
                                                      : 0x2cU)))))))
                                   : ((((((((((((((
                                                   ((0x0000001aU 
                                                     == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                    || (0x0000001bU 
                                                        == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                   || (0x0000001cU 
                                                       == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                  || (0x0000001dU 
                                                      == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                 || (0x0000001eU 
                                                     == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                || (0x0000001fU 
                                                    == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                               || (0x00000020U 
                                                   == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                              || (0x00000021U 
                                                  == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                             | ((((((((0x00000022U 
                                                       == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                      || (0x00000023U 
                                                          == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                     || (0x00000024U 
                                                         == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                    || (0x00000025U 
                                                        == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                   || (0x00000026U 
                                                       == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                  || (0x00000027U 
                                                      == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                 || (0x00000028U 
                                                     == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                || (0x00000029U 
                                                    == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b))) 
                                            | ((((((((0x0000002aU 
                                                      == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                     || (0x0000002bU 
                                                         == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                    || (0x0000002cU 
                                                        == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                   || (0x0000002dU 
                                                       == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                  || (0x0000002eU 
                                                      == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                 || (0x0000002fU 
                                                     == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                || (0x00000030U 
                                                    == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                               || (0x00000031U 
                                                   == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b))) 
                                           | (0x00000032U 
                                              == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                          | (0x00000033U 
                                             == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                         | (0x00000034U 
                                            == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                        | (0x00000035U 
                                           == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                       | (0x0000003eU 
                                          == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b))
                                       ? (((((((((0x0000001aU 
                                                  == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                 || (0x0000001bU 
                                                     == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                || (0x0000001cU 
                                                    == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                               || (0x0000001dU 
                                                   == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                              || (0x0000001eU 
                                                  == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                             || (0x0000001fU 
                                                 == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                            || (0x00000020U 
                                                == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                           || (0x00000021U 
                                               == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b))
                                           ? (((0U 
                                                == 
                                                (0x0000001fU 
                                                 & VL_MULS_III(32, (IData)(8U), 
                                                               ((IData)(0x00000021U) 
                                                                - vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b))))
                                                ? 0U
                                                : (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r
                                                   [
                                                   (((IData)(7U) 
                                                     + 
                                                     (0x0000003fU 
                                                      & VL_MULS_III(32, (IData)(8U), 
                                                                    ((IData)(0x00000021U) 
                                                                     - vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)))) 
                                                    >> 5U)] 
                                                   << 
                                                   ((IData)(0x00000020U) 
                                                    - 
                                                    (0x0000001fU 
                                                     & VL_MULS_III(32, (IData)(8U), 
                                                                   ((IData)(0x00000021U) 
                                                                    - vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)))))) 
                                              | (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r
                                                 [(1U 
                                                   & (VL_MULS_III(32, (IData)(8U), 
                                                                  ((IData)(0x00000021U) 
                                                                   - vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                      >> 5U))] 
                                                 >> 
                                                 (0x0000001fU 
                                                  & VL_MULS_III(32, (IData)(8U), 
                                                                ((IData)(0x00000021U) 
                                                                 - vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)))))
                                           : ((((((
                                                   (((0x00000022U 
                                                      == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                     || (0x00000023U 
                                                         == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                    || (0x00000024U 
                                                        == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                   || (0x00000025U 
                                                       == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                  || (0x00000026U 
                                                      == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                 || (0x00000027U 
                                                     == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                || (0x00000028U 
                                                    == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                               || (0x00000029U 
                                                   == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b))
                                               ? ((
                                                   (0U 
                                                    == 
                                                    (0x0000001fU 
                                                     & ((IData)(0x00000040U) 
                                                        + 
                                                        (0x0000003fU 
                                                         & VL_MULS_III(32, (IData)(8U), 
                                                                       ((IData)(0x00000029U) 
                                                                        - vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b))))))
                                                    ? 0U
                                                    : 
                                                   (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r
                                                    [
                                                    (((IData)(0x00000047U) 
                                                      + 
                                                      (0x0000003fU 
                                                       & VL_MULS_III(32, (IData)(8U), 
                                                                     ((IData)(0x00000029U) 
                                                                      - vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)))) 
                                                     >> 5U)] 
                                                    << 
                                                    ((IData)(0x00000020U) 
                                                     - 
                                                     (0x0000001fU 
                                                      & ((IData)(0x00000040U) 
                                                         + 
                                                         (0x0000003fU 
                                                          & VL_MULS_III(32, (IData)(8U), 
                                                                        ((IData)(0x00000029U) 
                                                                         - vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)))))))) 
                                                  | (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r
                                                     [
                                                     (((IData)(0x00000040U) 
                                                       + 
                                                       (0x0000003fU 
                                                        & VL_MULS_III(32, (IData)(8U), 
                                                                      ((IData)(0x00000029U) 
                                                                       - vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)))) 
                                                      >> 5U)] 
                                                     >> 
                                                     (0x0000001fU 
                                                      & ((IData)(0x00000040U) 
                                                         + 
                                                         (0x0000003fU 
                                                          & VL_MULS_III(32, (IData)(8U), 
                                                                        ((IData)(0x00000029U) 
                                                                         - vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)))))))
                                               : ((
                                                   (((((((0x0000002aU 
                                                          == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                         || (0x0000002bU 
                                                             == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                        || (0x0000002cU 
                                                            == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                       || (0x0000002dU 
                                                           == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                      || (0x0000002eU 
                                                          == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                     || (0x0000002fU 
                                                         == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                    || (0x00000030U 
                                                        == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                   || (0x00000031U 
                                                       == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b))
                                                   ? (IData)(
                                                             (vlSelfRef.milan_datapath__DOT__cfg_adp_entity_id 
                                                              >> 
                                                              (0x0000003fU 
                                                               & VL_MULS_III(32, (IData)(8U), 
                                                                             ((IData)(0x00000031U) 
                                                                              - vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)))))
                                                   : 
                                                  ((0x00000032U 
                                                    == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                                    ? 
                                                   ((vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r[8U] 
                                                     << 0x0000000cU) 
                                                    | (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r[8U] 
                                                       >> 0x00000014U))
                                                    : 
                                                   ((0x00000033U 
                                                     == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                                     ? 
                                                    ((vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r[8U] 
                                                      << 0x00000014U) 
                                                     | (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r[8U] 
                                                        >> 0x0000000cU))
                                                     : 
                                                    ((0x00000034U 
                                                      == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                                      ? 0U
                                                      : 
                                                     ((0x00000035U 
                                                       == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                                       ? (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_idx_r)
                                                       : 
                                                      ((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_seq_r) 
                                                       >> 8U))))))))
                                       : ((0x0000003fU 
                                           == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                           ? (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_seq_r)
                                           : ((0x00000040U 
                                               == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                               ? ((vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r[8U] 
                                                   << 0x0000001cU) 
                                                  | (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r[8U] 
                                                     >> 4U))
                                               : ((0x00000041U 
                                                   == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                                   ? 
                                                  (0xb7U 
                                                   & ((vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r[8U] 
                                                       << 4U) 
                                                      | (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r[7U] 
                                                         >> 0x0000001cU)))
                                                   : 0U)))))));
        vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_beat 
            = ((0xffffff00ffffffffULL & vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_beat) 
               | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT____VlemCall_4__probe_byte)) 
                  << 0x00000020U));
        if ((1U & (~ VL_ONEHOT_I((((((((((0x00000041U 
                                          == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                         << 3U) | (
                                                   (0x00000040U 
                                                    == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                   << 2U)) 
                                       | (((0x0000003fU 
                                            == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                           << 1U) | 
                                          (0x0000003eU 
                                           == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b))) 
                                      << 0x0000000aU) 
                                     | (((0x00000035U 
                                          == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                         << 9U) | (
                                                   ((0x00000034U 
                                                     == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                    << 8U) 
                                                   | ((0x00000033U 
                                                       == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                      << 7U)))) 
                                    | ((((((0x00000032U 
                                            == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                           << 3U) | 
                                          (((0x00000031U 
                                             == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                            | ((0x00000030U 
                                                == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                               | ((0x0000002fU 
                                                   == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                  | ((0x0000002eU 
                                                      == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                     | ((0x0000002dU 
                                                         == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                        | ((0x0000002cU 
                                                            == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                           | ((0x0000002bU 
                                                               == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                              | (0x0000002aU 
                                                                 == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)))))))) 
                                           << 2U)) 
                                         | ((((0x00000029U 
                                               == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                              | ((0x00000028U 
                                                  == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                 | ((0x00000027U 
                                                     == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                    | ((0x00000026U 
                                                        == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                       | ((0x00000025U 
                                                           == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                          | ((0x00000024U 
                                                              == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                             | ((0x00000023U 
                                                                 == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                                | (0x00000022U 
                                                                   == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)))))))) 
                                             << 1U) 
                                            | ((0x00000021U 
                                                == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                               | ((0x00000020U 
                                                   == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                  | ((0x0000001fU 
                                                      == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                     | ((0x0000001eU 
                                                         == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                        | ((0x0000001dU 
                                                            == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                           | ((0x0000001cU 
                                                               == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                              | ((0x0000001bU 
                                                                  == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                                 | (0x0000001aU 
                                                                    == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)))))))))) 
                                        << 3U) | ((
                                                   (0x00000011U 
                                                    == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                   << 2U) 
                                                  | (((0x00000010U 
                                                       == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                      << 1U) 
                                                     | (0x0000000fU 
                                                        == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b))))) 
                                   << 0x0000000dU) 
                                  | (((((((0x0000000eU 
                                           == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                          << 3U) | 
                                         ((0x0000000dU 
                                           == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                          << 2U)) | 
                                        (((0x0000000cU 
                                           == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                          << 1U) | 
                                         (0x0000000bU 
                                          == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b))) 
                                       << 9U) | (((0x0000000aU 
                                                   == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                  << 8U) 
                                                 | (((9U 
                                                      == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                     << 7U) 
                                                    | ((8U 
                                                        == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                       << 6U)))) 
                                     | ((((7U == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                          << 5U) | 
                                         (((6U == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                           << 4U) | 
                                          ((3U == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                           << 3U))) 
                                        | (((2U == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                            << 2U) 
                                           | (((1U 
                                                == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                               << 1U) 
                                              | (0U 
                                                 == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)))))))))) {
            if ((0U != (((((((((0x00000041U == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                               << 3U) | ((0x00000040U 
                                          == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                         << 2U)) | 
                             (((0x0000003fU == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                               << 1U) | (0x0000003eU 
                                         == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b))) 
                            << 0x0000000aU) | (((0x00000035U 
                                                 == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                << 9U) 
                                               | (((0x00000034U 
                                                    == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                   << 8U) 
                                                  | ((0x00000033U 
                                                      == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                     << 7U)))) 
                          | ((((((0x00000032U == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                 << 3U) | (((0x00000031U 
                                             == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                            | ((0x00000030U 
                                                == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                               | ((0x0000002fU 
                                                   == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                  | ((0x0000002eU 
                                                      == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                     | ((0x0000002dU 
                                                         == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                        | ((0x0000002cU 
                                                            == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                           | ((0x0000002bU 
                                                               == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                              | (0x0000002aU 
                                                                 == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)))))))) 
                                           << 2U)) 
                               | ((((0x00000029U == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                    | ((0x00000028U 
                                        == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                       | ((0x00000027U 
                                           == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                          | ((0x00000026U 
                                              == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                             | ((0x00000025U 
                                                 == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                | ((0x00000024U 
                                                    == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                   | ((0x00000023U 
                                                       == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                      | (0x00000022U 
                                                         == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)))))))) 
                                   << 1U) | ((0x00000021U 
                                              == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                             | ((0x00000020U 
                                                 == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                | ((0x0000001fU 
                                                    == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                   | ((0x0000001eU 
                                                       == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                      | ((0x0000001dU 
                                                          == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                         | ((0x0000001cU 
                                                             == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                            | ((0x0000001bU 
                                                                == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                               | (0x0000001aU 
                                                                  == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)))))))))) 
                              << 3U) | (((0x00000011U 
                                          == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                         << 2U) | (
                                                   ((0x00000010U 
                                                     == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                    << 1U) 
                                                   | (0x0000000fU 
                                                      == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b))))) 
                         << 0x0000000dU) | (((((((0x0000000eU 
                                                  == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                 << 3U) 
                                                | ((0x0000000dU 
                                                    == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                   << 2U)) 
                                               | (((0x0000000cU 
                                                    == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                   << 1U) 
                                                  | (0x0000000bU 
                                                     == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b))) 
                                              << 9U) 
                                             | (((0x0000000aU 
                                                  == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                 << 8U) 
                                                | (((9U 
                                                     == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                    << 7U) 
                                                   | ((8U 
                                                       == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                      << 6U)))) 
                                            | ((((7U 
                                                  == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                 << 5U) 
                                                | (((6U 
                                                     == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                    << 4U) 
                                                   | ((3U 
                                                       == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                      << 3U))) 
                                               | (((2U 
                                                    == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                   << 2U) 
                                                  | (((1U 
                                                       == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                      << 1U) 
                                                     | (0U 
                                                        == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)))))))) {
                if (VL_UNLIKELY((vlSymsp->_vm_contextp__->assertOn()))) {
                    VL_WRITEF_NX("[%0t] %%Error: KL_acmp_lstn_ctx.sv:431: Assertion failed in %m: unique case, but multiple matches found for '32'h%X'\n",4, 'M',vlSymsp->name(),"milan_datapath.acmp_listener_sm.u_ctx.probe_byte", 'T',-9
                                 , '#',64,VL_TIME_UNITED_Q(1000)
                                 , '#',32,vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b);
                    VL_STOP_MT("../../../configs/generated/endstation_ax7101_8x8/../../../hdl/ieee17221/acmp/KL_acmp_lstn_ctx.sv", 431, "");
                }
            }
        }
        vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b 
            = ((IData)(5U) + ((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__beat_r) 
                              << 3U));
        vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT____VlemCall_4__probe_byte 
            = (0x000000ffU & (((((((((0U == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                     | (1U == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                    | (2U == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                   | (3U == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                  | (6U == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                 | (7U == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                | (8U == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                               | (9U == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b))
                               ? ((0U == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                   ? 0x91U : ((1U == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                               ? 0xe0U
                                               : ((2U 
                                                   == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                                   ? 0xf0U
                                                   : 
                                                  ((3U 
                                                    == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                                    ? 1U
                                                    : 
                                                   ((6U 
                                                     == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                                     ? (IData)(
                                                               (vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w 
                                                                >> 0x28U))
                                                     : 
                                                    ((7U 
                                                      == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                                      ? (IData)(
                                                                (vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w 
                                                                 >> 0x20U))
                                                      : 
                                                     ((8U 
                                                       == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                                       ? (IData)(
                                                                 (vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w 
                                                                  >> 0x18U))
                                                       : (IData)(
                                                                 (vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w 
                                                                  >> 0x10U)))))))))
                               : (((((((((0x0000000aU 
                                          == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                         | (0x0000000bU 
                                            == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                        | (0x0000000cU 
                                           == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                       | (0x0000000dU 
                                          == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                      | (0x0000000eU 
                                         == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                     | (0x0000000fU 
                                        == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                    | (0x00000010U 
                                       == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                   | (0x00000011U == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b))
                                   ? ((0x0000000aU 
                                       == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                       ? (IData)((vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w 
                                                  >> 8U))
                                       : ((0x0000000bU 
                                           == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                           ? (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w)
                                           : ((0x0000000cU 
                                               == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                               ? 0x22U
                                               : ((0x0000000dU 
                                                   == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                                   ? 0xf0U
                                                   : 
                                                  ((0x0000000eU 
                                                    == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                                    ? 0xfcU
                                                    : 
                                                   ((0x0000000fU 
                                                     == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                                     ? 0U
                                                     : 
                                                    ((0x00000010U 
                                                      == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                                      ? 0U
                                                      : 0x2cU)))))))
                                   : ((((((((((((((
                                                   ((0x0000001aU 
                                                     == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                    || (0x0000001bU 
                                                        == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                   || (0x0000001cU 
                                                       == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                  || (0x0000001dU 
                                                      == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                 || (0x0000001eU 
                                                     == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                || (0x0000001fU 
                                                    == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                               || (0x00000020U 
                                                   == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                              || (0x00000021U 
                                                  == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                             | ((((((((0x00000022U 
                                                       == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                      || (0x00000023U 
                                                          == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                     || (0x00000024U 
                                                         == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                    || (0x00000025U 
                                                        == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                   || (0x00000026U 
                                                       == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                  || (0x00000027U 
                                                      == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                 || (0x00000028U 
                                                     == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                || (0x00000029U 
                                                    == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b))) 
                                            | ((((((((0x0000002aU 
                                                      == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                     || (0x0000002bU 
                                                         == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                    || (0x0000002cU 
                                                        == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                   || (0x0000002dU 
                                                       == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                  || (0x0000002eU 
                                                      == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                 || (0x0000002fU 
                                                     == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                || (0x00000030U 
                                                    == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                               || (0x00000031U 
                                                   == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b))) 
                                           | (0x00000032U 
                                              == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                          | (0x00000033U 
                                             == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                         | (0x00000034U 
                                            == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                        | (0x00000035U 
                                           == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                       | (0x0000003eU 
                                          == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b))
                                       ? (((((((((0x0000001aU 
                                                  == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                 || (0x0000001bU 
                                                     == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                || (0x0000001cU 
                                                    == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                               || (0x0000001dU 
                                                   == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                              || (0x0000001eU 
                                                  == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                             || (0x0000001fU 
                                                 == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                            || (0x00000020U 
                                                == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                           || (0x00000021U 
                                               == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b))
                                           ? (((0U 
                                                == 
                                                (0x0000001fU 
                                                 & VL_MULS_III(32, (IData)(8U), 
                                                               ((IData)(0x00000021U) 
                                                                - vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b))))
                                                ? 0U
                                                : (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r
                                                   [
                                                   (((IData)(7U) 
                                                     + 
                                                     (0x0000003fU 
                                                      & VL_MULS_III(32, (IData)(8U), 
                                                                    ((IData)(0x00000021U) 
                                                                     - vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)))) 
                                                    >> 5U)] 
                                                   << 
                                                   ((IData)(0x00000020U) 
                                                    - 
                                                    (0x0000001fU 
                                                     & VL_MULS_III(32, (IData)(8U), 
                                                                   ((IData)(0x00000021U) 
                                                                    - vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)))))) 
                                              | (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r
                                                 [(1U 
                                                   & (VL_MULS_III(32, (IData)(8U), 
                                                                  ((IData)(0x00000021U) 
                                                                   - vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                      >> 5U))] 
                                                 >> 
                                                 (0x0000001fU 
                                                  & VL_MULS_III(32, (IData)(8U), 
                                                                ((IData)(0x00000021U) 
                                                                 - vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)))))
                                           : ((((((
                                                   (((0x00000022U 
                                                      == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                     || (0x00000023U 
                                                         == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                    || (0x00000024U 
                                                        == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                   || (0x00000025U 
                                                       == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                  || (0x00000026U 
                                                      == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                 || (0x00000027U 
                                                     == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                || (0x00000028U 
                                                    == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                               || (0x00000029U 
                                                   == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b))
                                               ? ((
                                                   (0U 
                                                    == 
                                                    (0x0000001fU 
                                                     & ((IData)(0x00000040U) 
                                                        + 
                                                        (0x0000003fU 
                                                         & VL_MULS_III(32, (IData)(8U), 
                                                                       ((IData)(0x00000029U) 
                                                                        - vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b))))))
                                                    ? 0U
                                                    : 
                                                   (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r
                                                    [
                                                    (((IData)(0x00000047U) 
                                                      + 
                                                      (0x0000003fU 
                                                       & VL_MULS_III(32, (IData)(8U), 
                                                                     ((IData)(0x00000029U) 
                                                                      - vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)))) 
                                                     >> 5U)] 
                                                    << 
                                                    ((IData)(0x00000020U) 
                                                     - 
                                                     (0x0000001fU 
                                                      & ((IData)(0x00000040U) 
                                                         + 
                                                         (0x0000003fU 
                                                          & VL_MULS_III(32, (IData)(8U), 
                                                                        ((IData)(0x00000029U) 
                                                                         - vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)))))))) 
                                                  | (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r
                                                     [
                                                     (((IData)(0x00000040U) 
                                                       + 
                                                       (0x0000003fU 
                                                        & VL_MULS_III(32, (IData)(8U), 
                                                                      ((IData)(0x00000029U) 
                                                                       - vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)))) 
                                                      >> 5U)] 
                                                     >> 
                                                     (0x0000001fU 
                                                      & ((IData)(0x00000040U) 
                                                         + 
                                                         (0x0000003fU 
                                                          & VL_MULS_III(32, (IData)(8U), 
                                                                        ((IData)(0x00000029U) 
                                                                         - vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)))))))
                                               : ((
                                                   (((((((0x0000002aU 
                                                          == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                         || (0x0000002bU 
                                                             == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                        || (0x0000002cU 
                                                            == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                       || (0x0000002dU 
                                                           == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                      || (0x0000002eU 
                                                          == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                     || (0x0000002fU 
                                                         == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                    || (0x00000030U 
                                                        == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                   || (0x00000031U 
                                                       == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b))
                                                   ? (IData)(
                                                             (vlSelfRef.milan_datapath__DOT__cfg_adp_entity_id 
                                                              >> 
                                                              (0x0000003fU 
                                                               & VL_MULS_III(32, (IData)(8U), 
                                                                             ((IData)(0x00000031U) 
                                                                              - vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)))))
                                                   : 
                                                  ((0x00000032U 
                                                    == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                                    ? 
                                                   ((vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r[8U] 
                                                     << 0x0000000cU) 
                                                    | (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r[8U] 
                                                       >> 0x00000014U))
                                                    : 
                                                   ((0x00000033U 
                                                     == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                                     ? 
                                                    ((vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r[8U] 
                                                      << 0x00000014U) 
                                                     | (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r[8U] 
                                                        >> 0x0000000cU))
                                                     : 
                                                    ((0x00000034U 
                                                      == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                                      ? 0U
                                                      : 
                                                     ((0x00000035U 
                                                       == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                                       ? (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_idx_r)
                                                       : 
                                                      ((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_seq_r) 
                                                       >> 8U))))))))
                                       : ((0x0000003fU 
                                           == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                           ? (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_seq_r)
                                           : ((0x00000040U 
                                               == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                               ? ((vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r[8U] 
                                                   << 0x0000001cU) 
                                                  | (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r[8U] 
                                                     >> 4U))
                                               : ((0x00000041U 
                                                   == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                                   ? 
                                                  (0xb7U 
                                                   & ((vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r[8U] 
                                                       << 4U) 
                                                      | (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r[7U] 
                                                         >> 0x0000001cU)))
                                                   : 0U)))))));
        vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_beat 
            = ((0xffff00ffffffffffULL & vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_beat) 
               | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT____VlemCall_4__probe_byte)) 
                  << 0x00000028U));
        if ((1U & (~ VL_ONEHOT_I((((((((((0x00000041U 
                                          == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                         << 3U) | (
                                                   (0x00000040U 
                                                    == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                   << 2U)) 
                                       | (((0x0000003fU 
                                            == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                           << 1U) | 
                                          (0x0000003eU 
                                           == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b))) 
                                      << 0x0000000aU) 
                                     | (((0x00000035U 
                                          == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                         << 9U) | (
                                                   ((0x00000034U 
                                                     == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                    << 8U) 
                                                   | ((0x00000033U 
                                                       == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                      << 7U)))) 
                                    | ((((((0x00000032U 
                                            == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                           << 3U) | 
                                          (((0x00000031U 
                                             == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                            | ((0x00000030U 
                                                == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                               | ((0x0000002fU 
                                                   == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                  | ((0x0000002eU 
                                                      == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                     | ((0x0000002dU 
                                                         == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                        | ((0x0000002cU 
                                                            == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                           | ((0x0000002bU 
                                                               == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                              | (0x0000002aU 
                                                                 == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)))))))) 
                                           << 2U)) 
                                         | ((((0x00000029U 
                                               == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                              | ((0x00000028U 
                                                  == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                 | ((0x00000027U 
                                                     == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                    | ((0x00000026U 
                                                        == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                       | ((0x00000025U 
                                                           == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                          | ((0x00000024U 
                                                              == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                             | ((0x00000023U 
                                                                 == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                                | (0x00000022U 
                                                                   == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)))))))) 
                                             << 1U) 
                                            | ((0x00000021U 
                                                == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                               | ((0x00000020U 
                                                   == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                  | ((0x0000001fU 
                                                      == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                     | ((0x0000001eU 
                                                         == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                        | ((0x0000001dU 
                                                            == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                           | ((0x0000001cU 
                                                               == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                              | ((0x0000001bU 
                                                                  == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                                 | (0x0000001aU 
                                                                    == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)))))))))) 
                                        << 3U) | ((
                                                   (0x00000011U 
                                                    == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                   << 2U) 
                                                  | (((0x00000010U 
                                                       == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                      << 1U) 
                                                     | (0x0000000fU 
                                                        == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b))))) 
                                   << 0x0000000dU) 
                                  | (((((((0x0000000eU 
                                           == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                          << 3U) | 
                                         ((0x0000000dU 
                                           == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                          << 2U)) | 
                                        (((0x0000000cU 
                                           == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                          << 1U) | 
                                         (0x0000000bU 
                                          == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b))) 
                                       << 9U) | (((0x0000000aU 
                                                   == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                  << 8U) 
                                                 | (((9U 
                                                      == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                     << 7U) 
                                                    | ((8U 
                                                        == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                       << 6U)))) 
                                     | ((((7U == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                          << 5U) | 
                                         (((6U == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                           << 4U) | 
                                          ((3U == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                           << 3U))) 
                                        | (((2U == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                            << 2U) 
                                           | (((1U 
                                                == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                               << 1U) 
                                              | (0U 
                                                 == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)))))))))) {
            if ((0U != (((((((((0x00000041U == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                               << 3U) | ((0x00000040U 
                                          == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                         << 2U)) | 
                             (((0x0000003fU == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                               << 1U) | (0x0000003eU 
                                         == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b))) 
                            << 0x0000000aU) | (((0x00000035U 
                                                 == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                << 9U) 
                                               | (((0x00000034U 
                                                    == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                   << 8U) 
                                                  | ((0x00000033U 
                                                      == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                     << 7U)))) 
                          | ((((((0x00000032U == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                 << 3U) | (((0x00000031U 
                                             == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                            | ((0x00000030U 
                                                == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                               | ((0x0000002fU 
                                                   == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                  | ((0x0000002eU 
                                                      == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                     | ((0x0000002dU 
                                                         == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                        | ((0x0000002cU 
                                                            == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                           | ((0x0000002bU 
                                                               == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                              | (0x0000002aU 
                                                                 == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)))))))) 
                                           << 2U)) 
                               | ((((0x00000029U == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                    | ((0x00000028U 
                                        == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                       | ((0x00000027U 
                                           == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                          | ((0x00000026U 
                                              == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                             | ((0x00000025U 
                                                 == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                | ((0x00000024U 
                                                    == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                   | ((0x00000023U 
                                                       == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                      | (0x00000022U 
                                                         == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)))))))) 
                                   << 1U) | ((0x00000021U 
                                              == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                             | ((0x00000020U 
                                                 == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                | ((0x0000001fU 
                                                    == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                   | ((0x0000001eU 
                                                       == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                      | ((0x0000001dU 
                                                          == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                         | ((0x0000001cU 
                                                             == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                            | ((0x0000001bU 
                                                                == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                               | (0x0000001aU 
                                                                  == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)))))))))) 
                              << 3U) | (((0x00000011U 
                                          == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                         << 2U) | (
                                                   ((0x00000010U 
                                                     == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                    << 1U) 
                                                   | (0x0000000fU 
                                                      == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b))))) 
                         << 0x0000000dU) | (((((((0x0000000eU 
                                                  == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                 << 3U) 
                                                | ((0x0000000dU 
                                                    == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                   << 2U)) 
                                               | (((0x0000000cU 
                                                    == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                   << 1U) 
                                                  | (0x0000000bU 
                                                     == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b))) 
                                              << 9U) 
                                             | (((0x0000000aU 
                                                  == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                 << 8U) 
                                                | (((9U 
                                                     == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                    << 7U) 
                                                   | ((8U 
                                                       == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                      << 6U)))) 
                                            | ((((7U 
                                                  == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                 << 5U) 
                                                | (((6U 
                                                     == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                    << 4U) 
                                                   | ((3U 
                                                       == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                      << 3U))) 
                                               | (((2U 
                                                    == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                   << 2U) 
                                                  | (((1U 
                                                       == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                      << 1U) 
                                                     | (0U 
                                                        == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)))))))) {
                if (VL_UNLIKELY((vlSymsp->_vm_contextp__->assertOn()))) {
                    VL_WRITEF_NX("[%0t] %%Error: KL_acmp_lstn_ctx.sv:431: Assertion failed in %m: unique case, but multiple matches found for '32'h%X'\n",4, 'M',vlSymsp->name(),"milan_datapath.acmp_listener_sm.u_ctx.probe_byte", 'T',-9
                                 , '#',64,VL_TIME_UNITED_Q(1000)
                                 , '#',32,vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b);
                    VL_STOP_MT("../../../configs/generated/endstation_ax7101_8x8/../../../hdl/ieee17221/acmp/KL_acmp_lstn_ctx.sv", 431, "");
                }
            }
        }
        vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b 
            = ((IData)(6U) + ((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__beat_r) 
                              << 3U));
        vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT____VlemCall_4__probe_byte 
            = (0x000000ffU & (((((((((0U == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                     | (1U == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                    | (2U == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                   | (3U == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                  | (6U == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                 | (7U == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                | (8U == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                               | (9U == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b))
                               ? ((0U == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                   ? 0x91U : ((1U == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                               ? 0xe0U
                                               : ((2U 
                                                   == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                                   ? 0xf0U
                                                   : 
                                                  ((3U 
                                                    == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                                    ? 1U
                                                    : 
                                                   ((6U 
                                                     == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                                     ? (IData)(
                                                               (vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w 
                                                                >> 0x28U))
                                                     : 
                                                    ((7U 
                                                      == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                                      ? (IData)(
                                                                (vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w 
                                                                 >> 0x20U))
                                                      : 
                                                     ((8U 
                                                       == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                                       ? (IData)(
                                                                 (vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w 
                                                                  >> 0x18U))
                                                       : (IData)(
                                                                 (vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w 
                                                                  >> 0x10U)))))))))
                               : (((((((((0x0000000aU 
                                          == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                         | (0x0000000bU 
                                            == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                        | (0x0000000cU 
                                           == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                       | (0x0000000dU 
                                          == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                      | (0x0000000eU 
                                         == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                     | (0x0000000fU 
                                        == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                    | (0x00000010U 
                                       == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                   | (0x00000011U == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b))
                                   ? ((0x0000000aU 
                                       == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                       ? (IData)((vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w 
                                                  >> 8U))
                                       : ((0x0000000bU 
                                           == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                           ? (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w)
                                           : ((0x0000000cU 
                                               == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                               ? 0x22U
                                               : ((0x0000000dU 
                                                   == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                                   ? 0xf0U
                                                   : 
                                                  ((0x0000000eU 
                                                    == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                                    ? 0xfcU
                                                    : 
                                                   ((0x0000000fU 
                                                     == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                                     ? 0U
                                                     : 
                                                    ((0x00000010U 
                                                      == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                                      ? 0U
                                                      : 0x2cU)))))))
                                   : ((((((((((((((
                                                   ((0x0000001aU 
                                                     == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                    || (0x0000001bU 
                                                        == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                   || (0x0000001cU 
                                                       == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                  || (0x0000001dU 
                                                      == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                 || (0x0000001eU 
                                                     == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                || (0x0000001fU 
                                                    == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                               || (0x00000020U 
                                                   == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                              || (0x00000021U 
                                                  == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                             | ((((((((0x00000022U 
                                                       == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                      || (0x00000023U 
                                                          == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                     || (0x00000024U 
                                                         == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                    || (0x00000025U 
                                                        == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                   || (0x00000026U 
                                                       == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                  || (0x00000027U 
                                                      == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                 || (0x00000028U 
                                                     == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                || (0x00000029U 
                                                    == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b))) 
                                            | ((((((((0x0000002aU 
                                                      == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                     || (0x0000002bU 
                                                         == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                    || (0x0000002cU 
                                                        == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                   || (0x0000002dU 
                                                       == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                  || (0x0000002eU 
                                                      == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                 || (0x0000002fU 
                                                     == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                || (0x00000030U 
                                                    == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                               || (0x00000031U 
                                                   == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b))) 
                                           | (0x00000032U 
                                              == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                          | (0x00000033U 
                                             == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                         | (0x00000034U 
                                            == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                        | (0x00000035U 
                                           == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                       | (0x0000003eU 
                                          == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b))
                                       ? (((((((((0x0000001aU 
                                                  == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                 || (0x0000001bU 
                                                     == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                || (0x0000001cU 
                                                    == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                               || (0x0000001dU 
                                                   == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                              || (0x0000001eU 
                                                  == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                             || (0x0000001fU 
                                                 == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                            || (0x00000020U 
                                                == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                           || (0x00000021U 
                                               == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b))
                                           ? (((0U 
                                                == 
                                                (0x0000001fU 
                                                 & VL_MULS_III(32, (IData)(8U), 
                                                               ((IData)(0x00000021U) 
                                                                - vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b))))
                                                ? 0U
                                                : (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r
                                                   [
                                                   (((IData)(7U) 
                                                     + 
                                                     (0x0000003fU 
                                                      & VL_MULS_III(32, (IData)(8U), 
                                                                    ((IData)(0x00000021U) 
                                                                     - vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)))) 
                                                    >> 5U)] 
                                                   << 
                                                   ((IData)(0x00000020U) 
                                                    - 
                                                    (0x0000001fU 
                                                     & VL_MULS_III(32, (IData)(8U), 
                                                                   ((IData)(0x00000021U) 
                                                                    - vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)))))) 
                                              | (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r
                                                 [(1U 
                                                   & (VL_MULS_III(32, (IData)(8U), 
                                                                  ((IData)(0x00000021U) 
                                                                   - vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                      >> 5U))] 
                                                 >> 
                                                 (0x0000001fU 
                                                  & VL_MULS_III(32, (IData)(8U), 
                                                                ((IData)(0x00000021U) 
                                                                 - vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)))))
                                           : ((((((
                                                   (((0x00000022U 
                                                      == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                     || (0x00000023U 
                                                         == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                    || (0x00000024U 
                                                        == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                   || (0x00000025U 
                                                       == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                  || (0x00000026U 
                                                      == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                 || (0x00000027U 
                                                     == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                || (0x00000028U 
                                                    == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                               || (0x00000029U 
                                                   == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b))
                                               ? ((
                                                   (0U 
                                                    == 
                                                    (0x0000001fU 
                                                     & ((IData)(0x00000040U) 
                                                        + 
                                                        (0x0000003fU 
                                                         & VL_MULS_III(32, (IData)(8U), 
                                                                       ((IData)(0x00000029U) 
                                                                        - vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b))))))
                                                    ? 0U
                                                    : 
                                                   (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r
                                                    [
                                                    (((IData)(0x00000047U) 
                                                      + 
                                                      (0x0000003fU 
                                                       & VL_MULS_III(32, (IData)(8U), 
                                                                     ((IData)(0x00000029U) 
                                                                      - vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)))) 
                                                     >> 5U)] 
                                                    << 
                                                    ((IData)(0x00000020U) 
                                                     - 
                                                     (0x0000001fU 
                                                      & ((IData)(0x00000040U) 
                                                         + 
                                                         (0x0000003fU 
                                                          & VL_MULS_III(32, (IData)(8U), 
                                                                        ((IData)(0x00000029U) 
                                                                         - vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)))))))) 
                                                  | (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r
                                                     [
                                                     (((IData)(0x00000040U) 
                                                       + 
                                                       (0x0000003fU 
                                                        & VL_MULS_III(32, (IData)(8U), 
                                                                      ((IData)(0x00000029U) 
                                                                       - vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)))) 
                                                      >> 5U)] 
                                                     >> 
                                                     (0x0000001fU 
                                                      & ((IData)(0x00000040U) 
                                                         + 
                                                         (0x0000003fU 
                                                          & VL_MULS_III(32, (IData)(8U), 
                                                                        ((IData)(0x00000029U) 
                                                                         - vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)))))))
                                               : ((
                                                   (((((((0x0000002aU 
                                                          == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                         || (0x0000002bU 
                                                             == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                        || (0x0000002cU 
                                                            == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                       || (0x0000002dU 
                                                           == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                      || (0x0000002eU 
                                                          == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                     || (0x0000002fU 
                                                         == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                    || (0x00000030U 
                                                        == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                   || (0x00000031U 
                                                       == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b))
                                                   ? (IData)(
                                                             (vlSelfRef.milan_datapath__DOT__cfg_adp_entity_id 
                                                              >> 
                                                              (0x0000003fU 
                                                               & VL_MULS_III(32, (IData)(8U), 
                                                                             ((IData)(0x00000031U) 
                                                                              - vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)))))
                                                   : 
                                                  ((0x00000032U 
                                                    == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                                    ? 
                                                   ((vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r[8U] 
                                                     << 0x0000000cU) 
                                                    | (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r[8U] 
                                                       >> 0x00000014U))
                                                    : 
                                                   ((0x00000033U 
                                                     == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                                     ? 
                                                    ((vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r[8U] 
                                                      << 0x00000014U) 
                                                     | (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r[8U] 
                                                        >> 0x0000000cU))
                                                     : 
                                                    ((0x00000034U 
                                                      == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                                      ? 0U
                                                      : 
                                                     ((0x00000035U 
                                                       == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                                       ? (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_idx_r)
                                                       : 
                                                      ((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_seq_r) 
                                                       >> 8U))))))))
                                       : ((0x0000003fU 
                                           == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                           ? (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_seq_r)
                                           : ((0x00000040U 
                                               == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                               ? ((vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r[8U] 
                                                   << 0x0000001cU) 
                                                  | (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r[8U] 
                                                     >> 4U))
                                               : ((0x00000041U 
                                                   == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                                   ? 
                                                  (0xb7U 
                                                   & ((vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r[8U] 
                                                       << 4U) 
                                                      | (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r[7U] 
                                                         >> 0x0000001cU)))
                                                   : 0U)))))));
        vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_beat 
            = ((0xff00ffffffffffffULL & vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_beat) 
               | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT____VlemCall_4__probe_byte)) 
                  << 0x00000030U));
        if ((1U & (~ VL_ONEHOT_I((((((((((0x00000041U 
                                          == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                         << 3U) | (
                                                   (0x00000040U 
                                                    == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                   << 2U)) 
                                       | (((0x0000003fU 
                                            == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                           << 1U) | 
                                          (0x0000003eU 
                                           == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b))) 
                                      << 0x0000000aU) 
                                     | (((0x00000035U 
                                          == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                         << 9U) | (
                                                   ((0x00000034U 
                                                     == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                    << 8U) 
                                                   | ((0x00000033U 
                                                       == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                      << 7U)))) 
                                    | ((((((0x00000032U 
                                            == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                           << 3U) | 
                                          (((0x00000031U 
                                             == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                            | ((0x00000030U 
                                                == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                               | ((0x0000002fU 
                                                   == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                  | ((0x0000002eU 
                                                      == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                     | ((0x0000002dU 
                                                         == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                        | ((0x0000002cU 
                                                            == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                           | ((0x0000002bU 
                                                               == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                              | (0x0000002aU 
                                                                 == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)))))))) 
                                           << 2U)) 
                                         | ((((0x00000029U 
                                               == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                              | ((0x00000028U 
                                                  == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                 | ((0x00000027U 
                                                     == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                    | ((0x00000026U 
                                                        == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                       | ((0x00000025U 
                                                           == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                          | ((0x00000024U 
                                                              == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                             | ((0x00000023U 
                                                                 == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                                | (0x00000022U 
                                                                   == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)))))))) 
                                             << 1U) 
                                            | ((0x00000021U 
                                                == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                               | ((0x00000020U 
                                                   == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                  | ((0x0000001fU 
                                                      == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                     | ((0x0000001eU 
                                                         == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                        | ((0x0000001dU 
                                                            == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                           | ((0x0000001cU 
                                                               == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                              | ((0x0000001bU 
                                                                  == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                                 | (0x0000001aU 
                                                                    == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)))))))))) 
                                        << 3U) | ((
                                                   (0x00000011U 
                                                    == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                   << 2U) 
                                                  | (((0x00000010U 
                                                       == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                      << 1U) 
                                                     | (0x0000000fU 
                                                        == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b))))) 
                                   << 0x0000000dU) 
                                  | (((((((0x0000000eU 
                                           == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                          << 3U) | 
                                         ((0x0000000dU 
                                           == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                          << 2U)) | 
                                        (((0x0000000cU 
                                           == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                          << 1U) | 
                                         (0x0000000bU 
                                          == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b))) 
                                       << 9U) | (((0x0000000aU 
                                                   == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                  << 8U) 
                                                 | (((9U 
                                                      == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                     << 7U) 
                                                    | ((8U 
                                                        == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                       << 6U)))) 
                                     | ((((7U == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                          << 5U) | 
                                         (((6U == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                           << 4U) | 
                                          ((3U == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                           << 3U))) 
                                        | (((2U == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                            << 2U) 
                                           | (((1U 
                                                == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                               << 1U) 
                                              | (0U 
                                                 == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)))))))))) {
            if ((0U != (((((((((0x00000041U == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                               << 3U) | ((0x00000040U 
                                          == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                         << 2U)) | 
                             (((0x0000003fU == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                               << 1U) | (0x0000003eU 
                                         == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b))) 
                            << 0x0000000aU) | (((0x00000035U 
                                                 == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                << 9U) 
                                               | (((0x00000034U 
                                                    == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                   << 8U) 
                                                  | ((0x00000033U 
                                                      == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                     << 7U)))) 
                          | ((((((0x00000032U == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                 << 3U) | (((0x00000031U 
                                             == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                            | ((0x00000030U 
                                                == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                               | ((0x0000002fU 
                                                   == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                  | ((0x0000002eU 
                                                      == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                     | ((0x0000002dU 
                                                         == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                        | ((0x0000002cU 
                                                            == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                           | ((0x0000002bU 
                                                               == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                              | (0x0000002aU 
                                                                 == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)))))))) 
                                           << 2U)) 
                               | ((((0x00000029U == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                    | ((0x00000028U 
                                        == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                       | ((0x00000027U 
                                           == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                          | ((0x00000026U 
                                              == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                             | ((0x00000025U 
                                                 == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                | ((0x00000024U 
                                                    == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                   | ((0x00000023U 
                                                       == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                      | (0x00000022U 
                                                         == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)))))))) 
                                   << 1U) | ((0x00000021U 
                                              == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                             | ((0x00000020U 
                                                 == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                | ((0x0000001fU 
                                                    == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                   | ((0x0000001eU 
                                                       == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                      | ((0x0000001dU 
                                                          == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                         | ((0x0000001cU 
                                                             == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                            | ((0x0000001bU 
                                                                == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                               | (0x0000001aU 
                                                                  == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)))))))))) 
                              << 3U) | (((0x00000011U 
                                          == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                         << 2U) | (
                                                   ((0x00000010U 
                                                     == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                    << 1U) 
                                                   | (0x0000000fU 
                                                      == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b))))) 
                         << 0x0000000dU) | (((((((0x0000000eU 
                                                  == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                 << 3U) 
                                                | ((0x0000000dU 
                                                    == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                   << 2U)) 
                                               | (((0x0000000cU 
                                                    == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                   << 1U) 
                                                  | (0x0000000bU 
                                                     == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b))) 
                                              << 9U) 
                                             | (((0x0000000aU 
                                                  == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                 << 8U) 
                                                | (((9U 
                                                     == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                    << 7U) 
                                                   | ((8U 
                                                       == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                      << 6U)))) 
                                            | ((((7U 
                                                  == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                 << 5U) 
                                                | (((6U 
                                                     == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                    << 4U) 
                                                   | ((3U 
                                                       == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                      << 3U))) 
                                               | (((2U 
                                                    == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                   << 2U) 
                                                  | (((1U 
                                                       == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                      << 1U) 
                                                     | (0U 
                                                        == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)))))))) {
                if (VL_UNLIKELY((vlSymsp->_vm_contextp__->assertOn()))) {
                    VL_WRITEF_NX("[%0t] %%Error: KL_acmp_lstn_ctx.sv:431: Assertion failed in %m: unique case, but multiple matches found for '32'h%X'\n",4, 'M',vlSymsp->name(),"milan_datapath.acmp_listener_sm.u_ctx.probe_byte", 'T',-9
                                 , '#',64,VL_TIME_UNITED_Q(1000)
                                 , '#',32,vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b);
                    VL_STOP_MT("../../../configs/generated/endstation_ax7101_8x8/../../../hdl/ieee17221/acmp/KL_acmp_lstn_ctx.sv", 431, "");
                }
            }
        }
        vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b 
            = ((IData)(7U) + ((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__beat_r) 
                              << 3U));
        if ((1U & (~ VL_ONEHOT_I((((((((((0x00000041U 
                                          == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                         << 3U) | (
                                                   (0x00000040U 
                                                    == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                   << 2U)) 
                                       | (((0x0000003fU 
                                            == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                           << 1U) | 
                                          (0x0000003eU 
                                           == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b))) 
                                      << 0x0000000aU) 
                                     | (((0x00000035U 
                                          == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                         << 9U) | (
                                                   ((0x00000034U 
                                                     == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                    << 8U) 
                                                   | ((0x00000033U 
                                                       == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                      << 7U)))) 
                                    | ((((((0x00000032U 
                                            == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                           << 3U) | 
                                          (((0x00000031U 
                                             == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                            | ((0x00000030U 
                                                == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                               | ((0x0000002fU 
                                                   == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                  | ((0x0000002eU 
                                                      == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                     | ((0x0000002dU 
                                                         == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                        | ((0x0000002cU 
                                                            == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                           | ((0x0000002bU 
                                                               == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                              | (0x0000002aU 
                                                                 == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)))))))) 
                                           << 2U)) 
                                         | ((((0x00000029U 
                                               == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                              | ((0x00000028U 
                                                  == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                 | ((0x00000027U 
                                                     == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                    | ((0x00000026U 
                                                        == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                       | ((0x00000025U 
                                                           == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                          | ((0x00000024U 
                                                              == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                             | ((0x00000023U 
                                                                 == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                                | (0x00000022U 
                                                                   == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)))))))) 
                                             << 1U) 
                                            | ((0x00000021U 
                                                == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                               | ((0x00000020U 
                                                   == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                  | ((0x0000001fU 
                                                      == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                     | ((0x0000001eU 
                                                         == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                        | ((0x0000001dU 
                                                            == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                           | ((0x0000001cU 
                                                               == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                              | ((0x0000001bU 
                                                                  == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                                 | (0x0000001aU 
                                                                    == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)))))))))) 
                                        << 3U) | ((
                                                   (0x00000011U 
                                                    == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                   << 2U) 
                                                  | (((0x00000010U 
                                                       == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                      << 1U) 
                                                     | (0x0000000fU 
                                                        == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b))))) 
                                   << 0x0000000dU) 
                                  | (((((((0x0000000eU 
                                           == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                          << 3U) | 
                                         ((0x0000000dU 
                                           == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                          << 2U)) | 
                                        (((0x0000000cU 
                                           == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                          << 1U) | 
                                         (0x0000000bU 
                                          == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b))) 
                                       << 9U) | (((0x0000000aU 
                                                   == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                  << 8U) 
                                                 | (((9U 
                                                      == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                     << 7U) 
                                                    | ((8U 
                                                        == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                       << 6U)))) 
                                     | ((((7U == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                          << 5U) | 
                                         (((6U == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                           << 4U) | 
                                          ((3U == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                           << 3U))) 
                                        | (((2U == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                            << 2U) 
                                           | (((1U 
                                                == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                               << 1U) 
                                              | (0U 
                                                 == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)))))))))) {
            if ((0U != (((((((((0x00000041U == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                               << 3U) | ((0x00000040U 
                                          == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                         << 2U)) | 
                             (((0x0000003fU == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                               << 1U) | (0x0000003eU 
                                         == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b))) 
                            << 0x0000000aU) | (((0x00000035U 
                                                 == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                << 9U) 
                                               | (((0x00000034U 
                                                    == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                   << 8U) 
                                                  | ((0x00000033U 
                                                      == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                     << 7U)))) 
                          | ((((((0x00000032U == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                 << 3U) | (((0x00000031U 
                                             == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                            | ((0x00000030U 
                                                == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                               | ((0x0000002fU 
                                                   == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                  | ((0x0000002eU 
                                                      == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                     | ((0x0000002dU 
                                                         == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                        | ((0x0000002cU 
                                                            == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                           | ((0x0000002bU 
                                                               == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                              | (0x0000002aU 
                                                                 == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)))))))) 
                                           << 2U)) 
                               | ((((0x00000029U == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                    | ((0x00000028U 
                                        == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                       | ((0x00000027U 
                                           == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                          | ((0x00000026U 
                                              == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                             | ((0x00000025U 
                                                 == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                | ((0x00000024U 
                                                    == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                   | ((0x00000023U 
                                                       == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                      | (0x00000022U 
                                                         == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)))))))) 
                                   << 1U) | ((0x00000021U 
                                              == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                             | ((0x00000020U 
                                                 == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                | ((0x0000001fU 
                                                    == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                   | ((0x0000001eU 
                                                       == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                      | ((0x0000001dU 
                                                          == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                         | ((0x0000001cU 
                                                             == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                            | ((0x0000001bU 
                                                                == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                               | (0x0000001aU 
                                                                  == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)))))))))) 
                              << 3U) | (((0x00000011U 
                                          == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                         << 2U) | (
                                                   ((0x00000010U 
                                                     == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                    << 1U) 
                                                   | (0x0000000fU 
                                                      == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b))))) 
                         << 0x0000000dU) | (((((((0x0000000eU 
                                                  == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                 << 3U) 
                                                | ((0x0000000dU 
                                                    == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                   << 2U)) 
                                               | (((0x0000000cU 
                                                    == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                   << 1U) 
                                                  | (0x0000000bU 
                                                     == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b))) 
                                              << 9U) 
                                             | (((0x0000000aU 
                                                  == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                 << 8U) 
                                                | (((9U 
                                                     == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                    << 7U) 
                                                   | ((8U 
                                                       == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                      << 6U)))) 
                                            | ((((7U 
                                                  == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                 << 5U) 
                                                | (((6U 
                                                     == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                    << 4U) 
                                                   | ((3U 
                                                       == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                      << 3U))) 
                                               | (((2U 
                                                    == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                   << 2U) 
                                                  | (((1U 
                                                       == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                      << 1U) 
                                                     | (0U 
                                                        == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)))))))) {
                if (VL_UNLIKELY((vlSymsp->_vm_contextp__->assertOn()))) {
                    VL_WRITEF_NX("[%0t] %%Error: KL_acmp_lstn_ctx.sv:431: Assertion failed in %m: unique case, but multiple matches found for '32'h%X'\n",4, 'M',vlSymsp->name(),"milan_datapath.acmp_listener_sm.u_ctx.probe_byte", 'T',-9
                                 , '#',64,VL_TIME_UNITED_Q(1000)
                                 , '#',32,vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b);
                    VL_STOP_MT("../../../configs/generated/endstation_ax7101_8x8/../../../hdl/ieee17221/acmp/KL_acmp_lstn_ctx.sv", 431, "");
                }
            }
        }
        vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT____VlemCall_4__probe_byte 
            = (0x000000ffU & (((((((((0U == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                     | (1U == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                    | (2U == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                   | (3U == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                  | (6U == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                 | (7U == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                | (8U == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                               | (9U == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b))
                               ? ((0U == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                   ? 0x91U : ((1U == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                               ? 0xe0U
                                               : ((2U 
                                                   == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                                   ? 0xf0U
                                                   : 
                                                  ((3U 
                                                    == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                                    ? 1U
                                                    : 
                                                   ((6U 
                                                     == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                                     ? (IData)(
                                                               (vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w 
                                                                >> 0x28U))
                                                     : 
                                                    ((7U 
                                                      == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                                      ? (IData)(
                                                                (vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w 
                                                                 >> 0x20U))
                                                      : 
                                                     ((8U 
                                                       == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                                       ? (IData)(
                                                                 (vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w 
                                                                  >> 0x18U))
                                                       : (IData)(
                                                                 (vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w 
                                                                  >> 0x10U)))))))))
                               : (((((((((0x0000000aU 
                                          == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                         | (0x0000000bU 
                                            == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                        | (0x0000000cU 
                                           == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                       | (0x0000000dU 
                                          == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                      | (0x0000000eU 
                                         == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                     | (0x0000000fU 
                                        == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                    | (0x00000010U 
                                       == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                   | (0x00000011U == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b))
                                   ? ((0x0000000aU 
                                       == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                       ? (IData)((vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w 
                                                  >> 8U))
                                       : ((0x0000000bU 
                                           == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                           ? (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w)
                                           : ((0x0000000cU 
                                               == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                               ? 0x22U
                                               : ((0x0000000dU 
                                                   == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                                   ? 0xf0U
                                                   : 
                                                  ((0x0000000eU 
                                                    == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                                    ? 0xfcU
                                                    : 
                                                   ((0x0000000fU 
                                                     == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                                     ? 0U
                                                     : 
                                                    ((0x00000010U 
                                                      == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                                      ? 0U
                                                      : 0x2cU)))))))
                                   : ((((((((((((((
                                                   ((0x0000001aU 
                                                     == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                    || (0x0000001bU 
                                                        == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                   || (0x0000001cU 
                                                       == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                  || (0x0000001dU 
                                                      == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                 || (0x0000001eU 
                                                     == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                || (0x0000001fU 
                                                    == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                               || (0x00000020U 
                                                   == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                              || (0x00000021U 
                                                  == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                             | ((((((((0x00000022U 
                                                       == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                      || (0x00000023U 
                                                          == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                     || (0x00000024U 
                                                         == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                    || (0x00000025U 
                                                        == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                   || (0x00000026U 
                                                       == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                  || (0x00000027U 
                                                      == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                 || (0x00000028U 
                                                     == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                || (0x00000029U 
                                                    == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b))) 
                                            | ((((((((0x0000002aU 
                                                      == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                     || (0x0000002bU 
                                                         == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                    || (0x0000002cU 
                                                        == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                   || (0x0000002dU 
                                                       == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                  || (0x0000002eU 
                                                      == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                 || (0x0000002fU 
                                                     == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                || (0x00000030U 
                                                    == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                               || (0x00000031U 
                                                   == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b))) 
                                           | (0x00000032U 
                                              == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                          | (0x00000033U 
                                             == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                         | (0x00000034U 
                                            == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                        | (0x00000035U 
                                           == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                       | (0x0000003eU 
                                          == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b))
                                       ? (((((((((0x0000001aU 
                                                  == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                 || (0x0000001bU 
                                                     == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                || (0x0000001cU 
                                                    == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                               || (0x0000001dU 
                                                   == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                              || (0x0000001eU 
                                                  == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                             || (0x0000001fU 
                                                 == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                            || (0x00000020U 
                                                == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                           || (0x00000021U 
                                               == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b))
                                           ? (((0U 
                                                == 
                                                (0x0000001fU 
                                                 & VL_MULS_III(32, (IData)(8U), 
                                                               ((IData)(0x00000021U) 
                                                                - vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b))))
                                                ? 0U
                                                : (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r
                                                   [
                                                   (((IData)(7U) 
                                                     + 
                                                     (0x0000003fU 
                                                      & VL_MULS_III(32, (IData)(8U), 
                                                                    ((IData)(0x00000021U) 
                                                                     - vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)))) 
                                                    >> 5U)] 
                                                   << 
                                                   ((IData)(0x00000020U) 
                                                    - 
                                                    (0x0000001fU 
                                                     & VL_MULS_III(32, (IData)(8U), 
                                                                   ((IData)(0x00000021U) 
                                                                    - vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)))))) 
                                              | (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r
                                                 [(1U 
                                                   & (VL_MULS_III(32, (IData)(8U), 
                                                                  ((IData)(0x00000021U) 
                                                                   - vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                      >> 5U))] 
                                                 >> 
                                                 (0x0000001fU 
                                                  & VL_MULS_III(32, (IData)(8U), 
                                                                ((IData)(0x00000021U) 
                                                                 - vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)))))
                                           : ((((((
                                                   (((0x00000022U 
                                                      == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                     || (0x00000023U 
                                                         == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                    || (0x00000024U 
                                                        == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                   || (0x00000025U 
                                                       == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                  || (0x00000026U 
                                                      == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                 || (0x00000027U 
                                                     == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                || (0x00000028U 
                                                    == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                               || (0x00000029U 
                                                   == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b))
                                               ? ((
                                                   (0U 
                                                    == 
                                                    (0x0000001fU 
                                                     & ((IData)(0x00000040U) 
                                                        + 
                                                        (0x0000003fU 
                                                         & VL_MULS_III(32, (IData)(8U), 
                                                                       ((IData)(0x00000029U) 
                                                                        - vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b))))))
                                                    ? 0U
                                                    : 
                                                   (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r
                                                    [
                                                    (((IData)(0x00000047U) 
                                                      + 
                                                      (0x0000003fU 
                                                       & VL_MULS_III(32, (IData)(8U), 
                                                                     ((IData)(0x00000029U) 
                                                                      - vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)))) 
                                                     >> 5U)] 
                                                    << 
                                                    ((IData)(0x00000020U) 
                                                     - 
                                                     (0x0000001fU 
                                                      & ((IData)(0x00000040U) 
                                                         + 
                                                         (0x0000003fU 
                                                          & VL_MULS_III(32, (IData)(8U), 
                                                                        ((IData)(0x00000029U) 
                                                                         - vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)))))))) 
                                                  | (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r
                                                     [
                                                     (((IData)(0x00000040U) 
                                                       + 
                                                       (0x0000003fU 
                                                        & VL_MULS_III(32, (IData)(8U), 
                                                                      ((IData)(0x00000029U) 
                                                                       - vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)))) 
                                                      >> 5U)] 
                                                     >> 
                                                     (0x0000001fU 
                                                      & ((IData)(0x00000040U) 
                                                         + 
                                                         (0x0000003fU 
                                                          & VL_MULS_III(32, (IData)(8U), 
                                                                        ((IData)(0x00000029U) 
                                                                         - vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)))))))
                                               : ((
                                                   (((((((0x0000002aU 
                                                          == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b) 
                                                         || (0x0000002bU 
                                                             == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                        || (0x0000002cU 
                                                            == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                       || (0x0000002dU 
                                                           == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                      || (0x0000002eU 
                                                          == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                     || (0x0000002fU 
                                                         == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                    || (0x00000030U 
                                                        == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)) 
                                                   || (0x00000031U 
                                                       == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b))
                                                   ? (IData)(
                                                             (vlSelfRef.milan_datapath__DOT__cfg_adp_entity_id 
                                                              >> 
                                                              (0x0000003fU 
                                                               & VL_MULS_III(32, (IData)(8U), 
                                                                             ((IData)(0x00000031U) 
                                                                              - vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)))))
                                                   : 
                                                  ((0x00000032U 
                                                    == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                                    ? 
                                                   ((vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r[8U] 
                                                     << 0x0000000cU) 
                                                    | (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r[8U] 
                                                       >> 0x00000014U))
                                                    : 
                                                   ((0x00000033U 
                                                     == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                                     ? 
                                                    ((vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r[8U] 
                                                      << 0x00000014U) 
                                                     | (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r[8U] 
                                                        >> 0x0000000cU))
                                                     : 
                                                    ((0x00000034U 
                                                      == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                                      ? 0U
                                                      : 
                                                     ((0x00000035U 
                                                       == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                                       ? (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_idx_r)
                                                       : 
                                                      ((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_seq_r) 
                                                       >> 8U))))))))
                                       : ((0x0000003fU 
                                           == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                           ? (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_seq_r)
                                           : ((0x00000040U 
                                               == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                               ? ((vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r[8U] 
                                                   << 0x0000001cU) 
                                                  | (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r[8U] 
                                                     >> 4U))
                                               : ((0x00000041U 
                                                   == vlSelfRef.__Vfunc_milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_byte__149__b)
                                                   ? 
                                                  (0xb7U 
                                                   & ((vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r[8U] 
                                                       << 4U) 
                                                      | (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_r[7U] 
                                                         >> 0x0000001cU)))
                                                   : 0U)))))));
        vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_beat 
            = ((0x00ffffffffffffffULL & vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_beat) 
               | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT____VlemCall_4__probe_byte)) 
                  << 0x00000038U));
    } else {
        vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_beat 
            = milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_resp;
    }
    vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__st_ovl_byte_w 
        = vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__st_rom_byte_w;
    if ((0x00000080U & (IData)(vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_dyn__DOT__w_ovl))) {
        if ((0x00000040U & (IData)(vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_dyn__DOT__w_ovl))) {
            if ((0x00000020U & (IData)(vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_dyn__DOT__w_ovl))) {
                if ((0x00000010U & (IData)(vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_dyn__DOT__w_ovl))) {
                    vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__st_ovl_byte_w 
                        = vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__st_rom_byte_w;
                } else if ((8U & (IData)(vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_dyn__DOT__w_ovl))) {
                    if ((0ULL != vlSelfRef.milan_datapath__DOT__cfg_entity_name8)) {
                        vlSelfRef.__Vfunc_milan_datapath__DOT__aecp_listener__DOT__u_dyn__DOT__pick64__82__n 
                            = (7U & (IData)(vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_dyn__DOT__w_ovl));
                        vlSelfRef.__Vfunc_milan_datapath__DOT__aecp_listener__DOT__u_dyn__DOT__pick64__82__v 
                            = vlSelfRef.milan_datapath__DOT__cfg_entity_name8;
                        vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_dyn__DOT____VlemCall_0__pick64 
                            = (0x000000ffU & (IData)(
                                                     (vlSelfRef.__Vfunc_milan_datapath__DOT__aecp_listener__DOT__u_dyn__DOT__pick64__82__v 
                                                      >> 
                                                      (0x0000003fU 
                                                       & (((IData)(7U) 
                                                           - (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__aecp_listener__DOT__u_dyn__DOT__pick64__82__n)) 
                                                          << 3U)))));
                    } else {
                        vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_dyn__DOT____VlemCall_0__pick64 
                            = vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__st_rom_byte_w;
                    }
                    vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__st_ovl_byte_w 
                        = vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_dyn__DOT____VlemCall_0__pick64;
                } else {
                    vlSelfRef.__Vfunc_milan_datapath__DOT__aecp_listener__DOT__u_dyn__DOT__pick64__83__n 
                        = (7U & (IData)(vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_dyn__DOT__w_ovl));
                    vlSelfRef.__Vfunc_milan_datapath__DOT__aecp_listener__DOT__u_dyn__DOT__pick64__83__v 
                        = vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_dyn__DOT__w_clock_id;
                    vlSelfRef.__Vfunc_milan_datapath__DOT__aecp_listener__DOT__u_dyn__DOT__pick64__83__Vfuncout 
                        = (0x000000ffU & (IData)((vlSelfRef.__Vfunc_milan_datapath__DOT__aecp_listener__DOT__u_dyn__DOT__pick64__83__v 
                                                  >> 
                                                  (0x0000003fU 
                                                   & (((IData)(7U) 
                                                       - (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__aecp_listener__DOT__u_dyn__DOT__pick64__83__n)) 
                                                      << 3U)))));
                    vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__st_ovl_byte_w 
                        = vlSelfRef.__Vfunc_milan_datapath__DOT__aecp_listener__DOT__u_dyn__DOT__pick64__83__Vfuncout;
                }
            } else if ((0x00000010U & (IData)(vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_dyn__DOT__w_ovl))) {
                if ((8U & (IData)(vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_dyn__DOT__w_ovl))) {
                    vlSelfRef.__Vfunc_milan_datapath__DOT__aecp_listener__DOT__u_dyn__DOT__pick64__84__n 
                        = (7U & ((IData)(2U) + (IData)(vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_dyn__DOT__w_ovl)));
                    vlSelfRef.__Vfunc_milan_datapath__DOT__aecp_listener__DOT__u_dyn__DOT__pick64__84__v 
                        = vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w;
                    vlSelfRef.__Vfunc_milan_datapath__DOT__aecp_listener__DOT__u_dyn__DOT__pick64__84__Vfuncout 
                        = (0x000000ffU & (IData)((vlSelfRef.__Vfunc_milan_datapath__DOT__aecp_listener__DOT__u_dyn__DOT__pick64__84__v 
                                                  >> 
                                                  (0x0000003fU 
                                                   & (((IData)(7U) 
                                                       - (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__aecp_listener__DOT__u_dyn__DOT__pick64__84__n)) 
                                                      << 3U)))));
                    vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__st_ovl_byte_w 
                        = vlSelfRef.__Vfunc_milan_datapath__DOT__aecp_listener__DOT__u_dyn__DOT__pick64__84__Vfuncout;
                } else {
                    vlSelfRef.__Vfunc_milan_datapath__DOT__aecp_listener__DOT__u_dyn__DOT__pick64__85__n 
                        = (7U & ((IData)(6U) + (IData)(vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_dyn__DOT__w_ovl)));
                    vlSelfRef.__Vfunc_milan_datapath__DOT__aecp_listener__DOT__u_dyn__DOT__pick64__85__v 
                        = (QData)((IData)(vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_l0__DOT__current_config_r));
                    vlSelfRef.__Vfunc_milan_datapath__DOT__aecp_listener__DOT__u_dyn__DOT__pick64__85__Vfuncout 
                        = (0x000000ffU & (IData)((vlSelfRef.__Vfunc_milan_datapath__DOT__aecp_listener__DOT__u_dyn__DOT__pick64__85__v 
                                                  >> 
                                                  (0x0000003fU 
                                                   & (((IData)(7U) 
                                                       - (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__aecp_listener__DOT__u_dyn__DOT__pick64__85__n)) 
                                                      << 3U)))));
                    vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__st_ovl_byte_w 
                        = vlSelfRef.__Vfunc_milan_datapath__DOT__aecp_listener__DOT__u_dyn__DOT__pick64__85__Vfuncout;
                }
            } else if ((8U & (IData)(vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_dyn__DOT__w_ovl))) {
                vlSelfRef.__Vfunc_milan_datapath__DOT__aecp_listener__DOT__u_dyn__DOT__pick64__86__n 
                    = (7U & (IData)(vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_dyn__DOT__w_ovl));
                vlSelfRef.__Vfunc_milan_datapath__DOT__aecp_listener__DOT__u_dyn__DOT__pick64__86__v 
                    = vlSelfRef.milan_datapath__DOT__cfg_adp_association_id;
                vlSelfRef.__Vfunc_milan_datapath__DOT__aecp_listener__DOT__u_dyn__DOT__pick64__86__Vfuncout 
                    = (0x000000ffU & (IData)((vlSelfRef.__Vfunc_milan_datapath__DOT__aecp_listener__DOT__u_dyn__DOT__pick64__86__v 
                                              >> (0x0000003fU 
                                                  & (((IData)(7U) 
                                                      - (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__aecp_listener__DOT__u_dyn__DOT__pick64__86__n)) 
                                                     << 3U)))));
                vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__st_ovl_byte_w 
                    = vlSelfRef.__Vfunc_milan_datapath__DOT__aecp_listener__DOT__u_dyn__DOT__pick64__86__Vfuncout;
            } else {
                vlSelfRef.__Vfunc_milan_datapath__DOT__aecp_listener__DOT__u_dyn__DOT__pick64__87__n 
                    = (7U & ((IData)(4U) + (IData)(vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_dyn__DOT__w_ovl)));
                vlSelfRef.__Vfunc_milan_datapath__DOT__aecp_listener__DOT__u_dyn__DOT__pick64__87__v 
                    = (QData)((IData)(vlSelfRef.milan_datapath__DOT__adp_available_index));
                vlSelfRef.__Vfunc_milan_datapath__DOT__aecp_listener__DOT__u_dyn__DOT__pick64__87__Vfuncout 
                    = (0x000000ffU & (IData)((vlSelfRef.__Vfunc_milan_datapath__DOT__aecp_listener__DOT__u_dyn__DOT__pick64__87__v 
                                              >> (0x0000003fU 
                                                  & (((IData)(7U) 
                                                      - (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__aecp_listener__DOT__u_dyn__DOT__pick64__87__n)) 
                                                     << 3U)))));
                vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__st_ovl_byte_w 
                    = vlSelfRef.__Vfunc_milan_datapath__DOT__aecp_listener__DOT__u_dyn__DOT__pick64__87__Vfuncout;
            }
        } else if ((0x00000020U & (IData)(vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_dyn__DOT__w_ovl))) {
            if ((0x00000010U & (IData)(vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_dyn__DOT__w_ovl))) {
                if ((8U & (IData)(vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_dyn__DOT__w_ovl))) {
                    vlSelfRef.__Vfunc_milan_datapath__DOT__aecp_listener__DOT__u_dyn__DOT__pick64__88__n 
                        = (7U & ((IData)(4U) + (IData)(vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_dyn__DOT__w_ovl)));
                    vlSelfRef.__Vfunc_milan_datapath__DOT__aecp_listener__DOT__u_dyn__DOT__pick64__88__v 
                        = (QData)((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__adp_ccaps));
                    vlSelfRef.__Vfunc_milan_datapath__DOT__aecp_listener__DOT__u_dyn__DOT__pick64__88__Vfuncout 
                        = (0x000000ffU & (IData)((vlSelfRef.__Vfunc_milan_datapath__DOT__aecp_listener__DOT__u_dyn__DOT__pick64__88__v 
                                                  >> 
                                                  (0x0000003fU 
                                                   & (((IData)(7U) 
                                                       - (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__aecp_listener__DOT__u_dyn__DOT__pick64__88__n)) 
                                                      << 3U)))));
                    vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__st_ovl_byte_w 
                        = vlSelfRef.__Vfunc_milan_datapath__DOT__aecp_listener__DOT__u_dyn__DOT__pick64__88__Vfuncout;
                } else {
                    vlSelfRef.__Vfunc_milan_datapath__DOT__aecp_listener__DOT__u_dyn__DOT__pick64__89__n 
                        = (7U & ((IData)(6U) + (IData)(vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_dyn__DOT__w_ovl)));
                    vlSelfRef.__Vfunc_milan_datapath__DOT__aecp_listener__DOT__u_dyn__DOT__pick64__89__Vfuncout 
                        = (0x000000ffU & (IData)((0x0000000000004801ULL 
                                                  >> 
                                                  (0x0000003fU 
                                                   & (((IData)(7U) 
                                                       - (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__aecp_listener__DOT__u_dyn__DOT__pick64__89__n)) 
                                                      << 3U)))));
                    vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__st_ovl_byte_w 
                        = vlSelfRef.__Vfunc_milan_datapath__DOT__aecp_listener__DOT__u_dyn__DOT__pick64__89__Vfuncout;
                }
            } else if ((8U & (IData)(vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_dyn__DOT__w_ovl))) {
                vlSelfRef.__Vfunc_milan_datapath__DOT__aecp_listener__DOT__u_dyn__DOT__pick64__90__n 
                    = (7U & ((IData)(6U) + (IData)(vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_dyn__DOT__w_ovl)));
                vlSelfRef.__Vfunc_milan_datapath__DOT__aecp_listener__DOT__u_dyn__DOT__pick64__90__Vfuncout 
                    = (0x000000ffU & (IData)((9ULL 
                                              >> (0x0000003fU 
                                                  & (((IData)(7U) 
                                                      - (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__aecp_listener__DOT__u_dyn__DOT__pick64__90__n)) 
                                                     << 3U)))));
                vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__st_ovl_byte_w 
                    = vlSelfRef.__Vfunc_milan_datapath__DOT__aecp_listener__DOT__u_dyn__DOT__pick64__90__Vfuncout;
            } else {
                vlSelfRef.__Vfunc_milan_datapath__DOT__aecp_listener__DOT__u_dyn__DOT__pick64__91__n 
                    = (7U & ((IData)(6U) + (IData)(vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_dyn__DOT__w_ovl)));
                vlSelfRef.__Vfunc_milan_datapath__DOT__aecp_listener__DOT__u_dyn__DOT__pick64__91__Vfuncout 
                    = (0x000000ffU & (IData)((0x0000000000004801ULL 
                                              >> (0x0000003fU 
                                                  & (((IData)(7U) 
                                                      - (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__aecp_listener__DOT__u_dyn__DOT__pick64__91__n)) 
                                                     << 3U)))));
                vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__st_ovl_byte_w 
                    = vlSelfRef.__Vfunc_milan_datapath__DOT__aecp_listener__DOT__u_dyn__DOT__pick64__91__Vfuncout;
            }
        } else if ((0x00000010U & (IData)(vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_dyn__DOT__w_ovl))) {
            if ((8U & (IData)(vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_dyn__DOT__w_ovl))) {
                vlSelfRef.__Vfunc_milan_datapath__DOT__aecp_listener__DOT__u_dyn__DOT__pick64__92__n 
                    = (7U & ((IData)(6U) + (IData)(vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_dyn__DOT__w_ovl)));
                vlSelfRef.__Vfunc_milan_datapath__DOT__aecp_listener__DOT__u_dyn__DOT__pick64__92__Vfuncout 
                    = (0x000000ffU & (IData)((9ULL 
                                              >> (0x0000003fU 
                                                  & (((IData)(7U) 
                                                      - (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__aecp_listener__DOT__u_dyn__DOT__pick64__92__n)) 
                                                     << 3U)))));
                vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__st_ovl_byte_w 
                    = vlSelfRef.__Vfunc_milan_datapath__DOT__aecp_listener__DOT__u_dyn__DOT__pick64__92__Vfuncout;
            } else {
                vlSelfRef.__Vfunc_milan_datapath__DOT__aecp_listener__DOT__u_dyn__DOT__pick64__93__n 
                    = (7U & ((IData)(4U) + (IData)(vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_dyn__DOT__w_ovl)));
                vlSelfRef.__Vfunc_milan_datapath__DOT__aecp_listener__DOT__u_dyn__DOT__pick64__93__v 
                    = (QData)((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__adp_ecaps));
                vlSelfRef.__Vfunc_milan_datapath__DOT__aecp_listener__DOT__u_dyn__DOT__pick64__93__Vfuncout 
                    = (0x000000ffU & (IData)((vlSelfRef.__Vfunc_milan_datapath__DOT__aecp_listener__DOT__u_dyn__DOT__pick64__93__v 
                                              >> (0x0000003fU 
                                                  & (((IData)(7U) 
                                                      - (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__aecp_listener__DOT__u_dyn__DOT__pick64__93__n)) 
                                                     << 3U)))));
                vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__st_ovl_byte_w 
                    = vlSelfRef.__Vfunc_milan_datapath__DOT__aecp_listener__DOT__u_dyn__DOT__pick64__93__Vfuncout;
            }
        } else if ((8U & (IData)(vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_dyn__DOT__w_ovl))) {
            vlSelfRef.__Vfunc_milan_datapath__DOT__aecp_listener__DOT__u_dyn__DOT__pick64__94__n 
                = (7U & (IData)(vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_dyn__DOT__w_ovl));
            vlSelfRef.__Vfunc_milan_datapath__DOT__aecp_listener__DOT__u_dyn__DOT__pick64__94__v 
                = vlSelfRef.milan_datapath__DOT__cfg_adp_entity_model_id;
            vlSelfRef.__Vfunc_milan_datapath__DOT__aecp_listener__DOT__u_dyn__DOT__pick64__94__Vfuncout 
                = (0x000000ffU & (IData)((vlSelfRef.__Vfunc_milan_datapath__DOT__aecp_listener__DOT__u_dyn__DOT__pick64__94__v 
                                          >> (0x0000003fU 
                                              & (((IData)(7U) 
                                                  - (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__aecp_listener__DOT__u_dyn__DOT__pick64__94__n)) 
                                                 << 3U)))));
            vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__st_ovl_byte_w 
                = vlSelfRef.__Vfunc_milan_datapath__DOT__aecp_listener__DOT__u_dyn__DOT__pick64__94__Vfuncout;
        } else {
            vlSelfRef.__Vfunc_milan_datapath__DOT__aecp_listener__DOT__u_dyn__DOT__pick64__95__n 
                = (7U & (IData)(vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_dyn__DOT__w_ovl));
            vlSelfRef.__Vfunc_milan_datapath__DOT__aecp_listener__DOT__u_dyn__DOT__pick64__95__v 
                = vlSelfRef.milan_datapath__DOT__cfg_adp_entity_id;
            vlSelfRef.__Vfunc_milan_datapath__DOT__aecp_listener__DOT__u_dyn__DOT__pick64__95__Vfuncout 
                = (0x000000ffU & (IData)((vlSelfRef.__Vfunc_milan_datapath__DOT__aecp_listener__DOT__u_dyn__DOT__pick64__95__v 
                                          >> (0x0000003fU 
                                              & (((IData)(7U) 
                                                  - (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__aecp_listener__DOT__u_dyn__DOT__pick64__95__n)) 
                                                 << 3U)))));
            vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__st_ovl_byte_w 
                = vlSelfRef.__Vfunc_milan_datapath__DOT__aecp_listener__DOT__u_dyn__DOT__pick64__95__Vfuncout;
        }
    }
    vlSelfRef.milan_datapath__DOT__ctl_tx_tlast = ((IData)(vlSelfRef.milan_datapath__DOT__ctl_tx_mux__DOT__gsel)
                                                    ? (IData)(vlSelfRef.milan_datapath__DOT__ctl2_tx_tlast)
                                                    : (IData)(vlSelfRef.milan_datapath__DOT__adp_tx_tlast));
    vlSelfRef.milan_datapath__DOT__ctl_tx_tvalid = 
        (((IData)(vlSelfRef.milan_datapath__DOT__ctl_tx_mux__DOT__gsel)
           ? (IData)(vlSelfRef.milan_datapath__DOT__ctl2_tx_tvalid)
           : (1U == (IData)(vlSelfRef.milan_datapath__DOT__adp_adv__DOT__state_r))) 
         & (IData)(vlSelfRef.milan_datapath__DOT__ctl_tx_mux__DOT__active));
    vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__tmr_rd_w 
        = (vlSelfRef.milan_datapath__DOT__acmp_responder__DOT__tmr_ram
           [milan_datapath__DOT__acmp_responder__DOT__tmr_rd_idx_w] 
           & (- (IData)((8U >= (IData)(milan_datapath__DOT__acmp_responder__DOT__tmr_rd_idx_w)))));
    vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__w_smap_badidx 
        = ((0U != (0x0000ffffU & (IData)(vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__cw0_r))) 
           & (IData)(vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_bld__DOT__w_smap_has));
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
    if ((0U == (IData)(vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_val__DOT__state_r))) {
        milan_datapath__DOT__aecp_listener__DOT__u_val__DOT__m_tvalid_l 
            = ((IData)(vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_val__DOT__w_ok) 
               && (IData)(vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__ig_to_val_tvalid));
        vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_val__DOT__s_tready_l 
            = ((1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_val__DOT__w_ok))) 
               || (IData)(vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__val_to_par_tready));
    } else {
        milan_datapath__DOT__aecp_listener__DOT__u_val__DOT__m_tvalid_l 
            = ((1U == (IData)(vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_val__DOT__state_r)) 
               && (IData)(vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__ig_to_val_tvalid));
        vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_val__DOT__s_tready_l 
            = ((1U == (IData)(vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_val__DOT__state_r))
                ? (IData)(vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__val_to_par_tready)
                : (2U == (IData)(vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_val__DOT__state_r)));
    }
    vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__pairB_w = 0ULL;
    vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__pairA_w = 0ULL;
    vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__pushB_w = 0U;
    if ((1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__i2s_feed_lpf_act_w)))) {
        if (vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__pcm_acc_w) {
            if ((1U == (IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__c_eff_w))) {
                vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__pairB_w 
                    = ((QData)((IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__s1_w)) 
                       << 0x00000018U);
                vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__pushB_w = 1U;
            }
        }
    }
    vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__pushA_w = 0U;
    if (vlSelfRef.milan_datapath__DOT__i2s_feed_lpf_act_w) {
        vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__pairA_w 
            = (((QData)((IData)(((((0x0000ff00U & ((IData)(vlSelfRef.milan_datapath__DOT__pcm_lpf_tdata) 
                                                   << 8U)) 
                                   | (0x000000ffU & (IData)(
                                                            (vlSelfRef.milan_datapath__DOT__pcm_lpf_tdata 
                                                             >> 8U)))) 
                                  << 0x00000010U) | 
                                 ((0x0000ff00U & ((IData)(
                                                          (vlSelfRef.milan_datapath__DOT__pcm_lpf_tdata 
                                                           >> 0x00000010U)) 
                                                  << 8U)) 
                                  | (0x000000ffU & (IData)(
                                                           (vlSelfRef.milan_datapath__DOT__pcm_lpf_tdata 
                                                            >> 0x00000020U))))))) 
                << 0x00000010U) | (QData)((IData)((
                                                   (0x0000ff00U 
                                                    & ((IData)(
                                                               (vlSelfRef.milan_datapath__DOT__pcm_lpf_tdata 
                                                                >> 0x00000028U)) 
                                                       << 8U)) 
                                                   | (0x000000ffU 
                                                      & (IData)(
                                                                (vlSelfRef.milan_datapath__DOT__pcm_lpf_tdata 
                                                                 >> 0x00000030U)))))));
        vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__pushA_w 
            = vlSelfRef.milan_datapath__DOT__pcm_lpf_tvalid;
    } else if (vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__pcm_acc_w) {
        if ((1U == (IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__c_eff_w))) {
            vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__pairA_w 
                = ((QData)((IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__s0_w)) 
                   << 0x00000018U);
            vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__pushA_w = 1U;
        } else if ((0U == (IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__pos_r))) {
            vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__pairA_w 
                = (((QData)((IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__s0_w)) 
                    << 0x00000018U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__s1_w)));
            vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__pushA_w = 1U;
        } else if ((1U == (IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__pos_r))) {
            vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__pairA_w 
                = (((QData)((IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__lhold_r)) 
                    << 0x00000018U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__s0_w)));
            vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__pushA_w = 1U;
        }
    }
    vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__pass_now 
        = ((IData)(vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__sof)
            ? (IData)(vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__pass_sof)
            : (IData)(vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__pass_r));
    vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__w1_addr_w 
        = ((0x00000038U & ((IData)(vlSelfRef.m_axis_pcm_tuser) 
                           << 3U)) | (7U & (IData)(vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__ch1_w)));
    vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__pop_w 
        = (((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_tvalid_pipe_reg) 
            >> 1U) & (IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_tready_pipe));
    milan_datapath__DOT__chan_map_render__DOT__avb_ok_w 
        = ((8U > (IData)(vlSelfRef.m_axis_pcm_tuser)) 
           & (IData)(vlSelfRef.milan_datapath__DOT__dpkt_acc_w));
    __Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__202__s 
        = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ev_s_r;
    __Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__202__Vfuncout 
        = (8U | ((IData)(__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__202__s) 
                 << 5U));
    vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ram_raddr_w 
        = __Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__202__Vfuncout;
    if ((8U & (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__mst_r))) {
        vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__203__s 
            = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ev_s_r;
        vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__203__Vfuncout 
            = (8U | ((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__203__s) 
                     << 5U));
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ram_raddr_w 
            = vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__203__Vfuncout;
    } else if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__mst_r))) {
        if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__mst_r))) {
            if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__mst_r))) {
                vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__204__s 
                    = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ev_s_r;
                vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__204__Vfuncout 
                    = (8U | ((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__204__s) 
                             << 5U));
                vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ram_raddr_w 
                    = vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__204__Vfuncout;
            } else {
                vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__205__s 
                    = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ev_s_r;
                vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__205__Vfuncout 
                    = (8U | ((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__205__s) 
                             << 5U));
                vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ram_raddr_w 
                    = vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__205__Vfuncout;
            }
        } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__mst_r))) {
            if (vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__w11_mode_r) {
                vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__206__s 
                    = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ev_s_r;
                vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__206__Vfuncout 
                    = (0x0bU | ((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__206__s) 
                                << 5U));
                vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ram_raddr_w 
                    = vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__206__Vfuncout;
            } else if (vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__sil_mode_r) {
                if ((0U == (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__wrph_r))) {
                    vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__207__s 
                        = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ev_s_r;
                    vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT____VlemCall_8__laddr 
                        = (0x11U | ((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__207__s) 
                                    << 5U));
                } else {
                    vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__208__s 
                        = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ev_s_r;
                    vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT____VlemCall_8__laddr 
                        = (8U | ((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__208__s) 
                                 << 5U));
                }
                vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ram_raddr_w 
                    = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT____VlemCall_8__laddr;
            } else {
                vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__209__w 
                    = (0x10U | (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__inc_next_w));
                vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__209__s 
                    = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ev_s_r;
                vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__209__Vfuncout 
                    = (((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__209__s) 
                        << 5U) | (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__209__w));
                vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ram_raddr_w 
                    = vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__209__Vfuncout;
            }
        } else {
            vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__210__s 
                = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ev_s_r;
            vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__210__Vfuncout 
                = (8U | ((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__210__s) 
                         << 5U));
            vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ram_raddr_w 
                = vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__210__Vfuncout;
        }
    } else if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__mst_r))) {
        if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__mst_r))) {
            vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__211__s 
                = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ev_s_r;
            vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__211__Vfuncout 
                = (8U | ((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__211__s) 
                         << 5U));
            vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ram_raddr_w 
                = vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__211__Vfuncout;
        } else {
            vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__212__s 
                = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ev_s_r;
            vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__212__Vfuncout 
                = (8U | ((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__212__s) 
                         << 5U));
            vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ram_raddr_w 
                = vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__212__Vfuncout;
        }
    } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__mst_r))) {
        vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__213__s 
            = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ev_s_r;
        vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__213__Vfuncout 
            = (3U | ((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__213__s) 
                     << 5U));
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ram_raddr_w 
            = vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__213__Vfuncout;
    } else {
        if (vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ext_rd_go_w) {
            vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT____VlemCall_7__laddr 
                = ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_80)
                    ? ((0x000000e0U & ((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__snap_idx_r) 
                                       << 5U)) | (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__snap_word_r))
                    : (((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rds_idx_r) 
                        << 5U) | (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rds_word_r)));
        } else {
            vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__214__w 
                = ((0U == (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__disp_s_w))
                    ? 8U : 2U);
            vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__214__s 
                = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__disp_s_w;
            vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT____VlemCall_7__laddr 
                = (((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__214__s) 
                    << 5U) | (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__214__w));
        }
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ram_raddr_w 
            = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT____VlemCall_7__laddr;
    }
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_16 = (0U 
                                                 == 
                                                 (7U 
                                                  & (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__ctx_ram
                                                     [
                                                     ((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rd_idx_w) 
                                                      & (- (IData)(
                                                                   (8U 
                                                                    >= (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rd_idx_w)))))][9U] 
                                                     >> 0x0000001aU)));
    vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__refuse_w 
        = ((~ (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__fit_w)) 
           & (IData)(__VdfgRegularize_h6e95ff9d_0_88));
    vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__wgrant_now_w 
        = vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__wgrant_r;
    if ((8U >= (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__aidx_r))) {
        vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__wgrant_now_w 
            = (((~ ((IData)(1U) << (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__aidx_r))) 
                & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__wgrant_now_w)) 
               | (0x01ffU & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__fit_w) 
                             << (IData)(vlSelfRef.milan_datapath__DOT__lwsrp__DOT__bw_gate__DOT__aidx_r))));
    }
    vlSelfRef.milan_datapath__DOT__csr__DOT__snap_srp9_w 
        = (0x000001ffU & ((0U == (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__snap_idx_r))
                           ? (IData)(__VdfgRegularize_h6e95ff9d_0_24)
                           : ((IData)(vlSelfRef.milan_datapath__DOT__srp_ctx_rd_stat_w) 
                              & (- (IData)((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__srp_fresh_r))))));
    vlSelfRef.milan_datapath__DOT____Vcellinp__csr__i_lwsrp_status 
        = ((((IData)(vlSelfRef.milan_datapath__DOT__lwsrp_rx_drops) 
             << 0x00000018U) | ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp_tfail_code) 
                                << 0x00000010U)) | 
           ((((IData)(vlSelfRef.milan_datapath__DOT__lwsrp_ctx_oor_w) 
              << 0x0000000bU) | (((IData)(vlSelfRef.milan_datapath__DOT__lwsrp_tfail_valid) 
                                  << 0x0000000aU) | 
                                 ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp_slope_en) 
                                  << 9U))) | (IData)(__VdfgRegularize_h6e95ff9d_0_24)));
    vlSelfRef.milan_datapath__DOT__acmp_talker_active_v 
        = ((IData)(vlSelfRef.milan_datapath__DOT__acmp_probe_armed_v) 
           | (IData)(vlSelfRef.milan_datapath__DOT__acmp_lobs_v_w));
    __Vilp2 = 0U;
    while ((__Vilp2 <= 0x0000003fU)) {
        vlSelfRef.milan_datapath__DOT__crf_tx__DOT__fb[__Vilp2] = 0U;
        __Vilp2 = ((IData)(1U) + __Vilp2);
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
    vlSelfRef.milan_datapath__DOT__srp_ctl_mux__DOT__active 
        = ((IData)(vlSelfRef.milan_datapath__DOT__srp_ctl_mux__DOT__locked_r) 
           | ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp_tx_tvalid) 
              | (IData)(vlSelfRef.milan_datapath__DOT__ctl_tx_tvalid)));
    vlSelfRef.milan_datapath__DOT__srp_ctl_mux__DOT__gsel 
        = (1U & ((IData)(vlSelfRef.milan_datapath__DOT__srp_ctl_mux__DOT__locked_r)
                  ? (IData)(vlSelfRef.milan_datapath__DOT__srp_ctl_mux__DOT__sel_r)
                  : (((IData)(vlSelfRef.milan_datapath__DOT__ctl_tx_tvalid) 
                      & (IData)(vlSelfRef.milan_datapath__DOT__lwsrp_tx_tvalid))
                      ? (~ (IData)(vlSelfRef.milan_datapath__DOT__srp_ctl_mux__DOT__last_grant_r))
                      : (IData)(vlSelfRef.milan_datapath__DOT__lwsrp_tx_tvalid))));
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
    vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_parser__DOT__w_hs 
        = ((IData)(milan_datapath__DOT__aecp_listener__DOT__u_val__DOT__m_tvalid_l) 
           & (IData)(vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__val_to_par_tready));
    vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_ingress__DOT__frame_fifo__DOT__m_axis_tready_pipe 
        = (((~ (IData)(vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__req_valid_w)) 
            & (0U == (IData)(vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_ingress__DOT__rstate_r))) 
           | ((1U == (IData)(vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_ingress__DOT__rstate_r)) 
              | ((2U == (IData)(vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_ingress__DOT__rstate_r)) 
                 & ((~ (IData)(vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_ingress__DOT__hold_last_r)) 
                    & (IData)(vlSelfRef.milan_datapath__DOT__aecp_listener__DOT__u_val__DOT__s_tready_l)))));
    vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__wA_ok_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__pushA_w) 
           & (1U <= (IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__stg_space_w)));
    vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__wB_ok_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__pushB_w) 
           & ((IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__stg_space_w) 
              >= ((IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__pushA_w)
                   ? 2U : 1U)));
    vlSelfRef.m_axis_rx_tvalid = ((IData)(vlSelfRef.s_axis_mac_rx_tvalid) 
                                  & (IData)(vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__pass_now));
    vlSelfRef.s_axis_mac_rx_tready = (1U & ((~ (IData)(vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__pass_now)) 
                                            | (IData)(vlSelfRef.m_axis_rx_tready)));
    vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__w0_en_w 
        = ((8U > (IData)(vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__chpos_r)) 
           & (IData)(milan_datapath__DOT__chan_map_render__DOT__avb_ok_w));
    vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__w1_en_w 
        = ((8U > (IData)(vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__ch1_w)) 
           & (IData)(milan_datapath__DOT__chan_map_render__DOT__avb_ok_w));
    vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_en_w = 0U;
    vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_idx_w = 0U;
    VL_ASSIGN_W(317, vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_data_w, Vmilan_datapath__ConstPool__CONST_h8a04c6be_0);
    if (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__init_done_r) {
        if (((1U == (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__st_r)) 
             & (IData)(milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_frame_en_w))) {
            vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_en_w = 1U;
            vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_idx_w 
                = vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__cur_idx_r;
            vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_data_w[0U] 
                = milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_frame_w[0U];
            vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_data_w[1U] 
                = milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_frame_w[1U];
            vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_data_w[2U] 
                = milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_frame_w[2U];
            vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_data_w[3U] 
                = milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_frame_w[3U];
            vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_data_w[4U] 
                = milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_frame_w[4U];
            vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_data_w[5U] 
                = milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_frame_w[5U];
            vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_data_w[6U] 
                = milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_frame_w[6U];
            vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_data_w[7U] 
                = milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_frame_w[7U];
            vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_data_w[8U] 
                = milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_frame_w[8U];
            vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_data_w[9U] 
                = milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_frame_w[9U];
        } else if (vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_launch_ok) {
            vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_en_w = 1U;
            vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_idx_w 
                = Vmilan_datapath__ConstPool__TABLE_hc68454f1_0
                [vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__probe_pend_r];
            vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_data_w[0U] 
                = vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__ctx_ram
                [((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rd_idx_w) 
                  & (- (IData)((8U >= (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rd_idx_w)))))][0U];
            vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_data_w[1U] 
                = vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__ctx_ram
                [((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rd_idx_w) 
                  & (- (IData)((8U >= (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rd_idx_w)))))][1U];
            vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_data_w[2U] 
                = vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__ctx_ram
                [((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rd_idx_w) 
                  & (- (IData)((8U >= (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rd_idx_w)))))][2U];
            vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_data_w[3U] 
                = vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__ctx_ram
                [((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rd_idx_w) 
                  & (- (IData)((8U >= (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rd_idx_w)))))][3U];
            vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_data_w[4U] 
                = vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__ctx_ram
                [((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rd_idx_w) 
                  & (- (IData)((8U >= (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rd_idx_w)))))][4U];
            vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_data_w[5U] 
                = vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__ctx_ram
                [((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rd_idx_w) 
                  & (- (IData)((8U >= (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rd_idx_w)))))][5U];
            vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_data_w[6U] 
                = vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__ctx_ram
                [((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rd_idx_w) 
                  & (- (IData)((8U >= (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rd_idx_w)))))][6U];
            vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_data_w[7U] 
                = vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__ctx_ram
                [((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rd_idx_w) 
                  & (- (IData)((8U >= (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rd_idx_w)))))][7U];
            vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_data_w[8U] 
                = vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__ctx_ram
                [((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rd_idx_w) 
                  & (- (IData)((8U >= (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rd_idx_w)))))][8U];
            vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_data_w[9U] 
                = vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__ctx_ram
                [((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rd_idx_w) 
                  & (- (IData)((8U >= (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__rd_idx_w)))))][9U];
            vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_data_w[8U] 
                = (0x80000000U | (0x0fffffffU & vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_data_w[8U]));
            vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_data_w[9U] 
                = (0x0000000cU | (0x1ffffc00U & vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_data_w[9U]));
        } else if (((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_swp_run) 
                    & (IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__sn_wr_w))) {
            vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_en_w = 1U;
            vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_idx_w 
                = vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__swp_idx_r;
            vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_data_w[0U] 
                = vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__sn_w[0U];
            vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_data_w[1U] 
                = vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__sn_w[1U];
            vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_data_w[2U] 
                = vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__sn_w[2U];
            vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_data_w[3U] 
                = vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__sn_w[3U];
            vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_data_w[4U] 
                = vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__sn_w[4U];
            vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_data_w[5U] 
                = vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__sn_w[5U];
            vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_data_w[6U] 
                = vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__sn_w[6U];
            vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_data_w[7U] 
                = vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__sn_w[7U];
            vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_data_w[8U] 
                = vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__sn_w[8U];
            vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_data_w[9U] 
                = vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__sn_w[9U];
        } else if (((IData)(vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__w_rest_ok) 
                    & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_16))) {
            vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_en_w = 1U;
            vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_idx_w 
                = vlSelfRef.milan_datapath__DOT__csr__DOT__rest_idx_r;
            vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_data_w[0U] 
                = vlSelfRef.milan_datapath__DOT__csr__DOT__rest_ctlo;
            vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_data_w[1U] 
                = vlSelfRef.milan_datapath__DOT__csr__DOT__rest_cthi;
            vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_data_w[2U] 
                = (IData)((((QData)((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rest_tkhi)) 
                            << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rest_tklo))));
            vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_data_w[3U] 
                = (IData)(((((QData)((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rest_tkhi)) 
                             << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rest_tklo))) 
                           >> 0x00000020U));
            vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_data_w[4U] = 0U;
            vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_data_w[5U] = 0U;
            vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_data_w[6U] = 0U;
            vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_data_w[7U] 
                = ((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rest_flags_r) 
                   << 0x0000001cU);
            vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_data_w[8U] 
                = ((0xf0000000U & vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_data_w[8U]) 
                   | ((0x0ffff000U & (vlSelfRef.milan_datapath__DOT__csr__DOT__rest_meta 
                                      << 0x0000000cU)) 
                      | ((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rest_flags_r) 
                         >> 4U)));
            vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_data_w[8U] 
                = (0x0fffffffU & vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_data_w[8U]);
            vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_data_w[9U] = 0x04400000U;
        }
    } else {
        vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_en_w = 1U;
        vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__wr_idx_w 
            = vlSelfRef.milan_datapath__DOT__acmp_listener_sm__DOT__u_ctx__DOT__init_idx_r;
    }
    milan_datapath__DOT__csr__DOT__strm_read_mux__DOT__coff 
        = (0x0000ffffU & ((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q) 
                          - (IData)(0x0830U)));
    vlSelfRef.milan_datapath__DOT__csr__DOT__strm_mux = 0U;
    if ((0x0800U == (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
        vlSelfRef.milan_datapath__DOT__csr__DOT__strm_mux 
            = (((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__strm_dir_r) 
                << 8U) | (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__strm_idx_r));
    } else if ((0x0804U == (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
        vlSelfRef.milan_datapath__DOT__csr__DOT__strm_mux 
            = vlSelfRef.milan_datapath__DOT__csr__DOT__snap_busy_r;
    } else if ((8U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__strm_idx_r))) {
        if (((((((((0x0810U == (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                   | (0x0814U == (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) 
                  | (0x0818U == (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) 
                 | (0x081cU == (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) 
                | (0x0820U == (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) 
               | (0x082cU == (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) 
              | (0x0858U == (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) 
             | ((0x0824U == (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                || (0x0828U == (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))))) {
            if ((0x0810U == (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                if (((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__strm_dir_r) 
                     & (0U == (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__strm_idx_r)))) {
                    vlSelfRef.milan_datapath__DOT__csr__DOT__strm_mux 
                        = (1U & vlSelfRef.milan_datapath__DOT__csr__DOT__aaf_ctrl);
                }
            } else if ((0x0814U == (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                vlSelfRef.milan_datapath__DOT__csr__DOT__strm_mux 
                    = ((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__strm_dir_r)
                        ? ((0U == (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__strm_idx_r))
                            ? ((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w) 
                               << 0x00000010U) : ((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__srp_fresh_r)
                                                   ? (IData)(vlSelfRef.milan_datapath__DOT__srp_ctx_rd_sid_w)
                                                   : 0U))
                        : ((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__acmp_fresh_r)
                            ? (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__acmp_sid_q_r)
                            : 0U));
            } else if ((0x0818U == (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                vlSelfRef.milan_datapath__DOT__csr__DOT__strm_mux 
                    = ((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__strm_dir_r)
                        ? ((0U == (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__strm_idx_r))
                            ? (IData)((vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w 
                                       >> 0x10U)) : 
                           ((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__srp_fresh_r)
                             ? (IData)((vlSelfRef.milan_datapath__DOT__srp_ctx_rd_sid_w 
                                        >> 0x20U)) : 0U))
                        : ((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__acmp_fresh_r)
                            ? (IData)((vlSelfRef.milan_datapath__DOT__csr__DOT__acmp_sid_q_r 
                                       >> 0x20U)) : 0U));
            } else if ((0x081cU == (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                if (vlSelfRef.milan_datapath__DOT__csr__DOT__strm_dir_r) {
                    if ((0U == (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__strm_idx_r))) {
                        vlSelfRef.milan_datapath__DOT__csr__DOT__strm_mux 
                            = vlSelfRef.milan_datapath__DOT__csr__DOT__aaf_dmlo;
                    }
                } else {
                    vlSelfRef.milan_datapath__DOT__csr__DOT__strm_mux 
                        = ((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__acmp_fresh_r)
                            ? (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__acmp_dmac_q_r)
                            : 0U);
                }
            } else if ((0x0820U == (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                if (vlSelfRef.milan_datapath__DOT__csr__DOT__strm_dir_r) {
                    if ((0U == (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__strm_idx_r))) {
                        vlSelfRef.milan_datapath__DOT__csr__DOT__strm_mux 
                            = (0x0000ffffU & vlSelfRef.milan_datapath__DOT__csr__DOT__aaf_dmhi);
                    }
                } else {
                    vlSelfRef.milan_datapath__DOT__csr__DOT__strm_mux 
                        = ((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__acmp_fresh_r)
                            ? (0x0000ffffU & (IData)(
                                                     (vlSelfRef.milan_datapath__DOT__csr__DOT__acmp_dmac_q_r 
                                                      >> 0x20U)))
                            : 0U);
                }
            } else if ((0x082cU == (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                vlSelfRef.milan_datapath__DOT__csr__DOT__strm_mux 
                    = vlSelfRef.milan_datapath__DOT__csr__DOT__snap_shadow_r[0U];
            } else if ((0x0858U == (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                vlSelfRef.milan_datapath__DOT__csr__DOT__strm_mux 
                    = vlSelfRef.milan_datapath__DOT__csr__DOT__snap_shadow_r[11U];
            } else if (vlSelfRef.milan_datapath__DOT__csr__DOT__strm_dir_r) {
                vlSelfRef.milan_datapath__DOT__csr__DOT__strm_mux = 0xdeaddeadU;
            }
        } else if ((0x085cU == (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
            vlSelfRef.milan_datapath__DOT__csr__DOT__strm_mux 
                = ((0U == (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__strm_idx_r))
                    ? vlSelfRef.milan_datapath__DOT____Vcellinp__csr__i_lwsrp_status
                    : ((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__srp_fresh_r)
                        ? (IData)(vlSelfRef.milan_datapath__DOT__srp_ctx_rd_stat_w)
                        : 0U));
        } else if ((0x0860U == (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
            vlSelfRef.milan_datapath__DOT__csr__DOT__strm_mux 
                = ((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__strm_dir_r)
                    ? 0xdeaddeadU : ((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__acmp_fresh_r)
                                      ? (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__acmp_ctlr_q_r)
                                      : 0U));
        } else if ((0x0864U == (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
            vlSelfRef.milan_datapath__DOT__csr__DOT__strm_mux 
                = ((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__strm_dir_r)
                    ? 0xdeaddeadU : ((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__acmp_fresh_r)
                                      ? (IData)((vlSelfRef.milan_datapath__DOT__csr__DOT__acmp_ctlr_q_r 
                                                 >> 0x20U))
                                      : 0U));
        } else if ((0x0868U == (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
            vlSelfRef.milan_datapath__DOT__csr__DOT__strm_mux 
                = ((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__strm_dir_r)
                    ? 0xdeaddeadU : ((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__acmp_fresh_r)
                                      ? (((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__acmp_flags_q_r) 
                                          << 0x00000010U) 
                                         | (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__acmp_tuid_q_r))
                                      : 0U));
        } else if (((0x0830U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                    & (0x0858U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
            vlSelfRef.milan_datapath__DOT__csr__DOT__strm_mux 
                = ((0x0bU >= (0x0000000fU & ((IData)(1U) 
                                             + ((IData)(milan_datapath__DOT__csr__DOT__strm_read_mux__DOT__coff) 
                                                >> 2U))))
                    ? vlSelfRef.milan_datapath__DOT__csr__DOT__snap_shadow_r
                   [(0x0000000fU & ((IData)(1U) + ((IData)(milan_datapath__DOT__csr__DOT__strm_read_mux__DOT__coff) 
                                                   >> 2U)))]
                    : 0U);
        } else if ((0x086cU == (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
            vlSelfRef.milan_datapath__DOT__csr__DOT__strm_mux = 0xdeaddeadU;
        }
    }
}
