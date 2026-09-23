// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vmilan_datapath.h for the primary calling header

#include "Vmilan_datapath__pch.h"

extern const VlWide<9>/*287:0*/ Vmilan_datapath__ConstPool__CONST_hc5471b50_0;
extern const VlWide<256>/*8191:0*/ Vmilan_datapath__ConstPool__CONST_hc13a5b68_0;
extern const VlWide<16>/*511:0*/ Vmilan_datapath__ConstPool__CONST_h88ed57bb_0;
extern const VlUnpacked<SData/*15:0*/, 8> Vmilan_datapath__ConstPool__TABLE_h42b7b3b2_0;
extern const VlWide<8>/*255:0*/ Vmilan_datapath__ConstPool__CONST_h5302cfd2_0;
extern const VlUnpacked<CData/*2:0*/, 16> Vmilan_datapath__ConstPool__TABLE_h1b26f04f_0;
extern const VlUnpacked<CData/*0:0*/, 32> Vmilan_datapath__ConstPool__TABLE_h5f1389fb_0;
extern const VlUnpacked<CData/*2:0*/, 32> Vmilan_datapath__ConstPool__TABLE_h6dff1152_0;

VL_ATTR_COLD void Vmilan_datapath___024root___stl_sequent__TOP__1(Vmilan_datapath___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vmilan_datapath___024root___stl_sequent__TOP__1\n"); );
    Vmilan_datapath__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    QData/*63:0*/ milan_datapath__DOT__lb_tap_tdata_w;
    milan_datapath__DOT__lb_tap_tdata_w = 0;
    CData/*6:0*/ milan_datapath__DOT__csr_tctx_rd_addr_w;
    milan_datapath__DOT__csr_tctx_rd_addr_w = 0;
    CData/*0:0*/ milan_datapath__DOT__amap_page_ok_w;
    milan_datapath__DOT__amap_page_ok_w = 0;
    CData/*0:0*/ milan_datapath__DOT__amap_opage_ok_w;
    milan_datapath__DOT__amap_opage_ok_w = 0;
    CData/*0:0*/ milan_datapath__DOT__avtprx_stopped_w;
    milan_datapath__DOT__avtprx_stopped_w = 0;
    IData/*31:0*/ milan_datapath__DOT__amap_page_slot__DOT__off_c;
    milan_datapath__DOT__amap_page_slot__DOT__off_c = 0;
    IData/*31:0*/ milan_datapath__DOT__amap_page_slot__DOT__g_c;
    milan_datapath__DOT__amap_page_slot__DOT__g_c = 0;
    IData/*31:0*/ milan_datapath__DOT__amap_page_fmt__DOT__offq_c;
    milan_datapath__DOT__amap_page_fmt__DOT__offq_c = 0;
    IData/*31:0*/ milan_datapath__DOT__pp_ctr_event_pick__DOT__pick;
    milan_datapath__DOT__pp_ctr_event_pick__DOT__pick = 0;
    CData/*0:0*/ milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pool_oversize_w;
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pool_oversize_w = 0;
    CData/*0:0*/ milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__urb_we_w;
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__urb_we_w = 0;
    CData/*5:0*/ milan_datapath__DOT__render_setpoint__DOT__fill_pop_w;
    milan_datapath__DOT__render_setpoint__DOT__fill_pop_w = 0;
    IData/*31:0*/ milan_datapath__DOT__avtp_rx_monitor__DOT__eng_wdata_w;
    milan_datapath__DOT__avtp_rx_monitor__DOT__eng_wdata_w = 0;
    CData/*0:0*/ milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw;
    QData/*47:0*/ milan_datapath__DOT__aaf_packetizer__DOT__eff_dmac_w;
    milan_datapath__DOT__aaf_packetizer__DOT__eff_dmac_w = 0;
    SData/*11:0*/ milan_datapath__DOT__aaf_packetizer__DOT__eff_vid_w;
    milan_datapath__DOT__aaf_packetizer__DOT__eff_vid_w = 0;
    QData/*63:0*/ milan_datapath__DOT__aaf_packetizer__DOT__stream_id_w;
    milan_datapath__DOT__aaf_packetizer__DOT__stream_id_w = 0;
    IData/*31:0*/ milan_datapath__DOT__aaf_packetizer__DOT__frame_bytes__DOT__unnamedblk5__DOT__k;
    milan_datapath__DOT__aaf_packetizer__DOT__frame_bytes__DOT__unnamedblk5__DOT__k = 0;
    IData/*16:0*/ __Vfunc_milan_datapath__DOT__amap_out_cluster__7__Vfuncout;
    __Vfunc_milan_datapath__DOT__amap_out_cluster__7__Vfuncout = 0;
    SData/*12:0*/ __Vfunc_milan_datapath__DOT__amap_out_cluster__7__e;
    __Vfunc_milan_datapath__DOT__amap_out_cluster__7__e = 0;
    SData/*15:0*/ __Vfunc_milan_datapath__DOT__amap_out_cluster__7__port_i;
    __Vfunc_milan_datapath__DOT__amap_out_cluster__7__port_i = 0;
    IData/*16:0*/ __Vfunc_milan_datapath__DOT__amap_out_cluster__7__r;
    __Vfunc_milan_datapath__DOT__amap_out_cluster__7__r = 0;
    CData/*7:0*/ __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__75__Vfuncout;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__75__Vfuncout = 0;
    CData/*5:0*/ __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__75__idx;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__75__idx = 0;
    CData/*3:0*/ __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__75__msg;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__75__msg = 0;
    SData/*15:0*/ __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__75__off;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__75__off = 0;
    CData/*7:0*/ __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__75__cnt;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__75__cnt = 0;
    QData/*47:0*/ __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__75__dda;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__75__dda = 0;
    QData/*47:0*/ __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__75__ereq_s;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__75__ereq_s = 0;
    SData/*15:0*/ __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__75__ereq_c;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__75__ereq_c = 0;
    QData/*47:0*/ __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__75__econ_s;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__75__econ_s = 0;
    SData/*15:0*/ __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__75__econ_c;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__75__econ_c = 0;
    IData/*31:0*/ __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__75__i;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__75__i = 0;
    CData/*7:0*/ __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__75__b;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__75__b = 0;
    CData/*0:0*/ __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__75__dfd;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__75__dfd = 0;
    QData/*47:0*/ __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__75__req_s;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__75__req_s = 0;
    SData/*15:0*/ __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__75__req_c;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__75__req_c = 0;
    CData/*7:0*/ __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__117__Vfuncout;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__117__Vfuncout = 0;
    CData/*6:0*/ __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__117__idx;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__117__idx = 0;
    CData/*0:0*/ __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__117__dep;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__117__dep = 0;
    CData/*0:0*/ __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__117__ifx;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__117__ifx = 0;
    QData/*63:0*/ __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__117__gm;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__117__gm = 0;
    CData/*7:0*/ __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__117__dom;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__117__dom = 0;
    IData/*31:0*/ __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__117__aidx;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__117__aidx = 0;
    IData/*31:0*/ __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__117__i;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__117__i = 0;
    CData/*7:0*/ __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__117__b;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__117__b = 0;
    QData/*63:0*/ __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__189__Vfuncout;
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__189__Vfuncout = 0;
    CData/*2:0*/ __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__189__b;
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__189__b = 0;
    VlUnpacked<CData/*7:0*/, 64> __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__189__f;
    for (int __Vi0 = 0; __Vi0 < 64; ++__Vi0) {
        __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__189__f[__Vi0] = 0;
    }
    IData/*23:0*/ __Vfunc_milan_datapath__DOT__chan_map_render__DOT__src_rd__220__Vfuncout;
    __Vfunc_milan_datapath__DOT__chan_map_render__DOT__src_rd__220__Vfuncout = 0;
    CData/*6:0*/ __Vfunc_milan_datapath__DOT__chan_map_render__DOT__src_rd__220__a;
    __Vfunc_milan_datapath__DOT__chan_map_render__DOT__src_rd__220__a = 0;
    CData/*6:0*/ __Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__312__Vfuncout;
    __Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__312__Vfuncout = 0;
    CData/*2:0*/ __Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__312__t;
    __Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__312__t = 0;
    CData/*0:0*/ __VdfgRegularize_h6e95ff9d_0_403;
    __VdfgRegularize_h6e95ff9d_0_403 = 0;
    CData/*0:0*/ __VdfgRegularize_h6e95ff9d_0_448;
    __VdfgRegularize_h6e95ff9d_0_448 = 0;
    IData/*31:0*/ __Vtemp_8;
    IData/*31:0*/ __Vilp1;
    // Body
    __Vfunc_milan_datapath__DOT__chan_map_render__DOT__src_rd__220__a 
        = (0x0000007fU & (IData)(vlSelfRef.milan_datapath__DOT____Vcellinp__chan_map_render__map_wr_data_i));
    __Vfunc_milan_datapath__DOT__chan_map_render__DOT__src_rd__220__Vfuncout 
        = ((0x00000040U & (IData)(__Vfunc_milan_datapath__DOT__chan_map_render__DOT__src_rd__220__a))
            ? 0U : vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__cur_r
           [(7U & ((IData)(__Vfunc_milan_datapath__DOT__chan_map_render__DOT__src_rd__220__a) 
                   >> 3U))][(7U & (IData)(__Vfunc_milan_datapath__DOT__chan_map_render__DOT__src_rd__220__a))]);
    vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__map_seed_w 
        = __Vfunc_milan_datapath__DOT__chan_map_render__DOT__src_rd__220__Vfuncout;
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_180 = (0U 
                                                  == 
                                                  ((((((((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__cap_val_w[0U] 
                                                          ^ vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_last_r[0U]) 
                                                         | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__cap_val_w[1U] 
                                                            ^ vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_last_r[1U])) 
                                                        | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__cap_val_w[2U] 
                                                           ^ vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_last_r[2U])) 
                                                       | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__cap_val_w[3U] 
                                                          ^ vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_last_r[3U])) 
                                                      | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__cap_val_w[4U] 
                                                         ^ vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_last_r[4U])) 
                                                     | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__cap_val_w[5U] 
                                                        ^ vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_last_r[5U])) 
                                                    | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__cap_val_w[6U] 
                                                       ^ vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_last_r[6U])) 
                                                   | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__cap_val_w[7U] 
                                                      ^ vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_last_r[7U])));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_375 = ((1ULL 
                                                   + 
                                                   (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_last_r[8U])) 
                                                     << 0x00000030U) 
                                                    | (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_last_r[7U])) 
                                                        << 0x00000010U) 
                                                       | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_last_r[6U])) 
                                                          >> 0x00000010U)))) 
                                                  == 
                                                  (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__cap_val_w[8U])) 
                                                    << 0x00000030U) 
                                                   | (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__cap_val_w[7U])) 
                                                       << 0x00000010U) 
                                                      | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__cap_val_w[6U])) 
                                                         >> 0x00000010U))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__ntfy_stri_in_w 
        = (((((4U & ((0x03fffffcU & ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_9) 
                                     >> 6U)) | (((8U 
                                                  == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__sink_r)) 
                                                 & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_10)) 
                                                << 2U))) 
              | ((2U & ((0x03fffffeU & ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_9) 
                                        >> 6U)) | (
                                                   ((7U 
                                                     == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__sink_r)) 
                                                    & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_10)) 
                                                   << 1U))) 
                 | (1U & (((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_9) 
                           >> 6U) | ((6U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__sink_r)) 
                                     & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_10)))))) 
             << 6U) | (((2U & ((0x0ffffffeU & ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_9) 
                                               >> 4U)) 
                               | (((5U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__sink_r)) 
                                   & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_10)) 
                                  << 1U))) | (1U & 
                                              (((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_9) 
                                                >> 4U) 
                                               | ((4U 
                                                   == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__sink_r)) 
                                                  & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_10))))) 
                       << 4U)) | ((((2U & ((0x3ffffffeU 
                                            & ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_9) 
                                               >> 2U)) 
                                           | (((3U 
                                                == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__sink_r)) 
                                               & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_10)) 
                                              << 1U))) 
                                    | (1U & (((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_9) 
                                              >> 2U) 
                                             | ((2U 
                                                 == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__sink_r)) 
                                                & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_10))))) 
                                   << 2U) | ((2U & 
                                              ((0xfffffffeU 
                                                & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_9)) 
                                               | (((1U 
                                                    == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__sink_r)) 
                                                   & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_10)) 
                                                  << 1U))) 
                                             | (1U 
                                                & (((0U 
                                                     == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__sink_r)) 
                                                    & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_10)) 
                                                   | (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_9))))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_decoder__DOT__accept_w 
        = ((~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_407)) 
           & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_mrp_strip__DOT__out_vld_r));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_mrp_strip__DOT__space_w 
        = (1U & (~ (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_mrp_strip__DOT__out_vld_r) 
                     & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_mrp_strip__DOT__skid_vld_r)) 
                    | (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_mrp_strip__DOT__skid_vld_r) 
                        & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_mrp_strip__DOT__fetch_r)) 
                       | ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_mrp_strip__DOT__out_vld_r) 
                          & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_mrp_strip__DOT__fetch_r) 
                             & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_407)))))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pr_req_w 
        = ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__ntfy_prng_req_w) 
             << 5U) | (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__draw_req_r) 
                        << 4U) | ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_draw_req_w) 
                                  << 3U))) | (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__draw_req_r) 
                                               << 2U) 
                                              | ((((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__adp_prng_busy_w)) 
                                                   & (7U 
                                                      == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__state_r))) 
                                                  << 1U) 
                                                 | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__lstn_draw_req_w))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__DOT__ff_valid_w = 0U;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__DOT__ff_slot_w = 0U;
    if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__DOT__free_mask_w))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__DOT__ff_valid_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__DOT__ff_slot_w = 0U;
    }
    if ((1U & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__DOT__ff_valid_w)) 
               & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__DOT__free_mask_w) 
                  >> 1U)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__DOT__ff_valid_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__DOT__ff_slot_w = 1U;
    }
    if ((1U & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__DOT__ff_valid_w)) 
               & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__DOT__free_mask_w) 
                  >> 2U)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__DOT__ff_valid_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__DOT__ff_slot_w = 2U;
    }
    if (((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__DOT__ff_valid_w)) 
         & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__DOT__free_mask_w) 
            >> 3U))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__DOT__ff_valid_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__DOT__ff_slot_w = 3U;
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__4__KET____DOT__u_rx_slots__DOT__ff_valid_w = 0U;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__4__KET____DOT__u_rx_slots__DOT__ff_slot_w = 0U;
    if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__4__KET____DOT__u_rx_slots__DOT__free_mask_w))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__4__KET____DOT__u_rx_slots__DOT__ff_valid_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__4__KET____DOT__u_rx_slots__DOT__ff_slot_w = 0U;
    }
    if ((1U & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__4__KET____DOT__u_rx_slots__DOT__ff_valid_w)) 
               & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__4__KET____DOT__u_rx_slots__DOT__free_mask_w) 
                  >> 1U)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__4__KET____DOT__u_rx_slots__DOT__ff_valid_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__4__KET____DOT__u_rx_slots__DOT__ff_slot_w = 1U;
    }
    if ((1U & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__4__KET____DOT__u_rx_slots__DOT__ff_valid_w)) 
               & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__4__KET____DOT__u_rx_slots__DOT__free_mask_w) 
                  >> 2U)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__4__KET____DOT__u_rx_slots__DOT__ff_valid_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__4__KET____DOT__u_rx_slots__DOT__ff_slot_w = 2U;
    }
    if (((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__4__KET____DOT__u_rx_slots__DOT__ff_valid_w)) 
         & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__4__KET____DOT__u_rx_slots__DOT__free_mask_w) 
            >> 3U))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__4__KET____DOT__u_rx_slots__DOT__ff_valid_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__4__KET____DOT__u_rx_slots__DOT__ff_slot_w = 3U;
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__2__KET____DOT__u_rx_slots__DOT__ff_valid_w = 0U;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__2__KET____DOT__u_rx_slots__DOT__ff_slot_w = 0U;
    if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__2__KET____DOT__u_rx_slots__DOT__free_mask_w))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__2__KET____DOT__u_rx_slots__DOT__ff_valid_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__2__KET____DOT__u_rx_slots__DOT__ff_slot_w = 0U;
    }
    if ((1U & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__2__KET____DOT__u_rx_slots__DOT__ff_valid_w)) 
               & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__2__KET____DOT__u_rx_slots__DOT__free_mask_w) 
                  >> 1U)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__2__KET____DOT__u_rx_slots__DOT__ff_valid_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__2__KET____DOT__u_rx_slots__DOT__ff_slot_w = 1U;
    }
    if ((1U & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__2__KET____DOT__u_rx_slots__DOT__ff_valid_w)) 
               & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__2__KET____DOT__u_rx_slots__DOT__free_mask_w) 
                  >> 2U)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__2__KET____DOT__u_rx_slots__DOT__ff_valid_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__2__KET____DOT__u_rx_slots__DOT__ff_slot_w = 2U;
    }
    if (((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__2__KET____DOT__u_rx_slots__DOT__ff_valid_w)) 
         & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__2__KET____DOT__u_rx_slots__DOT__free_mask_w) 
            >> 3U))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__2__KET____DOT__u_rx_slots__DOT__ff_valid_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__2__KET____DOT__u_rx_slots__DOT__ff_slot_w = 3U;
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__1__KET____DOT__u_rx_slots__DOT__ff_valid_w = 0U;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__1__KET____DOT__u_rx_slots__DOT__ff_slot_w = 0U;
    if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__1__KET____DOT__u_rx_slots__DOT__free_mask_w))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__1__KET____DOT__u_rx_slots__DOT__ff_valid_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__1__KET____DOT__u_rx_slots__DOT__ff_slot_w = 0U;
    }
    if ((1U & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__1__KET____DOT__u_rx_slots__DOT__ff_valid_w)) 
               & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__1__KET____DOT__u_rx_slots__DOT__free_mask_w) 
                  >> 1U)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__1__KET____DOT__u_rx_slots__DOT__ff_valid_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__1__KET____DOT__u_rx_slots__DOT__ff_slot_w = 1U;
    }
    if ((1U & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__1__KET____DOT__u_rx_slots__DOT__ff_valid_w)) 
               & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__1__KET____DOT__u_rx_slots__DOT__free_mask_w) 
                  >> 2U)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__1__KET____DOT__u_rx_slots__DOT__ff_valid_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__1__KET____DOT__u_rx_slots__DOT__ff_slot_w = 2U;
    }
    if (((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__1__KET____DOT__u_rx_slots__DOT__ff_valid_w)) 
         & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__1__KET____DOT__u_rx_slots__DOT__free_mask_w) 
            >> 3U))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__1__KET____DOT__u_rx_slots__DOT__ff_valid_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__1__KET____DOT__u_rx_slots__DOT__ff_slot_w = 3U;
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__evt_w 
        = (0x0000000fU & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__src_txn_r)
                           ? ((6U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__msg_x_r))
                               ? (1U & (- (IData)((1U 
                                                   & (~ 
                                                      ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_230) 
                                                       & ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_231) 
                                                          & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__rec_r[0U] 
                                                             >> 0x0000000bU))))))))
                               : ((8U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__msg_x_r))
                                   ? 2U : ((0x0aU == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__msg_x_r))
                                            ? 3U : 
                                           ((0U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__status_x_r))
                                             ? 4U : 5U))))
                           : ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__src_tmr_r)
                               ? (0x79877677U >> (0x0000001cU 
                                                  & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__rec_r[0U] 
                                                     << 2U)))
                               : (0xdcbaU >> ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__tkkind_r) 
                                              << 2U)))));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_257 = (0x0000ffffffffffffULL 
                                                  & ((4U 
                                                      & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_131))
                                                      ? 
                                                     (((1U 
                                                        & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_131))
                                                        ? 
                                                       (vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r
                                                        [
                                                        (0x0000001fU 
                                                         & ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_261) 
                                                            + 
                                                            (0x0000001cU 
                                                             & ((vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r
                                                                 [
                                                                 ((IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__slot_r) 
                                                                  << 1U)] 
                                                                 >> 4U) 
                                                                << 2U))))] 
                                                        & (- (QData)((IData)(
                                                                             ((8U 
                                                                               > 
                                                                               (0x0000000fU 
                                                                                & (vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r
                                                                                [
                                                                                ((IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__slot_r) 
                                                                                << 1U)] 
                                                                                >> 4U))) 
                                                                              & (4U 
                                                                                > (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_261)))))))
                                                        : 
                                                       (((QData)((IData)(vlSelfRef.milan_datapath__DOT__tone_smp_media)) 
                                                         << 0x00000018U) 
                                                        | (QData)((IData)(vlSelfRef.milan_datapath__DOT__tone_smp_media)))) 
                                                      & (- (QData)((IData)(
                                                                           (1U 
                                                                            & (~ 
                                                                               ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_131) 
                                                                                >> 1U)))))))
                                                      : 
                                                     ((2U 
                                                       & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_131))
                                                       ? 
                                                      (vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__tdm_hold_r
                                                       [
                                                       (3U 
                                                        & vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r
                                                        [
                                                        ((IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__slot_r) 
                                                         << 1U)])] 
                                                       & (- (QData)((IData)(
                                                                            ((~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_131)) 
                                                                             & (4U 
                                                                                > (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_261)))))))
                                                       : 
                                                      (vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__i2s_hold_r 
                                                       & (- (QData)((IData)(
                                                                            (1U 
                                                                             & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_131)))))))));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_259 = (0x0000ffffffffffffULL 
                                                  & ((4U 
                                                      & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_130))
                                                      ? 
                                                     (((1U 
                                                        & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_130))
                                                        ? 
                                                       (vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r
                                                        [
                                                        (0x0000001fU 
                                                         & ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_262) 
                                                            + 
                                                            (0x0000001cU 
                                                             & ((vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r
                                                                 [
                                                                 (1U 
                                                                  | ((IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__slot_r) 
                                                                     << 1U))] 
                                                                 >> 4U) 
                                                                << 2U))))] 
                                                        & (- (QData)((IData)(
                                                                             ((8U 
                                                                               > 
                                                                               (0x0000000fU 
                                                                                & (vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r
                                                                                [
                                                                                (1U 
                                                                                | ((IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__slot_r) 
                                                                                << 1U))] 
                                                                                >> 4U))) 
                                                                              & (4U 
                                                                                > (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_262)))))))
                                                        : 
                                                       (((QData)((IData)(vlSelfRef.milan_datapath__DOT__tone_smp_media)) 
                                                         << 0x00000018U) 
                                                        | (QData)((IData)(vlSelfRef.milan_datapath__DOT__tone_smp_media)))) 
                                                      & (- (QData)((IData)(
                                                                           (1U 
                                                                            & (~ 
                                                                               ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_130) 
                                                                                >> 1U)))))))
                                                      : 
                                                     ((2U 
                                                       & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_130))
                                                       ? 
                                                      (vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__tdm_hold_r
                                                       [
                                                       (3U 
                                                        & vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r
                                                        [
                                                        (1U 
                                                         | ((IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__slot_r) 
                                                            << 1U))])] 
                                                       & (- (QData)((IData)(
                                                                            ((~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_130)) 
                                                                             & (4U 
                                                                                > (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_262)))))))
                                                       : 
                                                      (vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__i2s_hold_r 
                                                       & (- (QData)((IData)(
                                                                            (1U 
                                                                             & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_130)))))))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__maap_rsp_live_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_maap_shim__DOT__rsp_valid_r) 
           & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__maap_swallow_w)) 
              & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__maap_busy_r)));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__maap_tmo_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_maap_req_valid_w) 
           & (0x03ffU == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__mreq_tmo_r)));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__maap_accept_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_maap_req_ready_w) 
           & (IData)(vlSelfRef.milan_datapath__DOT__pp_maap_req_valid_w));
    milan_datapath__DOT__avtprx_stopped_w = 0U;
    if ((0U == (IData)(vlSelfRef.milan_datapath__DOT__avtprx_accept_idx_w))) {
        milan_datapath__DOT__avtprx_stopped_w = (1U 
                                                 & (IData)(vlSelfRef.milan_datapath__DOT__acmpl_stopped_v_w));
    }
    if ((1U == (IData)(vlSelfRef.milan_datapath__DOT__avtprx_accept_idx_w))) {
        milan_datapath__DOT__avtprx_stopped_w = (1U 
                                                 & ((IData)(vlSelfRef.milan_datapath__DOT__acmpl_stopped_v_w) 
                                                    >> 1U));
    }
    if ((2U == (IData)(vlSelfRef.milan_datapath__DOT__avtprx_accept_idx_w))) {
        milan_datapath__DOT__avtprx_stopped_w = (1U 
                                                 & ((IData)(vlSelfRef.milan_datapath__DOT__acmpl_stopped_v_w) 
                                                    >> 2U));
    }
    if ((3U == (IData)(vlSelfRef.milan_datapath__DOT__avtprx_accept_idx_w))) {
        milan_datapath__DOT__avtprx_stopped_w = (1U 
                                                 & ((IData)(vlSelfRef.milan_datapath__DOT__acmpl_stopped_v_w) 
                                                    >> 3U));
    }
    if ((4U == (IData)(vlSelfRef.milan_datapath__DOT__avtprx_accept_idx_w))) {
        milan_datapath__DOT__avtprx_stopped_w = (1U 
                                                 & ((IData)(vlSelfRef.milan_datapath__DOT__acmpl_stopped_v_w) 
                                                    >> 4U));
    }
    if ((5U == (IData)(vlSelfRef.milan_datapath__DOT__avtprx_accept_idx_w))) {
        milan_datapath__DOT__avtprx_stopped_w = (1U 
                                                 & ((IData)(vlSelfRef.milan_datapath__DOT__acmpl_stopped_v_w) 
                                                    >> 5U));
    }
    if ((6U == (IData)(vlSelfRef.milan_datapath__DOT__avtprx_accept_idx_w))) {
        milan_datapath__DOT__avtprx_stopped_w = (1U 
                                                 & ((IData)(vlSelfRef.milan_datapath__DOT__acmpl_stopped_v_w) 
                                                    >> 6U));
    }
    if ((7U == (IData)(vlSelfRef.milan_datapath__DOT__avtprx_accept_idx_w))) {
        milan_datapath__DOT__avtprx_stopped_w = (1U 
                                                 & ((IData)(vlSelfRef.milan_datapath__DOT__acmpl_stopped_v_w) 
                                                    >> 7U));
    }
    if ((8U == (IData)(vlSelfRef.milan_datapath__DOT__avtprx_accept_idx_w))) {
        milan_datapath__DOT__avtprx_stopped_w = (1U 
                                                 & ((IData)(vlSelfRef.milan_datapath__DOT__acmpl_stopped_v_w) 
                                                    >> 8U));
    }
    if ((1U & ((vlSelfRef.milan_datapath__DOT__csr__DOT__maap_ctrl 
                >> 1U) & (~ (IData)(vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__seed_used_r))))) {
        vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT____VlemCall_0__rand_offset 
            = (vlSelfRef.milan_datapath__DOT__csr__DOT__maap_ctrl 
               >> 0x00000010U);
    } else {
        vlSelfRef.__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rand_offset__190__cnt 
            = (0x000000ffU & (vlSelfRef.milan_datapath__DOT__csr__DOT__maap_ctrl 
                              >> 8U));
        vlSelfRef.__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rand_offset__190__rnd 
            = vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lfsr_next_w;
        vlSelfRef.__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rand_offset__190__o 
            = (0x0000ffffU & ((0xfe00U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rand_offset__190__rnd))
                               ? ((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rand_offset__190__rnd) 
                                  - (IData)(0xfe00U))
                               : (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rand_offset__190__rnd)));
        if (((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rand_offset__190__o) 
             > (0x0000ffffU & ((IData)(0xfe00U) - (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rand_offset__190__cnt))))) {
            vlSelfRef.__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rand_offset__190__o 
                = (0x0000ffffU & ((IData)(0xfe00U) 
                                  - (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rand_offset__190__cnt)));
        }
        vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT____VlemCall_0__rand_offset 
            = vlSelfRef.__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rand_offset__190__o;
    }
    vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__new_off_w 
        = vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT____VlemCall_0__rand_offset;
    vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__eff_chans_w 
        = ((0U == (IData)(vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__chans_raw_w))
            ? 2U : (IData)(vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__chans_raw_w));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_maap_q__DOT__rd_en_w 
        = ((0U != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_maap_q__DOT__cnt_r)) 
           & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_maap_q__DOT__out_valid_r)) 
              | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__maap_txn_ready_w)));
    __Vfunc_milan_datapath__DOT__amap_out_cluster__7__port_i 
        = (7U & (vlSelfRef.milan_datapath__DOT__csr__DOT__chmap_sel 
                 >> 3U));
    __Vfunc_milan_datapath__DOT__amap_out_cluster__7__e 
        = vlSelfRef.milan_datapath__DOT__cfg_cmap_entry_w;
    __Vfunc_milan_datapath__DOT__amap_out_cluster__7__r = 0U;
    if ((0U == (IData)(__Vfunc_milan_datapath__DOT__amap_out_cluster__7__port_i))) {
        vlSelfRef.__Vfunc_milan_datapath__DOT__amap_out_cluster__7__unnamedblk5__DOT__unnamedblk6__DOT__c = 0U;
        while (VL_GTS_III(32, 0x00000048U, vlSelfRef.__Vfunc_milan_datapath__DOT__amap_out_cluster__7__unnamedblk5__DOT__unnamedblk6__DOT__c)) {
            if (((((~ (__Vfunc_milan_datapath__DOT__amap_out_cluster__7__r 
                       >> 0x10U)) & (9U > vlSelfRef.__Vfunc_milan_datapath__DOT__amap_out_cluster__7__unnamedblk5__DOT__unnamedblk6__DOT__c)) 
                  & ((IData)(__Vfunc_milan_datapath__DOT__amap_out_cluster__7__e) 
                     >> 0x0cU)) & (((0x47U >= (0x0000007fU 
                                               & vlSelfRef.__Vfunc_milan_datapath__DOT__amap_out_cluster__7__unnamedblk5__DOT__unnamedblk6__DOT__c))
                                     ? vlSelfRef.milan_datapath__DOT__ADP_DMAP_OUT_CSRC_C
                                    [(0x0000007fU & vlSelfRef.__Vfunc_milan_datapath__DOT__amap_out_cluster__7__unnamedblk5__DOT__unnamedblk6__DOT__c)]
                                     : 0U) == (IData)(__Vfunc_milan_datapath__DOT__amap_out_cluster__7__e)))) {
                __Vfunc_milan_datapath__DOT__amap_out_cluster__7__r 
                    = (0x00010000U | (0x0000ffffU & vlSelfRef.__Vfunc_milan_datapath__DOT__amap_out_cluster__7__unnamedblk5__DOT__unnamedblk6__DOT__c));
            }
            vlSelfRef.__Vfunc_milan_datapath__DOT__amap_out_cluster__7__unnamedblk5__DOT__unnamedblk6__DOT__c 
                = ((IData)(1U) + vlSelfRef.__Vfunc_milan_datapath__DOT__amap_out_cluster__7__unnamedblk5__DOT__unnamedblk6__DOT__c);
        }
    }
    if ((1U == (IData)(__Vfunc_milan_datapath__DOT__amap_out_cluster__7__port_i))) {
        vlSelfRef.__Vfunc_milan_datapath__DOT__amap_out_cluster__7__unnamedblk5__DOT__unnamedblk6__DOT__c = 0U;
        while (VL_GTS_III(32, 0x00000048U, vlSelfRef.__Vfunc_milan_datapath__DOT__amap_out_cluster__7__unnamedblk5__DOT__unnamedblk6__DOT__c)) {
            if ((((((~ (__Vfunc_milan_datapath__DOT__amap_out_cluster__7__r 
                        >> 0x10U)) & (9U <= vlSelfRef.__Vfunc_milan_datapath__DOT__amap_out_cluster__7__unnamedblk5__DOT__unnamedblk6__DOT__c)) 
                   & (0x00000012U > vlSelfRef.__Vfunc_milan_datapath__DOT__amap_out_cluster__7__unnamedblk5__DOT__unnamedblk6__DOT__c)) 
                  & ((IData)(__Vfunc_milan_datapath__DOT__amap_out_cluster__7__e) 
                     >> 0x0cU)) & (((0x47U >= (0x0000007fU 
                                               & vlSelfRef.__Vfunc_milan_datapath__DOT__amap_out_cluster__7__unnamedblk5__DOT__unnamedblk6__DOT__c))
                                     ? vlSelfRef.milan_datapath__DOT__ADP_DMAP_OUT_CSRC_C
                                    [(0x0000007fU & vlSelfRef.__Vfunc_milan_datapath__DOT__amap_out_cluster__7__unnamedblk5__DOT__unnamedblk6__DOT__c)]
                                     : 0U) == (IData)(__Vfunc_milan_datapath__DOT__amap_out_cluster__7__e)))) {
                __Vfunc_milan_datapath__DOT__amap_out_cluster__7__r 
                    = (0x00010000U | (0x0000ffffU & 
                                      (vlSelfRef.__Vfunc_milan_datapath__DOT__amap_out_cluster__7__unnamedblk5__DOT__unnamedblk6__DOT__c 
                                       - (IData)(9U))));
            }
            vlSelfRef.__Vfunc_milan_datapath__DOT__amap_out_cluster__7__unnamedblk5__DOT__unnamedblk6__DOT__c 
                = ((IData)(1U) + vlSelfRef.__Vfunc_milan_datapath__DOT__amap_out_cluster__7__unnamedblk5__DOT__unnamedblk6__DOT__c);
        }
    }
    if ((2U == (IData)(__Vfunc_milan_datapath__DOT__amap_out_cluster__7__port_i))) {
        vlSelfRef.__Vfunc_milan_datapath__DOT__amap_out_cluster__7__unnamedblk5__DOT__unnamedblk6__DOT__c = 0U;
        while (VL_GTS_III(32, 0x00000048U, vlSelfRef.__Vfunc_milan_datapath__DOT__amap_out_cluster__7__unnamedblk5__DOT__unnamedblk6__DOT__c)) {
            if ((((((~ (__Vfunc_milan_datapath__DOT__amap_out_cluster__7__r 
                        >> 0x10U)) & (0x00000012U <= vlSelfRef.__Vfunc_milan_datapath__DOT__amap_out_cluster__7__unnamedblk5__DOT__unnamedblk6__DOT__c)) 
                   & (0x0000001bU > vlSelfRef.__Vfunc_milan_datapath__DOT__amap_out_cluster__7__unnamedblk5__DOT__unnamedblk6__DOT__c)) 
                  & ((IData)(__Vfunc_milan_datapath__DOT__amap_out_cluster__7__e) 
                     >> 0x0cU)) & (((0x47U >= (0x0000007fU 
                                               & vlSelfRef.__Vfunc_milan_datapath__DOT__amap_out_cluster__7__unnamedblk5__DOT__unnamedblk6__DOT__c))
                                     ? vlSelfRef.milan_datapath__DOT__ADP_DMAP_OUT_CSRC_C
                                    [(0x0000007fU & vlSelfRef.__Vfunc_milan_datapath__DOT__amap_out_cluster__7__unnamedblk5__DOT__unnamedblk6__DOT__c)]
                                     : 0U) == (IData)(__Vfunc_milan_datapath__DOT__amap_out_cluster__7__e)))) {
                __Vfunc_milan_datapath__DOT__amap_out_cluster__7__r 
                    = (0x00010000U | (0x0000ffffU & 
                                      (vlSelfRef.__Vfunc_milan_datapath__DOT__amap_out_cluster__7__unnamedblk5__DOT__unnamedblk6__DOT__c 
                                       - (IData)(0x0012U))));
            }
            vlSelfRef.__Vfunc_milan_datapath__DOT__amap_out_cluster__7__unnamedblk5__DOT__unnamedblk6__DOT__c 
                = ((IData)(1U) + vlSelfRef.__Vfunc_milan_datapath__DOT__amap_out_cluster__7__unnamedblk5__DOT__unnamedblk6__DOT__c);
        }
    }
    if ((3U == (IData)(__Vfunc_milan_datapath__DOT__amap_out_cluster__7__port_i))) {
        vlSelfRef.__Vfunc_milan_datapath__DOT__amap_out_cluster__7__unnamedblk5__DOT__unnamedblk6__DOT__c = 0U;
        while (VL_GTS_III(32, 0x00000048U, vlSelfRef.__Vfunc_milan_datapath__DOT__amap_out_cluster__7__unnamedblk5__DOT__unnamedblk6__DOT__c)) {
            if ((((((~ (__Vfunc_milan_datapath__DOT__amap_out_cluster__7__r 
                        >> 0x10U)) & (0x0000001bU <= vlSelfRef.__Vfunc_milan_datapath__DOT__amap_out_cluster__7__unnamedblk5__DOT__unnamedblk6__DOT__c)) 
                   & (0x00000024U > vlSelfRef.__Vfunc_milan_datapath__DOT__amap_out_cluster__7__unnamedblk5__DOT__unnamedblk6__DOT__c)) 
                  & ((IData)(__Vfunc_milan_datapath__DOT__amap_out_cluster__7__e) 
                     >> 0x0cU)) & (((0x47U >= (0x0000007fU 
                                               & vlSelfRef.__Vfunc_milan_datapath__DOT__amap_out_cluster__7__unnamedblk5__DOT__unnamedblk6__DOT__c))
                                     ? vlSelfRef.milan_datapath__DOT__ADP_DMAP_OUT_CSRC_C
                                    [(0x0000007fU & vlSelfRef.__Vfunc_milan_datapath__DOT__amap_out_cluster__7__unnamedblk5__DOT__unnamedblk6__DOT__c)]
                                     : 0U) == (IData)(__Vfunc_milan_datapath__DOT__amap_out_cluster__7__e)))) {
                __Vfunc_milan_datapath__DOT__amap_out_cluster__7__r 
                    = (0x00010000U | (0x0000ffffU & 
                                      (vlSelfRef.__Vfunc_milan_datapath__DOT__amap_out_cluster__7__unnamedblk5__DOT__unnamedblk6__DOT__c 
                                       - (IData)(0x001bU))));
            }
            vlSelfRef.__Vfunc_milan_datapath__DOT__amap_out_cluster__7__unnamedblk5__DOT__unnamedblk6__DOT__c 
                = ((IData)(1U) + vlSelfRef.__Vfunc_milan_datapath__DOT__amap_out_cluster__7__unnamedblk5__DOT__unnamedblk6__DOT__c);
        }
    }
    if ((4U == (IData)(__Vfunc_milan_datapath__DOT__amap_out_cluster__7__port_i))) {
        vlSelfRef.__Vfunc_milan_datapath__DOT__amap_out_cluster__7__unnamedblk5__DOT__unnamedblk6__DOT__c = 0U;
        while (VL_GTS_III(32, 0x00000048U, vlSelfRef.__Vfunc_milan_datapath__DOT__amap_out_cluster__7__unnamedblk5__DOT__unnamedblk6__DOT__c)) {
            if ((((((~ (__Vfunc_milan_datapath__DOT__amap_out_cluster__7__r 
                        >> 0x10U)) & (0x00000024U <= vlSelfRef.__Vfunc_milan_datapath__DOT__amap_out_cluster__7__unnamedblk5__DOT__unnamedblk6__DOT__c)) 
                   & (0x0000002dU > vlSelfRef.__Vfunc_milan_datapath__DOT__amap_out_cluster__7__unnamedblk5__DOT__unnamedblk6__DOT__c)) 
                  & ((IData)(__Vfunc_milan_datapath__DOT__amap_out_cluster__7__e) 
                     >> 0x0cU)) & (((0x47U >= (0x0000007fU 
                                               & vlSelfRef.__Vfunc_milan_datapath__DOT__amap_out_cluster__7__unnamedblk5__DOT__unnamedblk6__DOT__c))
                                     ? vlSelfRef.milan_datapath__DOT__ADP_DMAP_OUT_CSRC_C
                                    [(0x0000007fU & vlSelfRef.__Vfunc_milan_datapath__DOT__amap_out_cluster__7__unnamedblk5__DOT__unnamedblk6__DOT__c)]
                                     : 0U) == (IData)(__Vfunc_milan_datapath__DOT__amap_out_cluster__7__e)))) {
                __Vfunc_milan_datapath__DOT__amap_out_cluster__7__r 
                    = (0x00010000U | (0x0000ffffU & 
                                      (vlSelfRef.__Vfunc_milan_datapath__DOT__amap_out_cluster__7__unnamedblk5__DOT__unnamedblk6__DOT__c 
                                       - (IData)(0x0024U))));
            }
            vlSelfRef.__Vfunc_milan_datapath__DOT__amap_out_cluster__7__unnamedblk5__DOT__unnamedblk6__DOT__c 
                = ((IData)(1U) + vlSelfRef.__Vfunc_milan_datapath__DOT__amap_out_cluster__7__unnamedblk5__DOT__unnamedblk6__DOT__c);
        }
    }
    if ((5U == (IData)(__Vfunc_milan_datapath__DOT__amap_out_cluster__7__port_i))) {
        vlSelfRef.__Vfunc_milan_datapath__DOT__amap_out_cluster__7__unnamedblk5__DOT__unnamedblk6__DOT__c = 0U;
        while (VL_GTS_III(32, 0x00000048U, vlSelfRef.__Vfunc_milan_datapath__DOT__amap_out_cluster__7__unnamedblk5__DOT__unnamedblk6__DOT__c)) {
            if ((((((~ (__Vfunc_milan_datapath__DOT__amap_out_cluster__7__r 
                        >> 0x10U)) & (0x0000002dU <= vlSelfRef.__Vfunc_milan_datapath__DOT__amap_out_cluster__7__unnamedblk5__DOT__unnamedblk6__DOT__c)) 
                   & (0x00000036U > vlSelfRef.__Vfunc_milan_datapath__DOT__amap_out_cluster__7__unnamedblk5__DOT__unnamedblk6__DOT__c)) 
                  & ((IData)(__Vfunc_milan_datapath__DOT__amap_out_cluster__7__e) 
                     >> 0x0cU)) & (((0x47U >= (0x0000007fU 
                                               & vlSelfRef.__Vfunc_milan_datapath__DOT__amap_out_cluster__7__unnamedblk5__DOT__unnamedblk6__DOT__c))
                                     ? vlSelfRef.milan_datapath__DOT__ADP_DMAP_OUT_CSRC_C
                                    [(0x0000007fU & vlSelfRef.__Vfunc_milan_datapath__DOT__amap_out_cluster__7__unnamedblk5__DOT__unnamedblk6__DOT__c)]
                                     : 0U) == (IData)(__Vfunc_milan_datapath__DOT__amap_out_cluster__7__e)))) {
                __Vfunc_milan_datapath__DOT__amap_out_cluster__7__r 
                    = (0x00010000U | (0x0000ffffU & 
                                      (vlSelfRef.__Vfunc_milan_datapath__DOT__amap_out_cluster__7__unnamedblk5__DOT__unnamedblk6__DOT__c 
                                       - (IData)(0x002dU))));
            }
            vlSelfRef.__Vfunc_milan_datapath__DOT__amap_out_cluster__7__unnamedblk5__DOT__unnamedblk6__DOT__c 
                = ((IData)(1U) + vlSelfRef.__Vfunc_milan_datapath__DOT__amap_out_cluster__7__unnamedblk5__DOT__unnamedblk6__DOT__c);
        }
    }
    if ((6U == (IData)(__Vfunc_milan_datapath__DOT__amap_out_cluster__7__port_i))) {
        vlSelfRef.__Vfunc_milan_datapath__DOT__amap_out_cluster__7__unnamedblk5__DOT__unnamedblk6__DOT__c = 0U;
        while (VL_GTS_III(32, 0x00000048U, vlSelfRef.__Vfunc_milan_datapath__DOT__amap_out_cluster__7__unnamedblk5__DOT__unnamedblk6__DOT__c)) {
            if ((((((~ (__Vfunc_milan_datapath__DOT__amap_out_cluster__7__r 
                        >> 0x10U)) & (0x00000036U <= vlSelfRef.__Vfunc_milan_datapath__DOT__amap_out_cluster__7__unnamedblk5__DOT__unnamedblk6__DOT__c)) 
                   & (0x0000003fU > vlSelfRef.__Vfunc_milan_datapath__DOT__amap_out_cluster__7__unnamedblk5__DOT__unnamedblk6__DOT__c)) 
                  & ((IData)(__Vfunc_milan_datapath__DOT__amap_out_cluster__7__e) 
                     >> 0x0cU)) & (((0x47U >= (0x0000007fU 
                                               & vlSelfRef.__Vfunc_milan_datapath__DOT__amap_out_cluster__7__unnamedblk5__DOT__unnamedblk6__DOT__c))
                                     ? vlSelfRef.milan_datapath__DOT__ADP_DMAP_OUT_CSRC_C
                                    [(0x0000007fU & vlSelfRef.__Vfunc_milan_datapath__DOT__amap_out_cluster__7__unnamedblk5__DOT__unnamedblk6__DOT__c)]
                                     : 0U) == (IData)(__Vfunc_milan_datapath__DOT__amap_out_cluster__7__e)))) {
                __Vfunc_milan_datapath__DOT__amap_out_cluster__7__r 
                    = (0x00010000U | (0x0000ffffU & 
                                      (vlSelfRef.__Vfunc_milan_datapath__DOT__amap_out_cluster__7__unnamedblk5__DOT__unnamedblk6__DOT__c 
                                       - (IData)(0x0036U))));
            }
            vlSelfRef.__Vfunc_milan_datapath__DOT__amap_out_cluster__7__unnamedblk5__DOT__unnamedblk6__DOT__c 
                = ((IData)(1U) + vlSelfRef.__Vfunc_milan_datapath__DOT__amap_out_cluster__7__unnamedblk5__DOT__unnamedblk6__DOT__c);
        }
    }
    if ((7U == (IData)(__Vfunc_milan_datapath__DOT__amap_out_cluster__7__port_i))) {
        vlSelfRef.__Vfunc_milan_datapath__DOT__amap_out_cluster__7__unnamedblk5__DOT__unnamedblk6__DOT__c = 0U;
        while (VL_GTS_III(32, 0x00000048U, vlSelfRef.__Vfunc_milan_datapath__DOT__amap_out_cluster__7__unnamedblk5__DOT__unnamedblk6__DOT__c)) {
            if ((((((~ (__Vfunc_milan_datapath__DOT__amap_out_cluster__7__r 
                        >> 0x10U)) & (0x0000003fU <= vlSelfRef.__Vfunc_milan_datapath__DOT__amap_out_cluster__7__unnamedblk5__DOT__unnamedblk6__DOT__c)) 
                   & (0x00000048U > vlSelfRef.__Vfunc_milan_datapath__DOT__amap_out_cluster__7__unnamedblk5__DOT__unnamedblk6__DOT__c)) 
                  & ((IData)(__Vfunc_milan_datapath__DOT__amap_out_cluster__7__e) 
                     >> 0x0cU)) & (((0x47U >= (0x0000007fU 
                                               & vlSelfRef.__Vfunc_milan_datapath__DOT__amap_out_cluster__7__unnamedblk5__DOT__unnamedblk6__DOT__c))
                                     ? vlSelfRef.milan_datapath__DOT__ADP_DMAP_OUT_CSRC_C
                                    [(0x0000007fU & vlSelfRef.__Vfunc_milan_datapath__DOT__amap_out_cluster__7__unnamedblk5__DOT__unnamedblk6__DOT__c)]
                                     : 0U) == (IData)(__Vfunc_milan_datapath__DOT__amap_out_cluster__7__e)))) {
                __Vfunc_milan_datapath__DOT__amap_out_cluster__7__r 
                    = (0x00010000U | (0x0000ffffU & 
                                      (vlSelfRef.__Vfunc_milan_datapath__DOT__amap_out_cluster__7__unnamedblk5__DOT__unnamedblk6__DOT__c 
                                       - (IData)(0x003fU))));
            }
            vlSelfRef.__Vfunc_milan_datapath__DOT__amap_out_cluster__7__unnamedblk5__DOT__unnamedblk6__DOT__c 
                = ((IData)(1U) + vlSelfRef.__Vfunc_milan_datapath__DOT__amap_out_cluster__7__unnamedblk5__DOT__unnamedblk6__DOT__c);
        }
    }
    __Vfunc_milan_datapath__DOT__amap_out_cluster__7__Vfuncout 
        = __Vfunc_milan_datapath__DOT__amap_out_cluster__7__r;
    vlSelfRef.milan_datapath__DOT__cfg_cmap_cluster_w 
        = __Vfunc_milan_datapath__DOT__amap_out_cluster__7__Vfuncout;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__b_vlan_w = 0U;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__b_da_w = 0ULL;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__b_sid_w = 0ULL;
    if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__bk_r) 
                  >> 2U)))) {
        if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__bk_r))) {
            if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__bk_r))) {
                if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__settled_w) {
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__b_vlan_w 
                        = (0x00000fffU & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__rec_r[9U] 
                                          >> 0x00000010U));
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__b_da_w 
                        = (0x0000ffffffffffffULL & 
                           (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__rec_r[9U])) 
                             << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__rec_r[8U]))));
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__b_sid_w 
                        = (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__rec_r[7U])) 
                            << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__rec_r[6U])));
                } else {
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__b_vlan_w = 0U;
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__b_da_w = 0ULL;
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__b_sid_w = 0ULL;
                }
            }
        }
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__cap_active_w 
        = ((0U != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__hs_r)) 
           & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__recwr_en_w));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_maap_q__DOT__push_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_normalizer__DOT__txn_valid_r) 
           & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_294));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_acmp_q__DOT__push_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_normalizer__DOT__txn_valid_r) 
           & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_295));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_adp_q__DOT__push_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_normalizer__DOT__txn_valid_r) 
           & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_296));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__wr_madr_w 
        = (0x00000fffU & (((IData)(0x00000240U) * (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pool_wr_slot_w)) 
                          + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pool_wr_addr_w)));
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pool_oversize_w 
        = ((0x0240U < (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__frame_len_r)) 
           & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_178));
    vlSelfRef.milan_datapath__DOT____Vcellinp__aaf_packetizer__transit_ns_i[0U] 
        = (IData)((((QData)((IData)(((2U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__ptoff_v_r))
                                      ? vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__ptoff_r[1U]
                                      : 0x001e8480U))) 
                    << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT____Vcellinp__avtp_rx_monitor__pres_ofs_i))));
    vlSelfRef.milan_datapath__DOT____Vcellinp__aaf_packetizer__transit_ns_i[1U] 
        = (IData)(((((QData)((IData)(((2U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__ptoff_v_r))
                                       ? vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__ptoff_r[1U]
                                       : 0x001e8480U))) 
                     << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT____Vcellinp__avtp_rx_monitor__pres_ofs_i))) 
                   >> 0x00000020U));
    vlSelfRef.milan_datapath__DOT____Vcellinp__aaf_packetizer__transit_ns_i[2U] 
        = (IData)((((QData)((IData)(((8U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__ptoff_v_r))
                                      ? vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__ptoff_r[3U]
                                      : 0x001e8480U))) 
                    << 0x00000020U) | (QData)((IData)(
                                                      ((4U 
                                                        & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__ptoff_v_r))
                                                        ? vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__ptoff_r[2U]
                                                        : 0x001e8480U)))));
    vlSelfRef.milan_datapath__DOT____Vcellinp__aaf_packetizer__transit_ns_i[3U] 
        = (IData)(((((QData)((IData)(((8U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__ptoff_v_r))
                                       ? vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__ptoff_r[3U]
                                       : 0x001e8480U))) 
                     << 0x00000020U) | (QData)((IData)(
                                                       ((4U 
                                                         & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__ptoff_v_r))
                                                         ? vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__ptoff_r[2U]
                                                         : 0x001e8480U)))) 
                   >> 0x00000020U));
    vlSelfRef.milan_datapath__DOT____Vcellinp__aaf_packetizer__transit_ns_i[4U] 
        = (IData)((((QData)((IData)(((0x00000020U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__ptoff_v_r))
                                      ? vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__ptoff_r[5U]
                                      : 0x001e8480U))) 
                    << 0x00000020U) | (QData)((IData)(
                                                      ((0x00000010U 
                                                        & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__ptoff_v_r))
                                                        ? vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__ptoff_r[4U]
                                                        : 0x001e8480U)))));
    vlSelfRef.milan_datapath__DOT____Vcellinp__aaf_packetizer__transit_ns_i[5U] 
        = (IData)(((((QData)((IData)(((0x00000020U 
                                       & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__ptoff_v_r))
                                       ? vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__ptoff_r[5U]
                                       : 0x001e8480U))) 
                     << 0x00000020U) | (QData)((IData)(
                                                       ((0x00000010U 
                                                         & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__ptoff_v_r))
                                                         ? vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__ptoff_r[4U]
                                                         : 0x001e8480U)))) 
                   >> 0x00000020U));
    vlSelfRef.milan_datapath__DOT____Vcellinp__aaf_packetizer__transit_ns_i[6U] 
        = (IData)((((QData)((IData)(((0x00000080U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__ptoff_v_r))
                                      ? vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__ptoff_r[7U]
                                      : 0x001e8480U))) 
                    << 0x00000020U) | (QData)((IData)(
                                                      ((0x00000040U 
                                                        & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__ptoff_v_r))
                                                        ? vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__ptoff_r[6U]
                                                        : 0x001e8480U)))));
    vlSelfRef.milan_datapath__DOT____Vcellinp__aaf_packetizer__transit_ns_i[7U] 
        = (IData)(((((QData)((IData)(((0x00000080U 
                                       & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__ptoff_v_r))
                                       ? vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__ptoff_r[7U]
                                       : 0x001e8480U))) 
                     << 0x00000020U) | (QData)((IData)(
                                                       ((0x00000040U 
                                                         & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__ptoff_v_r))
                                                         ? vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__ptoff_r[6U]
                                                         : 0x001e8480U)))) 
                   >> 0x00000020U));
    vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__new_evt_w[0U] 
        = ((0xfffffffcU & vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__new_evt_w[0U]) 
           | ((VL_GTS_III(32, 0U, vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__tsd_w) 
               << 1U) | (VL_LTES_III(32, 0U, vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__tsd_w) 
                         & (vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__tsd_w 
                            > ((IData)(0x00989680U) 
                               + vlSelfRef.milan_datapath__DOT____Vcellinp__avtp_rx_monitor__pres_ofs_i)))));
    vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__new_evt_w[0U] 
        = ((3U & vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__new_evt_w[0U]) 
           | (vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__tsd_w 
              << 2U));
    vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__new_evt_w[1U] 
        = ((vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__tsd_w 
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
        = ((0x00fffffcU & vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__new_evt_w[4U]) 
           | (0x00ffffffU & (vlSelfRef.milan_datapath__DOT__avtprx_ts 
                             >> 0x0000001eU)));
    vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__new_evt_w[4U] 
        = ((3U & vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__new_evt_w[4U]) 
           | (0x00ffffffU & (((((IData)(vlSelfRef.milan_datapath__DOT__avtprx_idx) 
                                << 0x00000013U) | ((IData)(vlSelfRef.milan_datapath__DOT__avtprx_subtype) 
                                                   << 0x0000000bU)) 
                              | (((IData)(vlSelfRef.milan_datapath__DOT__avtprx_seq) 
                                  << 3U) | (((IData)(vlSelfRef.milan_datapath__DOT__avtprx_tu_bit) 
                                             << 2U) 
                                            | (((IData)(vlSelfRef.milan_datapath__DOT__avtprx_tv_bit) 
                                                << 1U) 
                                               | (IData)(vlSelfRef.milan_datapath__DOT__avtprx_mr_bit))))) 
                             << 2U)));
    milan_datapath__DOT__amap_opage_ok_w = ((0U == (IData)(vlSelfRef.milan_datapath__DOT__amapq_map_r)) 
                                            & (IData)(vlSelfRef.milan_datapath__DOT__amap_spo_w));
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
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__fl_giveup_w 
        = ((2U <= vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__fl_retry_r) 
           & (((0x0fU == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__hs_r)) 
               | (0x0eU == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__hs_r))) 
              & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__nvm_err_w)));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__line_waddr_w 
        = (0x0000007fU & ((0x0cU == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__st_r))
                           ? ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__patch_abs_byte_w) 
                              >> 3U) : (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__beat_ix_r)));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__line_wdata_w 
        = vlSelfRef.i_desc_mem_rsp_data;
    if ((0x0cU == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__st_r))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__line_wdata_w 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__line_q_r;
        if ((0U == (7U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__patch_abs_byte_w)))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__line_wdata_w 
                = ((0x00ffffffffffffffULL & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__line_wdata_w) 
                   | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__patch_data_w)) 
                      << 0x00000038U));
        }
        if ((1U == (7U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__patch_abs_byte_w)))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__line_wdata_w 
                = ((0xff00ffffffffffffULL & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__line_wdata_w) 
                   | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__patch_data_w)) 
                      << 0x00000030U));
        }
        if ((2U == (7U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__patch_abs_byte_w)))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__line_wdata_w 
                = ((0xffff00ffffffffffULL & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__line_wdata_w) 
                   | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__patch_data_w)) 
                      << 0x00000028U));
        }
        if ((3U == (7U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__patch_abs_byte_w)))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__line_wdata_w 
                = ((0xffffff00ffffffffULL & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__line_wdata_w) 
                   | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__patch_data_w)) 
                      << 0x00000020U));
        }
        if ((4U == (7U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__patch_abs_byte_w)))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__line_wdata_w 
                = ((0xffffffff00ffffffULL & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__line_wdata_w) 
                   | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__patch_data_w)) 
                      << 0x00000018U));
        }
        if ((5U == (7U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__patch_abs_byte_w)))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__line_wdata_w 
                = ((0xffffffffff00ffffULL & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__line_wdata_w) 
                   | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__patch_data_w)) 
                      << 0x00000010U));
        }
        if ((6U == (7U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__patch_abs_byte_w)))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__line_wdata_w 
                = ((0xffffffffffff00ffULL & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__line_wdata_w) 
                   | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__patch_data_w)) 
                      << 8U));
        }
        if ((7U == (7U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__patch_abs_byte_w)))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__line_wdata_w 
                = ((0xffffffffffffff00ULL & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__line_wdata_w) 
                   | (IData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__patch_data_w)));
        }
    }
    __VdfgRegularize_h6e95ff9d_0_403 = (1U & (~ ((4U 
                                                  == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__cnt_r)) 
                                                 | (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_297))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__rs_empty_w 
        = ((3U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__hs_r)) 
           & ((0U == vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__rbcnt_r) 
              & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__nvm_err_w) 
                 | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__nvm_done_w))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__rs_complete_w 
        = ((3U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__hs_r)) 
           & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__nvm_done_w) 
              & ((8U <= vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__rbcnt_r) 
                 & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__rbcnt_r 
                    == (0x0001ffffU & ((IData)(8U) 
                                       + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__rplen_r)))))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__rs_torn_w 
        = ((3U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__hs_r)) 
           & (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__nvm_done_w) 
               & ((0U != vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__rbcnt_r) 
                  & ((8U > vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__rbcnt_r) 
                     | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__rbcnt_r 
                        != (0x0001ffffU & ((IData)(8U) 
                                           + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__rplen_r))))))) 
              | ((0U != vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__rbcnt_r) 
                 & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__nvm_err_w))));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_47 = ((5U 
                                                  == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__st_r)) 
                                                 & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__beat_w));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__aecp_sb_done_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__aecp_sb_active_r) 
           & (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__aecp_sb_slot_r) 
               == (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cmd_r[1U] 
                         >> 0x00000019U))) & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__aecp_rxs_free_w)));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__keep_w 
        = ((0x000cU <= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__babs_w)) 
           & (0x0250U > (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__babs_w)));
    vlSelfRef.milan_datapath__DOT____Vcellinp__media_clock_restart__frame_p_i 
        = ((IData)(vlSelfRef.milan_datapath__DOT__aaf_frame_p_w) 
           | (IData)(vlSelfRef.milan_datapath__DOT__tkd_crf_p_w));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__fit_w 
        = ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__cand_w 
            <= (QData)((IData)(((((IData)(vlSelfRef.o_mac_is_1g)
                                   ? 0x3b9aca00U : 0x05f5e100U) 
                                 >> 1U) + (((IData)(vlSelfRef.o_mac_is_1g)
                                             ? 0x3b9aca00U
                                             : 0x05f5e100U) 
                                           >> 2U))))) 
           & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_298));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__enable_rise_w 
        = ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__enable_q_r)) 
           & (IData)(vlSelfRef.milan_datapath__DOT____Vcellinp__pp_shadow__enable_i));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__enable_fall_w 
        = ((~ (IData)(vlSelfRef.milan_datapath__DOT____Vcellinp__pp_shadow__enable_i)) 
           & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__enable_q_r));
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
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__rec_base_w = 0U;
    if ((0U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__rec_r))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__rec_base_w = 0U;
    } else if ((1U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__rec_r))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__rec_base_w = 0x0000000aU;
    } else if (((2U <= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__rec_r)) 
                & (3U > (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__rec_r)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__rec_base_w 
            = (0x0003ffffU & ((IData)(0x0000001aU) 
                              + ((IData)(0x0000000cU) 
                                 * (0x0003ffffU & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__rec_r) 
                                                   - (IData)(2U))))));
    } else if (((0x0aU <= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__rec_r)) 
                & (0x0bU > (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__rec_r)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__rec_base_w 
            = (0x0003ffffU & ((IData)(0x00000026U) 
                              + ((IData)(0x0000000aU) 
                                 * (0x0003ffffU & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__rec_r) 
                                                   - (IData)(0x0000000aU))))));
    } else if (((0x12U <= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__rec_r)) 
                & (0x13U > (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__rec_r)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__rec_base_w 
            = (0x0003ffffU & ((IData)(0x00000030U) 
                              + ((IData)(0x0000004aU) 
                                 * (0x0003ffffU & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__rec_r) 
                                                   - (IData)(0x00000012U))))));
    } else if (((0x20U <= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__rec_r)) 
                & (0x29U > (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__rec_r)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__rec_base_w 
            = (0x0003ffffU & ((IData)(0x0000007aU) 
                              + ((IData)(0x0000001cU) 
                                 * (0x0003ffffU & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__rec_r) 
                                                   - (IData)(0x00000020U))))));
    } else if (((0x30U <= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__rec_r)) 
                & (0x39U > (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__rec_r)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__rec_base_w 
            = (0x0003ffffU & ((IData)(0x00000176U) 
                              + (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__rec_r) 
                                  - (IData)(0x00000030U)) 
                                 << 4U)));
    } else if (((0x40U <= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__rec_r)) 
                & (0x49U > (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__rec_r)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__rec_base_w 
            = (0x0003ffffU & ((IData)(0x00000206U) 
                              + (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__rec_r) 
                                  - (IData)(0x00000040U)) 
                                 << 4U)));
    } else if (((0x50U <= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__rec_r)) 
                & (0x59U > (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__rec_r)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__rec_base_w 
            = (0x0003ffffU & ((IData)(0x00000296U) 
                              + ((IData)(0x0000000cU) 
                                 * (0x0003ffffU & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__rec_r) 
                                                   - (IData)(0x00000050U))))));
    } else if (((0x60U <= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__rec_r)) 
                & (0x68U > (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__rec_r)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__rec_base_w 
            = (0x0003ffffU & ((IData)(0x00000302U) 
                              + vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__mapi_pref_r
                              [(7U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__rec_r))]));
    } else if (((0x70U <= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__rec_r)) 
                & (0x78U > (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__rec_r)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__rec_base_w 
            = (0x0003ffffU & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__b_mapo_w 
                              + vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__mapo_pref_r
                              [(7U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__rec_r))]));
    } else if (((0x80U <= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__rec_r)) 
                & (0xe3U > (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__rec_r)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__rec_base_w 
            = (0x0003ffffU & ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__b_mapo_w 
                               + (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__mapo_len_r[7U] 
                                  + vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__mapo_pref_r[7U])) 
                              + ((IData)(0x00000048U) 
                                 * (0x0003ffffU & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__rec_r) 
                                                   - (IData)(0x00000080U))))));
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_txs_alloc_req_w 
        = ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_txs_gnt_w)) 
           & (1U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__st_r)));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__vlan_user_valid_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vsel_v_w) 
           | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vsel_v_w));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__vu_sel_ls_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vsel_v_w) 
           & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vsel_v_w)) 
              | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__vrr_r)));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__fsm_wr_gnt_w 
        = ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__c1_wr_w)) 
           & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__fsm_wr_req_w));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__wr_en_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__c1_wr_w) 
           | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__fsm_wr_req_w));
    if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__c1_wr_w) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__wr_addr_w 
            = (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__c1_sink_r));
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__wr_data_w[0U] 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__c1_proj_r[0U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__wr_data_w[1U] 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__c1_proj_r[1U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__wr_data_w[2U] 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__c1_proj_r[2U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__wr_data_w[3U] 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__c1_proj_r[3U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__wr_data_w[4U] 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__c1_proj_r[4U];
    } else if ((0U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__hs_r))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__wr_addr_w 
            = (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__init_cnt_r));
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__wr_data_w[0U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__wr_data_w[1U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__wr_data_w[2U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__wr_data_w[3U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__wr_data_w[4U] = 0U;
    } else {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__wr_addr_w 
            = (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__rs_k_r));
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__wr_data_w[0U] 
            = (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__rctlr_q_r);
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__wr_data_w[1U] 
            = (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__rctlr_q_r 
                       >> 0x00000020U));
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__wr_data_w[2U] 
            = (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__rtk_q_r);
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__wr_data_w[3U] 
            = (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__rtk_q_r 
                       >> 0x00000020U));
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__wr_data_w[4U] 
            = (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__rstarted_q_r) 
                << 0x00000011U) | (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__rsw_q_r) 
                                    << 0x00000010U) 
                                   | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__ruid_q_r)));
    }
    vlSelfRef.milan_datapath__DOT__media_grid_align__DOT__base_w 
        = ((VL_EXTENDS_II(32,14, (IData)(vlSelfRef.milan_datapath__DOT__media_grid_align__DOT__tst_next_w)) 
            - VL_EXTENDS_II(32,14, (IData)(vlSelfRef.milan_datapath__DOT__media_grid_align__DOT__ref_r))) 
           + VL_MULS_III(32, (IData)(0x00000823U), 
                         VL_EXTENDS_II(32,5, (IData)(vlSelfRef.milan_datapath__DOT__media_grid_align__DOT__slip_r))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxf_req_w 
        = (((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__maap_txn_ready_w) 
              & ((7U != (7U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_maap_q__DOT__out_data_r[1U] 
                               >> 0x00000019U))) & 
                 (4U > (7U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_maap_q__DOT__out_data_r[1U] 
                              >> 0x00000019U))))) << 5U) 
            | ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__aecp_rxs_free_w) 
               << 4U)) | (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_rxs_free_w) 
                           << 2U) | (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__lstn_rxs_free_w) 
                                      << 1U) | ((7U 
                                                 == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__rx_st_r)) 
                                                & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__rx_have_slot_w)))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__acmp_sb_done_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__acmp_sb_active_r) 
           & (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__lstn_rxs_free_w) 
               & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__acmp_sb_slot_r) 
                  == (3U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__rxslot_r)))) 
              | (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__acmp_sb_slot_r) 
                  == (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__txn_r[1U] 
                            >> 0x00000019U))) & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_rxs_free_w))));
    if (vlSelfRef.milan_datapath__DOT__amap_spi_w) {
        vlSelfRef.__VdfgRegularize_h6e95ff9d_0_163 
            = vlSelfRef.milan_datapath__DOT__amap_in_nmaps_w;
        milan_datapath__DOT__amap_page_ok_w = ((IData)(vlSelfRef.milan_datapath__DOT__amapq_map_r) 
                                               < (IData)(vlSelfRef.milan_datapath__DOT__amap_in_nmaps_w));
    } else {
        vlSelfRef.__VdfgRegularize_h6e95ff9d_0_163 
            = (1U & (- (IData)((IData)(vlSelfRef.milan_datapath__DOT__amap_spo_w))));
        milan_datapath__DOT__amap_page_ok_w = 0U;
    }
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
    milan_datapath__DOT__lb_tap_tdata_w = vlSelfRef.milan_datapath__DOT__dpkt_pcm_tdata_w;
    vlSelfRef.s_axi_wready = vlSelfRef.s_axi_awready;
    vlSelfRef.milan_datapath__DOT__csr__DOT__win_alias_ctrl_w 
        = (((0x0810U == (IData)(vlSelfRef.s_axi_awaddr)) 
            & (IData)(vlSelfRef.s_axi_awready)) & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_132));
    vlSelfRef.milan_datapath__DOT__csr__DOT__win_alias_dmlo_w 
        = ((IData)(vlSelfRef.s_axi_awready) & ((0x081cU 
                                                == (IData)(vlSelfRef.s_axi_awaddr)) 
                                               & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_132)));
    vlSelfRef.milan_datapath__DOT__csr__DOT__win_alias_dmhi_w 
        = ((IData)(vlSelfRef.s_axi_awready) & ((0x0820U 
                                                == (IData)(vlSelfRef.s_axi_awaddr)) 
                                               & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_132)));
    vlSelfRef.milan_datapath__DOT__csr__DOT__cmrd_go_w 
        = ((IData)(vlSelfRef.s_axi_awready) & (vlSelfRef.s_axi_wdata 
                                               & ((~ (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__cmrd_busy_r)) 
                                                  & (0x0910U 
                                                     == (IData)(vlSelfRef.s_axi_awaddr)))));
    milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
        = ((IData)(vlSelfRef.s_axi_awready) & (~ (0U 
                                                  != 
                                                  (0x0000001fU 
                                                   & ((IData)(vlSelfRef.s_axi_awaddr) 
                                                      >> 0x0bU)))));
    if (milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw) {
        vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a 
            = vlSelfRef.s_axi_awaddr;
        milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw = 0U;
        if ((0x00008000U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
            if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)) 
                 & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) {
                milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                    = ((((0U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) 
                         | (4U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                        | (8U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                       | (0x0cU == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))));
            }
        } else if ((0x00004000U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
            if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)) 
                 & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) {
                milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                    = ((((0U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) 
                         | (4U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                        | (8U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                       | (0x0cU == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))));
            }
        } else if ((0x00002000U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
            if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)) 
                 & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) {
                milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                    = ((((0U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) 
                         | (4U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                        | (8U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                       | (0x0cU == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))));
            }
        } else if ((0x00001000U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
            if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)) 
                 & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) {
                milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                    = ((((0U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) 
                         | (4U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                        | (8U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                       | (0x0cU == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))));
            }
        } else if ((0x00000800U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
            if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)) 
                 & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) {
                milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                    = ((((0U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) 
                         | (4U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                        | (8U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                       | (0x0cU == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))));
            }
        } else if ((0x00000400U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
            if ((0x00000200U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
                if ((0x00000100U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
                    if ((0x00000080U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
                        if ((0x00000040U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
                            if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)) 
                                 & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) {
                                milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                    = ((((0U == (0x0000001fU 
                                                 & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) 
                                         | (4U == (0x0000001fU 
                                                   & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                        | (8U == (0x0000001fU 
                                                  & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                       | (0x0cU == 
                                          (0x0000001fU 
                                           & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))));
                            }
                        } else if ((0x00000020U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
                            if ((0x00000010U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
                                if ((8U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
                                    if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)) 
                                         & (0x04a0U 
                                            > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) {
                                        milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                            = ((((0U 
                                                  == 
                                                  (0x0000001fU 
                                                   & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) 
                                                 | (4U 
                                                    == 
                                                    (0x0000001fU 
                                                     & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                                | (8U 
                                                   == 
                                                   (0x0000001fU 
                                                    & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                               | (0x0cU 
                                                  == 
                                                  (0x0000001fU 
                                                   & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))));
                                    }
                                } else if ((4U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
                                    if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)) 
                                         & (0x04a0U 
                                            > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) {
                                        milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                            = ((((0U 
                                                  == 
                                                  (0x0000001fU 
                                                   & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) 
                                                 | (4U 
                                                    == 
                                                    (0x0000001fU 
                                                     & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                                | (8U 
                                                   == 
                                                   (0x0000001fU 
                                                    & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                               | (0x0cU 
                                                  == 
                                                  (0x0000001fU 
                                                   & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))));
                                    }
                                } else if ((2U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
                                    if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)) 
                                         & (0x04a0U 
                                            > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) {
                                        milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                            = ((((0U 
                                                  == 
                                                  (0x0000001fU 
                                                   & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) 
                                                 | (4U 
                                                    == 
                                                    (0x0000001fU 
                                                     & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                                | (8U 
                                                   == 
                                                   (0x0000001fU 
                                                    & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                               | (0x0cU 
                                                  == 
                                                  (0x0000001fU 
                                                   & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))));
                                    }
                                } else if ((1U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
                                    if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)) 
                                         & (0x04a0U 
                                            > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) {
                                        milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                            = ((((0U 
                                                  == 
                                                  (0x0000001fU 
                                                   & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) 
                                                 | (4U 
                                                    == 
                                                    (0x0000001fU 
                                                     & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                                | (8U 
                                                   == 
                                                   (0x0000001fU 
                                                    & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                               | (0x0cU 
                                                  == 
                                                  (0x0000001fU 
                                                   & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))));
                                    }
                                } else {
                                    milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw = 1U;
                                }
                            } else if ((2U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
                                if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)) 
                                     & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) {
                                    milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                        = ((((0U == 
                                              (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) 
                                             | (4U 
                                                == 
                                                (0x0000001fU 
                                                 & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                            | (8U == 
                                               (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                           | (0x0cU 
                                              == (0x0000001fU 
                                                  & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))));
                                }
                            } else if ((1U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
                                if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)) 
                                     & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) {
                                    milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                        = ((((0U == 
                                              (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) 
                                             | (4U 
                                                == 
                                                (0x0000001fU 
                                                 & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                            | (8U == 
                                               (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                           | (0x0cU 
                                              == (0x0000001fU 
                                                  & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))));
                                }
                            } else {
                                milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw = 1U;
                            }
                        } else if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)) 
                                    & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) {
                            milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                = ((((0U == (0x0000001fU 
                                             & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) 
                                     | (4U == (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                    | (8U == (0x0000001fU 
                                              & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                   | (0x0cU == (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))));
                        }
                    } else if ((0x00000040U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
                        if ((0x00000020U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
                            if ((0x00000010U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
                                if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)) 
                                     & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) {
                                    milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                        = ((((0U == 
                                              (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) 
                                             | (4U 
                                                == 
                                                (0x0000001fU 
                                                 & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                            | (8U == 
                                               (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                           | (0x0cU 
                                              == (0x0000001fU 
                                                  & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))));
                                }
                            } else if ((8U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
                                if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)) 
                                     & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) {
                                    milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                        = ((((0U == 
                                              (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) 
                                             | (4U 
                                                == 
                                                (0x0000001fU 
                                                 & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                            | (8U == 
                                               (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                           | (0x0cU 
                                              == (0x0000001fU 
                                                  & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))));
                                }
                            } else if ((4U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
                                if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)) 
                                     & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) {
                                    milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                        = ((((0U == 
                                              (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) 
                                             | (4U 
                                                == 
                                                (0x0000001fU 
                                                 & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                            | (8U == 
                                               (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                           | (0x0cU 
                                              == (0x0000001fU 
                                                  & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))));
                                }
                            } else if ((2U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
                                if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)) 
                                     & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) {
                                    milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                        = ((((0U == 
                                              (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) 
                                             | (4U 
                                                == 
                                                (0x0000001fU 
                                                 & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                            | (8U == 
                                               (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                           | (0x0cU 
                                              == (0x0000001fU 
                                                  & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))));
                                }
                            } else if ((1U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
                                if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)) 
                                     & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) {
                                    milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                        = ((((0U == 
                                              (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) 
                                             | (4U 
                                                == 
                                                (0x0000001fU 
                                                 & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                            | (8U == 
                                               (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                           | (0x0cU 
                                              == (0x0000001fU 
                                                  & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))));
                                }
                            } else {
                                milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw = 1U;
                            }
                        } else if ((0x00000010U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
                            if ((8U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
                                if ((2U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
                                    if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)) 
                                         & (0x04a0U 
                                            > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) {
                                        milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                            = ((((0U 
                                                  == 
                                                  (0x0000001fU 
                                                   & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) 
                                                 | (4U 
                                                    == 
                                                    (0x0000001fU 
                                                     & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                                | (8U 
                                                   == 
                                                   (0x0000001fU 
                                                    & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                               | (0x0cU 
                                                  == 
                                                  (0x0000001fU 
                                                   & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))));
                                    }
                                } else if ((1U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
                                    if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)) 
                                         & (0x04a0U 
                                            > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) {
                                        milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                            = ((((0U 
                                                  == 
                                                  (0x0000001fU 
                                                   & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) 
                                                 | (4U 
                                                    == 
                                                    (0x0000001fU 
                                                     & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                                | (8U 
                                                   == 
                                                   (0x0000001fU 
                                                    & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                               | (0x0cU 
                                                  == 
                                                  (0x0000001fU 
                                                   & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))));
                                    }
                                } else {
                                    milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw = 1U;
                                }
                            } else if ((4U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
                                if ((2U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
                                    if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)) 
                                         & (0x04a0U 
                                            > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) {
                                        milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                            = ((((0U 
                                                  == 
                                                  (0x0000001fU 
                                                   & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) 
                                                 | (4U 
                                                    == 
                                                    (0x0000001fU 
                                                     & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                                | (8U 
                                                   == 
                                                   (0x0000001fU 
                                                    & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                               | (0x0cU 
                                                  == 
                                                  (0x0000001fU 
                                                   & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))));
                                    }
                                } else if ((1U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
                                    if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)) 
                                         & (0x04a0U 
                                            > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) {
                                        milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                            = ((((0U 
                                                  == 
                                                  (0x0000001fU 
                                                   & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) 
                                                 | (4U 
                                                    == 
                                                    (0x0000001fU 
                                                     & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                                | (8U 
                                                   == 
                                                   (0x0000001fU 
                                                    & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                               | (0x0cU 
                                                  == 
                                                  (0x0000001fU 
                                                   & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))));
                                    }
                                } else {
                                    milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw = 1U;
                                }
                            } else if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)) 
                                        & (0x04a0U 
                                           > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) {
                                milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                    = ((((0U == (0x0000001fU 
                                                 & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) 
                                         | (4U == (0x0000001fU 
                                                   & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                        | (8U == (0x0000001fU 
                                                  & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                       | (0x0cU == 
                                          (0x0000001fU 
                                           & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))));
                            }
                        } else if ((8U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
                            if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)) 
                                 & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) {
                                milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                    = ((((0U == (0x0000001fU 
                                                 & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) 
                                         | (4U == (0x0000001fU 
                                                   & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                        | (8U == (0x0000001fU 
                                                  & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                       | (0x0cU == 
                                          (0x0000001fU 
                                           & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))));
                            }
                        } else if ((4U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
                            if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)) 
                                 & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) {
                                milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                    = ((((0U == (0x0000001fU 
                                                 & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) 
                                         | (4U == (0x0000001fU 
                                                   & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                        | (8U == (0x0000001fU 
                                                  & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                       | (0x0cU == 
                                          (0x0000001fU 
                                           & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))));
                            }
                        } else if ((2U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
                            if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)) 
                                 & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) {
                                milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                    = ((((0U == (0x0000001fU 
                                                 & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) 
                                         | (4U == (0x0000001fU 
                                                   & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                        | (8U == (0x0000001fU 
                                                  & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                       | (0x0cU == 
                                          (0x0000001fU 
                                           & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))));
                            }
                        } else if ((1U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
                            if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)) 
                                 & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) {
                                milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                    = ((((0U == (0x0000001fU 
                                                 & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) 
                                         | (4U == (0x0000001fU 
                                                   & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                        | (8U == (0x0000001fU 
                                                  & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                       | (0x0cU == 
                                          (0x0000001fU 
                                           & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))));
                            }
                        } else {
                            milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw = 1U;
                        }
                    } else if ((0x00000020U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
                        if ((0x00000010U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
                            if ((8U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
                                if ((4U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
                                    if ((2U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
                                        if (((0x0400U 
                                              <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)) 
                                             & (0x04a0U 
                                                > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) {
                                            milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                                = (
                                                   (((0U 
                                                      == 
                                                      (0x0000001fU 
                                                       & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) 
                                                     | (4U 
                                                        == 
                                                        (0x0000001fU 
                                                         & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                                    | (8U 
                                                       == 
                                                       (0x0000001fU 
                                                        & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                                   | (0x0cU 
                                                      == 
                                                      (0x0000001fU 
                                                       & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))));
                                        }
                                    } else if ((1U 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
                                        if (((0x0400U 
                                              <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)) 
                                             & (0x04a0U 
                                                > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) {
                                            milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                                = (
                                                   (((0U 
                                                      == 
                                                      (0x0000001fU 
                                                       & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) 
                                                     | (4U 
                                                        == 
                                                        (0x0000001fU 
                                                         & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                                    | (8U 
                                                       == 
                                                       (0x0000001fU 
                                                        & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                                   | (0x0cU 
                                                      == 
                                                      (0x0000001fU 
                                                       & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))));
                                        }
                                    } else {
                                        milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw = 1U;
                                    }
                                } else if (((0x0400U 
                                             <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)) 
                                            & (0x04a0U 
                                               > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) {
                                    milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                        = ((((0U == 
                                              (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) 
                                             | (4U 
                                                == 
                                                (0x0000001fU 
                                                 & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                            | (8U == 
                                               (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                           | (0x0cU 
                                              == (0x0000001fU 
                                                  & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))));
                                }
                            } else if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)) 
                                        & (0x04a0U 
                                           > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) {
                                milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                    = ((((0U == (0x0000001fU 
                                                 & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) 
                                         | (4U == (0x0000001fU 
                                                   & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                        | (8U == (0x0000001fU 
                                                  & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                       | (0x0cU == 
                                          (0x0000001fU 
                                           & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))));
                            }
                        } else if ((8U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
                            if ((2U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
                                if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)) 
                                     & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) {
                                    milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                        = ((((0U == 
                                              (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) 
                                             | (4U 
                                                == 
                                                (0x0000001fU 
                                                 & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                            | (8U == 
                                               (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                           | (0x0cU 
                                              == (0x0000001fU 
                                                  & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))));
                                }
                            } else if ((1U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
                                if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)) 
                                     & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) {
                                    milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                        = ((((0U == 
                                              (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) 
                                             | (4U 
                                                == 
                                                (0x0000001fU 
                                                 & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                            | (8U == 
                                               (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                           | (0x0cU 
                                              == (0x0000001fU 
                                                  & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))));
                                }
                            } else {
                                milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw = 1U;
                            }
                        } else if ((4U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
                            if ((2U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
                                if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)) 
                                     & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) {
                                    milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                        = ((((0U == 
                                              (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) 
                                             | (4U 
                                                == 
                                                (0x0000001fU 
                                                 & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                            | (8U == 
                                               (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                           | (0x0cU 
                                              == (0x0000001fU 
                                                  & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))));
                                }
                            } else if ((1U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
                                if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)) 
                                     & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) {
                                    milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                        = ((((0U == 
                                              (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) 
                                             | (4U 
                                                == 
                                                (0x0000001fU 
                                                 & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                            | (8U == 
                                               (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                           | (0x0cU 
                                              == (0x0000001fU 
                                                  & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))));
                                }
                            } else {
                                milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw = 1U;
                            }
                        } else if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)) 
                                    & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) {
                            milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                = ((((0U == (0x0000001fU 
                                             & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) 
                                     | (4U == (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                    | (8U == (0x0000001fU 
                                              & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                   | (0x0cU == (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))));
                        }
                    } else if ((0x00000010U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
                        if ((8U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
                            if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)) 
                                 & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) {
                                milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                    = ((((0U == (0x0000001fU 
                                                 & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) 
                                         | (4U == (0x0000001fU 
                                                   & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                        | (8U == (0x0000001fU 
                                                  & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                       | (0x0cU == 
                                          (0x0000001fU 
                                           & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))));
                            }
                        } else if ((2U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
                            if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)) 
                                 & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) {
                                milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                    = ((((0U == (0x0000001fU 
                                                 & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) 
                                         | (4U == (0x0000001fU 
                                                   & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                        | (8U == (0x0000001fU 
                                                  & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                       | (0x0cU == 
                                          (0x0000001fU 
                                           & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))));
                            }
                        } else if ((1U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
                            if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)) 
                                 & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) {
                                milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                    = ((((0U == (0x0000001fU 
                                                 & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) 
                                         | (4U == (0x0000001fU 
                                                   & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                        | (8U == (0x0000001fU 
                                                  & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                       | (0x0cU == 
                                          (0x0000001fU 
                                           & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))));
                            }
                        } else {
                            milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw = 1U;
                        }
                    } else if ((2U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
                        if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)) 
                             & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) {
                            milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                = ((((0U == (0x0000001fU 
                                             & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) 
                                     | (4U == (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                    | (8U == (0x0000001fU 
                                              & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                   | (0x0cU == (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))));
                        }
                    } else if ((1U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
                        if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)) 
                             & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) {
                            milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                = ((((0U == (0x0000001fU 
                                             & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) 
                                     | (4U == (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                    | (8U == (0x0000001fU 
                                              & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                   | (0x0cU == (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))));
                        }
                    } else {
                        milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw = 1U;
                    }
                } else if ((0x00000080U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
                    if ((0x00000040U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
                        if ((0x00000020U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
                            if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)) 
                                 & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) {
                                milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                    = ((((0U == (0x0000001fU 
                                                 & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) 
                                         | (4U == (0x0000001fU 
                                                   & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                        | (8U == (0x0000001fU 
                                                  & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                       | (0x0cU == 
                                          (0x0000001fU 
                                           & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))));
                            }
                        } else if ((8U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
                            if ((4U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
                                if ((2U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
                                    if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)) 
                                         & (0x04a0U 
                                            > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) {
                                        milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                            = ((((0U 
                                                  == 
                                                  (0x0000001fU 
                                                   & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) 
                                                 | (4U 
                                                    == 
                                                    (0x0000001fU 
                                                     & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                                | (8U 
                                                   == 
                                                   (0x0000001fU 
                                                    & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                               | (0x0cU 
                                                  == 
                                                  (0x0000001fU 
                                                   & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))));
                                    }
                                } else if ((1U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
                                    if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)) 
                                         & (0x04a0U 
                                            > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) {
                                        milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                            = ((((0U 
                                                  == 
                                                  (0x0000001fU 
                                                   & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) 
                                                 | (4U 
                                                    == 
                                                    (0x0000001fU 
                                                     & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                                | (8U 
                                                   == 
                                                   (0x0000001fU 
                                                    & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                               | (0x0cU 
                                                  == 
                                                  (0x0000001fU 
                                                   & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))));
                                    }
                                } else {
                                    milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw = 1U;
                                }
                            } else if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)) 
                                        & (0x04a0U 
                                           > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) {
                                milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                    = ((((0U == (0x0000001fU 
                                                 & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) 
                                         | (4U == (0x0000001fU 
                                                   & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                        | (8U == (0x0000001fU 
                                                  & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                       | (0x0cU == 
                                          (0x0000001fU 
                                           & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))));
                            }
                        } else if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)) 
                                    & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) {
                            milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                = ((((0U == (0x0000001fU 
                                             & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) 
                                     | (4U == (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                    | (8U == (0x0000001fU 
                                              & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                   | (0x0cU == (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))));
                        }
                    } else if ((0x00000020U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
                        if ((0x00000010U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
                            if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)) 
                                 & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) {
                                milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                    = ((((0U == (0x0000001fU 
                                                 & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) 
                                         | (4U == (0x0000001fU 
                                                   & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                        | (8U == (0x0000001fU 
                                                  & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                       | (0x0cU == 
                                          (0x0000001fU 
                                           & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))));
                            }
                        } else if ((8U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
                            if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)) 
                                 & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) {
                                milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                    = ((((0U == (0x0000001fU 
                                                 & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) 
                                         | (4U == (0x0000001fU 
                                                   & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                        | (8U == (0x0000001fU 
                                                  & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                       | (0x0cU == 
                                          (0x0000001fU 
                                           & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))));
                            }
                        } else if ((4U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
                            if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)) 
                                 & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) {
                                milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                    = ((((0U == (0x0000001fU 
                                                 & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) 
                                         | (4U == (0x0000001fU 
                                                   & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                        | (8U == (0x0000001fU 
                                                  & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                       | (0x0cU == 
                                          (0x0000001fU 
                                           & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))));
                            }
                        } else if ((2U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
                            if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)) 
                                 & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) {
                                milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                    = ((((0U == (0x0000001fU 
                                                 & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) 
                                         | (4U == (0x0000001fU 
                                                   & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                        | (8U == (0x0000001fU 
                                                  & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                       | (0x0cU == 
                                          (0x0000001fU 
                                           & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))));
                            }
                        } else if ((1U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
                            if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)) 
                                 & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) {
                                milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                    = ((((0U == (0x0000001fU 
                                                 & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) 
                                         | (4U == (0x0000001fU 
                                                   & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                        | (8U == (0x0000001fU 
                                                  & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                       | (0x0cU == 
                                          (0x0000001fU 
                                           & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))));
                            }
                        } else {
                            milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw = 1U;
                        }
                    } else if ((0x00000010U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
                        if ((8U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
                            if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)) 
                                 & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) {
                                milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                    = ((((0U == (0x0000001fU 
                                                 & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) 
                                         | (4U == (0x0000001fU 
                                                   & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                        | (8U == (0x0000001fU 
                                                  & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                       | (0x0cU == 
                                          (0x0000001fU 
                                           & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))));
                            }
                        } else if ((4U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
                            if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)) 
                                 & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) {
                                milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                    = ((((0U == (0x0000001fU 
                                                 & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) 
                                         | (4U == (0x0000001fU 
                                                   & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                        | (8U == (0x0000001fU 
                                                  & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                       | (0x0cU == 
                                          (0x0000001fU 
                                           & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))));
                            }
                        } else if ((2U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
                            if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)) 
                                 & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) {
                                milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                    = ((((0U == (0x0000001fU 
                                                 & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) 
                                         | (4U == (0x0000001fU 
                                                   & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                        | (8U == (0x0000001fU 
                                                  & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                       | (0x0cU == 
                                          (0x0000001fU 
                                           & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))));
                            }
                        } else if ((1U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
                            if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)) 
                                 & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) {
                                milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                    = ((((0U == (0x0000001fU 
                                                 & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) 
                                         | (4U == (0x0000001fU 
                                                   & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                        | (8U == (0x0000001fU 
                                                  & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                       | (0x0cU == 
                                          (0x0000001fU 
                                           & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))));
                            }
                        } else {
                            milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw = 1U;
                        }
                    } else if ((2U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
                        if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)) 
                             & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) {
                            milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                = ((((0U == (0x0000001fU 
                                             & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) 
                                     | (4U == (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                    | (8U == (0x0000001fU 
                                              & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                   | (0x0cU == (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))));
                        }
                    } else if ((1U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
                        if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)) 
                             & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) {
                            milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                = ((((0U == (0x0000001fU 
                                             & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) 
                                     | (4U == (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                    | (8U == (0x0000001fU 
                                              & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                   | (0x0cU == (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))));
                        }
                    } else {
                        milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw = 1U;
                    }
                } else if ((0x00000040U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
                    if ((0x00000020U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
                        if ((0x00000010U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
                            if ((8U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
                                if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)) 
                                     & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) {
                                    milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                        = ((((0U == 
                                              (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) 
                                             | (4U 
                                                == 
                                                (0x0000001fU 
                                                 & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                            | (8U == 
                                               (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                           | (0x0cU 
                                              == (0x0000001fU 
                                                  & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))));
                                }
                            } else if ((4U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
                                if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)) 
                                     & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) {
                                    milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                        = ((((0U == 
                                              (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) 
                                             | (4U 
                                                == 
                                                (0x0000001fU 
                                                 & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                            | (8U == 
                                               (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                           | (0x0cU 
                                              == (0x0000001fU 
                                                  & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))));
                                }
                            } else if ((2U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
                                if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)) 
                                     & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) {
                                    milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                        = ((((0U == 
                                              (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) 
                                             | (4U 
                                                == 
                                                (0x0000001fU 
                                                 & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                            | (8U == 
                                               (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                           | (0x0cU 
                                              == (0x0000001fU 
                                                  & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))));
                                }
                            } else if ((1U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
                                if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)) 
                                     & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) {
                                    milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                        = ((((0U == 
                                              (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) 
                                             | (4U 
                                                == 
                                                (0x0000001fU 
                                                 & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                            | (8U == 
                                               (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                           | (0x0cU 
                                              == (0x0000001fU 
                                                  & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))));
                                }
                            } else {
                                milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw = 1U;
                            }
                        } else if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)) 
                                    & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) {
                            milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                = ((((0U == (0x0000001fU 
                                             & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) 
                                     | (4U == (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                    | (8U == (0x0000001fU 
                                              & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                   | (0x0cU == (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))));
                        }
                    } else if ((0x00000010U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
                        if ((8U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
                            if ((2U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
                                if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)) 
                                     & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) {
                                    milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                        = ((((0U == 
                                              (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) 
                                             | (4U 
                                                == 
                                                (0x0000001fU 
                                                 & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                            | (8U == 
                                               (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                           | (0x0cU 
                                              == (0x0000001fU 
                                                  & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))));
                                }
                            } else if ((1U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
                                if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)) 
                                     & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) {
                                    milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                        = ((((0U == 
                                              (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) 
                                             | (4U 
                                                == 
                                                (0x0000001fU 
                                                 & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                            | (8U == 
                                               (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                           | (0x0cU 
                                              == (0x0000001fU 
                                                  & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))));
                                }
                            } else {
                                milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw = 1U;
                            }
                        } else if ((4U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
                            if ((2U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
                                if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)) 
                                     & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) {
                                    milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                        = ((((0U == 
                                              (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) 
                                             | (4U 
                                                == 
                                                (0x0000001fU 
                                                 & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                            | (8U == 
                                               (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                           | (0x0cU 
                                              == (0x0000001fU 
                                                  & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))));
                                }
                            } else if ((1U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
                                if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)) 
                                     & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) {
                                    milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                        = ((((0U == 
                                              (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) 
                                             | (4U 
                                                == 
                                                (0x0000001fU 
                                                 & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                            | (8U == 
                                               (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                           | (0x0cU 
                                              == (0x0000001fU 
                                                  & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))));
                                }
                            } else {
                                milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw = 1U;
                            }
                        } else if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)) 
                                    & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) {
                            milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                = ((((0U == (0x0000001fU 
                                             & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) 
                                     | (4U == (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                    | (8U == (0x0000001fU 
                                              & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                   | (0x0cU == (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))));
                        }
                    } else if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)) 
                                & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) {
                        milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                            = ((((0U == (0x0000001fU 
                                         & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) 
                                 | (4U == (0x0000001fU 
                                           & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                | (8U == (0x0000001fU 
                                          & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                               | (0x0cU == (0x0000001fU 
                                            & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))));
                    }
                } else if ((0x00000020U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
                    if ((0x00000010U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
                        if ((2U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
                            if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)) 
                                 & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) {
                                milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                    = ((((0U == (0x0000001fU 
                                                 & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) 
                                         | (4U == (0x0000001fU 
                                                   & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                        | (8U == (0x0000001fU 
                                                  & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                       | (0x0cU == 
                                          (0x0000001fU 
                                           & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))));
                            }
                        } else if ((1U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
                            if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)) 
                                 & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) {
                                milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                    = ((((0U == (0x0000001fU 
                                                 & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) 
                                         | (4U == (0x0000001fU 
                                                   & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                        | (8U == (0x0000001fU 
                                                  & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                       | (0x0cU == 
                                          (0x0000001fU 
                                           & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))));
                            }
                        } else {
                            milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw = 1U;
                        }
                    } else if ((8U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
                        if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)) 
                             & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) {
                            milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                = ((((0U == (0x0000001fU 
                                             & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) 
                                     | (4U == (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                    | (8U == (0x0000001fU 
                                              & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                   | (0x0cU == (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))));
                        }
                    } else if ((4U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
                        if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)) 
                             & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) {
                            milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                = ((((0U == (0x0000001fU 
                                             & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) 
                                     | (4U == (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                    | (8U == (0x0000001fU 
                                              & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                   | (0x0cU == (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))));
                        }
                    } else if ((2U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
                        if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)) 
                             & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) {
                            milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                = ((((0U == (0x0000001fU 
                                             & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) 
                                     | (4U == (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                    | (8U == (0x0000001fU 
                                              & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                   | (0x0cU == (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))));
                        }
                    } else if ((1U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
                        if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)) 
                             & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) {
                            milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                = ((((0U == (0x0000001fU 
                                             & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) 
                                     | (4U == (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                    | (8U == (0x0000001fU 
                                              & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                   | (0x0cU == (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))));
                        }
                    } else {
                        milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw = 1U;
                    }
                } else if ((0x00000010U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
                    if ((8U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
                        if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)) 
                             & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) {
                            milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                = ((((0U == (0x0000001fU 
                                             & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) 
                                     | (4U == (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                    | (8U == (0x0000001fU 
                                              & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                   | (0x0cU == (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))));
                        }
                    } else if ((2U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
                        if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)) 
                             & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) {
                            milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                = ((((0U == (0x0000001fU 
                                             & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) 
                                     | (4U == (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                    | (8U == (0x0000001fU 
                                              & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                   | (0x0cU == (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))));
                        }
                    } else if ((1U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
                        if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)) 
                             & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) {
                            milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                = ((((0U == (0x0000001fU 
                                             & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) 
                                     | (4U == (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                    | (8U == (0x0000001fU 
                                              & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                   | (0x0cU == (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))));
                        }
                    } else {
                        milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw = 1U;
                    }
                } else if ((2U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
                    if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)) 
                         & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) {
                        milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                            = ((((0U == (0x0000001fU 
                                         & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) 
                                 | (4U == (0x0000001fU 
                                           & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                | (8U == (0x0000001fU 
                                          & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                               | (0x0cU == (0x0000001fU 
                                            & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))));
                    }
                } else if ((1U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
                    if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)) 
                         & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) {
                        milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                            = ((((0U == (0x0000001fU 
                                         & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) 
                                 | (4U == (0x0000001fU 
                                           & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                | (8U == (0x0000001fU 
                                          & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                               | (0x0cU == (0x0000001fU 
                                            & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))));
                    }
                } else {
                    milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw = 1U;
                }
            } else if ((0x00000100U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
                if ((0x00000080U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
                    if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)) 
                         & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) {
                        milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                            = ((((0U == (0x0000001fU 
                                         & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) 
                                 | (4U == (0x0000001fU 
                                           & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                | (8U == (0x0000001fU 
                                          & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                               | (0x0cU == (0x0000001fU 
                                            & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))));
                    }
                } else if ((0x00000040U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
                    if ((0x00000020U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
                        if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)) 
                             & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) {
                            milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                = ((((0U == (0x0000001fU 
                                             & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) 
                                     | (4U == (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                    | (8U == (0x0000001fU 
                                              & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                   | (0x0cU == (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))));
                        }
                    } else if ((0x00000010U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
                        if ((8U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
                            if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)) 
                                 & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) {
                                milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                    = ((((0U == (0x0000001fU 
                                                 & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) 
                                         | (4U == (0x0000001fU 
                                                   & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                        | (8U == (0x0000001fU 
                                                  & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                       | (0x0cU == 
                                          (0x0000001fU 
                                           & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))));
                            }
                        } else if ((4U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
                            if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)) 
                                 & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) {
                                milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                    = ((((0U == (0x0000001fU 
                                                 & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) 
                                         | (4U == (0x0000001fU 
                                                   & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                        | (8U == (0x0000001fU 
                                                  & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                       | (0x0cU == 
                                          (0x0000001fU 
                                           & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))));
                            }
                        } else if ((2U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
                            if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)) 
                                 & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) {
                                milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                    = ((((0U == (0x0000001fU 
                                                 & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) 
                                         | (4U == (0x0000001fU 
                                                   & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                        | (8U == (0x0000001fU 
                                                  & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                       | (0x0cU == 
                                          (0x0000001fU 
                                           & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))));
                            }
                        } else if ((1U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
                            if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)) 
                                 & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) {
                                milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                    = ((((0U == (0x0000001fU 
                                                 & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) 
                                         | (4U == (0x0000001fU 
                                                   & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                        | (8U == (0x0000001fU 
                                                  & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                       | (0x0cU == 
                                          (0x0000001fU 
                                           & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))));
                            }
                        } else {
                            milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw = 1U;
                        }
                    } else if ((8U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
                        if ((4U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
                            if ((2U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
                                if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)) 
                                     & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) {
                                    milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                        = ((((0U == 
                                              (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) 
                                             | (4U 
                                                == 
                                                (0x0000001fU 
                                                 & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                            | (8U == 
                                               (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                           | (0x0cU 
                                              == (0x0000001fU 
                                                  & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))));
                                }
                            } else if ((1U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
                                if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)) 
                                     & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) {
                                    milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                        = ((((0U == 
                                              (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) 
                                             | (4U 
                                                == 
                                                (0x0000001fU 
                                                 & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                            | (8U == 
                                               (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                           | (0x0cU 
                                              == (0x0000001fU 
                                                  & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))));
                                }
                            } else {
                                milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw = 1U;
                            }
                        } else if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)) 
                                    & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) {
                            milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                = ((((0U == (0x0000001fU 
                                             & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) 
                                     | (4U == (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                    | (8U == (0x0000001fU 
                                              & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                   | (0x0cU == (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))));
                        }
                    } else if ((2U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
                        if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)) 
                             & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) {
                            milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                = ((((0U == (0x0000001fU 
                                             & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) 
                                     | (4U == (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                    | (8U == (0x0000001fU 
                                              & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                   | (0x0cU == (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))));
                        }
                    } else if ((1U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
                        if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)) 
                             & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) {
                            milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                = ((((0U == (0x0000001fU 
                                             & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) 
                                     | (4U == (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                    | (8U == (0x0000001fU 
                                              & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                   | (0x0cU == (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))));
                        }
                    } else {
                        milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw = 1U;
                    }
                } else if ((0x00000020U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
                    if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)) 
                         & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) {
                        milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                            = ((((0U == (0x0000001fU 
                                         & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) 
                                 | (4U == (0x0000001fU 
                                           & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                | (8U == (0x0000001fU 
                                          & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                               | (0x0cU == (0x0000001fU 
                                            & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))));
                    }
                } else if ((0x00000010U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
                    if ((2U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
                        if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)) 
                             & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) {
                            milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                = ((((0U == (0x0000001fU 
                                             & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) 
                                     | (4U == (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                    | (8U == (0x0000001fU 
                                              & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                   | (0x0cU == (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))));
                        }
                    } else if ((1U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
                        if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)) 
                             & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) {
                            milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                = ((((0U == (0x0000001fU 
                                             & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) 
                                     | (4U == (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                    | (8U == (0x0000001fU 
                                              & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                   | (0x0cU == (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))));
                        }
                    } else {
                        milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw = 1U;
                    }
                } else if ((8U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
                    if ((4U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
                        if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)) 
                             & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) {
                            milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                = ((((0U == (0x0000001fU 
                                             & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) 
                                     | (4U == (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                    | (8U == (0x0000001fU 
                                              & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                   | (0x0cU == (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))));
                        }
                    } else if ((2U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
                        if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)) 
                             & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) {
                            milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                = ((((0U == (0x0000001fU 
                                             & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) 
                                     | (4U == (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                    | (8U == (0x0000001fU 
                                              & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                   | (0x0cU == (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))));
                        }
                    } else if ((1U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
                        if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)) 
                             & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) {
                            milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                = ((((0U == (0x0000001fU 
                                             & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) 
                                     | (4U == (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                    | (8U == (0x0000001fU 
                                              & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                   | (0x0cU == (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))));
                        }
                    } else {
                        milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw = 1U;
                    }
                } else if ((2U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
                    if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)) 
                         & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) {
                        milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                            = ((((0U == (0x0000001fU 
                                         & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) 
                                 | (4U == (0x0000001fU 
                                           & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                | (8U == (0x0000001fU 
                                          & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                               | (0x0cU == (0x0000001fU 
                                            & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))));
                    }
                } else if ((1U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
                    if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)) 
                         & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) {
                        milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                            = ((((0U == (0x0000001fU 
                                         & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) 
                                 | (4U == (0x0000001fU 
                                           & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                | (8U == (0x0000001fU 
                                          & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                               | (0x0cU == (0x0000001fU 
                                            & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))));
                    }
                } else {
                    milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw = 1U;
                }
            } else if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)) 
                        & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) {
                milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                    = ((((0U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) 
                         | (4U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                        | (8U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                       | (0x0cU == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))));
            }
        } else if ((0x00000200U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
            if ((0x00000100U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
                if ((0x00000080U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
                    if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)) 
                         & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) {
                        milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                            = ((((0U == (0x0000001fU 
                                         & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) 
                                 | (4U == (0x0000001fU 
                                           & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                | (8U == (0x0000001fU 
                                          & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                               | (0x0cU == (0x0000001fU 
                                            & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))));
                    }
                } else if ((0x00000040U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
                    if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)) 
                         & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) {
                        milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                            = ((((0U == (0x0000001fU 
                                         & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) 
                                 | (4U == (0x0000001fU 
                                           & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                | (8U == (0x0000001fU 
                                          & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                               | (0x0cU == (0x0000001fU 
                                            & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))));
                    }
                } else if ((0x00000020U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
                    if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)) 
                         & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) {
                        milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                            = ((((0U == (0x0000001fU 
                                         & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) 
                                 | (4U == (0x0000001fU 
                                           & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                | (8U == (0x0000001fU 
                                          & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                               | (0x0cU == (0x0000001fU 
                                            & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))));
                    }
                } else if ((0x00000010U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
                    if ((8U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
                        if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)) 
                             & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) {
                            milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                = ((((0U == (0x0000001fU 
                                             & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) 
                                     | (4U == (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                    | (8U == (0x0000001fU 
                                              & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                   | (0x0cU == (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))));
                        }
                    } else if ((4U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
                        if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)) 
                             & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) {
                            milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                = ((((0U == (0x0000001fU 
                                             & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) 
                                     | (4U == (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                    | (8U == (0x0000001fU 
                                              & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                   | (0x0cU == (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))));
                        }
                    } else if ((2U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
                        if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)) 
                             & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) {
                            milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                = ((((0U == (0x0000001fU 
                                             & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) 
                                     | (4U == (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                    | (8U == (0x0000001fU 
                                              & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                   | (0x0cU == (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))));
                        }
                    } else if ((1U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
                        if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)) 
                             & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) {
                            milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                = ((((0U == (0x0000001fU 
                                             & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) 
                                     | (4U == (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                    | (8U == (0x0000001fU 
                                              & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                   | (0x0cU == (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))));
                        }
                    } else {
                        milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw = 1U;
                    }
                } else if ((2U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
                    if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)) 
                         & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) {
                        milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                            = ((((0U == (0x0000001fU 
                                         & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) 
                                 | (4U == (0x0000001fU 
                                           & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                | (8U == (0x0000001fU 
                                          & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                               | (0x0cU == (0x0000001fU 
                                            & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))));
                    }
                } else if ((1U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
                    if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)) 
                         & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) {
                        milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                            = ((((0U == (0x0000001fU 
                                         & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) 
                                 | (4U == (0x0000001fU 
                                           & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                | (8U == (0x0000001fU 
                                          & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                               | (0x0cU == (0x0000001fU 
                                            & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))));
                    }
                } else {
                    milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw = 1U;
                }
            } else if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)) 
                        & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) {
                milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                    = ((((0U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) 
                         | (4U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                        | (8U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                       | (0x0cU == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))));
            }
        } else if ((0x00000100U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
            if ((0x00000080U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
                if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)) 
                     & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) {
                    milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                        = ((((0U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) 
                             | (4U == (0x0000001fU 
                                       & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                            | (8U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                           | (0x0cU == (0x0000001fU 
                                        & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))));
                }
            } else if ((0x00000040U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
                if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)) 
                     & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) {
                    milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                        = ((((0U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) 
                             | (4U == (0x0000001fU 
                                       & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                            | (8U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                           | (0x0cU == (0x0000001fU 
                                        & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))));
                }
            } else if ((0x00000020U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
                if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)) 
                     & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) {
                    milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                        = ((((0U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) 
                             | (4U == (0x0000001fU 
                                       & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                            | (8U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                           | (0x0cU == (0x0000001fU 
                                        & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))));
                }
            } else if ((0x00000010U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
                if ((8U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
                    if ((4U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
                        if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)) 
                             & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) {
                            milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                = ((((0U == (0x0000001fU 
                                             & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) 
                                     | (4U == (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                    | (8U == (0x0000001fU 
                                              & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                   | (0x0cU == (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))));
                        }
                    } else if ((2U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
                        if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)) 
                             & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) {
                            milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                = ((((0U == (0x0000001fU 
                                             & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) 
                                     | (4U == (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                    | (8U == (0x0000001fU 
                                              & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                   | (0x0cU == (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))));
                        }
                    } else if ((1U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
                        if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)) 
                             & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) {
                            milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                = ((((0U == (0x0000001fU 
                                             & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) 
                                     | (4U == (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                    | (8U == (0x0000001fU 
                                              & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                   | (0x0cU == (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))));
                        }
                    } else {
                        milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw = 1U;
                    }
                } else if ((4U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
                    if ((2U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
                        if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)) 
                             & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) {
                            milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                = ((((0U == (0x0000001fU 
                                             & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) 
                                     | (4U == (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                    | (8U == (0x0000001fU 
                                              & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                   | (0x0cU == (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))));
                        }
                    } else if ((1U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
                        if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)) 
                             & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) {
                            milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                = ((((0U == (0x0000001fU 
                                             & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) 
                                     | (4U == (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                    | (8U == (0x0000001fU 
                                              & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                   | (0x0cU == (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))));
                        }
                    } else {
                        milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw = 1U;
                    }
                } else if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)) 
                            & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) {
                    milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                        = ((((0U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) 
                             | (4U == (0x0000001fU 
                                       & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                            | (8U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                           | (0x0cU == (0x0000001fU 
                                        & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))));
                }
            } else if ((2U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
                if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)) 
                     & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) {
                    milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                        = ((((0U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) 
                             | (4U == (0x0000001fU 
                                       & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                            | (8U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                           | (0x0cU == (0x0000001fU 
                                        & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))));
                }
            } else if ((1U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
                if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)) 
                     & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) {
                    milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                        = ((((0U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) 
                             | (4U == (0x0000001fU 
                                       & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                            | (8U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                           | (0x0cU == (0x0000001fU 
                                        & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))));
                }
            } else {
                milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw = 1U;
            }
        } else if ((0x00000080U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
            if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)) 
                 & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) {
                milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                    = ((((0U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) 
                         | (4U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                        | (8U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                       | (0x0cU == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))));
            }
        } else if ((0x00000040U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
            if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)) 
                 & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) {
                milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                    = ((((0U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) 
                         | (4U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                        | (8U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                       | (0x0cU == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))));
            }
        } else if ((0x00000020U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
            if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)) 
                 & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) {
                milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                    = ((((0U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) 
                         | (4U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                        | (8U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                       | (0x0cU == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))));
            }
        } else if ((0x00000010U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
            if ((8U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
                if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)) 
                     & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) {
                    milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                        = ((((0U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) 
                             | (4U == (0x0000001fU 
                                       & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                            | (8U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                           | (0x0cU == (0x0000001fU 
                                        & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))));
                }
            } else if ((4U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
                if ((2U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
                    if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)) 
                         & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) {
                        milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                            = ((((0U == (0x0000001fU 
                                         & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) 
                                 | (4U == (0x0000001fU 
                                           & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                | (8U == (0x0000001fU 
                                          & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                               | (0x0cU == (0x0000001fU 
                                            & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))));
                    }
                } else if ((1U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
                    if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)) 
                         & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) {
                        milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                            = ((((0U == (0x0000001fU 
                                         & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) 
                                 | (4U == (0x0000001fU 
                                           & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                | (8U == (0x0000001fU 
                                          & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                               | (0x0cU == (0x0000001fU 
                                            & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))));
                    }
                } else {
                    milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw = 1U;
                }
            } else if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)) 
                        & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) {
                milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                    = ((((0U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) 
                         | (4U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                        | (8U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                       | (0x0cU == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))));
            }
        } else if ((8U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
            if ((4U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
                if ((2U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
                    if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)) 
                         & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) {
                        milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                            = ((((0U == (0x0000001fU 
                                         & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) 
                                 | (4U == (0x0000001fU 
                                           & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                | (8U == (0x0000001fU 
                                          & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                               | (0x0cU == (0x0000001fU 
                                            & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))));
                    }
                } else if ((1U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) {
                    if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)) 
                         & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) {
                        milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                            = ((((0U == (0x0000001fU 
                                         & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) 
                                 | (4U == (0x0000001fU 
                                           & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                                | (8U == (0x0000001fU 
                                          & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                               | (0x0cU == (0x0000001fU 
                                            & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))));
                    }
                } else {
                    milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw = 1U;
                }
            } else if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)) 
                        & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) {
                milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                    = ((((0U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) 
                         | (4U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                        | (8U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                       | (0x0cU == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))));
            }
        } else if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)) 
                    & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) {
            milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                = ((((0U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))) 
                     | (4U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                    | (8U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a)))) 
                   | (0x0cU == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__308__a))));
        }
    }
    vlSelfRef.milan_datapath__DOT__csr__DOT__shadow_axi_we 
        = milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw;
    vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__dup_sum_w 
        = (0x0001ffffU & (((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_440) 
                           & ((vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_fed_r 
                               >> (0x0000001fU & (IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__pop_idx_r))) 
                              & (0U == vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r
                                 [(0x0000001fU & (IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__pop_idx_r))]))) 
                          + (IData)(vlSelfRef.milan_datapath__DOT__lb_dup_cnt_w)));
    vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__pop_act_w 
        = ((0U != vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r
            [(0x0000001fU & (IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__pop_idx_r))]) 
           & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_440));
    milan_datapath__DOT__aaf_packetizer__DOT__eff_vid_w 
        = (0x00000fffU & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_domain__DOT__adopted_r)
                           ? (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_domain__DOT__decl_vid_r)
                           : ((0U == (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__et_r))
                               ? (IData)(vlSelfRef.milan_datapath__DOT____Vcellinp__aaf_packetizer__vlan_vid_i)
                               : ((0U != (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__evid_r))
                                   ? (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__evid_r)
                                   : (IData)(vlSelfRef.milan_datapath__DOT____Vcellinp__aaf_packetizer__vlan_vid_i)))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__rgy_any_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__eavl_r) 
           | (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_113));
    vlSelfRef.milan_datapath__DOT__ctr_avb_link_edge_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__ctr_link_q_r) 
           != (IData)(vlSelfRef.milan_datapath__DOT__eff_link_w));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_domain__DOT__link_rise_w 
        = ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_domain__DOT__link_q_r)) 
           & (IData)(vlSelfRef.milan_datapath__DOT__eff_link_w));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_domain__DOT__link_fall_w 
        = ((~ (IData)(vlSelfRef.milan_datapath__DOT__eff_link_w)) 
           & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_domain__DOT__link_q_r));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__link_fall_w 
        = ((~ (IData)(vlSelfRef.milan_datapath__DOT__eff_link_w)) 
           & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__link_q_r));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_382 = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__link_q_r) 
                                                  != (IData)(vlSelfRef.milan_datapath__DOT__eff_link_w));
    vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__subtype 
        = (0x000000ffU & ((((0U == (0x0000001fU & (
                                                   ((IData)(0x01bfU) 
                                                    - 
                                                    (0x000001f8U 
                                                     & (((IData)(2U) 
                                                         + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__et_off)) 
                                                        << 3U))) 
                                                   - (IData)(7U))))
                             ? 0U : (vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__hdr
                                     [(((IData)(7U) 
                                        + (0x000001ffU 
                                           & (((IData)(0x01bfU) 
                                               - (0x000001f8U 
                                                  & (((IData)(2U) 
                                                      + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__et_off)) 
                                                     << 3U))) 
                                              - (IData)(7U)))) 
                                       >> 5U)] << ((IData)(0x00000020U) 
                                                   - 
                                                   (0x0000001fU 
                                                    & (((IData)(0x01bfU) 
                                                        - 
                                                        (0x000001f8U 
                                                         & (((IData)(2U) 
                                                             + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__et_off)) 
                                                            << 3U))) 
                                                       - (IData)(7U)))))) 
                           | (vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__hdr
                              [(0x0000000fU & ((((IData)(0x01bfU) 
                                                 - 
                                                 (0x000001f8U 
                                                  & (((IData)(2U) 
                                                      + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__et_off)) 
                                                     << 3U))) 
                                                - (IData)(7U)) 
                                               >> 5U))] 
                              >> (0x0000001fU & (((IData)(0x01bfU) 
                                                  - 
                                                  (0x000001f8U 
                                                   & (((IData)(2U) 
                                                       + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__et_off)) 
                                                      << 3U))) 
                                                 - (IData)(7U))))) 
                          & (- (IData)((0x01bfU >= 
                                        (0x000001ffU 
                                         & (((IData)(0x01bfU) 
                                             - (0x000001f8U 
                                                & (((IData)(2U) 
                                                    + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__et_off)) 
                                                   << 3U))) 
                                            - (IData)(7U))))))));
    vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__b1 
        = (0x000000ffU & ((((0U == (0x0000001fU & (
                                                   ((IData)(0x01bfU) 
                                                    - 
                                                    (0x000001f8U 
                                                     & (((IData)(3U) 
                                                         + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__et_off)) 
                                                        << 3U))) 
                                                   - (IData)(7U))))
                             ? 0U : (vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__hdr
                                     [(((IData)(7U) 
                                        + (0x000001ffU 
                                           & (((IData)(0x01bfU) 
                                               - (0x000001f8U 
                                                  & (((IData)(3U) 
                                                      + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__et_off)) 
                                                     << 3U))) 
                                              - (IData)(7U)))) 
                                       >> 5U)] << ((IData)(0x00000020U) 
                                                   - 
                                                   (0x0000001fU 
                                                    & (((IData)(0x01bfU) 
                                                        - 
                                                        (0x000001f8U 
                                                         & (((IData)(3U) 
                                                             + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__et_off)) 
                                                            << 3U))) 
                                                       - (IData)(7U)))))) 
                           | (vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__hdr
                              [(0x0000000fU & ((((IData)(0x01bfU) 
                                                 - 
                                                 (0x000001f8U 
                                                  & (((IData)(3U) 
                                                      + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__et_off)) 
                                                     << 3U))) 
                                                - (IData)(7U)) 
                                               >> 5U))] 
                              >> (0x0000001fU & (((IData)(0x01bfU) 
                                                  - 
                                                  (0x000001f8U 
                                                   & (((IData)(3U) 
                                                       + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__et_off)) 
                                                      << 3U))) 
                                                 - (IData)(7U))))) 
                          & (- (IData)((0x01bfU >= 
                                        (0x000001ffU 
                                         & (((IData)(0x01bfU) 
                                             - (0x000001f8U 
                                                & (((IData)(3U) 
                                                    + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__et_off)) 
                                                   << 3U))) 
                                            - (IData)(7U))))))));
    vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__sid 
        = (((QData)((IData)(((((0x0000ff00U & (((((0U 
                                                   == 
                                                   (0x0000001fU 
                                                    & (((IData)(0x01bfU) 
                                                        - 
                                                        (0x000001f8U 
                                                         & (((IData)(6U) 
                                                             + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__et_off)) 
                                                            << 3U))) 
                                                       - (IData)(7U))))
                                                   ? 0U
                                                   : 
                                                  (vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__hdr
                                                   [
                                                   (((IData)(7U) 
                                                     + 
                                                     (0x000001ffU 
                                                      & (((IData)(0x01bfU) 
                                                          - 
                                                          (0x000001f8U 
                                                           & (((IData)(6U) 
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
                                                          & (((IData)(6U) 
                                                              + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__et_off)) 
                                                             << 3U))) 
                                                        - (IData)(7U)))))) 
                                                 | (vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__hdr
                                                    [
                                                    (0x0000000fU 
                                                     & ((((IData)(0x01bfU) 
                                                          - 
                                                          (0x000001f8U 
                                                           & (((IData)(6U) 
                                                               + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__et_off)) 
                                                              << 3U))) 
                                                         - (IData)(7U)) 
                                                        >> 5U))] 
                                                    >> 
                                                    (0x0000001fU 
                                                     & (((IData)(0x01bfU) 
                                                         - 
                                                         (0x000001f8U 
                                                          & (((IData)(6U) 
                                                              + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__et_off)) 
                                                             << 3U))) 
                                                        - (IData)(7U))))) 
                                                & (- (IData)(
                                                             (0x01bfU 
                                                              >= 
                                                              (0x000001ffU 
                                                               & (((IData)(0x01bfU) 
                                                                   - 
                                                                   (0x000001f8U 
                                                                    & (((IData)(6U) 
                                                                        + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__et_off)) 
                                                                       << 3U))) 
                                                                  - (IData)(7U))))))) 
                                               << 8U)) 
                               | (0x000000ffU & (((
                                                   (0U 
                                                    == 
                                                    (0x0000001fU 
                                                     & (((IData)(0x01bfU) 
                                                         - 
                                                         (0x000001f8U 
                                                          & (((IData)(7U) 
                                                              + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__et_off)) 
                                                             << 3U))) 
                                                        - (IData)(7U))))
                                                    ? 0U
                                                    : 
                                                   (vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__hdr
                                                    [
                                                    (((IData)(7U) 
                                                      + 
                                                      (0x000001ffU 
                                                       & (((IData)(0x01bfU) 
                                                           - 
                                                           (0x000001f8U 
                                                            & (((IData)(7U) 
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
                                                           & (((IData)(7U) 
                                                               + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__et_off)) 
                                                              << 3U))) 
                                                         - (IData)(7U)))))) 
                                                  | (vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__hdr
                                                     [
                                                     (0x0000000fU 
                                                      & ((((IData)(0x01bfU) 
                                                           - 
                                                           (0x000001f8U 
                                                            & (((IData)(7U) 
                                                                + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__et_off)) 
                                                               << 3U))) 
                                                          - (IData)(7U)) 
                                                         >> 5U))] 
                                                     >> 
                                                     (0x0000001fU 
                                                      & (((IData)(0x01bfU) 
                                                          - 
                                                          (0x000001f8U 
                                                           & (((IData)(7U) 
                                                               + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__et_off)) 
                                                              << 3U))) 
                                                         - (IData)(7U))))) 
                                                 & (- (IData)(
                                                              (0x01bfU 
                                                               >= 
                                                               (0x000001ffU 
                                                                & (((IData)(0x01bfU) 
                                                                    - 
                                                                    (0x000001f8U 
                                                                     & (((IData)(7U) 
                                                                         + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__et_off)) 
                                                                        << 3U))) 
                                                                   - (IData)(7U))))))))) 
                              << 0x00000010U) | ((0x0000ff00U 
                                                  & (((((0U 
                                                         == 
                                                         (0x0000001fU 
                                                          & (((IData)(0x01bfU) 
                                                              - 
                                                              (0x000001f8U 
                                                               & (((IData)(8U) 
                                                                   + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__et_off)) 
                                                                  << 3U))) 
                                                             - (IData)(7U))))
                                                         ? 0U
                                                         : 
                                                        (vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__hdr
                                                         [
                                                         (((IData)(7U) 
                                                           + 
                                                           (0x000001ffU 
                                                            & (((IData)(0x01bfU) 
                                                                - 
                                                                (0x000001f8U 
                                                                 & (((IData)(8U) 
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
                                                                & (((IData)(8U) 
                                                                    + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__et_off)) 
                                                                   << 3U))) 
                                                              - (IData)(7U)))))) 
                                                       | (vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__hdr
                                                          [
                                                          (0x0000000fU 
                                                           & ((((IData)(0x01bfU) 
                                                                - 
                                                                (0x000001f8U 
                                                                 & (((IData)(8U) 
                                                                     + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__et_off)) 
                                                                    << 3U))) 
                                                               - (IData)(7U)) 
                                                              >> 5U))] 
                                                          >> 
                                                          (0x0000001fU 
                                                           & (((IData)(0x01bfU) 
                                                               - 
                                                               (0x000001f8U 
                                                                & (((IData)(8U) 
                                                                    + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__et_off)) 
                                                                   << 3U))) 
                                                              - (IData)(7U))))) 
                                                      & (- (IData)(
                                                                   (0x01bfU 
                                                                    >= 
                                                                    (0x000001ffU 
                                                                     & (((IData)(0x01bfU) 
                                                                         - 
                                                                         (0x000001f8U 
                                                                          & (((IData)(8U) 
                                                                              + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__et_off)) 
                                                                             << 3U))) 
                                                                        - (IData)(7U))))))) 
                                                     << 8U)) 
                                                 | (0x000000ffU 
                                                    & ((((0U 
                                                          == 
                                                          (0x0000001fU 
                                                           & (((IData)(0x01bfU) 
                                                               - 
                                                               (0x000001f8U 
                                                                & (((IData)(9U) 
                                                                    + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__et_off)) 
                                                                   << 3U))) 
                                                              - (IData)(7U))))
                                                          ? 0U
                                                          : 
                                                         (vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__hdr
                                                          [
                                                          (((IData)(7U) 
                                                            + 
                                                            (0x000001ffU 
                                                             & (((IData)(0x01bfU) 
                                                                 - 
                                                                 (0x000001f8U 
                                                                  & (((IData)(9U) 
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
                                                                 & (((IData)(9U) 
                                                                     + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__et_off)) 
                                                                    << 3U))) 
                                                               - (IData)(7U)))))) 
                                                        | (vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__hdr
                                                           [
                                                           (0x0000000fU 
                                                            & ((((IData)(0x01bfU) 
                                                                 - 
                                                                 (0x000001f8U 
                                                                  & (((IData)(9U) 
                                                                      + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__et_off)) 
                                                                     << 3U))) 
                                                                - (IData)(7U)) 
                                                               >> 5U))] 
                                                           >> 
                                                           (0x0000001fU 
                                                            & (((IData)(0x01bfU) 
                                                                - 
                                                                (0x000001f8U 
                                                                 & (((IData)(9U) 
                                                                     + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__et_off)) 
                                                                    << 3U))) 
                                                               - (IData)(7U))))) 
                                                       & (- (IData)(
                                                                    (0x01bfU 
                                                                     >= 
                                                                     (0x000001ffU 
                                                                      & (((IData)(0x01bfU) 
                                                                          - 
                                                                          (0x000001f8U 
                                                                           & (((IData)(9U) 
                                                                               + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__et_off)) 
                                                                              << 3U))) 
                                                                         - (IData)(7U)))))))))))) 
            << 0x00000020U) | (QData)((IData)(((((0x0000ff00U 
                                                  & (((((0U 
                                                         == 
                                                         (0x0000001fU 
                                                          & (((IData)(0x01bfU) 
                                                              - 
                                                              (0x000001f8U 
                                                               & (((IData)(0x0aU) 
                                                                   + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__et_off)) 
                                                                  << 3U))) 
                                                             - (IData)(7U))))
                                                         ? 0U
                                                         : 
                                                        (vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__hdr
                                                         [
                                                         (((IData)(7U) 
                                                           + 
                                                           (0x000001ffU 
                                                            & (((IData)(0x01bfU) 
                                                                - 
                                                                (0x000001f8U 
                                                                 & (((IData)(0x0aU) 
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
                                                                & (((IData)(0x0aU) 
                                                                    + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__et_off)) 
                                                                   << 3U))) 
                                                              - (IData)(7U)))))) 
                                                       | (vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__hdr
                                                          [
                                                          (0x0000000fU 
                                                           & ((((IData)(0x01bfU) 
                                                                - 
                                                                (0x000001f8U 
                                                                 & (((IData)(0x0aU) 
                                                                     + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__et_off)) 
                                                                    << 3U))) 
                                                               - (IData)(7U)) 
                                                              >> 5U))] 
                                                          >> 
                                                          (0x0000001fU 
                                                           & (((IData)(0x01bfU) 
                                                               - 
                                                               (0x000001f8U 
                                                                & (((IData)(0x0aU) 
                                                                    + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__et_off)) 
                                                                   << 3U))) 
                                                              - (IData)(7U))))) 
                                                      & (- (IData)(
                                                                   (0x01bfU 
                                                                    >= 
                                                                    (0x000001ffU 
                                                                     & (((IData)(0x01bfU) 
                                                                         - 
                                                                         (0x000001f8U 
                                                                          & (((IData)(0x0aU) 
                                                                              + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__et_off)) 
                                                                             << 3U))) 
                                                                        - (IData)(7U))))))) 
                                                     << 8U)) 
                                                 | (0x000000ffU 
                                                    & ((((0U 
                                                          == 
                                                          (0x0000001fU 
                                                           & (((IData)(0x01bfU) 
                                                               - 
                                                               (0x000001f8U 
                                                                & (((IData)(0x0bU) 
                                                                    + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__et_off)) 
                                                                   << 3U))) 
                                                              - (IData)(7U))))
                                                          ? 0U
                                                          : 
                                                         (vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__hdr
                                                          [
                                                          (((IData)(7U) 
                                                            + 
                                                            (0x000001ffU 
                                                             & (((IData)(0x01bfU) 
                                                                 - 
                                                                 (0x000001f8U 
                                                                  & (((IData)(0x0bU) 
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
                                                                 & (((IData)(0x0bU) 
                                                                     + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__et_off)) 
                                                                    << 3U))) 
                                                               - (IData)(7U)))))) 
                                                        | (vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__hdr
                                                           [
                                                           (0x0000000fU 
                                                            & ((((IData)(0x01bfU) 
                                                                 - 
                                                                 (0x000001f8U 
                                                                  & (((IData)(0x0bU) 
                                                                      + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__et_off)) 
                                                                     << 3U))) 
                                                                - (IData)(7U)) 
                                                               >> 5U))] 
                                                           >> 
                                                           (0x0000001fU 
                                                            & (((IData)(0x01bfU) 
                                                                - 
                                                                (0x000001f8U 
                                                                 & (((IData)(0x0bU) 
                                                                     + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__et_off)) 
                                                                    << 3U))) 
                                                               - (IData)(7U))))) 
                                                       & (- (IData)(
                                                                    (0x01bfU 
                                                                     >= 
                                                                     (0x000001ffU 
                                                                      & (((IData)(0x01bfU) 
                                                                          - 
                                                                          (0x000001f8U 
                                                                           & (((IData)(0x0bU) 
                                                                               + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__et_off)) 
                                                                              << 3U))) 
                                                                         - (IData)(7U))))))))) 
                                                << 0x00000010U) 
                                               | ((0x0000ff00U 
                                                   & (((((0U 
                                                          == 
                                                          (0x0000001fU 
                                                           & (((IData)(0x01bfU) 
                                                               - 
                                                               (0x000001f8U 
                                                                & (((IData)(0x0cU) 
                                                                    + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__et_off)) 
                                                                   << 3U))) 
                                                              - (IData)(7U))))
                                                          ? 0U
                                                          : 
                                                         (vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__hdr
                                                          [
                                                          (((IData)(7U) 
                                                            + 
                                                            (0x000001ffU 
                                                             & (((IData)(0x01bfU) 
                                                                 - 
                                                                 (0x000001f8U 
                                                                  & (((IData)(0x0cU) 
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
                                                                 & (((IData)(0x0cU) 
                                                                     + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__et_off)) 
                                                                    << 3U))) 
                                                               - (IData)(7U)))))) 
                                                        | (vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__hdr
                                                           [
                                                           (0x0000000fU 
                                                            & ((((IData)(0x01bfU) 
                                                                 - 
                                                                 (0x000001f8U 
                                                                  & (((IData)(0x0cU) 
                                                                      + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__et_off)) 
                                                                     << 3U))) 
                                                                - (IData)(7U)) 
                                                               >> 5U))] 
                                                           >> 
                                                           (0x0000001fU 
                                                            & (((IData)(0x01bfU) 
                                                                - 
                                                                (0x000001f8U 
                                                                 & (((IData)(0x0cU) 
                                                                     + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__et_off)) 
                                                                    << 3U))) 
                                                               - (IData)(7U))))) 
                                                       & (- (IData)(
                                                                    (0x01bfU 
                                                                     >= 
                                                                     (0x000001ffU 
                                                                      & (((IData)(0x01bfU) 
                                                                          - 
                                                                          (0x000001f8U 
                                                                           & (((IData)(0x0cU) 
                                                                               + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__et_off)) 
                                                                              << 3U))) 
                                                                         - (IData)(7U))))))) 
                                                      << 8U)) 
                                                  | (0x000000ffU 
                                                     & ((((0U 
                                                           == 
                                                           (0x0000001fU 
                                                            & (((IData)(0x01bfU) 
                                                                - 
                                                                (0x000001f8U 
                                                                 & (((IData)(0x0dU) 
                                                                     + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__et_off)) 
                                                                    << 3U))) 
                                                               - (IData)(7U))))
                                                           ? 0U
                                                           : 
                                                          (vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__hdr
                                                           [
                                                           (((IData)(7U) 
                                                             + 
                                                             (0x000001ffU 
                                                              & (((IData)(0x01bfU) 
                                                                  - 
                                                                  (0x000001f8U 
                                                                   & (((IData)(0x0dU) 
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
                                                                  & (((IData)(0x0dU) 
                                                                      + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__et_off)) 
                                                                     << 3U))) 
                                                                - (IData)(7U)))))) 
                                                         | (vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__hdr
                                                            [
                                                            (0x0000000fU 
                                                             & ((((IData)(0x01bfU) 
                                                                  - 
                                                                  (0x000001f8U 
                                                                   & (((IData)(0x0dU) 
                                                                       + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__et_off)) 
                                                                      << 3U))) 
                                                                 - (IData)(7U)) 
                                                                >> 5U))] 
                                                            >> 
                                                            (0x0000001fU 
                                                             & (((IData)(0x01bfU) 
                                                                 - 
                                                                 (0x000001f8U 
                                                                  & (((IData)(0x0dU) 
                                                                      + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__et_off)) 
                                                                     << 3U))) 
                                                                - (IData)(7U))))) 
                                                        & (- (IData)(
                                                                     (0x01bfU 
                                                                      >= 
                                                                      (0x000001ffU 
                                                                       & (((IData)(0x01bfU) 
                                                                           - 
                                                                           (0x000001f8U 
                                                                            & (((IData)(0x0dU) 
                                                                                + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__et_off)) 
                                                                               << 3U))) 
                                                                          - (IData)(7U)))))))))))));
    vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ext_wr_ok_w 
        = ((~ (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__eng_we_w)) 
           & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__lctx_wr_p_r));
    vlSelfRef.milan_datapath__DOT__crf_rx__DOT__w_bind_rise_w 
        = ((~ (IData)(vlSelfRef.milan_datapath__DOT__crf_rx__DOT__en_q)) 
           & (IData)(vlSelfRef.milan_datapath__DOT____Vcellinp__crf_rx__en_i));
    vlSelfRef.milan_datapath__DOT__crf_rx__DOT__w_hit 
        = ((IData)(vlSelfRef.milan_datapath__DOT__avtprx_parse_p) 
           & ((IData)(vlSelfRef.milan_datapath__DOT____Vcellinp__crf_rx__en_i) 
              & ((4U == (IData)(vlSelfRef.milan_datapath__DOT__avtprx_subtype)) 
                 & (vlSelfRef.milan_datapath__DOT__avtprx_sid_frame 
                    == ((0x00000100U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__bound_hold_r))
                         ? (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__bound_sid_r[17U])) 
                             << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__bound_sid_r[16U])))
                         : (((QData)((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__crf_sidhi)) 
                             << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__crf_sidlo))))))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_stage_ser_w 
        = ((5U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__a_st_r)) 
           & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_133));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__pay_w 
        = ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_214) 
           & (0x0026U <= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__bidx_r)));
    vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pown_v_w = 0U;
    if ((((IData)(vlSelfRef.milan_datapath__DOT__cmap_slot_w) 
          >= vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pbase_w[0U]) 
         & ((IData)(vlSelfRef.milan_datapath__DOT__cmap_slot_w) 
            < vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pbase_w[1U]))) {
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pown_v_w = 1U;
    }
    if ((((IData)(vlSelfRef.milan_datapath__DOT__cmap_slot_w) 
          >= vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pbase_w[1U]) 
         & ((IData)(vlSelfRef.milan_datapath__DOT__cmap_slot_w) 
            < vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pbase_w[2U]))) {
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pown_v_w = 1U;
    }
    if ((((IData)(vlSelfRef.milan_datapath__DOT__cmap_slot_w) 
          >= vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pbase_w[2U]) 
         & ((IData)(vlSelfRef.milan_datapath__DOT__cmap_slot_w) 
            < vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pbase_w[3U]))) {
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pown_v_w = 1U;
    }
    if ((((IData)(vlSelfRef.milan_datapath__DOT__cmap_slot_w) 
          >= vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pbase_w[3U]) 
         & ((IData)(vlSelfRef.milan_datapath__DOT__cmap_slot_w) 
            < vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pbase_w[4U]))) {
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pown_v_w = 1U;
    }
    if ((((IData)(vlSelfRef.milan_datapath__DOT__cmap_slot_w) 
          >= vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pbase_w[4U]) 
         & ((IData)(vlSelfRef.milan_datapath__DOT__cmap_slot_w) 
            < vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pbase_w[5U]))) {
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pown_v_w = 1U;
    }
    if ((((IData)(vlSelfRef.milan_datapath__DOT__cmap_slot_w) 
          >= vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pbase_w[5U]) 
         & ((IData)(vlSelfRef.milan_datapath__DOT__cmap_slot_w) 
            < vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pbase_w[6U]))) {
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pown_v_w = 1U;
    }
    vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pown_o_w = 0U;
    if ((((IData)(vlSelfRef.milan_datapath__DOT__cmap_slot_w) 
          >= vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pbase_w[0U]) 
         & ((IData)(vlSelfRef.milan_datapath__DOT__cmap_slot_w) 
            < vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pbase_w[1U]))) {
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pown_o_w 
            = (3U & ((IData)(vlSelfRef.milan_datapath__DOT__cmap_slot_w) 
                     - vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pbase_w[0U]));
    }
    if ((((IData)(vlSelfRef.milan_datapath__DOT__cmap_slot_w) 
          >= vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pbase_w[1U]) 
         & ((IData)(vlSelfRef.milan_datapath__DOT__cmap_slot_w) 
            < vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pbase_w[2U]))) {
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pown_o_w 
            = (3U & ((IData)(vlSelfRef.milan_datapath__DOT__cmap_slot_w) 
                     - vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pbase_w[1U]));
    }
    if ((((IData)(vlSelfRef.milan_datapath__DOT__cmap_slot_w) 
          >= vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pbase_w[2U]) 
         & ((IData)(vlSelfRef.milan_datapath__DOT__cmap_slot_w) 
            < vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pbase_w[3U]))) {
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pown_o_w 
            = (3U & ((IData)(vlSelfRef.milan_datapath__DOT__cmap_slot_w) 
                     - vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pbase_w[2U]));
    }
    if ((((IData)(vlSelfRef.milan_datapath__DOT__cmap_slot_w) 
          >= vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pbase_w[3U]) 
         & ((IData)(vlSelfRef.milan_datapath__DOT__cmap_slot_w) 
            < vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pbase_w[4U]))) {
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pown_o_w 
            = (3U & ((IData)(vlSelfRef.milan_datapath__DOT__cmap_slot_w) 
                     - vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pbase_w[3U]));
    }
    if ((((IData)(vlSelfRef.milan_datapath__DOT__cmap_slot_w) 
          >= vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pbase_w[4U]) 
         & ((IData)(vlSelfRef.milan_datapath__DOT__cmap_slot_w) 
            < vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pbase_w[5U]))) {
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pown_o_w 
            = (3U & ((IData)(vlSelfRef.milan_datapath__DOT__cmap_slot_w) 
                     - vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pbase_w[4U]));
    }
    if ((((IData)(vlSelfRef.milan_datapath__DOT__cmap_slot_w) 
          >= vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pbase_w[5U]) 
         & ((IData)(vlSelfRef.milan_datapath__DOT__cmap_slot_w) 
            < vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pbase_w[6U]))) {
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pown_o_w 
            = (3U & ((IData)(vlSelfRef.milan_datapath__DOT__cmap_slot_w) 
                     - vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pbase_w[5U]));
    }
    if ((((IData)(vlSelfRef.milan_datapath__DOT__cmap_slot_w) 
          >= vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pbase_w[6U]) 
         & ((IData)(vlSelfRef.milan_datapath__DOT__cmap_slot_w) 
            < vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pbase_w[7U]))) {
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pown_v_w = 1U;
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pown_o_w 
            = (3U & ((IData)(vlSelfRef.milan_datapath__DOT__cmap_slot_w) 
                     - vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pbase_w[6U]));
    }
    vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pown_t_w = 0U;
    if ((((IData)(vlSelfRef.milan_datapath__DOT__cmap_slot_w) 
          >= vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pbase_w[0U]) 
         & ((IData)(vlSelfRef.milan_datapath__DOT__cmap_slot_w) 
            < vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pbase_w[1U]))) {
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pown_t_w = 0U;
    }
    if ((((IData)(vlSelfRef.milan_datapath__DOT__cmap_slot_w) 
          >= vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pbase_w[1U]) 
         & ((IData)(vlSelfRef.milan_datapath__DOT__cmap_slot_w) 
            < vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pbase_w[2U]))) {
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pown_t_w = 1U;
    }
    if ((((IData)(vlSelfRef.milan_datapath__DOT__cmap_slot_w) 
          >= vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pbase_w[2U]) 
         & ((IData)(vlSelfRef.milan_datapath__DOT__cmap_slot_w) 
            < vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pbase_w[3U]))) {
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pown_t_w = 2U;
    }
    if ((((IData)(vlSelfRef.milan_datapath__DOT__cmap_slot_w) 
          >= vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pbase_w[3U]) 
         & ((IData)(vlSelfRef.milan_datapath__DOT__cmap_slot_w) 
            < vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pbase_w[4U]))) {
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pown_t_w = 3U;
    }
    if ((((IData)(vlSelfRef.milan_datapath__DOT__cmap_slot_w) 
          >= vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pbase_w[4U]) 
         & ((IData)(vlSelfRef.milan_datapath__DOT__cmap_slot_w) 
            < vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pbase_w[5U]))) {
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pown_t_w = 4U;
    }
    if ((((IData)(vlSelfRef.milan_datapath__DOT__cmap_slot_w) 
          >= vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pbase_w[5U]) 
         & ((IData)(vlSelfRef.milan_datapath__DOT__cmap_slot_w) 
            < vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pbase_w[6U]))) {
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pown_t_w = 5U;
    }
    if ((((IData)(vlSelfRef.milan_datapath__DOT__cmap_slot_w) 
          >= vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pbase_w[6U]) 
         & ((IData)(vlSelfRef.milan_datapath__DOT__cmap_slot_w) 
            < vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pbase_w[7U]))) {
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pown_t_w = 6U;
    }
    if ((((IData)(vlSelfRef.milan_datapath__DOT__cmap_slot_w) 
          >= vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pbase_w[7U]) 
         & ((IData)(vlSelfRef.milan_datapath__DOT__cmap_slot_w) 
            < vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pbase_w[8U]))) {
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pown_v_w = 1U;
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pown_o_w 
            = (3U & ((IData)(vlSelfRef.milan_datapath__DOT__cmap_slot_w) 
                     - vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pbase_w[7U]));
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pown_t_w = 7U;
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__cad_hit_w 
        = ((5U > ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__chk_slot_r) 
                  - (IData)(0x00000047U))) & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__exp_fire_w));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__exp_hit_w 
        = ((9U > ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__chk_slot_r) 
                  - (IData)(0x0000004eU))) & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__exp_fire_w));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__noadp_exp_w 
        = ((9U > ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__chk_slot_r) 
                  - (IData)(1U))) & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__exp_fire_w));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__adv_exp_w 
        = ((1U > (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__chk_slot_r)) 
           & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__exp_fire_w));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__set_tmr_w = 0U;
    if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__exp_fire_w) 
         & ((9U > ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__chk_slot_r) 
                   - (IData)(0x00000013U))) & ((0x000000ffU 
                                                & ((IData)(0x50U) 
                                                   + 
                                                   ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__chk_slot_r) 
                                                    - (IData)(0x13U)))) 
                                               == (0x000000ffU 
                                                   & (IData)(
                                                             (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__sweep_rdata_r 
                                                              >> 0x00000020U))))))) {
        if ((8U >= (0x0000000fU & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__chk_slot_r) 
                                   - (IData)(3U))))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__set_tmr_w 
                = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__set_tmr_w) 
                   | (0x01ffU & ((IData)(1U) << (0x0000000fU 
                                                 & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__chk_slot_r) 
                                                    - (IData)(3U))))));
        }
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__exp_hit_w 
        = ((9U > ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__chk_slot_r) 
                  - (IData)(0x00000057U))) & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__exp_fire_w));
    vlSelfRef.milan_datapath__DOT__eff_crft_dmac_w 
        = (0x0000ffffffffffffULL & ((0U != vlSelfRef.milan_datapath__DOT__cfg_crft_dmac)
                                     ? vlSelfRef.milan_datapath__DOT__cfg_crft_dmac
                                     : (8ULL + vlSelfRef.milan_datapath__DOT__eff_aaf_dmac)));
    milan_datapath__DOT__aaf_packetizer__DOT__eff_dmac_w 
        = (0x0000ffffffffffffULL & ((0U == (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__et_r))
                                     ? vlSelfRef.milan_datapath__DOT__eff_aaf_dmac
                                     : ((0U != vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__edmac_r)
                                         ? vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__edmac_r
                                         : (vlSelfRef.milan_datapath__DOT__eff_aaf_dmac 
                                            + (QData)((IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__et_r))))));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_223 = (0x00000001ffffffffULL 
                                                  & ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__a_fmt_w)) 
                                                     - (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__b_or_imm_w))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__mut_req_w 
        = ((2U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__nvm_op_w)) 
           | (1U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__nvm_op_w)));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__eff_len_w 
        = (((2U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__nvm_op_w)) 
            & (0U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__nvm_len_w)))
            ? (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__rec_len_w)
            : (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__nvm_len_w));
    vlSelfRef.milan_datapath__DOT__pp_ctr_evt_valid_w = 0U;
    vlSelfRef.milan_datapath__DOT__pp_ctr_evt_type_w = 0U;
    vlSelfRef.milan_datapath__DOT__pp_ctr_evt_index_w = 0U;
    milan_datapath__DOT__pp_ctr_event_pick__DOT__pick 
        = vlSelfRef.milan_datapath__DOT__pp_ctr_rr_r;
    if ((0x00000014U <= milan_datapath__DOT__pp_ctr_event_pick__DOT__pick)) {
        milan_datapath__DOT__pp_ctr_event_pick__DOT__pick 
            = (milan_datapath__DOT__pp_ctr_event_pick__DOT__pick 
               - (IData)(0x00000014U));
    }
    if (((0x13U >= (0x0000001fU & milan_datapath__DOT__pp_ctr_event_pick__DOT__pick)) 
         && (1U & (vlSelfRef.milan_datapath__DOT__pp_ctr_all_pend_w 
                   >> (0x0000001fU & milan_datapath__DOT__pp_ctr_event_pick__DOT__pick))))) {
        vlSelfRef.milan_datapath__DOT__pp_ctr_evt_valid_w = 1U;
        if ((9U > milan_datapath__DOT__pp_ctr_event_pick__DOT__pick)) {
            vlSelfRef.milan_datapath__DOT__pp_ctr_evt_type_w = 5U;
            vlSelfRef.milan_datapath__DOT__pp_ctr_evt_index_w 
                = (0x0000ffffU & milan_datapath__DOT__pp_ctr_event_pick__DOT__pick);
        } else if ((0x00000012U > milan_datapath__DOT__pp_ctr_event_pick__DOT__pick)) {
            vlSelfRef.milan_datapath__DOT__pp_ctr_evt_type_w = 6U;
            vlSelfRef.milan_datapath__DOT__pp_ctr_evt_index_w 
                = (0x0000ffffU & (milan_datapath__DOT__pp_ctr_event_pick__DOT__pick 
                                  - (IData)(9U)));
        } else {
            vlSelfRef.milan_datapath__DOT__pp_ctr_evt_type_w 
                = ((0x00000012U == milan_datapath__DOT__pp_ctr_event_pick__DOT__pick)
                    ? 9U : 0x0024U);
        }
    }
    milan_datapath__DOT__pp_ctr_event_pick__DOT__pick 
        = ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_rr_r));
    if ((0x00000014U <= milan_datapath__DOT__pp_ctr_event_pick__DOT__pick)) {
        milan_datapath__DOT__pp_ctr_event_pick__DOT__pick 
            = (milan_datapath__DOT__pp_ctr_event_pick__DOT__pick 
               - (IData)(0x00000014U));
    }
    if (((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_evt_valid_w)) 
         & ((0x13U >= (0x0000001fU & milan_datapath__DOT__pp_ctr_event_pick__DOT__pick)) 
            && (1U & (vlSelfRef.milan_datapath__DOT__pp_ctr_all_pend_w 
                      >> (0x0000001fU & milan_datapath__DOT__pp_ctr_event_pick__DOT__pick)))))) {
        vlSelfRef.milan_datapath__DOT__pp_ctr_evt_valid_w = 1U;
        if ((9U > milan_datapath__DOT__pp_ctr_event_pick__DOT__pick)) {
            vlSelfRef.milan_datapath__DOT__pp_ctr_evt_type_w = 5U;
            vlSelfRef.milan_datapath__DOT__pp_ctr_evt_index_w 
                = (0x0000ffffU & milan_datapath__DOT__pp_ctr_event_pick__DOT__pick);
        } else if ((0x00000012U > milan_datapath__DOT__pp_ctr_event_pick__DOT__pick)) {
            vlSelfRef.milan_datapath__DOT__pp_ctr_evt_type_w = 6U;
            vlSelfRef.milan_datapath__DOT__pp_ctr_evt_index_w 
                = (0x0000ffffU & (milan_datapath__DOT__pp_ctr_event_pick__DOT__pick 
                                  - (IData)(9U)));
        } else {
            vlSelfRef.milan_datapath__DOT__pp_ctr_evt_type_w 
                = ((0x00000012U == milan_datapath__DOT__pp_ctr_event_pick__DOT__pick)
                    ? 9U : 0x0024U);
        }
    }
    milan_datapath__DOT__pp_ctr_event_pick__DOT__pick 
        = ((IData)(2U) + (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_rr_r));
    if ((0x00000014U <= milan_datapath__DOT__pp_ctr_event_pick__DOT__pick)) {
        milan_datapath__DOT__pp_ctr_event_pick__DOT__pick 
            = (milan_datapath__DOT__pp_ctr_event_pick__DOT__pick 
               - (IData)(0x00000014U));
    }
    if (((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_evt_valid_w)) 
         & ((0x13U >= (0x0000001fU & milan_datapath__DOT__pp_ctr_event_pick__DOT__pick)) 
            && (1U & (vlSelfRef.milan_datapath__DOT__pp_ctr_all_pend_w 
                      >> (0x0000001fU & milan_datapath__DOT__pp_ctr_event_pick__DOT__pick)))))) {
        vlSelfRef.milan_datapath__DOT__pp_ctr_evt_valid_w = 1U;
        if ((9U > milan_datapath__DOT__pp_ctr_event_pick__DOT__pick)) {
            vlSelfRef.milan_datapath__DOT__pp_ctr_evt_type_w = 5U;
            vlSelfRef.milan_datapath__DOT__pp_ctr_evt_index_w 
                = (0x0000ffffU & milan_datapath__DOT__pp_ctr_event_pick__DOT__pick);
        } else if ((0x00000012U > milan_datapath__DOT__pp_ctr_event_pick__DOT__pick)) {
            vlSelfRef.milan_datapath__DOT__pp_ctr_evt_type_w = 6U;
            vlSelfRef.milan_datapath__DOT__pp_ctr_evt_index_w 
                = (0x0000ffffU & (milan_datapath__DOT__pp_ctr_event_pick__DOT__pick 
                                  - (IData)(9U)));
        } else {
            vlSelfRef.milan_datapath__DOT__pp_ctr_evt_type_w 
                = ((0x00000012U == milan_datapath__DOT__pp_ctr_event_pick__DOT__pick)
                    ? 9U : 0x0024U);
        }
    }
    milan_datapath__DOT__pp_ctr_event_pick__DOT__pick 
        = ((IData)(3U) + (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_rr_r));
    if ((0x00000014U <= milan_datapath__DOT__pp_ctr_event_pick__DOT__pick)) {
        milan_datapath__DOT__pp_ctr_event_pick__DOT__pick 
            = (milan_datapath__DOT__pp_ctr_event_pick__DOT__pick 
               - (IData)(0x00000014U));
    }
    if (((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_evt_valid_w)) 
         & ((0x13U >= (0x0000001fU & milan_datapath__DOT__pp_ctr_event_pick__DOT__pick)) 
            && (1U & (vlSelfRef.milan_datapath__DOT__pp_ctr_all_pend_w 
                      >> (0x0000001fU & milan_datapath__DOT__pp_ctr_event_pick__DOT__pick)))))) {
        vlSelfRef.milan_datapath__DOT__pp_ctr_evt_valid_w = 1U;
        if ((9U > milan_datapath__DOT__pp_ctr_event_pick__DOT__pick)) {
            vlSelfRef.milan_datapath__DOT__pp_ctr_evt_type_w = 5U;
            vlSelfRef.milan_datapath__DOT__pp_ctr_evt_index_w 
                = (0x0000ffffU & milan_datapath__DOT__pp_ctr_event_pick__DOT__pick);
        } else if ((0x00000012U > milan_datapath__DOT__pp_ctr_event_pick__DOT__pick)) {
            vlSelfRef.milan_datapath__DOT__pp_ctr_evt_type_w = 6U;
            vlSelfRef.milan_datapath__DOT__pp_ctr_evt_index_w 
                = (0x0000ffffU & (milan_datapath__DOT__pp_ctr_event_pick__DOT__pick 
                                  - (IData)(9U)));
        } else {
            vlSelfRef.milan_datapath__DOT__pp_ctr_evt_type_w 
                = ((0x00000012U == milan_datapath__DOT__pp_ctr_event_pick__DOT__pick)
                    ? 9U : 0x0024U);
        }
    }
    milan_datapath__DOT__pp_ctr_event_pick__DOT__pick 
        = ((IData)(4U) + (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_rr_r));
    if ((0x00000014U <= milan_datapath__DOT__pp_ctr_event_pick__DOT__pick)) {
        milan_datapath__DOT__pp_ctr_event_pick__DOT__pick 
            = (milan_datapath__DOT__pp_ctr_event_pick__DOT__pick 
               - (IData)(0x00000014U));
    }
    if (((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_evt_valid_w)) 
         & ((0x13U >= (0x0000001fU & milan_datapath__DOT__pp_ctr_event_pick__DOT__pick)) 
            && (1U & (vlSelfRef.milan_datapath__DOT__pp_ctr_all_pend_w 
                      >> (0x0000001fU & milan_datapath__DOT__pp_ctr_event_pick__DOT__pick)))))) {
        vlSelfRef.milan_datapath__DOT__pp_ctr_evt_valid_w = 1U;
        if ((9U > milan_datapath__DOT__pp_ctr_event_pick__DOT__pick)) {
            vlSelfRef.milan_datapath__DOT__pp_ctr_evt_type_w = 5U;
            vlSelfRef.milan_datapath__DOT__pp_ctr_evt_index_w 
                = (0x0000ffffU & milan_datapath__DOT__pp_ctr_event_pick__DOT__pick);
        } else if ((0x00000012U > milan_datapath__DOT__pp_ctr_event_pick__DOT__pick)) {
            vlSelfRef.milan_datapath__DOT__pp_ctr_evt_type_w = 6U;
            vlSelfRef.milan_datapath__DOT__pp_ctr_evt_index_w 
                = (0x0000ffffU & (milan_datapath__DOT__pp_ctr_event_pick__DOT__pick 
                                  - (IData)(9U)));
        } else {
            vlSelfRef.milan_datapath__DOT__pp_ctr_evt_type_w 
                = ((0x00000012U == milan_datapath__DOT__pp_ctr_event_pick__DOT__pick)
                    ? 9U : 0x0024U);
        }
    }
    milan_datapath__DOT__pp_ctr_event_pick__DOT__pick 
        = ((IData)(5U) + (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_rr_r));
    if ((0x00000014U <= milan_datapath__DOT__pp_ctr_event_pick__DOT__pick)) {
        milan_datapath__DOT__pp_ctr_event_pick__DOT__pick 
            = (milan_datapath__DOT__pp_ctr_event_pick__DOT__pick 
               - (IData)(0x00000014U));
    }
    if (((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_evt_valid_w)) 
         & ((0x13U >= (0x0000001fU & milan_datapath__DOT__pp_ctr_event_pick__DOT__pick)) 
            && (1U & (vlSelfRef.milan_datapath__DOT__pp_ctr_all_pend_w 
                      >> (0x0000001fU & milan_datapath__DOT__pp_ctr_event_pick__DOT__pick)))))) {
        vlSelfRef.milan_datapath__DOT__pp_ctr_evt_valid_w = 1U;
        if ((9U > milan_datapath__DOT__pp_ctr_event_pick__DOT__pick)) {
            vlSelfRef.milan_datapath__DOT__pp_ctr_evt_type_w = 5U;
            vlSelfRef.milan_datapath__DOT__pp_ctr_evt_index_w 
                = (0x0000ffffU & milan_datapath__DOT__pp_ctr_event_pick__DOT__pick);
        } else if ((0x00000012U > milan_datapath__DOT__pp_ctr_event_pick__DOT__pick)) {
            vlSelfRef.milan_datapath__DOT__pp_ctr_evt_type_w = 6U;
            vlSelfRef.milan_datapath__DOT__pp_ctr_evt_index_w 
                = (0x0000ffffU & (milan_datapath__DOT__pp_ctr_event_pick__DOT__pick 
                                  - (IData)(9U)));
        } else {
            vlSelfRef.milan_datapath__DOT__pp_ctr_evt_type_w 
                = ((0x00000012U == milan_datapath__DOT__pp_ctr_event_pick__DOT__pick)
                    ? 9U : 0x0024U);
        }
    }
    milan_datapath__DOT__pp_ctr_event_pick__DOT__pick 
        = ((IData)(6U) + (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_rr_r));
    if ((0x00000014U <= milan_datapath__DOT__pp_ctr_event_pick__DOT__pick)) {
        milan_datapath__DOT__pp_ctr_event_pick__DOT__pick 
            = (milan_datapath__DOT__pp_ctr_event_pick__DOT__pick 
               - (IData)(0x00000014U));
    }
    if (((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_evt_valid_w)) 
         & ((0x13U >= (0x0000001fU & milan_datapath__DOT__pp_ctr_event_pick__DOT__pick)) 
            && (1U & (vlSelfRef.milan_datapath__DOT__pp_ctr_all_pend_w 
                      >> (0x0000001fU & milan_datapath__DOT__pp_ctr_event_pick__DOT__pick)))))) {
        vlSelfRef.milan_datapath__DOT__pp_ctr_evt_valid_w = 1U;
        if ((9U > milan_datapath__DOT__pp_ctr_event_pick__DOT__pick)) {
            vlSelfRef.milan_datapath__DOT__pp_ctr_evt_type_w = 5U;
            vlSelfRef.milan_datapath__DOT__pp_ctr_evt_index_w 
                = (0x0000ffffU & milan_datapath__DOT__pp_ctr_event_pick__DOT__pick);
        } else if ((0x00000012U > milan_datapath__DOT__pp_ctr_event_pick__DOT__pick)) {
            vlSelfRef.milan_datapath__DOT__pp_ctr_evt_type_w = 6U;
            vlSelfRef.milan_datapath__DOT__pp_ctr_evt_index_w 
                = (0x0000ffffU & (milan_datapath__DOT__pp_ctr_event_pick__DOT__pick 
                                  - (IData)(9U)));
        } else {
            vlSelfRef.milan_datapath__DOT__pp_ctr_evt_type_w 
                = ((0x00000012U == milan_datapath__DOT__pp_ctr_event_pick__DOT__pick)
                    ? 9U : 0x0024U);
        }
    }
    milan_datapath__DOT__pp_ctr_event_pick__DOT__pick 
        = ((IData)(7U) + (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_rr_r));
    if ((0x00000014U <= milan_datapath__DOT__pp_ctr_event_pick__DOT__pick)) {
        milan_datapath__DOT__pp_ctr_event_pick__DOT__pick 
            = (milan_datapath__DOT__pp_ctr_event_pick__DOT__pick 
               - (IData)(0x00000014U));
    }
    if (((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_evt_valid_w)) 
         & ((0x13U >= (0x0000001fU & milan_datapath__DOT__pp_ctr_event_pick__DOT__pick)) 
            && (1U & (vlSelfRef.milan_datapath__DOT__pp_ctr_all_pend_w 
                      >> (0x0000001fU & milan_datapath__DOT__pp_ctr_event_pick__DOT__pick)))))) {
        vlSelfRef.milan_datapath__DOT__pp_ctr_evt_valid_w = 1U;
        if ((9U > milan_datapath__DOT__pp_ctr_event_pick__DOT__pick)) {
            vlSelfRef.milan_datapath__DOT__pp_ctr_evt_type_w = 5U;
            vlSelfRef.milan_datapath__DOT__pp_ctr_evt_index_w 
                = (0x0000ffffU & milan_datapath__DOT__pp_ctr_event_pick__DOT__pick);
        } else if ((0x00000012U > milan_datapath__DOT__pp_ctr_event_pick__DOT__pick)) {
            vlSelfRef.milan_datapath__DOT__pp_ctr_evt_type_w = 6U;
            vlSelfRef.milan_datapath__DOT__pp_ctr_evt_index_w 
                = (0x0000ffffU & (milan_datapath__DOT__pp_ctr_event_pick__DOT__pick 
                                  - (IData)(9U)));
        } else {
            vlSelfRef.milan_datapath__DOT__pp_ctr_evt_type_w 
                = ((0x00000012U == milan_datapath__DOT__pp_ctr_event_pick__DOT__pick)
                    ? 9U : 0x0024U);
        }
    }
    milan_datapath__DOT__pp_ctr_event_pick__DOT__pick 
        = ((IData)(8U) + (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_rr_r));
    if ((0x00000014U <= milan_datapath__DOT__pp_ctr_event_pick__DOT__pick)) {
        milan_datapath__DOT__pp_ctr_event_pick__DOT__pick 
            = (milan_datapath__DOT__pp_ctr_event_pick__DOT__pick 
               - (IData)(0x00000014U));
    }
    if (((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_evt_valid_w)) 
         & ((0x13U >= (0x0000001fU & milan_datapath__DOT__pp_ctr_event_pick__DOT__pick)) 
            && (1U & (vlSelfRef.milan_datapath__DOT__pp_ctr_all_pend_w 
                      >> (0x0000001fU & milan_datapath__DOT__pp_ctr_event_pick__DOT__pick)))))) {
        vlSelfRef.milan_datapath__DOT__pp_ctr_evt_valid_w = 1U;
        if ((9U > milan_datapath__DOT__pp_ctr_event_pick__DOT__pick)) {
            vlSelfRef.milan_datapath__DOT__pp_ctr_evt_type_w = 5U;
            vlSelfRef.milan_datapath__DOT__pp_ctr_evt_index_w 
                = (0x0000ffffU & milan_datapath__DOT__pp_ctr_event_pick__DOT__pick);
        } else if ((0x00000012U > milan_datapath__DOT__pp_ctr_event_pick__DOT__pick)) {
            vlSelfRef.milan_datapath__DOT__pp_ctr_evt_type_w = 6U;
            vlSelfRef.milan_datapath__DOT__pp_ctr_evt_index_w 
                = (0x0000ffffU & (milan_datapath__DOT__pp_ctr_event_pick__DOT__pick 
                                  - (IData)(9U)));
        } else {
            vlSelfRef.milan_datapath__DOT__pp_ctr_evt_type_w 
                = ((0x00000012U == milan_datapath__DOT__pp_ctr_event_pick__DOT__pick)
                    ? 9U : 0x0024U);
        }
    }
    milan_datapath__DOT__pp_ctr_event_pick__DOT__pick 
        = ((IData)(9U) + (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_rr_r));
    if ((0x00000014U <= milan_datapath__DOT__pp_ctr_event_pick__DOT__pick)) {
        milan_datapath__DOT__pp_ctr_event_pick__DOT__pick 
            = (milan_datapath__DOT__pp_ctr_event_pick__DOT__pick 
               - (IData)(0x00000014U));
    }
    if (((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_evt_valid_w)) 
         & ((0x13U >= (0x0000001fU & milan_datapath__DOT__pp_ctr_event_pick__DOT__pick)) 
            && (1U & (vlSelfRef.milan_datapath__DOT__pp_ctr_all_pend_w 
                      >> (0x0000001fU & milan_datapath__DOT__pp_ctr_event_pick__DOT__pick)))))) {
        vlSelfRef.milan_datapath__DOT__pp_ctr_evt_valid_w = 1U;
        if ((9U > milan_datapath__DOT__pp_ctr_event_pick__DOT__pick)) {
            vlSelfRef.milan_datapath__DOT__pp_ctr_evt_type_w = 5U;
            vlSelfRef.milan_datapath__DOT__pp_ctr_evt_index_w 
                = (0x0000ffffU & milan_datapath__DOT__pp_ctr_event_pick__DOT__pick);
        } else if ((0x00000012U > milan_datapath__DOT__pp_ctr_event_pick__DOT__pick)) {
            vlSelfRef.milan_datapath__DOT__pp_ctr_evt_type_w = 6U;
            vlSelfRef.milan_datapath__DOT__pp_ctr_evt_index_w 
                = (0x0000ffffU & (milan_datapath__DOT__pp_ctr_event_pick__DOT__pick 
                                  - (IData)(9U)));
        } else {
            vlSelfRef.milan_datapath__DOT__pp_ctr_evt_type_w 
                = ((0x00000012U == milan_datapath__DOT__pp_ctr_event_pick__DOT__pick)
                    ? 9U : 0x0024U);
        }
    }
    milan_datapath__DOT__pp_ctr_event_pick__DOT__pick 
        = ((IData)(0x0000000aU) + (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_rr_r));
    if ((0x00000014U <= milan_datapath__DOT__pp_ctr_event_pick__DOT__pick)) {
        milan_datapath__DOT__pp_ctr_event_pick__DOT__pick 
            = (milan_datapath__DOT__pp_ctr_event_pick__DOT__pick 
               - (IData)(0x00000014U));
    }
    if (((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_evt_valid_w)) 
         & ((0x13U >= (0x0000001fU & milan_datapath__DOT__pp_ctr_event_pick__DOT__pick)) 
            && (1U & (vlSelfRef.milan_datapath__DOT__pp_ctr_all_pend_w 
                      >> (0x0000001fU & milan_datapath__DOT__pp_ctr_event_pick__DOT__pick)))))) {
        vlSelfRef.milan_datapath__DOT__pp_ctr_evt_valid_w = 1U;
        if ((9U > milan_datapath__DOT__pp_ctr_event_pick__DOT__pick)) {
            vlSelfRef.milan_datapath__DOT__pp_ctr_evt_type_w = 5U;
            vlSelfRef.milan_datapath__DOT__pp_ctr_evt_index_w 
                = (0x0000ffffU & milan_datapath__DOT__pp_ctr_event_pick__DOT__pick);
        } else if ((0x00000012U > milan_datapath__DOT__pp_ctr_event_pick__DOT__pick)) {
            vlSelfRef.milan_datapath__DOT__pp_ctr_evt_type_w = 6U;
            vlSelfRef.milan_datapath__DOT__pp_ctr_evt_index_w 
                = (0x0000ffffU & (milan_datapath__DOT__pp_ctr_event_pick__DOT__pick 
                                  - (IData)(9U)));
        } else {
            vlSelfRef.milan_datapath__DOT__pp_ctr_evt_type_w 
                = ((0x00000012U == milan_datapath__DOT__pp_ctr_event_pick__DOT__pick)
                    ? 9U : 0x0024U);
        }
    }
    milan_datapath__DOT__pp_ctr_event_pick__DOT__pick 
        = ((IData)(0x0000000bU) + (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_rr_r));
    if ((0x00000014U <= milan_datapath__DOT__pp_ctr_event_pick__DOT__pick)) {
        milan_datapath__DOT__pp_ctr_event_pick__DOT__pick 
            = (milan_datapath__DOT__pp_ctr_event_pick__DOT__pick 
               - (IData)(0x00000014U));
    }
    if (((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_evt_valid_w)) 
         & ((0x13U >= (0x0000001fU & milan_datapath__DOT__pp_ctr_event_pick__DOT__pick)) 
            && (1U & (vlSelfRef.milan_datapath__DOT__pp_ctr_all_pend_w 
                      >> (0x0000001fU & milan_datapath__DOT__pp_ctr_event_pick__DOT__pick)))))) {
        vlSelfRef.milan_datapath__DOT__pp_ctr_evt_valid_w = 1U;
        if ((9U > milan_datapath__DOT__pp_ctr_event_pick__DOT__pick)) {
            vlSelfRef.milan_datapath__DOT__pp_ctr_evt_type_w = 5U;
            vlSelfRef.milan_datapath__DOT__pp_ctr_evt_index_w 
                = (0x0000ffffU & milan_datapath__DOT__pp_ctr_event_pick__DOT__pick);
        } else if ((0x00000012U > milan_datapath__DOT__pp_ctr_event_pick__DOT__pick)) {
            vlSelfRef.milan_datapath__DOT__pp_ctr_evt_type_w = 6U;
            vlSelfRef.milan_datapath__DOT__pp_ctr_evt_index_w 
                = (0x0000ffffU & (milan_datapath__DOT__pp_ctr_event_pick__DOT__pick 
                                  - (IData)(9U)));
        } else {
            vlSelfRef.milan_datapath__DOT__pp_ctr_evt_type_w 
                = ((0x00000012U == milan_datapath__DOT__pp_ctr_event_pick__DOT__pick)
                    ? 9U : 0x0024U);
        }
    }
    milan_datapath__DOT__pp_ctr_event_pick__DOT__pick 
        = ((IData)(0x0000000cU) + (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_rr_r));
    if ((0x00000014U <= milan_datapath__DOT__pp_ctr_event_pick__DOT__pick)) {
        milan_datapath__DOT__pp_ctr_event_pick__DOT__pick 
            = (milan_datapath__DOT__pp_ctr_event_pick__DOT__pick 
               - (IData)(0x00000014U));
    }
    if (((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_evt_valid_w)) 
         & ((0x13U >= (0x0000001fU & milan_datapath__DOT__pp_ctr_event_pick__DOT__pick)) 
            && (1U & (vlSelfRef.milan_datapath__DOT__pp_ctr_all_pend_w 
                      >> (0x0000001fU & milan_datapath__DOT__pp_ctr_event_pick__DOT__pick)))))) {
        vlSelfRef.milan_datapath__DOT__pp_ctr_evt_valid_w = 1U;
        if ((9U > milan_datapath__DOT__pp_ctr_event_pick__DOT__pick)) {
            vlSelfRef.milan_datapath__DOT__pp_ctr_evt_type_w = 5U;
            vlSelfRef.milan_datapath__DOT__pp_ctr_evt_index_w 
                = (0x0000ffffU & milan_datapath__DOT__pp_ctr_event_pick__DOT__pick);
        } else if ((0x00000012U > milan_datapath__DOT__pp_ctr_event_pick__DOT__pick)) {
            vlSelfRef.milan_datapath__DOT__pp_ctr_evt_type_w = 6U;
            vlSelfRef.milan_datapath__DOT__pp_ctr_evt_index_w 
                = (0x0000ffffU & (milan_datapath__DOT__pp_ctr_event_pick__DOT__pick 
                                  - (IData)(9U)));
        } else {
            vlSelfRef.milan_datapath__DOT__pp_ctr_evt_type_w 
                = ((0x00000012U == milan_datapath__DOT__pp_ctr_event_pick__DOT__pick)
                    ? 9U : 0x0024U);
        }
    }
    milan_datapath__DOT__pp_ctr_event_pick__DOT__pick 
        = ((IData)(0x0000000dU) + (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_rr_r));
    if ((0x00000014U <= milan_datapath__DOT__pp_ctr_event_pick__DOT__pick)) {
        milan_datapath__DOT__pp_ctr_event_pick__DOT__pick 
            = (milan_datapath__DOT__pp_ctr_event_pick__DOT__pick 
               - (IData)(0x00000014U));
    }
    if (((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_evt_valid_w)) 
         & ((0x13U >= (0x0000001fU & milan_datapath__DOT__pp_ctr_event_pick__DOT__pick)) 
            && (1U & (vlSelfRef.milan_datapath__DOT__pp_ctr_all_pend_w 
                      >> (0x0000001fU & milan_datapath__DOT__pp_ctr_event_pick__DOT__pick)))))) {
        vlSelfRef.milan_datapath__DOT__pp_ctr_evt_valid_w = 1U;
        if ((9U > milan_datapath__DOT__pp_ctr_event_pick__DOT__pick)) {
            vlSelfRef.milan_datapath__DOT__pp_ctr_evt_type_w = 5U;
            vlSelfRef.milan_datapath__DOT__pp_ctr_evt_index_w 
                = (0x0000ffffU & milan_datapath__DOT__pp_ctr_event_pick__DOT__pick);
        } else if ((0x00000012U > milan_datapath__DOT__pp_ctr_event_pick__DOT__pick)) {
            vlSelfRef.milan_datapath__DOT__pp_ctr_evt_type_w = 6U;
            vlSelfRef.milan_datapath__DOT__pp_ctr_evt_index_w 
                = (0x0000ffffU & (milan_datapath__DOT__pp_ctr_event_pick__DOT__pick 
                                  - (IData)(9U)));
        } else {
            vlSelfRef.milan_datapath__DOT__pp_ctr_evt_type_w 
                = ((0x00000012U == milan_datapath__DOT__pp_ctr_event_pick__DOT__pick)
                    ? 9U : 0x0024U);
        }
    }
    milan_datapath__DOT__pp_ctr_event_pick__DOT__pick 
        = ((IData)(0x0000000eU) + (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_rr_r));
    if ((0x00000014U <= milan_datapath__DOT__pp_ctr_event_pick__DOT__pick)) {
        milan_datapath__DOT__pp_ctr_event_pick__DOT__pick 
            = (milan_datapath__DOT__pp_ctr_event_pick__DOT__pick 
               - (IData)(0x00000014U));
    }
    if (((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_evt_valid_w)) 
         & ((0x13U >= (0x0000001fU & milan_datapath__DOT__pp_ctr_event_pick__DOT__pick)) 
            && (1U & (vlSelfRef.milan_datapath__DOT__pp_ctr_all_pend_w 
                      >> (0x0000001fU & milan_datapath__DOT__pp_ctr_event_pick__DOT__pick)))))) {
        vlSelfRef.milan_datapath__DOT__pp_ctr_evt_valid_w = 1U;
        if ((9U > milan_datapath__DOT__pp_ctr_event_pick__DOT__pick)) {
            vlSelfRef.milan_datapath__DOT__pp_ctr_evt_type_w = 5U;
            vlSelfRef.milan_datapath__DOT__pp_ctr_evt_index_w 
                = (0x0000ffffU & milan_datapath__DOT__pp_ctr_event_pick__DOT__pick);
        } else if ((0x00000012U > milan_datapath__DOT__pp_ctr_event_pick__DOT__pick)) {
            vlSelfRef.milan_datapath__DOT__pp_ctr_evt_type_w = 6U;
            vlSelfRef.milan_datapath__DOT__pp_ctr_evt_index_w 
                = (0x0000ffffU & (milan_datapath__DOT__pp_ctr_event_pick__DOT__pick 
                                  - (IData)(9U)));
        } else {
            vlSelfRef.milan_datapath__DOT__pp_ctr_evt_type_w 
                = ((0x00000012U == milan_datapath__DOT__pp_ctr_event_pick__DOT__pick)
                    ? 9U : 0x0024U);
        }
    }
    milan_datapath__DOT__pp_ctr_event_pick__DOT__pick 
        = ((IData)(0x0000000fU) + (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_rr_r));
    if ((0x00000014U <= milan_datapath__DOT__pp_ctr_event_pick__DOT__pick)) {
        milan_datapath__DOT__pp_ctr_event_pick__DOT__pick 
            = (milan_datapath__DOT__pp_ctr_event_pick__DOT__pick 
               - (IData)(0x00000014U));
    }
    if (((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_evt_valid_w)) 
         & ((0x13U >= (0x0000001fU & milan_datapath__DOT__pp_ctr_event_pick__DOT__pick)) 
            && (1U & (vlSelfRef.milan_datapath__DOT__pp_ctr_all_pend_w 
                      >> (0x0000001fU & milan_datapath__DOT__pp_ctr_event_pick__DOT__pick)))))) {
        vlSelfRef.milan_datapath__DOT__pp_ctr_evt_valid_w = 1U;
        if ((9U > milan_datapath__DOT__pp_ctr_event_pick__DOT__pick)) {
            vlSelfRef.milan_datapath__DOT__pp_ctr_evt_type_w = 5U;
            vlSelfRef.milan_datapath__DOT__pp_ctr_evt_index_w 
                = (0x0000ffffU & milan_datapath__DOT__pp_ctr_event_pick__DOT__pick);
        } else if ((0x00000012U > milan_datapath__DOT__pp_ctr_event_pick__DOT__pick)) {
            vlSelfRef.milan_datapath__DOT__pp_ctr_evt_type_w = 6U;
            vlSelfRef.milan_datapath__DOT__pp_ctr_evt_index_w 
                = (0x0000ffffU & (milan_datapath__DOT__pp_ctr_event_pick__DOT__pick 
                                  - (IData)(9U)));
        } else {
            vlSelfRef.milan_datapath__DOT__pp_ctr_evt_type_w 
                = ((0x00000012U == milan_datapath__DOT__pp_ctr_event_pick__DOT__pick)
                    ? 9U : 0x0024U);
        }
    }
    milan_datapath__DOT__pp_ctr_event_pick__DOT__pick 
        = ((IData)(0x00000010U) + (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_rr_r));
    if ((0x00000014U <= milan_datapath__DOT__pp_ctr_event_pick__DOT__pick)) {
        milan_datapath__DOT__pp_ctr_event_pick__DOT__pick 
            = (milan_datapath__DOT__pp_ctr_event_pick__DOT__pick 
               - (IData)(0x00000014U));
    }
    if (((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_evt_valid_w)) 
         & ((0x13U >= (0x0000001fU & milan_datapath__DOT__pp_ctr_event_pick__DOT__pick)) 
            && (1U & (vlSelfRef.milan_datapath__DOT__pp_ctr_all_pend_w 
                      >> (0x0000001fU & milan_datapath__DOT__pp_ctr_event_pick__DOT__pick)))))) {
        vlSelfRef.milan_datapath__DOT__pp_ctr_evt_valid_w = 1U;
        if ((9U > milan_datapath__DOT__pp_ctr_event_pick__DOT__pick)) {
            vlSelfRef.milan_datapath__DOT__pp_ctr_evt_type_w = 5U;
            vlSelfRef.milan_datapath__DOT__pp_ctr_evt_index_w 
                = (0x0000ffffU & milan_datapath__DOT__pp_ctr_event_pick__DOT__pick);
        } else if ((0x00000012U > milan_datapath__DOT__pp_ctr_event_pick__DOT__pick)) {
            vlSelfRef.milan_datapath__DOT__pp_ctr_evt_type_w = 6U;
            vlSelfRef.milan_datapath__DOT__pp_ctr_evt_index_w 
                = (0x0000ffffU & (milan_datapath__DOT__pp_ctr_event_pick__DOT__pick 
                                  - (IData)(9U)));
        } else {
            vlSelfRef.milan_datapath__DOT__pp_ctr_evt_type_w 
                = ((0x00000012U == milan_datapath__DOT__pp_ctr_event_pick__DOT__pick)
                    ? 9U : 0x0024U);
        }
    }
    milan_datapath__DOT__pp_ctr_event_pick__DOT__pick 
        = ((IData)(0x00000011U) + (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_rr_r));
    if ((0x00000014U <= milan_datapath__DOT__pp_ctr_event_pick__DOT__pick)) {
        milan_datapath__DOT__pp_ctr_event_pick__DOT__pick 
            = (milan_datapath__DOT__pp_ctr_event_pick__DOT__pick 
               - (IData)(0x00000014U));
    }
    if (((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_evt_valid_w)) 
         & ((0x13U >= (0x0000001fU & milan_datapath__DOT__pp_ctr_event_pick__DOT__pick)) 
            && (1U & (vlSelfRef.milan_datapath__DOT__pp_ctr_all_pend_w 
                      >> (0x0000001fU & milan_datapath__DOT__pp_ctr_event_pick__DOT__pick)))))) {
        vlSelfRef.milan_datapath__DOT__pp_ctr_evt_valid_w = 1U;
        if ((9U > milan_datapath__DOT__pp_ctr_event_pick__DOT__pick)) {
            vlSelfRef.milan_datapath__DOT__pp_ctr_evt_type_w = 5U;
            vlSelfRef.milan_datapath__DOT__pp_ctr_evt_index_w 
                = (0x0000ffffU & milan_datapath__DOT__pp_ctr_event_pick__DOT__pick);
        } else if ((0x00000012U > milan_datapath__DOT__pp_ctr_event_pick__DOT__pick)) {
            vlSelfRef.milan_datapath__DOT__pp_ctr_evt_type_w = 6U;
            vlSelfRef.milan_datapath__DOT__pp_ctr_evt_index_w 
                = (0x0000ffffU & (milan_datapath__DOT__pp_ctr_event_pick__DOT__pick 
                                  - (IData)(9U)));
        } else {
            vlSelfRef.milan_datapath__DOT__pp_ctr_evt_type_w 
                = ((0x00000012U == milan_datapath__DOT__pp_ctr_event_pick__DOT__pick)
                    ? 9U : 0x0024U);
        }
    }
    milan_datapath__DOT__pp_ctr_event_pick__DOT__pick 
        = ((IData)(0x00000012U) + (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_rr_r));
    if ((0x00000014U <= milan_datapath__DOT__pp_ctr_event_pick__DOT__pick)) {
        milan_datapath__DOT__pp_ctr_event_pick__DOT__pick 
            = (milan_datapath__DOT__pp_ctr_event_pick__DOT__pick 
               - (IData)(0x00000014U));
    }
    if (((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_evt_valid_w)) 
         & ((0x13U >= (0x0000001fU & milan_datapath__DOT__pp_ctr_event_pick__DOT__pick)) 
            && (1U & (vlSelfRef.milan_datapath__DOT__pp_ctr_all_pend_w 
                      >> (0x0000001fU & milan_datapath__DOT__pp_ctr_event_pick__DOT__pick)))))) {
        vlSelfRef.milan_datapath__DOT__pp_ctr_evt_valid_w = 1U;
        if ((9U > milan_datapath__DOT__pp_ctr_event_pick__DOT__pick)) {
            vlSelfRef.milan_datapath__DOT__pp_ctr_evt_type_w = 5U;
            vlSelfRef.milan_datapath__DOT__pp_ctr_evt_index_w 
                = (0x0000ffffU & milan_datapath__DOT__pp_ctr_event_pick__DOT__pick);
        } else if ((0x00000012U > milan_datapath__DOT__pp_ctr_event_pick__DOT__pick)) {
            vlSelfRef.milan_datapath__DOT__pp_ctr_evt_type_w = 6U;
            vlSelfRef.milan_datapath__DOT__pp_ctr_evt_index_w 
                = (0x0000ffffU & (milan_datapath__DOT__pp_ctr_event_pick__DOT__pick 
                                  - (IData)(9U)));
        } else {
            vlSelfRef.milan_datapath__DOT__pp_ctr_evt_type_w 
                = ((0x00000012U == milan_datapath__DOT__pp_ctr_event_pick__DOT__pick)
                    ? 9U : 0x0024U);
        }
    }
    milan_datapath__DOT__pp_ctr_event_pick__DOT__pick 
        = ((IData)(0x00000013U) + (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_rr_r));
    if ((0x00000014U <= milan_datapath__DOT__pp_ctr_event_pick__DOT__pick)) {
        milan_datapath__DOT__pp_ctr_event_pick__DOT__pick 
            = (milan_datapath__DOT__pp_ctr_event_pick__DOT__pick 
               - (IData)(0x00000014U));
    }
    if (((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_evt_valid_w)) 
         & ((0x13U >= (0x0000001fU & milan_datapath__DOT__pp_ctr_event_pick__DOT__pick)) 
            && (1U & (vlSelfRef.milan_datapath__DOT__pp_ctr_all_pend_w 
                      >> (0x0000001fU & milan_datapath__DOT__pp_ctr_event_pick__DOT__pick)))))) {
        vlSelfRef.milan_datapath__DOT__pp_ctr_evt_valid_w = 1U;
        if ((9U > milan_datapath__DOT__pp_ctr_event_pick__DOT__pick)) {
            vlSelfRef.milan_datapath__DOT__pp_ctr_evt_type_w = 5U;
            vlSelfRef.milan_datapath__DOT__pp_ctr_evt_index_w 
                = (0x0000ffffU & milan_datapath__DOT__pp_ctr_event_pick__DOT__pick);
        } else if ((0x00000012U > milan_datapath__DOT__pp_ctr_event_pick__DOT__pick)) {
            vlSelfRef.milan_datapath__DOT__pp_ctr_evt_type_w = 6U;
            vlSelfRef.milan_datapath__DOT__pp_ctr_evt_index_w 
                = (0x0000ffffU & (milan_datapath__DOT__pp_ctr_event_pick__DOT__pick 
                                  - (IData)(9U)));
        } else {
            vlSelfRef.milan_datapath__DOT__pp_ctr_evt_type_w 
                = ((0x00000012U == milan_datapath__DOT__pp_ctr_event_pick__DOT__pick)
                    ? 9U : 0x0024U);
        }
    }
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_254 = ((IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__beat_r) 
                                                  == 
                                                  (0x0000001fU 
                                                   & ((IData)(5U) 
                                                      + 
                                                      ((IData)(6U) 
                                                       * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_246)))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gdi_w 
        = ((0x004bU == (0x0000ffffU & ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__out_data_r[4U] 
                                        << 4U) | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__out_data_r[3U] 
                                                  >> 0x0000001cU)))) 
           & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__aem_w));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__ssrate_w 
        = ((0x0014U == (0x0000ffffU & ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__out_data_r[4U] 
                                        << 4U) | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__out_data_r[3U] 
                                                  >> 0x0000001cU)))) 
           & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__aem_w));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__sclks_w 
        = ((0x0016U == (0x0000ffffU & ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__out_data_r[4U] 
                                        << 4U) | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__out_data_r[3U] 
                                                  >> 0x0000001cU)))) 
           & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__aem_w));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__sctrl_w 
        = ((0x0018U == (0x0000ffffU & ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__out_data_r[4U] 
                                        << 4U) | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__out_data_r[3U] 
                                                  >> 0x0000001cU)))) 
           & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__aem_w));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__ssfmt_w 
        = ((8U == (0x0000ffffU & ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__out_data_r[4U] 
                                   << 4U) | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__out_data_r[3U] 
                                             >> 0x0000001cU)))) 
           & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__aem_w));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__ssinfo_w 
        = ((0x000eU == (0x0000ffffU & ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__out_data_r[4U] 
                                        << 4U) | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__out_data_r[3U] 
                                                  >> 0x0000001cU)))) 
           & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__aem_w));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__strt_w 
        = ((0x0022U == (0x0000ffffU & ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__out_data_r[4U] 
                                        << 4U) | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__out_data_r[3U] 
                                                  >> 0x0000001cU)))) 
           & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__aem_w));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__stop_w 
        = ((0x0023U == (0x0000ffffU & ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__out_data_r[4U] 
                                        << 4U) | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__out_data_r[3U] 
                                                  >> 0x0000001cU)))) 
           & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__aem_w));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__ctrs_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__aem_w) 
           & ((0x0010U <= (0x000007ffU & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__out_data_r[10U] 
                                          >> 0x0000000eU))) 
              & (0x0029U == (0x0000ffffU & ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__out_data_r[4U] 
                                             << 4U) 
                                            | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__out_data_r[3U] 
                                               >> 0x0000001cU))))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__aem_w) 
           & ((0x0014U <= (0x000007ffU & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__out_data_r[10U] 
                                          >> 0x0000000eU))) 
              & (0x002bU == (0x0000ffffU & ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__out_data_r[4U] 
                                             << 4U) 
                                            | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__out_data_r[3U] 
                                               >> 0x0000001cU))))));
    vlSelfRef.milan_datapath__DOT__gsi_decl_w = ((8U 
                                                  >= 
                                                  (0x0000000fU 
                                                   & (IData)(vlSelfRef.milan_datapath__DOT__gsiq_index_r))) 
                                                 & (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__declaring_r) 
                                                     >> 
                                                     (0x0000000fU 
                                                      & (IData)(vlSelfRef.milan_datapath__DOT__gsiq_index_r))) 
                                                    & (IData)(vlSelfRef.milan_datapath__DOT__gsi_out_w)));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__0__KET____DOT__u_rx_slots__DOT__ff_valid_w = 0U;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__0__KET____DOT__u_rx_slots__DOT__ff_slot_w = 0U;
    if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__0__KET____DOT__u_rx_slots__DOT__free_mask_w))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__0__KET____DOT__u_rx_slots__DOT__ff_valid_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__0__KET____DOT__u_rx_slots__DOT__ff_slot_w = 0U;
    }
    if ((1U & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__0__KET____DOT__u_rx_slots__DOT__ff_valid_w)) 
               & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__0__KET____DOT__u_rx_slots__DOT__free_mask_w) 
                  >> 1U)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__0__KET____DOT__u_rx_slots__DOT__ff_valid_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__0__KET____DOT__u_rx_slots__DOT__ff_slot_w = 1U;
    }
    if ((1U & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__0__KET____DOT__u_rx_slots__DOT__ff_valid_w)) 
               & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__0__KET____DOT__u_rx_slots__DOT__free_mask_w) 
                  >> 2U)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__0__KET____DOT__u_rx_slots__DOT__ff_valid_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__0__KET____DOT__u_rx_slots__DOT__ff_slot_w = 2U;
    }
    if (((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__0__KET____DOT__u_rx_slots__DOT__ff_valid_w)) 
         & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__0__KET____DOT__u_rx_slots__DOT__free_mask_w) 
            >> 3U))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__0__KET____DOT__u_rx_slots__DOT__ff_valid_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__0__KET____DOT__u_rx_slots__DOT__ff_slot_w = 3U;
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__name_hold_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gx_req_w) 
           & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__sname_r) 
              & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_stage_ready_r)) 
                 & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gxf_fail_r)))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__rgy_hold_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gx_req_w) 
           & ((~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gxf_fail_r) 
                  | (3U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__n_st_r)))) 
              & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_113)));
    vlSelfRef.milan_datapath__DOT__pp_amap_req_w = 
        ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gx_req_w) 
         & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_r));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_213 = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gx_req_w) 
                                                  & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_edit_r));
    vlSelfRef.milan_datapath__DOT__sfv_need_out_w = 0ULL;
    if ((0x00001000U & vlSelfRef.milan_datapath__DOT__cmap_flat_w[0U])) {
        vlSelfRef.milan_datapath__DOT__sfv_need_out_w 
            = (1ULL | (0x0000000ffffffff0ULL & vlSelfRef.milan_datapath__DOT__sfv_need_out_w));
    }
    if ((0x02000000U & vlSelfRef.milan_datapath__DOT__cmap_flat_w[0U])) {
        vlSelfRef.milan_datapath__DOT__sfv_need_out_w 
            = (2ULL | (0x0000000ffffffff0ULL & vlSelfRef.milan_datapath__DOT__sfv_need_out_w));
    }
    if ((0x00000040U & vlSelfRef.milan_datapath__DOT__cmap_flat_w[1U])) {
        vlSelfRef.milan_datapath__DOT__sfv_need_out_w 
            = (3ULL | (0x0000000ffffffff0ULL & vlSelfRef.milan_datapath__DOT__sfv_need_out_w));
    }
    if ((0x00080000U & vlSelfRef.milan_datapath__DOT__cmap_flat_w[1U])) {
        vlSelfRef.milan_datapath__DOT__sfv_need_out_w 
            = (4ULL | (0x0000000ffffffff0ULL & vlSelfRef.milan_datapath__DOT__sfv_need_out_w));
    }
    if ((1U & vlSelfRef.milan_datapath__DOT__cmap_flat_w[2U])) {
        vlSelfRef.milan_datapath__DOT__sfv_need_out_w 
            = (5ULL | (0x0000000ffffffff0ULL & vlSelfRef.milan_datapath__DOT__sfv_need_out_w));
    }
    if ((0x00002000U & vlSelfRef.milan_datapath__DOT__cmap_flat_w[2U])) {
        vlSelfRef.milan_datapath__DOT__sfv_need_out_w 
            = (6ULL | (0x0000000ffffffff0ULL & vlSelfRef.milan_datapath__DOT__sfv_need_out_w));
    }
    if ((0x04000000U & vlSelfRef.milan_datapath__DOT__cmap_flat_w[2U])) {
        vlSelfRef.milan_datapath__DOT__sfv_need_out_w 
            = (7ULL | (0x0000000ffffffff0ULL & vlSelfRef.milan_datapath__DOT__sfv_need_out_w));
    }
    if ((0x00000080U & vlSelfRef.milan_datapath__DOT__cmap_flat_w[3U])) {
        vlSelfRef.milan_datapath__DOT__sfv_need_out_w 
            = (8ULL | (0x0000000ffffffff0ULL & vlSelfRef.milan_datapath__DOT__sfv_need_out_w));
    }
    if ((0x00100000U & vlSelfRef.milan_datapath__DOT__cmap_flat_w[3U])) {
        vlSelfRef.milan_datapath__DOT__sfv_need_out_w 
            = (0x0000000000000010ULL | (0x0000000fffffff0fULL 
                                        & vlSelfRef.milan_datapath__DOT__sfv_need_out_w));
    }
    if ((2U & vlSelfRef.milan_datapath__DOT__cmap_flat_w[4U])) {
        vlSelfRef.milan_datapath__DOT__sfv_need_out_w 
            = (0x0000000000000020ULL | (0x0000000fffffff0fULL 
                                        & vlSelfRef.milan_datapath__DOT__sfv_need_out_w));
    }
    if ((0x00004000U & vlSelfRef.milan_datapath__DOT__cmap_flat_w[4U])) {
        vlSelfRef.milan_datapath__DOT__sfv_need_out_w 
            = (0x0000000000000030ULL | (0x0000000fffffff0fULL 
                                        & vlSelfRef.milan_datapath__DOT__sfv_need_out_w));
    }
    if ((0x08000000U & vlSelfRef.milan_datapath__DOT__cmap_flat_w[4U])) {
        vlSelfRef.milan_datapath__DOT__sfv_need_out_w 
            = (0x0000000000000040ULL | (0x0000000fffffff0fULL 
                                        & vlSelfRef.milan_datapath__DOT__sfv_need_out_w));
    }
    if ((0x00000100U & vlSelfRef.milan_datapath__DOT__cmap_flat_w[5U])) {
        vlSelfRef.milan_datapath__DOT__sfv_need_out_w 
            = (0x0000000000000050ULL | (0x0000000fffffff0fULL 
                                        & vlSelfRef.milan_datapath__DOT__sfv_need_out_w));
    }
    if ((0x00200000U & vlSelfRef.milan_datapath__DOT__cmap_flat_w[5U])) {
        vlSelfRef.milan_datapath__DOT__sfv_need_out_w 
            = (0x0000000000000060ULL | (0x0000000fffffff0fULL 
                                        & vlSelfRef.milan_datapath__DOT__sfv_need_out_w));
    }
    if ((4U & vlSelfRef.milan_datapath__DOT__cmap_flat_w[6U])) {
        vlSelfRef.milan_datapath__DOT__sfv_need_out_w 
            = (0x0000000000000070ULL | (0x0000000fffffff0fULL 
                                        & vlSelfRef.milan_datapath__DOT__sfv_need_out_w));
    }
    if ((0x00008000U & vlSelfRef.milan_datapath__DOT__cmap_flat_w[6U])) {
        vlSelfRef.milan_datapath__DOT__sfv_need_out_w 
            = (0x0000000000000080ULL | (0x0000000fffffff0fULL 
                                        & vlSelfRef.milan_datapath__DOT__sfv_need_out_w));
    }
    if ((0x10000000U & vlSelfRef.milan_datapath__DOT__cmap_flat_w[6U])) {
        vlSelfRef.milan_datapath__DOT__sfv_need_out_w 
            = (0x0000000000000100ULL | (0x0000000ffffff0ffULL 
                                        & vlSelfRef.milan_datapath__DOT__sfv_need_out_w));
    }
    if ((0x00000200U & vlSelfRef.milan_datapath__DOT__cmap_flat_w[7U])) {
        vlSelfRef.milan_datapath__DOT__sfv_need_out_w 
            = (0x0000000000000200ULL | (0x0000000ffffff0ffULL 
                                        & vlSelfRef.milan_datapath__DOT__sfv_need_out_w));
    }
    if ((0x00400000U & vlSelfRef.milan_datapath__DOT__cmap_flat_w[7U])) {
        vlSelfRef.milan_datapath__DOT__sfv_need_out_w 
            = (0x0000000000000300ULL | (0x0000000ffffff0ffULL 
                                        & vlSelfRef.milan_datapath__DOT__sfv_need_out_w));
    }
    if ((8U & vlSelfRef.milan_datapath__DOT__cmap_flat_w[8U])) {
        vlSelfRef.milan_datapath__DOT__sfv_need_out_w 
            = (0x0000000000000400ULL | (0x0000000ffffff0ffULL 
                                        & vlSelfRef.milan_datapath__DOT__sfv_need_out_w));
    }
    if ((0x00010000U & vlSelfRef.milan_datapath__DOT__cmap_flat_w[8U])) {
        vlSelfRef.milan_datapath__DOT__sfv_need_out_w 
            = (0x0000000000000500ULL | (0x0000000ffffff0ffULL 
                                        & vlSelfRef.milan_datapath__DOT__sfv_need_out_w));
    }
    if ((0x20000000U & vlSelfRef.milan_datapath__DOT__cmap_flat_w[8U])) {
        vlSelfRef.milan_datapath__DOT__sfv_need_out_w 
            = (0x0000000000000600ULL | (0x0000000ffffff0ffULL 
                                        & vlSelfRef.milan_datapath__DOT__sfv_need_out_w));
    }
    if ((0x00000400U & vlSelfRef.milan_datapath__DOT__cmap_flat_w[9U])) {
        vlSelfRef.milan_datapath__DOT__sfv_need_out_w 
            = (0x0000000000000700ULL | (0x0000000ffffff0ffULL 
                                        & vlSelfRef.milan_datapath__DOT__sfv_need_out_w));
    }
    if ((0x00800000U & vlSelfRef.milan_datapath__DOT__cmap_flat_w[9U])) {
        vlSelfRef.milan_datapath__DOT__sfv_need_out_w 
            = (0x0000000000000800ULL | (0x0000000ffffff0ffULL 
                                        & vlSelfRef.milan_datapath__DOT__sfv_need_out_w));
    }
    if ((0x00000010U & vlSelfRef.milan_datapath__DOT__cmap_flat_w[10U])) {
        vlSelfRef.milan_datapath__DOT__sfv_need_out_w 
            = (0x0000000000001000ULL | (0x0000000fffff0fffULL 
                                        & vlSelfRef.milan_datapath__DOT__sfv_need_out_w));
    }
    if ((0x00020000U & vlSelfRef.milan_datapath__DOT__cmap_flat_w[10U])) {
        vlSelfRef.milan_datapath__DOT__sfv_need_out_w 
            = (0x0000000000002000ULL | (0x0000000fffff0fffULL 
                                        & vlSelfRef.milan_datapath__DOT__sfv_need_out_w));
    }
    if ((0x40000000U & vlSelfRef.milan_datapath__DOT__cmap_flat_w[10U])) {
        vlSelfRef.milan_datapath__DOT__sfv_need_out_w 
            = (0x0000000000003000ULL | (0x0000000fffff0fffULL 
                                        & vlSelfRef.milan_datapath__DOT__sfv_need_out_w));
    }
    if ((0x00000800U & vlSelfRef.milan_datapath__DOT__cmap_flat_w[11U])) {
        vlSelfRef.milan_datapath__DOT__sfv_need_out_w 
            = (0x0000000000004000ULL | (0x0000000fffff0fffULL 
                                        & vlSelfRef.milan_datapath__DOT__sfv_need_out_w));
    }
    if ((0x01000000U & vlSelfRef.milan_datapath__DOT__cmap_flat_w[11U])) {
        vlSelfRef.milan_datapath__DOT__sfv_need_out_w 
            = (0x0000000000005000ULL | (0x0000000fffff0fffULL 
                                        & vlSelfRef.milan_datapath__DOT__sfv_need_out_w));
    }
    if ((0x00000020U & vlSelfRef.milan_datapath__DOT__cmap_flat_w[12U])) {
        vlSelfRef.milan_datapath__DOT__sfv_need_out_w 
            = (0x0000000000006000ULL | (0x0000000fffff0fffULL 
                                        & vlSelfRef.milan_datapath__DOT__sfv_need_out_w));
    }
    if ((0x00040000U & vlSelfRef.milan_datapath__DOT__cmap_flat_w[12U])) {
        vlSelfRef.milan_datapath__DOT__sfv_need_out_w 
            = (0x0000000000007000ULL | (0x0000000fffff0fffULL 
                                        & vlSelfRef.milan_datapath__DOT__sfv_need_out_w));
    }
    if ((vlSelfRef.milan_datapath__DOT__cmap_flat_w[12U] 
         >> 0x0000001fU)) {
        vlSelfRef.milan_datapath__DOT__sfv_need_out_w 
            = (0x0000000000008000ULL | (0x0000000fffff0fffULL 
                                        & vlSelfRef.milan_datapath__DOT__sfv_need_out_w));
    }
    if ((0x00001000U & vlSelfRef.milan_datapath__DOT__cmap_flat_w[13U])) {
        vlSelfRef.milan_datapath__DOT__sfv_need_out_w 
            = (0x0000000000010000ULL | (0x0000000ffff0ffffULL 
                                        & vlSelfRef.milan_datapath__DOT__sfv_need_out_w));
    }
    if ((0x02000000U & vlSelfRef.milan_datapath__DOT__cmap_flat_w[13U])) {
        vlSelfRef.milan_datapath__DOT__sfv_need_out_w 
            = (0x0000000000020000ULL | (0x0000000ffff0ffffULL 
                                        & vlSelfRef.milan_datapath__DOT__sfv_need_out_w));
    }
    if ((0x00000040U & vlSelfRef.milan_datapath__DOT__cmap_flat_w[14U])) {
        vlSelfRef.milan_datapath__DOT__sfv_need_out_w 
            = (0x0000000000030000ULL | (0x0000000ffff0ffffULL 
                                        & vlSelfRef.milan_datapath__DOT__sfv_need_out_w));
    }
    if ((0x00080000U & vlSelfRef.milan_datapath__DOT__cmap_flat_w[14U])) {
        vlSelfRef.milan_datapath__DOT__sfv_need_out_w 
            = (0x0000000000040000ULL | (0x0000000ffff0ffffULL 
                                        & vlSelfRef.milan_datapath__DOT__sfv_need_out_w));
    }
    if ((1U & vlSelfRef.milan_datapath__DOT__cmap_flat_w[15U])) {
        vlSelfRef.milan_datapath__DOT__sfv_need_out_w 
            = (0x0000000000050000ULL | (0x0000000ffff0ffffULL 
                                        & vlSelfRef.milan_datapath__DOT__sfv_need_out_w));
    }
    if ((0x00002000U & vlSelfRef.milan_datapath__DOT__cmap_flat_w[15U])) {
        vlSelfRef.milan_datapath__DOT__sfv_need_out_w 
            = (0x0000000000060000ULL | (0x0000000ffff0ffffULL 
                                        & vlSelfRef.milan_datapath__DOT__sfv_need_out_w));
    }
    if ((0x04000000U & vlSelfRef.milan_datapath__DOT__cmap_flat_w[15U])) {
        vlSelfRef.milan_datapath__DOT__sfv_need_out_w 
            = (0x0000000000070000ULL | (0x0000000ffff0ffffULL 
                                        & vlSelfRef.milan_datapath__DOT__sfv_need_out_w));
    }
    if ((0x00000080U & vlSelfRef.milan_datapath__DOT__cmap_flat_w[16U])) {
        vlSelfRef.milan_datapath__DOT__sfv_need_out_w 
            = (0x0000000000080000ULL | (0x0000000ffff0ffffULL 
                                        & vlSelfRef.milan_datapath__DOT__sfv_need_out_w));
    }
    if ((0x00100000U & vlSelfRef.milan_datapath__DOT__cmap_flat_w[16U])) {
        vlSelfRef.milan_datapath__DOT__sfv_need_out_w 
            = (0x0000000000100000ULL | (0x0000000fff0fffffULL 
                                        & vlSelfRef.milan_datapath__DOT__sfv_need_out_w));
    }
    if ((2U & vlSelfRef.milan_datapath__DOT__cmap_flat_w[17U])) {
        vlSelfRef.milan_datapath__DOT__sfv_need_out_w 
            = (0x0000000000200000ULL | (0x0000000fff0fffffULL 
                                        & vlSelfRef.milan_datapath__DOT__sfv_need_out_w));
    }
    if ((0x00004000U & vlSelfRef.milan_datapath__DOT__cmap_flat_w[17U])) {
        vlSelfRef.milan_datapath__DOT__sfv_need_out_w 
            = (0x0000000000300000ULL | (0x0000000fff0fffffULL 
                                        & vlSelfRef.milan_datapath__DOT__sfv_need_out_w));
    }
    if ((0x08000000U & vlSelfRef.milan_datapath__DOT__cmap_flat_w[17U])) {
        vlSelfRef.milan_datapath__DOT__sfv_need_out_w 
            = (0x0000000000400000ULL | (0x0000000fff0fffffULL 
                                        & vlSelfRef.milan_datapath__DOT__sfv_need_out_w));
    }
    if ((0x00000100U & vlSelfRef.milan_datapath__DOT__cmap_flat_w[18U])) {
        vlSelfRef.milan_datapath__DOT__sfv_need_out_w 
            = (0x0000000000500000ULL | (0x0000000fff0fffffULL 
                                        & vlSelfRef.milan_datapath__DOT__sfv_need_out_w));
    }
    if ((0x00200000U & vlSelfRef.milan_datapath__DOT__cmap_flat_w[18U])) {
        vlSelfRef.milan_datapath__DOT__sfv_need_out_w 
            = (0x0000000000600000ULL | (0x0000000fff0fffffULL 
                                        & vlSelfRef.milan_datapath__DOT__sfv_need_out_w));
    }
    if ((4U & vlSelfRef.milan_datapath__DOT__cmap_flat_w[19U])) {
        vlSelfRef.milan_datapath__DOT__sfv_need_out_w 
            = (0x0000000000700000ULL | (0x0000000fff0fffffULL 
                                        & vlSelfRef.milan_datapath__DOT__sfv_need_out_w));
    }
    if ((0x00008000U & vlSelfRef.milan_datapath__DOT__cmap_flat_w[19U])) {
        vlSelfRef.milan_datapath__DOT__sfv_need_out_w 
            = (0x0000000000800000ULL | (0x0000000fff0fffffULL 
                                        & vlSelfRef.milan_datapath__DOT__sfv_need_out_w));
    }
    if ((0x10000000U & vlSelfRef.milan_datapath__DOT__cmap_flat_w[19U])) {
        vlSelfRef.milan_datapath__DOT__sfv_need_out_w 
            = (0x0000000001000000ULL | (0x0000000ff0ffffffULL 
                                        & vlSelfRef.milan_datapath__DOT__sfv_need_out_w));
    }
    if ((0x00000200U & vlSelfRef.milan_datapath__DOT__cmap_flat_w[20U])) {
        vlSelfRef.milan_datapath__DOT__sfv_need_out_w 
            = (0x0000000002000000ULL | (0x0000000ff0ffffffULL 
                                        & vlSelfRef.milan_datapath__DOT__sfv_need_out_w));
    }
    if ((0x00400000U & vlSelfRef.milan_datapath__DOT__cmap_flat_w[20U])) {
        vlSelfRef.milan_datapath__DOT__sfv_need_out_w 
            = (0x0000000003000000ULL | (0x0000000ff0ffffffULL 
                                        & vlSelfRef.milan_datapath__DOT__sfv_need_out_w));
    }
    if ((8U & vlSelfRef.milan_datapath__DOT__cmap_flat_w[21U])) {
        vlSelfRef.milan_datapath__DOT__sfv_need_out_w 
            = (0x0000000004000000ULL | (0x0000000ff0ffffffULL 
                                        & vlSelfRef.milan_datapath__DOT__sfv_need_out_w));
    }
    if ((0x00010000U & vlSelfRef.milan_datapath__DOT__cmap_flat_w[21U])) {
        vlSelfRef.milan_datapath__DOT__sfv_need_out_w 
            = (0x0000000005000000ULL | (0x0000000ff0ffffffULL 
                                        & vlSelfRef.milan_datapath__DOT__sfv_need_out_w));
    }
    if ((0x20000000U & vlSelfRef.milan_datapath__DOT__cmap_flat_w[21U])) {
        vlSelfRef.milan_datapath__DOT__sfv_need_out_w 
            = (0x0000000006000000ULL | (0x0000000ff0ffffffULL 
                                        & vlSelfRef.milan_datapath__DOT__sfv_need_out_w));
    }
    if ((0x00000400U & vlSelfRef.milan_datapath__DOT__cmap_flat_w[22U])) {
        vlSelfRef.milan_datapath__DOT__sfv_need_out_w 
            = (0x0000000007000000ULL | (0x0000000ff0ffffffULL 
                                        & vlSelfRef.milan_datapath__DOT__sfv_need_out_w));
    }
    if ((0x00800000U & vlSelfRef.milan_datapath__DOT__cmap_flat_w[22U])) {
        vlSelfRef.milan_datapath__DOT__sfv_need_out_w 
            = (0x0000000008000000ULL | (0x0000000ff0ffffffULL 
                                        & vlSelfRef.milan_datapath__DOT__sfv_need_out_w));
    }
    if ((0x00000010U & vlSelfRef.milan_datapath__DOT__cmap_flat_w[23U])) {
        vlSelfRef.milan_datapath__DOT__sfv_need_out_w 
            = (0x0000000010000000ULL | (0x0000000f0fffffffULL 
                                        & vlSelfRef.milan_datapath__DOT__sfv_need_out_w));
    }
    if ((0x00020000U & vlSelfRef.milan_datapath__DOT__cmap_flat_w[23U])) {
        vlSelfRef.milan_datapath__DOT__sfv_need_out_w 
            = (0x0000000020000000ULL | (0x0000000f0fffffffULL 
                                        & vlSelfRef.milan_datapath__DOT__sfv_need_out_w));
    }
    if ((0x40000000U & vlSelfRef.milan_datapath__DOT__cmap_flat_w[23U])) {
        vlSelfRef.milan_datapath__DOT__sfv_need_out_w 
            = (0x0000000030000000ULL | (0x0000000f0fffffffULL 
                                        & vlSelfRef.milan_datapath__DOT__sfv_need_out_w));
    }
    if ((0x00000800U & vlSelfRef.milan_datapath__DOT__cmap_flat_w[24U])) {
        vlSelfRef.milan_datapath__DOT__sfv_need_out_w 
            = (0x0000000040000000ULL | (0x0000000f0fffffffULL 
                                        & vlSelfRef.milan_datapath__DOT__sfv_need_out_w));
    }
    if ((0x01000000U & vlSelfRef.milan_datapath__DOT__cmap_flat_w[24U])) {
        vlSelfRef.milan_datapath__DOT__sfv_need_out_w 
            = (0x0000000050000000ULL | (0x0000000f0fffffffULL 
                                        & vlSelfRef.milan_datapath__DOT__sfv_need_out_w));
    }
    if ((0x00000020U & vlSelfRef.milan_datapath__DOT__cmap_flat_w[25U])) {
        vlSelfRef.milan_datapath__DOT__sfv_need_out_w 
            = (0x0000000060000000ULL | (0x0000000f0fffffffULL 
                                        & vlSelfRef.milan_datapath__DOT__sfv_need_out_w));
    }
    if ((0x00040000U & vlSelfRef.milan_datapath__DOT__cmap_flat_w[25U])) {
        vlSelfRef.milan_datapath__DOT__sfv_need_out_w 
            = (0x0000000070000000ULL | (0x0000000f0fffffffULL 
                                        & vlSelfRef.milan_datapath__DOT__sfv_need_out_w));
    }
    if ((vlSelfRef.milan_datapath__DOT__cmap_flat_w[25U] 
         >> 0x0000001fU)) {
        vlSelfRef.milan_datapath__DOT__sfv_need_out_w 
            = (0x0000000080000000ULL | (0x0000000f0fffffffULL 
                                        & vlSelfRef.milan_datapath__DOT__sfv_need_out_w));
    }
    milan_datapath__DOT__csr_tctx_rd_addr_w = ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_245)
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
        = (((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_245) 
            | ((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rds_busy_r) 
               & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rds_dir_r))) 
           & ((3U == (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__est_r)) 
              | ((~ (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__grant_v_w)) 
                 & (0U == (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__est_r)))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__tix_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__ctrs_r) 
           | ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_r) 
              | ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_edit_r) 
                 | ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gstri_r) 
                    | ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gavb_r) 
                       | ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gsfmt_r) 
                          | ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gsrate_r) 
                             | ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gclks_r) 
                                | ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__setc_r) 
                                   | ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gctrl_r) 
                                      | ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__strm_r) 
                                         | ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_289) 
                                            | (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_45)))))))))))));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_290 = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gsfmt_r) 
                                                  | (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_289));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_release_merge__DOT__available_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_release_merge__DOT__request_w) 
           | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_release_merge__DOT__pending_r));
    vlSelfRef.milan_datapath__DOT__sfv_crf_row_w = 
        ((8U == (IData)(vlSelfRef.milan_datapath__DOT__gsiq_index_r)) 
         & ((IData)(vlSelfRef.milan_datapath__DOT__gsi_in_w) 
            | (IData)(vlSelfRef.milan_datapath__DOT__gsi_out_w)));
    vlSelfRef.milan_datapath__DOT__sfv_decl_w = ((IData)(vlSelfRef.milan_datapath__DOT__gsi_in_w)
                                                  ? vlSelfRef.milan_datapath__DOT__sfv_decl_in_w
                                                  : 
                                                 (vlSelfRef.milan_datapath__DOT__sfv_decl_out_w 
                                                  & (- (QData)((IData)(vlSelfRef.milan_datapath__DOT__gsi_out_w)))));
    vlSelfRef.milan_datapath__DOT__gsi_bnd_w = ((8U 
                                                 >= 
                                                 (0x0000000fU 
                                                  & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__desc_ix_r))) 
                                                & (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__bound_hold_r) 
                                                    >> 
                                                    (0x0000000fU 
                                                     & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__desc_ix_r))) 
                                                   & (IData)(vlSelfRef.milan_datapath__DOT__gsi_in_w)));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__start0_w 
        = ((0U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__st_r)) 
           & ((0U != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__cnt_msrp_r)) 
              & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_377)));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__accept_w 
        = ((0x22f0U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__etype_w)) 
           | (((0x00000180c200000eULL == vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__da_r) 
               & (0x22eaU == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__etype_w))) 
              | ((0x00000180c2000021ULL == vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__da_r) 
                 & (0x88f5U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__etype_w)))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__da_num_w 
        = (((QData)((IData)(((0x0000ff00U & ((IData)(vlSelfRef.s_axis_mac_rx_tdata) 
                                             << 8U)) 
                             | (0x000000ffU & (IData)(
                                                      (vlSelfRef.s_axis_mac_rx_tdata 
                                                       >> 8U)))))) 
            << 0x00000020U) | (QData)((IData)((((IData)(
                                                        (vlSelfRef.s_axis_mac_rx_tdata 
                                                         >> 0x00000010U)) 
                                                << 0x00000018U) 
                                               | ((0x00ff0000U 
                                                   & ((IData)(
                                                              (vlSelfRef.s_axis_mac_rx_tdata 
                                                               >> 0x00000018U)) 
                                                      << 0x00000010U)) 
                                                  | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__etype_w))))));
    if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_domain__DOT__q0_valid_r) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__enc_ev_value_w[0U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__enc_ev_value_w[1U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__enc_ev_value_w[2U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__enc_ev_value_w[3U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__enc_ev_value_w[4U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__enc_ev_value_w[5U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__enc_ev_value_w[6U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__enc_ev_value_w[7U] 
            = (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_domain__DOT__q0_val_r 
               << 0x00000010U);
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__enc_ev_value_w[8U] 
            = (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_domain__DOT__q0_val_r 
               >> 0x00000010U);
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__enc_ev_event_w 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_domain__DOT__q0_ev_r;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__enc_ev_type_w = 4U;
    } else if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__vlan_ev_valid_w) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__enc_ev_value_w[0U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__enc_ev_value_w[1U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__enc_ev_value_w[2U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__enc_ev_value_w[3U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__enc_ev_value_w[4U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__enc_ev_value_w[5U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__enc_ev_value_w[6U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__enc_ev_value_w[7U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__enc_ev_value_w[8U] 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__ev_vid_r;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__enc_ev_event_w 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__ev_code_r;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__enc_ev_type_w = 1U;
    } else if ((2U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__walk_r))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__enc_ev_value_w[0U] 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__push_val_r[0U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__enc_ev_value_w[1U] 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__push_val_r[1U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__enc_ev_value_w[2U] 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__push_val_r[2U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__enc_ev_value_w[3U] 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__push_val_r[3U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__enc_ev_value_w[4U] 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__push_val_r[4U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__enc_ev_value_w[5U] 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__push_val_r[5U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__enc_ev_value_w[6U] 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__push_val_r[6U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__enc_ev_value_w[7U] 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__push_val_r[7U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__enc_ev_value_w[8U] 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__push_val_r[8U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__enc_ev_event_w 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__push_code_r;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__enc_ev_type_w 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__push_type_r;
    } else if ((2U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__walk_r))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__enc_ev_value_w[0U] 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__push_val_r[0U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__enc_ev_value_w[1U] 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__push_val_r[1U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__enc_ev_value_w[2U] 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__push_val_r[2U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__enc_ev_value_w[3U] 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__push_val_r[3U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__enc_ev_value_w[4U] 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__push_val_r[4U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__enc_ev_value_w[5U] 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__push_val_r[5U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__enc_ev_value_w[6U] 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__push_val_r[6U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__enc_ev_value_w[7U] 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__push_val_r[7U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__enc_ev_value_w[8U] 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__push_val_r[8U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__enc_ev_event_w 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__push_code_r;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__enc_ev_type_w = 3U;
    } else {
        VL_ASSIGN_W(272, vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__enc_ev_value_w, Vmilan_datapath__ConstPool__CONST_hc5471b50_0);
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__enc_ev_event_w = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__enc_ev_type_w = 0U;
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__enc_ev_valid_w = 1U;
    if ((1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_domain__DOT__q0_valid_r)))) {
        if ((1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__vlan_ev_valid_w)))) {
            if ((2U != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__walk_r))) {
                if ((2U != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__walk_r))) {
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__enc_ev_valid_w = 0U;
                }
            }
        }
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__enc_ev_app_w 
        = ((1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_domain__DOT__q0_valid_r))) 
           && (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__vlan_ev_valid_w));
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__urb_we_w = 0U;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__is_q_field_w 
        = (IData)((((0x0000000030000000ULL == (0x0000000070000000ULL 
                                               & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__uop_e_r)) 
                    & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__append_skip_w))) 
                   & ((0x14U == (0x0000001fU & (IData)(
                                                       (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__uop_e_r 
                                                        >> 0x0000002bU)))) 
                      | (0x1bU == (0x0000001fU & (IData)(
                                                         (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__uop_e_r 
                                                          >> 0x0000002bU)))))));
    vlSelfRef.milan_datapath__DOT__csr_lctx_rd_addr_w 
        = ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_271)
            ? ((0x000000e0U & ((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__snap_idx_r) 
                               << 5U)) | (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__snap_word_r))
            : (((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rds_idx_r) 
                << 5U) | (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rds_word_r)));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_to_maap_w = 0U;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_maap_rel_w = 0U;
    if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_code_r))) {
        if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_code_r))) {
            if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_code_r))) {
                if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__maap_avail_w) {
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_to_maap_w = 1U;
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_maap_rel_w = 1U;
                }
            } else if ((0U == (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__rec_q_r[2U] 
                                     >> 0x00000012U)))) {
                if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__maap_avail_w) {
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_to_maap_w = 1U;
                }
            }
        }
    } else if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_code_r) 
                         >> 1U)))) {
        if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_code_r))) {
            if (((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__rec_q_r[2U] 
                  >> 0x00000011U) & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__maap_avail_w))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_to_maap_w = 1U;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_maap_rel_w = 1U;
            }
        }
    }
    vlSelfRef.milan_datapath__DOT__pp_restore_busy_w 
        = ((8U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__hs_r)) 
           | (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_402));
    milan_datapath__DOT__avtp_rx_monitor__DOT__eng_wdata_w = 0U;
    vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__eng_waddr_w = 0U;
    if ((4U == (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__mst_r))) {
        if ((0U == (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__wrph_r))) {
            milan_datapath__DOT__avtp_rx_monitor__DOT__eng_wdata_w 
                = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__monst_r;
            vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__241__s 
                = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ev_s_r;
            vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__241__Vfuncout 
                = (8U | ((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__241__s) 
                         << 5U));
            vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__eng_waddr_w 
                = vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__241__Vfuncout;
        } else if ((1U == (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__wrph_r))) {
            milan_datapath__DOT__avtp_rx_monitor__DOT__eng_wdata_w 
                = ((vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__cur_r[4U] 
                    << 0x0000001eU) | (vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__cur_r[3U] 
                                       >> 2U));
            vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__242__s 
                = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ev_s_r;
            vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__242__Vfuncout 
                = (9U | ((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__242__s) 
                         << 5U));
            vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__eng_waddr_w 
                = vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__242__Vfuncout;
        } else {
            milan_datapath__DOT__avtp_rx_monitor__DOT__eng_wdata_w 
                = ((vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__cur_r[1U] 
                    << 0x0000001eU) | (vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__cur_r[0U] 
                                       >> 2U));
            vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__243__s 
                = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ev_s_r;
            vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__243__Vfuncout 
                = (0x0aU | ((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__243__s) 
                            << 5U));
            vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__eng_waddr_w 
                = vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__243__Vfuncout;
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
                vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__244__s 
                    = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ev_s_r;
                vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__244__Vfuncout 
                    = (0x0bU | ((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__244__s) 
                                << 5U));
                vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__eng_waddr_w 
                    = vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__244__Vfuncout;
            }
        } else if (vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__sil_mode_r) {
            if ((1U == (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__wrph_r))) {
                milan_datapath__DOT__avtp_rx_monitor__DOT__eng_wdata_w 
                    = ((IData)(1U) + vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ram_q_r);
                vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__245__s 
                    = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ev_s_r;
                vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__245__Vfuncout 
                    = (0x11U | ((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__245__s) 
                                << 5U));
                vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__eng_waddr_w 
                    = vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__245__Vfuncout;
            } else if ((3U == (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__wrph_r))) {
                milan_datapath__DOT__avtp_rx_monitor__DOT__eng_wdata_w 
                    = (0xffffefffU & vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ram_q_r);
                vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__246__s 
                    = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ev_s_r;
                vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__246__Vfuncout 
                    = (8U | ((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__246__s) 
                             << 5U));
                vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__eng_waddr_w 
                    = vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__246__Vfuncout;
            }
        } else if (vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__bind_zero_r) {
            milan_datapath__DOT__avtp_rx_monitor__DOT__eng_wdata_w = 0U;
            vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__247__w 
                = (0x10U | (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__zero_idx_r));
            vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__247__s 
                = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ev_s_r;
            vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__247__Vfuncout 
                = (((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__247__s) 
                    << 5U) | (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__247__w));
            vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__eng_waddr_w 
                = vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__247__Vfuncout;
        } else if (((0U != (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__inc_list_r)) 
                    & (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__inc_rd_q_r))) {
            milan_datapath__DOT__avtp_rx_monitor__DOT__eng_wdata_w 
                = (vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ram_q_r 
                   + ((9U == (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__inc_next_w))
                       ? (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__frx_add_r)
                       : 1U));
            vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__248__w 
                = (0x10U | (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__inc_next_w));
            vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__248__s 
                = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ev_s_r;
            vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__248__Vfuncout 
                = (((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__248__s) 
                    << 5U) | (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__248__w));
            vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__eng_waddr_w 
                = vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__248__Vfuncout;
        }
    } else if ((7U == (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__mst_r))) {
        if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__wrph_r) 
                      >> 3U)))) {
            if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__wrph_r))) {
                if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__wrph_r) 
                              >> 1U)))) {
                    if ((1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__wrph_r)))) {
                        milan_datapath__DOT__avtp_rx_monitor__DOT__eng_wdata_w 
                            = (IData)((vlSelfRef.milan_datapath__DOT__aecp_in0_fmt 
                                       >> 0x20U));
                        vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__249__s 
                            = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ev_s_r;
                        vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__249__Vfuncout 
                            = (3U | ((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__249__s) 
                                     << 5U));
                        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__eng_waddr_w 
                            = vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__249__Vfuncout;
                    }
                }
            } else if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__wrph_r))) {
                if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__wrph_r))) {
                    milan_datapath__DOT__avtp_rx_monitor__DOT__eng_wdata_w 
                        = (IData)(vlSelfRef.milan_datapath__DOT__aecp_in0_fmt);
                    vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__250__s 
                        = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ev_s_r;
                    vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__250__Vfuncout 
                        = (2U | ((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__250__s) 
                                 << 5U));
                    vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__eng_waddr_w 
                        = vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__250__Vfuncout;
                } else {
                    milan_datapath__DOT__avtp_rx_monitor__DOT__eng_wdata_w 
                        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__bound_sid_r[1U];
                    vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__251__s 
                        = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ev_s_r;
                    vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__251__Vfuncout 
                        = (1U | ((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__251__s) 
                                 << 5U));
                    vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__eng_waddr_w 
                        = vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__251__Vfuncout;
                }
            } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__wrph_r))) {
                milan_datapath__DOT__avtp_rx_monitor__DOT__eng_wdata_w 
                    = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__bound_sid_r[0U];
                vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__252__s 
                    = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ev_s_r;
                vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__252__Vfuncout 
                    = ((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__252__s) 
                       << 5U);
                vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__eng_waddr_w 
                    = vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__252__Vfuncout;
            } else {
                milan_datapath__DOT__avtp_rx_monitor__DOT__eng_wdata_w 
                    = (0xff3fc0ffU & vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ram_q_r);
                vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__253__s 
                    = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ev_s_r;
                vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__253__Vfuncout 
                    = (8U | ((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__253__s) 
                             << 5U));
                vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__eng_waddr_w 
                    = vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__253__Vfuncout;
            }
        }
    }
    vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__stg_drain_w 
        = (1U & (~ (((IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__fill_w) 
                     >> 9U) | (0U == (IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__stg_cnt_r)))));
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
    vlSelfRef.milan_datapath__DOT__pp_ctr_word_w = 
        ((0x00000080U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gx_sel_w))
          ? 0x20U : ((0x0000001cU & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gx_sel_w) 
                                     >> 2U)) | (3U 
                                                & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gx_sel_w))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__strm_state_w 
        = (IData)(((0xd0U == (0xf0U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gx_sel_w))) 
                   & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__strt_r) 
                      | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__stop_r))));
    vlSelfRef.milan_datapath__DOT__pp_amap_sel_w = 
        ((0x00000010U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gx_sel_w))
          ? 2U : (1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gx_sel_w)));
    vlSelfRef.milan_datapath__DOT__pp_amap_edit_phase_w 
        = (7U & Vmilan_datapath__ConstPool__CONST_hc13a5b68_0
           [(0x07ffffffU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gx_sel_w))]);
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
    __VdfgRegularize_h6e95ff9d_0_448 = ((IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__sched_r) 
                                        & ((~ (IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__prefill_pop_w)) 
                                           & (0U == (IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__beat_r))));
    vlSelfRef.milan_datapath__DOT__crf_dp_mux__DOT__src_tvalid_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__crf_dp_mux__DOT__gsel)
            ? (IData)(vlSelfRef.milan_datapath__DOT__crf_tx__DOT__st_r)
            : (3U == (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__est_r)));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_449 = (0x000001ffU 
                                                  & ((0x000001fcU 
                                                      & ((vlSelfRef.__VdfgRegularize_h6e95ff9d_0_435 
                                                          + 
                                                          (0x0000000fU 
                                                           & ((IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__wptr_in_w) 
                                                              >> 1U))) 
                                                         << 2U)) 
                                                     + 
                                                     (7U 
                                                      & ((IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__chpos_r) 
                                                         >> 1U))));
    vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__rd_row_w 
        = (0x0000001fU & ((0U == (IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__beat_r))
                           ? (IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__rptr_pop_w)
                           : (IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__ev_row_r)));
    milan_datapath__DOT__render_setpoint__DOT__fill_pop_w 
        = (0x0000003fU & ((IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__wptr_pop_w) 
                          - (IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__rptr_pop_w)));
    vlSelfRef.milan_datapath__DOT__aprb_regs_w[0U] 
        = vlSelfRef.milan_datapath__DOT__aprb_parsed_w;
    vlSelfRef.milan_datapath__DOT__aprb_regs_w[1U] 
        = vlSelfRef.milan_datapath__DOT__aprb_matched_w;
    vlSelfRef.milan_datapath__DOT__aprb_regs_w[2U] 
        = (IData)(vlSelfRef.milan_datapath__DOT__g_aprb__DOT__aprb_sid_r);
    vlSelfRef.milan_datapath__DOT__aprb_regs_w[3U] 
        = (IData)((vlSelfRef.milan_datapath__DOT__g_aprb__DOT__aprb_sid_r 
                   >> 0x00000020U));
    vlSelfRef.milan_datapath__DOT__aprb_regs_w[4U] 
        = ((0x00ff0000U & (VL_COUNTONES_I((IData)(vlSelfRef.milan_datapath__DOT__strtbl_en_w)) 
                           << 0x00000010U)) | ((((IData)(vlSelfRef.milan_datapath__DOT__g_aprb__DOT__aprb_idx_r) 
                                                 << 9U) 
                                                | ((IData)(vlSelfRef.milan_datapath__DOT__g_aprb__DOT__aprb_hit_r) 
                                                   << 8U)) 
                                               | (IData)(vlSelfRef.milan_datapath__DOT__g_aprb__DOT__aprb_subtype_r)));
    vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__penq_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__avtprx_match) 
           & (((IData)(vlSelfRef.milan_datapath__DOT__strtbl_en_w) 
               >> (IData)(vlSelfRef.milan_datapath__DOT__avtprx_idx)) 
              & (2U != (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__pq_cnt_r))));
    if (vlSelfRef.__VdfgRegularize_h6e95ff9d_0_222) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__line_raddr_w 
            = (0x0000007fU & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__patch_abs_byte_w) 
                              >> 3U));
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__name_raddr_w 
            = (0x000003ffU & ((0x0000ffffU & (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__desc_nbase_r) 
                                               + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__patch_name_r)) 
                                              << 3U)) 
                              + (7U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__patch_byte_r) 
                                       >> 3U))));
    } else {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__line_raddr_w 
            = (0x0000007fU & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__st_addr_w 
                              >> 3U));
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__name_raddr_w 
            = (0x000003ffU & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__st_addr_w 
                              >> 3U));
    }
    __Vtemp_8 = VL_MATCHMASKED_I(13, (0x00001fffU & 
                                      (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__st_addr_w 
                                       >> 3U)), Vmilan_datapath__ConstPool__CONST_h88ed57bb_0);
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__in_range_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT____Vcellinp__u_dyn__desc_index_i) 
           < Vmilan_datapath__ConstPool__TABLE_h42b7b3b2_0
           [__Vtemp_8]);
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__strq_sel_w 
        = (((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__st_name_w)) 
            & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__st_we_w)) 
           & (0x00030000U == (0x000f0000U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__st_addr_w)));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__dyn_sel_w 
        = ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__st_name_w)) 
           & ((1U == (0x0000000fU & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__st_addr_w 
                                     >> 0x00000010U))) 
              | (2U == (0x0000000fU & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__st_addr_w 
                                       >> 0x00000010U)))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__st_set_w = 0U;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__rec_wr_en_w = 0U;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__st_clr_w = 0U;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__ev_disc_w = 0U;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__iter_arm_w = 0U;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__iter_cancel_w = 0U;
    if ((4U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__rx_st_r))) {
        if ((0U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__rxq_msg_r))) {
            if ((1U & (~ ((8U >= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__sink_r)) 
                          && (1U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__disc_st_r) 
                                    >> (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__sink_r))))))) {
                if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__gm_dom_ok_w) {
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__st_set_w = 1U;
                }
            }
            if (((8U >= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__sink_r)) 
                 && (1U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__disc_st_r) 
                           >> (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__sink_r))))) {
                if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__rx_ifx_r) 
                     == (0x0000ffffU & (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__disc_rec_q_r 
                                                >> 0x00000020U))))) {
                    if ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__rx_aidx_r 
                         > (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__disc_rec_q_r))) {
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__rec_wr_en_w = 1U;
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__iter_arm_w = 1U;
                    } else if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__gm_dom_ok_w) {
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__rec_wr_en_w = 1U;
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__iter_arm_w = 1U;
                    }
                    if ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__rx_aidx_r 
                         <= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__disc_rec_q_r))) {
                        if ((1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__gm_dom_ok_w)))) {
                            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__st_clr_w = 1U;
                            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__iter_cancel_w = 1U;
                        }
                        if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__gm_dom_ok_w) {
                            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__ev_disc_w = 1U;
                        }
                    }
                }
            } else if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__gm_dom_ok_w) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__rec_wr_en_w = 1U;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__ev_disc_w = 1U;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__iter_arm_w = 1U;
            }
        } else if ((1U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__rxq_msg_r))) {
            if ((((8U >= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__sink_r)) 
                  && (1U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__disc_st_r) 
                            >> (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__sink_r)))) 
                 & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__rx_ifx_r) 
                    == (0x0000ffffU & (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__disc_rec_q_r 
                                               >> 0x00000020U)))))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__st_clr_w = 1U;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__iter_cancel_w = 1U;
            }
        }
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__evr_payload_w[0U] 
        = (0x00010000U | (((2U == (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_270)) 
                           << 0x0000001fU) | ((2U == (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_121)) 
                                              << 0x0000000fU)));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__evr_payload_w[1U] 
        = (0x00030002U | (((2U == (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_268)) 
                           << 0x0000001fU) | ((2U == (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_269)) 
                                              << 0x0000000fU)));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__evr_payload_w[2U] 
        = (0x00050004U | (((2U == (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_266)) 
                           << 0x0000001fU) | ((2U == (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_267)) 
                                              << 0x0000000fU)));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__evr_payload_w[3U] 
        = (0x00070006U | (((2U == (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_264)) 
                           << 0x0000001fU) | ((2U == (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_265)) 
                                              << 0x0000000fU)));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__evr_payload_w[4U] 
        = (8U | ((2U == (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_263)) 
                 << 0x0000000fU));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__evr_payload_w[5U] = 0x00020001U;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__evr_payload_w[6U] = 0x00040003U;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__evr_payload_w[7U] = 0x00060005U;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__evr_payload_w[8U] = 0x00080007U;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__evr_payload_w[9U] 
        = (IData)((((QData)((IData)(((0x0fff0000U & 
                                      ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_domain__DOT__decl_vid_r) 
                                       << 0x00000010U)) 
                                     | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__adp_evt_sink_w)))) 
                    << 0x00000010U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__adp_evt_sink_w))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__evr_payload_w[10U] 
        = ((0xffff0000U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__evr_payload_w[10U]) 
           | (IData)(((((QData)((IData)(((0x0fff0000U 
                                          & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_domain__DOT__decl_vid_r) 
                                             << 0x00000010U)) 
                                         | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__adp_evt_sink_w)))) 
                        << 0x00000010U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__adp_evt_sink_w))) 
                      >> 0x00000020U)));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__evr_payload_w[10U] 
        = (0x0000ffffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__evr_payload_w[10U]);
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__evr_payload_w[11U] = 0x00020001U;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__evr_payload_w[12U] = 0x00040003U;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__evr_payload_w[13U] = 0x00060005U;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__evr_payload_w[14U] = 0x00080007U;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__evr_payload_w[15U] 
        = ((IData)(vlSelfRef.milan_datapath__DOT__eff_link_w) 
           << 0x00000010U);
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_tk_reg_state_w 
        = ((((((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_263) 
               << 6U) | ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_264) 
                         << 4U)) | (((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_265) 
                                     << 2U) | (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_266))) 
            << 0x0000000aU) | ((((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_267) 
                                 << 8U) | ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_268) 
                                           << 6U)) 
                               | (((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_269) 
                                   << 4U) | (((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_270) 
                                              << 2U) 
                                             | (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_121)))));
    vlSelfRef.milan_datapath__DOT__lwsrp_ta_fail_code 
        = (0x000000ffU & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__fcode_r[0U] 
                          & (- (IData)((2U == (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_121))))));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_122 = ((
                                                   (0x00000080U 
                                                    & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__fail_r))
                                                    ? 2U
                                                    : 1U) 
                                                  & (- (IData)((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_111))));
    vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_tready_pipe 
        = ((0U == (IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__rstate_r)) 
           | ((2U == (IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__rstate_r)) 
              | ((1U == (IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__rstate_r)) 
                 & (~ (IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__hold_only_w)))));
    vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__emit_w 
        = ((1U == (IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__rstate_r)) 
           & ((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__hold_only_w) 
              | ((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_tvalid_pipe_reg) 
                 >> 1U)));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_123 = ((
                                                   (0x00000040U 
                                                    & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__fail_r))
                                                    ? 2U
                                                    : 1U) 
                                                  & (- (IData)((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_110))));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_124 = ((
                                                   (0x00000020U 
                                                    & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__fail_r))
                                                    ? 2U
                                                    : 1U) 
                                                  & (- (IData)((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_109))));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_125 = ((
                                                   (0x00000010U 
                                                    & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__fail_r))
                                                    ? 2U
                                                    : 1U) 
                                                  & (- (IData)((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_108))));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_126 = ((
                                                   (8U 
                                                    & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__fail_r))
                                                    ? 2U
                                                    : 1U) 
                                                  & (- (IData)((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_107))));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_127 = ((
                                                   (4U 
                                                    & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__fail_r))
                                                    ? 2U
                                                    : 1U) 
                                                  & (- (IData)((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_106))));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_128 = ((
                                                   (2U 
                                                    & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__fail_r))
                                                    ? 2U
                                                    : 1U) 
                                                  & (- (IData)((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_105))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__hit_ix_w = 0U;
    if (((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__valid_r) 
           >> 3U) & (0U == ((((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__key_r[3U][0U] 
                               ^ vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT____Vcellinp__u_originator__rsp_key_i[0U]) 
                              | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__key_r[3U][1U] 
                                 ^ vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT____Vcellinp__u_originator__rsp_key_i[1U])) 
                             | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__key_r[3U][2U] 
                                ^ vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT____Vcellinp__u_originator__rsp_key_i[2U])) 
                            | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__key_r[3U][3U] 
                               ^ vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT____Vcellinp__u_originator__rsp_key_i[3U])))) 
         & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__seq_r[3U] 
            == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__hdr_seq_r)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__hit_ix_w = 3U;
    }
    if (((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__valid_r) 
           >> 2U) & (0U == ((((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__key_r[2U][0U] 
                               ^ vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT____Vcellinp__u_originator__rsp_key_i[0U]) 
                              | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__key_r[2U][1U] 
                                 ^ vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT____Vcellinp__u_originator__rsp_key_i[1U])) 
                             | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__key_r[2U][2U] 
                                ^ vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT____Vcellinp__u_originator__rsp_key_i[2U])) 
                            | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__key_r[2U][3U] 
                               ^ vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT____Vcellinp__u_originator__rsp_key_i[3U])))) 
         & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__seq_r[2U] 
            == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__hdr_seq_r)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__hit_ix_w = 2U;
    }
    if (((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__valid_r) 
           >> 1U) & (0U == ((((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__key_r[1U][0U] 
                               ^ vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT____Vcellinp__u_originator__rsp_key_i[0U]) 
                              | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__key_r[1U][1U] 
                                 ^ vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT____Vcellinp__u_originator__rsp_key_i[1U])) 
                             | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__key_r[1U][2U] 
                                ^ vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT____Vcellinp__u_originator__rsp_key_i[2U])) 
                            | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__key_r[1U][3U] 
                               ^ vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT____Vcellinp__u_originator__rsp_key_i[3U])))) 
         & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__seq_r[1U] 
            == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__hdr_seq_r)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__hit_ix_w = 1U;
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__hit_ok_w = 0U;
    if (((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__valid_r) 
           >> 3U) & (0U == ((((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__key_r[3U][0U] 
                               ^ vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT____Vcellinp__u_originator__rsp_key_i[0U]) 
                              | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__key_r[3U][1U] 
                                 ^ vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT____Vcellinp__u_originator__rsp_key_i[1U])) 
                             | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__key_r[3U][2U] 
                                ^ vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT____Vcellinp__u_originator__rsp_key_i[2U])) 
                            | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__key_r[3U][3U] 
                               ^ vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT____Vcellinp__u_originator__rsp_key_i[3U])))) 
         & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__seq_r[3U] 
            == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__hdr_seq_r)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__hit_ok_w = 1U;
    }
    if (((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__valid_r) 
           >> 2U) & (0U == ((((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__key_r[2U][0U] 
                               ^ vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT____Vcellinp__u_originator__rsp_key_i[0U]) 
                              | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__key_r[2U][1U] 
                                 ^ vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT____Vcellinp__u_originator__rsp_key_i[1U])) 
                             | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__key_r[2U][2U] 
                                ^ vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT____Vcellinp__u_originator__rsp_key_i[2U])) 
                            | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__key_r[2U][3U] 
                               ^ vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT____Vcellinp__u_originator__rsp_key_i[3U])))) 
         & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__seq_r[2U] 
            == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__hdr_seq_r)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__hit_ok_w = 1U;
    }
    if (((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__valid_r) 
           >> 1U) & (0U == ((((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__key_r[1U][0U] 
                               ^ vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT____Vcellinp__u_originator__rsp_key_i[0U]) 
                              | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__key_r[1U][1U] 
                                 ^ vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT____Vcellinp__u_originator__rsp_key_i[1U])) 
                             | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__key_r[1U][2U] 
                                ^ vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT____Vcellinp__u_originator__rsp_key_i[2U])) 
                            | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__key_r[1U][3U] 
                               ^ vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT____Vcellinp__u_originator__rsp_key_i[3U])))) 
         & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__seq_r[1U] 
            == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__hdr_seq_r)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__hit_ok_w = 1U;
    }
    if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__valid_r) 
          & (0U == ((((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__key_r[0U][0U] 
                       ^ vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT____Vcellinp__u_originator__rsp_key_i[0U]) 
                      | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__key_r[0U][1U] 
                         ^ vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT____Vcellinp__u_originator__rsp_key_i[1U])) 
                     | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__key_r[0U][2U] 
                        ^ vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT____Vcellinp__u_originator__rsp_key_i[2U])) 
                    | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__key_r[0U][3U] 
                       ^ vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT____Vcellinp__u_originator__rsp_key_i[3U])))) 
         & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__seq_r[0U] 
            == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__hdr_seq_r)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__hit_ix_w = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__hit_ok_w = 1U;
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__sh_hdr_w[0U] 
        = (0x22f0U | ((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w) 
                      << 0x00000010U));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__sh_hdr_w[1U] 
        = (((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w) 
            >> 0x00000010U) | ((IData)((vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w 
                                        >> 0x00000020U)) 
                               << 0x00000010U));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__sh_hdr_w[2U] 
        = (0xf0010000U | ((IData)((vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w 
                                   >> 0x00000020U)) 
                          >> 0x00000010U));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__sh_hdr_w[3U] = 0x000091e0U;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__da_own_a_w 
        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__da_own_r;
    if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__ser_busy_r) 
          & (0U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__fr_st_r))) 
         & (5U >= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__idx_r)))) {
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__mac_byte_f__135__i 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__idx_r;
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__mac_byte_f__135__k 
            = ((5U < (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__mac_byte_f__135__i))
                ? 0U : ((IData)(5U) - (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__mac_byte_f__135__i)));
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT____VlemCall_1__mac_byte_f 
            = ((0x2fU >= (0x0000003fU & (vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__mac_byte_f__135__k 
                                         << 3U))) ? 
               (0x000000ffU & (IData)((0x000091e0f0010000ULL 
                                       >> (0x0000003fU 
                                           & (vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__mac_byte_f__135__k 
                                              << 3U)))))
                : 0U);
        if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__pp_rx_data_w) 
             != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT____VlemCall_1__mac_byte_f))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__da_mcast_a_w = 0U;
        }
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__mac_byte_f__136__i 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__idx_r;
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__mac_byte_f__136__k 
            = ((5U < (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__mac_byte_f__136__i))
                ? 0U : ((IData)(5U) - (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__mac_byte_f__136__i)));
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT____VlemCall_2__mac_byte_f 
            = ((0x2fU >= (0x0000003fU & (vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__mac_byte_f__136__k 
                                         << 3U))) ? 
               (0x000000ffU & (IData)((0x000091e0f000ff00ULL 
                                       >> (0x0000003fU 
                                           & (vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__mac_byte_f__136__k 
                                              << 3U)))))
                : 0U);
        if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__pp_rx_data_w) 
             != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT____VlemCall_2__mac_byte_f))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__da_maap_a_w = 0U;
        }
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__mac_byte_f__137__i 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__idx_r;
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__mac_byte_f__137__k 
            = ((5U < (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__mac_byte_f__137__i))
                ? 0U : ((IData)(5U) - (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__mac_byte_f__137__i)));
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT____VlemCall_3__mac_byte_f 
            = ((0x2fU >= (0x0000003fU & (vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__mac_byte_f__137__k 
                                         << 3U))) ? 
               (0x000000ffU & (IData)((0x00000180c200000eULL 
                                       >> (0x0000003fU 
                                           & (vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__mac_byte_f__137__k 
                                              << 3U)))))
                : 0U);
        if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__pp_rx_data_w) 
             != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT____VlemCall_3__mac_byte_f))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__da_msrp_a_w = 0U;
        }
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__mac_byte_f__138__i 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__idx_r;
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__mac_byte_f__138__k 
            = ((5U < (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__mac_byte_f__138__i))
                ? 0U : ((IData)(5U) - (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__mac_byte_f__138__i)));
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT____VlemCall_4__mac_byte_f 
            = ((0x2fU >= (0x0000003fU & (vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__mac_byte_f__138__k 
                                         << 3U))) ? 
               (0x000000ffU & (IData)((0x00000180c2000021ULL 
                                       >> (0x0000003fU 
                                           & (vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__mac_byte_f__138__k 
                                              << 3U)))))
                : 0U);
        if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__pp_rx_data_w) 
             != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT____VlemCall_4__mac_byte_f))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__da_mvrp_a_w = 0U;
        }
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__mac_byte_f__134__i 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__idx_r;
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__mac_byte_f__134__m 
            = vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w;
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__mac_byte_f__134__k 
            = ((5U < (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__mac_byte_f__134__i))
                ? 0U : ((IData)(5U) - (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__mac_byte_f__134__i)));
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT____VlemCall_0__mac_byte_f 
            = ((0x2fU >= (0x0000003fU & (vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__mac_byte_f__134__k 
                                         << 3U))) ? 
               (0x000000ffU & (IData)((vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__mac_byte_f__134__m 
                                       >> (0x0000003fU 
                                           & (vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__mac_byte_f__134__k 
                                              << 3U)))))
                : 0U);
        if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__pp_rx_data_w) 
             != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT____VlemCall_0__mac_byte_f))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__da_own_a_w = 0U;
        }
    }
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__189__b 
        = vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat_r;
    for (int __Vi0 = 0; __Vi0 < 64; ++__Vi0) {
        __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__189__f[__Vi0] = 0;
    }
    __Vilp1 = 0U;
    while ((__Vilp1 <= 0x0000003fU)) {
        __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__189__f[__Vilp1] = 0U;
        __Vilp1 = ((IData)(1U) + __Vilp1);
    }
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__189__f[0U] = 0x91U;
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__189__f[1U] = 0xe0U;
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__189__f[2U] = 0xf0U;
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__189__f[3U] = 0U;
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__189__f[4U] = 0xffU;
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__189__f[5U] = 0U;
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__189__f[6U] 
        = (0x000000ffU & (IData)((vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w 
                                  >> 0x00000028U)));
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__189__f[7U] 
        = (0x000000ffU & (IData)((vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w 
                                  >> 0x00000020U)));
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__189__f[8U] 
        = (0x000000ffU & (IData)((vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w 
                                  >> 0x00000018U)));
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__189__f[9U] 
        = (0x000000ffU & (IData)((vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w 
                                  >> 0x00000010U)));
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__189__f[10U] 
        = (0x000000ffU & (IData)((vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w 
                                  >> 8U)));
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__189__f[11U] 
        = (0x000000ffU & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w));
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__189__f[12U] = 0x22U;
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__189__f[13U] = 0xf0U;
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__189__f[14U] = 0xfeU;
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__189__f[15U] 
        = vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_msg_r;
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__189__f[16U] = 8U;
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__189__f[17U] = 0x1cU;
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__189__f[26U] = 0x91U;
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__189__f[27U] = 0xe0U;
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__189__f[28U] = 0xf0U;
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__189__f[29U] = 0U;
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__189__f[30U] 
        = (0x000000ffU & ((IData)(vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__offset_r) 
                          >> 8U));
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__189__f[31U] 
        = (0x000000ffU & (IData)(vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__offset_r));
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__189__f[32U] = 0U;
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__189__f[33U] 
        = (0x000000ffU & (vlSelfRef.milan_datapath__DOT__csr__DOT__maap_ctrl 
                          >> 8U));
    if ((2U == (IData)(vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_msg_r))) {
        __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__189__f[34U] = 0x91U;
        __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__189__f[35U] = 0xe0U;
        __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__189__f[36U] = 0xf0U;
        __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__189__f[37U] = 0U;
        __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__189__f[38U] 
            = (0x000000ffU & ((IData)(vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_conf_start_r) 
                              >> 8U));
        __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__189__f[39U] 
            = (0x000000ffU & (IData)(vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_conf_start_r));
        __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__189__f[40U] 
            = (0x000000ffU & ((IData)(vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_conf_cnt_r) 
                              >> 8U));
        __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__189__f[41U] 
            = (0x000000ffU & (IData)(vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_conf_cnt_r));
    }
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__189__Vfuncout 
        = (((QData)((IData)((((((IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__189__f
                                        [(7U | ((IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__189__b) 
                                                << 3U))]) 
                                << 8U) | __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__189__f
                               [(6U | ((IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__189__b) 
                                       << 3U))]) << 0x00000010U) 
                             | (((IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__189__f
                                         [(5U | ((IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__189__b) 
                                                 << 3U))]) 
                                 << 8U) | __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__189__f
                                [(4U | ((IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__189__b) 
                                        << 3U))])))) 
            << 0x00000020U) | (QData)((IData)((((((IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__189__f
                                                          [
                                                          (3U 
                                                           | ((IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__189__b) 
                                                              << 3U))]) 
                                                  << 8U) 
                                                 | __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__189__f
                                                 [(2U 
                                                   | ((IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__189__b) 
                                                      << 3U))]) 
                                                << 0x00000010U) 
                                               | (((IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__189__f
                                                           [
                                                           (1U 
                                                            | ((IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__189__b) 
                                                               << 3U))]) 
                                                   << 8U) 
                                                  | __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__189__f
                                                  [
                                                  ((IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__189__b) 
                                                   << 3U)])))));
    vlSelfRef.milan_datapath__DOT__maap_tx_tdata = __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__189__Vfuncout;
    milan_datapath__DOT__aaf_packetizer__DOT__stream_id_w 
        = ((vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w 
            << 0x00000010U) | (QData)((IData)((((0U 
                                                 != (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__euid_r))
                                                 ? (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__euid_r)
                                                 : (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__et_r)) 
                                               & (- (IData)(
                                                            (0U 
                                                             != (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__et_r))))))));
    vlSelfRef.milan_datapath__DOT__eff_crft_sid_w = 
        ((0U != vlSelfRef.milan_datapath__DOT__cfg_crft_sid)
          ? vlSelfRef.milan_datapath__DOT__cfg_crft_sid
          : (8ULL | (vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w 
                     << 0x00000010U)));
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__75__econ_c 
        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__def_conf_cnt_r;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__75__econ_s 
        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__def_conf_start_r;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__75__ereq_c 
        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__def_req_cnt_r;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__75__ereq_s 
        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__def_req_start_r;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__75__dda 
        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__def_da_r;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__75__cnt 
        = (0x000000ffU & (vlSelfRef.milan_datapath__DOT__csr__DOT__maap_ctrl 
                          >> 8U));
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__75__off 
        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__offset_r;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__75__msg 
        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__send_msg_r;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__75__idx 
        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__bld_idx_r;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__75__i 
        = __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__75__idx;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__75__dfd 
        = (2U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__75__msg));
    if (__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__75__dfd) {
        __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__75__req_s 
            = __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__75__ereq_s;
        __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__75__req_c 
            = __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__75__ereq_c;
    } else {
        __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__75__req_s 
            = (0x000091e0f0000000ULL | (QData)((IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__75__off)));
        __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__75__req_c 
            = __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__75__cnt;
    }
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__75__b = 0U;
    if ((6U > __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__75__i)) {
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__byte48_f__76__n 
            = __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__75__i;
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__byte48_f__76__v 
            = ((IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__75__dfd)
                ? __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__75__dda
                : 0x000091e0f000ff00ULL);
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__byte48_f__76__sh 
            = VL_SHIFTR_QQI(48,48,32, vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__byte48_f__76__v, 
                            (((IData)(5U) - vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__byte48_f__76__n) 
                             << 3U));
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__byte48_f__76__Vfuncout 
            = (0x000000ffU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__byte48_f__76__sh));
        __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__75__b 
            = vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__byte48_f__76__Vfuncout;
    } else if ((0x0000000cU > __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__75__i)) {
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__byte48_f__77__n 
            = (__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__75__i 
               - (IData)(6U));
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__byte48_f__77__v 
            = vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w;
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__byte48_f__77__sh 
            = VL_SHIFTR_QQI(48,48,32, vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__byte48_f__77__v, 
                            (((IData)(5U) - vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__byte48_f__77__n) 
                             << 3U));
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__byte48_f__77__Vfuncout 
            = (0x000000ffU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__byte48_f__77__sh));
        __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__75__b 
            = vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__byte48_f__77__Vfuncout;
    } else if ((0x0000000eU > __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__75__i)) {
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__byte16_f__78__n 
            = (__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__75__i 
               - (IData)(0x0000000cU));
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__byte16_f__78__sh 
            = VL_SHIFTR_III(16,16,32, 0x22f0U, (((IData)(1U) 
                                                 - vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__byte16_f__78__n) 
                                                << 3U));
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__byte16_f__78__Vfuncout 
            = (0x000000ffU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__byte16_f__78__sh));
        __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__75__b 
            = vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__byte16_f__78__Vfuncout;
    } else if ((0x0000000eU == __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__75__i)) {
        __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__75__b = 0xfeU;
    } else if ((0x0000000fU == __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__75__i)) {
        __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__75__b 
            = __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__75__msg;
    } else if ((0x00000010U == __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__75__i)) {
        __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__75__b = 8U;
    } else if ((0x00000011U == __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__75__i)) {
        __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__75__b = 0x10U;
    } else if (((0x0000001aU <= __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__75__i) 
                & (0x00000020U > __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__75__i))) {
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__byte48_f__79__n 
            = (__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__75__i 
               - (IData)(0x0000001aU));
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__byte48_f__79__v 
            = __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__75__req_s;
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__byte48_f__79__sh 
            = VL_SHIFTR_QQI(48,48,32, vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__byte48_f__79__v, 
                            (((IData)(5U) - vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__byte48_f__79__n) 
                             << 3U));
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__byte48_f__79__Vfuncout 
            = (0x000000ffU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__byte48_f__79__sh));
        __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__75__b 
            = vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__byte48_f__79__Vfuncout;
    } else if (((0x00000020U <= __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__75__i) 
                & (0x00000022U > __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__75__i))) {
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__byte16_f__80__n 
            = (__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__75__i 
               - (IData)(0x00000020U));
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__byte16_f__80__v 
            = __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__75__req_c;
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__byte16_f__80__sh 
            = VL_SHIFTR_III(16,16,32, (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__byte16_f__80__v), 
                            (((IData)(1U) - vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__byte16_f__80__n) 
                             << 3U));
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__byte16_f__80__Vfuncout 
            = (0x000000ffU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__byte16_f__80__sh));
        __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__75__b 
            = vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__byte16_f__80__Vfuncout;
    } else if ((((IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__75__dfd) 
                 & (0x00000022U <= __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__75__i)) 
                & (0x00000028U > __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__75__i))) {
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__byte48_f__81__n 
            = (__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__75__i 
               - (IData)(0x00000022U));
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__byte48_f__81__v 
            = __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__75__econ_s;
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__byte48_f__81__sh 
            = VL_SHIFTR_QQI(48,48,32, vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__byte48_f__81__v, 
                            (((IData)(5U) - vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__byte48_f__81__n) 
                             << 3U));
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__byte48_f__81__Vfuncout 
            = (0x000000ffU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__byte48_f__81__sh));
        __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__75__b 
            = vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__byte48_f__81__Vfuncout;
    } else if ((((IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__75__dfd) 
                 & (0x00000028U <= __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__75__i)) 
                & (0x0000002aU > __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__75__i))) {
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__byte16_f__82__n 
            = (__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__75__i 
               - (IData)(0x00000028U));
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__byte16_f__82__v 
            = __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__75__econ_c;
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__byte16_f__82__sh 
            = VL_SHIFTR_III(16,16,32, (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__byte16_f__82__v), 
                            (((IData)(1U) - vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__byte16_f__82__n) 
                             << 3U));
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__byte16_f__82__Vfuncout 
            = (0x000000ffU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__byte16_f__82__sh));
        __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__75__b 
            = vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__byte16_f__82__Vfuncout;
    }
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__75__Vfuncout 
        = __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__75__b;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__maapeng_txs_wr_data_w 
        = __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__75__Vfuncout;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__wr_valid_w = 0U;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__wr_data_w = 0U;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__nbytes_w = 1U;
    if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__vld_e_r) {
        if ((1U & (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__uop_e_r 
                           >> 0x0000002fU)))) {
            if ((1U & (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__uop_e_r 
                               >> 0x0000002eU)))) {
                if ((1U & (~ (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__uop_e_r 
                                      >> 0x0000002dU))))) {
                    if ((1U & (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__uop_e_r 
                                       >> 0x0000002cU)))) {
                        milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__urb_we_w 
                            = (1U & ((1U & (IData)(
                                                   (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__uop_e_r 
                                                    >> 0x0000002bU)))
                                      ? (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__append_skip_w))
                                      : (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__batch_r))));
                    }
                }
            } else if ((1U & (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__uop_e_r 
                                      >> 0x0000002dU)))) {
                if ((1U & (~ (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__uop_e_r 
                                      >> 0x0000002cU))))) {
                    if ((1U & (~ (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__uop_e_r 
                                          >> 0x0000002bU))))) {
                        milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__urb_we_w 
                            = (1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__append_skip_w)));
                    }
                }
            } else if ((1U & (~ (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__uop_e_r 
                                         >> 0x0000002cU))))) {
                if ((1U & (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__uop_e_r 
                                   >> 0x0000002bU)))) {
                    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__urb_we_w 
                        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gxr_valid_r) 
                           & (4U > (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__eseq_r)));
                }
            }
        } else if ((1U & (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__uop_e_r 
                                  >> 0x0000002eU)))) {
            if ((1U & (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__uop_e_r 
                               >> 0x0000002dU)))) {
                if ((1U & (~ (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__uop_e_r 
                                      >> 0x0000002cU))))) {
                    if ((1U & (~ (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__uop_e_r 
                                          >> 0x0000002bU))))) {
                        milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__urb_we_w 
                            = (((1U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__eseq_r)) 
                                & (0U != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__copy_adv1_w))) 
                               | ((2U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__eseq_r)) 
                                  & (0U != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__copy_adv2_w))));
                    }
                }
            }
        }
    }
    if ((8U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__st_r))) {
        if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__st_r))) {
            if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__st_r))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__wr_valid_w = 0U;
            } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__st_r))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__wr_valid_w = 1U;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__nbytes_w = 2U;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__wr_data_w = 0U;
            } else {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__wr_valid_w = 1U;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__nbytes_w = 2U;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__wr_data_w 
                    = (0x000000ffU & ((0U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__bidx_r))
                                       ? (7U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__ll_val_w) 
                                                >> 8U))
                                       : (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__ll_val_w)));
            }
        } else if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__st_r))) {
            if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__st_r))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__wr_valid_w = 1U;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__nbytes_w = 2U;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__wr_data_w = 0U;
            } else {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__wr_valid_w = 1U;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__nbytes_w 
                    = (0x0000000fU & (((IData)(3U) 
                                       + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_len_r)) 
                                      >> 2U));
                vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_fp_at_f__19__j 
                    = (0x0000003fU & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__bidx_r) 
                                      << 2U));
                {
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT____VlemCall_4__run_fp_at_f = 0;
                    if (((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_fp_at_f__19__j) 
                         >= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_len_r))) {
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT____VlemCall_4__run_fp_at_f = 0U;
                        goto __Vlabel0;
                    }
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT____VlemCall_4__run_fp_at_f 
                        = ((0x17U >= (0x0000001eU & 
                                      ((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_fp_at_f__19__j) 
                                       << 1U))) ? (3U 
                                                   & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_fp_r 
                                                      >> 
                                                      (0x0000001eU 
                                                       & ((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_fp_at_f__19__j) 
                                                          << 1U))))
                            : 0U);
                    __Vlabel0: ;
                }
                vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_fp_at_f__20__j 
                    = (0x0000003fU & ((IData)(1U) + 
                                      ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__bidx_r) 
                                       << 2U)));
                {
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT____VlemCall_5__run_fp_at_f = 0;
                    if (((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_fp_at_f__20__j) 
                         >= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_len_r))) {
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT____VlemCall_5__run_fp_at_f = 0U;
                        goto __Vlabel1;
                    }
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT____VlemCall_5__run_fp_at_f 
                        = ((0x17U >= (0x0000001eU & 
                                      ((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_fp_at_f__20__j) 
                                       << 1U))) ? (3U 
                                                   & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_fp_r 
                                                      >> 
                                                      (0x0000001eU 
                                                       & ((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_fp_at_f__20__j) 
                                                          << 1U))))
                            : 0U);
                    __Vlabel1: ;
                }
                vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_fp_at_f__21__j 
                    = (0x0000003fU & ((IData)(2U) + 
                                      ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__bidx_r) 
                                       << 2U)));
                {
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT____VlemCall_6__run_fp_at_f = 0;
                    if (((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_fp_at_f__21__j) 
                         >= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_len_r))) {
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT____VlemCall_6__run_fp_at_f = 0U;
                        goto __Vlabel2;
                    }
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT____VlemCall_6__run_fp_at_f 
                        = ((0x17U >= (0x0000001eU & 
                                      ((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_fp_at_f__21__j) 
                                       << 1U))) ? (3U 
                                                   & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_fp_r 
                                                      >> 
                                                      (0x0000001eU 
                                                       & ((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_fp_at_f__21__j) 
                                                          << 1U))))
                            : 0U);
                    __Vlabel2: ;
                }
                vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_fp_at_f__22__j 
                    = (0x0000003fU & ((IData)(3U) + 
                                      ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__bidx_r) 
                                       << 2U)));
                {
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT____VlemCall_7__run_fp_at_f = 0;
                    if (((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_fp_at_f__22__j) 
                         >= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_len_r))) {
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT____VlemCall_7__run_fp_at_f = 0U;
                        goto __Vlabel3;
                    }
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT____VlemCall_7__run_fp_at_f 
                        = ((0x17U >= (0x0000001eU & 
                                      ((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_fp_at_f__22__j) 
                                       << 1U))) ? (3U 
                                                   & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_fp_r 
                                                      >> 
                                                      (0x0000001eU 
                                                       & ((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_fp_at_f__22__j) 
                                                          << 1U))))
                            : 0U);
                    __Vlabel3: ;
                }
                vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__pack4_f__23__d 
                    = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT____VlemCall_7__run_fp_at_f;
                vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__pack4_f__23__c 
                    = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT____VlemCall_6__run_fp_at_f;
                vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__pack4_f__23__b 
                    = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT____VlemCall_5__run_fp_at_f;
                vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__pack4_f__23__a 
                    = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT____VlemCall_4__run_fp_at_f;
                vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__pack4_f__23__Vfuncout 
                    = (0x000000ffU & (((((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__pack4_f__23__a) 
                                         << 6U) + ((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__pack4_f__23__b) 
                                                   << 4U)) 
                                       + ((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__pack4_f__23__c) 
                                          << 2U)) + (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__pack4_f__23__d)));
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__wr_data_w 
                    = vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__pack4_f__23__Vfuncout;
            }
        } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__st_r))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__wr_valid_w = 1U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__nbytes_w 
                = (0x0000003fU & VL_DIV_III(6, (0x0000003fU 
                                                & ((IData)(2U) 
                                                   + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_len_r))), (IData)(3U)));
            vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_ev_at_f__24__j 
                = (0x0000003fU & ((IData)(3U) * (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__bidx_r)));
            {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT____VlemCall_1__run_ev_at_f = 0;
                if (((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_ev_at_f__24__j) 
                     >= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_len_r))) {
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT____VlemCall_1__run_ev_at_f = 0U;
                    goto __Vlabel4;
                }
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT____VlemCall_1__run_ev_at_f 
                    = ((0x23U >= (0x0000003fU & ((IData)(3U) 
                                                 * 
                                                 (0x0000000fU 
                                                  & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_ev_at_f__24__j)))))
                        ? (7U & (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_ev_r 
                                         >> (0x0000003fU 
                                             & ((IData)(3U) 
                                                * (0x0000000fU 
                                                   & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_ev_at_f__24__j)))))))
                        : 0U);
                __Vlabel4: ;
            }
            vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_ev_at_f__25__j 
                = (0x0000003fU & ((IData)(1U) + ((IData)(3U) 
                                                 * (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__bidx_r))));
            {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT____VlemCall_2__run_ev_at_f = 0;
                if (((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_ev_at_f__25__j) 
                     >= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_len_r))) {
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT____VlemCall_2__run_ev_at_f = 0U;
                    goto __Vlabel5;
                }
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT____VlemCall_2__run_ev_at_f 
                    = ((0x23U >= (0x0000003fU & ((IData)(3U) 
                                                 * 
                                                 (0x0000000fU 
                                                  & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_ev_at_f__25__j)))))
                        ? (7U & (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_ev_r 
                                         >> (0x0000003fU 
                                             & ((IData)(3U) 
                                                * (0x0000000fU 
                                                   & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_ev_at_f__25__j)))))))
                        : 0U);
                __Vlabel5: ;
            }
            vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_ev_at_f__26__j 
                = (0x0000003fU & ((IData)(2U) + ((IData)(3U) 
                                                 * (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__bidx_r))));
            {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT____VlemCall_3__run_ev_at_f = 0;
                if (((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_ev_at_f__26__j) 
                     >= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_len_r))) {
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT____VlemCall_3__run_ev_at_f = 0U;
                    goto __Vlabel6;
                }
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT____VlemCall_3__run_ev_at_f 
                    = ((0x23U >= (0x0000003fU & ((IData)(3U) 
                                                 * 
                                                 (0x0000000fU 
                                                  & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_ev_at_f__26__j)))))
                        ? (7U & (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_ev_r 
                                         >> (0x0000003fU 
                                             & ((IData)(3U) 
                                                * (0x0000000fU 
                                                   & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_ev_at_f__26__j)))))))
                        : 0U);
                __Vlabel6: ;
            }
            vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__pack3_f__27__c 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT____VlemCall_3__run_ev_at_f;
            vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__pack3_f__27__b 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT____VlemCall_2__run_ev_at_f;
            vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__pack3_f__27__a 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT____VlemCall_1__run_ev_at_f;
            vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__pack3_f__27__Vfuncout 
                = (0x000000ffU & ((((IData)(0x24U) 
                                    * (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__pack3_f__27__a)) 
                                   + ((IData)(6U) * (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__pack3_f__27__b))) 
                                  + (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__pack3_f__27__c)));
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__wr_data_w 
                = vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__pack3_f__27__Vfuncout;
        } else {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__wr_valid_w = 1U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__nbytes_w 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__alen_w;
            vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__fv_byte_f__28__i 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__bidx_r;
            vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__fv_byte_f__28__v[0U] 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_first_r[0U];
            vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__fv_byte_f__28__v[1U] 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_first_r[1U];
            vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__fv_byte_f__28__v[2U] 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_first_r[2U];
            vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__fv_byte_f__28__v[3U] 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_first_r[3U];
            vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__fv_byte_f__28__v[4U] 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_first_r[4U];
            vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__fv_byte_f__28__v[5U] 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_first_r[5U];
            vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__fv_byte_f__28__v[6U] 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_first_r[6U];
            vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__fv_byte_f__28__v[7U] 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_first_r[7U];
            vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__fv_byte_f__28__v[8U] 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_first_r[8U];
            vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__fv_byte_f__28__Vfuncout 
                = ((0x010fU >= (0x000001ffU & (((IData)(0x010fU) 
                                                - ((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__fv_byte_f__28__i) 
                                                   << 3U)) 
                                               - (IData)(7U))))
                    ? (0x000000ffU & (((0U == (0x0000001fU 
                                               & (((IData)(0x010fU) 
                                                   - 
                                                   ((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__fv_byte_f__28__i) 
                                                    << 3U)) 
                                                  - (IData)(7U))))
                                        ? 0U : (vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__fv_byte_f__28__v
                                                [(((IData)(7U) 
                                                   + 
                                                   (0x000001ffU 
                                                    & (((IData)(0x010fU) 
                                                        - 
                                                        ((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__fv_byte_f__28__i) 
                                                         << 3U)) 
                                                       - (IData)(7U)))) 
                                                  >> 5U)] 
                                                << 
                                                ((IData)(0x00000020U) 
                                                 - 
                                                 (0x0000001fU 
                                                  & (((IData)(0x010fU) 
                                                      - 
                                                      ((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__fv_byte_f__28__i) 
                                                       << 3U)) 
                                                     - (IData)(7U)))))) 
                                      | (vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__fv_byte_f__28__v
                                         [(0x0000000fU 
                                           & ((((IData)(0x010fU) 
                                                - ((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__fv_byte_f__28__i) 
                                                   << 3U)) 
                                               - (IData)(7U)) 
                                              >> 5U))] 
                                         >> (0x0000001fU 
                                             & (((IData)(0x010fU) 
                                                 - 
                                                 ((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__fv_byte_f__28__i) 
                                                  << 3U)) 
                                                - (IData)(7U))))))
                    : 0U);
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__wr_data_w 
                = vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__fv_byte_f__28__Vfuncout;
        }
    } else if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__st_r))) {
        if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__st_r))) {
            if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__st_r))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__wr_valid_w = 1U;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__nbytes_w = 2U;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__wr_data_w 
                    = ((0U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__bidx_r))
                        ? (0x00000020U & ((- (IData)(
                                                     ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__first_vec_r) 
                                                      & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__la_pend_r) 
                                                         >> (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__cur_app_r))))) 
                                          << 5U)) : (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_len_r));
            } else {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__wr_valid_w = 1U;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__nbytes_w 
                    = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__cur_app_r)
                        ? 2U : 4U);
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__wr_data_w 
                    = ((0U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__bidx_r))
                        ? (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_type_r)
                        : ((1U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__bidx_r))
                            ? (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__alen_w)
                            : 0U));
            }
        } else {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__wr_valid_w = 0U;
        }
    } else if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__st_r))) {
        if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__st_r))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__wr_valid_w = 0U;
        } else {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__wr_valid_w = 1U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__nbytes_w = 0x0fU;
            if ((6U > (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__bidx_r))) {
                vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__mac_byte_f__29__i 
                    = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__bidx_r;
                vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__mac_byte_f__29__v 
                    = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__cur_app_r)
                        ? 0x00000180c2000021ULL : 0x00000180c200000eULL);
                vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__mac_byte_f__29__Vfuncout 
                    = ((0x2fU >= (0x0000003fU & (((IData)(0x2fU) 
                                                  - 
                                                  ((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__mac_byte_f__29__i) 
                                                   << 3U)) 
                                                 - (IData)(7U))))
                        ? (0x000000ffU & (IData)((vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__mac_byte_f__29__v 
                                                  >> 
                                                  (0x0000003fU 
                                                   & (((IData)(0x2fU) 
                                                       - 
                                                       ((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__mac_byte_f__29__i) 
                                                        << 3U)) 
                                                      - (IData)(7U))))))
                        : 0U);
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__wr_data_w 
                    = vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__mac_byte_f__29__Vfuncout;
            } else if ((0x0cU > (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__bidx_r))) {
                vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__mac_byte_f__30__i 
                    = (0x0000003fU & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__bidx_r) 
                                      - (IData)(6U)));
                vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__mac_byte_f__30__v 
                    = vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w;
                vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__mac_byte_f__30__Vfuncout 
                    = ((0x2fU >= (0x0000003fU & (((IData)(0x2fU) 
                                                  - 
                                                  ((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__mac_byte_f__30__i) 
                                                   << 3U)) 
                                                 - (IData)(7U))))
                        ? (0x000000ffU & (IData)((vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__mac_byte_f__30__v 
                                                  >> 
                                                  (0x0000003fU 
                                                   & (((IData)(0x2fU) 
                                                       - 
                                                       ((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__mac_byte_f__30__i) 
                                                        << 3U)) 
                                                      - (IData)(7U))))))
                        : 0U);
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__wr_data_w 
                    = vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__mac_byte_f__30__Vfuncout;
            } else {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__wr_data_w 
                    = (0x000000ffU & ((0x0cU == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__bidx_r))
                                       ? (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__cur_app_r)
                                            ? 0x88f5U
                                            : 0x22eaU) 
                                          >> 8U) : 
                                      ((0x0dU == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__bidx_r))
                                        ? ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__cur_app_r)
                                            ? 0x88f5U
                                            : 0x22eaU)
                                        : 0U)));
            }
        }
    } else {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__wr_valid_w = 0U;
    }
    vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__chans_pop_raw_w = 0U;
    if ((0U == (IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__slot_r))) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__chans_pop_raw_w 
            = (0x0000000fU & vlSelfRef.milan_datapath__DOT__mon_wire_chans_all_w);
    }
    if ((1U == (IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__slot_r))) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__chans_pop_raw_w 
            = (0x0000000fU & (vlSelfRef.milan_datapath__DOT__mon_wire_chans_all_w 
                              >> 4U));
    }
    if ((2U == (IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__slot_r))) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__chans_pop_raw_w 
            = (0x0000000fU & (vlSelfRef.milan_datapath__DOT__mon_wire_chans_all_w 
                              >> 8U));
    }
    if ((3U == (IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__slot_r))) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__chans_pop_raw_w 
            = (0x0000000fU & (vlSelfRef.milan_datapath__DOT__mon_wire_chans_all_w 
                              >> 0x0cU));
    }
    if ((4U == (IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__slot_r))) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__chans_pop_raw_w 
            = (0x0000000fU & (vlSelfRef.milan_datapath__DOT__mon_wire_chans_all_w 
                              >> 0x10U));
    }
    if ((5U == (IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__slot_r))) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__chans_pop_raw_w 
            = (0x0000000fU & (vlSelfRef.milan_datapath__DOT__mon_wire_chans_all_w 
                              >> 0x14U));
    }
    if ((6U == (IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__slot_r))) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__chans_pop_raw_w 
            = (0x0000000fU & (vlSelfRef.milan_datapath__DOT__mon_wire_chans_all_w 
                              >> 0x18U));
    }
    if ((7U == (IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__slot_r))) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__chans_pop_raw_w 
            = (vlSelfRef.milan_datapath__DOT__mon_wire_chans_all_w 
               >> 0x1cU);
    }
    vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__chans_in_raw_w = 0U;
    if ((0U == vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__idxq_r
         [vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__idxq_rp_r])) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__chans_in_raw_w 
            = (0x0000000fU & vlSelfRef.milan_datapath__DOT__mon_wire_chans_all_w);
    }
    if ((1U == vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__idxq_r
         [vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__idxq_rp_r])) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__chans_in_raw_w 
            = (0x0000000fU & (vlSelfRef.milan_datapath__DOT__mon_wire_chans_all_w 
                              >> 4U));
    }
    if ((2U == vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__idxq_r
         [vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__idxq_rp_r])) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__chans_in_raw_w 
            = (0x0000000fU & (vlSelfRef.milan_datapath__DOT__mon_wire_chans_all_w 
                              >> 8U));
    }
    if ((3U == vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__idxq_r
         [vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__idxq_rp_r])) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__chans_in_raw_w 
            = (0x0000000fU & (vlSelfRef.milan_datapath__DOT__mon_wire_chans_all_w 
                              >> 0x0cU));
    }
    if ((4U == vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__idxq_r
         [vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__idxq_rp_r])) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__chans_in_raw_w 
            = (0x0000000fU & (vlSelfRef.milan_datapath__DOT__mon_wire_chans_all_w 
                              >> 0x10U));
    }
    if ((5U == vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__idxq_r
         [vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__idxq_rp_r])) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__chans_in_raw_w 
            = (0x0000000fU & (vlSelfRef.milan_datapath__DOT__mon_wire_chans_all_w 
                              >> 0x14U));
    }
    if ((6U == vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__idxq_r
         [vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__idxq_rp_r])) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__chans_in_raw_w 
            = (0x0000000fU & (vlSelfRef.milan_datapath__DOT__mon_wire_chans_all_w 
                              >> 0x18U));
    }
    if ((7U == vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__idxq_r
         [vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__idxq_rp_r])) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__chans_in_raw_w 
            = (vlSelfRef.milan_datapath__DOT__mon_wire_chans_all_w 
               >> 0x1cU);
    }
    vlSelfRef.milan_datapath__DOT__lb_tap_chans_w = vlSelfRef.milan_datapath__DOT__mon_wire_chans_all_w;
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_57 = (((0x00000100U 
                                                   & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__fail_r))
                                                   ? 2U
                                                   : 1U) 
                                                 & (- (IData)((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_112))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_out_w 
        = ((((((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_58) 
               << 6U) | ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_59) 
                         << 4U)) | (((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_60) 
                                     << 2U) | (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_61))) 
            << 0x0000000aU) | ((((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_62) 
                                 << 8U) | ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_63) 
                                           << 6U)) 
                               | (((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_64) 
                                   << 4U) | (((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_65) 
                                              << 2U) 
                                             | (IData)(vlSelfRef.milan_datapath__DOT__lwsrp_listener_decl)))));
    vlSelfRef.milan_datapath__DOT__lwsrp_listener_ready 
        = ((2U == (IData)(vlSelfRef.milan_datapath__DOT__lwsrp_listener_decl)) 
           | (3U == (IData)(vlSelfRef.milan_datapath__DOT__lwsrp_listener_decl)));
    vlSelfRef.milan_datapath__DOT__csr__DOT__pp_rd_hit_w 
        = ((0x0920U == (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
           | ((0x0924U == (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
              | ((0x0928U == (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                 | ((0x092cU == (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                    | ((0x0930U == (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                       | ((0x0934U == (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                          | (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__g_pp_csr__DOT__pp_nvm_rd_w)))))));
    vlSelfRef.milan_datapath__DOT__pp_nvm_csr_sel_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__g_pp_csr__DOT__pp_nvm_we_r) 
           | (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__g_pp_csr__DOT__pp_nvm_rd_w));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_129 = ((
                                                   (1U 
                                                    & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__fail_r))
                                                    ? 2U
                                                    : 1U) 
                                                  & (- (IData)((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_104))));
    vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__lb_a0_w 
        = (0x0000001fU & (((IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__lb_chpos_r) 
                           >> 1U) + (0x0000001cU & 
                                     ((IData)(vlSelfRef.milan_datapath__DOT__lb_tap_tuser_w) 
                                      << 2U))));
    vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__beat_flush_w = 0U;
    if (((IData)(vlSelfRef.milan_datapath__DOT__strtbl_bind_fall_w) 
         & (0U == (IData)(vlSelfRef.milan_datapath__DOT__lb_tap_tuser_w)))) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__beat_flush_w = 1U;
    }
    if ((((IData)(vlSelfRef.milan_datapath__DOT__strtbl_bind_fall_w) 
          >> 1U) & (1U == (IData)(vlSelfRef.milan_datapath__DOT__lb_tap_tuser_w)))) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__beat_flush_w = 1U;
    }
    if ((((IData)(vlSelfRef.milan_datapath__DOT__strtbl_bind_fall_w) 
          >> 2U) & (2U == (IData)(vlSelfRef.milan_datapath__DOT__lb_tap_tuser_w)))) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__beat_flush_w = 1U;
    }
    if ((((IData)(vlSelfRef.milan_datapath__DOT__strtbl_bind_fall_w) 
          >> 3U) & (3U == (IData)(vlSelfRef.milan_datapath__DOT__lb_tap_tuser_w)))) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__beat_flush_w = 1U;
    }
    if ((((IData)(vlSelfRef.milan_datapath__DOT__strtbl_bind_fall_w) 
          >> 4U) & (4U == (IData)(vlSelfRef.milan_datapath__DOT__lb_tap_tuser_w)))) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__beat_flush_w = 1U;
    }
    if ((((IData)(vlSelfRef.milan_datapath__DOT__strtbl_bind_fall_w) 
          >> 5U) & (5U == (IData)(vlSelfRef.milan_datapath__DOT__lb_tap_tuser_w)))) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__beat_flush_w = 1U;
    }
    if ((((IData)(vlSelfRef.milan_datapath__DOT__strtbl_bind_fall_w) 
          >> 6U) & (6U == (IData)(vlSelfRef.milan_datapath__DOT__lb_tap_tuser_w)))) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__beat_flush_w = 1U;
    }
    if ((((IData)(vlSelfRef.milan_datapath__DOT__strtbl_bind_fall_w) 
          >> 7U) & (7U == (IData)(vlSelfRef.milan_datapath__DOT__lb_tap_tuser_w)))) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__beat_flush_w = 1U;
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__seed_w 
        = (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__ctr_r 
           ^ vlSelfRef.milan_datapath__DOT__cfg_adp_entity_id);
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__drop_w 
        = (1U & ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__out_data_r[10U] 
                  >> 0x0000001eU) | ((((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__out_data_r[6U])) 
                                       << 0x00000022U) 
                                      | (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__out_data_r[5U])) 
                                          << 2U) | 
                                         ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__out_data_r[4U])) 
                                          >> 0x0000001eU))) 
                                     != vlSelfRef.milan_datapath__DOT__cfg_adp_entity_id)));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__ca_txs_wr_data_w = 0U;
    if ((6U > (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_ca_builder__DOT__byte_r))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__ca_txs_wr_data_w 
            = ((0x2fU >= (0x0000003fU & (((IData)(0x2fU) 
                                          - ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_ca_builder__DOT__byte_r) 
                                             << 3U)) 
                                         - (IData)(7U))))
                ? (0x000000ffU & (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_ca_builder__DOT__ctlr_mac_r 
                                          >> (0x0000003fU 
                                              & (((IData)(0x2fU) 
                                                  - 
                                                  ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_ca_builder__DOT__byte_r) 
                                                   << 3U)) 
                                                 - (IData)(7U))))))
                : 0U);
    } else if ((0x0cU > (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_ca_builder__DOT__byte_r))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__ca_txs_wr_data_w 
            = ((0x2fU >= (0x0000003fU & (((IData)(0x2fU) 
                                          - (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_ca_builder__DOT__byte_r) 
                                              - (IData)(6U)) 
                                             << 3U)) 
                                         - (IData)(7U))))
                ? (0x000000ffU & (IData)((vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w 
                                          >> (0x0000003fU 
                                              & (((IData)(0x2fU) 
                                                  - 
                                                  (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_ca_builder__DOT__byte_r) 
                                                    - (IData)(6U)) 
                                                   << 3U)) 
                                                 - (IData)(7U))))))
                : 0U);
    } else if ((0x0cU == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_ca_builder__DOT__byte_r))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__ca_txs_wr_data_w = 0x22U;
    } else if ((0x0dU == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_ca_builder__DOT__byte_r))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__ca_txs_wr_data_w = 0xf0U;
    } else if ((0x0eU == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_ca_builder__DOT__byte_r))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__ca_txs_wr_data_w = 0xfbU;
    } else if ((0x0fU == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_ca_builder__DOT__byte_r))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__ca_txs_wr_data_w = 0U;
    } else if ((0x10U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_ca_builder__DOT__byte_r))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__ca_txs_wr_data_w = 0U;
    } else if ((0x11U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_ca_builder__DOT__byte_r))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__ca_txs_wr_data_w = 0x0cU;
    } else if ((0x1aU > (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_ca_builder__DOT__byte_r))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__ca_txs_wr_data_w 
            = (0x000000ffU & (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_ca_builder__DOT__ctlr_eid_r 
                                      >> (0x0000003fU 
                                          & (((IData)(0x3fU) 
                                              - (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_ca_builder__DOT__byte_r) 
                                                  - (IData)(0x00000012U)) 
                                                 << 3U)) 
                                             - (IData)(7U))))));
    } else if ((0x22U > (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_ca_builder__DOT__byte_r))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__ca_txs_wr_data_w 
            = (0x000000ffU & (IData)((vlSelfRef.milan_datapath__DOT__cfg_adp_entity_id 
                                      >> (0x0000003fU 
                                          & (((IData)(0x3fU) 
                                              - (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_ca_builder__DOT__byte_r) 
                                                  - (IData)(0x0000001aU)) 
                                                 << 3U)) 
                                             - (IData)(7U))))));
    } else if ((0x22U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_ca_builder__DOT__byte_r))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__ca_txs_wr_data_w 
            = (0x000000ffU & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_ca_builder__DOT__seq_r) 
                              >> 8U));
    } else if ((0x23U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_ca_builder__DOT__byte_r))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__ca_txs_wr_data_w 
            = (0x000000ffU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_ca_builder__DOT__seq_r));
    } else if ((0x24U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_ca_builder__DOT__byte_r))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__ca_txs_wr_data_w = 0U;
    } else if ((0x25U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_ca_builder__DOT__byte_r))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__ca_txs_wr_data_w = 3U;
    }
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__117__aidx 
        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__bld_aidx_r;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__117__dom 
        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__bld_dom_r;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__117__gm 
        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__bld_gm_r;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__117__ifx 
        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__bld_if_r;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__117__dep 
        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__bld_dep_r;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__117__idx 
        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__bld_idx_r;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__117__i 
        = __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__117__idx;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__117__b = 0U;
    if ((6U > __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__117__i)) {
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte48_f__118__n 
            = __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__117__i;
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte48_f__118__sh 
            = VL_SHIFTR_QQI(48,48,32, 0x000091e0f0010000ULL, 
                            (((IData)(5U) - vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte48_f__118__n) 
                             << 3U));
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte48_f__118__Vfuncout 
            = (0x000000ffU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte48_f__118__sh));
        __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__117__b 
            = vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte48_f__118__Vfuncout;
    } else if ((0x0000000cU > __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__117__i)) {
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte48_f__119__n 
            = (__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__117__i 
               - (IData)(6U));
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte48_f__119__v 
            = vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w;
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte48_f__119__sh 
            = VL_SHIFTR_QQI(48,48,32, vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte48_f__119__v, 
                            (((IData)(5U) - vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte48_f__119__n) 
                             << 3U));
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte48_f__119__Vfuncout 
            = (0x000000ffU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte48_f__119__sh));
        __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__117__b 
            = vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte48_f__119__Vfuncout;
    } else if ((0x0000000eU > __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__117__i)) {
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte16_f__120__n 
            = (__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__117__i 
               - (IData)(0x0000000cU));
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte16_f__120__sh 
            = VL_SHIFTR_III(16,16,32, 0x22f0U, (((IData)(1U) 
                                                 - vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte16_f__120__n) 
                                                << 3U));
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte16_f__120__Vfuncout 
            = (0x000000ffU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte16_f__120__sh));
        __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__117__b 
            = vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte16_f__120__Vfuncout;
    } else if ((0x0000000eU == __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__117__i)) {
        __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__117__b = 0xfaU;
    } else if ((0x0000000fU == __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__117__i)) {
        __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__117__b 
            = ((IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__117__dep)
                ? 1U : 0U);
    } else if ((0x00000010U == __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__117__i)) {
        __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__117__b 
            = (((IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__117__dep)
                 ? 0U : 0x0aU) << 3U);
    } else if ((0x00000011U == __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__117__i)) {
        __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__117__b = 0x38U;
    } else if ((0x0000001aU > __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__117__i)) {
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte64_f__121__n 
            = (__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__117__i 
               - (IData)(0x00000012U));
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte64_f__121__v 
            = vlSelfRef.milan_datapath__DOT__cfg_adp_entity_id;
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte64_f__121__sh 
            = VL_SHIFTR_QQI(64,64,32, vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte64_f__121__v, 
                            (((IData)(7U) - vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte64_f__121__n) 
                             << 3U));
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte64_f__121__Vfuncout 
            = (0x000000ffU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte64_f__121__sh));
        __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__117__b 
            = vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte64_f__121__Vfuncout;
    } else if ((0x00000022U > __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__117__i)) {
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte64_f__122__n 
            = (__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__117__i 
               - (IData)(0x0000001aU));
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte64_f__122__v 
            = (((QData)((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__adp_midhi)) 
                << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__adp_midlo)));
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte64_f__122__sh 
            = VL_SHIFTR_QQI(64,64,32, vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte64_f__122__v, 
                            (((IData)(7U) - vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte64_f__122__n) 
                             << 3U));
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte64_f__122__Vfuncout 
            = (0x000000ffU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte64_f__122__sh));
        __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__117__b 
            = vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte64_f__122__Vfuncout;
    } else if ((0x00000026U > __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__117__i)) {
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte32_f__123__n 
            = (__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__117__i 
               - (IData)(0x00000022U));
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte32_f__123__sh 
            = VL_SHIFTR_III(32,32,32, 0x0000c588U, 
                            (((IData)(3U) - vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte32_f__123__n) 
                             << 3U));
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte32_f__123__Vfuncout 
            = (0x000000ffU & vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte32_f__123__sh);
        __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__117__b 
            = vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte32_f__123__Vfuncout;
    } else if ((0x00000028U > __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__117__i)) {
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte16_f__124__n 
            = (__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__117__i 
               - (IData)(0x00000026U));
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte16_f__124__sh 
            = VL_SHIFTR_III(16,16,32, 9U, (((IData)(1U) 
                                            - vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte16_f__124__n) 
                                           << 3U));
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte16_f__124__Vfuncout 
            = (0x000000ffU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte16_f__124__sh));
        __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__117__b 
            = vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte16_f__124__Vfuncout;
    } else if ((0x0000002aU > __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__117__i)) {
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte16_f__125__n 
            = (__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__117__i 
               - (IData)(0x00000028U));
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte16_f__125__sh 
            = VL_SHIFTR_III(16,16,32, 0x4801U, (((IData)(1U) 
                                                 - vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte16_f__125__n) 
                                                << 3U));
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte16_f__125__Vfuncout 
            = (0x000000ffU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte16_f__125__sh));
        __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__117__b 
            = vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte16_f__125__Vfuncout;
    } else if ((0x0000002cU > __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__117__i)) {
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte16_f__126__n 
            = (__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__117__i 
               - (IData)(0x0000002aU));
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte16_f__126__sh 
            = VL_SHIFTR_III(16,16,32, 9U, (((IData)(1U) 
                                            - vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte16_f__126__n) 
                                           << 3U));
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte16_f__126__Vfuncout 
            = (0x000000ffU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte16_f__126__sh));
        __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__117__b 
            = vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte16_f__126__Vfuncout;
    } else if ((0x0000002eU > __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__117__i)) {
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte16_f__127__n 
            = (__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__117__i 
               - (IData)(0x0000002cU));
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte16_f__127__sh 
            = VL_SHIFTR_III(16,16,32, 0x4801U, (((IData)(1U) 
                                                 - vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte16_f__127__n) 
                                                << 3U));
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte16_f__127__Vfuncout 
            = (0x000000ffU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte16_f__127__sh));
        __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__117__b 
            = vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte16_f__127__Vfuncout;
    } else if ((0x00000032U > __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__117__i)) {
        __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__117__b = 0U;
    } else if ((0x00000036U > __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__117__i)) {
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte32_f__128__n 
            = (__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__117__i 
               - (IData)(0x00000032U));
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte32_f__128__v 
            = __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__117__aidx;
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte32_f__128__sh 
            = VL_SHIFTR_III(32,32,32, vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte32_f__128__v, 
                            (((IData)(3U) - vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte32_f__128__n) 
                             << 3U));
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte32_f__128__Vfuncout 
            = (0x000000ffU & vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte32_f__128__sh);
        __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__117__b 
            = vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte32_f__128__Vfuncout;
    } else if ((0x0000003eU > __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__117__i)) {
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte64_f__129__n 
            = (__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__117__i 
               - (IData)(0x00000036U));
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte64_f__129__v 
            = __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__117__gm;
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte64_f__129__sh 
            = VL_SHIFTR_QQI(64,64,32, vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte64_f__129__v, 
                            (((IData)(7U) - vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte64_f__129__n) 
                             << 3U));
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte64_f__129__Vfuncout 
            = (0x000000ffU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte64_f__129__sh));
        __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__117__b 
            = vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte64_f__129__Vfuncout;
    } else if ((0x0000003eU == __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__117__i)) {
        __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__117__b 
            = __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__117__dom;
    } else if ((0x0000003fU == __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__117__i)) {
        __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__117__b = 0U;
    } else if ((0x00000042U > __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__117__i)) {
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte16_f__130__n 
            = (__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__117__i 
               - (IData)(0x00000040U));
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte16_f__130__v 
            = (0x0000ffffU & vlSelfRef.milan_datapath__DOT__csr__DOT__adp_idx0);
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte16_f__130__sh 
            = VL_SHIFTR_III(16,16,32, (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte16_f__130__v), 
                            (((IData)(1U) - vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte16_f__130__n) 
                             << 3U));
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte16_f__130__Vfuncout 
            = (0x000000ffU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte16_f__130__sh));
        __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__117__b 
            = vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte16_f__130__Vfuncout;
    } else if ((0x00000044U > __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__117__i)) {
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte16_f__131__n 
            = (__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__117__i 
               - (IData)(0x00000042U));
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte16_f__131__v 
            = (vlSelfRef.milan_datapath__DOT__csr__DOT__adp_idx0 
               >> 0x00000010U);
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte16_f__131__sh 
            = VL_SHIFTR_III(16,16,32, (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte16_f__131__v), 
                            (((IData)(1U) - vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte16_f__131__n) 
                             << 3U));
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte16_f__131__Vfuncout 
            = (0x000000ffU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte16_f__131__sh));
        __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__117__b 
            = vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte16_f__131__Vfuncout;
    } else if ((0x00000046U > __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__117__i)) {
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte16_f__132__n 
            = (__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__117__i 
               - (IData)(0x00000044U));
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte16_f__132__v 
            = __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__117__ifx;
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte16_f__132__sh 
            = VL_SHIFTR_III(16,16,32, (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte16_f__132__v), 
                            (((IData)(1U) - vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte16_f__132__n) 
                             << 3U));
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte16_f__132__Vfuncout 
            = (0x000000ffU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte16_f__132__sh));
        __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__117__b 
            = vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte16_f__132__Vfuncout;
    } else {
        __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__117__b = 0U;
    }
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__117__Vfuncout 
        = __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__117__b;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__adp_txs_wr_data_w 
        = __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__117__Vfuncout;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__talker_cmd_w 
        = (IData)(((4U == (0x0000001cU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__txn_r[11U])) 
                   & (((((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__txn_r[6U])) 
                         << 0x00000022U) | (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__txn_r[5U])) 
                                             << 2U) 
                                            | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__txn_r[4U])) 
                                               >> 0x0000001eU))) 
                       == vlSelfRef.milan_datapath__DOT__cfg_adp_entity_id) 
                      & ((0U == (0x0000000fU & ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__txn_r[11U] 
                                                 << 2U) 
                                                | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__txn_r[10U] 
                                                   >> 0x0000001eU)))) 
                         | ((2U == (0x0000000fU & (
                                                   (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__txn_r[11U] 
                                                    << 2U) 
                                                   | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__txn_r[10U] 
                                                      >> 0x0000001eU)))) 
                            | ((4U == (0x0000000fU 
                                       & ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__txn_r[11U] 
                                           << 2U) | 
                                          (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__txn_r[10U] 
                                           >> 0x0000001eU)))) 
                               | (0x0cU == (0x0000000fU 
                                            & ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__txn_r[11U] 
                                                << 2U) 
                                               | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__txn_r[10U] 
                                                  >> 0x0000001eU))))))))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__rx_cmd_hit_w 
        = ((((((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT____Vcellinp__u_notify__rx_cmd_valid_i) 
                 & (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__valid_r) 
                     >> 0x0000000fU) & ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__hdr_src_mac_r 
                                         == (0x0000ffffffffffffULL 
                                             & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__rows_r[15U][1U])) 
                                                 << 0x00000010U) 
                                                | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__rows_r[15U][0U])) 
                                                   >> 0x00000010U)))) 
                                        & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__hdr_ctlr_eid_r 
                                           == (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__rows_r[15U][3U])) 
                                                << 0x00000020U) 
                                               | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__rows_r[15U][2U]))))))) 
                << 3U) | (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT____Vcellinp__u_notify__rx_cmd_valid_i) 
                           & (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__valid_r) 
                               >> 0x0000000eU) & ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__hdr_src_mac_r 
                                                   == 
                                                   (0x0000ffffffffffffULL 
                                                    & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__rows_r[14U][1U])) 
                                                        << 0x00000010U) 
                                                       | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__rows_r[14U][0U])) 
                                                          >> 0x00000010U)))) 
                                                  & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__hdr_ctlr_eid_r 
                                                     == 
                                                     (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__rows_r[14U][3U])) 
                                                       << 0x00000020U) 
                                                      | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__rows_r[14U][2U]))))))) 
                          << 2U)) | ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT____Vcellinp__u_notify__rx_cmd_valid_i) 
                                       & (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__valid_r) 
                                           >> 0x0000000dU) 
                                          & ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__hdr_src_mac_r 
                                              == (0x0000ffffffffffffULL 
                                                  & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__rows_r[13U][1U])) 
                                                      << 0x00000010U) 
                                                     | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__rows_r[13U][0U])) 
                                                        >> 0x00000010U)))) 
                                             & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__hdr_ctlr_eid_r 
                                                == 
                                                (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__rows_r[13U][3U])) 
                                                  << 0x00000020U) 
                                                 | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__rows_r[13U][2U]))))))) 
                                      << 1U) | ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT____Vcellinp__u_notify__rx_cmd_valid_i) 
                                                & (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__valid_r) 
                                                    >> 0x0000000cU) 
                                                   & ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__hdr_src_mac_r 
                                                       == 
                                                       (0x0000ffffffffffffULL 
                                                        & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__rows_r[12U][1U])) 
                                                            << 0x00000010U) 
                                                           | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__rows_r[12U][0U])) 
                                                              >> 0x00000010U)))) 
                                                      & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__hdr_ctlr_eid_r 
                                                         == 
                                                         (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__rows_r[12U][3U])) 
                                                           << 0x00000020U) 
                                                          | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__rows_r[12U][2U]))))))))) 
             << 0x0000000cU) | ((((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT____Vcellinp__u_notify__rx_cmd_valid_i) 
                                    & (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__valid_r) 
                                        >> 0x0000000bU) 
                                       & ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__hdr_src_mac_r 
                                           == (0x0000ffffffffffffULL 
                                               & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__rows_r[11U][1U])) 
                                                   << 0x00000010U) 
                                                  | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__rows_r[11U][0U])) 
                                                     >> 0x00000010U)))) 
                                          & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__hdr_ctlr_eid_r 
                                             == (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__rows_r[11U][3U])) 
                                                  << 0x00000020U) 
                                                 | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__rows_r[11U][2U]))))))) 
                                   << 3U) | (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT____Vcellinp__u_notify__rx_cmd_valid_i) 
                                              & (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__valid_r) 
                                                  >> 0x0000000aU) 
                                                 & ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__hdr_src_mac_r 
                                                     == 
                                                     (0x0000ffffffffffffULL 
                                                      & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__rows_r[10U][1U])) 
                                                          << 0x00000010U) 
                                                         | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__rows_r[10U][0U])) 
                                                            >> 0x00000010U)))) 
                                                    & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__hdr_ctlr_eid_r 
                                                       == 
                                                       (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__rows_r[10U][3U])) 
                                                         << 0x00000020U) 
                                                        | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__rows_r[10U][2U]))))))) 
                                             << 2U)) 
                                 | ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT____Vcellinp__u_notify__rx_cmd_valid_i) 
                                      & (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__valid_r) 
                                          >> 9U) & 
                                         ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__hdr_src_mac_r 
                                           == (0x0000ffffffffffffULL 
                                               & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__rows_r[9U][1U])) 
                                                   << 0x00000010U) 
                                                  | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__rows_r[9U][0U])) 
                                                     >> 0x00000010U)))) 
                                          & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__hdr_ctlr_eid_r 
                                             == (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__rows_r[9U][3U])) 
                                                  << 0x00000020U) 
                                                 | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__rows_r[9U][2U]))))))) 
                                     << 1U) | ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT____Vcellinp__u_notify__rx_cmd_valid_i) 
                                               & (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__valid_r) 
                                                   >> 8U) 
                                                  & ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__hdr_src_mac_r 
                                                      == 
                                                      (0x0000ffffffffffffULL 
                                                       & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__rows_r[8U][1U])) 
                                                           << 0x00000010U) 
                                                          | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__rows_r[8U][0U])) 
                                                             >> 0x00000010U)))) 
                                                     & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__hdr_ctlr_eid_r 
                                                        == 
                                                        (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__rows_r[8U][3U])) 
                                                          << 0x00000020U) 
                                                         | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__rows_r[8U][2U]))))))))) 
                                << 8U)) | (((((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT____Vcellinp__u_notify__rx_cmd_valid_i) 
                                                & (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__valid_r) 
                                                    >> 7U) 
                                                   & ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__hdr_src_mac_r 
                                                       == 
                                                       (0x0000ffffffffffffULL 
                                                        & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__rows_r[7U][1U])) 
                                                            << 0x00000010U) 
                                                           | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__rows_r[7U][0U])) 
                                                              >> 0x00000010U)))) 
                                                      & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__hdr_ctlr_eid_r 
                                                         == 
                                                         (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__rows_r[7U][3U])) 
                                                           << 0x00000020U) 
                                                          | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__rows_r[7U][2U]))))))) 
                                               << 3U) 
                                              | (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT____Vcellinp__u_notify__rx_cmd_valid_i) 
                                                  & (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__valid_r) 
                                                      >> 6U) 
                                                     & ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__hdr_src_mac_r 
                                                         == 
                                                         (0x0000ffffffffffffULL 
                                                          & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__rows_r[6U][1U])) 
                                                              << 0x00000010U) 
                                                             | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__rows_r[6U][0U])) 
                                                                >> 0x00000010U)))) 
                                                        & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__hdr_ctlr_eid_r 
                                                           == 
                                                           (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__rows_r[6U][3U])) 
                                                             << 0x00000020U) 
                                                            | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__rows_r[6U][2U]))))))) 
                                                 << 2U)) 
                                             | ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT____Vcellinp__u_notify__rx_cmd_valid_i) 
                                                  & (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__valid_r) 
                                                      >> 5U) 
                                                     & ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__hdr_src_mac_r 
                                                         == 
                                                         (0x0000ffffffffffffULL 
                                                          & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__rows_r[5U][1U])) 
                                                              << 0x00000010U) 
                                                             | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__rows_r[5U][0U])) 
                                                                >> 0x00000010U)))) 
                                                        & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__hdr_ctlr_eid_r 
                                                           == 
                                                           (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__rows_r[5U][3U])) 
                                                             << 0x00000020U) 
                                                            | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__rows_r[5U][2U]))))))) 
                                                 << 1U) 
                                                | ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT____Vcellinp__u_notify__rx_cmd_valid_i) 
                                                   & (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__valid_r) 
                                                       >> 4U) 
                                                      & ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__hdr_src_mac_r 
                                                          == 
                                                          (0x0000ffffffffffffULL 
                                                           & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__rows_r[4U][1U])) 
                                                               << 0x00000010U) 
                                                              | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__rows_r[4U][0U])) 
                                                                 >> 0x00000010U)))) 
                                                         & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__hdr_ctlr_eid_r 
                                                            == 
                                                            (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__rows_r[4U][3U])) 
                                                              << 0x00000020U) 
                                                             | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__rows_r[4U][2U]))))))))) 
                                            << 4U) 
                                           | (((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT____Vcellinp__u_notify__rx_cmd_valid_i) 
                                                 & (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__valid_r) 
                                                     >> 3U) 
                                                    & ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__hdr_src_mac_r 
                                                        == 
                                                        (0x0000ffffffffffffULL 
                                                         & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__rows_r[3U][1U])) 
                                                             << 0x00000010U) 
                                                            | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__rows_r[3U][0U])) 
                                                               >> 0x00000010U)))) 
                                                       & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__hdr_ctlr_eid_r 
                                                          == 
                                                          (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__rows_r[3U][3U])) 
                                                            << 0x00000020U) 
                                                           | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__rows_r[3U][2U]))))))) 
                                                << 3U) 
                                               | (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT____Vcellinp__u_notify__rx_cmd_valid_i) 
                                                   & (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__valid_r) 
                                                       >> 2U) 
                                                      & ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__hdr_src_mac_r 
                                                          == 
                                                          (0x0000ffffffffffffULL 
                                                           & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__rows_r[2U][1U])) 
                                                               << 0x00000010U) 
                                                              | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__rows_r[2U][0U])) 
                                                                 >> 0x00000010U)))) 
                                                         & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__hdr_ctlr_eid_r 
                                                            == 
                                                            (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__rows_r[2U][3U])) 
                                                              << 0x00000020U) 
                                                             | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__rows_r[2U][2U]))))))) 
                                                  << 2U)) 
                                              | ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT____Vcellinp__u_notify__rx_cmd_valid_i) 
                                                   & (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__valid_r) 
                                                       >> 1U) 
                                                      & ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__hdr_src_mac_r 
                                                          == 
                                                          (0x0000ffffffffffffULL 
                                                           & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__rows_r[1U][1U])) 
                                                               << 0x00000010U) 
                                                              | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__rows_r[1U][0U])) 
                                                                 >> 0x00000010U)))) 
                                                         & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__hdr_ctlr_eid_r 
                                                            == 
                                                            (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__rows_r[1U][3U])) 
                                                              << 0x00000020U) 
                                                             | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__rows_r[1U][2U]))))))) 
                                                  << 1U) 
                                                 | ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT____Vcellinp__u_notify__rx_cmd_valid_i) 
                                                    & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__valid_r) 
                                                       & ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__hdr_src_mac_r 
                                                           == 
                                                           (0x0000ffffffffffffULL 
                                                            & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__rows_r[0U][1U])) 
                                                                << 0x00000010U) 
                                                               | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__rows_r[0U][0U])) 
                                                                  >> 0x00000010U)))) 
                                                          & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__hdr_ctlr_eid_r 
                                                             == 
                                                             (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__rows_r[0U][3U])) 
                                                               << 0x00000020U) 
                                                              | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__rows_r[0U][2U])))))))))));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_286 = ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__rsp_busy_w)) 
                                                  & (0U 
                                                     == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__a_st_r)));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__row_mac_w 
        = (0x0000ffffffffffffULL & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__rows_r
                                                     [
                                                     ((4U 
                                                       == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__n_st_r))
                                                       ? (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__pd_ix_w)
                                                       : (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__wk_ix_r))][1U])) 
                                     << 0x00000010U) 
                                    | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__rows_r
                                                       [
                                                       ((4U 
                                                         == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__n_st_r))
                                                         ? (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__pd_ix_w)
                                                         : (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__wk_ix_r))][0U])) 
                                       >> 0x00000010U)));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_116 = (0x0000ffffU 
                                                  & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__rows_r
                                                  [
                                                  ((4U 
                                                    == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__n_st_r))
                                                    ? (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__pd_ix_w)
                                                    : (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__wk_ix_r))][0U]);
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__row_eid_w 
        = (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__rows_r
                            [((4U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__n_st_r))
                               ? (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__pd_ix_w)
                               : (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__wk_ix_r))][3U])) 
            << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__rows_r
                                              [((4U 
                                                 == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__n_st_r))
                                                 ? (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__pd_ix_w)
                                                 : (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__wk_ix_r))][2U])));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_227 = ((4U 
                                                   == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__n_st_r)) 
                                                  & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__ca_probe_r) 
                                                     >> (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__pd_ix_w)));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_69 = ((8U 
                                                  == 
                                                  (0x0000000fU 
                                                   & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r))) 
                                                 & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__gate_acc_w));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_72 = ((7U 
                                                  == 
                                                  (0x0000000fU 
                                                   & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r))) 
                                                 & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__gate_acc_w));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_75 = ((6U 
                                                  == 
                                                  (0x0000000fU 
                                                   & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r))) 
                                                 & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__gate_acc_w));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_78 = ((5U 
                                                  == 
                                                  (0x0000000fU 
                                                   & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r))) 
                                                 & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__gate_acc_w));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_81 = ((4U 
                                                  == 
                                                  (0x0000000fU 
                                                   & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r))) 
                                                 & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__gate_acc_w));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_84 = ((3U 
                                                  == 
                                                  (0x0000000fU 
                                                   & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r))) 
                                                 & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__gate_acc_w));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_87 = ((2U 
                                                  == 
                                                  (0x0000000fU 
                                                   & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r))) 
                                                 & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__gate_acc_w));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_90 = ((1U 
                                                  == 
                                                  (0x0000000fU 
                                                   & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r))) 
                                                 & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__gate_acc_w));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_142 = ((0U 
                                                   == 
                                                   (0x0000000fU 
                                                    & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r))) 
                                                  & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__gate_acc_w));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_409 = (7U 
                                                  & ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_cnt_r 
                                                      >> 3U) 
                                                     - 
                                                     (1U 
                                                      & (- (IData)((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_428))))));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_426 = (((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_428) 
                                                   << 1U) 
                                                  | (0U 
                                                     != 
                                                     (7U 
                                                      & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_cnt_r)));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__4__KET____DOT__u_rx_slots__DOT__rd_maddr_w 
        = (0x00000fffU & (((IData)(0x0240U) * (3U & 
                                               (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_acmp_q__DOT__out_data_r[1U] 
                                                >> 0x00000019U))) 
                          + (0x000003ffU & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pf_idx_r) 
                                            + ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__acmp_is_tkr_w)
                                                ? 0x0014U
                                                : 0x001cU)))));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_167 = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__acmp_is_tkr_w)
                                                   ? 
                                                  ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__gp_valid_r)) 
                                                   & (1U 
                                                      == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__state_r)))
                                                   : (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__lstn_txn_ready_w));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_rx_hit_w 
        = (((((((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_1) 
                & (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rec_valid_r) 
                    >> 8U) & ((3U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_attr_type_w)) 
                              & ((5U >= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_mrp_event_w)) 
                                 & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_189))))) 
               << 4U) | ((((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_1) 
                           & (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rec_valid_r) 
                               >> 7U) & ((3U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_attr_type_w)) 
                                         & ((5U >= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_mrp_event_w)) 
                                            & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_188))))) 
                          << 3U) | (((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_1) 
                                     & (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rec_valid_r) 
                                         >> 6U) & (
                                                   (3U 
                                                    == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_attr_type_w)) 
                                                   & ((5U 
                                                       >= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_mrp_event_w)) 
                                                      & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_187))))) 
                                    << 2U))) | ((((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_1) 
                                                  & (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rec_valid_r) 
                                                      >> 5U) 
                                                     & ((3U 
                                                         == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_attr_type_w)) 
                                                        & ((5U 
                                                            >= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_mrp_event_w)) 
                                                           & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_186))))) 
                                                 << 1U) 
                                                | ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_1) 
                                                   & (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rec_valid_r) 
                                                       >> 4U) 
                                                      & ((3U 
                                                          == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_attr_type_w)) 
                                                         & ((5U 
                                                             >= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_mrp_event_w)) 
                                                            & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_185))))))) 
            << 4U) | (((((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_1) 
                         & (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rec_valid_r) 
                             >> 3U) & ((3U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_attr_type_w)) 
                                       & ((5U >= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_mrp_event_w)) 
                                          & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_184))))) 
                        << 3U) | (((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_1) 
                                   & (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rec_valid_r) 
                                       >> 2U) & ((3U 
                                                  == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_attr_type_w)) 
                                                 & ((5U 
                                                     >= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_mrp_event_w)) 
                                                    & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_183))))) 
                                  << 2U)) | ((((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_1) 
                                               & (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rec_valid_r) 
                                                   >> 1U) 
                                                  & ((3U 
                                                      == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_attr_type_w)) 
                                                     & ((5U 
                                                         >= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_mrp_event_w)) 
                                                        & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_182))))) 
                                              << 1U) 
                                             | ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_1) 
                                                & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rec_valid_r) 
                                                   & ((3U 
                                                       == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_attr_type_w)) 
                                                      & ((5U 
                                                          >= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_mrp_event_w)) 
                                                         & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_181))))))));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_144 = ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_1) 
                                                  & (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__armed_r) 
                                                      >> 8U) 
                                                     & ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_3) 
                                                        & ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_189) 
                                                           & ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_da_w 
                                                               == 
                                                               (0x0000ffffffffffffULL 
                                                                & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__da_r[13U])) 
                                                                    << 0x00000020U) 
                                                                   | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__da_r[12U]))))) 
                                                              & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_vid_w) 
                                                                 == 
                                                                 (0x00000fffU 
                                                                  & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vid_r[3U])))))));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_145 = ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_1) 
                                                  & (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__armed_r) 
                                                      >> 7U) 
                                                     & ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_3) 
                                                        & ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_188) 
                                                           & ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_da_w 
                                                               == 
                                                               (0x0000ffffffffffffULL 
                                                                & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__da_r[11U])) 
                                                                    << 0x00000010U) 
                                                                   | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__da_r[10U])) 
                                                                      >> 0x00000010U)))) 
                                                              & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_vid_w) 
                                                                 == 
                                                                 (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vid_r[2U] 
                                                                  >> 0x00000014U)))))));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_146 = ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_1) 
                                                  & (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__armed_r) 
                                                      >> 6U) 
                                                     & ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_3) 
                                                        & ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_187) 
                                                           & ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_da_w 
                                                               == 
                                                               (0x0000ffffffffffffULL 
                                                                & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__da_r[10U])) 
                                                                    << 0x00000020U) 
                                                                   | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__da_r[9U]))))) 
                                                              & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_vid_w) 
                                                                 == 
                                                                 (0x00000fffU 
                                                                  & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vid_r[2U] 
                                                                     >> 8U))))))));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_147 = ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_1) 
                                                  & (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__armed_r) 
                                                      >> 5U) 
                                                     & ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_3) 
                                                        & ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_186) 
                                                           & ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_da_w 
                                                               == 
                                                               (0x0000ffffffffffffULL 
                                                                & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__da_r[8U])) 
                                                                    << 0x00000010U) 
                                                                   | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__da_r[7U])) 
                                                                      >> 0x00000010U)))) 
                                                              & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_vid_w) 
                                                                 == 
                                                                 (0x00000fffU 
                                                                  & ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vid_r[2U] 
                                                                      << 4U) 
                                                                     | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vid_r[1U] 
                                                                        >> 0x0000001cU)))))))));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_148 = ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_1) 
                                                  & (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__armed_r) 
                                                      >> 4U) 
                                                     & ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_3) 
                                                        & ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_185) 
                                                           & ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_da_w 
                                                               == 
                                                               (0x0000ffffffffffffULL 
                                                                & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__da_r[7U])) 
                                                                    << 0x00000020U) 
                                                                   | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__da_r[6U]))))) 
                                                              & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_vid_w) 
                                                                 == 
                                                                 (0x00000fffU 
                                                                  & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vid_r[1U] 
                                                                     >> 0x00000010U))))))));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_149 = ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_1) 
                                                  & (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__armed_r) 
                                                      >> 3U) 
                                                     & ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_3) 
                                                        & ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_184) 
                                                           & ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_da_w 
                                                               == 
                                                               (0x0000ffffffffffffULL 
                                                                & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__da_r[5U])) 
                                                                    << 0x00000010U) 
                                                                   | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__da_r[4U])) 
                                                                      >> 0x00000010U)))) 
                                                              & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_vid_w) 
                                                                 == 
                                                                 (0x00000fffU 
                                                                  & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vid_r[1U] 
                                                                     >> 4U))))))));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_150 = ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_1) 
                                                  & (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__armed_r) 
                                                      >> 2U) 
                                                     & ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_3) 
                                                        & ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_183) 
                                                           & ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_da_w 
                                                               == 
                                                               (0x0000ffffffffffffULL 
                                                                & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__da_r[4U])) 
                                                                    << 0x00000020U) 
                                                                   | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__da_r[3U]))))) 
                                                              & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_vid_w) 
                                                                 == 
                                                                 (0x00000fffU 
                                                                  & ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vid_r[1U] 
                                                                      << 8U) 
                                                                     | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vid_r[0U] 
                                                                        >> 0x00000018U)))))))));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_151 = ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_1) 
                                                  & (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__armed_r) 
                                                      >> 1U) 
                                                     & ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_3) 
                                                        & ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_182) 
                                                           & ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_da_w 
                                                               == 
                                                               (0x0000ffffffffffffULL 
                                                                & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__da_r[2U])) 
                                                                    << 0x00000010U) 
                                                                   | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__da_r[1U])) 
                                                                      >> 0x00000010U)))) 
                                                              & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_vid_w) 
                                                                 == 
                                                                 (0x00000fffU 
                                                                  & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vid_r[0U] 
                                                                     >> 0x0000000cU))))))));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_152 = ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_1) 
                                                  & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__armed_r) 
                                                     & ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_3) 
                                                        & ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_181) 
                                                           & ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_da_w 
                                                               == 
                                                               (0x0000ffffffffffffULL 
                                                                & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__da_r[1U])) 
                                                                    << 0x00000020U) 
                                                                   | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__da_r[0U]))))) 
                                                              & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_vid_w) 
                                                                 == 
                                                                 (0x00000fffU 
                                                                  & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vid_r[0U])))))));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_350 = (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rec_valid_r) 
                                                   >> 8U) 
                                                  & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_1));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_351 = (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rec_valid_r) 
                                                   >> 7U) 
                                                  & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_1));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_352 = (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rec_valid_r) 
                                                   >> 6U) 
                                                  & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_1));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_353 = (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rec_valid_r) 
                                                   >> 5U) 
                                                  & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_1));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_354 = (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rec_valid_r) 
                                                   >> 4U) 
                                                  & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_1));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_355 = (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rec_valid_r) 
                                                   >> 3U) 
                                                  & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_1));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_356 = (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rec_valid_r) 
                                                   >> 2U) 
                                                  & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_1));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_357 = (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rec_valid_r) 
                                                   >> 1U) 
                                                  & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_1));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_358 = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rec_valid_r) 
                                                  & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_1));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_17 = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__declaring_r) 
                                                 & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__adm_admitted_w));
    vlSelfRef.milan_datapath__DOT__crft_emit_en_w = 
        (1U & (vlSelfRef.milan_datapath__DOT__csr__DOT__crft_ctrl 
               & (((vlSelfRef.milan_datapath__DOT__csr__DOT__aaf_ctrl 
                    >> 1U) | (3U != (3U & vlSelfRef.milan_datapath__DOT__csr__DOT__lwsrp_ctrl))) 
                  | ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__adm_admitted_w) 
                     >> 8U))));
    vlSelfRef.milan_datapath__DOT__aaf_gate = (((vlSelfRef.milan_datapath__DOT__csr__DOT__aaf_ctrl 
                                                 >> 1U) 
                                                | (((~ vlSelfRef.milan_datapath__DOT__csr__DOT__lwsrp_ctrl) 
                                                    | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__adm_admitted_w)) 
                                                   & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__declaring_r))) 
                                               & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_14));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__sr_adm_fsm_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__opt_r) 
           | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__adm_admitted_w));
    vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__diag_ridx_w 
        = (7U & ((IData)(vlSelfRef.milan_datapath__DOT__aecp_diag_idx_w) 
                 & (- (IData)((8U > (IData)(vlSelfRef.milan_datapath__DOT__aecp_diag_idx_w))))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__beat_w 
        = ((IData)(vlSelfRef.i_resp_mem_rsp_valid) 
           & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_285));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT____Vcellout__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__alloc_gnt_o 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__alloc_req_r) 
           & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__DOT__wr_active_r)) 
              & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__DOT__ff_valid_w)));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT____Vcellout__g_rx_pool__BRA__4__KET____DOT__u_rx_slots__alloc_gnt_o 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__alloc_req_r) 
           & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__4__KET____DOT__u_rx_slots__DOT__wr_active_r)) 
              & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__4__KET____DOT__u_rx_slots__DOT__ff_valid_w)));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT____Vcellout__g_rx_pool__BRA__2__KET____DOT__u_rx_slots__alloc_gnt_o 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__alloc_req_r) 
           & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__2__KET____DOT__u_rx_slots__DOT__wr_active_r)) 
              & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__2__KET____DOT__u_rx_slots__DOT__ff_valid_w)));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT____Vcellout__g_rx_pool__BRA__1__KET____DOT__u_rx_slots__alloc_gnt_o 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__alloc_req_r) 
           & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__1__KET____DOT__u_rx_slots__DOT__wr_active_r)) 
              & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__1__KET____DOT__u_rx_slots__DOT__ff_valid_w)));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__maap_rsp_tmo_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__maap_busy_r) 
           & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__maap_rsp_live_w)) 
              & (0x00002710U <= (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__now_ms_r 
                                 - vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__maap_t0_r))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__clr_relq_w = 0U;
    if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__maap_accept_w) 
         & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__mreq_rel_r))) {
        if ((8U >= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__mreq_src_r))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__clr_relq_w 
                = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__clr_relq_w) 
                   | (0x01ffU & ((IData)(1U) << (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__mreq_src_r))));
        }
    }
    vlSelfRef.milan_datapath__DOT__avtprx_accept_p 
        = ((~ (IData)(milan_datapath__DOT__avtprx_stopped_w)) 
           & (IData)(vlSelfRef.milan_datapath__DOT__avtprx_accept_p_w));
    vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__ch1_w 
        = (0x0000000fU & (((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__chpos_r)) 
                          & (- (IData)(((IData)(vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__eff_chans_w) 
                                        != (0x0000000fU 
                                            & ((IData)(1U) 
                                               + (IData)(vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__chpos_r))))))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__fsm_rd_gnt_w 
        = ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__cap_active_w)) 
           & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__fsm_rd_req_w));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__rd_addr_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__cap_active_w)
            ? (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__recwr_addr_w)
            : ((5U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__hs_r))
                ? (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__rp_k_r)
                : (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__fl_sink_r)));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__pick_w = 0U;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__pick_ok_w = 0U;
    if (milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pool_oversize_w) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__pick_w = 4U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__pick_ok_w 
            = (0U == vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__st_r[4U]);
    } else {
        if ((0U == vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__st_r[3U])) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__pick_w = 3U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__pick_ok_w = 1U;
        }
        if ((0U == vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__st_r[2U])) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__pick_w = 2U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__pick_ok_w = 1U;
        }
        if ((0U == vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__st_r[1U])) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__pick_w = 1U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__pick_ok_w = 1U;
        }
        if ((0U == vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__st_r[0U])) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__pick_w = 0U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__pick_ok_w = 1U;
        }
    }
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_157 = ((0x40U 
                                                   > (IData)(vlSelfRef.milan_datapath__DOT__amap_walk_j_r)) 
                                                  & (IData)(milan_datapath__DOT__amap_opage_ok_w));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__eof_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__out_last_r) 
           & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__consume_w));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__push_w 
        = ((IData)(__VdfgRegularize_h6e95ff9d_0_403) 
           & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_normalizer__DOT__txn_valid_r));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__nrm_txn_ready_w 
        = ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_296) 
           | ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_295) 
              | ((IData)(__VdfgRegularize_h6e95ff9d_0_403) 
                 | (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_294))));
    if (vlSelfRef.__VdfgRegularize_h6e95ff9d_0_47) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__name_wdata_w 
            = vlSelfRef.i_desc_mem_rsp_data;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__name_waddr_w 
            = (0x000003ffU & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__name_load_lane_r 
                              + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__beat_ix_r)));
    } else {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__name_wdata_w 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__opa_e_r;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__name_waddr_w 
            = (0x000003ffU & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__st_addr_w 
                              >> 3U));
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__name_wstrb_w 
        = (0x000000ffU & (Vmilan_datapath__ConstPool__CONST_h5302cfd2_0
                          [(7U & (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__uop_e_r 
                                          >> 0x0000001cU)))] 
                          | (- (IData)((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_47)))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__need_flush_w 
        = ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_220) 
           & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__keep_w) 
              & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__lane_open_r) 
                 & ((0U != Vmilan_datapath__ConstPool__TABLE_h1b26f04f_0
                     [vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__sk_strb_r]) 
                    & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__lane_ix_r) 
                       != (0x0000007fU & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__babs_w) 
                                          >> 3U)))))));
    vlSelfRef.milan_datapath__DOT__talker_diag__DOT__ev_f_w = 0U;
    vlSelfRef.milan_datapath__DOT__talker_diag__DOT__ev_mr_w = 0U;
    vlSelfRef.milan_datapath__DOT__talker_diag__DOT__ev_tu_w = 0U;
    if (((IData)(vlSelfRef.milan_datapath__DOT____Vcellinp__media_clock_restart__frame_p_i) 
         & (9U > (IData)(vlSelfRef.milan_datapath__DOT__media_clock_restart__DOT__fidx_w)))) {
        if ((8U >= (IData)(vlSelfRef.milan_datapath__DOT__media_clock_restart__DOT__fidx_w))) {
            vlSelfRef.milan_datapath__DOT__talker_diag__DOT__ev_f_w 
                = ((IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__ev_f_w) 
                   | (0x01ffU & ((IData)(1U) << (IData)(vlSelfRef.milan_datapath__DOT__media_clock_restart__DOT__fidx_w))));
        }
        if (((IData)(vlSelfRef.milan_datapath__DOT____Vcellinp__media_clock_restart__frame_mr_i) 
             != ((8U >= (IData)(vlSelfRef.milan_datapath__DOT__media_clock_restart__DOT__fidx_w)) 
                 && (1U & ((IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__mr_q_r) 
                           >> (IData)(vlSelfRef.milan_datapath__DOT__media_clock_restart__DOT__fidx_w)))))) {
            if ((8U >= (IData)(vlSelfRef.milan_datapath__DOT__media_clock_restart__DOT__fidx_w))) {
                vlSelfRef.milan_datapath__DOT__talker_diag__DOT__ev_mr_w 
                    = ((IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__ev_mr_w) 
                       | (0x01ffU & ((IData)(1U) << (IData)(vlSelfRef.milan_datapath__DOT__media_clock_restart__DOT__fidx_w))));
            }
        }
        if (((IData)(vlSelfRef.milan_datapath__DOT__aaf_frame_p_w)
              ? (IData)(vlSelfRef.milan_datapath__DOT__aaf_frame_tu_w)
              : (IData)(vlSelfRef.milan_datapath__DOT__crft_tu_last_w))) {
            if ((8U >= (IData)(vlSelfRef.milan_datapath__DOT__media_clock_restart__DOT__fidx_w))) {
                vlSelfRef.milan_datapath__DOT__talker_diag__DOT__ev_tu_w 
                    = ((IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__ev_tu_w) 
                       | (0x01ffU & ((IData)(1U) << (IData)(vlSelfRef.milan_datapath__DOT__media_clock_restart__DOT__fidx_w))));
            }
        }
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__refuse_w 
        = ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__fit_w)) 
           & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_298));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__wgrant_now_w 
        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__wgrant_r;
    if ((8U >= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__aidx_r))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__wgrant_now_w 
            = (((~ ((IData)(1U) << (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__aidx_r))) 
                & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__wgrant_now_w)) 
               | (0x01ffU & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__fit_w) 
                             << (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__aidx_r))));
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__wgslope_now_w[0U] 
        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__wgslope_r[0U];
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__wgslope_now_w[1U] 
        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__wgslope_r[1U];
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__wgslope_now_w[2U] 
        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__wgslope_r[2U];
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__wgslope_now_w[3U] 
        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__wgslope_r[3U];
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__wgslope_now_w[4U] 
        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__wgslope_r[4U];
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__wgslope_now_w[5U] 
        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__wgslope_r[5U];
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__wgslope_now_w[6U] 
        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__wgslope_r[6U];
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__wgslope_now_w[7U] 
        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__wgslope_r[7U];
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__wgslope_now_w[8U] 
        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__wgslope_r[8U];
    if ((0x011fU >= (0x000001ffU & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__aidx_r) 
                                    << 5U)))) {
        VL_ASSIGNSEL_WI(288, 32, (0x000001ffU & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__aidx_r) 
                                                 << 5U)), vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__wgslope_now_w, 
                        ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__fit_w)
                          ? ((0x011fU >= (0x000001ffU 
                                          & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__aidx_r) 
                                             << 5U)))
                              ? vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__slope_q_r
                             [(0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__aidx_r))]
                              : 0U) : 0U));
    }
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_35 = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_side_port__DOT__fwd_ok_w) 
                                                 & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_side_port__DOT__accept_w));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__ls_user_ready_w 
        = ((0U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__st_r)) 
           & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__vu_sel_ls_w));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tk_user_ready_w 
        = ((0U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__st_r)) 
           & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__vu_sel_ls_w)) 
              & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vsel_v_w)));
    vlSelfRef.milan_datapath__DOT__media_grid_align__DOT__diff_w 
        = (vlSelfRef.milan_datapath__DOT__media_grid_align__DOT__base_w 
           - VL_EXTENDS_II(32,16, (IData)(vlSelfRef.milan_datapath__DOT__media_grid_align__DOT__err_r)));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__sb_rel_acmp_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__acmp_sb_active_r) 
           & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__acmp_sb_done_pending_r) 
              | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__acmp_sb_done_w)));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_397 = ((IData)(milan_datapath__DOT__amap_opage_ok_w) 
                                                  | (IData)(milan_datapath__DOT__amap_page_ok_w));
    vlSelfRef.milan_datapath__DOT__amap_in_rec_w = 0ULL;
    milan_datapath__DOT__amap_page_fmt__DOT__offq_c 
        = (((IData)(milan_datapath__DOT__amap_page_ok_w)
             ? (IData)(vlSelfRef.milan_datapath__DOT__amapq_map_r)
             : 0U) + (IData)(vlSelfRef.milan_datapath__DOT__amap_walk_jq_r));
    if ((IData)((0x80U == (0xc0U & (IData)(vlSelfRef.milan_datapath__DOT__amap_in_ent_q_r))))) {
        vlSelfRef.milan_datapath__DOT__amap_in_rec_w 
            = (((QData)((IData)(((0x00070000U & ((IData)(vlSelfRef.milan_datapath__DOT__amap_in_ent_q_r) 
                                                 << 0x0000000dU)) 
                                 | (7U & (IData)(vlSelfRef.milan_datapath__DOT__amap_in_ent_q_r))))) 
                << 0x00000020U) | (QData)((IData)((milan_datapath__DOT__amap_page_fmt__DOT__offq_c 
                                                   << 0x00000010U))));
    }
    milan_datapath__DOT__amap_page_slot__DOT__off_c 
        = (((IData)(milan_datapath__DOT__amap_page_ok_w)
             ? (IData)(vlSelfRef.milan_datapath__DOT__amapq_map_r)
             : 0U) + (IData)(vlSelfRef.milan_datapath__DOT__amap_walk_j_r));
    milan_datapath__DOT__amap_page_slot__DOT__g_c = 
        ((IData)(vlSelfRef.milan_datapath__DOT__amap_in_pbase_w) 
         + milan_datapath__DOT__amap_page_slot__DOT__off_c);
    vlSelfRef.milan_datapath__DOT__amap_in_ent_w = 
        (((((IData)(milan_datapath__DOT__amap_page_ok_w) 
            & (1U > (IData)(vlSelfRef.milan_datapath__DOT__amap_walk_j_r))) 
           & (milan_datapath__DOT__amap_page_slot__DOT__off_c 
              < (IData)(vlSelfRef.milan_datapath__DOT__amap_in_pcls_w))) 
          & (1U > milan_datapath__DOT__amap_page_slot__DOT__g_c))
          ? (0x000000ffU & (IData)(vlSelfRef.milan_datapath__DOT__amap_in_store_r))
          : 0U);
    vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__lb_smp0_w 
        = ((0x00ff0000U & ((IData)(milan_datapath__DOT__lb_tap_tdata_w) 
                           << 0x00000010U)) | ((0x0000ff00U 
                                                & ((IData)(
                                                           (milan_datapath__DOT__lb_tap_tdata_w 
                                                            >> 8U)) 
                                                   << 8U)) 
                                               | (0x000000ffU 
                                                  & (IData)(
                                                            (milan_datapath__DOT__lb_tap_tdata_w 
                                                             >> 0x00000010U)))));
    vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__lb_smp1_w 
        = ((0x00ff0000U & ((IData)((milan_datapath__DOT__lb_tap_tdata_w 
                                    >> 0x00000020U)) 
                           << 0x00000010U)) | ((0x0000ff00U 
                                                & ((IData)(
                                                           (milan_datapath__DOT__lb_tap_tdata_w 
                                                            >> 0x00000028U)) 
                                                   << 8U)) 
                                               | (0x000000ffU 
                                                  & (IData)(
                                                            (milan_datapath__DOT__lb_tap_tdata_w 
                                                             >> 0x00000030U)))));
    vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__push_same_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__push_ram_w) 
           & ((vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__skid_addr_r
               [vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__skid_rp_r] 
               == (0x0000001fU & (IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__pop_idx_r))) 
              & (IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__pop_act_w)));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__aecp_rgy_req_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gx_req_w) 
           & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__rgy_any_w));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__evr_strobe_w 
        = ((((((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_382) 
               << 0x0000000dU) | ((IData)(vlSelfRef.milan_datapath__DOT__pp_gm_change_p_w) 
                                  << 0x0000000cU)) 
             | (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_lstn_reg_change_w) 
                 << 3U) | (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_evt_domain_change_w) 
                            << 2U) | ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__adp_evt_valid_w) 
                                        & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__adp_evt_departed_w)) 
                                       << 1U) | ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__adp_evt_departed_w)) 
                                                 & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__adp_evt_valid_w)))))) 
            << 0x00000012U) | (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_evt_tk_unreg_w) 
                                << 9U) | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_evt_tk_reg_w)));
    vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__fire 
        = ((((IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__in_acc) 
             & (0x80U == (0xf0U & (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__b1)))) 
            & (~ (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__parsed))) 
           & ((((((0x38U <= (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__bytes_in)) 
                  & (0x01bfU >= (0x000001ffU & (((IData)(0x01bfU) 
                                                 - 
                                                 ((IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__et_off) 
                                                  << 3U)) 
                                                - (IData)(7U))))) 
                 & (0x22U == (0x000000ffU & (((0U == 
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
                                                    - (IData)(7U)))))))) 
                & (0x01bfU >= (0x000001ffU & (((IData)(0x01bfU) 
                                               - (0x000001f8U 
                                                  & (((IData)(1U) 
                                                      + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__et_off)) 
                                                     << 3U))) 
                                              - (IData)(7U))))) 
               & (0xf0U == (0x000000ffU & (((0U == 
                                             (0x0000001fU 
                                              & (((IData)(0x01bfU) 
                                                  - 
                                                  (0x000001f8U 
                                                   & (((IData)(1U) 
                                                       + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__et_off)) 
                                                      << 3U))) 
                                                 - (IData)(7U))))
                                             ? 0U : 
                                            (vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__hdr
                                             [(((IData)(7U) 
                                                + (0x000001ffU 
                                                   & (((IData)(0x01bfU) 
                                                       - 
                                                       (0x000001f8U 
                                                        & (((IData)(1U) 
                                                            + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__et_off)) 
                                                           << 3U))) 
                                                      - (IData)(7U)))) 
                                               >> 5U)] 
                                             << ((IData)(0x00000020U) 
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
                                                     - 
                                                     (0x000001f8U 
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
                                                     - (IData)(7U)))))))) 
              & (7U >= (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__subtype))));
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
    vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ram_we_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__eng_we_w) 
           | (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ext_wr_ok_w));
    vlSelfRef.milan_datapath__DOT__crf_rx__DOT__w_ev_uf_w 
        = ((~ (IData)(vlSelfRef.milan_datapath__DOT__crf_rx__DOT__w_fmt_ok)) 
           & (IData)(vlSelfRef.milan_datapath__DOT__crf_rx__DOT__w_hit));
    vlSelfRef.milan_datapath__DOT__crf_rx__DOT__w_acc 
        = ((IData)(vlSelfRef.milan_datapath__DOT__crf_rx__DOT__w_hit) 
           & (IData)(vlSelfRef.milan_datapath__DOT__crf_rx__DOT__w_fmt_ok));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__byte_ok_w 
        = (1U & ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_133) 
                 | ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__echo_r) 
                    | ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__pay_w)) 
                       | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__rsp_rd_valid_w)))));
    vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__own_last_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pown_o_w) 
           == (3U & ((vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__chans_r
                      [vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pown_t_w] 
                      >> 1U) - (IData)(1U))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__cmp_z_w 
        = ((3U == (7U & (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__uop_e_r 
                                 >> 0x0000001cU))))
            ? (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__opa_e_r 
               == vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__b_or_imm_w)
            : (0U == (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_223)));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_273 = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__eff_len_w) 
                                                  + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__nvm_offset_w));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__ctr_ev_ok_w = 0U;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__ctr_ev_ix_w = 0U;
    if (((5U == (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_evt_type_w)) 
         & (9U > (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_evt_index_w)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__ctr_ev_ok_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__ctr_ev_ix_w 
            = (0x0000001fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_evt_index_w));
    } else if (((6U == (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_evt_type_w)) 
                & (9U > (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_evt_index_w)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__ctr_ev_ok_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__ctr_ev_ix_w 
            = (0x0000001fU & ((IData)(9U) + (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_evt_index_w)));
    } else if (((9U == (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_evt_type_w)) 
                & (0U == (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_evt_index_w)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__ctr_ev_ok_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__ctr_ev_ix_w = 0x12U;
    } else if (((0x0024U == (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_evt_type_w)) 
                & (0U == (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_evt_index_w)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__ctr_ev_ok_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__ctr_ev_ix_w = 0x13U;
    }
    vlSelfRef.milan_datapath__DOT__pp_ctr_sout_pend_n 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_sout_pend_r) 
           | (IData)(vlSelfRef.milan_datapath__DOT__tkd_dirty_p_w));
    if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_evt_valid_w) 
          & (6U == (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_evt_type_w))) 
         & (0U == (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_evt_index_w)))) {
        vlSelfRef.milan_datapath__DOT__pp_ctr_sout_pend_n 
            = (0x01feU & (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_sout_pend_n));
    }
    if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_evt_valid_w) 
          & (6U == (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_evt_type_w))) 
         & (1U == (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_evt_index_w)))) {
        vlSelfRef.milan_datapath__DOT__pp_ctr_sout_pend_n 
            = (0x01fdU & (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_sout_pend_n));
    }
    if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_evt_valid_w) 
          & (6U == (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_evt_type_w))) 
         & (2U == (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_evt_index_w)))) {
        vlSelfRef.milan_datapath__DOT__pp_ctr_sout_pend_n 
            = (0x01fbU & (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_sout_pend_n));
    }
    if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_evt_valid_w) 
          & (6U == (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_evt_type_w))) 
         & (3U == (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_evt_index_w)))) {
        vlSelfRef.milan_datapath__DOT__pp_ctr_sout_pend_n 
            = (0x01f7U & (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_sout_pend_n));
    }
    if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_evt_valid_w) 
          & (6U == (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_evt_type_w))) 
         & (4U == (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_evt_index_w)))) {
        vlSelfRef.milan_datapath__DOT__pp_ctr_sout_pend_n 
            = (0x01efU & (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_sout_pend_n));
    }
    if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_evt_valid_w) 
          & (6U == (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_evt_type_w))) 
         & (5U == (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_evt_index_w)))) {
        vlSelfRef.milan_datapath__DOT__pp_ctr_sout_pend_n 
            = (0x01dfU & (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_sout_pend_n));
    }
    if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_evt_valid_w) 
          & (6U == (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_evt_type_w))) 
         & (6U == (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_evt_index_w)))) {
        vlSelfRef.milan_datapath__DOT__pp_ctr_sout_pend_n 
            = (0x01bfU & (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_sout_pend_n));
    }
    if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_evt_valid_w) 
          & (6U == (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_evt_type_w))) 
         & (7U == (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_evt_index_w)))) {
        vlSelfRef.milan_datapath__DOT__pp_ctr_sout_pend_n 
            = (0x017fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_sout_pend_n));
    }
    if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_evt_valid_w) 
          & (6U == (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_evt_type_w))) 
         & (8U == (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_evt_index_w)))) {
        vlSelfRef.milan_datapath__DOT__pp_ctr_sout_pend_n 
            = (0x00ffU & (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_sout_pend_n));
    }
    vlSelfRef.milan_datapath__DOT__pp_ctr_sin_pend_n 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_sin_pend_r) 
           | (((IData)(vlSelfRef.milan_datapath__DOT__crf_dirty_p_w) 
               << 8U) | (IData)(vlSelfRef.milan_datapath__DOT__avtprx_dirty_p_w)));
    if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_evt_valid_w) 
          & (5U == (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_evt_type_w))) 
         & (0U == (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_evt_index_w)))) {
        vlSelfRef.milan_datapath__DOT__pp_ctr_sin_pend_n 
            = (0x01feU & (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_sin_pend_n));
    }
    if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_evt_valid_w) 
          & (5U == (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_evt_type_w))) 
         & (1U == (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_evt_index_w)))) {
        vlSelfRef.milan_datapath__DOT__pp_ctr_sin_pend_n 
            = (0x01fdU & (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_sin_pend_n));
    }
    if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_evt_valid_w) 
          & (5U == (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_evt_type_w))) 
         & (2U == (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_evt_index_w)))) {
        vlSelfRef.milan_datapath__DOT__pp_ctr_sin_pend_n 
            = (0x01fbU & (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_sin_pend_n));
    }
    if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_evt_valid_w) 
          & (5U == (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_evt_type_w))) 
         & (3U == (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_evt_index_w)))) {
        vlSelfRef.milan_datapath__DOT__pp_ctr_sin_pend_n 
            = (0x01f7U & (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_sin_pend_n));
    }
    if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_evt_valid_w) 
          & (5U == (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_evt_type_w))) 
         & (4U == (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_evt_index_w)))) {
        vlSelfRef.milan_datapath__DOT__pp_ctr_sin_pend_n 
            = (0x01efU & (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_sin_pend_n));
    }
    if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_evt_valid_w) 
          & (5U == (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_evt_type_w))) 
         & (5U == (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_evt_index_w)))) {
        vlSelfRef.milan_datapath__DOT__pp_ctr_sin_pend_n 
            = (0x01dfU & (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_sin_pend_n));
    }
    if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_evt_valid_w) 
          & (5U == (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_evt_type_w))) 
         & (6U == (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_evt_index_w)))) {
        vlSelfRef.milan_datapath__DOT__pp_ctr_sin_pend_n 
            = (0x01bfU & (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_sin_pend_n));
    }
    if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_evt_valid_w) 
          & (5U == (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_evt_type_w))) 
         & (7U == (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_evt_index_w)))) {
        vlSelfRef.milan_datapath__DOT__pp_ctr_sin_pend_n 
            = (0x017fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_sin_pend_n));
    }
    if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_evt_valid_w) 
          & (5U == (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_evt_type_w))) 
         & (8U == (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_evt_index_w)))) {
        vlSelfRef.milan_datapath__DOT__pp_ctr_sin_pend_n 
            = (0x00ffU & (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_sin_pend_n));
    }
    vlSelfRef.milan_datapath__DOT__aaf_tx_tlast = (
                                                   (3U 
                                                    == (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__est_r)) 
                                                   & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_254));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__upc_w 
        = ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__aem_w) 
             & (4U == (0x0000ffffU & ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__out_data_r[4U] 
                                       << 4U) | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__out_data_r[3U] 
                                                 >> 0x0000001cU))))) 
            & (0x0014U <= (0x000007ffU & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__out_data_r[10U] 
                                          >> 0x0000000eU))))
            ? 0x0280U : ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__ctrs_w)
                          ? 0x0300U : ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_w)
                                        ? 0x0320U : 
                                       (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__aem_w) 
                                         & ((((0x0026U 
                                               == (0x0000ffffU 
                                                   & ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__out_data_r[4U] 
                                                       << 4U) 
                                                      | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__out_data_r[3U] 
                                                         >> 0x0000001cU)))) 
                                              | ((4U 
                                                  == 
                                                  (0x0000ffffU 
                                                   & ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__out_data_r[4U] 
                                                       << 4U) 
                                                      | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__out_data_r[3U] 
                                                         >> 0x0000001cU)))) 
                                                 & (0x0014U 
                                                    > 
                                                    (0x000007ffU 
                                                     & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__out_data_r[10U] 
                                                        >> 0x0000000eU))))) 
                                             | ((0x0029U 
                                                 == 
                                                 (0x0000ffffU 
                                                  & ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__out_data_r[4U] 
                                                      << 4U) 
                                                     | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__out_data_r[3U] 
                                                        >> 0x0000001cU)))) 
                                                & (0x0010U 
                                                   > 
                                                   (0x000007ffU 
                                                    & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__out_data_r[10U] 
                                                       >> 0x0000000eU))))) 
                                            | ((0x002bU 
                                                == 
                                                (0x0000ffffU 
                                                 & ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__out_data_r[4U] 
                                                     << 4U) 
                                                    | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__out_data_r[3U] 
                                                       >> 0x0000001cU)))) 
                                               & (0x0014U 
                                                  > 
                                                  (0x000007ffU 
                                                   & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__out_data_r[10U] 
                                                      >> 0x0000000eU))))))
                                         ? 0x02c0U : 0x0230U))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__echo_w 
        = ((1U & (~ (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__aem_w) 
                      & (4U == (0x0000ffffU & ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__out_data_r[4U] 
                                                << 4U) 
                                               | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__out_data_r[3U] 
                                                  >> 0x0000001cU))))) 
                     & (0x0014U <= (0x000007ffU & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__out_data_r[10U] 
                                                   >> 0x0000000eU)))))) 
           && ((1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__ctrs_w))) 
               && (1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_w)))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__v_alloc_gnt_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__alloc_req_r) 
           & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__0__KET____DOT__u_rx_slots__DOT__wr_active_r)) 
              & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__0__KET____DOT__u_rx_slots__DOT__ff_valid_w)));
    __Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__312__t 
        = vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__et_r;
    __Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__312__Vfuncout 
        = (3U | ((IData)(__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__312__t) 
                 << 4U));
    vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__tram_raddr_w 
        = __Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__312__Vfuncout;
    if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__est_r))) {
        if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__est_r))) {
            if (vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__ext_trd_go_w) {
                vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT____VlemCall_0__taddr 
                    = milan_datapath__DOT__csr_tctx_rd_addr_w;
            } else {
                vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__313__w 
                    = ((0U == (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__grant_t_w))
                        ? 3U : 0U);
                vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__313__t 
                    = vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__grant_t_w;
                vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT____VlemCall_0__taddr 
                    = (((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__313__t) 
                        << 4U) | (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__313__w));
            }
            vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__tram_raddr_w 
                = vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT____VlemCall_0__taddr;
        } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__est_r))) {
            vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__314__t 
                = vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__et_r;
            vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__314__Vfuncout 
                = (5U | ((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__314__t) 
                         << 4U));
            vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__tram_raddr_w 
                = vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__314__Vfuncout;
        } else {
            vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__315__t 
                = vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__et_r;
            vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__315__Vfuncout 
                = (5U | ((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__315__t) 
                         << 4U));
            vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__tram_raddr_w 
                = vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__315__Vfuncout;
        }
    } else if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__est_r))) {
        if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__est_r))) {
            if (vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__ext_trd_go_w) {
                vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT____VlemCall_0__taddr 
                    = milan_datapath__DOT__csr_tctx_rd_addr_w;
            } else {
                vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__316__w 
                    = ((0U == (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__grant_t_w))
                        ? 3U : 0U);
                vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__316__t 
                    = vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__grant_t_w;
                vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT____VlemCall_0__taddr 
                    = (((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__316__t) 
                        << 4U) | (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__316__w));
            }
            vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__tram_raddr_w 
                = vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT____VlemCall_0__taddr;
        } else {
            vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__317__w 
                = ((0U == (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fph_r))
                    ? 4U : 3U);
            vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__317__t 
                = vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__et_r;
            vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__317__Vfuncout 
                = (((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__317__t) 
                    << 4U) | (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__317__w));
            vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__tram_raddr_w 
                = vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__317__Vfuncout;
        }
    } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__est_r))) {
        vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__318__w 
            = ((0U == (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fph_r))
                ? 1U : ((1U == (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fph_r))
                         ? 2U : 3U));
        vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__318__t 
            = vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__et_r;
        vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__318__Vfuncout 
            = (((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__318__t) 
                << 4U) | (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__318__w));
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__tram_raddr_w 
            = vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__318__Vfuncout;
    } else {
        if (vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__ext_trd_go_w) {
            vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT____VlemCall_0__taddr 
                = milan_datapath__DOT__csr_tctx_rd_addr_w;
        } else {
            vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__319__w 
                = ((0U == (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__grant_t_w))
                    ? 3U : 0U);
            vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__319__t 
                = vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__grant_t_w;
            vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT____VlemCall_0__taddr 
                = (((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__319__t) 
                    << 4U) | (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__319__w));
        }
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__tram_raddr_w 
            = vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT____VlemCall_0__taddr;
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__ix26_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__tix_w) 
           | ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__scfg_r) 
              | (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_113)));
    vlSelfRef.milan_datapath__DOT__pp_gsi_kind_w = 
        (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gavb_r)
           ? 1U : 2U) & (- (IData)((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gstri_r) 
                                             | (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_290)))))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gsi_any_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gstri_r) 
           | ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gavb_r) 
              | ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gasp_r) 
                 | (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_290))));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_153 = (Vmilan_datapath__ConstPool__TABLE_h5f1389fb_0
                                                  [vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_release_merge__DOT__available_w] 
                                                  & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__slot_r) 
                                                     == Vmilan_datapath__ConstPool__TABLE_h6dff1152_0
                                                     [vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_release_merge__DOT__available_w]));
    vlSelfRef.milan_datapath__DOT__sfv_base_ok_w = 
        ((~ (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__setval_r 
                     >> 0x00000034U))) & ((0xffefffff003fffffULL 
                                           & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__setval_r) 
                                          == (0xffefffff003fffffULL 
                                              & vlSelfRef.milan_datapath__DOT__sfv_decl_w)));
    vlSelfRef.milan_datapath__DOT__gsi_setl_w = ((0ULL 
                                                  != vlSelfRef.milan_datapath__DOT__gsi_sid_w) 
                                                 & (IData)(vlSelfRef.milan_datapath__DOT__gsi_bnd_w));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__start1_w 
        = ((0U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__st_r)) 
           & ((~ ((0U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__cnt_mvrp_r)) 
                  | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__start0_w))) 
              & ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_377) 
                 >> 1U)));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__fw_last_w 
        = vlSelfRef.s_axis_mac_rx_tlast;
    if ((0U != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__fw_S))) {
        if ((1U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__fw_S))) {
            if ((1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__accept_w)))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__fw_last_w = 1U;
            }
        }
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__fw_user_w = 0U;
    if ((0U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__fw_S))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__fw_user_w 
            = vlSelfRef.s_axis_mac_rx_tlast;
    } else if ((1U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__fw_S))) {
        if ((1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__accept_w)))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__fw_user_w = 1U;
        }
    }
    vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__hit 
        = (((((((vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_valid[15U] 
                 & (0ULL == (vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_mask[15U] 
                             & (vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_key[15U] 
                                ^ vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__da_num_w)))) 
                << 3U) | ((vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_valid[14U] 
                           & (0ULL == (vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_mask[14U] 
                                       & (vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_key[14U] 
                                          ^ vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__da_num_w)))) 
                          << 2U)) | (((vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_valid[13U] 
                                       & (0ULL == (vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_mask[13U] 
                                                   & (vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_key[13U] 
                                                      ^ vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__da_num_w)))) 
                                      << 1U) | (vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_valid[12U] 
                                                & (0ULL 
                                                   == 
                                                   (vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_mask[12U] 
                                                    & (vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_key[12U] 
                                                       ^ vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__da_num_w)))))) 
             << 0x0000000cU) | (((((vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_valid[11U] 
                                    & (0ULL == (vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_mask[11U] 
                                                & (vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_key[11U] 
                                                   ^ vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__da_num_w)))) 
                                   << 3U) | ((vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_valid[10U] 
                                              & (0ULL 
                                                 == 
                                                 (vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_mask[10U] 
                                                  & (vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_key[10U] 
                                                     ^ vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__da_num_w)))) 
                                             << 2U)) 
                                 | (((vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_valid[9U] 
                                      & (0ULL == (vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_mask[9U] 
                                                  & (vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_key[9U] 
                                                     ^ vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__da_num_w)))) 
                                     << 1U) | (vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_valid[8U] 
                                               & (0ULL 
                                                  == 
                                                  (vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_mask[8U] 
                                                   & (vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_key[8U] 
                                                      ^ vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__da_num_w)))))) 
                                << 8U)) | ((((((vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_valid[7U] 
                                                & (0ULL 
                                                   == 
                                                   (vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_mask[7U] 
                                                    & (vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_key[7U] 
                                                       ^ vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__da_num_w)))) 
                                               << 3U) 
                                              | ((vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_valid[6U] 
                                                  & (0ULL 
                                                     == 
                                                     (vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_mask[6U] 
                                                      & (vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_key[6U] 
                                                         ^ vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__da_num_w)))) 
                                                 << 2U)) 
                                             | (((vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_valid[5U] 
                                                  & (0ULL 
                                                     == 
                                                     (vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_mask[5U] 
                                                      & (vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_key[5U] 
                                                         ^ vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__da_num_w)))) 
                                                 << 1U) 
                                                | (vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_valid[4U] 
                                                   & (0ULL 
                                                      == 
                                                      (vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_mask[4U] 
                                                       & (vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_key[4U] 
                                                          ^ vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__da_num_w)))))) 
                                            << 4U) 
                                           | ((((vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_valid[3U] 
                                                 & (0ULL 
                                                    == 
                                                    (vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_mask[3U] 
                                                     & (vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_key[3U] 
                                                        ^ vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__da_num_w)))) 
                                                << 3U) 
                                               | ((vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_valid[2U] 
                                                   & (0ULL 
                                                      == 
                                                      (vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_mask[2U] 
                                                       & (vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_key[2U] 
                                                          ^ vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__da_num_w)))) 
                                                  << 2U)) 
                                              | (((vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_valid[1U] 
                                                   & (0ULL 
                                                      == 
                                                      (vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_mask[1U] 
                                                       & (vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_key[1U] 
                                                          ^ vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__da_num_w)))) 
                                                  << 1U) 
                                                 | (vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_valid[0U] 
                                                    & (0ULL 
                                                       == 
                                                       (vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_mask[0U] 
                                                        & (vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_key[0U] 
                                                           ^ vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__da_num_w))))))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__accept_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__wr_ready_r) 
           & ((IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__urb_we_w) 
              | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_rb_we_w)));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__rb_hold_w 
        = ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__wr_ready_r)) 
           & (IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__urb_we_w));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__urb_wstrb_w = 0x0fU;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__urb_addr_w 
        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__cursor_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__urb_wdata_w 
        = (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__a_fmt_w);
    if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__vld_e_r) {
        if ((1U & (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__uop_e_r 
                           >> 0x0000002fU)))) {
            if ((1U & (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__uop_e_r 
                               >> 0x0000002eU)))) {
                if ((1U & (~ (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__uop_e_r 
                                      >> 0x0000002dU))))) {
                    if ((1U & (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__uop_e_r 
                                       >> 0x0000002cU)))) {
                        if ((1U & (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__uop_e_r 
                                           >> 0x0000002bU)))) {
                            if ((1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__is_q_field_w)))) {
                                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__urb_wstrb_w 
                                    = (0x0000000fU 
                                       & (0xffffff31U 
                                          >> (0x0000001cU 
                                              & ((IData)(
                                                         (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__uop_e_r 
                                                          >> 0x0000001cU)) 
                                                 << 2U))));
                            }
                            if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__is_q_field_w) {
                                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__urb_addr_w 
                                    = (0x000003ffU 
                                       & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__cursor_r) 
                                          + ((1U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__eseq_r))
                                              ? 4U : 0U)));
                                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__urb_wdata_w 
                                    = ((0U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__eseq_r))
                                        ? (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__opa_e_r 
                                                   >> 0x20U))
                                        : (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__opa_e_r));
                            }
                        } else {
                            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__urb_addr_w 
                                = (0x0000000cU & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__eseq_r) 
                                                  << 2U));
                            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__urb_wdata_w 
                                = ((0U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__eseq_r))
                                    ? (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__opa_e_r 
                                               >> 0x00000020U))
                                    : ((1U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__eseq_r))
                                        ? (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__opa_e_r)
                                        : (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__opb_e_r) 
                                            << 0x00000010U) 
                                           | ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__status_r) 
                                              << 8U))));
                        }
                    }
                }
            } else if ((1U & (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__uop_e_r 
                                      >> 0x0000002dU)))) {
                if ((1U & (~ (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__uop_e_r 
                                      >> 0x0000002cU))))) {
                    if ((1U & (~ (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__uop_e_r 
                                          >> 0x0000002bU))))) {
                        if ((1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__is_q_field_w)))) {
                            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__urb_wstrb_w 
                                = (0x0000000fU & (0xffffff31U 
                                                  >> 
                                                  (0x0000001cU 
                                                   & ((IData)(
                                                              (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__uop_e_r 
                                                               >> 0x0000001cU)) 
                                                      << 2U))));
                        }
                        if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__is_q_field_w) {
                            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__urb_addr_w 
                                = (0x000003ffU & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__cursor_r) 
                                                  + 
                                                  ((1U 
                                                    == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__eseq_r))
                                                    ? 4U
                                                    : 0U)));
                            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__urb_wdata_w 
                                = ((0U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__eseq_r))
                                    ? (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__opa_e_r 
                                               >> 0x20U))
                                    : (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__opa_e_r));
                        }
                    }
                }
            } else if ((1U & (~ (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__uop_e_r 
                                         >> 0x0000002cU))))) {
                if ((1U & (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__uop_e_r 
                                   >> 0x0000002bU)))) {
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__urb_wdata_w 
                        = (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gxr_data_r);
                }
            }
        } else if ((1U & (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__uop_e_r 
                                  >> 0x0000002eU)))) {
            if ((1U & (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__uop_e_r 
                               >> 0x0000002dU)))) {
                if ((1U & (~ (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__uop_e_r 
                                      >> 0x0000002cU))))) {
                    if ((1U & (~ (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__uop_e_r 
                                          >> 0x0000002bU))))) {
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__urb_wdata_w 
                            = ((1U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__eseq_r))
                                ? (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__copy_lane_r 
                                           >> 0x20U))
                                : (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__copy_lane_r));
                    }
                }
            }
        }
    }
    if (vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__eng_we_w) {
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ram_wdata_w 
            = milan_datapath__DOT__avtp_rx_monitor__DOT__eng_wdata_w;
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ram_waddr_w 
            = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__eng_waddr_w;
    } else {
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ram_wdata_w 
            = vlSelfRef.milan_datapath__DOT__lctx_wr_data_sane_w;
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ram_waddr_w 
            = vlSelfRef.milan_datapath__DOT__csr__DOT__lctx_wr_addr_r;
    }
    vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__stg_space_w 
        = (7U & (((IData)(4U) - (IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__stg_cnt_r)) 
                 + (1U & (- (IData)((IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__stg_drain_w))))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__da_mrp_a_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__da_msrp_a_w) 
           | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__da_mvrp_a_w));
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
    vlSelfRef.milan_datapath__DOT__pp_amap_edit_req_w 
        = (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_stage_ready_r) 
            | (4U > (IData)(vlSelfRef.milan_datapath__DOT__pp_amap_edit_phase_w))) 
           & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_213));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_288 = ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_stage_ready_r)) 
                                                  & (4U 
                                                     <= (IData)(vlSelfRef.milan_datapath__DOT__pp_amap_edit_phase_w)));
    vlSelfRef.milan_datapath__DOT__ctlh_tx_tvalid = 
        ((IData)(vlSelfRef.milan_datapath__DOT__ctl_tx_mux__DOT__flush_r) 
         | ((IData)(vlSelfRef.milan_datapath__DOT__ctl_tx_mux__DOT__src_tvalid_w) 
            & (IData)(vlSelfRef.milan_datapath__DOT__ctl_tx_mux__DOT__active)));
    vlSelfRef.milan_datapath__DOT__dpcrf_tvalid = ((IData)(vlSelfRef.milan_datapath__DOT__crf_dp_mux__DOT__flush_r) 
                                                   | ((IData)(vlSelfRef.milan_datapath__DOT__crf_dp_mux__DOT__src_tvalid_w) 
                                                      & (IData)(vlSelfRef.milan_datapath__DOT__crf_dp_mux__DOT__active)));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_447 = (0x000001ffU 
                                                  & ((IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__beat_r) 
                                                     + 
                                                     (0x000001fcU 
                                                      & ((((IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__slot_r) 
                                                           << 4U) 
                                                          + 
                                                          (0x0000000fU 
                                                           & ((IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__rd_row_w) 
                                                              >> 1U))) 
                                                         << 2U))));
    vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__pop_dry_w 
        = ((0U == (IData)(milan_datapath__DOT__render_setpoint__DOT__fill_pop_w)) 
           & (IData)(__VdfgRegularize_h6e95ff9d_0_448));
    vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__pop_take_w 
        = ((0U != (IData)(milan_datapath__DOT__render_setpoint__DOT__fill_pop_w)) 
           & (IData)(__VdfgRegularize_h6e95ff9d_0_448));
    vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ext_rd_go_w 
        = ((0U == (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__mst_r)) 
           & ((0U == (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__pq_cnt_r)) 
              & ((0U == (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__bind_pend_r)) 
                 & ((0U == (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__sil_pend_r)) 
                    & ((0U == (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__iv_res_list_r)) 
                       & ((~ (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__depkt_any_w)) 
                          & ((((~ (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rds_dir_r)) 
                               & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rds_busy_r)) 
                              | (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_271)) 
                             & ((~ (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__penq_w)) 
                                & (0U == (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__iv_pend_r))))))))));
    vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__pdisp_new_w 
        = ((0U == (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__mst_r)) 
           & ((0U == (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__pq_cnt_r)) 
              & (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__penq_w)));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__val_w = 0ULL;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__vld_w = 0ULL;
    if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__in_range_w) {
        if ((0U == (0x00001fffU & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__st_addr_w 
                                   >> 3U)))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__val_w 
                = (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__cfg_r));
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__vld_w 
                = (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__cfg_v_r));
        } else if ((1U == (0x00001fffU & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__st_addr_w 
                                          >> 3U)))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__val_w 
                = (QData)((IData)(((0U >= (1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT____Vcellinp__u_dyn__desc_index_i)))
                                    ? vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__rate_r
                                   [(1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT____Vcellinp__u_dyn__desc_index_i))]
                                    : 0U)));
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__vld_w 
                = (QData)((IData)(((0U >= (1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT____Vcellinp__u_dyn__desc_index_i))) 
                                   && (1U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__rate_v_r) 
                                             >> (1U 
                                                 & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT____Vcellinp__u_dyn__desc_index_i)))))));
        } else if ((2U == (0x00001fffU & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__st_addr_w 
                                          >> 3U)))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__val_w 
                = (QData)((IData)(((0U >= (1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT____Vcellinp__u_dyn__desc_index_i)))
                                    ? vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__clksrc_r
                                   [(1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT____Vcellinp__u_dyn__desc_index_i))]
                                    : 0U)));
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__vld_w 
                = (QData)((IData)(((0U >= (1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT____Vcellinp__u_dyn__desc_index_i))) 
                                   && (1U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__clksrc_v_r) 
                                             >> (1U 
                                                 & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT____Vcellinp__u_dyn__desc_index_i)))))));
        } else if ((3U == (0x00001fffU & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__st_addr_w 
                                          >> 3U)))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__val_w 
                = ((8U >= (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT____Vcellinp__u_dyn__desc_index_i)))
                    ? vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__fmtin_r
                   [(0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT____Vcellinp__u_dyn__desc_index_i))]
                    : 0ULL);
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__vld_w 
                = (QData)((IData)(((8U >= (0x0000000fU 
                                           & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT____Vcellinp__u_dyn__desc_index_i))) 
                                   && (1U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__fmtin_v_r) 
                                             >> (0x0000000fU 
                                                 & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT____Vcellinp__u_dyn__desc_index_i)))))));
        } else if ((4U == (0x00001fffU & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__st_addr_w 
                                          >> 3U)))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__val_w 
                = ((8U >= (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT____Vcellinp__u_dyn__desc_index_i)))
                    ? vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__fmtout_r
                   [(0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT____Vcellinp__u_dyn__desc_index_i))]
                    : 0ULL);
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__vld_w 
                = (QData)((IData)(((8U >= (0x0000000fU 
                                           & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT____Vcellinp__u_dyn__desc_index_i))) 
                                   && (1U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__fmtout_v_r) 
                                             >> (0x0000000fU 
                                                 & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT____Vcellinp__u_dyn__desc_index_i)))))));
        } else if ((5U == (0x00001fffU & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__st_addr_w 
                                          >> 3U)))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__val_w 
                = (QData)((IData)(((8U >= (0x0000000fU 
                                           & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT____Vcellinp__u_dyn__desc_index_i)))
                                    ? vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__ptoff_r
                                   [(0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT____Vcellinp__u_dyn__desc_index_i))]
                                    : 0U)));
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__vld_w 
                = (QData)((IData)(((8U >= (0x0000000fU 
                                           & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT____Vcellinp__u_dyn__desc_index_i))) 
                                   && (1U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__ptoff_v_r) 
                                             >> (0x0000000fU 
                                                 & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT____Vcellinp__u_dyn__desc_index_i)))))));
        } else if ((7U == (0x00001fffU & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__st_addr_w 
                                          >> 3U)))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__val_w 
                = (QData)((IData)(((0U >= (1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT____Vcellinp__u_dyn__desc_index_i)))
                                    ? vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__ident_r
                                   [(1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT____Vcellinp__u_dyn__desc_index_i))]
                                    : 0U)));
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__vld_w 
                = (QData)((IData)(((0U >= (1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT____Vcellinp__u_dyn__desc_index_i))) 
                                   && (1U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__ident_v_r) 
                                             >> (1U 
                                                 & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT____Vcellinp__u_dyn__desc_index_i)))))));
        }
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__strm_set_valid_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__st_req_w) 
           & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__strq_sel_w));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__st_rdata_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__dyn_sel_w)
            ? vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__rd_data_r
            : vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__ans_data_r);
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__st_err_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__strq_sel_w)
            ? (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__strq_fail_r)
            : ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__dyn_sel_w)) 
               & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__ans_err_r)));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT____Vcellinp__u_store__st_req_i 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__st_req_w) 
           & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__dyn_sel_w)) 
              & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__strq_sel_w))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__st_rvalid_w 
        = ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__strq_sel_w)) 
           & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__dyn_sel_w)
               ? (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__rd_pend_r)
               : (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__store_rvalid_w)));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT____Vcellinp__u_dyn__st_req_i 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__st_req_w) 
           & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__dyn_sel_w));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__iter_evt_w 
        = ((4U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__rx_st_r)) 
           & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__ev_disc_w) 
              | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__ev_dep_w)));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__iter_port_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__iter_cancel_w) 
           | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__iter_arm_w));
    vlSelfRef.milan_datapath__DOT__gsi_tkreg_w = (3U 
                                                  & ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_tk_reg_state_w 
                                                      >> 
                                                      (0x0000001eU 
                                                       & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__desc_ix_r) 
                                                          << 1U))) 
                                                     & (- (IData)(
                                                                  (0x11U 
                                                                   >= 
                                                                   (0x0000001eU 
                                                                    & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__desc_ix_r) 
                                                                       << 1U)))))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_snk_fail_code_w[0U] 
        = ((((0x0000ff00U & ((((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__fcode_r[0U] 
                                << 8U) | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__fcode_r[0U] 
                                          >> 0x00000018U)) 
                              & (- (IData)((2U == (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_268))))) 
                             << 8U)) | (0x000000ffU 
                                        & (((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__fcode_r[0U] 
                                             << 0x00000010U) 
                                            | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__fcode_r[0U] 
                                               >> 0x00000010U)) 
                                           & (- (IData)(
                                                        (2U 
                                                         == (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_269))))))) 
            << 0x00000010U) | ((0x0000ff00U & ((((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__fcode_r[0U] 
                                                  << 0x00000018U) 
                                                 | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__fcode_r[0U] 
                                                    >> 8U)) 
                                                & (- (IData)(
                                                             (2U 
                                                              == (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_270))))) 
                                               << 8U)) 
                               | (IData)(vlSelfRef.milan_datapath__DOT__lwsrp_ta_fail_code)));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_snk_fail_code_w[1U] 
        = ((((0x0000ff00U & ((((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__fcode_r[1U] 
                                << 8U) | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__fcode_r[1U] 
                                          >> 0x00000018U)) 
                              & (- (IData)((2U == (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_264))))) 
                             << 8U)) | (0x000000ffU 
                                        & (((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__fcode_r[1U] 
                                             << 0x00000010U) 
                                            | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__fcode_r[1U] 
                                               >> 0x00000010U)) 
                                           & (- (IData)(
                                                        (2U 
                                                         == (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_265))))))) 
            << 0x00000010U) | ((0x0000ff00U & ((((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__fcode_r[1U] 
                                                  << 0x00000018U) 
                                                 | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__fcode_r[1U] 
                                                    >> 8U)) 
                                                & (- (IData)(
                                                             (2U 
                                                              == (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_266))))) 
                                               << 8U)) 
                               | (0x000000ffU & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__fcode_r[1U] 
                                                 & (- (IData)(
                                                              (2U 
                                                               == (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_267))))))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_snk_fail_code_w[2U] 
        = (0x000000ffU & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__fcode_r[2U] 
                          & (- (IData)((2U == (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_263))))));
    vlSelfRef.milan_datapath__DOT____Vcellinp__csr__i_acmpl_state 
        = ((0x80000000U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__bound_hold_r) 
                           << 0x00000017U)) | ((0x0fff0000U 
                                                & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__bound_vlan_r[0U] 
                                                   << 0x00000010U)) 
                                               | ((((0U 
                                                     != (IData)(vlSelfRef.milan_datapath__DOT__lwsrp_ta_fail_code)) 
                                                    << 7U) 
                                                   | (((1U 
                                                        == (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_121)) 
                                                       << 6U) 
                                                      | (0x00000010U 
                                                         & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__bound_hold_r) 
                                                            << 4U)))) 
                                                  | (8U 
                                                     & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__bound_hold_r) 
                                                        << 3U)))));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_176 = ((1U 
                                                   == (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_122)) 
                                                  & ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_59) 
                                                     >> 1U));
    vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__pop_w 
        = (((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_tvalid_pipe_reg) 
            >> 1U) & (IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_tready_pipe));
    vlSelfRef.milan_datapath__DOT__rend_pcm_tvalid_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__emit_w) 
           & ((IData)(vlSelfRef.milan_datapath__DOT__pcm_route__DOT__render_active_o) 
              & ((IData)(vlSelfRef.milan_datapath__DOT__route_render_sel_w) 
                 == vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__idxq_r
                 [vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__idxq_rp_r])));
    vlSelfRef.milan_datapath__DOT__dpkt_pcm_tlast_w 
        = ((8U >= (IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__remain_r)) 
           & (IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__emit_w));
    vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__s_ok_w 
        = ((8U > vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__idxq_r
            [vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__idxq_rp_r]) 
           & (IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__emit_w));
    vlSelfRef.milan_datapath__DOT__lb_tap_tvalid_w 
        = vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__emit_w;
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_175 = ((1U 
                                                   == (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_123)) 
                                                  & ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_60) 
                                                     >> 1U));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_174 = ((1U 
                                                   == (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_124)) 
                                                  & ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_61) 
                                                     >> 1U));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_173 = ((1U 
                                                   == (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_125)) 
                                                  & ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_62) 
                                                     >> 1U));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_172 = ((1U 
                                                   == (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_126)) 
                                                  & ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_63) 
                                                     >> 1U));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_171 = ((1U 
                                                   == (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_127)) 
                                                  & ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_64) 
                                                     >> 1U));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_170 = ((1U 
                                                   == (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_128)) 
                                                  & ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_65) 
                                                     >> 1U));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__ev_rsp_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__hit_ok_w) 
           & (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__cp_r) 
               >> 1U) & ((2U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__hdr_protocol_r)) 
                         & ((1U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__hdr_msg_type_r)) 
                            & ((3U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__hdr_opcode_r)) 
                               & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__hdr_ctlr_eid_r 
                                  == vlSelfRef.milan_datapath__DOT__cfg_adp_entity_id))))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__da_1722_a_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__da_own_a_w) 
           | ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__da_mcast_a_w) 
              | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__da_maap_a_w)));
    milan_datapath__DOT__aaf_packetizer__DOT__frame_bytes__DOT__unnamedblk5__DOT__k = 0U;
    while ((0x000000f0U > milan_datapath__DOT__aaf_packetizer__DOT__frame_bytes__DOT__unnamedblk5__DOT__k)) {
        if (VL_LIKELY(((0xefU >= (0x000000ffU & milan_datapath__DOT__aaf_packetizer__DOT__frame_bytes__DOT__unnamedblk5__DOT__k))))) {
            vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[(0x000000ffU 
                                                                    & milan_datapath__DOT__aaf_packetizer__DOT__frame_bytes__DOT__unnamedblk5__DOT__k)] = 0U;
        }
        milan_datapath__DOT__aaf_packetizer__DOT__frame_bytes__DOT__unnamedblk5__DOT__k 
            = ((IData)(1U) + milan_datapath__DOT__aaf_packetizer__DOT__frame_bytes__DOT__unnamedblk5__DOT__k);
    }
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
        = (((IData)(vlSelfRef.milan_datapath__DOT__crft_pcp_w) 
            << 5U) | (0x0000000fU & ((IData)(milan_datapath__DOT__aaf_packetizer__DOT__eff_vid_w) 
                                     >> 8U)));
    vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[15U] 
        = (0x000000ffU & (IData)(milan_datapath__DOT__aaf_packetizer__DOT__eff_vid_w));
    vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[16U] = 0x22U;
    vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[17U] = 0xf0U;
    vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[18U] = 2U;
    vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[19U] 
        = (0x00000081U | ((IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__emr_r) 
                          << 3U));
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
        = (0x000000f8U & (((IData)(6U) * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_246)) 
                          << 3U));
    vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[40U] = 0U;
    vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[41U] = 0U;
    if ((0U < (0x0000001fU & ((IData)(6U) * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_246))))) {
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
    if ((1U < (0x0000001fU & ((IData)(6U) * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_246))))) {
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
    if ((2U < (0x0000001fU & ((IData)(6U) * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_246))))) {
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
    if ((3U < (0x0000001fU & ((IData)(6U) * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_246))))) {
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
    if ((4U < (0x0000001fU & ((IData)(6U) * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_246))))) {
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
    if ((5U < (0x0000001fU & ((IData)(6U) * (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_246))))) {
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
}
