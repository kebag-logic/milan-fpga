// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vmilan_datapath.h for the primary calling header

#include "Vmilan_datapath__pch.h"

extern const VlWide<9>/*287:0*/ Vmilan_datapath__ConstPool__CONST_hc5471b50_0;
extern const VlWide<256>/*8191:0*/ Vmilan_datapath__ConstPool__CONST_hc13a5b68_0;
extern const VlWide<16>/*511:0*/ Vmilan_datapath__ConstPool__CONST_h88ed57bb_0;
extern const VlUnpacked<SData/*15:0*/, 8> Vmilan_datapath__ConstPool__TABLE_hed845b49_0;
extern const VlWide<8>/*255:0*/ Vmilan_datapath__ConstPool__CONST_h5302cfd2_0;
extern const VlUnpacked<CData/*2:0*/, 16> Vmilan_datapath__ConstPool__TABLE_h1b26f04f_0;
extern const VlUnpacked<CData/*0:0*/, 32> Vmilan_datapath__ConstPool__TABLE_h5f1389fb_0;
extern const VlUnpacked<CData/*2:0*/, 32> Vmilan_datapath__ConstPool__TABLE_h6dff1152_0;

VL_ATTR_COLD void Vmilan_datapath___024root___stl_sequent__TOP__1(Vmilan_datapath___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vmilan_datapath___024root___stl_sequent__TOP__1\n"); );
    Vmilan_datapath__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    IData/*31:0*/ milan_datapath__DOT__amap_page_slot__DOT__off_c;
    milan_datapath__DOT__amap_page_slot__DOT__off_c = 0;
    IData/*31:0*/ milan_datapath__DOT__amap_page_slot__DOT__g_c;
    milan_datapath__DOT__amap_page_slot__DOT__g_c = 0;
    IData/*31:0*/ milan_datapath__DOT__amap_page_fmt__DOT__offq_c;
    milan_datapath__DOT__amap_page_fmt__DOT__offq_c = 0;
    IData/*31:0*/ milan_datapath__DOT__pp_ctr_event_pick__DOT__pick;
    milan_datapath__DOT__pp_ctr_event_pick__DOT__pick = 0;
    CData/*5:0*/ milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__nbytes_w;
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__nbytes_w = 0;
    CData/*0:0*/ milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__urb_we_w;
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__urb_we_w = 0;
    CData/*0:0*/ milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_gate_w;
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_gate_w = 0;
    CData/*0:0*/ milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_daok2_w;
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_daok2_w = 0;
    CData/*0:0*/ milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__iter_arm_w;
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__iter_arm_w = 0;
    CData/*3:0*/ milan_datapath__DOT__render_setpoint__DOT__chans_in_raw_w;
    milan_datapath__DOT__render_setpoint__DOT__chans_in_raw_w = 0;
    CData/*5:0*/ milan_datapath__DOT__render_setpoint__DOT__fill_pop_w;
    milan_datapath__DOT__render_setpoint__DOT__fill_pop_w = 0;
    CData/*5:0*/ milan_datapath__DOT__avtp_rx_monitor__DOT__eng_waddr_w;
    milan_datapath__DOT__avtp_rx_monitor__DOT__eng_waddr_w = 0;
    IData/*31:0*/ milan_datapath__DOT__avtp_rx_monitor__DOT__eng_wdata_w;
    milan_datapath__DOT__avtp_rx_monitor__DOT__eng_wdata_w = 0;
    QData/*63:0*/ milan_datapath__DOT__aaf_packetizer__DOT__stream_id_w;
    milan_datapath__DOT__aaf_packetizer__DOT__stream_id_w = 0;
    IData/*31:0*/ milan_datapath__DOT__aaf_packetizer__DOT__frame_bytes__DOT__unnamedblk5__DOT__k;
    milan_datapath__DOT__aaf_packetizer__DOT__frame_bytes__DOT__unnamedblk5__DOT__k = 0;
    CData/*7:0*/ __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__68__Vfuncout;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__68__Vfuncout = 0;
    CData/*5:0*/ __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__68__idx;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__68__idx = 0;
    CData/*3:0*/ __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__68__msg;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__68__msg = 0;
    SData/*15:0*/ __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__68__off;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__68__off = 0;
    CData/*7:0*/ __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__68__cnt;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__68__cnt = 0;
    QData/*47:0*/ __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__68__dda;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__68__dda = 0;
    QData/*47:0*/ __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__68__ereq_s;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__68__ereq_s = 0;
    SData/*15:0*/ __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__68__ereq_c;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__68__ereq_c = 0;
    QData/*47:0*/ __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__68__econ_s;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__68__econ_s = 0;
    SData/*15:0*/ __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__68__econ_c;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__68__econ_c = 0;
    IData/*31:0*/ __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__68__i;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__68__i = 0;
    CData/*7:0*/ __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__68__b;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__68__b = 0;
    CData/*0:0*/ __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__68__dfd;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__68__dfd = 0;
    QData/*47:0*/ __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__68__req_s;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__68__req_s = 0;
    SData/*15:0*/ __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__68__req_c;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__68__req_c = 0;
    CData/*7:0*/ __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__110__Vfuncout;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__110__Vfuncout = 0;
    CData/*6:0*/ __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__110__idx;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__110__idx = 0;
    CData/*0:0*/ __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__110__dep;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__110__dep = 0;
    CData/*0:0*/ __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__110__ifx;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__110__ifx = 0;
    QData/*63:0*/ __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__110__gm;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__110__gm = 0;
    CData/*7:0*/ __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__110__dom;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__110__dom = 0;
    IData/*31:0*/ __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__110__aidx;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__110__aidx = 0;
    IData/*31:0*/ __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__110__i;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__110__i = 0;
    CData/*7:0*/ __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__110__b;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__110__b = 0;
    QData/*63:0*/ __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__182__Vfuncout;
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__182__Vfuncout = 0;
    CData/*2:0*/ __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__182__b;
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__182__b = 0;
    VlUnpacked<CData/*7:0*/, 64> __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__182__f;
    for (int __Vi0 = 0; __Vi0 < 64; ++__Vi0) {
        __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__182__f[__Vi0] = 0;
    }
    CData/*4:0*/ __Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__305__Vfuncout;
    __Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__305__Vfuncout = 0;
    CData/*0:0*/ __Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__305__t;
    __Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__305__t = 0;
    IData/*31:0*/ __Vtemp_3;
    IData/*31:0*/ __Vilp1;
    // Body
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_115 = (0x00000001ffffffffULL 
                                                  & ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__a_fmt_w)) 
                                                     - (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__b_or_imm_w))));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_180 = ((IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__beat_r) 
                                                  == 
                                                  (0x0000001fU 
                                                   & ((IData)(5U) 
                                                      + 
                                                      ((IData)(6U) 
                                                       * 
                                                       (7U 
                                                        & ((IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__echn_w) 
                                                           >> 1U))))));
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
    if ((6U <= milan_datapath__DOT__pp_ctr_event_pick__DOT__pick)) {
        milan_datapath__DOT__pp_ctr_event_pick__DOT__pick 
            = (milan_datapath__DOT__pp_ctr_event_pick__DOT__pick 
               - (IData)(6U));
    }
    if (((5U >= (7U & milan_datapath__DOT__pp_ctr_event_pick__DOT__pick)) 
         && (1U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_all_pend_w) 
                   >> (7U & milan_datapath__DOT__pp_ctr_event_pick__DOT__pick))))) {
        vlSelfRef.milan_datapath__DOT__pp_ctr_evt_valid_w = 1U;
        if ((2U > milan_datapath__DOT__pp_ctr_event_pick__DOT__pick)) {
            vlSelfRef.milan_datapath__DOT__pp_ctr_evt_type_w = 5U;
            vlSelfRef.milan_datapath__DOT__pp_ctr_evt_index_w 
                = (0x0000ffffU & milan_datapath__DOT__pp_ctr_event_pick__DOT__pick);
        } else if ((4U > milan_datapath__DOT__pp_ctr_event_pick__DOT__pick)) {
            vlSelfRef.milan_datapath__DOT__pp_ctr_evt_type_w = 6U;
            vlSelfRef.milan_datapath__DOT__pp_ctr_evt_index_w 
                = (0x0000ffffU & (milan_datapath__DOT__pp_ctr_event_pick__DOT__pick 
                                  - (IData)(2U)));
        } else {
            vlSelfRef.milan_datapath__DOT__pp_ctr_evt_type_w 
                = ((4U == milan_datapath__DOT__pp_ctr_event_pick__DOT__pick)
                    ? 9U : 0x0024U);
        }
    }
    milan_datapath__DOT__pp_ctr_event_pick__DOT__pick 
        = ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_rr_r));
    if ((6U <= milan_datapath__DOT__pp_ctr_event_pick__DOT__pick)) {
        milan_datapath__DOT__pp_ctr_event_pick__DOT__pick 
            = (milan_datapath__DOT__pp_ctr_event_pick__DOT__pick 
               - (IData)(6U));
    }
    if (((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_evt_valid_w)) 
         & ((5U >= (7U & milan_datapath__DOT__pp_ctr_event_pick__DOT__pick)) 
            && (1U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_all_pend_w) 
                      >> (7U & milan_datapath__DOT__pp_ctr_event_pick__DOT__pick)))))) {
        vlSelfRef.milan_datapath__DOT__pp_ctr_evt_valid_w = 1U;
        if ((2U > milan_datapath__DOT__pp_ctr_event_pick__DOT__pick)) {
            vlSelfRef.milan_datapath__DOT__pp_ctr_evt_type_w = 5U;
            vlSelfRef.milan_datapath__DOT__pp_ctr_evt_index_w 
                = (0x0000ffffU & milan_datapath__DOT__pp_ctr_event_pick__DOT__pick);
        } else if ((4U > milan_datapath__DOT__pp_ctr_event_pick__DOT__pick)) {
            vlSelfRef.milan_datapath__DOT__pp_ctr_evt_type_w = 6U;
            vlSelfRef.milan_datapath__DOT__pp_ctr_evt_index_w 
                = (0x0000ffffU & (milan_datapath__DOT__pp_ctr_event_pick__DOT__pick 
                                  - (IData)(2U)));
        } else {
            vlSelfRef.milan_datapath__DOT__pp_ctr_evt_type_w 
                = ((4U == milan_datapath__DOT__pp_ctr_event_pick__DOT__pick)
                    ? 9U : 0x0024U);
        }
    }
    milan_datapath__DOT__pp_ctr_event_pick__DOT__pick 
        = ((IData)(2U) + (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_rr_r));
    if ((6U <= milan_datapath__DOT__pp_ctr_event_pick__DOT__pick)) {
        milan_datapath__DOT__pp_ctr_event_pick__DOT__pick 
            = (milan_datapath__DOT__pp_ctr_event_pick__DOT__pick 
               - (IData)(6U));
    }
    if (((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_evt_valid_w)) 
         & ((5U >= (7U & milan_datapath__DOT__pp_ctr_event_pick__DOT__pick)) 
            && (1U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_all_pend_w) 
                      >> (7U & milan_datapath__DOT__pp_ctr_event_pick__DOT__pick)))))) {
        vlSelfRef.milan_datapath__DOT__pp_ctr_evt_valid_w = 1U;
        if ((2U > milan_datapath__DOT__pp_ctr_event_pick__DOT__pick)) {
            vlSelfRef.milan_datapath__DOT__pp_ctr_evt_type_w = 5U;
            vlSelfRef.milan_datapath__DOT__pp_ctr_evt_index_w 
                = (0x0000ffffU & milan_datapath__DOT__pp_ctr_event_pick__DOT__pick);
        } else if ((4U > milan_datapath__DOT__pp_ctr_event_pick__DOT__pick)) {
            vlSelfRef.milan_datapath__DOT__pp_ctr_evt_type_w = 6U;
            vlSelfRef.milan_datapath__DOT__pp_ctr_evt_index_w 
                = (0x0000ffffU & (milan_datapath__DOT__pp_ctr_event_pick__DOT__pick 
                                  - (IData)(2U)));
        } else {
            vlSelfRef.milan_datapath__DOT__pp_ctr_evt_type_w 
                = ((4U == milan_datapath__DOT__pp_ctr_event_pick__DOT__pick)
                    ? 9U : 0x0024U);
        }
    }
    milan_datapath__DOT__pp_ctr_event_pick__DOT__pick 
        = ((IData)(3U) + (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_rr_r));
    if ((6U <= milan_datapath__DOT__pp_ctr_event_pick__DOT__pick)) {
        milan_datapath__DOT__pp_ctr_event_pick__DOT__pick 
            = (milan_datapath__DOT__pp_ctr_event_pick__DOT__pick 
               - (IData)(6U));
    }
    if (((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_evt_valid_w)) 
         & ((5U >= (7U & milan_datapath__DOT__pp_ctr_event_pick__DOT__pick)) 
            && (1U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_all_pend_w) 
                      >> (7U & milan_datapath__DOT__pp_ctr_event_pick__DOT__pick)))))) {
        vlSelfRef.milan_datapath__DOT__pp_ctr_evt_valid_w = 1U;
        if ((2U > milan_datapath__DOT__pp_ctr_event_pick__DOT__pick)) {
            vlSelfRef.milan_datapath__DOT__pp_ctr_evt_type_w = 5U;
            vlSelfRef.milan_datapath__DOT__pp_ctr_evt_index_w 
                = (0x0000ffffU & milan_datapath__DOT__pp_ctr_event_pick__DOT__pick);
        } else if ((4U > milan_datapath__DOT__pp_ctr_event_pick__DOT__pick)) {
            vlSelfRef.milan_datapath__DOT__pp_ctr_evt_type_w = 6U;
            vlSelfRef.milan_datapath__DOT__pp_ctr_evt_index_w 
                = (0x0000ffffU & (milan_datapath__DOT__pp_ctr_event_pick__DOT__pick 
                                  - (IData)(2U)));
        } else {
            vlSelfRef.milan_datapath__DOT__pp_ctr_evt_type_w 
                = ((4U == milan_datapath__DOT__pp_ctr_event_pick__DOT__pick)
                    ? 9U : 0x0024U);
        }
    }
    milan_datapath__DOT__pp_ctr_event_pick__DOT__pick 
        = ((IData)(4U) + (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_rr_r));
    if ((6U <= milan_datapath__DOT__pp_ctr_event_pick__DOT__pick)) {
        milan_datapath__DOT__pp_ctr_event_pick__DOT__pick 
            = (milan_datapath__DOT__pp_ctr_event_pick__DOT__pick 
               - (IData)(6U));
    }
    if (((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_evt_valid_w)) 
         & ((5U >= (7U & milan_datapath__DOT__pp_ctr_event_pick__DOT__pick)) 
            && (1U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_all_pend_w) 
                      >> (7U & milan_datapath__DOT__pp_ctr_event_pick__DOT__pick)))))) {
        vlSelfRef.milan_datapath__DOT__pp_ctr_evt_valid_w = 1U;
        if ((2U > milan_datapath__DOT__pp_ctr_event_pick__DOT__pick)) {
            vlSelfRef.milan_datapath__DOT__pp_ctr_evt_type_w = 5U;
            vlSelfRef.milan_datapath__DOT__pp_ctr_evt_index_w 
                = (0x0000ffffU & milan_datapath__DOT__pp_ctr_event_pick__DOT__pick);
        } else if ((4U > milan_datapath__DOT__pp_ctr_event_pick__DOT__pick)) {
            vlSelfRef.milan_datapath__DOT__pp_ctr_evt_type_w = 6U;
            vlSelfRef.milan_datapath__DOT__pp_ctr_evt_index_w 
                = (0x0000ffffU & (milan_datapath__DOT__pp_ctr_event_pick__DOT__pick 
                                  - (IData)(2U)));
        } else {
            vlSelfRef.milan_datapath__DOT__pp_ctr_evt_type_w 
                = ((4U == milan_datapath__DOT__pp_ctr_event_pick__DOT__pick)
                    ? 9U : 0x0024U);
        }
    }
    milan_datapath__DOT__pp_ctr_event_pick__DOT__pick 
        = ((IData)(5U) + (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_rr_r));
    if ((6U <= milan_datapath__DOT__pp_ctr_event_pick__DOT__pick)) {
        milan_datapath__DOT__pp_ctr_event_pick__DOT__pick 
            = (milan_datapath__DOT__pp_ctr_event_pick__DOT__pick 
               - (IData)(6U));
    }
    if (((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_evt_valid_w)) 
         & ((5U >= (7U & milan_datapath__DOT__pp_ctr_event_pick__DOT__pick)) 
            && (1U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_all_pend_w) 
                      >> (7U & milan_datapath__DOT__pp_ctr_event_pick__DOT__pick)))))) {
        vlSelfRef.milan_datapath__DOT__pp_ctr_evt_valid_w = 1U;
        if ((2U > milan_datapath__DOT__pp_ctr_event_pick__DOT__pick)) {
            vlSelfRef.milan_datapath__DOT__pp_ctr_evt_type_w = 5U;
            vlSelfRef.milan_datapath__DOT__pp_ctr_evt_index_w 
                = (0x0000ffffU & milan_datapath__DOT__pp_ctr_event_pick__DOT__pick);
        } else if ((4U > milan_datapath__DOT__pp_ctr_event_pick__DOT__pick)) {
            vlSelfRef.milan_datapath__DOT__pp_ctr_evt_type_w = 6U;
            vlSelfRef.milan_datapath__DOT__pp_ctr_evt_index_w 
                = (0x0000ffffU & (milan_datapath__DOT__pp_ctr_event_pick__DOT__pick 
                                  - (IData)(2U)));
        } else {
            vlSelfRef.milan_datapath__DOT__pp_ctr_evt_type_w 
                = ((4U == milan_datapath__DOT__pp_ctr_event_pick__DOT__pick)
                    ? 9U : 0x0024U);
        }
    }
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
    vlSelfRef.milan_datapath__DOT__gsi_decl_w = (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__declaring_r) 
                                                  >> 
                                                  (1U 
                                                   & (IData)(vlSelfRef.milan_datapath__DOT__gsiq_index_r))) 
                                                 & (IData)(vlSelfRef.milan_datapath__DOT__gsi_out_w));
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
              & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_42)));
    vlSelfRef.milan_datapath__DOT__pp_amap_req_w = 
        ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gx_req_w) 
         & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_r));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_105 = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gx_req_w) 
                                                  & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_edit_r));
    vlSelfRef.milan_datapath__DOT__sfv_need_out_w = 0U;
    if ((0x00001000U & vlSelfRef.milan_datapath__DOT__cmap_flat_w[0U])) {
        vlSelfRef.milan_datapath__DOT__sfv_need_out_w 
            = (1U | (0xf0U & (IData)(vlSelfRef.milan_datapath__DOT__sfv_need_out_w)));
    }
    if ((0x02000000U & vlSelfRef.milan_datapath__DOT__cmap_flat_w[0U])) {
        vlSelfRef.milan_datapath__DOT__sfv_need_out_w 
            = (2U | (0xf0U & (IData)(vlSelfRef.milan_datapath__DOT__sfv_need_out_w)));
    }
    if ((0x00000040U & vlSelfRef.milan_datapath__DOT__cmap_flat_w[1U])) {
        vlSelfRef.milan_datapath__DOT__sfv_need_out_w 
            = (3U | (0xf0U & (IData)(vlSelfRef.milan_datapath__DOT__sfv_need_out_w)));
    }
    if ((0x00080000U & vlSelfRef.milan_datapath__DOT__cmap_flat_w[1U])) {
        vlSelfRef.milan_datapath__DOT__sfv_need_out_w 
            = (4U | (0xf0U & (IData)(vlSelfRef.milan_datapath__DOT__sfv_need_out_w)));
    }
    if ((1U & vlSelfRef.milan_datapath__DOT__cmap_flat_w[2U])) {
        vlSelfRef.milan_datapath__DOT__sfv_need_out_w 
            = (5U | (0xf0U & (IData)(vlSelfRef.milan_datapath__DOT__sfv_need_out_w)));
    }
    if ((0x00002000U & vlSelfRef.milan_datapath__DOT__cmap_flat_w[2U])) {
        vlSelfRef.milan_datapath__DOT__sfv_need_out_w 
            = (6U | (0xf0U & (IData)(vlSelfRef.milan_datapath__DOT__sfv_need_out_w)));
    }
    if ((0x04000000U & vlSelfRef.milan_datapath__DOT__cmap_flat_w[2U])) {
        vlSelfRef.milan_datapath__DOT__sfv_need_out_w 
            = (7U | (0xf0U & (IData)(vlSelfRef.milan_datapath__DOT__sfv_need_out_w)));
    }
    if ((0x00000080U & vlSelfRef.milan_datapath__DOT__cmap_flat_w[3U])) {
        vlSelfRef.milan_datapath__DOT__sfv_need_out_w 
            = (8U | (0xf0U & (IData)(vlSelfRef.milan_datapath__DOT__sfv_need_out_w)));
    }
    vlSelfRef.milan_datapath__DOT__csr_tctx_rd_addr_w 
        = ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_172)
            ? ((0x00000070U & ((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__snap_idx_r) 
                               << 4U)) | (0x0000000fU 
                                          & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__snap_word_r)))
            : (((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rds_idx_r) 
                << 4U) | (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rds_word_r))));
    vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__ext_trd_go_w 
        = (((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_172) 
            | ((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rds_busy_r) 
               & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rds_dir_r))) 
           & ((3U == (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__est_r)) 
              | ((~ (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pend_r[0U])) 
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
                                         | ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_207) 
                                            | (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_26)))))))))))));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_208 = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gsfmt_r) 
                                                  | (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_207));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_release_merge__DOT__available_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_release_merge__DOT__request_w) 
           | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_release_merge__DOT__pending_r));
    vlSelfRef.milan_datapath__DOT__sfv_crf_row_w = 
        ((1U == (IData)(vlSelfRef.milan_datapath__DOT__gsiq_index_r)) 
         & ((IData)(vlSelfRef.milan_datapath__DOT__gsi_in_w) 
            | (IData)(vlSelfRef.milan_datapath__DOT__gsi_out_w)));
    if (vlSelfRef.milan_datapath__DOT__gsi_in_w) {
        vlSelfRef.milan_datapath__DOT__sfv_decl_w = 
            (0x0205022002006000ULL & (- (QData)((IData)(
                                                        (0U 
                                                         == (IData)(vlSelfRef.milan_datapath__DOT__gsiq_index_r))))));
        vlSelfRef.milan_datapath__DOT__gsi_bnd_w = 
            (1U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__bound_hold_r) 
                   >> (1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__desc_ix_r))));
    } else {
        vlSelfRef.milan_datapath__DOT__sfv_decl_w = 
            (0x0205022002006000ULL & ((- (QData)((IData)(vlSelfRef.milan_datapath__DOT__gsi_out_w))) 
                                      & (- (QData)((IData)(
                                                           (0U 
                                                            == (IData)(vlSelfRef.milan_datapath__DOT__gsiq_index_r)))))));
        vlSelfRef.milan_datapath__DOT__gsi_bnd_w = 0U;
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__start0_w 
        = ((0U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__st_r)) 
           & ((0U != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__cnt_msrp_r)) 
              & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_239)));
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
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_36 = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r) 
                                                 & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__gate_acc_w));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_65 = ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r)) 
                                                 & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__gate_acc_w));
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
        = ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_190)
            ? ((0x000000e0U & ((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__snap_idx_r) 
                               << 5U)) | (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__snap_word_r))
            : (((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rds_idx_r) 
                << 5U) | (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rds_word_r)));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_to_maap_w = 0U;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_maap_rel_w = 0U;
    vlSelfRef.milan_datapath__DOT__pp_restore_busy_w 
        = ((8U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__hs_r)) 
           | (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_260));
    milan_datapath__DOT__avtp_rx_monitor__DOT__eng_wdata_w = 0U;
    milan_datapath__DOT__avtp_rx_monitor__DOT__eng_waddr_w = 0U;
    if ((4U == (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__mst_r))) {
        if ((0U == (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__wrph_r))) {
            milan_datapath__DOT__avtp_rx_monitor__DOT__eng_wdata_w 
                = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__monst_r;
            vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__234__s 
                = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ev_s_r;
            vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__234__Vfuncout 
                = (8U | ((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__234__s) 
                         << 5U));
            milan_datapath__DOT__avtp_rx_monitor__DOT__eng_waddr_w 
                = vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__234__Vfuncout;
        } else if ((1U == (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__wrph_r))) {
            milan_datapath__DOT__avtp_rx_monitor__DOT__eng_wdata_w 
                = ((vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__cur_r[4U] 
                    << 0x0000001eU) | (vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__cur_r[3U] 
                                       >> 2U));
            vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__235__s 
                = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ev_s_r;
            vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__235__Vfuncout 
                = (9U | ((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__235__s) 
                         << 5U));
            milan_datapath__DOT__avtp_rx_monitor__DOT__eng_waddr_w 
                = vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__235__Vfuncout;
        } else {
            milan_datapath__DOT__avtp_rx_monitor__DOT__eng_wdata_w 
                = ((vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__cur_r[1U] 
                    << 0x0000001eU) | (vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__cur_r[0U] 
                                       >> 2U));
            vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__236__s 
                = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ev_s_r;
            vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__236__Vfuncout 
                = (0x0aU | ((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__236__s) 
                            << 5U));
            milan_datapath__DOT__avtp_rx_monitor__DOT__eng_waddr_w 
                = vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__236__Vfuncout;
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
                vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__237__s 
                    = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ev_s_r;
                vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__237__Vfuncout 
                    = (0x0bU | ((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__237__s) 
                                << 5U));
                milan_datapath__DOT__avtp_rx_monitor__DOT__eng_waddr_w 
                    = vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__237__Vfuncout;
            }
        } else if (vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__sil_mode_r) {
            if ((1U == (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__wrph_r))) {
                milan_datapath__DOT__avtp_rx_monitor__DOT__eng_wdata_w 
                    = ((IData)(1U) + vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ram_q_r);
                vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__238__s 
                    = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ev_s_r;
                vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__238__Vfuncout 
                    = (0x11U | ((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__238__s) 
                                << 5U));
                milan_datapath__DOT__avtp_rx_monitor__DOT__eng_waddr_w 
                    = vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__238__Vfuncout;
            } else if ((3U == (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__wrph_r))) {
                milan_datapath__DOT__avtp_rx_monitor__DOT__eng_wdata_w 
                    = (0xffffefffU & vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ram_q_r);
                vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__239__s 
                    = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ev_s_r;
                vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__239__Vfuncout 
                    = (8U | ((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__239__s) 
                             << 5U));
                milan_datapath__DOT__avtp_rx_monitor__DOT__eng_waddr_w 
                    = vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__239__Vfuncout;
            }
        } else if (vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__bind_zero_r) {
            milan_datapath__DOT__avtp_rx_monitor__DOT__eng_wdata_w = 0U;
            vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__240__w 
                = (0x10U | (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__zero_idx_r));
            vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__240__s 
                = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ev_s_r;
            vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__240__Vfuncout 
                = (((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__240__s) 
                    << 5U) | (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__240__w));
            milan_datapath__DOT__avtp_rx_monitor__DOT__eng_waddr_w 
                = vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__240__Vfuncout;
        } else if (((0U != (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__inc_list_r)) 
                    & (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__inc_rd_q_r))) {
            milan_datapath__DOT__avtp_rx_monitor__DOT__eng_wdata_w 
                = (vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ram_q_r 
                   + ((9U == (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__inc_next_w))
                       ? (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__frx_add_r)
                       : 1U));
            vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__241__w 
                = (0x10U | (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__inc_next_w));
            vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__241__s 
                = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ev_s_r;
            vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__241__Vfuncout 
                = (((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__241__s) 
                    << 5U) | (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__241__w));
            milan_datapath__DOT__avtp_rx_monitor__DOT__eng_waddr_w 
                = vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__241__Vfuncout;
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
                        vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__242__s 
                            = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ev_s_r;
                        vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__242__Vfuncout 
                            = (3U | ((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__242__s) 
                                     << 5U));
                        milan_datapath__DOT__avtp_rx_monitor__DOT__eng_waddr_w 
                            = vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__242__Vfuncout;
                    }
                }
            } else if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__wrph_r))) {
                if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__wrph_r))) {
                    milan_datapath__DOT__avtp_rx_monitor__DOT__eng_wdata_w 
                        = (IData)(vlSelfRef.milan_datapath__DOT__aecp_in0_fmt);
                    vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__243__s 
                        = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ev_s_r;
                    vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__243__Vfuncout 
                        = (2U | ((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__243__s) 
                                 << 5U));
                    milan_datapath__DOT__avtp_rx_monitor__DOT__eng_waddr_w 
                        = vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__243__Vfuncout;
                } else {
                    milan_datapath__DOT__avtp_rx_monitor__DOT__eng_wdata_w 
                        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__bound_sid_r[1U];
                    vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__244__s 
                        = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ev_s_r;
                    vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__244__Vfuncout 
                        = (1U | ((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__244__s) 
                                 << 5U));
                    milan_datapath__DOT__avtp_rx_monitor__DOT__eng_waddr_w 
                        = vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__244__Vfuncout;
                }
            } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__wrph_r))) {
                milan_datapath__DOT__avtp_rx_monitor__DOT__eng_wdata_w 
                    = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__bound_sid_r[0U];
                vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__245__s 
                    = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ev_s_r;
                vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__245__Vfuncout 
                    = ((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__245__s) 
                       << 5U);
                milan_datapath__DOT__avtp_rx_monitor__DOT__eng_waddr_w 
                    = vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__245__Vfuncout;
            } else {
                milan_datapath__DOT__avtp_rx_monitor__DOT__eng_wdata_w 
                    = (0xff3fc0ffU & vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ram_q_r);
                vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__246__s 
                    = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ev_s_r;
                vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__246__Vfuncout 
                    = (8U | ((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__246__s) 
                             << 5U));
                milan_datapath__DOT__avtp_rx_monitor__DOT__eng_waddr_w 
                    = vlSelfRef.__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__246__Vfuncout;
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
    vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__chans_q_in_w 
        = (vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__chans_q_r[0U] 
           & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_303));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_294 = ((IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__sched_r) 
                                                  & ((0U 
                                                      == (IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__beat_r)) 
                                                     & ((~ (IData)(vlSelfRef.milan_datapath__DOT__rsp_prefill_w)) 
                                                        & (0U 
                                                           == (IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__slot_r)))));
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
    vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__chans_pop_raw_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__mon_wire_chans_all_w) 
           & (- (IData)((0U == (IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__slot_r)))));
    milan_datapath__DOT__render_setpoint__DOT__chans_in_raw_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__mon_wire_chans_all_w) 
           & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_303));
    vlSelfRef.milan_datapath__DOT__crf_dp_mux__DOT__src_tvalid_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__crf_dp_mux__DOT__gsel)
            ? (IData)(vlSelfRef.milan_datapath__DOT__crf_tx__DOT__st_r)
            : (3U == (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__est_r)));
    vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__rd_row_w 
        = (0x0000001fU & ((0U == (IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__beat_r))
                           ? (IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__rptr_pop_w)
                           : (IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__ev_row_r)));
    milan_datapath__DOT__render_setpoint__DOT__fill_pop_w 
        = (0x0000003fU & ((vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__wptr_r[0U] 
                           & (- (IData)((0U == (IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__slot_r))))) 
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
           & ((0U >= (IData)(vlSelfRef.milan_datapath__DOT__avtprx_idx)) 
              & (((IData)(vlSelfRef.milan_datapath__DOT__strtbl_en_w) 
                  >> (IData)(vlSelfRef.milan_datapath__DOT__avtprx_idx)) 
                 & (2U != (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__pq_cnt_r)))));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_67 = ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_9) 
                                                 & (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__armed_r) 
                                                     >> 1U) 
                                                    & ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_39) 
                                                       & ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_93) 
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
                                                                 & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vid_r 
                                                                    >> 0x0000000cU))))))));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_68 = ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_9) 
                                                 & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__armed_r) 
                                                    & ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_39) 
                                                       & ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_92) 
                                                          & ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_da_w 
                                                              == 
                                                              (0x0000ffffffffffffULL 
                                                               & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__da_r[1U])) 
                                                                   << 0x00000020U) 
                                                                  | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__da_r[0U]))))) 
                                                             & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_vid_w) 
                                                                == 
                                                                (0x00000fffU 
                                                                 & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vid_r)))))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_rx_hit_w 
        = ((((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_9) 
             & (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rec_valid_r) 
                 >> 1U) & ((3U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_attr_type_w)) 
                           & ((5U >= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_mrp_event_w)) 
                              & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_93))))) 
            << 1U) | ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_9) 
                      & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rec_valid_r) 
                         & ((3U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_attr_type_w)) 
                            & ((5U >= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_mrp_event_w)) 
                               & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_92))))));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_228 = (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rec_valid_r) 
                                                   >> 1U) 
                                                  & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_9));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_229 = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rec_valid_r) 
                                                  & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_9));
    if (vlSelfRef.__VdfgRegularize_h6e95ff9d_0_114) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__line_raddr_w 
            = (0x0000007fU & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__patch_abs_byte_w) 
                              >> 3U));
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__name_raddr_w 
            = (0x000001ffU & ((0x0000ffffU & (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__desc_nbase_r) 
                                               + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__patch_name_r)) 
                                              << 3U)) 
                              + (7U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__patch_byte_r) 
                                       >> 3U))));
    } else {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__line_raddr_w 
            = (0x0000007fU & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__st_addr_w 
                              >> 3U));
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__name_raddr_w 
            = (0x000001ffU & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__st_addr_w 
                              >> 3U));
    }
    __Vtemp_3 = VL_MATCHMASKED_I(13, (0x00001fffU & 
                                      (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__st_addr_w 
                                       >> 3U)), Vmilan_datapath__ConstPool__CONST_h88ed57bb_0);
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__in_range_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT____Vcellinp__u_dyn__desc_index_i) 
           < Vmilan_datapath__ConstPool__TABLE_hed845b49_0
           [__Vtemp_3]);
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
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__iter_arm_w = 0U;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__iter_cancel_w = 0U;
    if ((4U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__rx_st_r))) {
        if ((0U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__rxq_msg_r))) {
            if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__disc_st_r) 
                          >> (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__sink_r))))) {
                if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__gm_dom_ok_w) {
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__st_set_w = 1U;
                }
            }
            if ((1U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__disc_st_r) 
                       >> (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__sink_r)))) {
                if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__rx_ifx_r) 
                     == (0x0000ffffU & (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__disc_rec_q_r 
                                                >> 0x00000020U))))) {
                    if ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__rx_aidx_r 
                         > (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__disc_rec_q_r))) {
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__rec_wr_en_w = 1U;
                        milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__iter_arm_w = 1U;
                    } else if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__gm_dom_ok_w) {
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__rec_wr_en_w = 1U;
                        milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__iter_arm_w = 1U;
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
                milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__iter_arm_w = 1U;
            }
        } else if ((1U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__rxq_msg_r))) {
            if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__disc_st_r) 
                  >> (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__sink_r)) 
                 & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__rx_ifx_r) 
                    == (0x0000ffffU & (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__disc_rec_q_r 
                                               >> 0x00000020U)))))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__st_clr_w = 1U;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__iter_cancel_w = 1U;
            }
        }
    }
    vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__wptr_in_w 
        = (vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__wptr_r[0U] 
           & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_302));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__evr_payload_w[0U] 
        = (0x00010000U | (((2U == (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_187)) 
                           << 0x0000001fU) | ((2U == (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_50)) 
                                              << 0x0000000fU)));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__evr_payload_w[1U] 
        = (IData)((0x0000000000010000ULL | ((QData)((IData)(
                                                            (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__adp_evt_sink_w) 
                                                              << 0x00000010U) 
                                                             | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__adp_evt_sink_w)))) 
                                            << 0x00000020U)));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__evr_payload_w[2U] 
        = (IData)(((0x0000000000010000ULL | ((QData)((IData)(
                                                             (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__adp_evt_sink_w) 
                                                               << 0x00000010U) 
                                                              | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__adp_evt_sink_w)))) 
                                             << 0x00000020U)) 
                   >> 0x00000020U));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__evr_payload_w[3U] 
        = (IData)((0x0000000100000000ULL | (QData)((IData)(
                                                           (0x00000fffU 
                                                            & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_domain__DOT__decl_vid_r))))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__evr_payload_w[4U] 
        = (IData)(((0x0000000100000000ULL | (QData)((IData)(
                                                            (0x00000fffU 
                                                             & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_domain__DOT__decl_vid_r))))) 
                   >> 0x00000020U));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__evr_payload_w[5U] 
        = (0x0000ffffU & (IData)(vlSelfRef.milan_datapath__DOT__eff_link_w));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_tk_reg_state_w 
        = (((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_187) 
            << 2U) | (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_50));
    vlSelfRef.milan_datapath__DOT__lwsrp_ta_fail_code 
        = (0x000000ffU & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__fcode_r) 
                          & (- (IData)((2U == (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_50))))));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_31 = (((2U 
                                                   & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__fail_r))
                                                   ? 2U
                                                   : 1U) 
                                                 & (- (IData)((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_41))));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_51 = (((1U 
                                                   & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__fail_r))
                                                   ? 2U
                                                   : 1U) 
                                                 & (- (IData)((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_40))));
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
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__mac_byte_f__128__i 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__idx_r;
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__mac_byte_f__128__k 
            = ((5U < (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__mac_byte_f__128__i))
                ? 0U : ((IData)(5U) - (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__mac_byte_f__128__i)));
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT____VlemCall_1__mac_byte_f 
            = ((0x2fU >= (0x0000003fU & (vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__mac_byte_f__128__k 
                                         << 3U))) ? 
               (0x000000ffU & (IData)((0x000091e0f0010000ULL 
                                       >> (0x0000003fU 
                                           & (vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__mac_byte_f__128__k 
                                              << 3U)))))
                : 0U);
        if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__pp_rx_data_w) 
             != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT____VlemCall_1__mac_byte_f))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__da_mcast_a_w = 0U;
        }
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__mac_byte_f__129__i 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__idx_r;
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__mac_byte_f__129__k 
            = ((5U < (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__mac_byte_f__129__i))
                ? 0U : ((IData)(5U) - (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__mac_byte_f__129__i)));
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT____VlemCall_2__mac_byte_f 
            = ((0x2fU >= (0x0000003fU & (vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__mac_byte_f__129__k 
                                         << 3U))) ? 
               (0x000000ffU & (IData)((0x000091e0f000ff00ULL 
                                       >> (0x0000003fU 
                                           & (vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__mac_byte_f__129__k 
                                              << 3U)))))
                : 0U);
        if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__pp_rx_data_w) 
             != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT____VlemCall_2__mac_byte_f))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__da_maap_a_w = 0U;
        }
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__mac_byte_f__130__i 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__idx_r;
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__mac_byte_f__130__k 
            = ((5U < (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__mac_byte_f__130__i))
                ? 0U : ((IData)(5U) - (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__mac_byte_f__130__i)));
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT____VlemCall_3__mac_byte_f 
            = ((0x2fU >= (0x0000003fU & (vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__mac_byte_f__130__k 
                                         << 3U))) ? 
               (0x000000ffU & (IData)((0x00000180c200000eULL 
                                       >> (0x0000003fU 
                                           & (vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__mac_byte_f__130__k 
                                              << 3U)))))
                : 0U);
        if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__pp_rx_data_w) 
             != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT____VlemCall_3__mac_byte_f))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__da_msrp_a_w = 0U;
        }
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__mac_byte_f__131__i 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__idx_r;
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__mac_byte_f__131__k 
            = ((5U < (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__mac_byte_f__131__i))
                ? 0U : ((IData)(5U) - (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__mac_byte_f__131__i)));
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT____VlemCall_4__mac_byte_f 
            = ((0x2fU >= (0x0000003fU & (vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__mac_byte_f__131__k 
                                         << 3U))) ? 
               (0x000000ffU & (IData)((0x00000180c2000021ULL 
                                       >> (0x0000003fU 
                                           & (vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__mac_byte_f__131__k 
                                              << 3U)))))
                : 0U);
        if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__pp_rx_data_w) 
             != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT____VlemCall_4__mac_byte_f))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__da_mvrp_a_w = 0U;
        }
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__mac_byte_f__127__i 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__idx_r;
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__mac_byte_f__127__m 
            = vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w;
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__mac_byte_f__127__k 
            = ((5U < (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__mac_byte_f__127__i))
                ? 0U : ((IData)(5U) - (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__mac_byte_f__127__i)));
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT____VlemCall_0__mac_byte_f 
            = ((0x2fU >= (0x0000003fU & (vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__mac_byte_f__127__k 
                                         << 3U))) ? 
               (0x000000ffU & (IData)((vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__mac_byte_f__127__m 
                                       >> (0x0000003fU 
                                           & (vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__mac_byte_f__127__k 
                                              << 3U)))))
                : 0U);
        if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__pp_rx_data_w) 
             != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT____VlemCall_0__mac_byte_f))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__da_own_a_w = 0U;
        }
    }
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__182__b 
        = vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat_r;
    for (int __Vi0 = 0; __Vi0 < 64; ++__Vi0) {
        __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__182__f[__Vi0] = 0;
    }
    __Vilp1 = 0U;
    while ((__Vilp1 <= 0x0000003fU)) {
        __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__182__f[__Vilp1] = 0U;
        __Vilp1 = ((IData)(1U) + __Vilp1);
    }
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__182__f[0U] = 0x91U;
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__182__f[1U] = 0xe0U;
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__182__f[2U] = 0xf0U;
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__182__f[3U] = 0U;
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__182__f[4U] = 0xffU;
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__182__f[5U] = 0U;
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__182__f[6U] 
        = (0x000000ffU & (IData)((vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w 
                                  >> 0x00000028U)));
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__182__f[7U] 
        = (0x000000ffU & (IData)((vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w 
                                  >> 0x00000020U)));
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__182__f[8U] 
        = (0x000000ffU & (IData)((vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w 
                                  >> 0x00000018U)));
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__182__f[9U] 
        = (0x000000ffU & (IData)((vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w 
                                  >> 0x00000010U)));
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__182__f[10U] 
        = (0x000000ffU & (IData)((vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w 
                                  >> 8U)));
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__182__f[11U] 
        = (0x000000ffU & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w));
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__182__f[12U] = 0x22U;
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__182__f[13U] = 0xf0U;
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__182__f[14U] = 0xfeU;
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__182__f[15U] 
        = vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_msg_r;
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__182__f[16U] = 8U;
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__182__f[17U] = 0x1cU;
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__182__f[26U] = 0x91U;
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__182__f[27U] = 0xe0U;
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__182__f[28U] = 0xf0U;
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__182__f[29U] = 0U;
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__182__f[30U] 
        = (0x000000ffU & ((IData)(vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__offset_r) 
                          >> 8U));
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__182__f[31U] 
        = (0x000000ffU & (IData)(vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__offset_r));
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__182__f[32U] = 0U;
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__182__f[33U] 
        = (0x000000ffU & (vlSelfRef.milan_datapath__DOT__csr__DOT__maap_ctrl 
                          >> 8U));
    if ((2U == (IData)(vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_msg_r))) {
        __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__182__f[34U] = 0x91U;
        __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__182__f[35U] = 0xe0U;
        __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__182__f[36U] = 0xf0U;
        __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__182__f[37U] = 0U;
        __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__182__f[38U] 
            = (0x000000ffU & ((IData)(vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_conf_start_r) 
                              >> 8U));
        __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__182__f[39U] 
            = (0x000000ffU & (IData)(vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_conf_start_r));
        __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__182__f[40U] 
            = (0x000000ffU & ((IData)(vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_conf_cnt_r) 
                              >> 8U));
        __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__182__f[41U] 
            = (0x000000ffU & (IData)(vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_conf_cnt_r));
    }
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__182__Vfuncout 
        = (((QData)((IData)((((((IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__182__f
                                        [(7U | ((IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__182__b) 
                                                << 3U))]) 
                                << 8U) | __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__182__f
                               [(6U | ((IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__182__b) 
                                       << 3U))]) << 0x00000010U) 
                             | (((IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__182__f
                                         [(5U | ((IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__182__b) 
                                                 << 3U))]) 
                                 << 8U) | __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__182__f
                                [(4U | ((IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__182__b) 
                                        << 3U))])))) 
            << 0x00000020U) | (QData)((IData)((((((IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__182__f
                                                          [
                                                          (3U 
                                                           | ((IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__182__b) 
                                                              << 3U))]) 
                                                  << 8U) 
                                                 | __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__182__f
                                                 [(2U 
                                                   | ((IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__182__b) 
                                                      << 3U))]) 
                                                << 0x00000010U) 
                                               | (((IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__182__f
                                                           [
                                                           (1U 
                                                            | ((IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__182__b) 
                                                               << 3U))]) 
                                                   << 8U) 
                                                  | __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__182__f
                                                  [
                                                  ((IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__182__b) 
                                                   << 3U)])))));
    vlSelfRef.milan_datapath__DOT__maap_tx_tdata = __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat__182__Vfuncout;
    milan_datapath__DOT__aaf_packetizer__DOT__stream_id_w 
        = ((vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w 
            << 0x00000010U) | (QData)((IData)((((0U 
                                                 != (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__euid_r))
                                                 ? (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__euid_r)
                                                 : (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__et_r)) 
                                               & (- (IData)((IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__et_r)))))));
    vlSelfRef.milan_datapath__DOT__eff_crft_sid_w = 
        ((0U != vlSelfRef.milan_datapath__DOT__cfg_crft_sid)
          ? vlSelfRef.milan_datapath__DOT__cfg_crft_sid
          : (1ULL | (vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w 
                     << 0x00000010U)));
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__68__econ_c 
        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__def_conf_cnt_r;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__68__econ_s 
        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__def_conf_start_r;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__68__ereq_c 
        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__def_req_cnt_r;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__68__ereq_s 
        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__def_req_start_r;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__68__dda 
        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__def_da_r;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__68__cnt 
        = (0x000000ffU & (vlSelfRef.milan_datapath__DOT__csr__DOT__maap_ctrl 
                          >> 8U));
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__68__off 
        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__offset_r;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__68__msg 
        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__send_msg_r;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__68__idx 
        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__bld_idx_r;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__68__i 
        = __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__68__idx;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__68__dfd 
        = (2U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__68__msg));
    if (__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__68__dfd) {
        __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__68__req_s 
            = __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__68__ereq_s;
        __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__68__req_c 
            = __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__68__ereq_c;
    } else {
        __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__68__req_s 
            = (0x000091e0f0000000ULL | (QData)((IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__68__off)));
        __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__68__req_c 
            = __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__68__cnt;
    }
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__68__b = 0U;
    if ((6U > __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__68__i)) {
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__byte48_f__69__n 
            = __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__68__i;
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__byte48_f__69__v 
            = ((IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__68__dfd)
                ? __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__68__dda
                : 0x000091e0f000ff00ULL);
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__byte48_f__69__sh 
            = VL_SHIFTR_QQI(48,48,32, vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__byte48_f__69__v, 
                            (((IData)(5U) - vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__byte48_f__69__n) 
                             << 3U));
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__byte48_f__69__Vfuncout 
            = (0x000000ffU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__byte48_f__69__sh));
        __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__68__b 
            = vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__byte48_f__69__Vfuncout;
    } else if ((0x0000000cU > __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__68__i)) {
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__byte48_f__70__n 
            = (__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__68__i 
               - (IData)(6U));
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__byte48_f__70__v 
            = vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w;
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__byte48_f__70__sh 
            = VL_SHIFTR_QQI(48,48,32, vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__byte48_f__70__v, 
                            (((IData)(5U) - vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__byte48_f__70__n) 
                             << 3U));
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__byte48_f__70__Vfuncout 
            = (0x000000ffU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__byte48_f__70__sh));
        __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__68__b 
            = vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__byte48_f__70__Vfuncout;
    } else if ((0x0000000eU > __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__68__i)) {
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__byte16_f__71__n 
            = (__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__68__i 
               - (IData)(0x0000000cU));
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__byte16_f__71__sh 
            = VL_SHIFTR_III(16,16,32, 0x22f0U, (((IData)(1U) 
                                                 - vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__byte16_f__71__n) 
                                                << 3U));
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__byte16_f__71__Vfuncout 
            = (0x000000ffU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__byte16_f__71__sh));
        __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__68__b 
            = vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__byte16_f__71__Vfuncout;
    } else if ((0x0000000eU == __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__68__i)) {
        __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__68__b = 0xfeU;
    } else if ((0x0000000fU == __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__68__i)) {
        __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__68__b 
            = __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__68__msg;
    } else if ((0x00000010U == __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__68__i)) {
        __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__68__b = 8U;
    } else if ((0x00000011U == __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__68__i)) {
        __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__68__b = 0x10U;
    } else if (((0x0000001aU <= __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__68__i) 
                & (0x00000020U > __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__68__i))) {
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__byte48_f__72__n 
            = (__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__68__i 
               - (IData)(0x0000001aU));
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__byte48_f__72__v 
            = __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__68__req_s;
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__byte48_f__72__sh 
            = VL_SHIFTR_QQI(48,48,32, vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__byte48_f__72__v, 
                            (((IData)(5U) - vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__byte48_f__72__n) 
                             << 3U));
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__byte48_f__72__Vfuncout 
            = (0x000000ffU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__byte48_f__72__sh));
        __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__68__b 
            = vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__byte48_f__72__Vfuncout;
    } else if (((0x00000020U <= __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__68__i) 
                & (0x00000022U > __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__68__i))) {
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__byte16_f__73__n 
            = (__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__68__i 
               - (IData)(0x00000020U));
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__byte16_f__73__v 
            = __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__68__req_c;
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__byte16_f__73__sh 
            = VL_SHIFTR_III(16,16,32, (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__byte16_f__73__v), 
                            (((IData)(1U) - vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__byte16_f__73__n) 
                             << 3U));
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__byte16_f__73__Vfuncout 
            = (0x000000ffU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__byte16_f__73__sh));
        __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__68__b 
            = vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__byte16_f__73__Vfuncout;
    } else if ((((IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__68__dfd) 
                 & (0x00000022U <= __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__68__i)) 
                & (0x00000028U > __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__68__i))) {
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__byte48_f__74__n 
            = (__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__68__i 
               - (IData)(0x00000022U));
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__byte48_f__74__v 
            = __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__68__econ_s;
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__byte48_f__74__sh 
            = VL_SHIFTR_QQI(48,48,32, vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__byte48_f__74__v, 
                            (((IData)(5U) - vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__byte48_f__74__n) 
                             << 3U));
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__byte48_f__74__Vfuncout 
            = (0x000000ffU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__byte48_f__74__sh));
        __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__68__b 
            = vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__byte48_f__74__Vfuncout;
    } else if ((((IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__68__dfd) 
                 & (0x00000028U <= __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__68__i)) 
                & (0x0000002aU > __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__68__i))) {
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__byte16_f__75__n 
            = (__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__68__i 
               - (IData)(0x00000028U));
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__byte16_f__75__v 
            = __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__68__econ_c;
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__byte16_f__75__sh 
            = VL_SHIFTR_III(16,16,32, (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__byte16_f__75__v), 
                            (((IData)(1U) - vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__byte16_f__75__n) 
                             << 3U));
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__byte16_f__75__Vfuncout 
            = (0x000000ffU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__byte16_f__75__sh));
        __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__68__b 
            = vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__byte16_f__75__Vfuncout;
    }
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__68__Vfuncout 
        = __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__68__b;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__maapeng_txs_wr_data_w 
        = __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__frame_byte_f__68__Vfuncout;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__wr_valid_w = 0U;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__wr_data_w = 0U;
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__nbytes_w = 1U;
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
    if ((8U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__st_r))) {
        if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__st_r))) {
            if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__st_r))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__wr_valid_w = 0U;
            } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__st_r))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__wr_valid_w = 1U;
                milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__nbytes_w = 2U;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__wr_data_w = 0U;
            } else {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__wr_valid_w = 1U;
                milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__nbytes_w = 2U;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__wr_data_w 
                    = (0x000000ffU & ((0U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__bidx_r))
                                       ? (7U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__ll_val_w) 
                                                >> 8U))
                                       : (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__ll_val_w)));
            }
        } else if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__st_r))) {
            if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__st_r))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__wr_valid_w = 1U;
                milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__nbytes_w = 2U;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__wr_data_w = 0U;
            } else {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__wr_valid_w = 1U;
                milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__nbytes_w 
                    = (0x0000000fU & (((IData)(3U) 
                                       + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_len_r)) 
                                      >> 2U));
                vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_fp_at_f__12__j 
                    = (0x0000003fU & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__bidx_r) 
                                      << 2U));
                {
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT____VlemCall_4__run_fp_at_f = 0;
                    if (((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_fp_at_f__12__j) 
                         >= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_len_r))) {
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT____VlemCall_4__run_fp_at_f = 0U;
                        goto __Vlabel0;
                    }
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT____VlemCall_4__run_fp_at_f 
                        = ((0x17U >= (0x0000001eU & 
                                      ((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_fp_at_f__12__j) 
                                       << 1U))) ? (3U 
                                                   & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_fp_r 
                                                      >> 
                                                      (0x0000001eU 
                                                       & ((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_fp_at_f__12__j) 
                                                          << 1U))))
                            : 0U);
                    __Vlabel0: ;
                }
                vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_fp_at_f__13__j 
                    = (0x0000003fU & ((IData)(1U) + 
                                      ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__bidx_r) 
                                       << 2U)));
                {
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT____VlemCall_5__run_fp_at_f = 0;
                    if (((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_fp_at_f__13__j) 
                         >= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_len_r))) {
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT____VlemCall_5__run_fp_at_f = 0U;
                        goto __Vlabel1;
                    }
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT____VlemCall_5__run_fp_at_f 
                        = ((0x17U >= (0x0000001eU & 
                                      ((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_fp_at_f__13__j) 
                                       << 1U))) ? (3U 
                                                   & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_fp_r 
                                                      >> 
                                                      (0x0000001eU 
                                                       & ((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_fp_at_f__13__j) 
                                                          << 1U))))
                            : 0U);
                    __Vlabel1: ;
                }
                vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_fp_at_f__14__j 
                    = (0x0000003fU & ((IData)(2U) + 
                                      ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__bidx_r) 
                                       << 2U)));
                {
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT____VlemCall_6__run_fp_at_f = 0;
                    if (((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_fp_at_f__14__j) 
                         >= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_len_r))) {
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT____VlemCall_6__run_fp_at_f = 0U;
                        goto __Vlabel2;
                    }
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT____VlemCall_6__run_fp_at_f 
                        = ((0x17U >= (0x0000001eU & 
                                      ((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_fp_at_f__14__j) 
                                       << 1U))) ? (3U 
                                                   & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_fp_r 
                                                      >> 
                                                      (0x0000001eU 
                                                       & ((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_fp_at_f__14__j) 
                                                          << 1U))))
                            : 0U);
                    __Vlabel2: ;
                }
                vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_fp_at_f__15__j 
                    = (0x0000003fU & ((IData)(3U) + 
                                      ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__bidx_r) 
                                       << 2U)));
                {
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT____VlemCall_7__run_fp_at_f = 0;
                    if (((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_fp_at_f__15__j) 
                         >= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_len_r))) {
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT____VlemCall_7__run_fp_at_f = 0U;
                        goto __Vlabel3;
                    }
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT____VlemCall_7__run_fp_at_f 
                        = ((0x17U >= (0x0000001eU & 
                                      ((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_fp_at_f__15__j) 
                                       << 1U))) ? (3U 
                                                   & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_fp_r 
                                                      >> 
                                                      (0x0000001eU 
                                                       & ((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_fp_at_f__15__j) 
                                                          << 1U))))
                            : 0U);
                    __Vlabel3: ;
                }
                vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__pack4_f__16__d 
                    = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT____VlemCall_7__run_fp_at_f;
                vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__pack4_f__16__c 
                    = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT____VlemCall_6__run_fp_at_f;
                vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__pack4_f__16__b 
                    = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT____VlemCall_5__run_fp_at_f;
                vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__pack4_f__16__a 
                    = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT____VlemCall_4__run_fp_at_f;
                vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__pack4_f__16__Vfuncout 
                    = (0x000000ffU & (((((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__pack4_f__16__a) 
                                         << 6U) + ((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__pack4_f__16__b) 
                                                   << 4U)) 
                                       + ((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__pack4_f__16__c) 
                                          << 2U)) + (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__pack4_f__16__d)));
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__wr_data_w 
                    = vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__pack4_f__16__Vfuncout;
            }
        } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__st_r))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__wr_valid_w = 1U;
            milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__nbytes_w 
                = (0x0000003fU & VL_DIV_III(6, (0x0000003fU 
                                                & ((IData)(2U) 
                                                   + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_len_r))), (IData)(3U)));
            vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_ev_at_f__17__j 
                = (0x0000003fU & ((IData)(3U) * (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__bidx_r)));
            {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT____VlemCall_1__run_ev_at_f = 0;
                if (((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_ev_at_f__17__j) 
                     >= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_len_r))) {
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT____VlemCall_1__run_ev_at_f = 0U;
                    goto __Vlabel4;
                }
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT____VlemCall_1__run_ev_at_f 
                    = ((0x23U >= (0x0000003fU & ((IData)(3U) 
                                                 * 
                                                 (0x0000000fU 
                                                  & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_ev_at_f__17__j)))))
                        ? (7U & (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_ev_r 
                                         >> (0x0000003fU 
                                             & ((IData)(3U) 
                                                * (0x0000000fU 
                                                   & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_ev_at_f__17__j)))))))
                        : 0U);
                __Vlabel4: ;
            }
            vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_ev_at_f__18__j 
                = (0x0000003fU & ((IData)(1U) + ((IData)(3U) 
                                                 * (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__bidx_r))));
            {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT____VlemCall_2__run_ev_at_f = 0;
                if (((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_ev_at_f__18__j) 
                     >= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_len_r))) {
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT____VlemCall_2__run_ev_at_f = 0U;
                    goto __Vlabel5;
                }
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT____VlemCall_2__run_ev_at_f 
                    = ((0x23U >= (0x0000003fU & ((IData)(3U) 
                                                 * 
                                                 (0x0000000fU 
                                                  & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_ev_at_f__18__j)))))
                        ? (7U & (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_ev_r 
                                         >> (0x0000003fU 
                                             & ((IData)(3U) 
                                                * (0x0000000fU 
                                                   & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_ev_at_f__18__j)))))))
                        : 0U);
                __Vlabel5: ;
            }
            vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_ev_at_f__19__j 
                = (0x0000003fU & ((IData)(2U) + ((IData)(3U) 
                                                 * (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__bidx_r))));
            {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT____VlemCall_3__run_ev_at_f = 0;
                if (((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_ev_at_f__19__j) 
                     >= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_len_r))) {
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT____VlemCall_3__run_ev_at_f = 0U;
                    goto __Vlabel6;
                }
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT____VlemCall_3__run_ev_at_f 
                    = ((0x23U >= (0x0000003fU & ((IData)(3U) 
                                                 * 
                                                 (0x0000000fU 
                                                  & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_ev_at_f__19__j)))))
                        ? (7U & (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_ev_r 
                                         >> (0x0000003fU 
                                             & ((IData)(3U) 
                                                * (0x0000000fU 
                                                   & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_ev_at_f__19__j)))))))
                        : 0U);
                __Vlabel6: ;
            }
            vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__pack3_f__20__c 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT____VlemCall_3__run_ev_at_f;
            vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__pack3_f__20__b 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT____VlemCall_2__run_ev_at_f;
            vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__pack3_f__20__a 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT____VlemCall_1__run_ev_at_f;
            vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__pack3_f__20__Vfuncout 
                = (0x000000ffU & ((((IData)(0x24U) 
                                    * (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__pack3_f__20__a)) 
                                   + ((IData)(6U) * (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__pack3_f__20__b))) 
                                  + (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__pack3_f__20__c)));
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__wr_data_w 
                = vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__pack3_f__20__Vfuncout;
        } else {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__wr_valid_w = 1U;
            milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__nbytes_w 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__alen_w;
            vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__fv_byte_f__21__i 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__bidx_r;
            vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__fv_byte_f__21__v[0U] 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_first_r[0U];
            vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__fv_byte_f__21__v[1U] 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_first_r[1U];
            vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__fv_byte_f__21__v[2U] 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_first_r[2U];
            vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__fv_byte_f__21__v[3U] 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_first_r[3U];
            vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__fv_byte_f__21__v[4U] 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_first_r[4U];
            vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__fv_byte_f__21__v[5U] 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_first_r[5U];
            vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__fv_byte_f__21__v[6U] 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_first_r[6U];
            vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__fv_byte_f__21__v[7U] 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_first_r[7U];
            vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__fv_byte_f__21__v[8U] 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_first_r[8U];
            vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__fv_byte_f__21__Vfuncout 
                = ((0x010fU >= (0x000001ffU & (((IData)(0x010fU) 
                                                - ((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__fv_byte_f__21__i) 
                                                   << 3U)) 
                                               - (IData)(7U))))
                    ? (0x000000ffU & (((0U == (0x0000001fU 
                                               & (((IData)(0x010fU) 
                                                   - 
                                                   ((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__fv_byte_f__21__i) 
                                                    << 3U)) 
                                                  - (IData)(7U))))
                                        ? 0U : (vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__fv_byte_f__21__v
                                                [(((IData)(7U) 
                                                   + 
                                                   (0x000001ffU 
                                                    & (((IData)(0x010fU) 
                                                        - 
                                                        ((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__fv_byte_f__21__i) 
                                                         << 3U)) 
                                                       - (IData)(7U)))) 
                                                  >> 5U)] 
                                                << 
                                                ((IData)(0x00000020U) 
                                                 - 
                                                 (0x0000001fU 
                                                  & (((IData)(0x010fU) 
                                                      - 
                                                      ((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__fv_byte_f__21__i) 
                                                       << 3U)) 
                                                     - (IData)(7U)))))) 
                                      | (vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__fv_byte_f__21__v
                                         [(0x0000000fU 
                                           & ((((IData)(0x010fU) 
                                                - ((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__fv_byte_f__21__i) 
                                                   << 3U)) 
                                               - (IData)(7U)) 
                                              >> 5U))] 
                                         >> (0x0000001fU 
                                             & (((IData)(0x010fU) 
                                                 - 
                                                 ((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__fv_byte_f__21__i) 
                                                  << 3U)) 
                                                - (IData)(7U))))))
                    : 0U);
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__wr_data_w 
                = vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__fv_byte_f__21__Vfuncout;
        }
    } else if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__st_r))) {
        if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__st_r))) {
            if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__st_r))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__wr_valid_w = 1U;
                milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__nbytes_w = 2U;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__wr_data_w 
                    = ((0U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__bidx_r))
                        ? (0x00000020U & ((- (IData)(
                                                     ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__first_vec_r) 
                                                      & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__la_pend_r) 
                                                         >> (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__cur_app_r))))) 
                                          << 5U)) : (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_len_r));
            } else {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__wr_valid_w = 1U;
                milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__nbytes_w 
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
            milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__nbytes_w = 0x0fU;
            if ((6U > (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__bidx_r))) {
                vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__mac_byte_f__22__i 
                    = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__bidx_r;
                vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__mac_byte_f__22__v 
                    = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__cur_app_r)
                        ? 0x00000180c2000021ULL : 0x00000180c200000eULL);
                vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__mac_byte_f__22__Vfuncout 
                    = ((0x2fU >= (0x0000003fU & (((IData)(0x2fU) 
                                                  - 
                                                  ((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__mac_byte_f__22__i) 
                                                   << 3U)) 
                                                 - (IData)(7U))))
                        ? (0x000000ffU & (IData)((vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__mac_byte_f__22__v 
                                                  >> 
                                                  (0x0000003fU 
                                                   & (((IData)(0x2fU) 
                                                       - 
                                                       ((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__mac_byte_f__22__i) 
                                                        << 3U)) 
                                                      - (IData)(7U))))))
                        : 0U);
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__wr_data_w 
                    = vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__mac_byte_f__22__Vfuncout;
            } else if ((0x0cU > (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__bidx_r))) {
                vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__mac_byte_f__23__i 
                    = (0x0000003fU & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__bidx_r) 
                                      - (IData)(6U)));
                vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__mac_byte_f__23__v 
                    = vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w;
                vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__mac_byte_f__23__Vfuncout 
                    = ((0x2fU >= (0x0000003fU & (((IData)(0x2fU) 
                                                  - 
                                                  ((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__mac_byte_f__23__i) 
                                                   << 3U)) 
                                                 - (IData)(7U))))
                        ? (0x000000ffU & (IData)((vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__mac_byte_f__23__v 
                                                  >> 
                                                  (0x0000003fU 
                                                   & (((IData)(0x2fU) 
                                                       - 
                                                       ((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__mac_byte_f__23__i) 
                                                        << 3U)) 
                                                      - (IData)(7U))))))
                        : 0U);
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__wr_data_w 
                    = vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__mac_byte_f__23__Vfuncout;
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
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_out_w 
        = (((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_33) 
            << 2U) | (IData)(vlSelfRef.milan_datapath__DOT__lwsrp_listener_decl));
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
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__110__aidx 
        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__bld_aidx_r;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__110__dom 
        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__bld_dom_r;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__110__gm 
        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__bld_gm_r;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__110__ifx 
        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__bld_if_r;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__110__dep 
        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__bld_dep_r;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__110__idx 
        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__bld_idx_r;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__110__i 
        = __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__110__idx;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__110__b = 0U;
    if ((6U > __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__110__i)) {
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte48_f__111__n 
            = __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__110__i;
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte48_f__111__sh 
            = VL_SHIFTR_QQI(48,48,32, 0x000091e0f0010000ULL, 
                            (((IData)(5U) - vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte48_f__111__n) 
                             << 3U));
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte48_f__111__Vfuncout 
            = (0x000000ffU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte48_f__111__sh));
        __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__110__b 
            = vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte48_f__111__Vfuncout;
    } else if ((0x0000000cU > __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__110__i)) {
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte48_f__112__n 
            = (__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__110__i 
               - (IData)(6U));
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte48_f__112__v 
            = vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w;
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte48_f__112__sh 
            = VL_SHIFTR_QQI(48,48,32, vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte48_f__112__v, 
                            (((IData)(5U) - vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte48_f__112__n) 
                             << 3U));
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte48_f__112__Vfuncout 
            = (0x000000ffU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte48_f__112__sh));
        __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__110__b 
            = vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte48_f__112__Vfuncout;
    } else if ((0x0000000eU > __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__110__i)) {
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte16_f__113__n 
            = (__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__110__i 
               - (IData)(0x0000000cU));
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte16_f__113__sh 
            = VL_SHIFTR_III(16,16,32, 0x22f0U, (((IData)(1U) 
                                                 - vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte16_f__113__n) 
                                                << 3U));
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte16_f__113__Vfuncout 
            = (0x000000ffU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte16_f__113__sh));
        __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__110__b 
            = vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte16_f__113__Vfuncout;
    } else if ((0x0000000eU == __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__110__i)) {
        __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__110__b = 0xfaU;
    } else if ((0x0000000fU == __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__110__i)) {
        __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__110__b 
            = ((IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__110__dep)
                ? 1U : 0U);
    } else if ((0x00000010U == __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__110__i)) {
        __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__110__b 
            = (((IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__110__dep)
                 ? 0U : 0x0aU) << 3U);
    } else if ((0x00000011U == __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__110__i)) {
        __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__110__b = 0x38U;
    } else if ((0x0000001aU > __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__110__i)) {
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte64_f__114__n 
            = (__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__110__i 
               - (IData)(0x00000012U));
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte64_f__114__v 
            = vlSelfRef.milan_datapath__DOT__cfg_adp_entity_id;
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte64_f__114__sh 
            = VL_SHIFTR_QQI(64,64,32, vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte64_f__114__v, 
                            (((IData)(7U) - vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte64_f__114__n) 
                             << 3U));
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte64_f__114__Vfuncout 
            = (0x000000ffU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte64_f__114__sh));
        __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__110__b 
            = vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte64_f__114__Vfuncout;
    } else if ((0x00000022U > __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__110__i)) {
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte64_f__115__n 
            = (__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__110__i 
               - (IData)(0x0000001aU));
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte64_f__115__v 
            = (((QData)((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__adp_midhi)) 
                << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__adp_midlo)));
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte64_f__115__sh 
            = VL_SHIFTR_QQI(64,64,32, vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte64_f__115__v, 
                            (((IData)(7U) - vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte64_f__115__n) 
                             << 3U));
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte64_f__115__Vfuncout 
            = (0x000000ffU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte64_f__115__sh));
        __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__110__b 
            = vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte64_f__115__Vfuncout;
    } else if ((0x00000026U > __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__110__i)) {
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte32_f__116__n 
            = (__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__110__i 
               - (IData)(0x00000022U));
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte32_f__116__sh 
            = VL_SHIFTR_III(32,32,32, 0x0000c588U, 
                            (((IData)(3U) - vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte32_f__116__n) 
                             << 3U));
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte32_f__116__Vfuncout 
            = (0x000000ffU & vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte32_f__116__sh);
        __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__110__b 
            = vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte32_f__116__Vfuncout;
    } else if ((0x00000028U > __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__110__i)) {
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte16_f__117__n 
            = (__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__110__i 
               - (IData)(0x00000026U));
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte16_f__117__sh 
            = VL_SHIFTR_III(16,16,32, 2U, (((IData)(1U) 
                                            - vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte16_f__117__n) 
                                           << 3U));
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte16_f__117__Vfuncout 
            = (0x000000ffU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte16_f__117__sh));
        __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__110__b 
            = vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte16_f__117__Vfuncout;
    } else if ((0x0000002aU > __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__110__i)) {
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte16_f__118__n 
            = (__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__110__i 
               - (IData)(0x00000028U));
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte16_f__118__sh 
            = VL_SHIFTR_III(16,16,32, 0x4801U, (((IData)(1U) 
                                                 - vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte16_f__118__n) 
                                                << 3U));
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte16_f__118__Vfuncout 
            = (0x000000ffU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte16_f__118__sh));
        __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__110__b 
            = vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte16_f__118__Vfuncout;
    } else if ((0x0000002cU > __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__110__i)) {
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte16_f__119__n 
            = (__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__110__i 
               - (IData)(0x0000002aU));
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte16_f__119__sh 
            = VL_SHIFTR_III(16,16,32, 2U, (((IData)(1U) 
                                            - vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte16_f__119__n) 
                                           << 3U));
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte16_f__119__Vfuncout 
            = (0x000000ffU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte16_f__119__sh));
        __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__110__b 
            = vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte16_f__119__Vfuncout;
    } else if ((0x0000002eU > __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__110__i)) {
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte16_f__120__n 
            = (__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__110__i 
               - (IData)(0x0000002cU));
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte16_f__120__sh 
            = VL_SHIFTR_III(16,16,32, 0x4801U, (((IData)(1U) 
                                                 - vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte16_f__120__n) 
                                                << 3U));
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte16_f__120__Vfuncout 
            = (0x000000ffU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte16_f__120__sh));
        __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__110__b 
            = vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte16_f__120__Vfuncout;
    } else if ((0x00000032U > __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__110__i)) {
        __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__110__b = 0U;
    } else if ((0x00000036U > __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__110__i)) {
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte32_f__121__n 
            = (__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__110__i 
               - (IData)(0x00000032U));
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte32_f__121__v 
            = __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__110__aidx;
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte32_f__121__sh 
            = VL_SHIFTR_III(32,32,32, vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte32_f__121__v, 
                            (((IData)(3U) - vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte32_f__121__n) 
                             << 3U));
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte32_f__121__Vfuncout 
            = (0x000000ffU & vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte32_f__121__sh);
        __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__110__b 
            = vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte32_f__121__Vfuncout;
    } else if ((0x0000003eU > __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__110__i)) {
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte64_f__122__n 
            = (__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__110__i 
               - (IData)(0x00000036U));
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte64_f__122__v 
            = __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__110__gm;
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte64_f__122__sh 
            = VL_SHIFTR_QQI(64,64,32, vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte64_f__122__v, 
                            (((IData)(7U) - vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte64_f__122__n) 
                             << 3U));
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte64_f__122__Vfuncout 
            = (0x000000ffU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte64_f__122__sh));
        __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__110__b 
            = vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte64_f__122__Vfuncout;
    } else if ((0x0000003eU == __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__110__i)) {
        __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__110__b 
            = __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__110__dom;
    } else if ((0x0000003fU == __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__110__i)) {
        __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__110__b = 0U;
    } else if ((0x00000042U > __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__110__i)) {
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte16_f__123__n 
            = (__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__110__i 
               - (IData)(0x00000040U));
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte16_f__123__v 
            = (0x0000ffffU & vlSelfRef.milan_datapath__DOT__csr__DOT__adp_idx0);
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte16_f__123__sh 
            = VL_SHIFTR_III(16,16,32, (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte16_f__123__v), 
                            (((IData)(1U) - vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte16_f__123__n) 
                             << 3U));
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte16_f__123__Vfuncout 
            = (0x000000ffU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte16_f__123__sh));
        __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__110__b 
            = vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte16_f__123__Vfuncout;
    } else if ((0x00000044U > __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__110__i)) {
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte16_f__124__n 
            = (__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__110__i 
               - (IData)(0x00000042U));
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte16_f__124__v 
            = (vlSelfRef.milan_datapath__DOT__csr__DOT__adp_idx0 
               >> 0x00000010U);
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte16_f__124__sh 
            = VL_SHIFTR_III(16,16,32, (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte16_f__124__v), 
                            (((IData)(1U) - vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte16_f__124__n) 
                             << 3U));
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte16_f__124__Vfuncout 
            = (0x000000ffU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte16_f__124__sh));
        __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__110__b 
            = vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte16_f__124__Vfuncout;
    } else if ((0x00000046U > __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__110__i)) {
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte16_f__125__n 
            = (__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__110__i 
               - (IData)(0x00000044U));
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte16_f__125__v 
            = __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__110__ifx;
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte16_f__125__sh 
            = VL_SHIFTR_III(16,16,32, (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte16_f__125__v), 
                            (((IData)(1U) - vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte16_f__125__n) 
                             << 3U));
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte16_f__125__Vfuncout 
            = (0x000000ffU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte16_f__125__sh));
        __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__110__b 
            = vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte16_f__125__Vfuncout;
    } else {
        __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__110__b = 0U;
    }
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__110__Vfuncout 
        = __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__110__b;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__adp_txs_wr_data_w 
        = __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__frame_byte_f__110__Vfuncout;
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
    vlSelfRef.milan_datapath__DOT__crft_emit_en_w = 
        (1U & (vlSelfRef.milan_datapath__DOT__csr__DOT__crft_ctrl 
               & (((vlSelfRef.milan_datapath__DOT__csr__DOT__aaf_ctrl 
                    >> 1U) | (3U != (3U & vlSelfRef.milan_datapath__DOT__csr__DOT__lwsrp_ctrl))) 
                  | ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__adm_admitted_w) 
                     >> 1U))));
    vlSelfRef.milan_datapath__DOT__aaf_stream_en_raw_w 
        = (1U & (vlSelfRef.milan_datapath__DOT__csr__DOT__aaf_ctrl 
                 & (((~ vlSelfRef.milan_datapath__DOT__csr__DOT__maap_ctrl) 
                     | (2U == (IData)(vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__state_r))) 
                    & (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__declaring_r) 
                        & ((~ vlSelfRef.milan_datapath__DOT__csr__DOT__lwsrp_ctrl) 
                           | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__adm_admitted_w))) 
                       | (vlSelfRef.milan_datapath__DOT__csr__DOT__aaf_ctrl 
                          >> 1U)))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__sr_adm_fsm_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__opt_r) 
           | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__adm_admitted_w));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_204 = ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__rsp_busy_w)) 
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
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_45 = (0x0000ffffU 
                                                 & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__rows_r
                                                 [(
                                                   (4U 
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
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_119 = ((4U 
                                                   == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__n_st_r)) 
                                                  & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__ca_probe_r) 
                                                     >> (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__pd_ix_w)));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_267 = (7U 
                                                  & ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_cnt_r 
                                                      >> 3U) 
                                                     - 
                                                     (1U 
                                                      & (- (IData)((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_286))))));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_284 = (((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_286) 
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
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_84 = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__acmp_is_tkr_w)
                                                  ? 
                                                 ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__gp_valid_r)) 
                                                  & (1U 
                                                     == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__state_r)))
                                                  : (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__lstn_txn_ready_w));
    vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__diag_ridx_w 
        = ((1U > (IData)(vlSelfRef.milan_datapath__DOT__aecp_diag_idx_w)) 
           & (IData)(vlSelfRef.milan_datapath__DOT__aecp_diag_idx_w));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__beat_w 
        = ((IData)(vlSelfRef.i_resp_mem_rsp_valid) 
           & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_203));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__fsm_rd_gnt_w 
        = ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__cap_active_w)) 
           & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__fsm_rd_req_w));
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
    vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__w1_en_w 
        = ((8U > (IData)(vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__ch1_w)) 
           & (IData)(vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__avb_ok_w));
    vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__w1_addr_w 
        = ((0x00000038U & ((IData)(vlSelfRef.milan_datapath__DOT__rsp_tuser_w) 
                           << 3U)) | (7U & (IData)(vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__ch1_w)));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__clr_relq_w = 0U;
    if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__maap_accept_w) 
         & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__mreq_rel_r))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__clr_relq_w 
            = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__clr_relq_w) 
               | (3U & ((IData)(1U) << (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__mreq_src_r))));
    }
    vlSelfRef.milan_datapath__DOT__avtprx_accept_p 
        = ((~ (IData)(vlSelfRef.milan_datapath__DOT__avtprx_stopped_w)) 
           & (IData)(vlSelfRef.milan_datapath__DOT__avtprx_accept_p_w));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__pick_w = 0U;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__pick_ok_w = 0U;
    if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pool_oversize_w) {
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
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_72 = ((8U 
                                                  > (IData)(vlSelfRef.milan_datapath__DOT__amap_walk_j_r)) 
                                                 & (IData)(vlSelfRef.milan_datapath__DOT__amap_opage_ok_w));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__eof_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__out_last_r) 
           & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__consume_w));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__push_w 
        = ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_261) 
           & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_normalizer__DOT__txn_valid_r));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__nrm_txn_ready_w 
        = ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_214) 
           | ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_213) 
              | ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_261) 
                 | (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_212))));
    if (vlSelfRef.__VdfgRegularize_h6e95ff9d_0_28) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__name_wdata_w 
            = vlSelfRef.i_desc_mem_rsp_data;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__name_waddr_w 
            = (0x000001ffU & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__beat_ix_r) 
                              + vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__name_load_lane_r));
    } else {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__name_wdata_w 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__opa_e_r;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__name_waddr_w 
            = (0x000001ffU & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__st_addr_w 
                              >> 3U));
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__name_wstrb_w 
        = (0x000000ffU & (Vmilan_datapath__ConstPool__CONST_h5302cfd2_0
                          [(7U & (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__uop_e_r 
                                          >> 0x0000001cU)))] 
                          | (- (IData)((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_28)))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__need_flush_w 
        = ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_112) 
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
         & (2U > (IData)(vlSelfRef.milan_datapath__DOT____Vcellinp__media_clock_restart__frame_idx_i)))) {
        vlSelfRef.milan_datapath__DOT__talker_diag__DOT__ev_f_w 
            = ((IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__ev_f_w) 
               | (3U & ((IData)(1U) << (1U & (IData)(vlSelfRef.milan_datapath__DOT____Vcellinp__media_clock_restart__frame_idx_i)))));
        if (((IData)(vlSelfRef.milan_datapath__DOT____Vcellinp__media_clock_restart__frame_mr_i) 
             != (1U & ((IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__mr_q_r) 
                       >> (1U & (IData)(vlSelfRef.milan_datapath__DOT____Vcellinp__media_clock_restart__frame_idx_i)))))) {
            vlSelfRef.milan_datapath__DOT__talker_diag__DOT__ev_mr_w 
                = ((IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__ev_mr_w) 
                   | (3U & ((IData)(1U) << (1U & (IData)(vlSelfRef.milan_datapath__DOT____Vcellinp__media_clock_restart__frame_idx_i)))));
        }
        if (((IData)(vlSelfRef.milan_datapath__DOT__aaf_frame_p_w)
              ? (IData)(vlSelfRef.milan_datapath__DOT__aaf_frame_tu_w)
              : (IData)(vlSelfRef.milan_datapath__DOT__crft_tu_last_w))) {
            vlSelfRef.milan_datapath__DOT__talker_diag__DOT__ev_tu_w 
                = ((IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__ev_tu_w) 
                   | (3U & ((IData)(1U) << (1U & (IData)(vlSelfRef.milan_datapath__DOT____Vcellinp__media_clock_restart__frame_idx_i)))));
        }
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__refuse_w 
        = ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__fit_w)) 
           & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_100));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__wgrant_now_w 
        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__wgrant_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__wgrant_now_w 
        = (((~ ((IData)(1U) << (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__aidx_r))) 
            & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__wgrant_now_w)) 
           | (3U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__fit_w) 
                    << (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__aidx_r))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__wgslope_now_w 
        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__wgslope_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__wgslope_now_w 
        = (((~ (0x00000000ffffffffULL << (0x0000003fU 
                                          & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__aidx_r) 
                                             << 5U)))) 
            & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__wgslope_now_w) 
           | ((QData)((IData)(((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__fit_w)
                                ? (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__slope_q_r 
                                           >> (0x0000003fU 
                                               & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__aidx_r) 
                                                  << 5U))))
                                : 0U))) << (0x0000003fU 
                                            & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__aidx_r) 
                                               << 5U))));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_21 = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_side_port__DOT__fwd_ok_w) 
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
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_254 = ((IData)(vlSelfRef.milan_datapath__DOT__amap_opage_ok_w) 
                                                  | (IData)(vlSelfRef.milan_datapath__DOT__amap_page_ok_w));
    vlSelfRef.milan_datapath__DOT__amap_in_rec_w = 0ULL;
    milan_datapath__DOT__amap_page_fmt__DOT__offq_c 
        = ((((IData)(vlSelfRef.milan_datapath__DOT__amap_page_ok_w)
              ? (IData)(vlSelfRef.milan_datapath__DOT__amapq_map_r)
              : 0U) << 3U) + (IData)(vlSelfRef.milan_datapath__DOT__amap_walk_jq_r));
    if ((IData)((0x80U == (0xc0U & (IData)(vlSelfRef.milan_datapath__DOT__amap_in_ent_q_r))))) {
        vlSelfRef.milan_datapath__DOT__amap_in_rec_w 
            = (((QData)((IData)(((0x00070000U & ((IData)(vlSelfRef.milan_datapath__DOT__amap_in_ent_q_r) 
                                                 << 0x0000000dU)) 
                                 | (7U & (IData)(vlSelfRef.milan_datapath__DOT__amap_in_ent_q_r))))) 
                << 0x00000020U) | (QData)((IData)((milan_datapath__DOT__amap_page_fmt__DOT__offq_c 
                                                   << 0x00000010U))));
    }
    milan_datapath__DOT__amap_page_slot__DOT__off_c 
        = ((((IData)(vlSelfRef.milan_datapath__DOT__amap_page_ok_w)
              ? (IData)(vlSelfRef.milan_datapath__DOT__amapq_map_r)
              : 0U) << 3U) + (IData)(vlSelfRef.milan_datapath__DOT__amap_walk_j_r));
    milan_datapath__DOT__amap_page_slot__DOT__g_c = milan_datapath__DOT__amap_page_slot__DOT__off_c;
    vlSelfRef.milan_datapath__DOT__amap_in_ent_w = 
        (((((IData)(vlSelfRef.milan_datapath__DOT__amap_page_ok_w) 
            & (8U > (IData)(vlSelfRef.milan_datapath__DOT__amap_walk_j_r))) 
           & (milan_datapath__DOT__amap_page_slot__DOT__off_c 
              < (8U & (- (IData)((0U == (IData)(vlSelfRef.milan_datapath__DOT__amapq_index_r))))))) 
          & (8U > milan_datapath__DOT__amap_page_slot__DOT__g_c))
          ? (0x000000ffU & (IData)((vlSelfRef.milan_datapath__DOT__amap_in_store_r 
                                    >> (0x0000003fU 
                                        & (milan_datapath__DOT__amap_page_slot__DOT__g_c 
                                           << 3U)))))
          : 0U);
    vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__push_same_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__push_ram_w) 
           & (((IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__pop_idx_r) 
               == vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__skid_addr_r
               [vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__skid_rp_r]) 
              & (IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__pop_act_w)));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__evr_strobe_w 
        = ((((((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_245) 
               << 5U) | ((IData)(vlSelfRef.milan_datapath__DOT__pp_gm_change_p_w) 
                         << 4U)) | (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_lstn_reg_change_w) 
                                     << 2U) | (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_evt_domain_change_w) 
                                                << 1U) 
                                               | ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__adp_evt_valid_w) 
                                                  & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__adp_evt_departed_w))))) 
            << 5U) | ((((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__adp_evt_departed_w)) 
                        & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__adp_evt_valid_w)) 
                       << 4U) | (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_evt_tk_unreg_w) 
                                  << 2U) | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_evt_tk_reg_w))));
    vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__match_hit 
        = ((vlSelfRef.milan_datapath__DOT__strtbl_sid_w 
            == vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__sid) 
           & (IData)(vlSelfRef.milan_datapath__DOT__strtbl_en_w));
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
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__aecp_rgy_req_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gx_req_w) 
           & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__rgy_any_w));
    vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pown_o_w 
        = (3U & (((IData)(vlSelfRef.milan_datapath__DOT__cmap_slot_w) 
                  - vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pbase_w[0U]) 
                 & (- (IData)((IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pown_v_w)))));
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
        = (1U & ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_55) 
                 | ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__echo_r) 
                    | ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__pay_w)) 
                       | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__rsp_rd_valid_w)))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__cmp_z_w 
        = ((3U == (7U & (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__uop_e_r 
                                 >> 0x0000001cU))))
            ? (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__opa_e_r 
               == vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__b_or_imm_w)
            : (0U == (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_115)));
    vlSelfRef.milan_datapath__DOT__aaf_tx_tlast = (
                                                   (3U 
                                                    == (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__est_r)) 
                                                   & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_180));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_192 = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__eff_len_w) 
                                                  + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__nvm_offset_w));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__ctr_ev_ok_w = 0U;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__ctr_ev_ix_w = 0U;
    if (((5U == (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_evt_type_w)) 
         & (2U > (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_evt_index_w)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__ctr_ev_ok_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__ctr_ev_ix_w 
            = (7U & (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_evt_index_w));
    } else if (((6U == (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_evt_type_w)) 
                & (2U > (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_evt_index_w)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__ctr_ev_ok_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__ctr_ev_ix_w 
            = (7U & ((IData)(2U) + (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_evt_index_w)));
    } else if (((9U == (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_evt_type_w)) 
                & (0U == (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_evt_index_w)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__ctr_ev_ok_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__ctr_ev_ix_w = 4U;
    } else if (((0x0024U == (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_evt_type_w)) 
                & (0U == (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_evt_index_w)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__ctr_ev_ok_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__ctr_ev_ix_w = 5U;
    }
    vlSelfRef.milan_datapath__DOT__pp_ctr_sout_pend_n 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_sout_pend_r) 
           | (IData)(vlSelfRef.milan_datapath__DOT__tkd_dirty_p_w));
    if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_evt_valid_w) 
          & (6U == (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_evt_type_w))) 
         & (0U == (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_evt_index_w)))) {
        vlSelfRef.milan_datapath__DOT__pp_ctr_sout_pend_n 
            = (2U & (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_sout_pend_n));
    }
    if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_evt_valid_w) 
          & (6U == (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_evt_type_w))) 
         & (1U == (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_evt_index_w)))) {
        vlSelfRef.milan_datapath__DOT__pp_ctr_sout_pend_n 
            = (1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_sout_pend_n));
    }
    vlSelfRef.milan_datapath__DOT__pp_ctr_sin_pend_n 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_sin_pend_r) 
           | (((IData)(vlSelfRef.milan_datapath__DOT__crf_dirty_p_w) 
               << 1U) | (IData)(vlSelfRef.milan_datapath__DOT__avtprx_dirty_p_w)));
    if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_evt_valid_w) 
          & (5U == (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_evt_type_w))) 
         & (0U == (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_evt_index_w)))) {
        vlSelfRef.milan_datapath__DOT__pp_ctr_sin_pend_n 
            = (2U & (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_sin_pend_n));
    }
    if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_evt_valid_w) 
          & (5U == (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_evt_type_w))) 
         & (1U == (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_evt_index_w)))) {
        vlSelfRef.milan_datapath__DOT__pp_ctr_sin_pend_n 
            = (1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_ctr_sin_pend_n));
    }
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
    __Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__305__t 
        = vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__et_r;
    __Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__305__Vfuncout 
        = (3U | ((IData)(__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__305__t) 
                 << 4U));
    vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__tram_raddr_w 
        = __Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__305__Vfuncout;
    if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__est_r))) {
        if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__est_r))) {
            vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT____VlemCall_0__taddr 
                = ((IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__ext_trd_go_w)
                    ? (0x0000001fU & (IData)(vlSelfRef.milan_datapath__DOT__csr_tctx_rd_addr_w))
                    : 3U);
            vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__tram_raddr_w 
                = vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT____VlemCall_0__taddr;
        } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__est_r))) {
            vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__307__t 
                = vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__et_r;
            vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__307__Vfuncout 
                = (5U | ((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__307__t) 
                         << 4U));
            vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__tram_raddr_w 
                = vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__307__Vfuncout;
        } else {
            vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__308__t 
                = vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__et_r;
            vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__308__Vfuncout 
                = (5U | ((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__308__t) 
                         << 4U));
            vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__tram_raddr_w 
                = vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__308__Vfuncout;
        }
    } else if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__est_r))) {
        if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__est_r))) {
            vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT____VlemCall_0__taddr 
                = ((IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__ext_trd_go_w)
                    ? (0x0000001fU & (IData)(vlSelfRef.milan_datapath__DOT__csr_tctx_rd_addr_w))
                    : 3U);
            vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__tram_raddr_w 
                = vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT____VlemCall_0__taddr;
        } else {
            vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__310__w 
                = ((0U == (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fph_r))
                    ? 4U : 3U);
            vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__310__t 
                = vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__et_r;
            vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__310__Vfuncout 
                = (((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__310__t) 
                    << 4U) | (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__310__w));
            vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__tram_raddr_w 
                = vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__310__Vfuncout;
        }
    } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__est_r))) {
        vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__311__w 
            = ((0U == (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fph_r))
                ? 1U : ((1U == (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fph_r))
                         ? 2U : 3U));
        vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__311__t 
            = vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__et_r;
        vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__311__Vfuncout 
            = (((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__311__t) 
                << 4U) | (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__311__w));
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__tram_raddr_w 
            = vlSelfRef.__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__311__Vfuncout;
    } else {
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT____VlemCall_0__taddr 
            = ((IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__ext_trd_go_w)
                ? (0x0000001fU & (IData)(vlSelfRef.milan_datapath__DOT__csr_tctx_rd_addr_w))
                : 3U);
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__tram_raddr_w 
            = vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT____VlemCall_0__taddr;
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__ix26_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__tix_w) 
           | ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__scfg_r) 
              | (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_42)));
    vlSelfRef.milan_datapath__DOT__pp_gsi_kind_w = 
        (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gavb_r)
           ? 1U : 2U) & (- (IData)((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gstri_r) 
                                             | (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_208)))))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gsi_any_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gstri_r) 
           | ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gavb_r) 
              | ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gasp_r) 
                 | (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_208))));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_69 = (Vmilan_datapath__ConstPool__TABLE_h5f1389fb_0
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
              & ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_239) 
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
            = (0x0000003fU & (IData)(milan_datapath__DOT__avtp_rx_monitor__DOT__eng_waddr_w));
    } else {
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ram_wdata_w 
            = vlSelfRef.milan_datapath__DOT__lctx_wr_data_sane_w;
        vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ram_waddr_w 
            = (0x0000003fU & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__lctx_wr_addr_r));
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
           & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_105));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_206 = ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_stage_ready_r)) 
                                                  & (4U 
                                                     <= (IData)(vlSelfRef.milan_datapath__DOT__pp_amap_edit_phase_w)));
    vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__pop_w 
        = (((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_tvalid_pipe_reg) 
            >> 1U) & (IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_tready_pipe));
    vlSelfRef.milan_datapath__DOT__rend_pcm_tvalid_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__emit_w) 
           & ((0U == vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__idxq_r
               [vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__idxq_rp_r]) 
              & (vlSelfRef.milan_datapath__DOT__pcm_route__DOT__route_r[0U] 
                 >> 1U)));
    vlSelfRef.milan_datapath__DOT__dpkt_pcm_tlast_w 
        = ((8U >= (IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__remain_r)) 
           & (IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__emit_w));
    vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__s_ok_w 
        = ((1U > vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__idxq_r
            [vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__idxq_rp_r]) 
           & (IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__emit_w));
    vlSelfRef.milan_datapath__DOT__ctlh_tx_tvalid = 
        ((IData)(vlSelfRef.milan_datapath__DOT__ctl_tx_mux__DOT__flush_r) 
         | ((IData)(vlSelfRef.milan_datapath__DOT__ctl_tx_mux__DOT__src_tvalid_w) 
            & (IData)(vlSelfRef.milan_datapath__DOT__ctl_tx_mux__DOT__active)));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_304 = ((0U 
                                                   == (IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__chans_pop_raw_w))
                                                   ? 2U
                                                   : (IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__chans_pop_raw_w));
    vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__c_in_w 
        = ((0U == (IData)(milan_datapath__DOT__render_setpoint__DOT__chans_in_raw_w))
            ? 2U : (IData)(milan_datapath__DOT__render_setpoint__DOT__chans_in_raw_w));
    vlSelfRef.milan_datapath__DOT__dpcrf_tvalid = ((IData)(vlSelfRef.milan_datapath__DOT__crf_dp_mux__DOT__flush_r) 
                                                   | ((IData)(vlSelfRef.milan_datapath__DOT__crf_dp_mux__DOT__src_tvalid_w) 
                                                      & (IData)(vlSelfRef.milan_datapath__DOT__crf_dp_mux__DOT__active)));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_293 = (0x0000003fU 
                                                  & ((IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__beat_r) 
                                                     + 
                                                     (0x0000003cU 
                                                      & ((((IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__slot_r) 
                                                           << 4U) 
                                                          + 
                                                          ((IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__rd_row_w) 
                                                           >> 1U)) 
                                                         << 2U))));
    vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__pop_dry_w 
        = ((0U == (IData)(milan_datapath__DOT__render_setpoint__DOT__fill_pop_w)) 
           & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_294));
    vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__pop_take_w 
        = ((0U != (IData)(milan_datapath__DOT__render_setpoint__DOT__fill_pop_w)) 
           & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_294));
    vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ext_rd_go_w 
        = ((0U == (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__mst_r)) 
           & ((0U == (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__pq_cnt_r)) 
              & ((~ (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__bind_pend_r)) 
                 & ((~ (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__sil_pend_r)) 
                    & ((((~ (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rds_dir_r)) 
                         & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rds_busy_r)) 
                        | (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_190)) 
                       & ((~ ((IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__penq_w) 
                              | ((IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__iv_pend_r) 
                                 | (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__depkt_any_w)))) 
                          & (0U == (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__iv_res_list_r))))))));
    vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__pdisp_new_w 
        = ((0U == (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__mst_r)) 
           & ((0U == (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__pq_cnt_r)) 
              & (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__penq_w)));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_235 = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rx_registering_w) 
                                                  & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_67));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_rx_hit_w 
        = (((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_67) 
            << 1U) | (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_68));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_236 = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rx_registering_w) 
                                                  & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_68));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__decl_grant_w 
        = (2U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__decl_grant_w));
    if ((1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_rx_hit_w)))) {
        if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__ctl_acc_w) 
                      & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r)))))) {
            if ((0U != (3U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__decl_pend_r)))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__decl_grant_w 
                    = (1U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__decl_grant_w));
            }
        }
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__decl_grant_w 
        = (1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__decl_grant_w));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_grant_w 
        = (2U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_grant_w));
    if ((1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_rx_hit_w)))) {
        if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__ctl_acc_w) 
                      & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r)))))) {
            if ((0U == (3U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__decl_pend_r)))) {
                if ((1U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_pend_r) 
                           | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_la_msrp_w)))) {
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_grant_w 
                        = (1U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_grant_w));
                }
            }
        }
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_grant_w 
        = (1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_grant_w));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_grant_w 
        = (2U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_grant_w));
    if ((1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_rx_hit_w)))) {
        if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__ctl_acc_w) 
                      & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r)))))) {
            if ((0U == (3U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__decl_pend_r)))) {
                if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_pend_r) 
                              | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_la_msrp_w))))) {
                    if ((1U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_pend_r) 
                               | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__p_periodic_r)))) {
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_grant_w 
                            = (1U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_grant_w));
                    }
                }
            }
        }
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_grant_w 
        = (1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_grant_w));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__walk_grant_w = 0U;
    if ((1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_rx_hit_w)))) {
        if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__ctl_acc_w) 
                      & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r)))))) {
            if ((0U == (3U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__decl_pend_r)))) {
                if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_pend_r) 
                              | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_la_msrp_w))))) {
                    if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_pend_r) 
                                  | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__p_periodic_r))))) {
                        if (((1U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__walk_r)) 
                             & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__wsrc_r)))) {
                            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__walk_grant_w = 1U;
                        }
                    }
                }
            }
        }
    }
    if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_rx_hit_w) 
                  >> 1U)))) {
        if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__ctl_acc_w) 
                      & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r))))) {
            if ((0U != (3U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__decl_pend_r) 
                              >> 2U)))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__decl_grant_w 
                    = (2U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__decl_grant_w));
            }
            if ((0U == (3U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__decl_pend_r) 
                              >> 2U)))) {
                if ((IData)((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_pend_r) 
                              >> 1U) | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_la_msrp_w)))) {
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_grant_w 
                        = (2U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_grant_w));
                }
                if ((1U & (~ (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_pend_r) 
                               >> 1U) | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_la_msrp_w))))) {
                    if ((IData)((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_pend_r) 
                                  >> 1U) | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__p_periodic_r)))) {
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_grant_w 
                            = (2U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_grant_w));
                    }
                    if ((1U & (~ (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_pend_r) 
                                   >> 1U) | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__p_periodic_r))))) {
                        if (((1U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__walk_r)) 
                             & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__wsrc_r))) {
                            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__walk_grant_w = 1U;
                        }
                    }
                }
            }
        }
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w 
        = (2U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w));
    if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_rx_hit_w))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w 
            = (1U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w));
    } else if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__ctl_acc_w) 
                & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w 
            = ((2U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w)) 
               | (1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_open_r))));
    } else if ((0U != (3U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__decl_pend_r)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w 
            = (1U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w));
    } else if ((1U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_pend_r) 
                      | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_la_msrp_w)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w 
            = (1U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w));
    } else if ((1U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_pend_r) 
                      | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__p_periodic_r)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w 
            = (1U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w));
    } else if (((1U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__walk_r)) 
                & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__wsrc_r)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w 
            = (1U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w));
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w 
        = (1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w 
        = (3U | (0xf0U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w)));
    if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_rx_hit_w))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w 
            = ((0xf0U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w)) 
               | (0x0000000fU & ((IData)(3U) + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_mrp_event_w))));
    } else if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__ctl_acc_w) 
                & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w 
            = (2U | (0xf0U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w)));
    } else if ((0U != (3U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__decl_pend_r)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w 
            = ((0xf0U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w)) 
               | ((1U == (3U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__decl_pend_r)))
                   ? 0U : 2U));
    } else if ((1U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_pend_r) 
                      | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_la_msrp_w)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w 
            = (9U | (0xf0U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w)));
    } else if ((1U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_pend_r) 
                      | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__p_periodic_r)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w 
            = (0x0000000aU | (0xf0U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w)));
    } else if (((1U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__walk_r)) 
                & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__wsrc_r)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w 
            = ((0xf0U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w)) 
               | ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__wtxla_r)
                   ? 0x0cU : 0x0bU));
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w 
        = (0x00000030U | (0x0fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w)));
    if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_rx_hit_w))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w 
            = (2U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w));
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w 
            = ((0x0fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w)) 
               | (0x000000f0U & (((IData)(3U) + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_mrp_event_w)) 
                                 << 4U)));
    } else if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__ctl_acc_w) 
                & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w 
            = ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w)) 
               | (2U & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_open_r)) 
                        << 1U)));
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w 
            = (0x00000020U | (0x0fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w)));
    } else if ((0U != (3U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__decl_pend_r) 
                             >> 2U)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w 
            = (2U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w));
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w 
            = ((0x0fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w)) 
               | (((1U == (3U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__decl_pend_r) 
                                 >> 2U))) ? 0U : 2U) 
                  << 4U));
    } else if ((IData)((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_pend_r) 
                         >> 1U) | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_la_msrp_w)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w 
            = (2U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w));
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w 
            = (0x00000090U | (0x0fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w)));
    } else if ((IData)((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_pend_r) 
                         >> 1U) | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__p_periodic_r)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w 
            = (2U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w));
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w 
            = (0x000000a0U | (0x0fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w)));
    } else if (((1U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__walk_r)) 
                & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__wsrc_r))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w 
            = (2U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w));
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w 
            = ((0x0fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w)) 
               | (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__wtxla_r)
                    ? 0x0cU : 0x0bU) << 4U));
    }
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_22 = ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_228) 
                                                 & ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_39) 
                                                    & ((5U 
                                                        >= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_mrp_event_w)) 
                                                       & ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_95) 
                                                          & ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_da_w 
                                                              == 
                                                              (0x0000ffffffffffffULL 
                                                               & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__da_r[2U])) 
                                                                   << 0x00000010U) 
                                                                  | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__da_r[1U])) 
                                                                     >> 0x00000010U)))) 
                                                             & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_vid_w) 
                                                                == 
                                                                (0x00000fffU 
                                                                 & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vid_r 
                                                                    >> 0x0000000cU))))))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_rx_hit_w 
        = ((((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_228) 
             & ((3U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_attr_type_w)) 
                & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_95))) 
            << 1U) | ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_229) 
                      & ((3U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_attr_type_w)) 
                         & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_94))));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_38 = ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_229) 
                                                 & ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_39) 
                                                    & ((5U 
                                                        >= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_mrp_event_w)) 
                                                       & ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_94) 
                                                          & ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_da_w 
                                                              == 
                                                              (0x0000ffffffffffffULL 
                                                               & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__da_r[1U])) 
                                                                   << 0x00000020U) 
                                                                  | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__da_r[0U]))))) 
                                                             & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_vid_w) 
                                                                == 
                                                                (0x00000fffU 
                                                                 & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vid_r)))))));
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
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__fmtin_r
                [(1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT____Vcellinp__u_dyn__desc_index_i))];
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__vld_w 
                = (QData)((IData)((1U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__fmtin_v_r) 
                                         >> (1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT____Vcellinp__u_dyn__desc_index_i))))));
        } else if ((4U == (0x00001fffU & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__st_addr_w 
                                          >> 3U)))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__val_w 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__fmtout_r
                [(1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT____Vcellinp__u_dyn__desc_index_i))];
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__vld_w 
                = (QData)((IData)((1U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__fmtout_v_r) 
                                         >> (1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT____Vcellinp__u_dyn__desc_index_i))))));
        } else if ((5U == (0x00001fffU & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__st_addr_w 
                                          >> 3U)))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__val_w 
                = (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__ptoff_r
                                  [(1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT____Vcellinp__u_dyn__desc_index_i))]));
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__vld_w 
                = (QData)((IData)((1U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__ptoff_v_r) 
                                         >> (1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT____Vcellinp__u_dyn__desc_index_i))))));
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
           | (IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__iter_arm_w));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_296 = (0x0000003fU 
                                                  & ((0x0000003cU 
                                                      & ((vlSelfRef.__VdfgRegularize_h6e95ff9d_0_292 
                                                          + 
                                                          ((IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__wptr_in_w) 
                                                           >> 1U)) 
                                                         << 2U)) 
                                                     + 
                                                     (7U 
                                                      & ((IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__chpos_r) 
                                                         >> 1U))));
    vlSelfRef.milan_datapath__DOT__gsi_tkreg_w = (3U 
                                                  & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_tk_reg_state_w) 
                                                     >> 
                                                     (2U 
                                                      & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__desc_ix_r) 
                                                         << 1U))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_snk_fail_code_w 
        = ((0x0000ff00U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__fcode_r) 
                           & ((- (IData)((2U == (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_187)))) 
                              << 8U))) | (IData)(vlSelfRef.milan_datapath__DOT__lwsrp_ta_fail_code));
    vlSelfRef.milan_datapath__DOT____Vcellinp__csr__i_acmpl_state 
        = ((0x80000000U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__bound_hold_r) 
                           << 0x0000001eU)) | ((0x0fff0000U 
                                                & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__bound_vlan_r 
                                                   << 0x00000010U)) 
                                               | ((((0U 
                                                     != (IData)(vlSelfRef.milan_datapath__DOT__lwsrp_ta_fail_code)) 
                                                    << 7U) 
                                                   | (((1U 
                                                        == (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_50)) 
                                                       << 6U) 
                                                      | (0x00000010U 
                                                         & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__bound_hold_r) 
                                                            << 4U)))) 
                                                  | (8U 
                                                     & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__bound_hold_r) 
                                                        << 3U)))));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_88 = ((1U 
                                                  == (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_31)) 
                                                 & ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_33) 
                                                    >> 1U));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_87 = ((1U 
                                                  == (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_51)) 
                                                 & ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp_listener_decl) 
                                                    >> 1U));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_tk_decl_state_w 
        = (((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_31) 
            << 2U) | (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_51));
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
        = (0x000000ffU & (IData)((vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__eff_dmac_w 
                                  >> 0x00000028U)));
    vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[1U] 
        = (0x000000ffU & (IData)((vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__eff_dmac_w 
                                  >> 0x00000020U)));
    vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[2U] 
        = (0x000000ffU & (IData)((vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__eff_dmac_w 
                                  >> 0x00000018U)));
    vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[3U] 
        = (0x000000ffU & (IData)((vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__eff_dmac_w 
                                  >> 0x00000010U)));
    vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[4U] 
        = (0x000000ffU & (IData)((vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__eff_dmac_w 
                                  >> 8U)));
    vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[5U] 
        = (0x000000ffU & (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__eff_dmac_w));
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
            << 5U) | (0x0000000fU & ((IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__eff_vid_w) 
                                     >> 8U)));
    vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[15U] 
        = (0x000000ffU & (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__eff_vid_w));
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
        = vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__echn_w;
    vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[37U] = 0x20U;
    vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[38U] = 0U;
    vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[39U] 
        = (0x000000f8U & (((IData)(6U) * (7U & ((IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__echn_w) 
                                                >> 1U))) 
                          << 3U));
    vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[40U] = 0U;
    vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__fb[41U] = 0U;
    if ((0U < (0x0000001fU & ((IData)(6U) * (7U & ((IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__echn_w) 
                                                   >> 1U)))))) {
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
    if ((1U < (0x0000001fU & ((IData)(6U) * (7U & ((IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__echn_w) 
                                                   >> 1U)))))) {
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
    if ((2U < (0x0000001fU & ((IData)(6U) * (7U & ((IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__echn_w) 
                                                   >> 1U)))))) {
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
    if ((3U < (0x0000001fU & ((IData)(6U) * (7U & ((IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__echn_w) 
                                                   >> 1U)))))) {
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
    if ((4U < (0x0000001fU & ((IData)(6U) * (7U & ((IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__echn_w) 
                                                   >> 1U)))))) {
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
    if ((5U < (0x0000001fU & ((IData)(6U) * (7U & ((IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__echn_w) 
                                                   >> 1U)))))) {
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
    if ((6U < (0x0000001fU & ((IData)(6U) * (7U & ((IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__echn_w) 
                                                   >> 1U)))))) {
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
    if ((7U < (0x0000001fU & ((IData)(6U) * (7U & ((IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__echn_w) 
                                                   >> 1U)))))) {
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
    if ((8U < (0x0000001fU & ((IData)(6U) * (7U & ((IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__echn_w) 
                                                   >> 1U)))))) {
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
    if ((9U < (0x0000001fU & ((IData)(6U) * (7U & ((IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__echn_w) 
                                                   >> 1U)))))) {
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
    if ((0x0aU < (0x0000001fU & ((IData)(6U) * (7U 
                                                & ((IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__echn_w) 
                                                   >> 1U)))))) {
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
    if ((0x0bU < (0x0000001fU & ((IData)(6U) * (7U 
                                                & ((IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__echn_w) 
                                                   >> 1U)))))) {
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
    if ((0x0cU < (0x0000001fU & ((IData)(6U) * (7U 
                                                & ((IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__echn_w) 
                                                   >> 1U)))))) {
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
    if ((0x0dU < (0x0000001fU & ((IData)(6U) * (7U 
                                                & ((IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__echn_w) 
                                                   >> 1U)))))) {
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
    if ((0x0eU < (0x0000001fU & ((IData)(6U) * (7U 
                                                & ((IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__echn_w) 
                                                   >> 1U)))))) {
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
    if ((0x0fU < (0x0000001fU & ((IData)(6U) * (7U 
                                                & ((IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__echn_w) 
                                                   >> 1U)))))) {
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
    if ((0x10U < (0x0000001fU & ((IData)(6U) * (7U 
                                                & ((IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__echn_w) 
                                                   >> 1U)))))) {
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
    if ((0x11U < (0x0000001fU & ((IData)(6U) * (7U 
                                                & ((IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__echn_w) 
                                                   >> 1U)))))) {
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
    if ((0x12U < (0x0000001fU & ((IData)(6U) * (7U 
                                                & ((IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__echn_w) 
                                                   >> 1U)))))) {
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
    if ((0x13U < (0x0000001fU & ((IData)(6U) * (7U 
                                                & ((IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__echn_w) 
                                                   >> 1U)))))) {
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
    if ((0x14U < (0x0000001fU & ((IData)(6U) * (7U 
                                                & ((IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__echn_w) 
                                                   >> 1U)))))) {
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
    if ((0x15U < (0x0000001fU & ((IData)(6U) * (7U 
                                                & ((IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__echn_w) 
                                                   >> 1U)))))) {
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
    if ((0x16U < (0x0000001fU & ((IData)(6U) * (7U 
                                                & ((IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__echn_w) 
                                                   >> 1U)))))) {
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
    if ((0x17U < (0x0000001fU & ((IData)(6U) * (7U 
                                                & ((IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__echn_w) 
                                                   >> 1U)))))) {
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
    vlSelfRef.milan_datapath__DOT__pp_src_sid_w[0U] 
        = (IData)((vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w 
                   << 0x00000010U));
    vlSelfRef.milan_datapath__DOT__pp_src_sid_w[1U] 
        = (IData)(((vlSelfRef.milan_datapath__DOT__csr__DOT__mac_wire_w 
                    << 0x00000010U) >> 0x00000020U));
    vlSelfRef.milan_datapath__DOT__pp_src_sid_w[2U] 
        = (IData)(vlSelfRef.milan_datapath__DOT__eff_crft_sid_w);
    vlSelfRef.milan_datapath__DOT__pp_src_sid_w[3U] 
        = (IData)((vlSelfRef.milan_datapath__DOT__eff_crft_sid_w 
                   >> 0x00000020U));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__last_byte_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__wr_valid_w) 
           & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__bidx_r) 
              == (0x0000003fU & ((IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__nbytes_w) 
                                 - (IData)(1U)))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__set_lsn_w = 0U;
    if (((3U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_out_w)) 
         != (3U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__lsn_q_r)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__set_lsn_w 
            = (1U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__set_lsn_w));
    }
    if (((3U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_out_w) 
                >> 2U)) != (3U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__lsn_q_r) 
                                  >> 2U)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__set_lsn_w 
            = (2U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__set_lsn_w));
    }
    vlSelfRef.milan_datapath__DOT__gsi_lreg_w = (3U 
                                                 & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_out_w) 
                                                    >> 
                                                    (2U 
                                                     & ((IData)(vlSelfRef.milan_datapath__DOT__gsiq_index_r) 
                                                        << 1U))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_rec2_w[0U] 
        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__rec_q_r[0U];
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_rec2_w[1U] 
        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__rec_q_r[1U];
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_rec2_w[2U] 
        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__rec_q_r[2U];
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_we_w = 0U;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_open_w = 0U;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_close_w = 0U;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_initset_w = 0U;
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_daok2_w = 0U;
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_gate_w = 0U;
    if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_code_r))) {
        if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_code_r))) {
            if ((1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_code_r)))) {
                if ((0U == (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__rec_q_r[2U] 
                                  >> 0x00000012U)))) {
                    if ((1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__maap_avail_w)))) {
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_initset_w = 1U;
                    }
                }
            }
        } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_code_r))) {
            milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_daok2_w 
                = (1U & ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__rec_q_r[2U] 
                          >> 0x00000011U) & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__pe_conflict_r) 
                                                >> (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_src_r)))));
            vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__fresh_f__84__r[0U] 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__rec_q_r[0U];
            vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__fresh_f__84__r[1U] 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__rec_q_r[1U];
            vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__fresh_f__84__r[2U] 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__rec_q_r[2U];
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT____VlemCall_8__fresh_f 
                = ((vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__fresh_f__84__r[2U] 
                    >> 0x00000010U) & (0x00003a98U 
                                       > (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__now_ms_r 
                                          - ((vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__fresh_f__84__r[2U] 
                                              << 0x00000010U) 
                                             | (vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__fresh_f__84__r[1U] 
                                                >> 0x00000010U)))));
            vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__lsn_reg_f__85__s 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_src_r;
            vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__lsn_state_f__86__s 
                = vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__lsn_reg_f__85__s;
            vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__lsn_state_f__86__Vfuncout 
                = (3U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_out_w) 
                         >> (3U & ((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__lsn_state_f__86__s) 
                                   << 1U))));
            vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__lsn_reg_f__85____VlefCall_0__lsn_state_f 
                = vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__lsn_state_f__86__Vfuncout;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT____VlemCall_9__lsn_reg_f 
                = (0U != (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__lsn_reg_f__85____VlefCall_0__lsn_state_f));
            milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_gate_w 
                = ((IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_daok2_w) 
                   & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT____VlemCall_8__fresh_f) 
                      | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT____VlemCall_9__lsn_reg_f)));
            if ((IData)(((0x00040000U == (0x000c0000U 
                                          & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__rec_q_r[2U])) 
                         & (IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_gate_w)))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_rec2_w[2U] 
                    = (0x00080000U | (0x0003ffffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_rec2_w[2U]));
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_open_w = 1U;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_we_w = 1U;
            } else if ((IData)(((0x00080000U == (0x000c0000U 
                                                 & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__rec_q_r[2U])) 
                                & (~ (IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_gate_w))))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_rec2_w[2U] 
                    = (0x00040000U | (0x0003ffffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_rec2_w[2U]));
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_close_w = 1U;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_we_w = 1U;
            } else if ((0U == (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__rec_q_r[2U] 
                                     >> 0x00000012U)))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_initset_w = 1U;
            }
        } else if ((3U == (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__rec_q_r[2U] 
                                 >> 0x00000012U)))) {
            if ((0x00020000U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__rec_q_r[2U])) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_rec2_w[2U] 
                    = (0x00040000U | (0x0003ffffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_rec2_w[2U]));
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_we_w = 1U;
                milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_daok2_w 
                    = (1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__pe_conflict_r) 
                                >> (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_src_r))));
                vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__fresh_f__87__r[0U] 
                    = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__rec_q_r[0U];
                vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__fresh_f__87__r[1U] 
                    = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__rec_q_r[1U];
                vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__fresh_f__87__r[2U] 
                    = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__rec_q_r[2U];
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT____VlemCall_3__fresh_f 
                    = ((vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__fresh_f__87__r[2U] 
                        >> 0x00000010U) & (0x00003a98U 
                                           > (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__now_ms_r 
                                              - ((vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__fresh_f__87__r[2U] 
                                                  << 0x00000010U) 
                                                 | (vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__fresh_f__87__r[1U] 
                                                    >> 0x00000010U)))));
                vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__lsn_reg_f__88__s 
                    = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_src_r;
                vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__lsn_state_f__89__s 
                    = vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__lsn_reg_f__88__s;
                vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__lsn_state_f__89__Vfuncout 
                    = (3U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_out_w) 
                             >> (3U & ((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__lsn_state_f__89__s) 
                                       << 1U))));
                vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__lsn_reg_f__88____VlefCall_0__lsn_state_f 
                    = vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__lsn_state_f__89__Vfuncout;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT____VlemCall_4__lsn_reg_f 
                    = (0U != (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__lsn_reg_f__88____VlefCall_0__lsn_state_f));
                milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_gate_w 
                    = ((IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_daok2_w) 
                       & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT____VlemCall_3__fresh_f) 
                          | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT____VlemCall_4__lsn_reg_f)));
                if (milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_gate_w) {
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_rec2_w[2U] 
                        = (0x00080000U | (0x0003ffffU 
                                          & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_rec2_w[2U]));
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_open_w = 1U;
                }
            } else {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_rec2_w[2U] 
                    = (0x0003ffffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_rec2_w[2U]);
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_we_w = 1U;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_initset_w = 1U;
            }
        } else {
            milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_daok2_w 
                = (1U & ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__rec_q_r[2U] 
                          >> 0x00000011U) & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__pe_conflict_r) 
                                                >> (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_src_r)))));
            vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__fresh_f__91__r[0U] 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__rec_q_r[0U];
            vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__fresh_f__91__r[1U] 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__rec_q_r[1U];
            vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__fresh_f__91__r[2U] 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__rec_q_r[2U];
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT____VlemCall_6__fresh_f 
                = ((vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__fresh_f__91__r[2U] 
                    >> 0x00000010U) & (0x00003a98U 
                                       > (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__now_ms_r 
                                          - ((vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__fresh_f__91__r[2U] 
                                              << 0x00000010U) 
                                             | (vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__fresh_f__91__r[1U] 
                                                >> 0x00000010U)))));
            vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__lsn_reg_f__92__s 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_src_r;
            vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__lsn_state_f__93__s 
                = vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__lsn_reg_f__92__s;
            vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__lsn_state_f__93__Vfuncout 
                = (3U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_out_w) 
                         >> (3U & ((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__lsn_state_f__93__s) 
                                   << 1U))));
            vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__lsn_reg_f__92____VlefCall_0__lsn_state_f 
                = vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__lsn_state_f__93__Vfuncout;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT____VlemCall_7__lsn_reg_f 
                = (0U != (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__lsn_reg_f__92____VlefCall_0__lsn_state_f));
            milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_gate_w 
                = ((IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_daok2_w) 
                   & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT____VlemCall_6__fresh_f) 
                      | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT____VlemCall_7__lsn_reg_f)));
            if ((IData)(((0x00080000U == (0x000c0000U 
                                          & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__rec_q_r[2U])) 
                         & (~ (IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_gate_w))))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_close_w = 1U;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_rec2_w[2U] 
                    = (0x00040000U | (0x0003ffffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_rec2_w[2U]));
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_we_w = 1U;
            }
        }
    } else if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_code_r))) {
        if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_code_r))) {
            if ((2U == (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__rec_q_r[2U] 
                              >> 0x00000012U)))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_close_w = 1U;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_rec2_w[2U] 
                    = (0x000c0000U | vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_rec2_w[2U]);
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_we_w = 1U;
            }
        } else {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_rec2_w[2U] 
                = (0x000dffffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_rec2_w[2U]);
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_we_w = 1U;
            if ((2U == (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__rec_q_r[2U] 
                              >> 0x00000012U)))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_close_w = 1U;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_rec2_w[2U] 
                    = (0x000c0000U | vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_rec2_w[2U]);
            } else if ((1U == (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__rec_q_r[2U] 
                                     >> 0x00000012U)))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_rec2_w[2U] 
                    = (0x0003ffffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_rec2_w[2U]);
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_initset_w = 1U;
            }
        }
    } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_code_r))) {
        if ((2U == (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__rec_q_r[2U] 
                          >> 0x00000012U)))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_close_w = 1U;
        }
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_rec2_w[0U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_rec2_w[1U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_rec2_w[2U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_we_w = 1U;
    } else {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_rec2_w[0U] 
            = (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__gp_da_r);
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_rec2_w[1U] 
            = ((0xffff0000U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_rec2_w[1U]) 
               | (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__gp_da_r 
                          >> 0x00000020U)));
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_we_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_rec2_w[2U] 
            = (0x00020000U | vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_rec2_w[2U]);
        if ((0U == (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__rec_q_r[2U] 
                          >> 0x00000012U)))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_rec2_w[2U] 
                = (0x00040000U | (0x0003ffffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_rec2_w[2U]));
        }
        milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_daok2_w 
            = (1U & ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_rec2_w[2U] 
                      >> 0x00000011U) & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__pe_conflict_r) 
                                            >> (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_src_r)))));
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__fresh_f__94__r[0U] 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_rec2_w[0U];
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__fresh_f__94__r[1U] 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_rec2_w[1U];
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__fresh_f__94__r[2U] 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_rec2_w[2U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT____VlemCall_1__fresh_f 
            = ((vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__fresh_f__94__r[2U] 
                >> 0x00000010U) & (0x00003a98U > (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__now_ms_r 
                                                  - 
                                                  ((vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__fresh_f__94__r[2U] 
                                                    << 0x00000010U) 
                                                   | (vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__fresh_f__94__r[1U] 
                                                      >> 0x00000010U)))));
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__lsn_reg_f__95__s 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_src_r;
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__lsn_state_f__96__s 
            = vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__lsn_reg_f__95__s;
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__lsn_state_f__96__Vfuncout 
            = (3U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_out_w) 
                     >> (3U & ((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__lsn_state_f__96__s) 
                               << 1U))));
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__lsn_reg_f__95____VlefCall_0__lsn_state_f 
            = vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__lsn_state_f__96__Vfuncout;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT____VlemCall_2__lsn_reg_f 
            = (0U != (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__lsn_reg_f__95____VlefCall_0__lsn_state_f));
        milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_gate_w 
            = ((IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_daok2_w) 
               & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT____VlemCall_1__fresh_f) 
                  | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT____VlemCall_2__lsn_reg_f)));
        if ((IData)(((0x00040000U == (0x000c0000U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_rec2_w[2U])) 
                     & (IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_gate_w)))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_rec2_w[2U] 
                = (0x00080000U | (0x0003ffffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_rec2_w[2U]));
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_open_w = 1U;
        }
    }
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
                } else if ((0x00000010U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
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
                        if ((0x00000020U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                            if ((0x00000010U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                                if ((8U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
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
                                } else if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
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
                                } else if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
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
                        } else if ((0x00000010U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                            if ((8U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
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
                        } else if ((8U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
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
                    } else if ((0x00000020U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                        if ((0x00000010U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                            if ((8U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                                if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
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
                                } else if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
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
                } else if ((0x00000010U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                    if ((8U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                        if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
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
            } else if ((0x00000020U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                if ((0x00000010U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
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
                if ((0x00000020U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
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
                } else if ((8U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                    if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
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
                if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
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
}
