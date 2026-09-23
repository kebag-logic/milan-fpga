// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vmilan_datapath.h for the primary calling header

#include "Vmilan_datapath__pch.h"

extern const VlWide<14>/*447:0*/ Vmilan_datapath__ConstPool__CONST_hcc9a9126_0;
extern const VlWide<9>/*287:0*/ Vmilan_datapath__ConstPool__CONST_h9a2fc1c8_0;
extern const VlWide<18>/*575:0*/ Vmilan_datapath__ConstPool__CONST_h026f187a_0;
extern const VlWide<9>/*287:0*/ Vmilan_datapath__ConstPool__CONST_hc5471b50_0;

void Vmilan_datapath___024root___nba_sequent__TOP__2(Vmilan_datapath___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vmilan_datapath___024root___nba_sequent__TOP__2\n"); );
    Vmilan_datapath__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    VlUnpacked<SData/*9:0*/, 4> milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__4__KET____DOT__u_rx_slots__DOT__len_r;
    for (int __Vi0 = 0; __Vi0 < 4; ++__Vi0) {
        milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__4__KET____DOT__u_rx_slots__DOT__len_r[__Vi0] = 0;
    }
    VlUnpacked<SData/*9:0*/, 4> milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__1__KET____DOT__u_rx_slots__DOT__len_r;
    for (int __Vi0 = 0; __Vi0 < 4; ++__Vi0) {
        milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__1__KET____DOT__u_rx_slots__DOT__len_r[__Vi0] = 0;
    }
    VlUnpacked<SData/*9:0*/, 4> milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__0__KET____DOT__u_rx_slots__DOT__len_r;
    for (int __Vi0 = 0; __Vi0 < 4; ++__Vi0) {
        milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__0__KET____DOT__u_rx_slots__DOT__len_r[__Vi0] = 0;
    }
    QData/*63:0*/ __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__gm_slice_f__115__Vfuncout;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__gm_slice_f__115__Vfuncout = 0;
    CData/*0:0*/ __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__gm_slice_f__115__ifx;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__gm_slice_f__115__ifx = 0;
    IData/*31:0*/ __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__gm_slice_f__115__i;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__gm_slice_f__115__i = 0;
    CData/*7:0*/ __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__dom_slice_f__116__Vfuncout;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__dom_slice_f__116__Vfuncout = 0;
    CData/*0:0*/ __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__dom_slice_f__116__ifx;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__dom_slice_f__116__ifx = 0;
    IData/*31:0*/ __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__dom_slice_f__116__i;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__dom_slice_f__116__i = 0;
    SData/*15:0*/ __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__inc16__142__Vfuncout;
    __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__inc16__142__Vfuncout = 0;
    SData/*15:0*/ __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__inc16__142__v;
    __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__inc16__142__v = 0;
    IData/*31:0*/ __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__143__didx;
    __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__143__didx = 0;
    SData/*15:0*/ __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__143__meas;
    __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__143__meas = 0;
    IData/*31:0*/ __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__144__didx;
    __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__144__didx = 0;
    SData/*15:0*/ __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__144__meas;
    __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__144__meas = 0;
    IData/*31:0*/ __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__145__didx;
    __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__145__didx = 0;
    SData/*15:0*/ __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__145__meas;
    __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__145__meas = 0;
    IData/*31:0*/ __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__146__didx;
    __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__146__didx = 0;
    SData/*15:0*/ __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__146__meas;
    __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__146__meas = 0;
    IData/*31:0*/ __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__147__didx;
    __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__147__didx = 0;
    SData/*15:0*/ __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__147__meas;
    __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__147__meas = 0;
    SData/*15:0*/ __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__inc16__148__Vfuncout;
    __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__inc16__148__Vfuncout = 0;
    SData/*15:0*/ __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__inc16__148__v;
    __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__inc16__148__v = 0;
    SData/*15:0*/ __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__inc16__149__Vfuncout;
    __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__inc16__149__Vfuncout = 0;
    SData/*15:0*/ __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__inc16__149__v;
    __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__inc16__149__v = 0;
    SData/*15:0*/ __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__inc16__150__Vfuncout;
    __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__inc16__150__Vfuncout = 0;
    SData/*15:0*/ __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__inc16__150__v;
    __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__inc16__150__v = 0;
    IData/*31:0*/ __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__151__didx;
    __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__151__didx = 0;
    SData/*15:0*/ __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__151__meas;
    __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__151__meas = 0;
    IData/*31:0*/ __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__152__didx;
    __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__152__didx = 0;
    SData/*15:0*/ __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__152__meas;
    __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__152__meas = 0;
    IData/*31:0*/ __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__153__didx;
    __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__153__didx = 0;
    SData/*15:0*/ __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__153__meas;
    __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__153__meas = 0;
    IData/*31:0*/ __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__154__didx;
    __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__154__didx = 0;
    SData/*15:0*/ __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__154__meas;
    __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__154__meas = 0;
    IData/*31:0*/ __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__155__didx;
    __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__155__didx = 0;
    SData/*15:0*/ __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__155__meas;
    __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__155__meas = 0;
    SData/*15:0*/ __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__inc16__156__Vfuncout;
    __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__inc16__156__Vfuncout = 0;
    SData/*15:0*/ __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__inc16__156__v;
    __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__inc16__156__v = 0;
    SData/*15:0*/ __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__inc16__157__Vfuncout;
    __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__inc16__157__Vfuncout = 0;
    SData/*15:0*/ __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__inc16__157__v;
    __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__inc16__157__v = 0;
    QData/*47:0*/ __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_hit__211__start_a;
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_hit__211__start_a = 0;
    SData/*15:0*/ __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_hit__211__cnt_a;
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_hit__211__cnt_a = 0;
    SData/*15:0*/ __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_hit__211__our_s;
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_hit__211__our_s = 0;
    SData/*15:0*/ __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_hit__211__our_e;
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_hit__211__our_e = 0;
    SData/*15:0*/ __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_hit__211__req_s;
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_hit__211__req_s = 0;
    SData/*15:0*/ __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_hit__211__req_e;
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_hit__211__req_e = 0;
    SData/*15:0*/ __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rand_offset__212__Vfuncout;
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rand_offset__212__Vfuncout = 0;
    SData/*15:0*/ __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rand_offset__212__rnd;
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rand_offset__212__rnd = 0;
    CData/*7:0*/ __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rand_offset__212__cnt;
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rand_offset__212__cnt = 0;
    SData/*15:0*/ __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rand_offset__212__o;
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rand_offset__212__o = 0;
    QData/*47:0*/ __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__213__start_a;
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__213__start_a = 0;
    SData/*15:0*/ __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__213__cnt_a;
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__213__cnt_a = 0;
    SData/*15:0*/ __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__213__our_s;
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__213__our_s = 0;
    SData/*15:0*/ __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__213__our_e;
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__213__our_e = 0;
    SData/*15:0*/ __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__213__req_s;
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__213__req_s = 0;
    SData/*15:0*/ __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__213__req_e;
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__213__req_e = 0;
    SData/*15:0*/ __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__213__c_s;
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__213__c_s = 0;
    SData/*15:0*/ __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__213__c_c;
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__213__c_c = 0;
    QData/*47:0*/ __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__214__start_a;
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__214__start_a = 0;
    SData/*15:0*/ __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__214__cnt_a;
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__214__cnt_a = 0;
    SData/*15:0*/ __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__214__our_s;
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__214__our_s = 0;
    SData/*15:0*/ __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__214__our_e;
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__214__our_e = 0;
    SData/*15:0*/ __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__214__req_s;
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__214__req_s = 0;
    SData/*15:0*/ __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__214__req_e;
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__214__req_e = 0;
    SData/*15:0*/ __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__214__c_s;
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__214__c_s = 0;
    SData/*15:0*/ __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__214__c_c;
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__214__c_c = 0;
    QData/*47:0*/ __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_hit__215__start_a;
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_hit__215__start_a = 0;
    SData/*15:0*/ __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_hit__215__cnt_a;
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_hit__215__cnt_a = 0;
    SData/*15:0*/ __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_hit__215__our_s;
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_hit__215__our_s = 0;
    SData/*15:0*/ __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_hit__215__our_e;
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_hit__215__our_e = 0;
    SData/*15:0*/ __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_hit__215__req_s;
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_hit__215__req_s = 0;
    SData/*15:0*/ __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_hit__215__req_e;
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_hit__215__req_e = 0;
    SData/*15:0*/ __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rand_offset__216__Vfuncout;
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rand_offset__216__Vfuncout = 0;
    SData/*15:0*/ __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rand_offset__216__rnd;
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rand_offset__216__rnd = 0;
    CData/*7:0*/ __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rand_offset__216__cnt;
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rand_offset__216__cnt = 0;
    SData/*15:0*/ __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rand_offset__216__o;
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rand_offset__216__o = 0;
    CData/*3:0*/ __Vfunc_milan_datapath__DOT__render_setpoint__DOT__chwrap__228__ch;
    __Vfunc_milan_datapath__DOT__render_setpoint__DOT__chwrap__228__ch = 0;
    CData/*3:0*/ __Vfunc_milan_datapath__DOT__render_setpoint__DOT__chwrap__228__chans;
    __Vfunc_milan_datapath__DOT__render_setpoint__DOT__chwrap__228__chans = 0;
    SData/*15:0*/ __VdlyVal__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__last_r__v3;
    __VdlyVal__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__last_r__v3 = 0;
    SData/*15:0*/ __VdlyVal__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__min_r__v3;
    __VdlyVal__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__min_r__v3 = 0;
    SData/*15:0*/ __VdlyVal__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__max_r__v3;
    __VdlyVal__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__max_r__v3 = 0;
    SData/*15:0*/ __VdlyVal__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__last_r__v4;
    __VdlyVal__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__last_r__v4 = 0;
    SData/*15:0*/ __VdlyVal__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__min_r__v4;
    __VdlyVal__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__min_r__v4 = 0;
    SData/*15:0*/ __VdlyVal__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__max_r__v4;
    __VdlyVal__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__max_r__v4 = 0;
    SData/*15:0*/ __VdlyVal__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__last_r__v5;
    __VdlyVal__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__last_r__v5 = 0;
    SData/*15:0*/ __VdlyVal__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__min_r__v5;
    __VdlyVal__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__min_r__v5 = 0;
    SData/*15:0*/ __VdlyVal__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__max_r__v5;
    __VdlyVal__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__max_r__v5 = 0;
    SData/*15:0*/ __VdlyVal__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__last_r__v3;
    __VdlyVal__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__last_r__v3 = 0;
    SData/*15:0*/ __VdlyVal__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__min_r__v3;
    __VdlyVal__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__min_r__v3 = 0;
    SData/*15:0*/ __VdlyVal__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__max_r__v3;
    __VdlyVal__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__max_r__v3 = 0;
    SData/*15:0*/ __VdlyVal__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__last_r__v4;
    __VdlyVal__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__last_r__v4 = 0;
    SData/*15:0*/ __VdlyVal__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__min_r__v4;
    __VdlyVal__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__min_r__v4 = 0;
    SData/*15:0*/ __VdlyVal__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__max_r__v4;
    __VdlyVal__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__max_r__v4 = 0;
    SData/*15:0*/ __VdlyVal__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__last_r__v5;
    __VdlyVal__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__last_r__v5 = 0;
    SData/*15:0*/ __VdlyVal__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__min_r__v5;
    __VdlyVal__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__min_r__v5 = 0;
    SData/*15:0*/ __VdlyVal__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__max_r__v5;
    __VdlyVal__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__max_r__v5 = 0;
    IData/*31:0*/ __VdlyVal__milan_datapath__DOT__csr__DOT__snap_shadow_r__v0;
    __VdlyVal__milan_datapath__DOT__csr__DOT__snap_shadow_r__v0 = 0;
    IData/*31:0*/ __VdlyVal__milan_datapath__DOT__csr__DOT__snap_shadow_r__v1;
    __VdlyVal__milan_datapath__DOT__csr__DOT__snap_shadow_r__v1 = 0;
    IData/*31:0*/ __VdlyVal__milan_datapath__DOT__csr__DOT__snap_shadow_r__v2;
    __VdlyVal__milan_datapath__DOT__csr__DOT__snap_shadow_r__v2 = 0;
    IData/*31:0*/ __VdlyVal__milan_datapath__DOT__csr__DOT__snap_shadow_r__v3;
    __VdlyVal__milan_datapath__DOT__csr__DOT__snap_shadow_r__v3 = 0;
    IData/*31:0*/ __VdlyVal__milan_datapath__DOT__csr__DOT__snap_shadow_r__v4;
    __VdlyVal__milan_datapath__DOT__csr__DOT__snap_shadow_r__v4 = 0;
    CData/*3:0*/ __VdlyDim0__milan_datapath__DOT__csr__DOT__snap_shadow_r__v4;
    __VdlyDim0__milan_datapath__DOT__csr__DOT__snap_shadow_r__v4 = 0;
    IData/*31:0*/ __VdlyVal__milan_datapath__DOT__csr__DOT__snap_shadow_r__v5;
    __VdlyVal__milan_datapath__DOT__csr__DOT__snap_shadow_r__v5 = 0;
    IData/*31:0*/ __VdlyVal__milan_datapath__DOT__csr__DOT__snap_shadow_r__v16;
    __VdlyVal__milan_datapath__DOT__csr__DOT__snap_shadow_r__v16 = 0;
    IData/*31:0*/ __VdlyVal__milan_datapath__DOT__csr__DOT__snap_shadow_r__v17;
    __VdlyVal__milan_datapath__DOT__csr__DOT__snap_shadow_r__v17 = 0;
    IData/*31:0*/ __VdlyVal__milan_datapath__DOT__csr__DOT__snap_shadow_r__v18;
    __VdlyVal__milan_datapath__DOT__csr__DOT__snap_shadow_r__v18 = 0;
    IData/*31:0*/ __VdlyVal__milan_datapath__DOT__csr__DOT__snap_shadow_r__v19;
    __VdlyVal__milan_datapath__DOT__csr__DOT__snap_shadow_r__v19 = 0;
    IData/*31:0*/ __VdlyVal__milan_datapath__DOT__csr__DOT__snap_shadow_r__v20;
    __VdlyVal__milan_datapath__DOT__csr__DOT__snap_shadow_r__v20 = 0;
    IData/*31:0*/ __VdlyVal__milan_datapath__DOT__csr__DOT__snap_shadow_r__v21;
    __VdlyVal__milan_datapath__DOT__csr__DOT__snap_shadow_r__v21 = 0;
    IData/*31:0*/ __VdlyVal__milan_datapath__DOT__csr__DOT__snap_shadow_r__v22;
    __VdlyVal__milan_datapath__DOT__csr__DOT__snap_shadow_r__v22 = 0;
    IData/*31:0*/ __VdlyVal__milan_datapath__DOT__csr__DOT__snap_shadow_r__v23;
    __VdlyVal__milan_datapath__DOT__csr__DOT__snap_shadow_r__v23 = 0;
    IData/*31:0*/ __VdlyVal__milan_datapath__DOT__csr__DOT__snap_shadow_r__v24;
    __VdlyVal__milan_datapath__DOT__csr__DOT__snap_shadow_r__v24 = 0;
    IData/*31:0*/ __VdlyVal__milan_datapath__DOT__csr__DOT__snap_shadow_r__v25;
    __VdlyVal__milan_datapath__DOT__csr__DOT__snap_shadow_r__v25 = 0;
    IData/*31:0*/ __VdlyVal__milan_datapath__DOT__csr__DOT__snap_shadow_r__v26;
    __VdlyVal__milan_datapath__DOT__csr__DOT__snap_shadow_r__v26 = 0;
    IData/*31:0*/ __VdlyVal__milan_datapath__DOT__csr__DOT__snap_shadow_r__v27;
    __VdlyVal__milan_datapath__DOT__csr__DOT__snap_shadow_r__v27 = 0;
    IData/*31:0*/ __VdlyVal__milan_datapath__DOT__csr__DOT__snap_shadow_r__v28;
    __VdlyVal__milan_datapath__DOT__csr__DOT__snap_shadow_r__v28 = 0;
    // Body
    if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__trc_rd_en_w) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_trace__DOT__rd_lane_r 
            = (3U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__hb_addr_r);
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_trace__DOT__rd_word_r[0U] 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_trace__DOT__mem_r
            [(0x000000ffU & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__hb_addr_r 
                             >> 2U))][0U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_trace__DOT__rd_word_r[1U] 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_trace__DOT__mem_r
            [(0x000000ffU & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__hb_addr_r 
                             >> 2U))][1U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_trace__DOT__rd_word_r[2U] 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_trace__DOT__mem_r
            [(0x000000ffU & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__hb_addr_r 
                             >> 2U))][2U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_trace__DOT__rd_word_r[3U] 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_trace__DOT__mem_r
            [(0x000000ffU & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__hb_addr_r 
                             >> 2U))][3U];
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__sp_img_rvalid_r 
        = ((IData)(vlSelfRef.axis_resetn) && (IData)(
                                                     ((0U 
                                                       == 
                                                       (0x000f0000U 
                                                        & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__hb_addr_r)) 
                                                      & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_35))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__sp_dbg_rvalid_r 
        = ((IData)(vlSelfRef.axis_resetn) && (IData)(
                                                     ((0x00010000U 
                                                       == 
                                                       (0x000f0000U 
                                                        & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__hb_addr_r)) 
                                                      & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_35))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__sp_snap_rvalid_r 
        = ((IData)(vlSelfRef.axis_resetn) && (IData)(
                                                     ((0x00020000U 
                                                       == 
                                                       (0x000f0000U 
                                                        & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__hb_addr_r)) 
                                                      & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_35))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__pend_r 
        = ((IData)(vlSelfRef.axis_resetn) && ((IData)(vlSelfRef.milan_datapath__DOT__pp_aecp_dyn_dirty_w) 
                                              | ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__aecp_mark_pend_r) 
                                                 | (0U 
                                                    != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__dirty_r)))));
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__h0e_r__v0) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__h0e_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__render_setpoint__DOT__h0e_r__v0] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__render_setpoint__DOT__h0e_r__v0;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__h0o_r__v0) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__h0o_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__render_setpoint__DOT__h0o_r__v0] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__render_setpoint__DOT__h0o_r__v0;
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__us_cnt_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__us_cnt_r;
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__cnt_r__v0) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__cnt_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__cnt_r__v0] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__cnt_r__v0;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__cnt_r__v1) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__cnt_r[0U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__cnt_r[1U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__cnt_r[2U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__cnt_r[3U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__cnt_r[4U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__cnt_r[5U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__cnt_r[6U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__cnt_r[7U] = 0U;
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_maap_q__DOT__cnt_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_maap_q__DOT__cnt_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_maap_q__DOT__out_valid_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_maap_q__DOT__out_valid_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__alive_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__alive_r;
    vlSelfRef.milan_datapath__DOT__link_guard__DOT__act_sync_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__link_guard__DOT__act_sync_r;
    vlSelfRef.milan_datapath__DOT__link_guard__DOT__act_age_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__link_guard__DOT__act_age_r;
    vlSelfRef.milan_datapath__DOT__ptp_clock_validity__DOT__ival_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__ptp_clock_validity__DOT__ival_r;
    vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__skid_cnt_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__chan_map_capture__DOT__skid_cnt_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__deb_open_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__deb_open_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__deb_cnt_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__deb_cnt_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__maap_stale_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__maap_stale_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__hold_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__hold_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__cap_hold_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__cap_hold_r;
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__aaf_packetizer__DOT__chans_r__v0) {
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__chans_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__aaf_packetizer__DOT__chans_r__v0] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__aaf_packetizer__DOT__chans_r__v0;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__aaf_packetizer__DOT__chans_r__v1) {
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__chans_r[0U] = 2U;
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__chans_r[1U] = 2U;
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__chans_r[2U] = 2U;
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__chans_r[3U] = 2U;
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__chans_r[4U] = 2U;
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__chans_r[5U] = 2U;
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__chans_r[6U] = 2U;
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__chans_r[7U] = 2U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__skid_strm_r__v0) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__skid_strm_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__chan_map_capture__DOT__skid_strm_r__v0] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__chan_map_capture__DOT__skid_strm_r__v0;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__skid_strm_r__v1) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__skid_strm_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__chan_map_capture__DOT__skid_strm_r__v1] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__chan_map_capture__DOT__skid_strm_r__v1;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__rate_r__v0) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__rate_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__rate_r__v0] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__rate_r__v0;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__rate_r__v1) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__rate_r[0U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__clksrc_r__v0) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__clksrc_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__clksrc_r__v0] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__clksrc_r__v0;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__clksrc_r__v1) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__clksrc_r[0U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__ident_r__v0) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__ident_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__ident_r__v0] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__ident_r__v0;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__ident_r__v1) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__ident_r[0U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__ptoff_r__v0) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__ptoff_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__ptoff_r__v0] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__ptoff_r__v0;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__ptoff_r__v1) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__ptoff_r[0U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__ptoff_r[1U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__ptoff_r[2U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__ptoff_r[3U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__ptoff_r[4U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__ptoff_r[5U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__ptoff_r[6U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__ptoff_r[7U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__ptoff_r[8U] = 0U;
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__cap_valid_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__cap_valid_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__cap_open_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__cap_open_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__commit_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__commit_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__ms_div_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__ms_div_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__commit_busy_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__commit_busy_r;
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__fmtout_r__v0) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__fmtout_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__fmtout_r__v0] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__fmtout_r__v0;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__fmtout_r__v1) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__fmtout_r[0U] = 0ULL;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__fmtout_r[1U] = 0ULL;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__fmtout_r[2U] = 0ULL;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__fmtout_r[3U] = 0ULL;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__fmtout_r[4U] = 0ULL;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__fmtout_r[5U] = 0ULL;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__fmtout_r[6U] = 0ULL;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__fmtout_r[7U] = 0ULL;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__fmtout_r[8U] = 0ULL;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__q_wr_r__v0) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_wr_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__chan_map_capture__DOT__q_wr_r__v0] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__chan_map_capture__DOT__q_wr_r__v0;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__q_wr_r__v1) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_wr_r[0U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__q_wr_r__v2) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_wr_r[1U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__q_wr_r__v3) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_wr_r[2U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__q_wr_r__v4) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_wr_r[3U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__q_wr_r__v5) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_wr_r[4U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__q_wr_r__v6) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_wr_r[5U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__q_wr_r__v7) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_wr_r[6U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__q_wr_r__v8) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_wr_r[7U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__q_wr_r__v9) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_wr_r[8U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__q_wr_r__v10) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_wr_r[9U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__q_wr_r__v11) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_wr_r[10U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__q_wr_r__v12) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_wr_r[11U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__q_wr_r__v13) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_wr_r[12U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__q_wr_r__v14) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_wr_r[13U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__q_wr_r__v15) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_wr_r[14U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__q_wr_r__v16) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_wr_r[15U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__q_wr_r__v17) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_wr_r[16U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__q_wr_r__v18) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_wr_r[17U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__q_wr_r__v19) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_wr_r[18U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__q_wr_r__v20) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_wr_r[19U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__q_wr_r__v21) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_wr_r[20U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__q_wr_r__v22) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_wr_r[21U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__q_wr_r__v23) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_wr_r[22U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__q_wr_r__v24) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_wr_r[23U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__q_wr_r__v25) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_wr_r[24U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__q_wr_r__v26) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_wr_r[25U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__q_wr_r__v27) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_wr_r[26U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__q_wr_r__v28) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_wr_r[27U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__q_wr_r__v29) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_wr_r[28U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__q_wr_r__v30) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_wr_r[29U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__q_wr_r__v31) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_wr_r[30U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__q_wr_r__v32) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_wr_r[31U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__q_wr_r__v33) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_wr_r[0U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_wr_r[1U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_wr_r[2U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_wr_r[3U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_wr_r[4U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_wr_r[5U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_wr_r[6U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_wr_r[7U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_wr_r[8U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_wr_r[9U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_wr_r[10U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_wr_r[11U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_wr_r[12U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_wr_r[13U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_wr_r[14U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_wr_r[15U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_wr_r[16U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_wr_r[17U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_wr_r[18U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_wr_r[19U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_wr_r[20U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_wr_r[21U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_wr_r[22U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_wr_r[23U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_wr_r[24U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_wr_r[25U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_wr_r[26U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_wr_r[27U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_wr_r[28U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_wr_r[29U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_wr_r[30U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_wr_r[31U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__key_r__v0) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__key_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__key_r__v0] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__key_r__v0;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__key_r__v1) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__key_r[0U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__key_r[1U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__key_r[2U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__key_r[3U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__key_r[4U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__key_r[5U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__key_r[6U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__key_r[7U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__fmtin_r__v0) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__fmtin_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__fmtin_r__v0] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__fmtin_r__v0;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__fmtin_r__v1) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__fmtin_r[0U] = 0ULL;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__fmtin_r[1U] = 0ULL;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__fmtin_r[2U] = 0ULL;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__fmtin_r[3U] = 0ULL;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__fmtin_r[4U] = 0ULL;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__fmtin_r[5U] = 0ULL;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__fmtin_r[6U] = 0ULL;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__fmtin_r[7U] = 0ULL;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__fmtin_r[8U] = 0ULL;
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__ctl_fifo__DOT__rd_ptr_reg 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__ctl_fifo__DOT__rd_ptr_reg;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__ctl_fifo__DOT__wr_ptr_reg 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__ctl_fifo__DOT__wr_ptr_reg;
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__ctl_fifo__DOT__mem__v0) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__ctl_fifo__DOT__mem[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__ctl_fifo__DOT__mem__v0][0U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__ctl_fifo__DOT__mem__v0[0U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__ctl_fifo__DOT__mem[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__ctl_fifo__DOT__mem__v0][1U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__ctl_fifo__DOT__mem__v0[1U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__ctl_fifo__DOT__mem[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__ctl_fifo__DOT__mem__v0][2U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__ctl_fifo__DOT__mem__v0[2U];
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__cls_r__v0) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__cls_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__cls_r__v0] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__cls_r__v0;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__cls_r__v1) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__cls_r[0U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__cls_r[1U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__cls_r[2U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__cls_r[3U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__cls_r[4U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__cls_r[5U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__cls_r[6U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__cls_r[7U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__age_r__v0) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__age_r[0U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__age_r__v1) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__age_r[0U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__age_r__v1;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__age_r__v2) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__age_r[0U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__age_r__v3) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__age_r[1U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__age_r__v4) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__age_r[1U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__age_r__v4;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__age_r__v5) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__age_r[1U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__age_r__v6) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__age_r[2U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__age_r__v7) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__age_r[2U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__age_r__v7;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__age_r__v8) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__age_r[2U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__age_r__v9) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__age_r[3U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__age_r__v10) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__age_r[3U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__age_r__v10;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__age_r__v11) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__age_r[3U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__age_r__v12) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__age_r[4U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__age_r__v13) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__age_r[4U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__age_r__v13;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__age_r__v14) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__age_r[4U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__age_r__v15) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__age_r[5U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__age_r__v16) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__age_r[5U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__age_r__v16;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__age_r__v17) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__age_r[5U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__age_r__v18) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__age_r[6U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__age_r__v19) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__age_r[6U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__age_r__v19;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__age_r__v20) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__age_r[6U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__age_r__v21) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__age_r[7U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__age_r__v22) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__age_r[7U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__age_r__v22;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__age_r__v23) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__age_r[7U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__age_r__v24) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__age_r[0U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__age_r[1U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__age_r[2U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__age_r[3U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__age_r[4U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__age_r[5U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__age_r[6U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__age_r[7U] = 0U;
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_mrp_strip__DOT__wr_tent_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_mrp_strip__DOT__wr_tent_r;
    vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_tvalid_pipe_reg 
        = vlSelfRef.__Vdly__milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_tvalid_pipe_reg;
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__h1_r__v0) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__h1_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__render_setpoint__DOT__h1_r__v0] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__render_setpoint__DOT__h1_r__v0;
    }
    vlSelfRef.milan_datapath__DOT__crf_rx__DOT__iv_frx_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__crf_rx__DOT__iv_frx_r;
    vlSelfRef.milan_datapath__DOT__ethernet_counters__DOT____Vcellout__event_counter_gen__BRA__8__KET____DOT__counter_inst__count 
        = vlSelfRef.__Vdly__milan_datapath__DOT__ethernet_counters__DOT____Vcellout__event_counter_gen__BRA__8__KET____DOT__counter_inst__count;
    vlSelfRef.milan_datapath__DOT__ethernet_counters__DOT____Vcellout__event_counter_gen__BRA__3__KET____DOT__counter_inst__count 
        = vlSelfRef.__Vdly__milan_datapath__DOT__ethernet_counters__DOT____Vcellout__event_counter_gen__BRA__3__KET____DOT__counter_inst__count;
    vlSelfRef.milan_datapath__DOT__ethernet_counters__DOT____Vcellout__event_counter_gen__BRA__7__KET____DOT__counter_inst__count 
        = vlSelfRef.__Vdly__milan_datapath__DOT__ethernet_counters__DOT____Vcellout__event_counter_gen__BRA__7__KET____DOT__counter_inst__count;
    vlSelfRef.milan_datapath__DOT__ethernet_counters__DOT____Vcellout__event_counter_gen__BRA__6__KET____DOT__counter_inst__count 
        = vlSelfRef.__Vdly__milan_datapath__DOT__ethernet_counters__DOT____Vcellout__event_counter_gen__BRA__6__KET____DOT__counter_inst__count;
    vlSelfRef.milan_datapath__DOT__ethernet_counters__DOT____Vcellout__event_counter_gen__BRA__5__KET____DOT__counter_inst__count 
        = vlSelfRef.__Vdly__milan_datapath__DOT__ethernet_counters__DOT____Vcellout__event_counter_gen__BRA__5__KET____DOT__counter_inst__count;
    vlSelfRef.milan_datapath__DOT__ethernet_counters__DOT____Vcellout__event_counter_gen__BRA__4__KET____DOT__counter_inst__count 
        = vlSelfRef.__Vdly__milan_datapath__DOT__ethernet_counters__DOT____Vcellout__event_counter_gen__BRA__4__KET____DOT__counter_inst__count;
    vlSelfRef.milan_datapath__DOT__ethernet_counters__DOT____Vcellout__event_counter_gen__BRA__2__KET____DOT__counter_inst__count 
        = vlSelfRef.__Vdly__milan_datapath__DOT__ethernet_counters__DOT____Vcellout__event_counter_gen__BRA__2__KET____DOT__counter_inst__count;
    vlSelfRef.milan_datapath__DOT__ethernet_counters__DOT____Vcellout__event_counter_gen__BRA__1__KET____DOT__counter_inst__count 
        = vlSelfRef.__Vdly__milan_datapath__DOT__ethernet_counters__DOT____Vcellout__event_counter_gen__BRA__1__KET____DOT__counter_inst__count;
    vlSelfRef.milan_datapath__DOT__ethernet_counters__DOT____Vcellout__event_counter_gen__BRA__0__KET____DOT__counter_inst__count 
        = vlSelfRef.__Vdly__milan_datapath__DOT__ethernet_counters__DOT____Vcellout__event_counter_gen__BRA__0__KET____DOT__counter_inst__count;
    vlSelfRef.milan_datapath__DOT__i2spb_overruns = vlSelfRef.__Vdly__milan_datapath__DOT__i2spb_overruns;
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__cmdq_class_r__v0) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__cmdq_arg0_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__cmdq_arg0_r__v0] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__cmdq_arg0_r__v0;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__cmdq_arg1_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__cmdq_arg1_r__v0] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__cmdq_arg1_r__v0;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__cmdq_class_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__cmdq_class_r__v0] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__cmdq_class_r__v0;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__cmdq_type_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__cmdq_type_r__v0] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__cmdq_type_r__v0;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__cmdq_index_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__cmdq_index_r__v0] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__cmdq_index_r__v0;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__seq_r__v0) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__seq_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__seq_r__v0] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__seq_r__v0;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r__v0) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r__v0] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r__v0;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r__v1) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r__v1] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r__v1;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r__v2) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r[0U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r__v3) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r[1U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r__v4) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r[2U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r__v5) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r[3U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r__v6) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r[4U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r__v7) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r[5U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r__v8) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r[6U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r__v9) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r[7U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r__v10) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r[8U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r__v11) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r[9U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r__v12) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r[10U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r__v13) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r[11U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r__v14) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r[12U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r__v15) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r[13U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r__v16) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r[14U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r__v17) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r[15U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r__v18) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r[16U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r__v19) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r[17U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r__v20) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r[18U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r__v21) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r[19U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r__v22) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r[20U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r__v23) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r[21U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r__v24) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r[22U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r__v25) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r[23U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r__v26) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r[24U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r__v27) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r[25U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r__v28) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r[26U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r__v29) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r[27U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r__v30) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r[28U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r__v31) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r[29U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r__v32) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r[30U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r__v33) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r[31U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r__v34) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r[0U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r[1U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r[2U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r[3U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r[4U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r[5U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r[6U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r[7U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r[8U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r[9U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r[10U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r[11U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r[12U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r[13U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r[14U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r[15U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r[16U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r[17U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r[18U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r[19U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r[20U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r[21U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r[22U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r[23U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r[24U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r[25U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r[26U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r[27U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r[28U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r[29U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r[30U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r[31U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__csr__DOT__stat_snap__v0) {
        vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap[0U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__csr__DOT__stat_snap__v0;
        vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap[1U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__csr__DOT__stat_snap__v1;
        vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap[2U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__csr__DOT__stat_snap__v2;
        vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap[3U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__csr__DOT__stat_snap__v3;
        vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap[4U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__csr__DOT__stat_snap__v4;
        vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap[5U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__csr__DOT__stat_snap__v5;
        vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap[6U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__csr__DOT__stat_snap__v6;
        vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap[7U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__csr__DOT__stat_snap__v7;
        vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap[8U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__csr__DOT__stat_snap__v8;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__csr__DOT__stat_snap__v9) {
        vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap[0U] = 0U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap[1U] = 0U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap[2U] = 0U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap[3U] = 0U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap[4U] = 0U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap[5U] = 0U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap[6U] = 0U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap[7U] = 0U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap[8U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__csr__DOT__stat_snap__v18) {
        vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap[0U] = 0U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap[1U] = 0U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap[2U] = 0U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap[3U] = 0U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap[4U] = 0U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap[5U] = 0U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap[6U] = 0U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap[7U] = 0U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__stat_snap[8U] = 0U;
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__fetch_idx_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__fetch_idx_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__out_last_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__out_last_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__run_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__run_r;
    vlSelfRef.milan_datapath__DOT__ptp_clock_validity__DOT__qdiv_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__ptp_clock_validity__DOT__qdiv_r;
    vlSelfRef.milan_datapath__DOT__ptp_clock_validity__DOT__hold_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__ptp_clock_validity__DOT__hold_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_stage_assem_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_stage_assem_r;
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__chans_q_r__v0) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__chans_q_r[0U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__render_setpoint__DOT__chans_q_r__v0;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__chans_q_r__v1) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__chans_q_r[1U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__render_setpoint__DOT__chans_q_r__v1;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__chans_q_r__v2) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__chans_q_r[2U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__render_setpoint__DOT__chans_q_r__v2;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__chans_q_r__v3) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__chans_q_r[3U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__render_setpoint__DOT__chans_q_r__v3;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__chans_q_r__v4) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__chans_q_r[4U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__render_setpoint__DOT__chans_q_r__v4;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__chans_q_r__v5) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__chans_q_r[5U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__render_setpoint__DOT__chans_q_r__v5;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__chans_q_r__v6) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__chans_q_r[6U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__render_setpoint__DOT__chans_q_r__v6;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__chans_q_r__v7) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__chans_q_r[7U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__render_setpoint__DOT__chans_q_r__v7;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__chans_q_r__v8) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__chans_q_r[0U] = 0U;
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__chans_q_r[1U] = 0U;
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__chans_q_r[2U] = 0U;
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__chans_q_r[3U] = 0U;
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__chans_q_r[4U] = 0U;
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__chans_q_r[5U] = 0U;
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__chans_q_r[6U] = 0U;
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__chans_q_r[7U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_action__v0) {
        vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_action[vlSelfRef.__VdlyDim0__milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_action__v0] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_action__v0;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_valid__v0) {
        vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_valid[vlSelfRef.__VdlyDim0__milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_valid__v0] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_valid__v0;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_valid__v1) {
        vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_valid[0U] = 0U;
        vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_valid[1U] = 0U;
        vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_valid[2U] = 0U;
        vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_valid[3U] = 0U;
        vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_valid[4U] = 0U;
        vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_valid[5U] = 0U;
        vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_valid[6U] = 0U;
        vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_valid[7U] = 0U;
        vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_valid[8U] = 0U;
        vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_valid[9U] = 0U;
        vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_valid[10U] = 0U;
        vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_valid[11U] = 0U;
        vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_valid[12U] = 0U;
        vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_valid[13U] = 0U;
        vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_valid[14U] = 0U;
        vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_valid[15U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__aaf_packetizer__DOT__stg_r__v0) {
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__stg_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__aaf_packetizer__DOT__stg_r__v0] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__aaf_packetizer__DOT__stg_r__v0;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r__v0) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r__v0] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r__v0;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r__v1) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r[0U] = 0ULL;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r__v2) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r[1U] = 0ULL;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r__v3) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r[2U] = 0ULL;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r__v4) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r[3U] = 0ULL;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r__v5) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r[4U] = 0ULL;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r__v6) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r[5U] = 0ULL;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r__v7) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r[6U] = 0ULL;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r__v8) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r[7U] = 0ULL;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r__v9) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r[8U] = 0ULL;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r__v10) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r[9U] = 0ULL;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r__v11) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r[10U] = 0ULL;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r__v12) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r[11U] = 0ULL;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r__v13) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r[12U] = 0ULL;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r__v14) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r[13U] = 0ULL;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r__v15) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r[14U] = 0ULL;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r__v16) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r[15U] = 0ULL;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r__v17) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r[16U] = 0ULL;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r__v18) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r[17U] = 0ULL;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r__v19) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r[18U] = 0ULL;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r__v20) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r[19U] = 0ULL;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r__v21) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r[20U] = 0ULL;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r__v22) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r[21U] = 0ULL;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r__v23) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r[22U] = 0ULL;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r__v24) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r[23U] = 0ULL;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r__v25) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r[24U] = 0ULL;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r__v26) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r[25U] = 0ULL;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r__v27) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r[26U] = 0ULL;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r__v28) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r[27U] = 0ULL;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r__v29) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r[28U] = 0ULL;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r__v30) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r[29U] = 0ULL;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r__v31) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r[30U] = 0ULL;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r__v32) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r[31U] = 0ULL;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r__v33) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r[0U] = 0ULL;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r[1U] = 0ULL;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r[2U] = 0ULL;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r[3U] = 0ULL;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r[4U] = 0ULL;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r[5U] = 0ULL;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r[6U] = 0ULL;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r[7U] = 0ULL;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r[8U] = 0ULL;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r[9U] = 0ULL;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r[10U] = 0ULL;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r[11U] = 0ULL;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r[12U] = 0ULL;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r[13U] = 0ULL;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r[14U] = 0ULL;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r[15U] = 0ULL;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r[16U] = 0ULL;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r[17U] = 0ULL;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r[18U] = 0ULL;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r[19U] = 0ULL;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r[20U] = 0ULL;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r[21U] = 0ULL;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r[22U] = 0ULL;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r[23U] = 0ULL;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r[24U] = 0ULL;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r[25U] = 0ULL;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r[26U] = 0ULL;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r[27U] = 0ULL;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r[28U] = 0ULL;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r[29U] = 0ULL;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r[30U] = 0ULL;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r[31U] = 0ULL;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_mask__v0) {
        vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_mask[vlSelfRef.__VdlyDim0__milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_mask__v0] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_mask__v0;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_key__v0) {
        vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_key[vlSelfRef.__VdlyDim0__milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_key__v0] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_key__v0;
    }
    vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__skid_wp_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__chan_map_capture__DOT__skid_wp_r;
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__skid_data_r__v0) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__skid_data_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__chan_map_capture__DOT__skid_data_r__v0] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__chan_map_capture__DOT__skid_data_r__v0;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__skid_data_r__v1) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__skid_data_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__chan_map_capture__DOT__skid_data_r__v1] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__chan_map_capture__DOT__skid_data_r__v1;
    }
    vlSelfRef.milan_datapath__DOT__media_clock_restart__DOT__tgt_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__media_clock_restart__DOT__tgt_r;
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__media_clock_restart__DOT__hold_r__v0) {
        vlSelfRef.milan_datapath__DOT__media_clock_restart__DOT__hold_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__media_clock_restart__DOT__hold_r__v0] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__media_clock_restart__DOT__hold_r__v0;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__media_clock_restart__DOT__hold_r__v1) {
        vlSelfRef.milan_datapath__DOT__media_clock_restart__DOT__hold_r[0U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__media_clock_restart__DOT__hold_r__v2) {
        vlSelfRef.milan_datapath__DOT__media_clock_restart__DOT__hold_r[0U] = 8U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__media_clock_restart__DOT__hold_r__v3) {
        vlSelfRef.milan_datapath__DOT__media_clock_restart__DOT__hold_r[1U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__media_clock_restart__DOT__hold_r__v4) {
        vlSelfRef.milan_datapath__DOT__media_clock_restart__DOT__hold_r[1U] = 8U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__media_clock_restart__DOT__hold_r__v5) {
        vlSelfRef.milan_datapath__DOT__media_clock_restart__DOT__hold_r[2U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__media_clock_restart__DOT__hold_r__v6) {
        vlSelfRef.milan_datapath__DOT__media_clock_restart__DOT__hold_r[2U] = 8U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__media_clock_restart__DOT__hold_r__v7) {
        vlSelfRef.milan_datapath__DOT__media_clock_restart__DOT__hold_r[3U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__media_clock_restart__DOT__hold_r__v8) {
        vlSelfRef.milan_datapath__DOT__media_clock_restart__DOT__hold_r[3U] = 8U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__media_clock_restart__DOT__hold_r__v9) {
        vlSelfRef.milan_datapath__DOT__media_clock_restart__DOT__hold_r[4U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__media_clock_restart__DOT__hold_r__v10) {
        vlSelfRef.milan_datapath__DOT__media_clock_restart__DOT__hold_r[4U] = 8U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__media_clock_restart__DOT__hold_r__v11) {
        vlSelfRef.milan_datapath__DOT__media_clock_restart__DOT__hold_r[5U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__media_clock_restart__DOT__hold_r__v12) {
        vlSelfRef.milan_datapath__DOT__media_clock_restart__DOT__hold_r[5U] = 8U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__media_clock_restart__DOT__hold_r__v13) {
        vlSelfRef.milan_datapath__DOT__media_clock_restart__DOT__hold_r[6U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__media_clock_restart__DOT__hold_r__v14) {
        vlSelfRef.milan_datapath__DOT__media_clock_restart__DOT__hold_r[6U] = 8U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__media_clock_restart__DOT__hold_r__v15) {
        vlSelfRef.milan_datapath__DOT__media_clock_restart__DOT__hold_r[7U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__media_clock_restart__DOT__hold_r__v16) {
        vlSelfRef.milan_datapath__DOT__media_clock_restart__DOT__hold_r[7U] = 8U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__media_clock_restart__DOT__hold_r__v17) {
        vlSelfRef.milan_datapath__DOT__media_clock_restart__DOT__hold_r[8U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__media_clock_restart__DOT__hold_r__v18) {
        vlSelfRef.milan_datapath__DOT__media_clock_restart__DOT__hold_r[8U] = 8U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__media_clock_restart__DOT__hold_r__v19) {
        vlSelfRef.milan_datapath__DOT__media_clock_restart__DOT__hold_r[0U] = 8U;
        vlSelfRef.milan_datapath__DOT__media_clock_restart__DOT__hold_r[1U] = 8U;
        vlSelfRef.milan_datapath__DOT__media_clock_restart__DOT__hold_r[2U] = 8U;
        vlSelfRef.milan_datapath__DOT__media_clock_restart__DOT__hold_r[3U] = 8U;
        vlSelfRef.milan_datapath__DOT__media_clock_restart__DOT__hold_r[4U] = 8U;
        vlSelfRef.milan_datapath__DOT__media_clock_restart__DOT__hold_r[5U] = 8U;
        vlSelfRef.milan_datapath__DOT__media_clock_restart__DOT__hold_r[6U] = 8U;
        vlSelfRef.milan_datapath__DOT__media_clock_restart__DOT__hold_r[7U] = 8U;
        vlSelfRef.milan_datapath__DOT__media_clock_restart__DOT__hold_r[8U] = 8U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__mapo_pref_r__v0) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__mapo_pref_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__mapo_pref_r__v0] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__mapo_pref_r__v0;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__mapi_pref_r__v0) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__mapi_pref_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__mapi_pref_r__v0] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__mapi_pref_r__v0;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__mapo_len_r__v0) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__mapo_len_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__mapo_len_r__v0] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__mapo_len_r__v0;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__mapi_len_r__v0) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__mapi_len_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__mapi_len_r__v0] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__mapi_len_r__v0;
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__held_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__held_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__release_pend_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__release_pend_r;
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__len_r__v0) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__len_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__len_r__v0] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__len_r__v0;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__len_r__v1) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__len_r[0U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__len_r[1U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__len_r[2U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__len_r[3U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__len_r[4U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__len_r[5U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__len_r[6U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__len_r[7U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__st_r__v0) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__st_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__st_r__v0] = 1U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__st_r__v1) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__st_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__st_r__v1] = 2U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__st_r__v2) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__st_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__st_r__v2] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__st_r__v3) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__st_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__st_r__v3] = 3U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__st_r__v4) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__st_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__st_r__v4] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__st_r__v5) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__st_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__st_r__v5] = 2U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__st_r__v6) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__st_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__st_r__v6] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__st_r__v7) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__st_r[0U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__st_r__v8) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__st_r[1U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__st_r[2U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__st_r[3U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__st_r[4U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__st_r[5U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__st_r[6U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__st_r[7U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__key_r__v0) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__key_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__key_r__v0][0U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__key_r__v0[0U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__key_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__key_r__v0][1U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__key_r__v0[1U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__key_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__key_r__v0][2U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__key_r__v0[2U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__key_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__key_r__v0][3U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__key_r__v0[3U];
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_r;
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_render__DOT__cur_r__v0) {
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__cur_r[vlSelfRef.__VdlyDim1__milan_datapath__DOT__chan_map_render__DOT__cur_r__v0][vlSelfRef.__VdlyDim0__milan_datapath__DOT__chan_map_render__DOT__cur_r__v0] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__cur_r__v0;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_render__DOT__cur_r__v1) {
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__cur_r[vlSelfRef.__VdlyDim1__milan_datapath__DOT__chan_map_render__DOT__cur_r__v1][vlSelfRef.__VdlyDim0__milan_datapath__DOT__chan_map_render__DOT__cur_r__v1] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__cur_r__v1;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_render__DOT__cur_r__v2) {
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__cur_r[0U][0U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__cur_r[0U][1U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__cur_r[0U][2U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__cur_r[0U][3U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__cur_r[0U][4U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__cur_r[0U][5U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__cur_r[0U][6U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__cur_r[0U][7U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__cur_r[1U][0U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__cur_r[1U][1U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__cur_r[1U][2U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__cur_r[1U][3U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__cur_r[1U][4U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__cur_r[1U][5U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__cur_r[1U][6U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__cur_r[1U][7U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__cur_r[2U][0U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__cur_r[2U][1U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__cur_r[2U][2U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__cur_r[2U][3U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__cur_r[2U][4U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__cur_r[2U][5U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__cur_r[2U][6U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__cur_r[2U][7U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__cur_r[3U][0U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__cur_r[3U][1U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__cur_r[3U][2U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__cur_r[3U][3U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__cur_r[3U][4U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__cur_r[3U][5U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__cur_r[3U][6U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__cur_r[3U][7U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__cur_r[4U][0U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__cur_r[4U][1U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__cur_r[4U][2U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__cur_r[4U][3U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__cur_r[4U][4U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__cur_r[4U][5U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__cur_r[4U][6U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__cur_r[4U][7U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__cur_r[5U][0U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__cur_r[5U][1U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__cur_r[5U][2U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__cur_r[5U][3U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__cur_r[5U][4U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__cur_r[5U][5U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__cur_r[5U][6U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__cur_r[5U][7U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__cur_r[6U][0U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__cur_r[6U][1U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__cur_r[6U][2U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__cur_r[6U][3U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__cur_r[6U][4U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__cur_r[6U][5U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__cur_r[6U][6U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__cur_r[6U][7U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__cur_r[7U][0U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__cur_r[7U][1U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__cur_r[7U][2U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__cur_r[7U][3U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__cur_r[7U][4U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__cur_r[7U][5U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__cur_r[7U][6U] = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__cur_r[7U][7U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__tdm_hold_r__v0) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__tdm_hold_r[0U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__chan_map_capture__DOT__tdm_hold_r__v0;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__tdm_hold_r__v1) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__tdm_hold_r[0U] = 0ULL;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__tdm_hold_r[1U] = 0ULL;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__tdm_hold_r[2U] = 0ULL;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__tdm_hold_r[3U] = 0ULL;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pcm_route__DOT__route_r__v0) {
        vlSelfRef.milan_datapath__DOT__pcm_route__DOT__route_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pcm_route__DOT__route_r__v0] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pcm_route__DOT__route_r__v0;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pcm_route__DOT__route_r__v1) {
        vlSelfRef.milan_datapath__DOT__pcm_route__DOT__route_r[0U] = 2U;
        vlSelfRef.milan_datapath__DOT__pcm_route__DOT__route_r[1U] = 0U;
        vlSelfRef.milan_datapath__DOT__pcm_route__DOT__route_r[2U] = 0U;
        vlSelfRef.milan_datapath__DOT__pcm_route__DOT__route_r[3U] = 0U;
        vlSelfRef.milan_datapath__DOT__pcm_route__DOT__route_r[4U] = 0U;
        vlSelfRef.milan_datapath__DOT__pcm_route__DOT__route_r[5U] = 0U;
        vlSelfRef.milan_datapath__DOT__pcm_route__DOT__route_r[6U] = 0U;
        vlSelfRef.milan_datapath__DOT__pcm_route__DOT__route_r[7U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__stream_table__DOT__ovr_en_r__v0) {
        vlSelfRef.milan_datapath__DOT__stream_table__DOT__ovr_en_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__stream_table__DOT__ovr_en_r__v0] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__stream_table__DOT__ovr_en_r__v0;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__stream_table__DOT__ovr_en_r__v1) {
        vlSelfRef.milan_datapath__DOT__stream_table__DOT__ovr_en_r[0U] = 0U;
        vlSelfRef.milan_datapath__DOT__stream_table__DOT__ovr_en_r[1U] = 0U;
        vlSelfRef.milan_datapath__DOT__stream_table__DOT__ovr_en_r[2U] = 0U;
        vlSelfRef.milan_datapath__DOT__stream_table__DOT__ovr_en_r[3U] = 0U;
        vlSelfRef.milan_datapath__DOT__stream_table__DOT__ovr_en_r[4U] = 0U;
        vlSelfRef.milan_datapath__DOT__stream_table__DOT__ovr_en_r[5U] = 0U;
        vlSelfRef.milan_datapath__DOT__stream_table__DOT__ovr_en_r[6U] = 0U;
        vlSelfRef.milan_datapath__DOT__stream_table__DOT__ovr_en_r[7U] = 0U;
    }
    vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__ms_div_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__render_setpoint__DOT__ms_div_r;
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__wptr_r__v0) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__wptr_r[0U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__render_setpoint__DOT__wptr_r__v0;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__wptr_r__v1) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__wptr_r[1U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__render_setpoint__DOT__wptr_r__v1;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__wptr_r__v2) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__wptr_r[2U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__render_setpoint__DOT__wptr_r__v2;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__wptr_r__v3) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__wptr_r[3U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__render_setpoint__DOT__wptr_r__v3;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__wptr_r__v4) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__wptr_r[4U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__render_setpoint__DOT__wptr_r__v4;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__wptr_r__v5) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__wptr_r[5U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__render_setpoint__DOT__wptr_r__v5;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__wptr_r__v6) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__wptr_r[6U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__render_setpoint__DOT__wptr_r__v6;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__wptr_r__v7) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__wptr_r[7U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__render_setpoint__DOT__wptr_r__v7;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__wptr_r__v8) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__wptr_r[0U] = 0U;
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__wptr_r[1U] = 0U;
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__wptr_r[2U] = 0U;
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__wptr_r[3U] = 0U;
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__wptr_r[4U] = 0U;
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__wptr_r[5U] = 0U;
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__wptr_r[6U] = 0U;
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__wptr_r[7U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v1) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__pend_r[0U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__prefill_r__v2) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__pend_r[0U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__pend_r__v2) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__pend_r[0U] = 1U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v3) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__pend_r[0U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v5) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__pend_r[1U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__prefill_r__v7) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__pend_r[1U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__pend_r__v6) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__pend_r[1U] = 1U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v7) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__pend_r[1U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v9) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__pend_r[2U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__prefill_r__v12) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__pend_r[2U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__pend_r__v10) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__pend_r[2U] = 1U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v11) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__pend_r[2U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v13) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__pend_r[3U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__prefill_r__v17) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__pend_r[3U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__pend_r__v14) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__pend_r[3U] = 1U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v15) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__pend_r[3U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v17) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__pend_r[4U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__prefill_r__v22) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__pend_r[4U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__pend_r__v18) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__pend_r[4U] = 1U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v19) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__pend_r[4U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v21) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__pend_r[5U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__prefill_r__v27) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__pend_r[5U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__pend_r__v22) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__pend_r[5U] = 1U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v23) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__pend_r[5U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v25) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__pend_r[6U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__prefill_r__v32) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__pend_r[6U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__pend_r__v26) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__pend_r[6U] = 1U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v27) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__pend_r[6U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v29) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__pend_r[7U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__prefill_r__v37) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__pend_r[7U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__pend_r__v30) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__pend_r[7U] = 1U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__prefill_r__v0) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__converged_r[0U] = 0U;
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__dev_ok_r[0U] = 0U;
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__conv_ms_r[0U] = 0U;
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__prefill_r[0U] = 1U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__converged_r__v1) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__converged_r[0U] = 1U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__prefill_r__v2) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__converged_r[0U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v2) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__converged_r[0U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__prefill_r__v3) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__converged_r[0U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v3) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__converged_r[0U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__prefill_r__v5) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__converged_r[1U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__converged_r__v7) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__converged_r[1U] = 1U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__prefill_r__v7) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__converged_r[1U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v6) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__converged_r[1U] = 0U;
    }
    if (vlSelfRef.axis_resetn) {
        if (vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ext_wr_ok_w) {
            if ((0U == (0x0000001fU & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__lctx_wr_addr_r)))) {
                vlSelfRef.milan_datapath__DOT__wing_stg_vld_r = 1U;
                vlSelfRef.milan_datapath__DOT__wing_stg_idx_r 
                    = (7U & ((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__lctx_wr_addr_r) 
                             >> 5U));
            } else if ((1U == (0x0000001fU & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__lctx_wr_addr_r)))) {
                vlSelfRef.milan_datapath__DOT__wing_stg_vld_r = 1U;
                vlSelfRef.milan_datapath__DOT__wing_stg_idx_r 
                    = (7U & ((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__lctx_wr_addr_r) 
                             >> 5U));
            } else if ((4U == (0x0000001fU & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__lctx_wr_addr_r)))) {
                vlSelfRef.milan_datapath__DOT__wing_stg_vld_r = 0U;
            }
        }
        if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_resp_valid_w) {
            if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_pend_r) {
                if ((0xffffU != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_drop_r))) {
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_drop_r 
                        = (0x0000ffffU & ((IData)(1U) 
                                          + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_drop_r)));
                }
            } else {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_pend_r = 1U;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_msg_r 
                    = (0x0000000fU & ((1U | ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__txn_r[11U] 
                                              << 2U) 
                                             | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__txn_r[10U] 
                                                >> 0x0000001eU))) 
                                      & (- (IData)((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_117)))));
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_status_r 
                    = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_resp_status_w;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_sid_r 
                    = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_resp_sid_w;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_ctlr_r 
                    = ((((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__txn_r[8U])) 
                         << 0x00000022U) | (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__txn_r[7U])) 
                                             << 2U) 
                                            | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__txn_r[6U])) 
                                               >> 0x0000001eU))) 
                       & (- (QData)((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_117))));
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_tkeid_r 
                    = (vlSelfRef.milan_datapath__DOT__cfg_adp_entity_id 
                       & (- (QData)((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_117))));
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_lseid_r 
                    = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_resp_lseid_w;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_tkuid_r 
                    = (0x0000ffffU & (((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__txn_r[2U] 
                                        << 4U) | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__txn_r[1U] 
                                                  >> 0x0000001cU)) 
                                      & (- (IData)((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_117)))));
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_lsuid_r 
                    = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_resp_lsuid_w;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_cc_r = 0U;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_seq_r 
                    = (0x0000ffffU & (((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__txn_r[4U] 
                                        << 0x00000012U) 
                                       | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__txn_r[4U] 
                                          >> 0x0000000eU)) 
                                      & (- (IData)((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_117)))));
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_flags_r 
                    = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_resp_flags_w;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_vlan_r 
                    = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_resp_vlan_w;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_da_r 
                    = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_resp_da_w;
            }
        }
        if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_st_r))) {
            if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_st_r))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_st_r = 0U;
            } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_st_r))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_st_r = 0U;
            } else if ((0x00000020U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__gnt_r))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_lane_valid_r = 0U;
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_pend_r = 0U;
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_st_r = 0U;
            }
        } else if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_st_r))) {
            if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_st_r))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_st_r = 4U;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_lane_valid_r = 1U;
            } else if ((0x37U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_bidx_r))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_st_r = 3U;
            } else {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_bidx_r 
                    = (0x0000003fU & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_bidx_r)));
            }
        } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_st_r))) {
            if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__txc_locked_r) 
                 & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__alloc_gnt_r) 
                    & (3U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__txc_owner_r))))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_slot_r 
                    = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__alloc_slot_r;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_bidx_r = 0U;
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_st_r = 2U;
            }
        } else if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_pend_r) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_st_r = 1U;
        }
        if ((8U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__aidx_r))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__grant_r 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__wgrant_now_w;
        }
        if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__acmp_sb_accept_w) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__acmp_sb_slot_r 
                = (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_acmp_q__DOT__out_data_r[1U] 
                         >> 0x00000019U));
        }
        if (vlSelfRef.milan_datapath__DOT__chmap_phys_v_w) {
            vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__pos_r = 0U;
            if ((0U == (IData)(vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__p1_w))) {
                vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__lhold_r 
                    = (0x00ffffffU & ((vlSelfRef.milan_datapath__DOT__chmap_phys_w[1U] 
                                       << 8U) | (vlSelfRef.milan_datapath__DOT__chmap_phys_w[0U] 
                                                 >> 0x00000018U)));
            }
        }
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__arm_v_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__draw_req_r = 0U;
        if ((8U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__w_st_r))) {
            if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__w_st_r))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__w_st_r = 0U;
            } else if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__w_st_r))) {
                if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__w_st_r))) {
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__arm_v_r = 1U;
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__arm_c_r = 1U;
                    if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__teardown_ph_r) {
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__arm_ann_r = 1U;
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__w_st_r = 0U;
                    } else {
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__arm_ann_r = 0U;
                    }
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__teardown_ph_r = 1U;
                } else {
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__w_st_r = 1U;
                }
            } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__w_st_r))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__w_st_r = 1U;
                if ((1U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__send_msg_r))) {
                    if ((1U != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__pstate_r))) {
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__pstate_r = 1U;
                    }
                    if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__chain_ann_r) {
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__chain_ann_r = 0U;
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__ival_ann_r = 1U;
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__w_st_r = 3U;
                    }
                } else if ((3U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__send_msg_r))) {
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__pstate_r = 2U;
                }
            } else if ((0x00000040U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__gnt_r))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__w_st_r = 9U;
            }
        } else if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__w_st_r))) {
            if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__w_st_r))) {
                if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__w_st_r))) {
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__w_st_r = 8U;
                } else if ((0x3bU == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__bld_idx_r))) {
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__w_st_r = 7U;
                } else {
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__bld_idx_r 
                        = (0x0000003fU & ((IData)(1U) 
                                          + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__bld_idx_r)));
                }
            } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__w_st_r))) {
                if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__txc_locked_r) 
                     & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__alloc_gnt_r) 
                        & (5U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__txc_owner_r))))) {
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__bld_slot_r 
                        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__alloc_slot_r;
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__bld_idx_r = 0U;
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__w_st_r = 6U;
                } else {
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__w_st_r = 4U;
                }
            } else {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__w_st_r = 5U;
            }
        } else if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__w_st_r))) {
            if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__w_st_r))) {
                if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__draw_act_r) {
                    if (((4U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pr_owner_r)) 
                         & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_18))) {
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__draw_act_r = 0U;
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__arm_v_r = 1U;
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__arm_c_r = 0U;
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__arm_ann_r 
                            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__ival_ann_r;
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__arm_dl_r 
                            = (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__now_ms_r 
                               + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__prng_ms_w));
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__w_st_r = 4U;
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__send_msg_r 
                            = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__ival_ann_r)
                                ? 3U : 1U);
                    }
                } else if ((1U & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__adp_prng_busy_w)) 
                                  & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__draw_req_r))))) {
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__draw_req_r = 1U;
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__draw_kind_r 
                        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__ival_ann_r)
                            ? 6U : 5U);
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__draw_act_r = 1U;
                }
            } else {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__w_st_r = 0U;
            }
        } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__w_st_r))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__pstate_r = 0U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__teardown_ph_r = 0U;
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__w_st_r = 0x0bU;
        } else {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__pstate_r = 0U;
        }
        if ((4U & vlSelfRef.milan_datapath__DOT__csr__DOT__link_ctrl)) {
            vlSelfRef.__Vdly__milan_datapath__DOT__link_guard__DOT__state_r = 0U;
            vlSelfRef.milan_datapath__DOT__link_guard__DOT__guard_rst_r = 0U;
            vlSelfRef.milan_datapath__DOT__link_guard__DOT__eth_rst_r = 0U;
            vlSelfRef.__Vdly__milan_datapath__DOT__link_guard__DOT__bounced_r = 0U;
        } else if ((0U == (IData)(vlSelfRef.milan_datapath__DOT__link_guard__DOT__state_r))) {
            vlSelfRef.milan_datapath__DOT__link_guard__DOT__guard_rst_r = 0U;
            vlSelfRef.milan_datapath__DOT__link_guard__DOT__eth_rst_r = 0U;
            if ((1U & ((~ (IData)(vlSelfRef.milan_datapath__DOT__link_guard__DOT__both_alive_w)) 
                       | ((~ (IData)(vlSelfRef.milan_datapath__DOT__link_guard__DOT__man_reinit_r)) 
                          & (vlSelfRef.milan_datapath__DOT__csr__DOT__link_ctrl 
                             >> 1U))))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__link_guard__DOT__state_r = 1U;
                vlSelfRef.milan_datapath__DOT__link_guard__DOT__guard_rst_r = 1U;
                vlSelfRef.milan_datapath__DOT__link_guard__DOT__eth_rst_r = 1U;
                if (vlSelfRef.milan_datapath__DOT__link_guard__DOT__both_alive_w) {
                    vlSelfRef.__Vdly__milan_datapath__DOT__link_guard__DOT__bounced_r = 0U;
                } else {
                    vlSelfRef.__Vdly__milan_datapath__DOT__link_guard__DOT__bounce_cnt_r 
                        = (0x0000ffffU & ((0x0000ffffU 
                                           == (IData)(vlSelfRef.milan_datapath__DOT__link_guard__DOT__bounce_cnt_r))
                                           ? (IData)(vlSelfRef.milan_datapath__DOT__link_guard__DOT__bounce_cnt_r)
                                           : ((IData)(1U) 
                                              + (IData)(vlSelfRef.milan_datapath__DOT__link_guard__DOT__bounce_cnt_r))));
                    vlSelfRef.__Vdly__milan_datapath__DOT__link_guard__DOT__bounced_r = 1U;
                }
            }
        } else if ((1U == (IData)(vlSelfRef.milan_datapath__DOT__link_guard__DOT__state_r))) {
            if ((1U & ((~ (IData)(vlSelfRef.milan_datapath__DOT__link_guard__DOT__both_alive_w)) 
                       & (~ (IData)(vlSelfRef.milan_datapath__DOT__link_guard__DOT__bounced_r))))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__link_guard__DOT__bounce_cnt_r 
                    = (0x0000ffffU & ((0x0000ffffU 
                                       == (IData)(vlSelfRef.milan_datapath__DOT__link_guard__DOT__bounce_cnt_r))
                                       ? (IData)(vlSelfRef.milan_datapath__DOT__link_guard__DOT__bounce_cnt_r)
                                       : ((IData)(1U) 
                                          + (IData)(vlSelfRef.milan_datapath__DOT__link_guard__DOT__bounce_cnt_r))));
                vlSelfRef.__Vdly__milan_datapath__DOT__link_guard__DOT__bounced_r = 1U;
            }
            vlSelfRef.milan_datapath__DOT__link_guard__DOT__guard_rst_r = 1U;
            vlSelfRef.milan_datapath__DOT__link_guard__DOT__eth_rst_r = 1U;
            if (vlSelfRef.milan_datapath__DOT__link_guard__DOT__both_alive_w) {
                vlSelfRef.__Vdly__milan_datapath__DOT__link_guard__DOT__state_r = 2U;
                vlSelfRef.__Vdly__milan_datapath__DOT__link_guard__DOT__settle_r = 0U;
            }
        } else if ((2U == (IData)(vlSelfRef.milan_datapath__DOT__link_guard__DOT__state_r))) {
            vlSelfRef.milan_datapath__DOT__link_guard__DOT__guard_rst_r = 1U;
            if (vlSelfRef.milan_datapath__DOT__link_guard__DOT__both_alive_w) {
                if ((0x00200000U == vlSelfRef.milan_datapath__DOT__link_guard__DOT__settle_r)) {
                    vlSelfRef.__Vdly__milan_datapath__DOT__link_guard__DOT__state_r = 0U;
                    vlSelfRef.milan_datapath__DOT__link_guard__DOT__guard_rst_r = 0U;
                    vlSelfRef.__Vdly__milan_datapath__DOT__link_guard__DOT__bounced_r = 0U;
                } else {
                    vlSelfRef.__Vdly__milan_datapath__DOT__link_guard__DOT__settle_r 
                        = (0x003fffffU & ((IData)(1U) 
                                          + vlSelfRef.milan_datapath__DOT__link_guard__DOT__settle_r));
                    if ((0x00100000U == vlSelfRef.milan_datapath__DOT__link_guard__DOT__settle_r)) {
                        vlSelfRef.milan_datapath__DOT__link_guard__DOT__eth_rst_r = 0U;
                    }
                }
            } else {
                vlSelfRef.__Vdly__milan_datapath__DOT__link_guard__DOT__state_r = 1U;
                vlSelfRef.milan_datapath__DOT__link_guard__DOT__eth_rst_r = 1U;
            }
        } else {
            vlSelfRef.__Vdly__milan_datapath__DOT__link_guard__DOT__state_r = 0U;
        }
        if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__p_periodic_r) 
              & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__per_grant_w))) 
             & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_ev_v_w)) 
                | (0x0aU != (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_ev_w)))))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__per_pend_r 
                = (1U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__per_pend_r));
        } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__per_grant_w))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__per_pend_r 
                = (0x01feU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__per_pend_r));
        }
        if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__p_periodic_r) 
              & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__per_grant_w) 
                    >> 1U))) & ((~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_ev_v_w) 
                                    >> 1U)) | (0x0aU 
                                               != (0x0000000fU 
                                                   & (IData)(
                                                             (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_ev_w 
                                                              >> 4U))))))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__per_pend_r 
                = (2U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__per_pend_r));
        } else if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__per_grant_w))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__per_pend_r 
                = (0x01fdU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__per_pend_r));
        }
        if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__p_periodic_r) 
              & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__per_grant_w) 
                    >> 2U))) & ((~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_ev_v_w) 
                                    >> 2U)) | (0x0aU 
                                               != (0x0000000fU 
                                                   & (IData)(
                                                             (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_ev_w 
                                                              >> 8U))))))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__per_pend_r 
                = (4U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__per_pend_r));
        } else if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__per_grant_w))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__per_pend_r 
                = (0x01fbU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__per_pend_r));
        }
        if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__p_periodic_r) 
              & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__per_grant_w) 
                    >> 3U))) & ((~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_ev_v_w) 
                                    >> 3U)) | (0x0aU 
                                               != (0x0000000fU 
                                                   & (IData)(
                                                             (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_ev_w 
                                                              >> 0x0cU))))))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__per_pend_r 
                = (8U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__per_pend_r));
        } else if ((8U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__per_grant_w))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__per_pend_r 
                = (0x01f7U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__per_pend_r));
        }
        if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__p_periodic_r) 
              & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__per_grant_w) 
                    >> 4U))) & ((~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_ev_v_w) 
                                    >> 4U)) | (0x0aU 
                                               != (0x0000000fU 
                                                   & (IData)(
                                                             (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_ev_w 
                                                              >> 0x10U))))))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__per_pend_r 
                = (0x00000010U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__per_pend_r));
        } else if ((0x00000010U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__per_grant_w))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__per_pend_r 
                = (0x01efU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__per_pend_r));
        }
        if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__p_periodic_r) 
              & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__per_grant_w) 
                    >> 5U))) & ((~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_ev_v_w) 
                                    >> 5U)) | (0x0aU 
                                               != (0x0000000fU 
                                                   & (IData)(
                                                             (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_ev_w 
                                                              >> 0x14U))))))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__per_pend_r 
                = (0x00000020U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__per_pend_r));
        } else if ((0x00000020U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__per_grant_w))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__per_pend_r 
                = (0x01dfU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__per_pend_r));
        }
        if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__p_periodic_r) 
              & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__per_grant_w) 
                    >> 6U))) & ((~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_ev_v_w) 
                                    >> 6U)) | (0x0aU 
                                               != (0x0000000fU 
                                                   & (IData)(
                                                             (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_ev_w 
                                                              >> 0x18U))))))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__per_pend_r 
                = (0x00000040U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__per_pend_r));
        } else if ((0x00000040U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__per_grant_w))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__per_pend_r 
                = (0x01bfU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__per_pend_r));
        }
        if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__p_periodic_r) 
              & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__per_grant_w) 
                    >> 7U))) & ((~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_ev_v_w) 
                                    >> 7U)) | (0x0aU 
                                               != (0x0000000fU 
                                                   & (IData)(
                                                             (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_ev_w 
                                                              >> 0x1cU))))))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__per_pend_r 
                = (0x00000080U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__per_pend_r));
        } else if ((0x00000080U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__per_grant_w))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__per_pend_r 
                = (0x017fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__per_pend_r));
        }
        if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__p_periodic_r) 
              & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__per_grant_w) 
                    >> 8U))) & ((~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_ev_v_w) 
                                    >> 8U)) | (0x0aU 
                                               != (0x0000000fU 
                                                   & (IData)(
                                                             (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_ev_w 
                                                              >> 0x20U))))))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__per_pend_r 
                = (0x00000100U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__per_pend_r));
        } else if ((0x00000100U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__per_grant_w))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__per_pend_r 
                = (0x00ffU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__per_pend_r));
        }
        if ((0U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_side_port__DOT__state_r))) {
            if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_side_port__DOT__accept_w) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_side_port__DOT__state_r 
                    = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_side_port__DOT__fwd_ok_w)
                        ? 1U : 2U);
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_side_port__DOT__sel_r 
                    = (7U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__hb_addr_r 
                             >> 0x00000010U));
            }
        } else if ((1U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_side_port__DOT__state_r))) {
            if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_side_port__DOT__sel_rvalid_w) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_side_port__DOT__state_r = 0U;
            }
        } else {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_side_port__DOT__state_r = 0U;
        }
        vlSelfRef.milan_datapath__DOT__src_recentre_p_r = 0U;
        if ((((IData)(vlSelfRef.milan_datapath__DOT__media_clk_src_r) 
              != (IData)(vlSelfRef.milan_datapath__DOT__src_recentre_q_r)) 
             | ((IData)(vlSelfRef.milan_datapath__DOT__media_grid_align__DOT__engaged_r) 
                & (~ (IData)(vlSelfRef.milan_datapath__DOT__mga_engaged_q_r))))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__src_pend_r = 1U;
            vlSelfRef.__Vdly__milan_datapath__DOT__src_band_ticks_r = 0U;
            vlSelfRef.__Vdly__milan_datapath__DOT__src_eng_ticks_r = 0U;
        } else if (vlSelfRef.milan_datapath__DOT__src_pend_r) {
            if (vlSelfRef.milan_datapath__DOT__media_tick_p) {
                vlSelfRef.__Vdly__milan_datapath__DOT__src_band_ticks_r 
                    = ((1U & ((~ (IData)(vlSelfRef.milan_datapath__DOT__crf_clk_selected_r)) 
                              | ((IData)(vlSelfRef.milan_datapath__DOT__media_grid_align__DOT__engaged_r) 
                                 & VL_GTES_III(16, 0x0020U, 
                                               (0x0000ffffU 
                                                & (VL_GTS_III(16, 0U, (IData)(vlSelfRef.milan_datapath__DOT__media_grid_align__DOT__err_r))
                                                    ? 
                                                   (- (IData)(vlSelfRef.milan_datapath__DOT__media_grid_align__DOT__err_r))
                                                    : (IData)(vlSelfRef.milan_datapath__DOT__media_grid_align__DOT__err_r)))))))
                        ? (0x0000ffffU & ((IData)(1U) 
                                          + (IData)(vlSelfRef.milan_datapath__DOT__src_band_ticks_r)))
                        : 0U);
                vlSelfRef.__Vdly__milan_datapath__DOT__src_eng_ticks_r 
                    = (((IData)(vlSelfRef.milan_datapath__DOT__crf_clk_selected_r) 
                        & (IData)(vlSelfRef.milan_datapath__DOT__media_grid_align__DOT__engaged_r))
                        ? (0x0000ffffU & ((IData)(1U) 
                                          + (IData)(vlSelfRef.milan_datapath__DOT__src_eng_ticks_r)))
                        : 0U);
            }
            if (((0x0800U <= (IData)(vlSelfRef.milan_datapath__DOT__src_band_ticks_r)) 
                 | (0x8000U <= (IData)(vlSelfRef.milan_datapath__DOT__src_eng_ticks_r)))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__src_pend_r = 0U;
                vlSelfRef.milan_datapath__DOT__src_recentre_p_r = 1U;
                vlSelfRef.__Vdly__milan_datapath__DOT__src_band_ticks_r = 0U;
                vlSelfRef.__Vdly__milan_datapath__DOT__src_eng_ticks_r = 0U;
            }
        }
        if (vlSelfRef.milan_datapath__DOT__csr__DOT__ltap_clr_p) {
            vlSelfRef.__Vdly__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__active_r = 0U;
            vlSelfRef.__Vdly__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__stg_r = 1U;
            vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__epoch_r = 0U;
            vlSelfRef.__Vdly__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__samples_r = 0U;
            vlSelfRef.__Vdly__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__timeouts_r = 0U;
            vlSelfRef.__VdlySet__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__last_r__v0 = 1U;
            vlSelfRef.__Vdly__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__active_r = 0U;
            vlSelfRef.__Vdly__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__stg_r = 1U;
            vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__epoch_r = 0U;
            vlSelfRef.__Vdly__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__samples_r = 0U;
            vlSelfRef.__Vdly__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__timeouts_r = 0U;
            vlSelfRef.__VdlySet__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__last_r__v0 = 1U;
        } else if (vlSelfRef.milan_datapath__DOT__csr__DOT__ltap_en_r) {
            if (vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__active_r) {
                if ((0U == (IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__to_r))) {
                    __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__inc16__150__v 
                        = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__timeouts_r;
                    __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__inc16__150__Vfuncout 
                        = (0x0000ffffU & ((0x0000ffffU 
                                           == (IData)(__Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__inc16__150__v))
                                           ? (IData)(__Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__inc16__150__v)
                                           : ((IData)(1U) 
                                              + (IData)(__Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__inc16__150__v))));
                    vlSelfRef.__Vdly__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__active_r = 0U;
                    vlSelfRef.__Vdly__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__timeouts_r 
                        = __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__inc16__150__Vfuncout;
                } else {
                    vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__to_r 
                        = (0x0000ffffU & ((IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__to_r) 
                                          - (IData)(1U)));
                    if ((0U != (IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__nadv_w))) {
                        if (((0U >= (IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__didx_w)) 
                             & (0U < ((IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__didx_w) 
                                      + (IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__nadv_w))))) {
                            __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__151__meas 
                                = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__dsat_w;
                            __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__152__meas 
                                = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__dsat_w;
                            __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__154__meas 
                                = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__dsat_w;
                            __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__151__didx 
                                = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__didx_w;
                            __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__152__didx 
                                = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__didx_w;
                            __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__154__didx 
                                = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__didx_w;
                            vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT____VlemCall_0__hopd 
                                = ((0U == __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__151__didx)
                                    ? (IData)(__Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__151__meas)
                                    : 0U);
                            vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT____VlemCall_1__hopd 
                                = ((0U == __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__152__didx)
                                    ? (IData)(__Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__152__meas)
                                    : 0U);
                            vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT____VlemCall_3__hopd 
                                = ((0U == __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__154__didx)
                                    ? (IData)(__Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__154__meas)
                                    : 0U);
                            __VdlyVal__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__last_r__v3 
                                = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT____VlemCall_0__hopd;
                            vlSelfRef.__VdlySet__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__last_r__v3 = 1U;
                            if (((IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT____VlemCall_1__hopd) 
                                 < vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__min_r[0U])) {
                                __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__153__meas 
                                    = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__dsat_w;
                                __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__153__didx 
                                    = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__didx_w;
                                vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT____VlemCall_2__hopd 
                                    = ((0U == __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__153__didx)
                                        ? (IData)(__Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__153__meas)
                                        : 0U);
                                __VdlyVal__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__min_r__v3 
                                    = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT____VlemCall_2__hopd;
                                vlSelfRef.__VdlySet__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__min_r__v3 = 1U;
                            }
                            if (((IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT____VlemCall_3__hopd) 
                                 > vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__max_r[0U])) {
                                __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__155__meas 
                                    = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__dsat_w;
                                __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__155__didx 
                                    = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__didx_w;
                                vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT____VlemCall_4__hopd 
                                    = ((0U == __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__155__didx)
                                        ? (IData)(__Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__155__meas)
                                        : 0U);
                                __VdlyVal__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__max_r__v3 
                                    = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT____VlemCall_4__hopd;
                                vlSelfRef.__VdlySet__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__max_r__v3 = 1U;
                            }
                        }
                        vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__prevc_r 
                            = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__cyc_r;
                        vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__to_r = 0xc350U;
                        if ((3U == (((IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__stg_r) 
                                     + (IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__nadv_w)) 
                                    - (IData)(1U)))) {
                            __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__inc16__156__v 
                                = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__samples_r;
                            __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__inc16__156__Vfuncout 
                                = (0x0000ffffU & ((0x0000ffffU 
                                                   == (IData)(__Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__inc16__156__v))
                                                   ? (IData)(__Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__inc16__156__v)
                                                   : 
                                                  ((IData)(1U) 
                                                   + (IData)(__Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__inc16__156__v))));
                            vlSelfRef.__Vdly__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__active_r = 0U;
                            vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__epoch_r 
                                = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__epoch_pend_r;
                            vlSelfRef.__Vdly__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__samples_r 
                                = __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__inc16__156__Vfuncout;
                        } else {
                            vlSelfRef.__Vdly__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__stg_r 
                                = (3U & ((IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__stg_r) 
                                         + (IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__nadv_w)));
                        }
                        if (((1U >= (IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__didx_w)) 
                             & (1U < ((IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__didx_w) 
                                      + (IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__nadv_w))))) {
                            __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__151__meas 
                                = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__dsat_w;
                            __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__152__meas 
                                = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__dsat_w;
                            __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__154__meas 
                                = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__dsat_w;
                            __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__151__didx 
                                = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__didx_w;
                            __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__152__didx 
                                = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__didx_w;
                            __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__154__didx 
                                = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__didx_w;
                            vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT____VlemCall_0__hopd 
                                = ((1U == __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__151__didx)
                                    ? (IData)(__Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__151__meas)
                                    : 0U);
                            vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT____VlemCall_1__hopd 
                                = ((1U == __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__152__didx)
                                    ? (IData)(__Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__152__meas)
                                    : 0U);
                            vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT____VlemCall_3__hopd 
                                = ((1U == __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__154__didx)
                                    ? (IData)(__Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__154__meas)
                                    : 0U);
                            __VdlyVal__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__last_r__v4 
                                = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT____VlemCall_0__hopd;
                            vlSelfRef.__VdlySet__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__last_r__v4 = 1U;
                            if (((IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT____VlemCall_1__hopd) 
                                 < vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__min_r[1U])) {
                                __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__153__meas 
                                    = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__dsat_w;
                                __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__153__didx 
                                    = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__didx_w;
                                vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT____VlemCall_2__hopd 
                                    = ((1U == __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__153__didx)
                                        ? (IData)(__Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__153__meas)
                                        : 0U);
                                __VdlyVal__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__min_r__v4 
                                    = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT____VlemCall_2__hopd;
                                vlSelfRef.__VdlySet__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__min_r__v4 = 1U;
                            }
                            if (((IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT____VlemCall_3__hopd) 
                                 > vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__max_r[1U])) {
                                __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__155__meas 
                                    = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__dsat_w;
                                __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__155__didx 
                                    = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__didx_w;
                                vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT____VlemCall_4__hopd 
                                    = ((1U == __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__155__didx)
                                        ? (IData)(__Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__155__meas)
                                        : 0U);
                                __VdlyVal__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__max_r__v4 
                                    = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT____VlemCall_4__hopd;
                                vlSelfRef.__VdlySet__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__max_r__v4 = 1U;
                            }
                        }
                        if (((2U >= (IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__didx_w)) 
                             & (2U < ((IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__didx_w) 
                                      + (IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__nadv_w))))) {
                            __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__151__meas 
                                = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__dsat_w;
                            __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__152__meas 
                                = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__dsat_w;
                            __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__154__meas 
                                = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__dsat_w;
                            __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__151__didx 
                                = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__didx_w;
                            __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__152__didx 
                                = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__didx_w;
                            __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__154__didx 
                                = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__didx_w;
                            vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT____VlemCall_0__hopd 
                                = ((2U == __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__151__didx)
                                    ? (IData)(__Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__151__meas)
                                    : 0U);
                            vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT____VlemCall_1__hopd 
                                = ((2U == __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__152__didx)
                                    ? (IData)(__Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__152__meas)
                                    : 0U);
                            vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT____VlemCall_3__hopd 
                                = ((2U == __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__154__didx)
                                    ? (IData)(__Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__154__meas)
                                    : 0U);
                            __VdlyVal__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__last_r__v5 
                                = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT____VlemCall_0__hopd;
                            vlSelfRef.__VdlySet__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__last_r__v5 = 1U;
                            if (((IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT____VlemCall_1__hopd) 
                                 < vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__min_r[2U])) {
                                __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__153__meas 
                                    = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__dsat_w;
                                __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__153__didx 
                                    = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__didx_w;
                                vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT____VlemCall_2__hopd 
                                    = ((2U == __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__153__didx)
                                        ? (IData)(__Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__153__meas)
                                        : 0U);
                                __VdlyVal__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__min_r__v5 
                                    = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT____VlemCall_2__hopd;
                                vlSelfRef.__VdlySet__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__min_r__v5 = 1U;
                            }
                            if (((IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT____VlemCall_3__hopd) 
                                 > vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__max_r[2U])) {
                                __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__155__meas 
                                    = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__dsat_w;
                                __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__155__didx 
                                    = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__didx_w;
                                vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT____VlemCall_4__hopd 
                                    = ((2U == __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__155__didx)
                                        ? (IData)(__Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__155__meas)
                                        : 0U);
                                __VdlyVal__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__max_r__v5 
                                    = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT____VlemCall_4__hopd;
                                vlSelfRef.__VdlySet__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__max_r__v5 = 1U;
                            }
                        }
                    }
                }
            } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__ltap_txp_q_r))) {
                vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__to_r = 0xc350U;
                vlSelfRef.__Vdly__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__active_r = 1U;
                vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__prevc_r 
                    = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__cyc_r;
                vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__epoch_pend_r 
                    = ((vlSelfRef.milan_datapath__DOT__ts_counter__DOT__acc[1U] 
                        << 8U) | (vlSelfRef.milan_datapath__DOT__ts_counter__DOT__acc[0U] 
                                  >> 0x00000018U));
                vlSelfRef.__Vdly__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__stg_r = 1U;
                if ((0U != (IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__nadv0_w))) {
                    if ((0U < (IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__nadv0_w))) {
                        vlSelfRef.__VdlySet__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__last_r__v6 = 1U;
                    }
                    if ((3U == (IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__nadv0_w))) {
                        __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__inc16__157__v 
                            = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__samples_r;
                        __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__inc16__157__Vfuncout 
                            = (0x0000ffffU & ((0x0000ffffU 
                                               == (IData)(__Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__inc16__157__v))
                                               ? (IData)(__Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__inc16__157__v)
                                               : ((IData)(1U) 
                                                  + (IData)(__Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__inc16__157__v))));
                        vlSelfRef.__Vdly__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__active_r = 0U;
                        vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__epoch_r 
                            = ((vlSelfRef.milan_datapath__DOT__ts_counter__DOT__acc[1U] 
                                << 8U) | (vlSelfRef.milan_datapath__DOT__ts_counter__DOT__acc[0U] 
                                          >> 0x00000018U));
                        vlSelfRef.__Vdly__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__samples_r 
                            = __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__inc16__157__Vfuncout;
                    } else {
                        vlSelfRef.__Vdly__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__stg_r 
                            = (3U & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__nadv0_w)));
                    }
                    if ((1U < (IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__nadv0_w))) {
                        vlSelfRef.__VdlySet__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__last_r__v7 = 1U;
                    }
                    if ((2U < (IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__nadv0_w))) {
                        vlSelfRef.__VdlySet__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__last_r__v8 = 1U;
                    }
                }
            }
            if (vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__active_r) {
                if ((0U == (IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__to_r))) {
                    __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__inc16__142__v 
                        = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__timeouts_r;
                    __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__inc16__142__Vfuncout 
                        = (0x0000ffffU & ((0x0000ffffU 
                                           == (IData)(__Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__inc16__142__v))
                                           ? (IData)(__Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__inc16__142__v)
                                           : ((IData)(1U) 
                                              + (IData)(__Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__inc16__142__v))));
                    vlSelfRef.__Vdly__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__active_r = 0U;
                    vlSelfRef.__Vdly__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__timeouts_r 
                        = __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__inc16__142__Vfuncout;
                } else {
                    vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__to_r 
                        = (0x0000ffffU & ((IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__to_r) 
                                          - (IData)(1U)));
                    if ((0U != (IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__nadv_w))) {
                        if (((0U >= (IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__didx_w)) 
                             & (0U < ((IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__didx_w) 
                                      + (IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__nadv_w))))) {
                            __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__143__meas 
                                = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__dsat_w;
                            __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__144__meas 
                                = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__dsat_w;
                            __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__146__meas 
                                = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__dsat_w;
                            __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__143__didx 
                                = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__didx_w;
                            __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__144__didx 
                                = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__didx_w;
                            __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__146__didx 
                                = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__didx_w;
                            vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT____VlemCall_0__hopd 
                                = ((0U == __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__143__didx)
                                    ? (IData)(__Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__143__meas)
                                    : 0U);
                            vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT____VlemCall_1__hopd 
                                = ((0U == __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__144__didx)
                                    ? (IData)(__Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__144__meas)
                                    : 0U);
                            vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT____VlemCall_3__hopd 
                                = ((0U == __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__146__didx)
                                    ? (IData)(__Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__146__meas)
                                    : 0U);
                            __VdlyVal__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__last_r__v3 
                                = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT____VlemCall_0__hopd;
                            vlSelfRef.__VdlySet__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__last_r__v3 = 1U;
                            if (((IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT____VlemCall_1__hopd) 
                                 < vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__min_r[0U])) {
                                __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__145__meas 
                                    = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__dsat_w;
                                __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__145__didx 
                                    = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__didx_w;
                                vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT____VlemCall_2__hopd 
                                    = ((0U == __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__145__didx)
                                        ? (IData)(__Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__145__meas)
                                        : 0U);
                                __VdlyVal__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__min_r__v3 
                                    = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT____VlemCall_2__hopd;
                                vlSelfRef.__VdlySet__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__min_r__v3 = 1U;
                            }
                            if (((IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT____VlemCall_3__hopd) 
                                 > vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__max_r[0U])) {
                                __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__147__meas 
                                    = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__dsat_w;
                                __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__147__didx 
                                    = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__didx_w;
                                vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT____VlemCall_4__hopd 
                                    = ((0U == __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__147__didx)
                                        ? (IData)(__Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__147__meas)
                                        : 0U);
                                __VdlyVal__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__max_r__v3 
                                    = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT____VlemCall_4__hopd;
                                vlSelfRef.__VdlySet__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__max_r__v3 = 1U;
                            }
                        }
                        vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__prevc_r 
                            = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__cyc_r;
                        vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__to_r = 0xc350U;
                        if ((3U == (((IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__stg_r) 
                                     + (IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__nadv_w)) 
                                    - (IData)(1U)))) {
                            __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__inc16__148__v 
                                = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__samples_r;
                            __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__inc16__148__Vfuncout 
                                = (0x0000ffffU & ((0x0000ffffU 
                                                   == (IData)(__Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__inc16__148__v))
                                                   ? (IData)(__Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__inc16__148__v)
                                                   : 
                                                  ((IData)(1U) 
                                                   + (IData)(__Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__inc16__148__v))));
                            vlSelfRef.__Vdly__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__active_r = 0U;
                            vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__epoch_r 
                                = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__epoch_pend_r;
                            vlSelfRef.__Vdly__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__samples_r 
                                = __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__inc16__148__Vfuncout;
                        } else {
                            vlSelfRef.__Vdly__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__stg_r 
                                = (3U & ((IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__stg_r) 
                                         + (IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__nadv_w)));
                        }
                        if (((1U >= (IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__didx_w)) 
                             & (1U < ((IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__didx_w) 
                                      + (IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__nadv_w))))) {
                            __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__143__meas 
                                = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__dsat_w;
                            __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__144__meas 
                                = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__dsat_w;
                            __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__146__meas 
                                = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__dsat_w;
                            __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__143__didx 
                                = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__didx_w;
                            __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__144__didx 
                                = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__didx_w;
                            __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__146__didx 
                                = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__didx_w;
                            vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT____VlemCall_0__hopd 
                                = ((1U == __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__143__didx)
                                    ? (IData)(__Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__143__meas)
                                    : 0U);
                            vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT____VlemCall_1__hopd 
                                = ((1U == __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__144__didx)
                                    ? (IData)(__Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__144__meas)
                                    : 0U);
                            vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT____VlemCall_3__hopd 
                                = ((1U == __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__146__didx)
                                    ? (IData)(__Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__146__meas)
                                    : 0U);
                            __VdlyVal__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__last_r__v4 
                                = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT____VlemCall_0__hopd;
                            vlSelfRef.__VdlySet__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__last_r__v4 = 1U;
                            if (((IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT____VlemCall_1__hopd) 
                                 < vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__min_r[1U])) {
                                __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__145__meas 
                                    = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__dsat_w;
                                __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__145__didx 
                                    = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__didx_w;
                                vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT____VlemCall_2__hopd 
                                    = ((1U == __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__145__didx)
                                        ? (IData)(__Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__145__meas)
                                        : 0U);
                                __VdlyVal__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__min_r__v4 
                                    = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT____VlemCall_2__hopd;
                                vlSelfRef.__VdlySet__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__min_r__v4 = 1U;
                            }
                            if (((IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT____VlemCall_3__hopd) 
                                 > vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__max_r[1U])) {
                                __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__147__meas 
                                    = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__dsat_w;
                                __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__147__didx 
                                    = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__didx_w;
                                vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT____VlemCall_4__hopd 
                                    = ((1U == __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__147__didx)
                                        ? (IData)(__Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__147__meas)
                                        : 0U);
                                __VdlyVal__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__max_r__v4 
                                    = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT____VlemCall_4__hopd;
                                vlSelfRef.__VdlySet__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__max_r__v4 = 1U;
                            }
                        }
                        if (((2U >= (IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__didx_w)) 
                             & (2U < ((IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__didx_w) 
                                      + (IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__nadv_w))))) {
                            __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__143__meas 
                                = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__dsat_w;
                            __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__144__meas 
                                = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__dsat_w;
                            __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__146__meas 
                                = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__dsat_w;
                            __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__143__didx 
                                = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__didx_w;
                            __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__144__didx 
                                = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__didx_w;
                            __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__146__didx 
                                = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__didx_w;
                            vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT____VlemCall_0__hopd 
                                = ((2U == __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__143__didx)
                                    ? (IData)(__Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__143__meas)
                                    : 0U);
                            vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT____VlemCall_1__hopd 
                                = ((2U == __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__144__didx)
                                    ? (IData)(__Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__144__meas)
                                    : 0U);
                            vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT____VlemCall_3__hopd 
                                = ((2U == __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__146__didx)
                                    ? (IData)(__Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__146__meas)
                                    : 0U);
                            __VdlyVal__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__last_r__v5 
                                = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT____VlemCall_0__hopd;
                            vlSelfRef.__VdlySet__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__last_r__v5 = 1U;
                            if (((IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT____VlemCall_1__hopd) 
                                 < vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__min_r[2U])) {
                                __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__145__meas 
                                    = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__dsat_w;
                                __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__145__didx 
                                    = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__didx_w;
                                vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT____VlemCall_2__hopd 
                                    = ((2U == __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__145__didx)
                                        ? (IData)(__Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__145__meas)
                                        : 0U);
                                __VdlyVal__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__min_r__v5 
                                    = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT____VlemCall_2__hopd;
                                vlSelfRef.__VdlySet__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__min_r__v5 = 1U;
                            }
                            if (((IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT____VlemCall_3__hopd) 
                                 > vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__max_r[2U])) {
                                __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__147__meas 
                                    = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__dsat_w;
                                __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__147__didx 
                                    = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__didx_w;
                                vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT____VlemCall_4__hopd 
                                    = ((2U == __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__147__didx)
                                        ? (IData)(__Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__147__meas)
                                        : 0U);
                                __VdlyVal__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__max_r__v5 
                                    = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT____VlemCall_4__hopd;
                                vlSelfRef.__VdlySet__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__max_r__v5 = 1U;
                            }
                        }
                    }
                }
            } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__ltap_rxp_q_r))) {
                vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__to_r = 0xc350U;
                vlSelfRef.__Vdly__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__active_r = 1U;
                vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__prevc_r 
                    = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__cyc_r;
                vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__epoch_pend_r 
                    = ((vlSelfRef.milan_datapath__DOT__ts_counter__DOT__acc[1U] 
                        << 8U) | (vlSelfRef.milan_datapath__DOT__ts_counter__DOT__acc[0U] 
                                  >> 0x00000018U));
                vlSelfRef.__Vdly__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__stg_r = 1U;
                if ((0U != (IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__nadv0_w))) {
                    if ((0U < (IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__nadv0_w))) {
                        vlSelfRef.__VdlySet__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__last_r__v6 = 1U;
                    }
                    if ((3U == (IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__nadv0_w))) {
                        __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__inc16__149__v 
                            = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__samples_r;
                        __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__inc16__149__Vfuncout 
                            = (0x0000ffffU & ((0x0000ffffU 
                                               == (IData)(__Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__inc16__149__v))
                                               ? (IData)(__Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__inc16__149__v)
                                               : ((IData)(1U) 
                                                  + (IData)(__Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__inc16__149__v))));
                        vlSelfRef.__Vdly__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__active_r = 0U;
                        vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__epoch_r 
                            = ((vlSelfRef.milan_datapath__DOT__ts_counter__DOT__acc[1U] 
                                << 8U) | (vlSelfRef.milan_datapath__DOT__ts_counter__DOT__acc[0U] 
                                          >> 0x00000018U));
                        vlSelfRef.__Vdly__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__samples_r 
                            = __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__inc16__149__Vfuncout;
                    } else {
                        vlSelfRef.__Vdly__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__stg_r 
                            = (3U & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__nadv0_w)));
                    }
                    if ((1U < (IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__nadv0_w))) {
                        vlSelfRef.__VdlySet__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__last_r__v7 = 1U;
                    }
                    if ((2U < (IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__nadv0_w))) {
                        vlSelfRef.__VdlySet__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__last_r__v8 = 1U;
                    }
                }
            }
        } else {
            vlSelfRef.__Vdly__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__active_r = 0U;
            vlSelfRef.__Vdly__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__active_r = 0U;
        }
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_cnt_r 
            = ((0x00fffff8U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_cnt_r) 
               | (7U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_mid_w 
                        + ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_push_ok_w))
                            ? 1U : 0U))));
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_cnt_r 
            = ((0x00ffffc7U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_cnt_r) 
               | (0x00000038U & (((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_mid_w 
                                   >> 3U) + ((2U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_push_ok_w))
                                              ? 1U : 0U)) 
                                 << 3U)));
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_cnt_r 
            = ((0x00fffe3fU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_cnt_r) 
               | (0x000001c0U & (((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_mid_w 
                                   >> 6U) + ((4U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_push_ok_w))
                                              ? 1U : 0U)) 
                                 << 6U)));
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_cnt_r 
            = ((0x00fff1ffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_cnt_r) 
               | (0x00000e00U & (((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_mid_w 
                                   >> 9U) + ((8U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_push_ok_w))
                                              ? 1U : 0U)) 
                                 << 9U)));
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_cnt_r 
            = ((0x00ff8fffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_cnt_r) 
               | (0x00007000U & (((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_mid_w 
                                   >> 0x0cU) + ((0x00000010U 
                                                 & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_push_ok_w))
                                                 ? 1U
                                                 : 0U)) 
                                 << 0x0000000cU)));
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_cnt_r 
            = ((0x00fc7fffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_cnt_r) 
               | (0x00038000U & (((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_mid_w 
                                   >> 0x0fU) + ((0x00000020U 
                                                 & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_push_ok_w))
                                                 ? 1U
                                                 : 0U)) 
                                 << 0x0000000fU)));
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_cnt_r 
            = ((0x00e3ffffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_cnt_r) 
               | (0x001c0000U & (((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_mid_w 
                                   >> 0x12U) + ((0x00000040U 
                                                 & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_push_ok_w))
                                                 ? 1U
                                                 : 0U)) 
                                 << 0x00000012U)));
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_cnt_r 
            = ((0x001fffffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_cnt_r) 
               | (0x00e00000U & (((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_mid_w 
                                   >> 0x15U) + ((0x00000080U 
                                                 & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_push_ok_w))
                                                 ? 1U
                                                 : 0U)) 
                                 << 0x00000015U)));
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
                                                        (1U 
                                                         & (~ 
                                                            ((IData)(vlSelfRef.s_axi_awaddr) 
                                                             >> 5U)))) {
                                                        if (
                                                            (0x00000010U 
                                                             & (IData)(vlSelfRef.s_axi_awaddr))) {
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
                                                                                vlSelfRef.milan_datapath__DOT__csr__DOT__irq_status 
                                                                                = 
                                                                                (0xfffffffdU 
                                                                                & vlSelfRef.milan_datapath__DOT__csr__DOT__irq_status);
                                                                            }
                                                                            if (
                                                                                (4U 
                                                                                & vlSelfRef.s_axi_wdata)) {
                                                                                vlSelfRef.milan_datapath__DOT__csr__DOT__irq_status 
                                                                                = 
                                                                                (0xfffffffbU 
                                                                                & vlSelfRef.milan_datapath__DOT__csr__DOT__irq_status);
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
        if (vlSelfRef.milan_datapath__DOT__evt_link_change) {
            vlSelfRef.milan_datapath__DOT__csr__DOT__irq_status 
                = (2U | vlSelfRef.milan_datapath__DOT__csr__DOT__irq_status);
        }
        if (vlSelfRef.milan_datapath__DOT__ethernet_counters__DOT__rollover_r) {
            vlSelfRef.milan_datapath__DOT__csr__DOT__irq_status 
                = (4U | vlSelfRef.milan_datapath__DOT__csr__DOT__irq_status);
        }
        if (vlSelfRef.milan_datapath__DOT__csr__DOT__cmrd_go_w) {
            vlSelfRef.milan_datapath__DOT__csr__DOT__cmrd_valid_r = 0U;
            vlSelfRef.milan_datapath__DOT__csr__DOT__cmrd_to_r = 0U;
            vlSelfRef.__Vdly__milan_datapath__DOT__csr__DOT__cmrd_busy_r = 1U;
            vlSelfRef.__Vdly__milan_datapath__DOT__csr__DOT__cmrd_flush_r = 1U;
            vlSelfRef.__Vdly__milan_datapath__DOT__csr__DOT__cmrd_wd_r = 0x0fU;
        } else if (vlSelfRef.milan_datapath__DOT__csr__DOT__cmrd_busy_r) {
            if (vlSelfRef.milan_datapath__DOT__csr__DOT__cmrd_flush_r) {
                vlSelfRef.__Vdly__milan_datapath__DOT__csr__DOT__cmrd_wd_r 
                    = (0x0000000fU & ((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__cmrd_wd_r) 
                                      - (IData)(1U)));
                vlSelfRef.__Vdly__milan_datapath__DOT__csr__DOT__cmrd_flush_r = 0U;
            } else if (((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__cmrd_side_r)
                         ? (IData)(vlSelfRef.milan_datapath__DOT__cmap_rd_valid_w)
                         : (IData)(vlSelfRef.milan_datapath__DOT__rmap_rd_valid_r))) {
                vlSelfRef.milan_datapath__DOT__csr__DOT__cmrd_data_r 
                    = ((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__cmrd_side_r)
                        ? (IData)(vlSelfRef.milan_datapath__DOT__cmap_rd_data_w)
                        : (IData)(vlSelfRef.milan_datapath__DOT__rmap_rd_data_w));
                vlSelfRef.milan_datapath__DOT__csr__DOT__cmrd_valid_r = 1U;
                vlSelfRef.__Vdly__milan_datapath__DOT__csr__DOT__cmrd_busy_r = 0U;
            } else if ((0U == (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__cmrd_wd_r))) {
                vlSelfRef.milan_datapath__DOT__csr__DOT__cmrd_to_r = 1U;
                vlSelfRef.__Vdly__milan_datapath__DOT__csr__DOT__cmrd_busy_r = 0U;
            } else {
                vlSelfRef.__Vdly__milan_datapath__DOT__csr__DOT__cmrd_wd_r 
                    = (0x0000000fU & ((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__cmrd_wd_r) 
                                      - (IData)(1U)));
            }
        }
        if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT____Vcellout__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__alloc_gnt_o) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__DOT__wr_closed_r = 0U;
        }
        if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__DOT__byte_acc_w) {
            if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__p2_l_r) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__DOT__wr_closed_r = 1U;
            }
        }
        if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT____Vcellout__g_rx_pool__BRA__4__KET____DOT__u_rx_slots__alloc_gnt_o) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__4__KET____DOT__u_rx_slots__DOT__wr_closed_r = 0U;
        }
        if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__4__KET____DOT__u_rx_slots__DOT__byte_acc_w) {
            if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__p2_l_r) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__4__KET____DOT__u_rx_slots__DOT__wr_closed_r = 1U;
            }
        }
        if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT____Vcellout__g_rx_pool__BRA__2__KET____DOT__u_rx_slots__alloc_gnt_o) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__2__KET____DOT__u_rx_slots__DOT__wr_closed_r = 0U;
        }
        if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__2__KET____DOT__u_rx_slots__DOT__byte_acc_w) {
            if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__p2_l_r) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__2__KET____DOT__u_rx_slots__DOT__wr_closed_r = 1U;
            }
        }
        if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT____Vcellout__g_rx_pool__BRA__1__KET____DOT__u_rx_slots__alloc_gnt_o) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__1__KET____DOT__u_rx_slots__DOT__wr_closed_r = 0U;
        }
        if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__1__KET____DOT__u_rx_slots__DOT__byte_acc_w) {
            if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__p2_l_r) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__1__KET____DOT__u_rx_slots__DOT__wr_closed_r = 1U;
            }
        }
        if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__v_alloc_gnt_w) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__0__KET____DOT__u_rx_slots__DOT__wr_closed_r = 0U;
        }
        if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__0__KET____DOT__u_rx_slots__DOT__byte_acc_w) {
            if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__p2_l_r) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__0__KET____DOT__u_rx_slots__DOT__wr_closed_r = 1U;
            }
        }
        if (vlSelfRef.milan_datapath__DOT__aafcap_pv_w) {
            vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__i2s_hold_r 
                = (((QData)((IData)(vlSelfRef.milan_datapath__DOT__aafcap_l_w)) 
                    << 0x00000018U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__aafcap_r_w)));
        }
        if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_la_msrp_w) 
              & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_grant_w))) 
             & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w)) 
                | (9U != (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w)))))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_pend_r 
                = (1U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_pend_r));
        } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_grant_w))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_pend_r 
                = (0x01feU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_pend_r));
        }
        if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_la_msrp_w) 
              & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_grant_w) 
                    >> 1U))) & ((~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w) 
                                    >> 1U)) | (9U != 
                                               (0x0000000fU 
                                                & (IData)(
                                                          (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w 
                                                           >> 4U))))))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_pend_r 
                = (2U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_pend_r));
        } else if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_grant_w))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_pend_r 
                = (0x01fdU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_pend_r));
        }
        if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_la_msrp_w) 
              & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_grant_w) 
                    >> 2U))) & ((~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w) 
                                    >> 2U)) | (9U != 
                                               (0x0000000fU 
                                                & (IData)(
                                                          (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w 
                                                           >> 8U))))))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_pend_r 
                = (4U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_pend_r));
        } else if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_grant_w))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_pend_r 
                = (0x01fbU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_pend_r));
        }
        if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_la_msrp_w) 
              & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_grant_w) 
                    >> 3U))) & ((~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w) 
                                    >> 3U)) | (9U != 
                                               (0x0000000fU 
                                                & (IData)(
                                                          (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w 
                                                           >> 0x0cU))))))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_pend_r 
                = (8U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_pend_r));
        } else if ((8U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_grant_w))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_pend_r 
                = (0x01f7U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_pend_r));
        }
        if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_la_msrp_w) 
              & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_grant_w) 
                    >> 4U))) & ((~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w) 
                                    >> 4U)) | (9U != 
                                               (0x0000000fU 
                                                & (IData)(
                                                          (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w 
                                                           >> 0x10U))))))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_pend_r 
                = (0x00000010U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_pend_r));
        } else if ((0x00000010U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_grant_w))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_pend_r 
                = (0x01efU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_pend_r));
        }
        if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_la_msrp_w) 
              & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_grant_w) 
                    >> 5U))) & ((~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w) 
                                    >> 5U)) | (9U != 
                                               (0x0000000fU 
                                                & (IData)(
                                                          (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w 
                                                           >> 0x14U))))))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_pend_r 
                = (0x00000020U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_pend_r));
        } else if ((0x00000020U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_grant_w))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_pend_r 
                = (0x01dfU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_pend_r));
        }
        if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_la_msrp_w) 
              & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_grant_w) 
                    >> 6U))) & ((~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w) 
                                    >> 6U)) | (9U != 
                                               (0x0000000fU 
                                                & (IData)(
                                                          (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w 
                                                           >> 0x18U))))))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_pend_r 
                = (0x00000040U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_pend_r));
        } else if ((0x00000040U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_grant_w))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_pend_r 
                = (0x01bfU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_pend_r));
        }
        if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_la_msrp_w) 
              & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_grant_w) 
                    >> 7U))) & ((~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w) 
                                    >> 7U)) | (9U != 
                                               (0x0000000fU 
                                                & (IData)(
                                                          (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w 
                                                           >> 0x1cU))))))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_pend_r 
                = (0x00000080U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_pend_r));
        } else if ((0x00000080U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_grant_w))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_pend_r 
                = (0x017fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_pend_r));
        }
        if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_la_msrp_w) 
              & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_grant_w) 
                    >> 8U))) & ((~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w) 
                                    >> 8U)) | (9U != 
                                               (0x0000000fU 
                                                & (IData)(
                                                          (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w 
                                                           >> 0x20U))))))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_pend_r 
                = (0x00000100U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_pend_r));
        } else if ((0x00000100U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_grant_w))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_pend_r 
                = (0x00ffU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_pend_r));
        }
        if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_la_msrp_w) 
              & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rla_grant_w))) 
             & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_ev_v_w)) 
                | (9U != (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_ev_w)))))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rla_pend_r 
                = (1U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rla_pend_r));
        } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rla_grant_w))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rla_pend_r 
                = (0x01feU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rla_pend_r));
        }
        if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_la_msrp_w) 
              & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rla_grant_w) 
                    >> 1U))) & ((~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_ev_v_w) 
                                    >> 1U)) | (9U != 
                                               (0x0000000fU 
                                                & (IData)(
                                                          (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_ev_w 
                                                           >> 4U))))))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rla_pend_r 
                = (2U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rla_pend_r));
        } else if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rla_grant_w))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rla_pend_r 
                = (0x01fdU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rla_pend_r));
        }
        if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_la_msrp_w) 
              & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rla_grant_w) 
                    >> 2U))) & ((~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_ev_v_w) 
                                    >> 2U)) | (9U != 
                                               (0x0000000fU 
                                                & (IData)(
                                                          (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_ev_w 
                                                           >> 8U))))))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rla_pend_r 
                = (4U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rla_pend_r));
        } else if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rla_grant_w))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rla_pend_r 
                = (0x01fbU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rla_pend_r));
        }
        if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_la_msrp_w) 
              & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rla_grant_w) 
                    >> 3U))) & ((~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_ev_v_w) 
                                    >> 3U)) | (9U != 
                                               (0x0000000fU 
                                                & (IData)(
                                                          (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_ev_w 
                                                           >> 0x0cU))))))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rla_pend_r 
                = (8U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rla_pend_r));
        } else if ((8U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rla_grant_w))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rla_pend_r 
                = (0x01f7U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rla_pend_r));
        }
        if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_la_msrp_w) 
              & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rla_grant_w) 
                    >> 4U))) & ((~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_ev_v_w) 
                                    >> 4U)) | (9U != 
                                               (0x0000000fU 
                                                & (IData)(
                                                          (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_ev_w 
                                                           >> 0x10U))))))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rla_pend_r 
                = (0x00000010U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rla_pend_r));
        } else if ((0x00000010U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rla_grant_w))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rla_pend_r 
                = (0x01efU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rla_pend_r));
        }
        if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_la_msrp_w) 
              & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rla_grant_w) 
                    >> 5U))) & ((~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_ev_v_w) 
                                    >> 5U)) | (9U != 
                                               (0x0000000fU 
                                                & (IData)(
                                                          (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_ev_w 
                                                           >> 0x14U))))))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rla_pend_r 
                = (0x00000020U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rla_pend_r));
        } else if ((0x00000020U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rla_grant_w))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rla_pend_r 
                = (0x01dfU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rla_pend_r));
        }
        if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_la_msrp_w) 
              & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rla_grant_w) 
                    >> 6U))) & ((~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_ev_v_w) 
                                    >> 6U)) | (9U != 
                                               (0x0000000fU 
                                                & (IData)(
                                                          (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_ev_w 
                                                           >> 0x18U))))))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rla_pend_r 
                = (0x00000040U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rla_pend_r));
        } else if ((0x00000040U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rla_grant_w))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rla_pend_r 
                = (0x01bfU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rla_pend_r));
        }
        if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_la_msrp_w) 
              & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rla_grant_w) 
                    >> 7U))) & ((~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_ev_v_w) 
                                    >> 7U)) | (9U != 
                                               (0x0000000fU 
                                                & (IData)(
                                                          (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_ev_w 
                                                           >> 0x1cU))))))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rla_pend_r 
                = (0x00000080U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rla_pend_r));
        } else if ((0x00000080U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rla_grant_w))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rla_pend_r 
                = (0x017fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rla_pend_r));
        }
        if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_la_msrp_w) 
              & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rla_grant_w) 
                    >> 8U))) & ((~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_ev_v_w) 
                                    >> 8U)) | (9U != 
                                               (0x0000000fU 
                                                & (IData)(
                                                          (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_ev_w 
                                                           >> 0x20U))))))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rla_pend_r 
                = (0x00000100U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rla_pend_r));
        } else if ((0x00000100U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rla_grant_w))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rla_pend_r 
                = (0x00ffU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rla_pend_r));
        }
        if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_rx_hit_w) 
             & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rx_registering_w))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rtype_r 
                = ((0x01feU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rtype_r)) 
                   | (2U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_attr_type_w)));
            if ((2U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_attr_type_w))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__fcode_r[0U] 
                    = ((0xffffff00U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__fcode_r[0U]) 
                       | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_fail_code_w));
            }
        }
        if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__ctl_acc_w) 
             & (0U == (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r))))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rtype_r 
                = (0x01feU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rtype_r));
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__fcode_r[0U] 
                = (0xffffff00U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__fcode_r[0U]);
        }
        if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_rx_hit_w) 
              >> 1U) & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rx_registering_w))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rtype_r 
                = ((0x01fdU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rtype_r)) 
                   | ((2U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_attr_type_w)) 
                      << 1U));
            if ((2U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_attr_type_w))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__fcode_r[0U] 
                    = ((0xffff00ffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__fcode_r[0U]) 
                       | ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_fail_code_w) 
                          << 8U));
            }
        }
        if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__ctl_acc_w) 
             & (1U == (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r))))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rtype_r 
                = (0x01fdU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rtype_r));
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__fcode_r[0U] 
                = (0xffff00ffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__fcode_r[0U]);
        }
        if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_rx_hit_w) 
              >> 2U) & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rx_registering_w))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rtype_r 
                = ((0x01fbU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rtype_r)) 
                   | ((2U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_attr_type_w)) 
                      << 2U));
            if ((2U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_attr_type_w))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__fcode_r[0U] 
                    = ((0xff00ffffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__fcode_r[0U]) 
                       | ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_fail_code_w) 
                          << 0x00000010U));
            }
        }
        if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__ctl_acc_w) 
             & (2U == (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r))))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rtype_r 
                = (0x01fbU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rtype_r));
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__fcode_r[0U] 
                = (0xff00ffffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__fcode_r[0U]);
        }
        if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_rx_hit_w) 
              >> 3U) & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rx_registering_w))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rtype_r 
                = ((0x01f7U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rtype_r)) 
                   | ((2U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_attr_type_w)) 
                      << 3U));
            if ((2U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_attr_type_w))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__fcode_r[0U] 
                    = ((0x00ffffffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__fcode_r[0U]) 
                       | ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_fail_code_w) 
                          << 0x00000018U));
            }
        }
        if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__ctl_acc_w) 
             & (3U == (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r))))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rtype_r 
                = (0x01f7U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rtype_r));
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__fcode_r[0U] 
                = (0x00ffffffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__fcode_r[0U]);
        }
        if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_rx_hit_w) 
              >> 4U) & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rx_registering_w))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rtype_r 
                = ((0x01efU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rtype_r)) 
                   | ((2U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_attr_type_w)) 
                      << 4U));
            if ((2U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_attr_type_w))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__fcode_r[1U] 
                    = ((0xffffff00U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__fcode_r[1U]) 
                       | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_fail_code_w));
            }
        }
        if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__ctl_acc_w) 
             & (4U == (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r))))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rtype_r 
                = (0x01efU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rtype_r));
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__fcode_r[1U] 
                = (0xffffff00U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__fcode_r[1U]);
        }
        if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_rx_hit_w) 
              >> 5U) & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rx_registering_w))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rtype_r 
                = ((0x01dfU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rtype_r)) 
                   | ((2U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_attr_type_w)) 
                      << 5U));
            if ((2U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_attr_type_w))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__fcode_r[1U] 
                    = ((0xffff00ffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__fcode_r[1U]) 
                       | ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_fail_code_w) 
                          << 8U));
            }
        }
        if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__ctl_acc_w) 
             & (5U == (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r))))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rtype_r 
                = (0x01dfU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rtype_r));
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__fcode_r[1U] 
                = (0xffff00ffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__fcode_r[1U]);
        }
        if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_rx_hit_w) 
              >> 6U) & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rx_registering_w))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rtype_r 
                = ((0x01bfU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rtype_r)) 
                   | ((2U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_attr_type_w)) 
                      << 6U));
            if ((2U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_attr_type_w))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__fcode_r[1U] 
                    = ((0xff00ffffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__fcode_r[1U]) 
                       | ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_fail_code_w) 
                          << 0x00000010U));
            }
        }
        if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__ctl_acc_w) 
             & (6U == (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r))))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rtype_r 
                = (0x01bfU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rtype_r));
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__fcode_r[1U] 
                = (0xff00ffffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__fcode_r[1U]);
        }
        if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_rx_hit_w) 
              >> 7U) & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rx_registering_w))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rtype_r 
                = ((0x017fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rtype_r)) 
                   | ((2U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_attr_type_w)) 
                      << 7U));
            if ((2U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_attr_type_w))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__fcode_r[1U] 
                    = ((0x00ffffffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__fcode_r[1U]) 
                       | ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_fail_code_w) 
                          << 0x00000018U));
            }
        }
        if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__ctl_acc_w) 
             & (7U == (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r))))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rtype_r 
                = (0x017fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rtype_r));
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__fcode_r[1U] 
                = (0x00ffffffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__fcode_r[1U]);
        }
        if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_rx_hit_w) 
              >> 8U) & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rx_registering_w))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rtype_r 
                = ((0x00ffU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rtype_r)) 
                   | ((2U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_attr_type_w)) 
                      << 8U));
            if ((2U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_attr_type_w))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__fcode_r[2U] 
                    = (0x000000ffU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_fail_code_w));
            }
        }
        if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__ctl_acc_w) 
             & (8U == (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r))))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rtype_r 
                = (0x00ffU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rtype_r));
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__fcode_r[2U] = 0U;
        }
        if (((0U == vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tickdiv_r) 
             & (0U != (IData)(vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__timer_ms_r)))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__timer_ms_r 
                = (0x0000ffffU & ((IData)(vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__timer_ms_r) 
                                  - (IData)(1U)));
        }
        if (((IData)(vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_busy_r) 
             & ((IData)(vlSelfRef.milan_datapath__DOT__ctl_tx_mux__DOT__active) 
                & ((IData)(vlSelfRef.milan_datapath__DOT__ctl_tx_mux__DOT__gsel) 
                   & ((~ (IData)(vlSelfRef.milan_datapath__DOT__ctl_tx_mux__DOT__flush_r)) 
                      & (IData)(vlSelfRef.milan_datapath__DOT__ctlh_tx_tready)))))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat_r 
                = (7U & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat_r)));
            if ((7U == (IData)(vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat_r))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_busy_r = 0U;
                vlSelfRef.__Vdly__milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat_r = 0U;
            }
        }
        if (((IData)(vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rx_done_p) 
             & (0U != (IData)(vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__state_r)))) {
            if ((1U == (IData)(vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rx_msg_r))) {
                __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_hit__211__cnt_a 
                    = vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rx_req_cnt_r;
                __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_hit__211__start_a 
                    = vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rx_req_start_r;
                __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_hit__211__our_s 
                    = vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__offset_r;
                __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_hit__211__our_e 
                    = (0x0000ffffU & ((IData)(vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__offset_r) 
                                      + (0x000000ffU 
                                         & (vlSelfRef.milan_datapath__DOT__csr__DOT__maap_ctrl 
                                            >> 8U))));
                __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_hit__211__req_s 
                    = (0x0000ffffU & (IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_hit__211__start_a));
                __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_hit__211__req_e 
                    = (0x0000ffffU & ((IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_hit__211__req_s) 
                                      + (IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_hit__211__cnt_a)));
                vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT____VlemCall_21__conflict_hit 
                    = ((0x91e0f000U == (IData)((__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_hit__211__start_a 
                                                >> 0x10U))) 
                       & ((((IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_hit__211__our_s) 
                            >= (IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_hit__211__req_s)) 
                           & ((IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_hit__211__our_s) 
                              <= (IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_hit__211__req_e))) 
                          | (((IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_hit__211__req_s) 
                              >= (IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_hit__211__our_s)) 
                             & ((IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_hit__211__req_s) 
                                <= (IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_hit__211__our_e)))));
                if (vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT____VlemCall_21__conflict_hit) {
                    if ((1U == (IData)(vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__state_r))) {
                        __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rand_offset__212__cnt 
                            = (0x000000ffU & (vlSelfRef.milan_datapath__DOT__csr__DOT__maap_ctrl 
                                              >> 8U));
                        __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rand_offset__212__rnd 
                            = vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lfsr_r;
                        vlSelfRef.__Vdly__milan_datapath__DOT__maap_conflicts 
                            = (0x000000ffU & ((0x000000ffU 
                                               == (IData)(vlSelfRef.milan_datapath__DOT__maap_conflicts))
                                               ? (IData)(vlSelfRef.milan_datapath__DOT__maap_conflicts)
                                               : ((IData)(1U) 
                                                  + (IData)(vlSelfRef.milan_datapath__DOT__maap_conflicts))));
                        __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rand_offset__212__o 
                            = (0x0000ffffU & ((0xfe00U 
                                               <= (IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rand_offset__212__rnd))
                                               ? ((IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rand_offset__212__rnd) 
                                                  - (IData)(0xfe00U))
                                               : (IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rand_offset__212__rnd)));
                        vlSelfRef.__Vdly__milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__probe_left_r = 3U;
                        vlSelfRef.__Vdly__milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__timer_ms_r 
                            = (0x0000ffffU & ((IData)(0x01f4U) 
                                              + (0x0000007fU 
                                                 & (IData)(vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lfsr_r))));
                        if (((IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rand_offset__212__o) 
                             > (0x0000ffffU & ((IData)(0xfe00U) 
                                               - (IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rand_offset__212__cnt))))) {
                            __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rand_offset__212__o 
                                = (0x0000ffffU & ((IData)(0xfe00U) 
                                                  - (IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rand_offset__212__cnt)));
                        }
                        __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rand_offset__212__Vfuncout 
                            = __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rand_offset__212__o;
                        vlSelfRef.__Vdly__milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__offset_r 
                            = __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rand_offset__212__Vfuncout;
                    } else if ((1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_busy_r)))) {
                        __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__213__cnt_a 
                            = vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rx_req_cnt_r;
                        __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__213__start_a 
                            = vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rx_req_start_r;
                        vlSelfRef.milan_datapath__DOT__maap_defends 
                            = (0x000000ffU & ((0x000000ffU 
                                               == (IData)(vlSelfRef.milan_datapath__DOT__maap_defends))
                                               ? (IData)(vlSelfRef.milan_datapath__DOT__maap_defends)
                                               : ((IData)(1U) 
                                                  + (IData)(vlSelfRef.milan_datapath__DOT__maap_defends))));
                        __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__213__our_s 
                            = vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__offset_r;
                        vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_msg_r = 2U;
                        vlSelfRef.__Vdly__milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_busy_r = 1U;
                        __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__213__our_e 
                            = (0x0000ffffU & ((IData)(vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__offset_r) 
                                              + (0x000000ffU 
                                                 & (vlSelfRef.milan_datapath__DOT__csr__DOT__maap_ctrl 
                                                    >> 8U))));
                        __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__213__req_s 
                            = (0x0000ffffU & (IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__213__start_a));
                        __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__213__req_e 
                            = (0x0000ffffU & ((IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__213__req_s) 
                                              + (IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__213__cnt_a)));
                        if ((((IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__213__our_s) 
                              >= (IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__213__req_s)) 
                             & ((IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__213__our_s) 
                                <= (IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__213__req_e)))) {
                            __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__213__c_s 
                                = __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__213__our_s;
                            __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__213__c_c 
                                = (0x0000ffffU & ((
                                                   ((IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__213__our_e) 
                                                    < (IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__213__req_e))
                                                    ? (IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__213__our_e)
                                                    : (IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__213__req_e)) 
                                                  - (IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__213__our_s)));
                        } else {
                            __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__213__c_s 
                                = __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__213__req_s;
                            __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__213__c_c 
                                = (0x0000ffffU & ((
                                                   ((IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__213__req_e) 
                                                    < (IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__213__our_e))
                                                    ? (IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__213__req_e)
                                                    : (IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__213__our_e)) 
                                                  - (IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__213__req_s)));
                        }
                        vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT____VlemCall_22__conflict_range 
                            = (((IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__213__c_s) 
                                << 0x00000010U) | (IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__213__c_c));
                        vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_conf_start_r 
                            = (vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT____VlemCall_22__conflict_range 
                               >> 0x00000010U);
                        __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__214__cnt_a 
                            = vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rx_req_cnt_r;
                        __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__214__start_a 
                            = vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rx_req_start_r;
                        __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__214__our_s 
                            = vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__offset_r;
                        __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__214__our_e 
                            = (0x0000ffffU & ((IData)(vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__offset_r) 
                                              + (0x000000ffU 
                                                 & (vlSelfRef.milan_datapath__DOT__csr__DOT__maap_ctrl 
                                                    >> 8U))));
                        __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__214__req_s 
                            = (0x0000ffffU & (IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__214__start_a));
                        __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__214__req_e 
                            = (0x0000ffffU & ((IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__214__req_s) 
                                              + (IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__214__cnt_a)));
                        if ((((IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__214__our_s) 
                              >= (IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__214__req_s)) 
                             & ((IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__214__our_s) 
                                <= (IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__214__req_e)))) {
                            __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__214__c_s 
                                = __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__214__our_s;
                            __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__214__c_c 
                                = (0x0000ffffU & ((
                                                   ((IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__214__our_e) 
                                                    < (IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__214__req_e))
                                                    ? (IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__214__our_e)
                                                    : (IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__214__req_e)) 
                                                  - (IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__214__our_s)));
                        } else {
                            __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__214__c_s 
                                = __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__214__req_s;
                            __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__214__c_c 
                                = (0x0000ffffU & ((
                                                   ((IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__214__req_e) 
                                                    < (IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__214__our_e))
                                                    ? (IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__214__req_e)
                                                    : (IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__214__our_e)) 
                                                  - (IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__214__req_s)));
                        }
                        vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT____VlemCall_23__conflict_range 
                            = (((IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__214__c_s) 
                                << 0x00000010U) | (IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__214__c_c));
                        vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_conf_cnt_r 
                            = (0x0000ffffU & vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT____VlemCall_23__conflict_range);
                    }
                }
            } else if (((2U == (IData)(vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rx_msg_r)) 
                        || (3U == (IData)(vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rx_msg_r)))) {
                __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_hit__215__cnt_a 
                    = vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rx_conf_cnt_r;
                __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_hit__215__start_a 
                    = vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rx_conf_start_r;
                __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_hit__215__our_s 
                    = vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__offset_r;
                __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_hit__215__our_e 
                    = (0x0000ffffU & ((IData)(vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__offset_r) 
                                      + (0x000000ffU 
                                         & (vlSelfRef.milan_datapath__DOT__csr__DOT__maap_ctrl 
                                            >> 8U))));
                __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_hit__215__req_s 
                    = (0x0000ffffU & (IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_hit__215__start_a));
                __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_hit__215__req_e 
                    = (0x0000ffffU & ((IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_hit__215__req_s) 
                                      + (IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_hit__215__cnt_a)));
                vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT____VlemCall_24__conflict_hit 
                    = ((0x91e0f000U == (IData)((__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_hit__215__start_a 
                                                >> 0x10U))) 
                       & ((((IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_hit__215__our_s) 
                            >= (IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_hit__215__req_s)) 
                           & ((IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_hit__215__our_s) 
                              <= (IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_hit__215__req_e))) 
                          | (((IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_hit__215__req_s) 
                              >= (IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_hit__215__our_s)) 
                             & ((IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_hit__215__req_s) 
                                <= (IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_hit__215__our_e)))));
                if (vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT____VlemCall_24__conflict_hit) {
                    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rand_offset__216__cnt 
                        = (0x000000ffU & (vlSelfRef.milan_datapath__DOT__csr__DOT__maap_ctrl 
                                          >> 8U));
                    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rand_offset__216__rnd 
                        = vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lfsr_r;
                    vlSelfRef.__Vdly__milan_datapath__DOT__maap_conflicts 
                        = (0x000000ffU & ((0x000000ffU 
                                           == (IData)(vlSelfRef.milan_datapath__DOT__maap_conflicts))
                                           ? (IData)(vlSelfRef.milan_datapath__DOT__maap_conflicts)
                                           : ((IData)(1U) 
                                              + (IData)(vlSelfRef.milan_datapath__DOT__maap_conflicts))));
                    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rand_offset__216__o 
                        = (0x0000ffffU & ((0xfe00U 
                                           <= (IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rand_offset__216__rnd))
                                           ? ((IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rand_offset__216__rnd) 
                                              - (IData)(0xfe00U))
                                           : (IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rand_offset__216__rnd)));
                    vlSelfRef.__Vdly__milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__probe_left_r = 3U;
                    vlSelfRef.__Vdly__milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__timer_ms_r 
                        = (0x0000ffffU & ((IData)(0x01f4U) 
                                          + (0x0000007fU 
                                             & (IData)(vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lfsr_r))));
                    vlSelfRef.__Vdly__milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__state_r = 1U;
                    if (((IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rand_offset__216__o) 
                         > (0x0000ffffU & ((IData)(0xfe00U) 
                                           - (IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rand_offset__216__cnt))))) {
                        __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rand_offset__216__o 
                            = (0x0000ffffU & ((IData)(0xfe00U) 
                                              - (IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rand_offset__216__cnt)));
                    }
                    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rand_offset__216__Vfuncout 
                        = __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rand_offset__216__o;
                    vlSelfRef.__Vdly__milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__offset_r 
                        = __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rand_offset__216__Vfuncout;
                }
            }
        }
        if ((0U == (IData)(vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__state_r))) {
            if ((1U & (~ vlSelfRef.milan_datapath__DOT__csr__DOT__maap_ctrl))) {
                vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__seed_used_r = 0U;
            }
            if ((1U & vlSelfRef.milan_datapath__DOT__csr__DOT__maap_ctrl)) {
                vlSelfRef.__Vdly__milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__offset_r 
                    = vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__new_off_w;
                vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__seed_used_r = 1U;
                vlSelfRef.__Vdly__milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__probe_left_r = 3U;
                vlSelfRef.__Vdly__milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__timer_ms_r 
                    = (0x0000ffffU & ((IData)(0x01f4U) 
                                      + (0x0000007fU 
                                         & (IData)(vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lfsr_r))));
                vlSelfRef.__Vdly__milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__state_r = 1U;
            }
        } else if ((1U == (IData)(vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__state_r))) {
            if ((1U & vlSelfRef.milan_datapath__DOT__csr__DOT__maap_ctrl)) {
                if (((0U == (IData)(vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__timer_ms_r)) 
                     & (~ (IData)(vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_busy_r)))) {
                    vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_msg_r = 1U;
                    vlSelfRef.__Vdly__milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_busy_r = 1U;
                    if ((1U >= (IData)(vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__probe_left_r))) {
                        vlSelfRef.__Vdly__milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__state_r = 2U;
                        vlSelfRef.__Vdly__milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__timer_ms_r 
                            = (0x0000ffffU & ((IData)(0x0bb8U) 
                                              + (0x000007ffU 
                                                 & (IData)(vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lfsr_r))));
                    } else {
                        vlSelfRef.__Vdly__milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__probe_left_r 
                            = (0x000000ffU & ((IData)(vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__probe_left_r) 
                                              - (IData)(1U)));
                        vlSelfRef.__Vdly__milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__timer_ms_r 
                            = (0x0000ffffU & ((IData)(0x01f4U) 
                                              + (0x0000007fU 
                                                 & (IData)(vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lfsr_r))));
                    }
                }
            } else {
                vlSelfRef.__Vdly__milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__state_r = 0U;
            }
        } else if ((2U == (IData)(vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__state_r))) {
            if ((1U & vlSelfRef.milan_datapath__DOT__csr__DOT__maap_ctrl)) {
                if (((0U == (IData)(vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__timer_ms_r)) 
                     & (~ (IData)(vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_busy_r)))) {
                    vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_msg_r = 3U;
                    vlSelfRef.__Vdly__milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_busy_r = 1U;
                    vlSelfRef.__Vdly__milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__timer_ms_r 
                        = (0x0000ffffU & ((IData)(0x0bb8U) 
                                          + (0x000007ffU 
                                             & (IData)(vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lfsr_r))));
                }
            } else {
                vlSelfRef.__Vdly__milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__state_r = 0U;
            }
        } else {
            vlSelfRef.__Vdly__milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__state_r = 0U;
        }
        if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__p_periodic_r) 
             | ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_la_mvrp_w) 
                | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__p_la_mvrp_r)))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__rejoin_pend_r = 1U;
        }
        if ((8U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__st_r))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__st_r = 0U;
        } else if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__st_r))) {
            if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__st_r))) {
                if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__st_r))) {
                    if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__vlan_ev_ready_w) {
                        if ((3U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__ridx_r))) {
                            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__st_r = 0U;
                        } else {
                            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__ridx_r 
                                = (3U & ((IData)(1U) 
                                         + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__ridx_r)));
                            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__st_r = 4U;
                        }
                    }
                } else {
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__ev_code_r = 1U;
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__ev_vid_r 
                        = (0x00000fffU & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__tbl_q_r 
                                          >> 5U));
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__st_r = 7U;
                }
            } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__st_r))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__st_r = 6U;
            } else if ((1U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__active_r) 
                              >> (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__ridx_r)))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__st_r = 5U;
            } else if ((3U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__ridx_r))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__st_r = 0U;
            } else {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__ridx_r 
                    = (3U & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__ridx_r)));
            }
        } else if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__st_r))) {
            if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__st_r))) {
                if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__vlan_ev_ready_w) {
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__st_r = 0U;
                }
            } else if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__op_join_r) {
                if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__found_v_r) {
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__st_r = 0U;
                } else if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__free_v_r) {
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__active_r 
                        = ((IData)(vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__active_r) 
                           | (0x0fU & ((IData)(1U) 
                                       << (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__free_ix_r))));
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__ev_code_r = 0U;
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__ev_vid_r 
                        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__op_vid_r;
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__st_r = 3U;
                } else {
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__st_r = 0U;
                }
            } else if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__found_v_r) 
                        & (1U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__found_cnt_r)))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__active_r 
                    = ((~ ((IData)(1U) << (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__found_ix_r))) 
                       & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__active_r));
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__ev_code_r = 5U;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__ev_vid_r 
                    = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__op_vid_r;
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__st_r = 3U;
            } else {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__st_r = 0U;
            }
        } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__st_r))) {
            if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__chk_v_r) {
                if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__active_r) 
                      >> (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__chk_ix_r)) 
                     & ((0x00000fffU & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__tbl_q_r 
                                        >> 5U)) == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__op_vid_r)))) {
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__found_v_r = 1U;
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__found_ix_r 
                        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__chk_ix_r;
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__found_cnt_r 
                        = (0x0000001fU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__tbl_q_r);
                }
                if ((1U & ((~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__active_r) 
                               >> (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__chk_ix_r))) 
                           & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__free_v_r))))) {
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__free_v_r = 1U;
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__free_ix_r 
                        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__chk_ix_r;
                }
            }
            if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__chk_v_r) 
                 & (3U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__chk_ix_r)))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__st_r = 2U;
            }
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__chk_ix_r 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__scan_ix_r;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__chk_v_r = 1U;
            if ((3U != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__scan_ix_r))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__scan_ix_r 
                    = (3U & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__scan_ix_r)));
            }
        } else {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__chk_v_r = 0U;
            if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__vlan_user_valid_w) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__scan_ix_r = 0U;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__free_v_r = 0U;
                if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__vu_sel_ls_w) {
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__op_join_r 
                        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vsel_join_w;
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__op_vid_r 
                        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__ls_user_vid_w;
                } else {
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__op_join_r 
                        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vsel_join_w;
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__op_vid_r 
                        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tk_user_vid_w;
                }
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__found_v_r = 0U;
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__st_r = 1U;
            } else if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__rejoin_pend_r) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__rejoin_pend_r = 0U;
                if ((0U != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__active_r))) {
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__ridx_r = 0U;
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__st_r = 4U;
                }
            }
        }
        if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vsel_v_w) 
             & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__ls_user_ready_w))) {
            if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vsel_join_w) {
                if ((8U >= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vsel_ix_w))) {
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vj_pend_r 
                        = ((~ ((IData)(1U) << (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vsel_ix_w))) 
                           & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vj_pend_r));
                }
            } else if ((8U >= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vsel_ix_w))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vl_pend_r 
                    = ((~ ((IData)(1U) << (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vsel_ix_w))) 
                       & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vl_pend_r));
            }
        }
        if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__ctl_acc_w) {
            if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_open_r) {
                if ((0x01afU >= (0x000001ffU & ((IData)(0x00000030U) 
                                                * (0x0000000fU 
                                                   & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r)))))) {
                    VL_ASSIGNSEL_WQ(432, 48, (0x000001ffU 
                                              & ((IData)(0x00000030U) 
                                                 * 
                                                 (0x0000000fU 
                                                  & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r)))), vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__da_r, vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_da_r);
                }
                if (((((8U >= (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r))) 
                       && (1U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vl_pend_r) 
                                 >> (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r))))) 
                      & (((0x6bU >= (0x0000007fU & 
                                     ((IData)(0x0000000cU) 
                                      * (0x0000000fU 
                                         & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r)))))
                           ? (0x00000fffU & (((0U == 
                                               (0x0000001fU 
                                                & ((IData)(0x0000000cU) 
                                                   * 
                                                   (0x0000000fU 
                                                    & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r)))))
                                               ? 0U
                                               : (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vl_vid_r
                                                  [
                                                  (((IData)(0x0000000bU) 
                                                    + 
                                                    (0x0000007fU 
                                                     & ((IData)(0x0000000cU) 
                                                        * 
                                                        (0x0000000fU 
                                                         & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r))))) 
                                                   >> 5U)] 
                                                  << 
                                                  ((IData)(0x00000020U) 
                                                   - 
                                                   (0x0000001fU 
                                                    & ((IData)(0x0000000cU) 
                                                       * 
                                                       (0x0000000fU 
                                                        & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r))))))) 
                                             | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vl_vid_r
                                                [(3U 
                                                  & (((IData)(0x0000000cU) 
                                                      * 
                                                      (0x0000000fU 
                                                       & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r))) 
                                                     >> 5U))] 
                                                >> 
                                                (0x0000001fU 
                                                 & ((IData)(0x0000000cU) 
                                                    * 
                                                    (0x0000000fU 
                                                     & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r)))))))
                           : 0U) == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_vid_r))) 
                     & (~ ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vsel_v_w) 
                             & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__ls_user_ready_w)) 
                            & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vsel_join_w))) 
                           & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vsel_ix_w) 
                              == (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r))))))) {
                    if ((8U >= (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r)))) {
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vl_pend_r 
                            = ((~ ((IData)(1U) << (0x0000000fU 
                                                   & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r)))) 
                               & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vl_pend_r));
                    }
                } else {
                    if ((8U >= (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r)))) {
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vj_pend_r 
                            = ((IData)(vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vj_pend_r) 
                               | (0x01ffU & ((IData)(1U) 
                                             << (0x0000000fU 
                                                 & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r)))));
                    }
                    if ((0x6bU >= (0x0000007fU & ((IData)(0x0000000cU) 
                                                  * 
                                                  (0x0000000fU 
                                                   & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r)))))) {
                        VL_ASSIGNSEL_WI(108, 12, (0x0000007fU 
                                                  & ((IData)(0x0000000cU) 
                                                     * 
                                                     (0x0000000fU 
                                                      & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r)))), vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vj_vid_r, vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_vid_r);
                    }
                }
            } else if ((((8U >= (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r))) 
                         && (1U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vj_pend_r) 
                                   >> (0x0000000fU 
                                       & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r))))) 
                        & (~ ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vsel_v_w) 
                                & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__ls_user_ready_w)) 
                               & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vsel_join_w)) 
                              & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vsel_ix_w) 
                                 == (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r))))))) {
                if ((8U >= (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r)))) {
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vj_pend_r 
                        = ((~ ((IData)(1U) << (0x0000000fU 
                                               & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r)))) 
                           & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vj_pend_r));
                }
            } else {
                if ((8U >= (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r)))) {
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vl_pend_r 
                        = ((IData)(vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vl_pend_r) 
                           | (0x01ffU & ((IData)(1U) 
                                         << (0x0000000fU 
                                             & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r)))));
                }
                if ((0x6bU >= (0x0000007fU & ((IData)(0x0000000cU) 
                                              * (0x0000000fU 
                                                 & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r)))))) {
                    VL_ASSIGNSEL_WI(108, 12, (0x0000007fU 
                                              & ((IData)(0x0000000cU) 
                                                 * 
                                                 (0x0000000fU 
                                                  & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r)))), vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vl_vid_r, 
                                    ((0x6bU >= (0x0000007fU 
                                                & ((IData)(0x0000000cU) 
                                                   * 
                                                   (0x0000000fU 
                                                    & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r)))))
                                      ? (0x00000fffU 
                                         & (((0U == 
                                              (0x0000001fU 
                                               & ((IData)(0x0000000cU) 
                                                  * 
                                                  (0x0000000fU 
                                                   & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r)))))
                                              ? 0U : 
                                             (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vid_r
                                              [(((IData)(0x0000000bU) 
                                                 + 
                                                 (0x0000007fU 
                                                  & ((IData)(0x0000000cU) 
                                                     * 
                                                     (0x0000000fU 
                                                      & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r))))) 
                                                >> 5U)] 
                                              << ((IData)(0x00000020U) 
                                                  - 
                                                  (0x0000001fU 
                                                   & ((IData)(0x0000000cU) 
                                                      * 
                                                      (0x0000000fU 
                                                       & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r))))))) 
                                            | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vid_r
                                               [(3U 
                                                 & (((IData)(0x0000000cU) 
                                                     * 
                                                     (0x0000000fU 
                                                      & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r))) 
                                                    >> 5U))] 
                                               >> (0x0000001fU 
                                                   & ((IData)(0x0000000cU) 
                                                      * 
                                                      (0x0000000fU 
                                                       & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r)))))))
                                      : 0U));
                }
            }
        }
        if ((0x011fU >= (0x000001ffU & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__cidx_q2_r) 
                                        << 5U)))) {
            VL_ASSIGNSEL_WI(288, 32, (0x000001ffU & 
                                      ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__cidx_q2_r) 
                                       << 5U)), vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__slope_q_r, 
                            ((0x0000000000010624ULL 
                              < vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__iv_bytes_r)
                              ? 0xffffffffU : (IData)(
                                                      (0x00000001ffffffffULL 
                                                       & (0x000000000000fa00ULL 
                                                          * (QData)((IData)(
                                                                            (0x0001ffffU 
                                                                             & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__iv_bytes_r)))))))));
        }
        if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vsel_v_w) 
             & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tk_user_ready_w))) {
            if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vsel_join_w) {
                if ((8U >= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vsel_ix_w))) {
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vj_pend_r 
                        = ((~ ((IData)(1U) << (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vsel_ix_w))) 
                           & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vj_pend_r));
                }
            } else if ((8U >= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vsel_ix_w))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vl_pend_r 
                    = ((~ ((IData)(1U) << (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vsel_ix_w))) 
                       & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vl_pend_r));
            }
        }
        if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__gate_acc_w) {
            if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_open_r) {
                if (((((8U >= (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r))) 
                       && (1U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vl_pend_r) 
                                 >> (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r))))) 
                      & (((0x6bU >= (0x0000007fU & 
                                     ((IData)(0x0000000cU) 
                                      * (0x0000000fU 
                                         & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r)))))
                           ? (0x00000fffU & (((0U == 
                                               (0x0000001fU 
                                                & ((IData)(0x0000000cU) 
                                                   * 
                                                   (0x0000000fU 
                                                    & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r)))))
                                               ? 0U
                                               : (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vl_vid_r
                                                  [
                                                  (((IData)(0x0000000bU) 
                                                    + 
                                                    (0x0000007fU 
                                                     & ((IData)(0x0000000cU) 
                                                        * 
                                                        (0x0000000fU 
                                                         & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r))))) 
                                                   >> 5U)] 
                                                  << 
                                                  ((IData)(0x00000020U) 
                                                   - 
                                                   (0x0000001fU 
                                                    & ((IData)(0x0000000cU) 
                                                       * 
                                                       (0x0000000fU 
                                                        & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r))))))) 
                                             | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vl_vid_r
                                                [(3U 
                                                  & (((IData)(0x0000000cU) 
                                                      * 
                                                      (0x0000000fU 
                                                       & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r))) 
                                                     >> 5U))] 
                                                >> 
                                                (0x0000001fU 
                                                 & ((IData)(0x0000000cU) 
                                                    * 
                                                    (0x0000000fU 
                                                     & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r)))))))
                           : 0U) == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_vid_r))) 
                     & (~ ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vsel_v_w) 
                             & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tk_user_ready_w)) 
                            & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vsel_join_w))) 
                           & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vsel_ix_w) 
                              == (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r))))))) {
                    if ((8U >= (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r)))) {
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vl_pend_r 
                            = ((~ ((IData)(1U) << (0x0000000fU 
                                                   & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r)))) 
                               & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vl_pend_r));
                    }
                } else {
                    if ((8U >= (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r)))) {
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vj_pend_r 
                            = ((IData)(vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vj_pend_r) 
                               | (0x01ffU & ((IData)(1U) 
                                             << (0x0000000fU 
                                                 & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r)))));
                    }
                    if ((0x6bU >= (0x0000007fU & ((IData)(0x0000000cU) 
                                                  * 
                                                  (0x0000000fU 
                                                   & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r)))))) {
                        VL_ASSIGNSEL_WI(108, 12, (0x0000007fU 
                                                  & ((IData)(0x0000000cU) 
                                                     * 
                                                     (0x0000000fU 
                                                      & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r)))), vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vj_vid_r, vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_vid_r);
                    }
                }
            } else if ((((8U >= (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r))) 
                         && (1U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vj_pend_r) 
                                   >> (0x0000000fU 
                                       & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r))))) 
                        & (~ ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vsel_v_w) 
                                & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tk_user_ready_w)) 
                               & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vsel_join_w)) 
                              & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vsel_ix_w) 
                                 == (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r))))))) {
                if ((8U >= (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r)))) {
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vj_pend_r 
                        = ((~ ((IData)(1U) << (0x0000000fU 
                                               & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r)))) 
                           & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vj_pend_r));
                }
            } else {
                if ((8U >= (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r)))) {
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vl_pend_r 
                        = ((IData)(vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vl_pend_r) 
                           | (0x01ffU & ((IData)(1U) 
                                         << (0x0000000fU 
                                             & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r)))));
                }
                if ((0x6bU >= (0x0000007fU & ((IData)(0x0000000cU) 
                                              * (0x0000000fU 
                                                 & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r)))))) {
                    VL_ASSIGNSEL_WI(108, 12, (0x0000007fU 
                                              & ((IData)(0x0000000cU) 
                                                 * 
                                                 (0x0000000fU 
                                                  & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r)))), vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vl_vid_r, 
                                    ((0x6bU >= (0x0000007fU 
                                                & ((IData)(0x0000000cU) 
                                                   * 
                                                   (0x0000000fU 
                                                    & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r)))))
                                      ? (0x00000fffU 
                                         & (((0U == 
                                              (0x0000001fU 
                                               & ((IData)(0x0000000cU) 
                                                  * 
                                                  (0x0000000fU 
                                                   & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r)))))
                                              ? 0U : 
                                             (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vid_r
                                              [(((IData)(0x0000000bU) 
                                                 + 
                                                 (0x0000007fU 
                                                  & ((IData)(0x0000000cU) 
                                                     * 
                                                     (0x0000000fU 
                                                      & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r))))) 
                                                >> 5U)] 
                                              << ((IData)(0x00000020U) 
                                                  - 
                                                  (0x0000001fU 
                                                   & ((IData)(0x0000000cU) 
                                                      * 
                                                      (0x0000000fU 
                                                       & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r))))))) 
                                            | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vid_r
                                               [(3U 
                                                 & (((IData)(0x0000000cU) 
                                                     * 
                                                     (0x0000000fU 
                                                      & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r))) 
                                                    >> 5U))] 
                                               >> (0x0000001fU 
                                                   & ((IData)(0x0000000cU) 
                                                      * 
                                                      (0x0000000fU 
                                                       & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r)))))))
                                      : 0U));
                }
            }
        }
        if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_rx_hit_w) 
             & (((0U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_mrp_event_w)) 
                 | (1U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_mrp_event_w))) 
                | (3U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_mrp_event_w))))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_val_r 
                = ((0x0003fffcU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_val_r) 
                   | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_fourpacked_w));
        }
        if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__gate_acc_w) 
              & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_open_r)) 
             & (0U == (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r))))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_val_r 
                = (0x0003fffcU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_val_r);
        }
        if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_rx_hit_w) 
              >> 1U) & (((0U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_mrp_event_w)) 
                         | (1U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_mrp_event_w))) 
                        | (3U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_mrp_event_w))))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_val_r 
                = ((0x0003fff3U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_val_r) 
                   | ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_fourpacked_w) 
                      << 2U));
        }
        if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__gate_acc_w) 
              & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_open_r)) 
             & (1U == (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r))))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_val_r 
                = (0x0003fff3U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_val_r);
        }
        if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_rx_hit_w) 
              >> 2U) & (((0U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_mrp_event_w)) 
                         | (1U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_mrp_event_w))) 
                        | (3U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_mrp_event_w))))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_val_r 
                = ((0x0003ffcfU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_val_r) 
                   | ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_fourpacked_w) 
                      << 4U));
        }
        if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__gate_acc_w) 
              & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_open_r)) 
             & (2U == (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r))))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_val_r 
                = (0x0003ffcfU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_val_r);
        }
        if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_rx_hit_w) 
              >> 3U) & (((0U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_mrp_event_w)) 
                         | (1U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_mrp_event_w))) 
                        | (3U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_mrp_event_w))))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_val_r 
                = ((0x0003ff3fU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_val_r) 
                   | ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_fourpacked_w) 
                      << 6U));
        }
        if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__gate_acc_w) 
              & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_open_r)) 
             & (3U == (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r))))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_val_r 
                = (0x0003ff3fU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_val_r);
        }
        if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_rx_hit_w) 
              >> 4U) & (((0U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_mrp_event_w)) 
                         | (1U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_mrp_event_w))) 
                        | (3U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_mrp_event_w))))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_val_r 
                = ((0x0003fcffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_val_r) 
                   | ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_fourpacked_w) 
                      << 8U));
        }
        if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__gate_acc_w) 
              & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_open_r)) 
             & (4U == (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r))))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_val_r 
                = (0x0003fcffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_val_r);
        }
        if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_rx_hit_w) 
              >> 5U) & (((0U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_mrp_event_w)) 
                         | (1U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_mrp_event_w))) 
                        | (3U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_mrp_event_w))))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_val_r 
                = ((0x0003f3ffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_val_r) 
                   | ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_fourpacked_w) 
                      << 0x0000000aU));
        }
        if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__gate_acc_w) 
              & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_open_r)) 
             & (5U == (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r))))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_val_r 
                = (0x0003f3ffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_val_r);
        }
        if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_rx_hit_w) 
              >> 6U) & (((0U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_mrp_event_w)) 
                         | (1U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_mrp_event_w))) 
                        | (3U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_mrp_event_w))))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_val_r 
                = ((0x0003cfffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_val_r) 
                   | ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_fourpacked_w) 
                      << 0x0000000cU));
        }
        if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__gate_acc_w) 
              & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_open_r)) 
             & (6U == (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r))))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_val_r 
                = (0x0003cfffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_val_r);
        }
        if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_rx_hit_w) 
              >> 7U) & (((0U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_mrp_event_w)) 
                         | (1U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_mrp_event_w))) 
                        | (3U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_mrp_event_w))))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_val_r 
                = ((0x00033fffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_val_r) 
                   | ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_fourpacked_w) 
                      << 0x0000000eU));
        }
        if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__gate_acc_w) 
              & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_open_r)) 
             & (7U == (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r))))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_val_r 
                = (0x00033fffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_val_r);
        }
        if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_rx_hit_w) 
              >> 8U) & (((0U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_mrp_event_w)) 
                         | (1U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_mrp_event_w))) 
                        | (3U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_mrp_event_w))))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_val_r 
                = ((0x0000ffffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_val_r) 
                   | ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_fourpacked_w) 
                      << 0x00000010U));
        }
        if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__gate_acc_w) 
              & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_open_r)) 
             & (8U == (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r))))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_val_r 
                = (0x0000ffffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_val_r);
        }
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__sp_ctrl_rdata_r 
            = ((0U == (0x000000ffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__hb_addr_r))
                ? vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__ctrl_scratch_r
                : ((1U == (0x000000ffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__hb_addr_r))
                    ? ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__fail_r) 
                         << 3U) | ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__done_r) 
                                   << 2U)) | (((IData)(vlSelfRef.milan_datapath__DOT__pp_restore_busy_w) 
                                               << 1U) 
                                              | (IData)(vlSelfRef.milan_datapath__DOT____Vcellinp__pp_shadow__enable_i)))
                    : 0U));
        if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__maap_rsp_live_w) 
              & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__maap_rel_r))) 
             & (IData)(vlSelfRef.milan_datapath__DOT__pp_maap_shim__DOT__rsp_ok_r))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__gp_valid_r = 1U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__gp_src_r 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__maap_src_r;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__gp_da_r 
                = vlSelfRef.milan_datapath__DOT__pp_maap_shim__DOT__rsp_da_r;
        }
        if (((6U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__state_r)) 
             & (0U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_code_r)))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__gp_valid_r = 0U;
        }
        if (vlSelfRef.milan_datapath__DOT__csr__DOT__rd_pend2) {
            vlSelfRef.milan_datapath__DOT__csr__DOT__r_data 
                = ((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__strm_hit_q)
                    ? vlSelfRef.milan_datapath__DOT__csr__DOT__strm_mux_q
                    : ((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_in_window_q)
                        ? ((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__live_hit_q)
                            ? vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux_q
                            : vlSelfRef.milan_datapath__DOT__csr__DOT__shadow_qq)
                        : 0U));
        } else if (vlSelfRef.milan_datapath__DOT__csr__DOT__rds_done_w) {
            vlSelfRef.milan_datapath__DOT__csr__DOT__r_data 
                = ((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rds_dir_r)
                    ? vlSelfRef.milan_datapath__DOT__tctx_rd_data_w
                    : vlSelfRef.milan_datapath__DOT__lctx_rd_data_w);
        }
        if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__done_r) 
             & ((5U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__state_r)) 
                | ((6U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__state_r)) 
                   | ((9U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__state_r)) 
                      | ((0x0dU == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__state_r)) 
                         | (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__gnt_r) 
                             & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__nvm_req_w)) 
                            | ((3U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__state_r)) 
                               | ((7U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__state_r)) 
                                  | ((0x0aU == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__state_r)) 
                                     | (0x0eU == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__state_r)))))))))))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__done_seen_r = 1U;
        }
        if ((8U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__state_r))) {
            if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__state_r))) {
                if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__state_r))) {
                    if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__state_r))) {
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__done_seen_r = 0U;
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__state_r = 0U;
                    } else if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__err_r) {
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__err_r = 1U;
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__state_r = 0x0fU;
                    } else if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__done_r) 
                                | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__done_seen_r))) {
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__done_seen_r = 0U;
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__state_r = 0x0fU;
                    }
                } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__state_r))) {
                    if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__err_r) {
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__err_r = 1U;
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__state_r = 0x0fU;
                    } else if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__nvm_rvalid_w) 
                                & (3U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__hs_r)))) {
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__bcnt_r 
                            = (0x0000ffffU & ((IData)(1U) 
                                              + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__bcnt_r)));
                        if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__bcnt_r) 
                             == (0x0000ffffU & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__plen_r) 
                                                - (IData)(1U))))) {
                            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__state_r = 0x0eU;
                        }
                    }
                } else if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__err_r) {
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__err_r = 1U;
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__state_r = 0x0fU;
                } else if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__gnt_r) {
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__bcnt_r = 0U;
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__state_r = 0x0dU;
                }
            } else if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__state_r))) {
                if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__state_r))) {
                    if ((3U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__hs_r))) {
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__hidx_r 
                            = (7U & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__hidx_r)));
                        if ((7U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__hidx_r))) {
                            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__bcnt_r = 0U;
                            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__state_r 
                                = ((0U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__plen_r))
                                    ? 0x0fU : 0x0cU);
                        }
                    }
                } else if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__err_r) {
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__err_r = 1U;
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__state_r = 0x0fU;
                } else if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__done_r) 
                            | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__done_seen_r))) {
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__done_seen_r = 0U;
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__plen_r 
                        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__hdr_plen_w;
                    if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__hdr_ok_w) {
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__hidx_r = 0U;
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__state_r = 0x0bU;
                    } else {
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__err_r = 1U;
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__state_r = 0x0fU;
                    }
                }
            } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__state_r))) {
                if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__err_r) {
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__err_r = 1U;
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__state_r = 0x0fU;
                } else {
                    if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__nvm_rvalid_w) {
                        vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__hdr_r__v0 
                            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__nvm_rdata_w;
                        vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__hdr_r__v0 
                            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__hidx_r;
                        vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__hdr_r__v0 = 1U;
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__hidx_r 
                            = (7U & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__hidx_r)));
                        if ((7U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__hidx_r))) {
                            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__state_r = 0x0aU;
                        }
                    }
                    if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__done_r) 
                         & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__nvm_rvalid_w) 
                               & (7U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__hidx_r)))))) {
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__err_r = 1U;
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__state_r = 0x0fU;
                    }
                }
            } else if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__err_r) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__err_r = 1U;
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__state_r = 0x0fU;
            } else if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__gnt_r) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__hidx_r = 0U;
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__state_r = 9U;
            }
        } else if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__state_r))) {
            if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__state_r))) {
                if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__state_r))) {
                    if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__err_r) {
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__err_r = 1U;
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__state_r = 0x0fU;
                    } else if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__done_r) 
                                | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__done_seen_r))) {
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__done_seen_r = 0U;
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__state_r = 0x0fU;
                    }
                } else if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__err_r) {
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__err_r = 1U;
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__state_r = 0x0fU;
                } else if (((0x0eU == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__hs_r)) 
                            & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__nvm_wready_w))) {
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__bcnt_r 
                        = (0x0000ffffU & ((IData)(1U) 
                                          + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__bcnt_r)));
                    if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__bcnt_r) 
                         == (0x0000ffffU & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__plen_r) 
                                            - (IData)(1U))))) {
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__state_r = 7U;
                    }
                }
            } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__state_r))) {
                if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__err_r) {
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__err_r = 1U;
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__state_r = 0x0fU;
                } else if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__nvm_wready_w) {
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__hidx_r 
                        = (7U & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__hidx_r)));
                    if ((7U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__hidx_r))) {
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__bcnt_r = 0U;
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__state_r 
                            = ((0U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__plen_r))
                                ? 7U : 6U);
                    }
                }
            } else if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__err_r) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__err_r = 1U;
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__state_r = 0x0fU;
            } else if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__gnt_r) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__hidx_r = 0U;
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__state_r = 5U;
            }
        } else if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__state_r))) {
            if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__state_r))) {
                if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__err_r) {
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__err_r = 1U;
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__state_r = 0x0fU;
                } else if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__done_r) 
                            | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__done_seen_r))) {
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__done_seen_r = 0U;
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__state_r = 4U;
                }
            } else if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__err_r) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__err_r = 1U;
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__state_r = 0x0fU;
            } else if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__gnt_r) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__state_r = 3U;
            }
        } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__state_r))) {
            if ((0x0eU == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__hs_r))) {
                vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__hdr_r__v1 
                    = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__nvm_wdata_w;
                vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__hdr_r__v1 
                    = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__hidx_r;
                vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__hdr_r__v1 = 1U;
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__hidx_r 
                    = (7U & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__hidx_r)));
                if ((7U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__hidx_r))) {
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__plen_r 
                        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__hdr_plen_w;
                    if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__hdr_ok_w) {
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__state_r = 2U;
                    } else {
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__err_r = 1U;
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__state_r = 0x0fU;
                    }
                }
            }
        } else {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__err_r = 0U;
            if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__nvm_req_w) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__rec_r 
                    = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__nvm_record_id_w;
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__hidx_r = 0U;
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__bcnt_r = 0U;
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__done_seen_r = 0U;
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__state_r 
                    = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__nvm_we_w)
                        ? 1U : 8U);
            }
        }
        if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__lstn_act_settle_w) {
            if ((0x023fU >= (0x000003ffU & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__sink_r) 
                                            << 6U)))) {
                VL_ASSIGNSEL_WQ(576, 64, (0x000003ffU 
                                          & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__sink_r) 
                                             << 6U)), vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__bound_sid_r, vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__sid_f_r);
            }
        }
        if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__lstn_disc_disarm_w) {
            if ((0x023fU >= (0x000003ffU & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__sink_r) 
                                            << 6U)))) {
                VL_ASSIGNSEL_WQ(576, 64, (0x000003ffU 
                                          & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__sink_r) 
                                             << 6U)), vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__bound_sid_r, 0ULL);
            }
        }
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__bound_q_r 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__bound_r;
        if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__snap_st_r))) {
            if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__snap_st_r))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__csr__DOT__snap_st_r = 0U;
            } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__snap_st_r))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__csr__DOT__snap_st_r = 0U;
            } else if ((0U != (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__snap_cyc_r))) {
                vlSelfRef.milan_datapath__DOT__csr__DOT__snap_cyc_r 
                    = (3U & ((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__snap_cyc_r) 
                             - (IData)(1U)));
            } else if (((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__snap_dir_r)
                         ? (IData)(vlSelfRef.milan_datapath__DOT__tctx_rd_valid_w)
                         : (IData)(vlSelfRef.milan_datapath__DOT__lctx_rd_valid_w))) {
                if (vlSelfRef.milan_datapath__DOT__csr__DOT__snap_dir_r) {
                    __VdlyVal__milan_datapath__DOT__csr__DOT__snap_shadow_r__v0 
                        = vlSelfRef.milan_datapath__DOT__tctx_rd_data_w;
                    vlSelfRef.__VdlySet__milan_datapath__DOT__csr__DOT__snap_shadow_r__v0 = 1U;
                    vlSelfRef.milan_datapath__DOT__csr__DOT__snap_rden_r = 0U;
                    vlSelfRef.__Vdly__milan_datapath__DOT__csr__DOT__snap_req_r = 0U;
                    vlSelfRef.__Vdly__milan_datapath__DOT__csr__DOT__snap_st_r = 1U;
                    __VdlyVal__milan_datapath__DOT__csr__DOT__snap_shadow_r__v1 
                        = (((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__snap_srp9_w) 
                            << 0x00000013U) | ((((2U 
                                                  & (((IData)(vlSelfRef.milan_datapath__DOT__aaf_stream_en_w) 
                                                      >> 
                                                      (7U 
                                                       & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__snap_idx_r))) 
                                                     << 1U)) 
                                                 | (1U 
                                                    & ((((((2U 
                                                            & ((vlSelfRef.milan_datapath__DOT__csr__DOT__acmp_lobs 
                                                                | (vlSelfRef.milan_datapath__DOT__csr__DOT__lwsrp_ctrl 
                                                                   & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__adm_admitted_w) 
                                                                      >> 7U))) 
                                                               << 1U)) 
                                                           | (1U 
                                                              & (vlSelfRef.milan_datapath__DOT__csr__DOT__acmp_lobs 
                                                                 | (vlSelfRef.milan_datapath__DOT__csr__DOT__lwsrp_ctrl 
                                                                    & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__adm_admitted_w) 
                                                                       >> 6U))))) 
                                                          << 6U) 
                                                         | (((2U 
                                                              & ((vlSelfRef.milan_datapath__DOT__csr__DOT__acmp_lobs 
                                                                  | (vlSelfRef.milan_datapath__DOT__csr__DOT__lwsrp_ctrl 
                                                                     & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__adm_admitted_w) 
                                                                        >> 5U))) 
                                                                 << 1U)) 
                                                             | (1U 
                                                                & (vlSelfRef.milan_datapath__DOT__csr__DOT__acmp_lobs 
                                                                   | (vlSelfRef.milan_datapath__DOT__csr__DOT__lwsrp_ctrl 
                                                                      & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__adm_admitted_w) 
                                                                         >> 4U))))) 
                                                            << 4U)) 
                                                        | ((((2U 
                                                              & ((vlSelfRef.milan_datapath__DOT__csr__DOT__acmp_lobs 
                                                                  | (vlSelfRef.milan_datapath__DOT__csr__DOT__lwsrp_ctrl 
                                                                     & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__adm_admitted_w) 
                                                                        >> 3U))) 
                                                                 << 1U)) 
                                                             | (1U 
                                                                & (vlSelfRef.milan_datapath__DOT__csr__DOT__acmp_lobs 
                                                                   | (vlSelfRef.milan_datapath__DOT__csr__DOT__lwsrp_ctrl 
                                                                      & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__adm_admitted_w) 
                                                                         >> 2U))))) 
                                                            << 2U) 
                                                           | ((2U 
                                                               & ((vlSelfRef.milan_datapath__DOT__csr__DOT__acmp_lobs 
                                                                   | (vlSelfRef.milan_datapath__DOT__csr__DOT__lwsrp_ctrl 
                                                                      & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__adm_admitted_w) 
                                                                         >> 1U))) 
                                                                  << 1U)) 
                                                              | (1U 
                                                                 & (vlSelfRef.milan_datapath__DOT__csr__DOT__acmp_lobs 
                                                                    | ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp_listener_ready) 
                                                                       & vlSelfRef.milan_datapath__DOT__csr__DOT__lwsrp_ctrl)))))) 
                                                       >> 
                                                       (7U 
                                                        & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__snap_idx_r))))) 
                                                << 2U) 
                                               | (2U 
                                                  & (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__declaring_r) 
                                                      >> 
                                                      (7U 
                                                       & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__snap_idx_r))) 
                                                     << 1U))));
                    vlSelfRef.__VdlySet__milan_datapath__DOT__csr__DOT__snap_shadow_r__v1 = 1U;
                } else {
                    if ((0U == (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__snap_wi_r))) {
                        vlSelfRef.__Vdly__milan_datapath__DOT__csr__DOT__snap_m8_r 
                            = vlSelfRef.milan_datapath__DOT__lctx_rd_data_w;
                    } else if ((0x0bU == (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__snap_wi_r))) {
                        __VdlyVal__milan_datapath__DOT__csr__DOT__snap_shadow_r__v2 
                            = vlSelfRef.milan_datapath__DOT__lctx_rd_data_w;
                        vlSelfRef.__VdlySet__milan_datapath__DOT__csr__DOT__snap_shadow_r__v2 = 1U;
                        __VdlyVal__milan_datapath__DOT__csr__DOT__snap_shadow_r__v3 
                            = (((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__snap_srp9_w) 
                                << 0x00000013U) | (
                                                   (((0x000001feU 
                                                      & (vlSelfRef.milan_datapath__DOT__csr__DOT__snap_m8_r 
                                                         >> 0x0000000dU)) 
                                                     | (1U 
                                                        & (vlSelfRef.milan_datapath__DOT__csr__DOT__snap_m8_r 
                                                           >> 0x0cU))) 
                                                    << 0x0000000aU) 
                                                   | ((((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__acmp_fresh_r)
                                                         ? (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__acmp_status_q_r)
                                                         : 0U) 
                                                       << 5U) 
                                                      | ((((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__acmp_fresh_r)
                                                            ? (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__acmp_probing_q_r)
                                                            : 0U) 
                                                          << 3U) 
                                                         | ((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__acmp_fresh_r)
                                                             ? (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__acmp_state_q_r)
                                                             : 0U)))));
                    } else if ((0x0bU >= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__snap_wi_r))) {
                        __VdlyVal__milan_datapath__DOT__csr__DOT__snap_shadow_r__v4 
                            = vlSelfRef.milan_datapath__DOT__lctx_rd_data_w;
                        __VdlyDim0__milan_datapath__DOT__csr__DOT__snap_shadow_r__v4 
                            = vlSelfRef.milan_datapath__DOT__csr__DOT__snap_wi_r;
                        vlSelfRef.__VdlySet__milan_datapath__DOT__csr__DOT__snap_shadow_r__v4 = 1U;
                    }
                    if ((0x0bU == (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__snap_wi_r))) {
                        vlSelfRef.milan_datapath__DOT__csr__DOT__snap_rden_r = 0U;
                        vlSelfRef.__Vdly__milan_datapath__DOT__csr__DOT__snap_req_r = 0U;
                        vlSelfRef.__Vdly__milan_datapath__DOT__csr__DOT__snap_st_r = 1U;
                    } else {
                        vlSelfRef.__Vdly__milan_datapath__DOT__csr__DOT__snap_wi_r 
                            = (0x0000000fU & ((IData)(1U) 
                                              + (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__snap_wi_r)));
                        vlSelfRef.milan_datapath__DOT__csr__DOT__snap_word_r 
                            = ((0U == (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__snap_wi_r))
                                ? 0x00000010U : ((0x0aU 
                                                  == (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__snap_wi_r))
                                                  ? 0x0000000bU
                                                  : 
                                                 (0x0000001fU 
                                                  & ((IData)(1U) 
                                                     + (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__snap_word_r)))));
                        vlSelfRef.milan_datapath__DOT__csr__DOT__snap_cyc_r = 3U;
                    }
                }
            }
        } else if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__snap_st_r))) {
            if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__snap_st_r))) {
                if (((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__snap_dir_r)
                      ? ((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__snap_dir_r) 
                         & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__snap_req_r))
                      : ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_244) 
                         & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__snap_req_r)))) {
                    vlSelfRef.milan_datapath__DOT__csr__DOT__snap_rden_r = 1U;
                    vlSelfRef.__Vdly__milan_datapath__DOT__csr__DOT__snap_wi_r = 0U;
                    vlSelfRef.milan_datapath__DOT__csr__DOT__snap_cyc_r = 3U;
                    vlSelfRef.milan_datapath__DOT__csr__DOT__snap_word_r 
                        = ((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__snap_dir_r)
                            ? 5U : 8U);
                    vlSelfRef.__Vdly__milan_datapath__DOT__csr__DOT__snap_st_r = 4U;
                }
            } else if ((1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rds_busy_r)))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__csr__DOT__snap_req_r = 1U;
                vlSelfRef.__Vdly__milan_datapath__DOT__csr__DOT__snap_st_r = 3U;
            }
        } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__snap_st_r))) {
            vlSelfRef.milan_datapath__DOT__csr__DOT__snap_busy_r = 0U;
            vlSelfRef.__Vdly__milan_datapath__DOT__csr__DOT__snap_st_r = 0U;
        } else if (((IData)(vlSelfRef.s_axi_awready) 
                    & (vlSelfRef.s_axi_wdata & ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_243) 
                                                & (0x0804U 
                                                   == (IData)(vlSelfRef.s_axi_awaddr)))))) {
            vlSelfRef.milan_datapath__DOT__csr__DOT__snap_busy_r = 1U;
            vlSelfRef.milan_datapath__DOT__csr__DOT__snap_dir_r 
                = vlSelfRef.milan_datapath__DOT__csr__DOT__strm_dir_r;
            vlSelfRef.milan_datapath__DOT__csr__DOT__snap_idx_r 
                = vlSelfRef.milan_datapath__DOT__csr__DOT__strm_idx_r;
            if ((8U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__strm_idx_r))) {
                if ((0U == (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__strm_idx_r))) {
                    if (vlSelfRef.milan_datapath__DOT__csr__DOT__strm_dir_r) {
                        __VdlyVal__milan_datapath__DOT__csr__DOT__snap_shadow_r__v5 
                            = ((0x0ff80000U & (vlSelfRef.milan_datapath__DOT____Vcellinp__csr__i_lwsrp_status 
                                               << 0x00000013U)) 
                               | ((((IData)(vlSelfRef.milan_datapath__DOT__aaf_gate) 
                                    << 3U) | (4U & 
                                              (vlSelfRef.milan_datapath__DOT__csr__DOT__acmp_lobs 
                                               << 2U))) 
                                  | (2U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__declaring_r) 
                                           << 1U))));
                        vlSelfRef.__VdlySet__milan_datapath__DOT__csr__DOT__snap_shadow_r__v5 = 1U;
                        __VdlyVal__milan_datapath__DOT__csr__DOT__snap_shadow_r__v16 
                            = vlSelfRef.milan_datapath__DOT__aaf_frames_w;
                    } else {
                        __VdlyVal__milan_datapath__DOT__csr__DOT__snap_shadow_r__v17 
                            = ((0x0ff80000U & (vlSelfRef.milan_datapath__DOT____Vcellinp__csr__i_lwsrp_status 
                                               << 0x00000013U)) 
                               | ((0x00000400U & (vlSelfRef.milan_datapath__DOT____Vcellinp__csr__i_avtprx_stat 
                                                  << 0x0000000aU)) 
                                  | ((0x000003e0U & 
                                      (vlSelfRef.milan_datapath__DOT____Vcellinp__csr__i_acmpl_state 
                                       >> 3U)) | ((0x00000018U 
                                                   & (vlSelfRef.milan_datapath__DOT____Vcellinp__csr__i_acmpl_state 
                                                      >> 0x0000000aU)) 
                                                  | (7U 
                                                     & vlSelfRef.milan_datapath__DOT____Vcellinp__csr__i_acmpl_state)))));
                        vlSelfRef.__VdlySet__milan_datapath__DOT__csr__DOT__snap_shadow_r__v17 = 1U;
                        __VdlyVal__milan_datapath__DOT__csr__DOT__snap_shadow_r__v18 
                            = vlSelfRef.milan_datapath__DOT____Vcellinp__csr__i_avtprx_cnt10[0U];
                        __VdlyVal__milan_datapath__DOT__csr__DOT__snap_shadow_r__v19 
                            = vlSelfRef.milan_datapath__DOT____Vcellinp__csr__i_avtprx_cnt10[1U];
                        __VdlyVal__milan_datapath__DOT__csr__DOT__snap_shadow_r__v20 
                            = vlSelfRef.milan_datapath__DOT____Vcellinp__csr__i_avtprx_cnt10[2U];
                        __VdlyVal__milan_datapath__DOT__csr__DOT__snap_shadow_r__v21 
                            = vlSelfRef.milan_datapath__DOT____Vcellinp__csr__i_avtprx_cnt10[3U];
                        __VdlyVal__milan_datapath__DOT__csr__DOT__snap_shadow_r__v22 
                            = vlSelfRef.milan_datapath__DOT____Vcellinp__csr__i_avtprx_cnt10[4U];
                        __VdlyVal__milan_datapath__DOT__csr__DOT__snap_shadow_r__v23 
                            = vlSelfRef.milan_datapath__DOT____Vcellinp__csr__i_avtprx_cnt10[5U];
                        __VdlyVal__milan_datapath__DOT__csr__DOT__snap_shadow_r__v24 
                            = vlSelfRef.milan_datapath__DOT____Vcellinp__csr__i_avtprx_cnt10[6U];
                        __VdlyVal__milan_datapath__DOT__csr__DOT__snap_shadow_r__v25 
                            = vlSelfRef.milan_datapath__DOT____Vcellinp__csr__i_avtprx_cnt10[7U];
                        __VdlyVal__milan_datapath__DOT__csr__DOT__snap_shadow_r__v26 
                            = vlSelfRef.milan_datapath__DOT____Vcellinp__csr__i_avtprx_cnt10[8U];
                        __VdlyVal__milan_datapath__DOT__csr__DOT__snap_shadow_r__v27 
                            = vlSelfRef.milan_datapath__DOT____Vcellinp__csr__i_avtprx_cnt10[9U];
                        __VdlyVal__milan_datapath__DOT__csr__DOT__snap_shadow_r__v28 
                            = vlSelfRef.milan_datapath__DOT____Vcellinp__csr__i_pcmrx_cnt;
                    }
                    vlSelfRef.__Vdly__milan_datapath__DOT__csr__DOT__snap_st_r = 1U;
                } else {
                    if (vlSelfRef.milan_datapath__DOT__csr__DOT__strm_dir_r) {
                        vlSelfRef.__VdlySet__milan_datapath__DOT__csr__DOT__snap_shadow_r__v29 = 1U;
                    }
                    vlSelfRef.__Vdly__milan_datapath__DOT__csr__DOT__snap_st_r = 2U;
                }
            } else {
                vlSelfRef.__VdlySet__milan_datapath__DOT__csr__DOT__snap_shadow_r__v39 = 1U;
                vlSelfRef.__Vdly__milan_datapath__DOT__csr__DOT__snap_st_r = 1U;
                vlSelfRef.__VdlySet__milan_datapath__DOT__csr__DOT__snap_shadow_r__v40 = 1U;
            }
        }
        if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__push_msrp_w) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__cnt_msrp_r 
                = (0x0000000fU & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__cnt_msrp_r)));
        }
        if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__push_mvrp_w) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__cnt_mvrp_r 
                = (0x0000000fU & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__cnt_mvrp_r)));
        }
        if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__wr_valid_w) {
            if ((0x0cU != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__st_r))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__waddr_r 
                    = (0x000007ffU & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__waddr_r)));
            }
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__bidx_r 
                = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__last_byte_w)
                    ? 0U : (0x0000003fU & ((IData)(1U) 
                                           + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__bidx_r))));
        }
        if ((8U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__st_r))) {
            if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__st_r))) {
                if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__st_r))) {
                    if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__st_r))) {
                        if ((0x00000010U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__gnt_r))) {
                            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__st_r = 0U;
                        }
                    } else {
                        if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__cur_app_r) {
                            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__cnt_mvrp_r = 0U;
                        } else {
                            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__cnt_msrp_r = 0U;
                        }
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__la_pend_r 
                            = ((~ ((IData)(1U) << (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__cur_app_r))) 
                               & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__la_pend_r));
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__st_r = 0x0fU;
                    }
                } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__st_r))) {
                    if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__last_byte_w) {
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__st_r = 0x0eU;
                    }
                } else if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__last_byte_w) {
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__st_r 
                        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__close_for_pdu_r)
                            ? 0x0dU : 6U);
                }
            } else if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__st_r))) {
                if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__st_r))) {
                    if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__last_byte_w) {
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__msg_open_r = 0U;
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__st_r 
                            = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__cur_app_r)
                                ? ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__close_for_pdu_r)
                                    ? 0x0dU : 6U) : 0x0cU);
                    }
                } else if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__last_byte_w) {
                    if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__hold_valid_r) {
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__hold_valid_r = 0U;
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_type_r 
                            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__hold_type_r;
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_first_r[0U] 
                            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__hold_val_r[0U];
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_first_r[1U] 
                            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__hold_val_r[1U];
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_first_r[2U] 
                            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__hold_val_r[2U];
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_first_r[3U] 
                            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__hold_val_r[3U];
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_first_r[4U] 
                            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__hold_val_r[4U];
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_first_r[5U] 
                            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__hold_val_r[5U];
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_first_r[6U] 
                            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__hold_val_r[6U];
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_first_r[7U] 
                            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__hold_val_r[7U];
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_first_r[8U] 
                            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__hold_val_r[8U];
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_last_r[0U] 
                            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__hold_val_r[0U];
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_last_r[1U] 
                            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__hold_val_r[1U];
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_last_r[2U] 
                            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__hold_val_r[2U];
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_last_r[3U] 
                            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__hold_val_r[3U];
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_last_r[4U] 
                            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__hold_val_r[4U];
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_last_r[5U] 
                            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__hold_val_r[5U];
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_last_r[6U] 
                            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__hold_val_r[6U];
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_last_r[7U] 
                            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__hold_val_r[7U];
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_last_r[8U] 
                            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__hold_val_r[8U];
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_ev_r 
                            = ((0x0000000ffffffff8ULL 
                                & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_ev_r) 
                               | (IData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__hold_ev_r)));
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_fp_r 
                            = ((0x00fffffcU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_fp_r) 
                               | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__hold_fp_r));
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_len_r = 1U;
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__st_r 
                            = (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__rd_idx_r) 
                                < (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__drain_n_r))
                                ? 3U : 5U);
                    } else {
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_open_r = 0U;
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__close_for_pdu_r = 1U;
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__st_r = 0x0bU;
                    }
                }
            } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__st_r))) {
                if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__last_byte_w) {
                    if (((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__cur_app_r)) 
                         & (3U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_type_r)))) {
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__st_r = 0x0aU;
                    } else if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__hold_valid_r) {
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__hold_valid_r = 0U;
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_type_r 
                            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__hold_type_r;
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_first_r[0U] 
                            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__hold_val_r[0U];
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_first_r[1U] 
                            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__hold_val_r[1U];
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_first_r[2U] 
                            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__hold_val_r[2U];
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_first_r[3U] 
                            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__hold_val_r[3U];
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_first_r[4U] 
                            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__hold_val_r[4U];
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_first_r[5U] 
                            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__hold_val_r[5U];
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_first_r[6U] 
                            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__hold_val_r[6U];
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_first_r[7U] 
                            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__hold_val_r[7U];
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_first_r[8U] 
                            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__hold_val_r[8U];
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_last_r[0U] 
                            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__hold_val_r[0U];
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_last_r[1U] 
                            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__hold_val_r[1U];
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_last_r[2U] 
                            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__hold_val_r[2U];
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_last_r[3U] 
                            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__hold_val_r[3U];
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_last_r[4U] 
                            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__hold_val_r[4U];
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_last_r[5U] 
                            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__hold_val_r[5U];
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_last_r[6U] 
                            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__hold_val_r[6U];
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_last_r[7U] 
                            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__hold_val_r[7U];
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_last_r[8U] 
                            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__hold_val_r[8U];
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_ev_r 
                            = ((0x0000000ffffffff8ULL 
                                & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_ev_r) 
                               | (IData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__hold_ev_r)));
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_fp_r 
                            = ((0x00fffffcU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_fp_r) 
                               | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__hold_fp_r));
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_len_r = 1U;
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__st_r 
                            = (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__rd_idx_r) 
                                < (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__drain_n_r))
                                ? 3U : 5U);
                    } else {
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_open_r = 0U;
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__close_for_pdu_r = 1U;
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__st_r = 0x0bU;
                    }
                }
            } else if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__last_byte_w) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__st_r = 9U;
            }
        } else if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__st_r))) {
            if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__st_r))) {
                if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__st_r))) {
                    if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__last_byte_w) {
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__first_vec_r = 0U;
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__st_r = 8U;
                    }
                } else {
                    if ((2U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__bidx_r))) {
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__ll_addr_r 
                            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__waddr_r;
                    }
                    if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__last_byte_w) {
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__msg_open_r = 1U;
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__msg_type_r 
                            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_type_r;
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__st_r = 7U;
                    }
                }
            } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__st_r))) {
                if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__msg_open_r) {
                    if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__msg_type_r) 
                         != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_type_r))) {
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__close_for_pdu_r = 0U;
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__st_r = 0x0bU;
                    } else {
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__st_r = 7U;
                    }
                } else {
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__st_r = 6U;
                }
            } else {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__rd_idx_r 
                    = (0x0000000fU & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__rd_idx_r)));
                if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__open_w) 
                     | ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_open_r) 
                        & (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_type_r) 
                            == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__cap_type_w)) 
                           & (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__cur_app_r)
                                ? ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_180) 
                                   & ((0x0000ffffU 
                                       & ((IData)(1U) 
                                          + vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_last_r[8U])) 
                                      == (0x0000ffffU 
                                          & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__cap_val_w[8U])))
                                : (((1U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_type_r)) 
                                    | (2U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_type_r)))
                                    ? ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_375) 
                                       & ((0U == ((
                                                   (((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__cap_val_w[0U] 
                                                      ^ vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_last_r[0U]) 
                                                     | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__cap_val_w[1U] 
                                                        ^ vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_last_r[1U])) 
                                                    | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__cap_val_w[2U] 
                                                       ^ vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_last_r[2U])) 
                                                   | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__cap_val_w[3U] 
                                                      ^ vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_last_r[3U])) 
                                                  | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__cap_val_w[4U] 
                                                     ^ vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_last_r[4U]))) 
                                          & ((0x0000ffffffffffffULL 
                                              & (1ULL 
                                                 + 
                                                 (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_last_r[6U])) 
                                                   << 0x00000020U) 
                                                  | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_last_r[5U]))))) 
                                             == (0x0000ffffffffffffULL 
                                                 & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__cap_val_w[6U])) 
                                                     << 0x00000020U) 
                                                    | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__cap_val_w[5U])))))))
                                    : ((3U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_type_r))
                                        ? ((0U == (
                                                   ((((((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__cap_val_w[0U] 
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
                                                   | ((0x0000ffffU 
                                                       & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__cap_val_w[6U]) 
                                                      ^ 
                                                      (0x0000ffffU 
                                                       & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_last_r[6U])))) 
                                           & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_375))
                                        : ((4U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_type_r)) 
                                           & ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_180) 
                                              & (((0x000000ffU 
                                                   & ((IData)(1U) 
                                                      + vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_last_r[8U])) 
                                                  == 
                                                  (0x000000ffU 
                                                   & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__cap_val_w[8U])) 
                                                 & ((0x000000ffU 
                                                     & ((IData)(1U) 
                                                        + 
                                                        ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_last_r[8U] 
                                                          << 0x00000018U) 
                                                         | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_last_r[8U] 
                                                            >> 8U)))) 
                                                    == 
                                                    (0x000000ffU 
                                                     & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__cap_val_w[8U] 
                                                        >> 8U))))))))) 
                              & (0x0cU > (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_len_r))))))) {
                    if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__open_w) {
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_open_r = 1U;
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_type_r 
                            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__cap_type_w;
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_first_r[0U] 
                            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__cap_val_w[0U];
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_first_r[1U] 
                            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__cap_val_w[1U];
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_first_r[2U] 
                            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__cap_val_w[2U];
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_first_r[3U] 
                            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__cap_val_w[3U];
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_first_r[4U] 
                            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__cap_val_w[4U];
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_first_r[5U] 
                            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__cap_val_w[5U];
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_first_r[6U] 
                            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__cap_val_w[6U];
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_first_r[7U] 
                            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__cap_val_w[7U];
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_first_r[8U] 
                            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__cap_val_w[8U];
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_last_r[0U] 
                            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__cap_val_w[0U];
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_last_r[1U] 
                            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__cap_val_w[1U];
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_last_r[2U] 
                            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__cap_val_w[2U];
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_last_r[3U] 
                            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__cap_val_w[3U];
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_last_r[4U] 
                            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__cap_val_w[4U];
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_last_r[5U] 
                            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__cap_val_w[5U];
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_last_r[6U] 
                            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__cap_val_w[6U];
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_last_r[7U] 
                            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__cap_val_w[7U];
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_last_r[8U] 
                            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__cap_val_w[8U];
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_ev_r 
                            = ((0x0000000ffffffff8ULL 
                                & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_ev_r) 
                               | (IData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__cap_ev_w)));
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_fp_r 
                            = ((0x00fffffcU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_fp_r) 
                               | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__cap_fp_w));
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_len_r = 1U;
                    } else {
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_last_r[0U] 
                            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__cap_val_w[0U];
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_last_r[1U] 
                            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__cap_val_w[1U];
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_last_r[2U] 
                            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__cap_val_w[2U];
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_last_r[3U] 
                            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__cap_val_w[3U];
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_last_r[4U] 
                            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__cap_val_w[4U];
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_last_r[5U] 
                            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__cap_val_w[5U];
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_last_r[6U] 
                            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__cap_val_w[6U];
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_last_r[7U] 
                            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__cap_val_w[7U];
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_last_r[8U] 
                            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__cap_val_w[8U];
                        if ((0x23U >= (0x0000003fU 
                                       & ((IData)(3U) 
                                          * (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_len_r))))) {
                            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_ev_r 
                                = (((~ (7ULL << (0x0000003fU 
                                                 & ((IData)(3U) 
                                                    * (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_len_r))))) 
                                    & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_ev_r) 
                                   | (0x0000000fffffffffULL 
                                      & ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__cap_ev_w)) 
                                         << (0x0000003fU 
                                             & ((IData)(3U) 
                                                * (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_len_r))))));
                        }
                        if ((0x17U >= (0x0000001fU 
                                       & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_len_r) 
                                          << 1U)))) {
                            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_fp_r 
                                = (((~ ((IData)(3U) 
                                        << (0x0000001fU 
                                            & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_len_r) 
                                               << 1U)))) 
                                    & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_fp_r) 
                                   | (0x00ffffffU & 
                                      ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__cap_fp_w) 
                                       << (0x0000001fU 
                                           & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_len_r) 
                                              << 1U)))));
                        }
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_len_r 
                            = (0x0000000fU & ((IData)(1U) 
                                              + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_len_r)));
                    }
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__st_r 
                        = (((0x0000000fU & ((IData)(1U) 
                                            + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__rd_idx_r))) 
                            < (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__drain_n_r))
                            ? 3U : 5U);
                } else {
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__hold_type_r 
                        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__cap_type_w;
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__hold_ev_r 
                        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__cap_ev_w;
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__hold_fp_r 
                        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__cap_fp_w;
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__hold_val_r[0U] 
                        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__cap_val_w[0U];
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__hold_val_r[1U] 
                        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__cap_val_w[1U];
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__hold_val_r[2U] 
                        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__cap_val_w[2U];
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__hold_val_r[3U] 
                        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__cap_val_w[3U];
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__hold_val_r[4U] 
                        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__cap_val_w[4U];
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__hold_val_r[5U] 
                        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__cap_val_w[5U];
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__hold_val_r[6U] 
                        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__cap_val_w[6U];
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__hold_val_r[7U] 
                        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__cap_val_w[7U];
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__hold_val_r[8U] 
                        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__cap_val_w[8U];
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__hold_valid_r = 1U;
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__st_r = 5U;
                }
            }
        } else if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__st_r))) {
            if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__st_r))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__st_r = 4U;
            } else if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__last_byte_w) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__st_r = 3U;
            }
        } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__st_r))) {
            if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_txs_gnt_w) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__bidx_r = 0U;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__slot_r 
                    = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__alloc_slot_r;
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__st_r = 2U;
            }
        } else if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__start0_w) 
                    | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__start1_w))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__waddr_r = 0U;
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__bidx_r = 0U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__cur_app_r 
                = (1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__start0_w)));
            if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__start0_w) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__drain_n_r 
                    = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__cnt_msrp_r;
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__join_pend_r 
                    = (2U & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__join_pend_r));
            } else {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__drain_n_r 
                    = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__cnt_mvrp_r;
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__join_pend_r 
                    = (1U & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__join_pend_r));
            }
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__rd_idx_r = 0U;
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__msg_open_r = 0U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__first_vec_r = 1U;
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_open_r = 0U;
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__hold_valid_r = 0U;
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__st_r = 1U;
        } else {
            if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__join_pend_r) 
                 & (0U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__cnt_msrp_r)))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__join_pend_r 
                    = (2U & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__join_pend_r));
            }
            if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__join_pend_r) 
                  >> 1U) & (0U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__cnt_mvrp_r)))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__join_pend_r 
                    = (1U & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__join_pend_r));
            }
        }
        if ((1U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__enc_join_r) 
                   & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__start0_w))))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__join_pend_r 
                = (1U | (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__join_pend_r));
        }
        if ((IData)((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__enc_join_r) 
                      >> 1U) & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__start1_w))))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__join_pend_r 
                = (2U | (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__join_pend_r));
        }
        if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__enc_la_r))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__la_pend_r 
                = (1U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__la_pend_r));
        }
        if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__enc_la_r))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__la_pend_r 
                = (2U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__la_pend_r));
        }
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__sp_snap_rdata_r 
            = ((0x00000020U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__hb_addr_r)
                ? ((0x00000010U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__hb_addr_r)
                    ? 0U : ((8U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__hb_addr_r)
                             ? 0U : ((4U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__hb_addr_r)
                                      ? ((2U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__hb_addr_r)
                                          ? 0U : ((1U 
                                                   & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__hb_addr_r)
                                                   ? 0U
                                                   : (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__fcode_r)))
                                      : ((2U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__hb_addr_r)
                                          ? ((1U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__hb_addr_r)
                                              ? (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__rerr_cnt_r) 
                                                  << 0x00000010U) 
                                                 | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__lanewr_r))
                                              : (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__frame_len_r) 
                                                  << 0x0000000aU) 
                                                 | (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__status_r) 
                                                     << 5U) 
                                                    | (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__fault_r) 
                                                        << 1U) 
                                                       | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__img_valid_r)))))
                                          : ((1U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__hb_addr_r)
                                              ? (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__drop_cnt_r) 
                                                  << 0x00000010U) 
                                                 | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__miss_cnt_r))
                                              : (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cmd_cnt_r) 
                                                  << 0x00000010U) 
                                                 | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__resp_cnt_r)))))))
                : ((0x00000010U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__hb_addr_r)
                    ? ((8U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__hb_addr_r)
                        ? ((4U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__hb_addr_r)
                            ? ((2U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__hb_addr_r)
                                ? ((1U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__hb_addr_r)
                                    ? vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__adv_st_r[0U]
                                    : (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__gslope_r[0U] 
                                       & (- (IData)(
                                                    (1U 
                                                     & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__adm_admitted_w))))))
                                : ((1U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__hb_addr_r)
                                    ? (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxf_drop_r) 
                                        << 0x00000010U) 
                                       | (0x000000ffU 
                                          & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_snk_fail_code_w[0U]))
                                    : (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__bound_r) 
                                        << 0x00000018U) 
                                       | (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_drop_r) 
                                           << 8U) | 
                                          (0x000000ffU 
                                           & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__svc_drop_r))))))
                            : ((2U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__hb_addr_r)
                                ? ((1U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__hb_addr_r)
                                    ? ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__arb_gnt_cnt_w[2U] 
                                        << 0x00000010U) 
                                       | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__arb_gnt_cnt_w[2U] 
                                          >> 0x00000010U))
                                    : ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__arb_gnt_cnt_w[1U] 
                                        << 0x00000010U) 
                                       | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__arb_gnt_cnt_w[1U] 
                                          >> 0x00000010U)))
                                : ((1U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__hb_addr_r)
                                    ? ((0x00000038U 
                                        & (VL_COUNTONES_I((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__0__KET____DOT__u_rx_slots__DOT__free_mask_w)) 
                                           << 3U)) 
                                       | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__txs_free_w))
                                    : (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__arm_drop_r) 
                                        << 0x00000010U) 
                                       | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__mrp_drop_w)))))
                        : ((0x011fU >= (0x000000e0U 
                                        & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__hb_addr_r 
                                           << 5U)))
                            ? vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__lat_r
                           [(7U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__hb_addr_r)]
                            : 0U)) : ((8U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__hb_addr_r)
                                       ? ((4U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__hb_addr_r)
                                           ? ((2U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__hb_addr_r)
                                               ? ((1U 
                                                   & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__hb_addr_r)
                                                   ? 
                                                  (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__valid_r) 
                                                    << 0x00000018U) 
                                                   | ((((2U 
                                                         & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__ff_valid_w)) 
                                                            << 1U)) 
                                                        | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__barrier_pend_r)) 
                                                       << 0x00000010U) 
                                                      | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_trace__DOT__wr_count_r)))
                                                   : 
                                                  (((((0x0000000cU 
                                                       & ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__fourpack_r 
                                                           >> 0x0000000cU) 
                                                          & ((- (IData)(
                                                                        (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rec_valid_r) 
                                                                          >> 7U) 
                                                                         & ((1U 
                                                                             == 
                                                                             (0x0000000fU 
                                                                              & (IData)(
                                                                                (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_r 
                                                                                >> 0x0000001cU)))) 
                                                                            | ((2U 
                                                                                == 
                                                                                (0x0000000fU 
                                                                                & (IData)(
                                                                                (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_r 
                                                                                >> 0x0000001cU)))) 
                                                                               | ((3U 
                                                                                == 
                                                                                (0x0000000fU 
                                                                                & (IData)(
                                                                                (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_r 
                                                                                >> 0x0000001cU)))) 
                                                                                | ((4U 
                                                                                == 
                                                                                (0x0000000fU 
                                                                                & (IData)(
                                                                                (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_r 
                                                                                >> 0x0000001cU)))) 
                                                                                | ((5U 
                                                                                == 
                                                                                (0x0000000fU 
                                                                                & (IData)(
                                                                                (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_r 
                                                                                >> 0x0000001cU)))) 
                                                                                | ((9U 
                                                                                == 
                                                                                (0x0000000fU 
                                                                                & (IData)(
                                                                                (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_r 
                                                                                >> 0x0000001cU)))) 
                                                                                | (0x0aU 
                                                                                == 
                                                                                (0x0000000fU 
                                                                                & (IData)(
                                                                                (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_r 
                                                                                >> 0x0000001cU))))))))))))) 
                                                             << 2U))) 
                                                      | (3U 
                                                         & ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__fourpack_r 
                                                             >> 0x0000000cU) 
                                                            & (- (IData)(
                                                                         (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rec_valid_r) 
                                                                           >> 6U) 
                                                                          & ((1U 
                                                                              == 
                                                                              (0x0000000fU 
                                                                               & (IData)(
                                                                                (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_r 
                                                                                >> 0x00000018U)))) 
                                                                             | ((2U 
                                                                                == 
                                                                                (0x0000000fU 
                                                                                & (IData)(
                                                                                (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_r 
                                                                                >> 0x00000018U)))) 
                                                                                | ((3U 
                                                                                == 
                                                                                (0x0000000fU 
                                                                                & (IData)(
                                                                                (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_r 
                                                                                >> 0x00000018U)))) 
                                                                                | ((4U 
                                                                                == 
                                                                                (0x0000000fU 
                                                                                & (IData)(
                                                                                (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_r 
                                                                                >> 0x00000018U)))) 
                                                                                | ((5U 
                                                                                == 
                                                                                (0x0000000fU 
                                                                                & (IData)(
                                                                                (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_r 
                                                                                >> 0x00000018U)))) 
                                                                                | ((9U 
                                                                                == 
                                                                                (0x0000000fU 
                                                                                & (IData)(
                                                                                (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_r 
                                                                                >> 0x00000018U)))) 
                                                                                | (0x0aU 
                                                                                == 
                                                                                (0x0000000fU 
                                                                                & (IData)(
                                                                                (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_r 
                                                                                >> 0x00000018U)))))))))))))))) 
                                                     << 0x0000001cU) 
                                                    | (((0x0000000cU 
                                                         & ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__fourpack_r 
                                                             >> 8U) 
                                                            & ((- (IData)(
                                                                          (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rec_valid_r) 
                                                                            >> 5U) 
                                                                           & ((1U 
                                                                               == 
                                                                               (0x0000000fU 
                                                                                & (IData)(
                                                                                (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_r 
                                                                                >> 0x00000014U)))) 
                                                                              | ((2U 
                                                                                == 
                                                                                (0x0000000fU 
                                                                                & (IData)(
                                                                                (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_r 
                                                                                >> 0x00000014U)))) 
                                                                                | ((3U 
                                                                                == 
                                                                                (0x0000000fU 
                                                                                & (IData)(
                                                                                (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_r 
                                                                                >> 0x00000014U)))) 
                                                                                | ((4U 
                                                                                == 
                                                                                (0x0000000fU 
                                                                                & (IData)(
                                                                                (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_r 
                                                                                >> 0x00000014U)))) 
                                                                                | ((5U 
                                                                                == 
                                                                                (0x0000000fU 
                                                                                & (IData)(
                                                                                (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_r 
                                                                                >> 0x00000014U)))) 
                                                                                | ((9U 
                                                                                == 
                                                                                (0x0000000fU 
                                                                                & (IData)(
                                                                                (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_r 
                                                                                >> 0x00000014U)))) 
                                                                                | (0x0aU 
                                                                                == 
                                                                                (0x0000000fU 
                                                                                & (IData)(
                                                                                (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_r 
                                                                                >> 0x00000014U))))))))))))) 
                                                               << 2U))) 
                                                        | (3U 
                                                           & ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__fourpack_r 
                                                               >> 8U) 
                                                              & (- (IData)(
                                                                           (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rec_valid_r) 
                                                                             >> 4U) 
                                                                            & ((1U 
                                                                                == 
                                                                                (0x0000000fU 
                                                                                & (IData)(
                                                                                (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_r 
                                                                                >> 0x00000010U)))) 
                                                                               | ((2U 
                                                                                == 
                                                                                (0x0000000fU 
                                                                                & (IData)(
                                                                                (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_r 
                                                                                >> 0x00000010U)))) 
                                                                                | ((3U 
                                                                                == 
                                                                                (0x0000000fU 
                                                                                & (IData)(
                                                                                (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_r 
                                                                                >> 0x00000010U)))) 
                                                                                | ((4U 
                                                                                == 
                                                                                (0x0000000fU 
                                                                                & (IData)(
                                                                                (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_r 
                                                                                >> 0x00000010U)))) 
                                                                                | ((5U 
                                                                                == 
                                                                                (0x0000000fU 
                                                                                & (IData)(
                                                                                (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_r 
                                                                                >> 0x00000010U)))) 
                                                                                | ((9U 
                                                                                == 
                                                                                (0x0000000fU 
                                                                                & (IData)(
                                                                                (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_r 
                                                                                >> 0x00000010U)))) 
                                                                                | (0x0aU 
                                                                                == 
                                                                                (0x0000000fU 
                                                                                & (IData)(
                                                                                (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_r 
                                                                                >> 0x00000010U)))))))))))))))) 
                                                       << 0x00000018U)) 
                                                   | ((((0x0000000cU 
                                                         & ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__fourpack_r 
                                                             >> 4U) 
                                                            & ((- (IData)(
                                                                          (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rec_valid_r) 
                                                                            >> 3U) 
                                                                           & ((1U 
                                                                               == 
                                                                               (0x0000000fU 
                                                                                & (IData)(
                                                                                (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_r 
                                                                                >> 0x0000000cU)))) 
                                                                              | ((2U 
                                                                                == 
                                                                                (0x0000000fU 
                                                                                & (IData)(
                                                                                (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_r 
                                                                                >> 0x0000000cU)))) 
                                                                                | ((3U 
                                                                                == 
                                                                                (0x0000000fU 
                                                                                & (IData)(
                                                                                (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_r 
                                                                                >> 0x0000000cU)))) 
                                                                                | ((4U 
                                                                                == 
                                                                                (0x0000000fU 
                                                                                & (IData)(
                                                                                (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_r 
                                                                                >> 0x0000000cU)))) 
                                                                                | ((5U 
                                                                                == 
                                                                                (0x0000000fU 
                                                                                & (IData)(
                                                                                (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_r 
                                                                                >> 0x0000000cU)))) 
                                                                                | ((9U 
                                                                                == 
                                                                                (0x0000000fU 
                                                                                & (IData)(
                                                                                (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_r 
                                                                                >> 0x0000000cU)))) 
                                                                                | (0x0aU 
                                                                                == 
                                                                                (0x0000000fU 
                                                                                & (IData)(
                                                                                (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_r 
                                                                                >> 0x0000000cU))))))))))))) 
                                                               << 2U))) 
                                                        | (3U 
                                                           & ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__fourpack_r 
                                                               >> 4U) 
                                                              & (- (IData)(
                                                                           (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rec_valid_r) 
                                                                             >> 2U) 
                                                                            & ((1U 
                                                                                == 
                                                                                (0x0000000fU 
                                                                                & (IData)(
                                                                                (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_r 
                                                                                >> 8U)))) 
                                                                               | ((2U 
                                                                                == 
                                                                                (0x0000000fU 
                                                                                & (IData)(
                                                                                (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_r 
                                                                                >> 8U)))) 
                                                                                | ((3U 
                                                                                == 
                                                                                (0x0000000fU 
                                                                                & (IData)(
                                                                                (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_r 
                                                                                >> 8U)))) 
                                                                                | ((4U 
                                                                                == 
                                                                                (0x0000000fU 
                                                                                & (IData)(
                                                                                (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_r 
                                                                                >> 8U)))) 
                                                                                | ((5U 
                                                                                == 
                                                                                (0x0000000fU 
                                                                                & (IData)(
                                                                                (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_r 
                                                                                >> 8U)))) 
                                                                                | ((9U 
                                                                                == 
                                                                                (0x0000000fU 
                                                                                & (IData)(
                                                                                (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_r 
                                                                                >> 8U)))) 
                                                                                | (0x0aU 
                                                                                == 
                                                                                (0x0000000fU 
                                                                                & (IData)(
                                                                                (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_r 
                                                                                >> 8U)))))))))))))))) 
                                                       << 0x00000014U) 
                                                      | ((0x000c0000U 
                                                          & ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__fourpack_r 
                                                              << 0x00000010U) 
                                                             & ((- (IData)(
                                                                           (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rec_valid_r) 
                                                                             >> 1U) 
                                                                            & ((1U 
                                                                                == 
                                                                                (0x0000000fU 
                                                                                & (IData)(
                                                                                (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_r 
                                                                                >> 4U)))) 
                                                                               | ((2U 
                                                                                == 
                                                                                (0x0000000fU 
                                                                                & (IData)(
                                                                                (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_r 
                                                                                >> 4U)))) 
                                                                                | ((3U 
                                                                                == 
                                                                                (0x0000000fU 
                                                                                & (IData)(
                                                                                (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_r 
                                                                                >> 4U)))) 
                                                                                | ((4U 
                                                                                == 
                                                                                (0x0000000fU 
                                                                                & (IData)(
                                                                                (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_r 
                                                                                >> 4U)))) 
                                                                                | ((5U 
                                                                                == 
                                                                                (0x0000000fU 
                                                                                & (IData)(
                                                                                (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_r 
                                                                                >> 4U)))) 
                                                                                | ((9U 
                                                                                == 
                                                                                (0x0000000fU 
                                                                                & (IData)(
                                                                                (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_r 
                                                                                >> 4U)))) 
                                                                                | (0x0aU 
                                                                                == 
                                                                                (0x0000000fU 
                                                                                & (IData)(
                                                                                (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_r 
                                                                                >> 4U))))))))))))) 
                                                                << 0x00000012U))) 
                                                         | ((0x00030000U 
                                                             & ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__fourpack_r 
                                                                 & (- (IData)(
                                                                              ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rec_valid_r) 
                                                                               & ((1U 
                                                                                == 
                                                                                (0x0000000fU 
                                                                                & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_r))) 
                                                                                | ((2U 
                                                                                == 
                                                                                (0x0000000fU 
                                                                                & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_r))) 
                                                                                | ((3U 
                                                                                == 
                                                                                (0x0000000fU 
                                                                                & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_r))) 
                                                                                | ((4U 
                                                                                == 
                                                                                (0x0000000fU 
                                                                                & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_r))) 
                                                                                | ((5U 
                                                                                == 
                                                                                (0x0000000fU 
                                                                                & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_r))) 
                                                                                | ((9U 
                                                                                == 
                                                                                (0x0000000fU 
                                                                                & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_r))) 
                                                                                | (0x0aU 
                                                                                == 
                                                                                (0x0000000fU 
                                                                                & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_r))))))))))))) 
                                                                << 0x00000010U)) 
                                                            | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__active_r))))))
                                               : ((1U 
                                                   & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__hb_addr_r)
                                                   ? 
                                                  ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_tk_decl_state_w 
                                                    << 0x00000010U) 
                                                   | (0x0000ffffU 
                                                      & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_out_w))
                                                   : 
                                                  (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__adm_admitted_w) 
                                                    << 0x00000018U) 
                                                   | ((((((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_301) 
                                                          << 3U) 
                                                         | ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_302) 
                                                            << 2U)) 
                                                        | (((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_303) 
                                                            << 1U) 
                                                           | (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_304))) 
                                                       << 0x00000014U) 
                                                      | ((((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_305) 
                                                           << 0x00000013U) 
                                                          | ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_306) 
                                                             << 0x00000012U)) 
                                                         | (((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_307) 
                                                             << 0x00000011U) 
                                                            | (((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_308) 
                                                                << 0x00000010U) 
                                                               | (0x0000ffffU 
                                                                  & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_tk_reg_state_w))))))))
                                           : ((2U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__hb_addr_r)
                                               ? ((1U 
                                                   & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__hb_addr_r)
                                                   ? vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__sum_r
                                                   : 
                                                  ((0x00070000U 
                                                    & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_domain__DOT__decl_prio_r) 
                                                       << 0x00000010U)) 
                                                   | (0x00000fffU 
                                                      & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_domain__DOT__decl_vid_r))))
                                               : ((1U 
                                                   & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__hb_addr_r)
                                                   ? 
                                                  (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__aecp_stall_r) 
                                                    << 0x00000010U) 
                                                   | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__hdr_drop_r))
                                                   : 
                                                  (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__adp_stall_r) 
                                                    << 0x00000010U) 
                                                   | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__acmp_stall_r)))))
                                       : ((4U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__hb_addr_r)
                                           ? ((2U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__hb_addr_r)
                                               ? ((1U 
                                                   & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__hb_addr_r)
                                                   ? 
                                                  ((((0x0000ff00U 
                                                      & (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_adp_q__DOT__out_valid_r) 
                                                          + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_adp_q__DOT__cnt_r)) 
                                                         << 8U)) 
                                                     | (0x000000ffU 
                                                        & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_acmp_q__DOT__out_valid_r) 
                                                           + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_acmp_q__DOT__cnt_r)))) 
                                                    << 0x00000010U) 
                                                   | (0x0000ff00U 
                                                      & (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__out_valid_r) 
                                                          + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__cnt_r)) 
                                                         << 8U)))
                                                   : 
                                                  (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__cnt_len_r) 
                                                    << 0x00000010U) 
                                                   | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__0__KET____DOT__u_rx_slots__DOT__ovr_cnt_r)))
                                               : ((1U 
                                                   & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__hb_addr_r)
                                                   ? 
                                                  (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__cnt_sub_r) 
                                                    << 0x00000010U) 
                                                   | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__cnt_ver_r))
                                                   : 
                                                  (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__cnt_da_r) 
                                                    << 0x00000010U) 
                                                   | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__cnt_et_r))))
                                           : ((2U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__hb_addr_r)
                                               ? ((1U 
                                                   & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__hb_addr_r)
                                                   ? 
                                                  ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__alarm_r) 
                                                     << 5U) 
                                                    | (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__over_r) 
                                                        << 4U) 
                                                       | ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_domain__DOT__adopted_r) 
                                                          << 3U))) 
                                                   | (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__seeded_r) 
                                                       << 2U) 
                                                      | (((IData)(vlSelfRef.milan_datapath__DOT__eff_link_w) 
                                                          << 1U) 
                                                         | (IData)(vlSelfRef.milan_datapath__DOT____Vcellinp__pp_shadow__enable_i))))
                                                   : vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__now_ms_r)
                                               : ((1U 
                                                   & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__hb_addr_r)
                                                   ? 0x09090404U
                                                   : 0x4b4c5050U))))));
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__p2_d_r 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__p1_d_r;
        if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__v_mrp_valid_w) {
            if ((0x0cU == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_mrp_strip__DOT__hdr_idx_r))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_mrp_strip__DOT__et_r 
                    = ((0x00ffU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_mrp_strip__DOT__et_r)) 
                       | ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__od_data_r) 
                          << 8U));
            }
            if ((0x0dU == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_mrp_strip__DOT__hdr_idx_r))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_mrp_strip__DOT__et_r 
                    = ((0xff00U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_mrp_strip__DOT__et_r)) 
                       | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__od_data_r));
            }
            if ((0x0eU != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_mrp_strip__DOT__hdr_idx_r))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_mrp_strip__DOT__hdr_idx_r 
                    = (0x0000000fU & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_mrp_strip__DOT__hdr_idx_r)));
            }
            if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__v_mrp_last_w) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_mrp_strip__DOT__hdr_idx_r = 0U;
            }
        }
        if (vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__s_ok_w) {
            if (vlSelfRef.milan_datapath__DOT__dpkt_pcm_tlast_w) {
                vlSelfRef.milan_datapath__DOT__render_setpoint__DOT____VlemCond_4 = 0U;
            } else {
                __Vfunc_milan_datapath__DOT__render_setpoint__DOT__chwrap__228__chans 
                    = vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__c_in_w;
                __Vfunc_milan_datapath__DOT__render_setpoint__DOT__chwrap__228__ch 
                    = vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__ch1_w;
                vlSelfRef.milan_datapath__DOT__render_setpoint__DOT____VlemCall_3__chwrap 
                    = (((0x0000000fU & ((IData)(1U) 
                                        + (IData)(__Vfunc_milan_datapath__DOT__render_setpoint__DOT__chwrap__228__ch))) 
                        == (IData)(__Vfunc_milan_datapath__DOT__render_setpoint__DOT__chwrap__228__chans))
                        ? 0U : (0x0000000fU & ((IData)(1U) 
                                               + (IData)(__Vfunc_milan_datapath__DOT__render_setpoint__DOT__chwrap__228__ch))));
                vlSelfRef.milan_datapath__DOT__render_setpoint__DOT____VlemCond_4 
                    = vlSelfRef.milan_datapath__DOT__render_setpoint__DOT____VlemCall_3__chwrap;
            }
            vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__chpos_r 
                = vlSelfRef.milan_datapath__DOT__render_setpoint__DOT____VlemCond_4;
        }
        vlSelfRef.milan_datapath__DOT__csr__DOT__i2spb_clru_p = 0U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__ptp_snap_p = 0U;
        if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__hb_kick_w) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__ever_backed_r = 1U;
        }
        vlSelfRef.milan_datapath__DOT__csr__DOT__i2spb_clro_p = 0U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__ptp_load_p = 0U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__ptp_adj_p = 0U;
        if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__st_r))) {
            if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__st_r))) {
                vlSelfRef.milan_datapath__DOT__cmap_pv_w = 0U;
                if ((0U == (IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__gap_r))) {
                    if ((0x1fU == (IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__slot_r))) {
                        vlSelfRef.__Vdly__milan_datapath__DOT__chan_map_capture__DOT__st_r = 0U;
                    } else {
                        vlSelfRef.__Vdly__milan_datapath__DOT__chan_map_capture__DOT__slot_r 
                            = (0x0000001fU & ((IData)(1U) 
                                              + (IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__slot_r)));
                        vlSelfRef.__Vdly__milan_datapath__DOT__chan_map_capture__DOT__st_r = 2U;
                    }
                } else {
                    vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__gap_r 
                        = (0x0000001fU & ((IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__gap_r) 
                                          - (IData)(1U)));
                }
            } else {
                vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__gap_r = 0x18U;
                vlSelfRef.milan_datapath__DOT__cmap_pv_w = 1U;
                vlSelfRef.milan_datapath__DOT__cmap_slot_w 
                    = vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__slot_r;
                vlSelfRef.__Vdly__milan_datapath__DOT__chan_map_capture__DOT__st_r = 3U;
                vlSelfRef.milan_datapath__DOT__cmap_l_w 
                    = (0x00ffffffU & ((0x00000800U 
                                       & vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r
                                       [((IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__slot_r) 
                                         << 1U)]) ? (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_257)
                                       : (IData)((vlSelfRef.__VdfgRegularize_h6e95ff9d_0_257 
                                                  >> 0x00000018U))));
                vlSelfRef.milan_datapath__DOT__cmap_r_w 
                    = (0x00ffffffU & ((0x00000800U 
                                       & vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__map_r
                                       [(1U | ((IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__slot_r) 
                                               << 1U))])
                                       ? (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_259)
                                       : (IData)((vlSelfRef.__VdfgRegularize_h6e95ff9d_0_259 
                                                  >> 0x00000018U))));
            }
        } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__st_r))) {
            if ((0x20U == (IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__pop_idx_r))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__chan_map_capture__DOT__st_r = 2U;
            } else {
                vlSelfRef.__Vdly__milan_datapath__DOT__chan_map_capture__DOT__pop_idx_r 
                    = (0x0000003fU & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__pop_idx_r)));
            }
        } else {
            vlSelfRef.milan_datapath__DOT__cmap_pv_w = 0U;
            if (vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__tick_pend_r) {
                vlSelfRef.__Vdly__milan_datapath__DOT__chan_map_capture__DOT__slot_r = 0U;
                vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__tick_pend_r = 0U;
                vlSelfRef.__Vdly__milan_datapath__DOT__chan_map_capture__DOT__pop_idx_r = 0U;
                vlSelfRef.__Vdly__milan_datapath__DOT__chan_map_capture__DOT__st_r = 1U;
            }
        }
        if (vlSelfRef.milan_datapath__DOT__media_tick_p) {
            vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__tick_pend_r = 1U;
        }
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__pop_ret_pair_r 
            = (0x0000001fU & (IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__pop_idx_r));
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_rdata_r 
            = vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__lb_q_r
            [((0x000000f8U & ((IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__pop_idx_r) 
                              << 3U)) | vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_rd_r
              [(0x0000001fU & (IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__pop_idx_r))])];
        vlSelfRef.milan_datapath__DOT__csr__DOT__tcam_wr_p = 0U;
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
                                                            (0x00000010U 
                                                             & (IData)(vlSelfRef.s_axi_awaddr))) {
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
                                                                                (0U 
                                                                                != 
                                                                                (vlSelfRef.s_axi_wdata 
                                                                                >> 0x10U))) {
                                                                                vlSelfRef.milan_datapath__DOT__csr__DOT__i2spb_clru_p = 1U;
                                                                            }
                                                                            if (
                                                                                (0U 
                                                                                != 
                                                                                (0x0000ffffU 
                                                                                & vlSelfRef.s_axi_wdata))) {
                                                                                vlSelfRef.milan_datapath__DOT__csr__DOT__i2spb_clro_p = 1U;
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
                                                                            vlSelfRef.milan_datapath__DOT__csr__DOT__tcam_act 
                                                                                = vlSelfRef.s_axi_wdata;
                                                                        }
                                                                    }
                                                                }
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
                                                                            vlSelfRef.milan_datapath__DOT__csr__DOT__tcam_mhi 
                                                                                = vlSelfRef.s_axi_wdata;
                                                                        }
                                                                    }
                                                                }
                                                            }
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
                                                                                (0x00010000U 
                                                                                & vlSelfRef.s_axi_wdata)) {
                                                                                vlSelfRef.milan_datapath__DOT__csr__DOT__tcam_wr_valid_r 
                                                                                = 
                                                                                (1U 
                                                                                & (vlSelfRef.s_axi_wdata 
                                                                                >> 8U));
                                                                                vlSelfRef.milan_datapath__DOT__csr__DOT__tcam_wr_p = 1U;
                                                                                vlSelfRef.milan_datapath__DOT__csr__DOT__tcam_wr_index 
                                                                                = 
                                                                                (0x0000001fU 
                                                                                & vlSelfRef.s_axi_wdata);
                                                                            }
                                                                        }
                                                                    }
                                                                }
                                                            }
                                                        }
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
                                                                            vlSelfRef.milan_datapath__DOT__csr__DOT__tcam_mlo 
                                                                                = vlSelfRef.s_axi_wdata;
                                                                        }
                                                                    }
                                                                }
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
                                                                            vlSelfRef.milan_datapath__DOT__csr__DOT__tcam_khi 
                                                                                = vlSelfRef.s_axi_wdata;
                                                                        }
                                                                    }
                                                                }
                                                            }
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
                                                                            vlSelfRef.milan_datapath__DOT__csr__DOT__tcam_klo 
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
                                                        (0x00000020U 
                                                         & (IData)(vlSelfRef.s_axi_awaddr))) {
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
                                                                                (4U 
                                                                                & vlSelfRef.s_axi_wdata)) {
                                                                                vlSelfRef.milan_datapath__DOT__csr__DOT__ptp_snap_p = 1U;
                                                                            }
                                                                            if (
                                                                                (1U 
                                                                                & vlSelfRef.s_axi_wdata)) {
                                                                                vlSelfRef.milan_datapath__DOT__csr__DOT__ptp_load_p = 1U;
                                                                            }
                                                                            if (
                                                                                (2U 
                                                                                & vlSelfRef.s_axi_wdata)) {
                                                                                vlSelfRef.milan_datapath__DOT__csr__DOT__ptp_adj_p = 1U;
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
        if (vlSelfRef.milan_datapath__DOT__lb_tap_tvalid_w) {
            if (vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__stash_open_w) {
                vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__stash_vld_r = 1U;
                vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__stash_val_r 
                    = vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__lb_smp1_w;
            } else {
                vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__stash_vld_r = 0U;
            }
            vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__lb_chpos_r 
                = (0x0000000fU & (((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__lb_ch1_w)) 
                                  & ((- (IData)((1U 
                                                 & (~ (IData)(vlSelfRef.milan_datapath__DOT__lb_tap_tlast_w))))) 
                                     & (- (IData)(((IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__lb_chans_w) 
                                                   != 
                                                   (0x0000000fU 
                                                    & ((IData)(1U) 
                                                       + (IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__lb_ch1_w)))))))));
        }
        if (vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__stash_flush_w) {
            vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__stash_vld_r = 0U;
        }
        if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__bld_st_r))) {
            if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__bld_st_r))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__bld_st_r = 0U;
            } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__bld_st_r))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__bld_st_r = 6U;
            } else if ((0x51U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__bld_idx_r))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__bld_st_r = 5U;
            } else {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__bld_idx_r 
                    = (0x0000007fU & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__bld_idx_r)));
            }
        } else if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__bld_st_r))) {
            if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__bld_st_r))) {
                if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__txc_locked_r) 
                     & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__alloc_gnt_r) 
                        & (0U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__txc_owner_r))))) {
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__bld_slot_r 
                        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__alloc_slot_r;
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__bld_idx_r = 0U;
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__bld_st_r = 4U;
                } else {
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__bld_st_r = 2U;
                }
            } else {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__bld_st_r = 3U;
            }
        } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__bld_st_r))) {
            __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__gm_slice_f__115__ifx 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__bld_if_r;
            __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__dom_slice_f__116__ifx 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__bld_if_r;
            __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__gm_slice_f__115__i 
                = ((1U > (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__gm_slice_f__115__ifx))
                    ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__gm_slice_f__115__ifx)
                    : 0U);
            __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__dom_slice_f__116__i 
                = ((1U > (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__dom_slice_f__116__ifx))
                    ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__dom_slice_f__116__ifx)
                    : 0U);
            __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__gm_slice_f__115__Vfuncout = 0ULL;
            __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__dom_slice_f__116__Vfuncout = 0U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__bld_aidx_r 
                = ((0U >= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__bld_if_r))
                    ? vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__aidx_r
                   [vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__bld_if_r]
                    : 0U);
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__bld_st_r = 2U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__bld_gm_r 
                = __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__gm_slice_f__115__Vfuncout;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__bld_dom_r 
                = __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__dom_slice_f__116__Vfuncout;
        } else if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__pick_vld_w) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__bld_dep_r 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__pick_dep_w;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__bld_if_r 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__pick_if_w;
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__bld_st_r = 1U;
        }
        if ((2U == (((IData)(vlSelfRef.milan_datapath__DOT__aafcap_pv_w) 
                     << 1U) | (IData)(vlSelfRef.milan_datapath__DOT__media_tick_p)))) {
            vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__tdm_frame_pend_r = 1U;
            vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__tdm_fed_r = 1U;
        } else {
            if ((1U == (((IData)(vlSelfRef.milan_datapath__DOT__aafcap_pv_w) 
                         << 1U) | (IData)(vlSelfRef.milan_datapath__DOT__media_tick_p)))) {
                vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__tdm_frame_pend_r = 0U;
            } else if ((3U == (((IData)(vlSelfRef.milan_datapath__DOT__aafcap_pv_w) 
                                << 1U) | (IData)(vlSelfRef.milan_datapath__DOT__media_tick_p)))) {
                vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__tdm_frame_pend_r = 0U;
            }
            if ((1U != (((IData)(vlSelfRef.milan_datapath__DOT__aafcap_pv_w) 
                         << 1U) | (IData)(vlSelfRef.milan_datapath__DOT__media_tick_p)))) {
                if ((3U == (((IData)(vlSelfRef.milan_datapath__DOT__aafcap_pv_w) 
                             << 1U) | (IData)(vlSelfRef.milan_datapath__DOT__media_tick_p)))) {
                    vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__tdm_fed_r = 1U;
                }
            }
        }
        vlSelfRef.milan_datapath__DOT__media_clock_restart__DOT__clk_src_q_r 
            = vlSelfRef.milan_datapath__DOT__media_clk_src_r;
        if ((1U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__evr_strobe_w)) {
            if ((1U & ((~ vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r) 
                       | vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__delivered_w))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r 
                    = (1U | vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r);
                vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r__v0 
                    = (0x0000ffffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__evr_payload_w[0U]);
                vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r__v0 = 1U;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r 
                    = (0xfffffffeU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r);
            } else {
                if ((0xffU != vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r[0U])) {
                    vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r__v0 
                        = (0x000000ffU & ((IData)(1U) 
                                          + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r[0U])));
                    vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r__v0 = 1U;
                }
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r 
                    = (1U | vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r);
            }
        } else if ((1U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__delivered_w)) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r 
                = (0xfffffffeU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r);
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r 
                = (0xfffffffeU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r);
        }
        if ((2U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__evr_strobe_w)) {
            if ((1U & ((~ (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r 
                           >> 1U)) | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__delivered_w 
                                      >> 1U)))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r 
                    = (2U | vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r);
                vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r__v1 
                    = (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__evr_payload_w[0U] 
                       >> 0x00000010U);
                vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r__v1 = 1U;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r 
                    = (0xfffffffdU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r);
            } else {
                if ((0xffU != vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r[1U])) {
                    vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r__v1 
                        = (0x000000ffU & ((IData)(1U) 
                                          + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r[1U])));
                    vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r__v1 = 1U;
                }
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r 
                    = (2U | vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r);
            }
        } else if ((2U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__delivered_w)) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r 
                = (0xfffffffdU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r);
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r 
                = (0xfffffffdU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r);
        }
        if ((4U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__evr_strobe_w)) {
            if ((1U & ((~ (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r 
                           >> 2U)) | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__delivered_w 
                                      >> 2U)))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r 
                    = (4U | vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r);
                vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r__v2 
                    = (0x0000ffffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__evr_payload_w[1U]);
                vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r__v2 = 1U;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r 
                    = (0xfffffffbU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r);
            } else {
                if ((0xffU != vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r[2U])) {
                    vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r__v2 
                        = (0x000000ffU & ((IData)(1U) 
                                          + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r[2U])));
                    vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r__v2 = 1U;
                }
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r 
                    = (4U | vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r);
            }
        } else if ((4U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__delivered_w)) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r 
                = (0xfffffffbU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r);
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r 
                = (0xfffffffbU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r);
        }
        if ((8U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__evr_strobe_w)) {
            if ((1U & ((~ (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r 
                           >> 3U)) | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__delivered_w 
                                      >> 3U)))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r 
                    = (8U | vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r);
                vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r__v3 
                    = (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__evr_payload_w[1U] 
                       >> 0x00000010U);
                vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r__v3 = 1U;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r 
                    = (0xfffffff7U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r);
            } else {
                if ((0xffU != vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r[3U])) {
                    vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r__v3 
                        = (0x000000ffU & ((IData)(1U) 
                                          + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r[3U])));
                    vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r__v3 = 1U;
                }
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r 
                    = (8U | vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r);
            }
        } else if ((8U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__delivered_w)) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r 
                = (0xfffffff7U & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r);
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r 
                = (0xfffffff7U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r);
        }
        if ((0x00000010U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__evr_strobe_w)) {
            if ((1U & ((~ (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r 
                           >> 4U)) | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__delivered_w 
                                      >> 4U)))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r 
                    = (0x00000010U | vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r);
                vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r__v4 
                    = (0x0000ffffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__evr_payload_w[2U]);
                vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r__v4 = 1U;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r 
                    = (0xffffffefU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r);
            } else {
                if ((0xffU != vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r[4U])) {
                    vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r__v4 
                        = (0x000000ffU & ((IData)(1U) 
                                          + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r[4U])));
                    vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r__v4 = 1U;
                }
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r 
                    = (0x00000010U | vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r);
            }
        } else if ((0x00000010U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__delivered_w)) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r 
                = (0xffffffefU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r);
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r 
                = (0xffffffefU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r);
        }
        if ((0x00000020U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__evr_strobe_w)) {
            if ((1U & ((~ (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r 
                           >> 5U)) | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__delivered_w 
                                      >> 5U)))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r 
                    = (0x00000020U | vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r);
                vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r__v5 
                    = (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__evr_payload_w[2U] 
                       >> 0x00000010U);
                vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r__v5 = 1U;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r 
                    = (0xffffffdfU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r);
            } else {
                if ((0xffU != vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r[5U])) {
                    vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r__v5 
                        = (0x000000ffU & ((IData)(1U) 
                                          + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r[5U])));
                    vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r__v5 = 1U;
                }
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r 
                    = (0x00000020U | vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r);
            }
        } else if ((0x00000020U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__delivered_w)) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r 
                = (0xffffffdfU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r);
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r 
                = (0xffffffdfU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r);
        }
        if ((0x00000040U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__evr_strobe_w)) {
            if ((1U & ((~ (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r 
                           >> 6U)) | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__delivered_w 
                                      >> 6U)))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r 
                    = (0x00000040U | vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r);
                vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r__v6 
                    = (0x0000ffffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__evr_payload_w[3U]);
                vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r__v6 = 1U;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r 
                    = (0xffffffbfU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r);
            } else {
                if ((0xffU != vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r[6U])) {
                    vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r__v6 
                        = (0x000000ffU & ((IData)(1U) 
                                          + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r[6U])));
                    vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r__v6 = 1U;
                }
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r 
                    = (0x00000040U | vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r);
            }
        } else if ((0x00000040U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__delivered_w)) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r 
                = (0xffffffbfU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r);
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r 
                = (0xffffffbfU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r);
        }
        if ((0x00000080U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__evr_strobe_w)) {
            if ((1U & ((~ (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r 
                           >> 7U)) | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__delivered_w 
                                      >> 7U)))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r 
                    = (0x00000080U | vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r);
                vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r__v7 
                    = (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__evr_payload_w[3U] 
                       >> 0x00000010U);
                vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r__v7 = 1U;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r 
                    = (0xffffff7fU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r);
            } else {
                if ((0xffU != vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r[7U])) {
                    vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r__v7 
                        = (0x000000ffU & ((IData)(1U) 
                                          + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r[7U])));
                    vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r__v7 = 1U;
                }
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r 
                    = (0x00000080U | vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r);
            }
        } else if ((0x00000080U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__delivered_w)) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r 
                = (0xffffff7fU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r);
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r 
                = (0xffffff7fU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r);
        }
        if ((0x00000100U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__evr_strobe_w)) {
            if ((1U & ((~ (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r 
                           >> 8U)) | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__delivered_w 
                                      >> 8U)))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r 
                    = (0x00000100U | vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r);
                vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r__v8 
                    = (0x0000ffffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__evr_payload_w[4U]);
                vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r__v8 = 1U;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r 
                    = (0xfffffeffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r);
            } else {
                if ((0xffU != vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r[8U])) {
                    vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r__v8 
                        = (0x000000ffU & ((IData)(1U) 
                                          + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r[8U])));
                    vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r__v8 = 1U;
                }
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r 
                    = (0x00000100U | vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r);
            }
        } else if ((0x00000100U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__delivered_w)) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r 
                = (0xfffffeffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r);
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r 
                = (0xfffffeffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r);
        }
        if ((0x00000200U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__evr_strobe_w)) {
            if ((1U & ((~ (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r 
                           >> 9U)) | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__delivered_w 
                                      >> 9U)))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r 
                    = (0x00000200U | vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r);
                vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r__v9 
                    = (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__evr_payload_w[4U] 
                       >> 0x00000010U);
                vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r__v9 = 1U;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r 
                    = (0xfffffdffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r);
            } else {
                if ((0xffU != vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r[9U])) {
                    vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r__v9 
                        = (0x000000ffU & ((IData)(1U) 
                                          + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r[9U])));
                    vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r__v9 = 1U;
                }
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r 
                    = (0x00000200U | vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r);
            }
        } else if ((0x00000200U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__delivered_w)) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r 
                = (0xfffffdffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r);
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r 
                = (0xfffffdffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r);
        }
        if ((0x00000400U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__evr_strobe_w)) {
            if ((1U & ((~ (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r 
                           >> 0x0aU)) | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__delivered_w 
                                         >> 0x0aU)))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r 
                    = (0x00000400U | vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r);
                vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r__v10 
                    = (0x0000ffffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__evr_payload_w[5U]);
                vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r__v10 = 1U;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r 
                    = (0xfffffbffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r);
            } else {
                if ((0xffU != vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r[10U])) {
                    vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r__v10 
                        = (0x000000ffU & ((IData)(1U) 
                                          + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r[10U])));
                    vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r__v10 = 1U;
                }
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r 
                    = (0x00000400U | vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r);
            }
        } else if ((0x00000400U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__delivered_w)) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r 
                = (0xfffffbffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r);
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r 
                = (0xfffffbffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r);
        }
        if ((0x00000800U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__evr_strobe_w)) {
            if ((1U & ((~ (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r 
                           >> 0x0bU)) | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__delivered_w 
                                         >> 0x0bU)))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r 
                    = (0x00000800U | vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r);
                vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r__v11 
                    = (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__evr_payload_w[5U] 
                       >> 0x00000010U);
                vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r__v11 = 1U;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r 
                    = (0xfffff7ffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r);
            } else {
                if ((0xffU != vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r[11U])) {
                    vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r__v11 
                        = (0x000000ffU & ((IData)(1U) 
                                          + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r[11U])));
                    vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r__v11 = 1U;
                }
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r 
                    = (0x00000800U | vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r);
            }
        } else if ((0x00000800U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__delivered_w)) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r 
                = (0xfffff7ffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r);
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r 
                = (0xfffff7ffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r);
        }
        if ((0x00001000U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__evr_strobe_w)) {
            if ((1U & ((~ (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r 
                           >> 0x0cU)) | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__delivered_w 
                                         >> 0x0cU)))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r 
                    = (0x00001000U | vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r);
                vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r__v12 
                    = (0x0000ffffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__evr_payload_w[6U]);
                vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r__v12 = 1U;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r 
                    = (0xffffefffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r);
            } else {
                if ((0xffU != vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r[12U])) {
                    vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r__v12 
                        = (0x000000ffU & ((IData)(1U) 
                                          + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r[12U])));
                    vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r__v12 = 1U;
                }
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r 
                    = (0x00001000U | vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r);
            }
        } else if ((0x00001000U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__delivered_w)) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r 
                = (0xffffefffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r);
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r 
                = (0xffffefffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r);
        }
        if ((0x00002000U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__evr_strobe_w)) {
            if ((1U & ((~ (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r 
                           >> 0x0dU)) | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__delivered_w 
                                         >> 0x0dU)))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r 
                    = (0x00002000U | vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r);
                vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r__v13 
                    = (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__evr_payload_w[6U] 
                       >> 0x00000010U);
                vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r__v13 = 1U;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r 
                    = (0xffffdfffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r);
            } else {
                if ((0xffU != vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r[13U])) {
                    vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r__v13 
                        = (0x000000ffU & ((IData)(1U) 
                                          + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r[13U])));
                    vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r__v13 = 1U;
                }
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r 
                    = (0x00002000U | vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r);
            }
        } else if ((0x00002000U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__delivered_w)) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r 
                = (0xffffdfffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r);
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r 
                = (0xffffdfffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r);
        }
        if ((0x00004000U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__evr_strobe_w)) {
            if ((1U & ((~ (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r 
                           >> 0x0eU)) | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__delivered_w 
                                         >> 0x0eU)))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r 
                    = (0x00004000U | vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r);
                vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r__v14 
                    = (0x0000ffffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__evr_payload_w[7U]);
                vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r__v14 = 1U;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r 
                    = (0xffffbfffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r);
            } else {
                if ((0xffU != vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r[14U])) {
                    vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r__v14 
                        = (0x000000ffU & ((IData)(1U) 
                                          + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r[14U])));
                    vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r__v14 = 1U;
                }
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r 
                    = (0x00004000U | vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r);
            }
        } else if ((0x00004000U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__delivered_w)) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r 
                = (0xffffbfffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r);
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r 
                = (0xffffbfffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r);
        }
        if ((0x00008000U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__evr_strobe_w)) {
            if ((1U & ((~ (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r 
                           >> 0x0fU)) | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__delivered_w 
                                         >> 0x0fU)))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r 
                    = (0x00008000U | vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r);
                vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r__v15 
                    = (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__evr_payload_w[7U] 
                       >> 0x00000010U);
                vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r__v15 = 1U;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r 
                    = (0xffff7fffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r);
            } else {
                if ((0xffU != vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r[15U])) {
                    vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r__v15 
                        = (0x000000ffU & ((IData)(1U) 
                                          + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r[15U])));
                    vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r__v15 = 1U;
                }
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r 
                    = (0x00008000U | vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r);
            }
        } else if ((0x00008000U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__delivered_w)) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r 
                = (0xffff7fffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r);
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r 
                = (0xffff7fffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r);
        }
        if ((0x00010000U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__evr_strobe_w)) {
            if ((1U & ((~ (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r 
                           >> 0x10U)) | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__delivered_w 
                                         >> 0x10U)))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r 
                    = (0x00010000U | vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r);
                vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r__v16 
                    = (0x0000ffffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__evr_payload_w[8U]);
                vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r__v16 = 1U;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r 
                    = (0xfffeffffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r);
            } else {
                if ((0xffU != vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r[16U])) {
                    vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r__v16 
                        = (0x000000ffU & ((IData)(1U) 
                                          + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r[16U])));
                    vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r__v16 = 1U;
                }
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r 
                    = (0x00010000U | vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r);
            }
        } else if ((0x00010000U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__delivered_w)) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r 
                = (0xfffeffffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r);
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r 
                = (0xfffeffffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r);
        }
        if ((0x00020000U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__evr_strobe_w)) {
            if ((1U & ((~ (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r 
                           >> 0x11U)) | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__delivered_w 
                                         >> 0x11U)))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r 
                    = (0x00020000U | vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r);
                vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r__v17 
                    = (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__evr_payload_w[8U] 
                       >> 0x00000010U);
                vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r__v17 = 1U;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r 
                    = (0xfffdffffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r);
            } else {
                if ((0xffU != vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r[17U])) {
                    vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r__v17 
                        = (0x000000ffU & ((IData)(1U) 
                                          + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r[17U])));
                    vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r__v17 = 1U;
                }
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r 
                    = (0x00020000U | vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r);
            }
        } else if ((0x00020000U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__delivered_w)) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r 
                = (0xfffdffffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r);
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r 
                = (0xfffdffffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r);
        }
        if ((0x00040000U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__evr_strobe_w)) {
            if ((1U & ((~ (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r 
                           >> 0x12U)) | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__delivered_w 
                                         >> 0x12U)))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r 
                    = (0x00040000U | vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r);
                vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r__v18 
                    = (0x0000ffffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__evr_payload_w[9U]);
                vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r__v18 = 1U;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r 
                    = (0xfffbffffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r);
            } else {
                if ((0xffU != vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r[18U])) {
                    vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r__v18 
                        = (0x000000ffU & ((IData)(1U) 
                                          + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r[18U])));
                    vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r__v18 = 1U;
                }
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r 
                    = (0x00040000U | vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r);
            }
        } else if ((0x00040000U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__delivered_w)) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r 
                = (0xfffbffffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r);
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r 
                = (0xfffbffffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r);
        }
        if ((0x00080000U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__evr_strobe_w)) {
            if ((1U & ((~ (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r 
                           >> 0x13U)) | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__delivered_w 
                                         >> 0x13U)))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r 
                    = (0x00080000U | vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r);
                vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r__v19 
                    = (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__evr_payload_w[9U] 
                       >> 0x00000010U);
                vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r__v19 = 1U;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r 
                    = (0xfff7ffffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r);
            } else {
                if ((0xffU != vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r[19U])) {
                    vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r__v19 
                        = (0x000000ffU & ((IData)(1U) 
                                          + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r[19U])));
                    vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r__v19 = 1U;
                }
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r 
                    = (0x00080000U | vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r);
            }
        } else if ((0x00080000U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__delivered_w)) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r 
                = (0xfff7ffffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r);
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r 
                = (0xfff7ffffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r);
        }
        if ((0x00100000U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__evr_strobe_w)) {
            if ((1U & ((~ (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r 
                           >> 0x14U)) | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__delivered_w 
                                         >> 0x14U)))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r 
                    = (0x00100000U | vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r);
                vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r__v20 
                    = (0x0000ffffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__evr_payload_w[10U]);
                vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r__v20 = 1U;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r 
                    = (0xffefffffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r);
            } else {
                if ((0xffU != vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r[20U])) {
                    vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r__v20 
                        = (0x000000ffU & ((IData)(1U) 
                                          + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r[20U])));
                    vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r__v20 = 1U;
                }
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r 
                    = (0x00100000U | vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r);
            }
        } else if ((0x00100000U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__delivered_w)) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r 
                = (0xffefffffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r);
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r 
                = (0xffefffffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r);
        }
        if ((0x00200000U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__evr_strobe_w)) {
            if ((1U & ((~ (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r 
                           >> 0x15U)) | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__delivered_w 
                                         >> 0x15U)))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r 
                    = (0x00200000U | vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r);
                vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r__v21 
                    = (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__evr_payload_w[10U] 
                       >> 0x00000010U);
                vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r__v21 = 1U;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r 
                    = (0xffdfffffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r);
            } else {
                if ((0xffU != vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r[21U])) {
                    vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r__v21 
                        = (0x000000ffU & ((IData)(1U) 
                                          + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r[21U])));
                    vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r__v21 = 1U;
                }
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r 
                    = (0x00200000U | vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r);
            }
        } else if ((0x00200000U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__delivered_w)) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r 
                = (0xffdfffffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r);
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r 
                = (0xffdfffffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r);
        }
        if ((0x00400000U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__evr_strobe_w)) {
            if ((1U & ((~ (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r 
                           >> 0x16U)) | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__delivered_w 
                                         >> 0x16U)))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r 
                    = (0x00400000U | vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r);
                vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r__v22 
                    = (0x0000ffffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__evr_payload_w[11U]);
                vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r__v22 = 1U;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r 
                    = (0xffbfffffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r);
            } else {
                if ((0xffU != vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r[22U])) {
                    vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r__v22 
                        = (0x000000ffU & ((IData)(1U) 
                                          + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r[22U])));
                    vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r__v22 = 1U;
                }
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r 
                    = (0x00400000U | vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r);
            }
        } else if ((0x00400000U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__delivered_w)) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r 
                = (0xffbfffffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r);
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r 
                = (0xffbfffffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r);
        }
        if ((0x00800000U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__evr_strobe_w)) {
            if ((1U & ((~ (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r 
                           >> 0x17U)) | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__delivered_w 
                                         >> 0x17U)))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r 
                    = (0x00800000U | vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r);
                vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r__v23 
                    = (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__evr_payload_w[11U] 
                       >> 0x00000010U);
                vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r__v23 = 1U;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r 
                    = (0xff7fffffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r);
            } else {
                if ((0xffU != vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r[23U])) {
                    vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r__v23 
                        = (0x000000ffU & ((IData)(1U) 
                                          + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r[23U])));
                    vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r__v23 = 1U;
                }
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r 
                    = (0x00800000U | vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r);
            }
        } else if ((0x00800000U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__delivered_w)) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r 
                = (0xff7fffffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r);
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r 
                = (0xff7fffffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r);
        }
        if ((0x01000000U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__evr_strobe_w)) {
            if ((1U & ((~ (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r 
                           >> 0x18U)) | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__delivered_w 
                                         >> 0x18U)))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r 
                    = (0x01000000U | vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r);
                vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r__v24 
                    = (0x0000ffffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__evr_payload_w[12U]);
                vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r__v24 = 1U;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r 
                    = (0xfeffffffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r);
            } else {
                if ((0xffU != vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r[24U])) {
                    vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r__v24 
                        = (0x000000ffU & ((IData)(1U) 
                                          + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r[24U])));
                    vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r__v24 = 1U;
                }
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r 
                    = (0x01000000U | vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r);
            }
        } else if ((0x01000000U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__delivered_w)) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r 
                = (0xfeffffffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r);
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r 
                = (0xfeffffffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r);
        }
        if ((0x02000000U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__evr_strobe_w)) {
            if ((1U & ((~ (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r 
                           >> 0x19U)) | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__delivered_w 
                                         >> 0x19U)))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r 
                    = (0x02000000U | vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r);
                vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r__v25 
                    = (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__evr_payload_w[12U] 
                       >> 0x00000010U);
                vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r__v25 = 1U;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r 
                    = (0xfdffffffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r);
            } else {
                if ((0xffU != vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r[25U])) {
                    vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r__v25 
                        = (0x000000ffU & ((IData)(1U) 
                                          + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r[25U])));
                    vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r__v25 = 1U;
                }
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r 
                    = (0x02000000U | vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r);
            }
        } else if ((0x02000000U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__delivered_w)) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r 
                = (0xfdffffffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r);
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r 
                = (0xfdffffffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r);
        }
        if ((0x04000000U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__evr_strobe_w)) {
            if ((1U & ((~ (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r 
                           >> 0x1aU)) | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__delivered_w 
                                         >> 0x1aU)))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r 
                    = (0x04000000U | vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r);
                vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r__v26 
                    = (0x0000ffffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__evr_payload_w[13U]);
                vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r__v26 = 1U;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r 
                    = (0xfbffffffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r);
            } else {
                if ((0xffU != vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r[26U])) {
                    vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r__v26 
                        = (0x000000ffU & ((IData)(1U) 
                                          + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r[26U])));
                    vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r__v26 = 1U;
                }
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r 
                    = (0x04000000U | vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r);
            }
        } else if ((0x04000000U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__delivered_w)) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r 
                = (0xfbffffffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r);
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r 
                = (0xfbffffffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r);
        }
        if ((0x08000000U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__evr_strobe_w)) {
            if ((1U & ((~ (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r 
                           >> 0x1bU)) | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__delivered_w 
                                         >> 0x1bU)))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r 
                    = (0x08000000U | vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r);
                vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r__v27 
                    = (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__evr_payload_w[13U] 
                       >> 0x00000010U);
                vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r__v27 = 1U;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r 
                    = (0xf7ffffffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r);
            } else {
                if ((0xffU != vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r[27U])) {
                    vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r__v27 
                        = (0x000000ffU & ((IData)(1U) 
                                          + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r[27U])));
                    vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r__v27 = 1U;
                }
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r 
                    = (0x08000000U | vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r);
            }
        } else if ((0x08000000U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__delivered_w)) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r 
                = (0xf7ffffffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r);
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r 
                = (0xf7ffffffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r);
        }
        if ((0x10000000U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__evr_strobe_w)) {
            if ((1U & ((~ (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r 
                           >> 0x1cU)) | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__delivered_w 
                                         >> 0x1cU)))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r 
                    = (0x10000000U | vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r);
                vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r__v28 
                    = (0x0000ffffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__evr_payload_w[14U]);
                vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r__v28 = 1U;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r 
                    = (0xefffffffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r);
            } else {
                if ((0xffU != vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r[28U])) {
                    vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r__v28 
                        = (0x000000ffU & ((IData)(1U) 
                                          + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r[28U])));
                    vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r__v28 = 1U;
                }
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r 
                    = (0x10000000U | vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r);
            }
        } else if ((0x10000000U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__delivered_w)) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r 
                = (0xefffffffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r);
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r 
                = (0xefffffffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r);
        }
        if ((0x20000000U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__evr_strobe_w)) {
            if ((1U & ((~ (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r 
                           >> 0x1dU)) | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__delivered_w 
                                         >> 0x1dU)))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r 
                    = (0x20000000U | vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r);
                vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r__v29 
                    = (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__evr_payload_w[14U] 
                       >> 0x00000010U);
                vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r__v29 = 1U;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r 
                    = (0xdfffffffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r);
            } else {
                if ((0xffU != vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r[29U])) {
                    vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r__v29 
                        = (0x000000ffU & ((IData)(1U) 
                                          + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r[29U])));
                    vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r__v29 = 1U;
                }
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r 
                    = (0x20000000U | vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r);
            }
        } else if ((0x20000000U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__delivered_w)) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r 
                = (0xdfffffffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r);
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r 
                = (0xdfffffffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r);
        }
        if ((0x40000000U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__evr_strobe_w)) {
            if ((1U & ((~ (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r 
                           >> 0x1eU)) | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__delivered_w 
                                         >> 0x1eU)))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r 
                    = (0x40000000U | vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r);
                vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r__v30 
                    = (0x0000ffffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__evr_payload_w[15U]);
                vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r__v30 = 1U;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r 
                    = (0xbfffffffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r);
            } else {
                if ((0xffU != vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r[30U])) {
                    vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r__v30 
                        = (0x000000ffU & ((IData)(1U) 
                                          + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r[30U])));
                    vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r__v30 = 1U;
                }
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r 
                    = (0x40000000U | vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r);
            }
        } else if ((0x40000000U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__delivered_w)) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r 
                = (0xbfffffffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r);
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r 
                = (0xbfffffffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r);
        }
        if ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__evr_strobe_w 
             >> 0x1fU)) {
            if ((1U & ((~ (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r 
                           >> 0x1fU)) | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__delivered_w 
                                         >> 0x1fU)))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r 
                    = (0x80000000U | vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r);
                vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r__v31 
                    = (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__evr_payload_w[15U] 
                       >> 0x00000010U);
                vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r__v31 = 1U;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r 
                    = (0x7fffffffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r);
            } else {
                if ((0xffU != vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r[31U])) {
                    vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r__v31 
                        = (0x000000ffU & ((IData)(1U) 
                                          + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r[31U])));
                    vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r__v31 = 1U;
                }
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r 
                    = (0x80000000U | vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r);
            }
        } else if ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__delivered_w 
                    >> 0x1fU)) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r 
                = (0x7fffffffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r);
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r 
                = (0x7fffffffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r);
        }
    } else {
        vlSelfRef.milan_datapath__DOT__wing_stg_vld_r = 0U;
        vlSelfRef.milan_datapath__DOT__wing_stg_idx_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_st_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_pend_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_msg_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_status_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_sid_r = 0ULL;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_ctlr_r = 0ULL;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_tkeid_r = 0ULL;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_lseid_r = 0ULL;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_tkuid_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_lsuid_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_cc_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_seq_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_flags_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_vlan_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_da_r = 0ULL;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_drop_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_slot_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_bidx_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_lane_valid_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__grant_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__acmp_sb_slot_r = 0U;
        vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__pos_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__pstate_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__chain_ann_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__draw_req_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__w_st_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__ival_ann_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__send_msg_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__teardown_ph_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__draw_act_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__draw_kind_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__bld_slot_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__bld_idx_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__arm_v_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__arm_c_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__arm_ann_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__arm_dl_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__link_guard__DOT__bounce_cnt_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__link_guard__DOT__state_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__link_guard__DOT__settle_r = 0U;
        vlSelfRef.milan_datapath__DOT__link_guard__DOT__guard_rst_r = 0U;
        vlSelfRef.milan_datapath__DOT__link_guard__DOT__eth_rst_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__link_guard__DOT__bounced_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__per_pend_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_side_port__DOT__state_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_side_port__DOT__sel_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__src_pend_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__src_band_ticks_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__src_eng_ticks_r = 0U;
        vlSelfRef.milan_datapath__DOT__src_recentre_p_r = 0U;
        vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__to_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__active_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__stg_r = 1U;
        vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__prevc_r = 0U;
        vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__epoch_pend_r = 0U;
        vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__epoch_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__samples_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__timeouts_r = 0U;
        vlSelfRef.__VdlySet__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__last_r__v9 = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_cnt_r = 0U;
        vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__to_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__active_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__stg_r = 1U;
        vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__prevc_r = 0U;
        vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__epoch_pend_r = 0U;
        vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__epoch_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__samples_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__timeouts_r = 0U;
        vlSelfRef.__VdlySet__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__last_r__v9 = 1U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__irq_status = 0U;
        vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__lhold_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__csr__DOT__cmrd_busy_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__csr__DOT__cmrd_flush_r = 0U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__cmrd_valid_r = 0U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__cmrd_to_r = 0U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__cmrd_data_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__csr__DOT__cmrd_wd_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__DOT__wr_closed_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__4__KET____DOT__u_rx_slots__DOT__wr_closed_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__2__KET____DOT__u_rx_slots__DOT__wr_closed_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__1__KET____DOT__u_rx_slots__DOT__wr_closed_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__0__KET____DOT__u_rx_slots__DOT__wr_closed_r = 0U;
        VL_ASSIGN_W(432, vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__da_r, Vmilan_datapath__ConstPool__CONST_hcc9a9126_0);
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__i2s_hold_r = 0ULL;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_pend_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rla_pend_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rtype_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__probe_left_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__maap_conflicts = 0U;
        vlSelfRef.milan_datapath__DOT__maap_defends = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__state_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__offset_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__timer_ms_r = 0U;
        vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__seed_used_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_busy_r = 0U;
        vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_msg_r = 0U;
        vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_conf_start_r = 0U;
        vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_conf_cnt_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__scan_ix_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__free_v_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__ridx_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__rejoin_pend_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__st_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__active_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__op_join_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__op_vid_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__chk_ix_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__chk_v_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__found_v_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__found_ix_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__found_cnt_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__free_ix_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__ev_code_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__ev_vid_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vj_pend_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vl_pend_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vj_vid_r[0U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vj_vid_r[1U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vj_vid_r[2U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vj_vid_r[3U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vl_vid_r[0U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vl_vid_r[1U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vl_vid_r[2U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vl_vid_r[3U] = 0U;
        VL_ASSIGN_W(288, vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__slope_q_r, Vmilan_datapath__ConstPool__CONST_h9a2fc1c8_0);
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vj_pend_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vl_pend_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vj_vid_r[0U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vj_vid_r[1U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vj_vid_r[2U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vj_vid_r[3U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vl_vid_r[0U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vl_vid_r[1U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vl_vid_r[2U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vl_vid_r[3U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__fcode_r[0U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__fcode_r[1U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__fcode_r[2U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_val_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__sp_ctrl_rdata_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__gp_valid_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__gp_src_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__gp_da_r = 0ULL;
        vlSelfRef.milan_datapath__DOT__csr__DOT__r_data = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__done_seen_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__state_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__err_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__hidx_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__bcnt_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__plen_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__rec_r = 0U;
        vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__hdr_r__v2 = 1U;
        VL_ASSIGN_W(576, vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__bound_sid_r, Vmilan_datapath__ConstPool__CONST_h026f187a_0);
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__bound_q_r = 0U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__snap_busy_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__csr__DOT__snap_st_r = 0U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__snap_dir_r = 0U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__snap_idx_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__csr__DOT__snap_wi_r = 0U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__snap_cyc_r = 0U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__snap_word_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__csr__DOT__snap_req_r = 0U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__snap_rden_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__csr__DOT__snap_m8_r = 0U;
        vlSelfRef.__VdlySet__milan_datapath__DOT__csr__DOT__snap_shadow_r__v51 = 1U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__waddr_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__bidx_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__st_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__cur_app_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__drain_n_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__slot_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__ll_addr_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__msg_open_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__msg_type_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__first_vec_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__close_for_pdu_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_open_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_type_r = 0U;
        VL_ASSIGN_W(272, vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_first_r, Vmilan_datapath__ConstPool__CONST_hc5471b50_0);
        VL_ASSIGN_W(272, vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_last_r, Vmilan_datapath__ConstPool__CONST_hc5471b50_0);
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_len_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__hold_valid_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__hold_type_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__hold_ev_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__hold_fp_r = 0U;
        VL_ASSIGN_W(272, vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__hold_val_r, Vmilan_datapath__ConstPool__CONST_hc5471b50_0);
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__cnt_msrp_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__cnt_mvrp_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__rd_idx_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__join_pend_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__la_pend_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__sp_snap_rdata_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__p2_d_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_mrp_strip__DOT__hdr_idx_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_mrp_strip__DOT__et_r = 0U;
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__chpos_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__ever_backed_r = 0U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__tcam_act = 0U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__tcam_wr_valid_r = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__tick_pend_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__chan_map_capture__DOT__slot_r = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__gap_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__chan_map_capture__DOT__st_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__chan_map_capture__DOT__pop_idx_r = 0U;
        vlSelfRef.milan_datapath__DOT__cmap_pv_w = 0U;
        vlSelfRef.milan_datapath__DOT__cmap_slot_w = 0U;
        vlSelfRef.milan_datapath__DOT__cmap_l_w = 0U;
        vlSelfRef.milan_datapath__DOT__cmap_r_w = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__pop_ret_pair_r = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_rdata_r = 0ULL;
        vlSelfRef.milan_datapath__DOT__csr__DOT__tcam_mhi = 0U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__tcam_mlo = 0U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__tcam_khi = 0U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__tcam_klo = 0U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__tcam_wr_index = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__stash_vld_r = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__stash_val_r = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__lb_chpos_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__bld_st_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__bld_dep_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__bld_if_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__bld_slot_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__bld_idx_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__bld_gm_r = 0ULL;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__bld_dom_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__bld_aidx_r = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__tdm_frame_pend_r = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__tdm_fed_r = 0U;
        vlSelfRef.milan_datapath__DOT__media_clock_restart__DOT__clk_src_q_r = 0U;
        vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r__v32 = 1U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r = 0U;
        vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r__v32 = 1U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__prefill_r__v8) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__converged_r[1U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v7) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__converged_r[1U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__prefill_r__v10) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__converged_r[2U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__converged_r__v13) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__converged_r[2U] = 1U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__prefill_r__v12) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__converged_r[2U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v10) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__converged_r[2U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__prefill_r__v13) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__converged_r[2U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v11) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__converged_r[2U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__prefill_r__v15) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__converged_r[3U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__converged_r__v19) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__converged_r[3U] = 1U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__prefill_r__v17) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__converged_r[3U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v14) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__converged_r[3U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__prefill_r__v18) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__converged_r[3U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v15) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__converged_r[3U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__prefill_r__v20) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__converged_r[4U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__converged_r__v25) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__converged_r[4U] = 1U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__prefill_r__v22) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__converged_r[4U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v18) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__converged_r[4U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__prefill_r__v23) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__converged_r[4U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v19) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__converged_r[4U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__prefill_r__v25) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__converged_r[5U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__converged_r__v31) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__converged_r[5U] = 1U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__prefill_r__v27) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__converged_r[5U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v22) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__converged_r[5U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__prefill_r__v28) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__converged_r[5U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v23) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__converged_r[5U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__prefill_r__v30) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__converged_r[6U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__converged_r__v37) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__converged_r[6U] = 1U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__prefill_r__v32) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__converged_r[6U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v26) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__converged_r[6U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__prefill_r__v33) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__converged_r[6U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v27) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__converged_r[6U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__prefill_r__v35) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__converged_r[7U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__converged_r__v43) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__converged_r[7U] = 1U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__prefill_r__v37) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__converged_r[7U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v30) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__converged_r[7U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__prefill_r__v38) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__converged_r[7U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__prefill_r__v2) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__dev_ok_r[0U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__dev_ok_r__v2) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__dev_ok_r[0U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__render_setpoint__DOT__dev_ok_r__v2;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v2) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__dev_ok_r[0U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__prefill_r__v3) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__dev_ok_r[0U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v3) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__dev_ok_r[0U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__prefill_r__v5) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__dev_ok_r[1U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__prefill_r__v7) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__dev_ok_r[1U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__dev_ok_r__v8) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__dev_ok_r[1U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__render_setpoint__DOT__dev_ok_r__v8;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v6) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__dev_ok_r[1U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__prefill_r__v8) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__dev_ok_r[1U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v7) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__dev_ok_r[1U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__prefill_r__v10) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__dev_ok_r[2U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__prefill_r__v12) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__dev_ok_r[2U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__dev_ok_r__v14) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__dev_ok_r[2U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__render_setpoint__DOT__dev_ok_r__v14;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v10) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__dev_ok_r[2U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__prefill_r__v13) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__dev_ok_r[2U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v11) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__dev_ok_r[2U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__prefill_r__v15) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__dev_ok_r[3U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__prefill_r__v17) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__dev_ok_r[3U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__dev_ok_r__v20) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__dev_ok_r[3U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__render_setpoint__DOT__dev_ok_r__v20;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v14) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__dev_ok_r[3U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__prefill_r__v18) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__dev_ok_r[3U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v15) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__dev_ok_r[3U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__prefill_r__v20) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__dev_ok_r[4U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__prefill_r__v22) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__dev_ok_r[4U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__dev_ok_r__v26) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__dev_ok_r[4U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__render_setpoint__DOT__dev_ok_r__v26;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v18) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__dev_ok_r[4U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__prefill_r__v23) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__dev_ok_r[4U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v19) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__dev_ok_r[4U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__prefill_r__v25) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__dev_ok_r[5U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__prefill_r__v27) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__dev_ok_r[5U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__dev_ok_r__v32) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__dev_ok_r[5U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__render_setpoint__DOT__dev_ok_r__v32;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v22) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__dev_ok_r[5U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__prefill_r__v28) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__dev_ok_r[5U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v23) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__dev_ok_r[5U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__prefill_r__v30) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__dev_ok_r[6U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__prefill_r__v32) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__dev_ok_r[6U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__dev_ok_r__v38) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__dev_ok_r[6U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__render_setpoint__DOT__dev_ok_r__v38;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v26) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__dev_ok_r[6U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__prefill_r__v33) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__dev_ok_r[6U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v27) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__dev_ok_r[6U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__prefill_r__v35) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__dev_ok_r[7U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__prefill_r__v37) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__dev_ok_r[7U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__dev_ok_r__v44) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__dev_ok_r[7U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__render_setpoint__DOT__dev_ok_r__v44;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v30) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__dev_ok_r[7U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__prefill_r__v38) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__dev_ok_r[7U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__conv_ms_r__v1) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__conv_ms_r[0U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__render_setpoint__DOT__conv_ms_r__v1;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__prefill_r__v2) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__conv_ms_r[0U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v1) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__prefill_r[0U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__prefill_r__v2) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__prefill_r[0U] = 1U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v2) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__conv_ms_r[0U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__prefill_r__v3) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__conv_ms_r[0U] = 0U;
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__prefill_r[0U] = 1U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v3) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__conv_ms_r[0U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__prefill_r__v5) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__conv_ms_r[1U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v3) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__prefill_r[0U] = 1U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__prefill_r__v5) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__prefill_r[1U] = 1U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__conv_ms_r__v7) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__conv_ms_r[1U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__render_setpoint__DOT__conv_ms_r__v7;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__prefill_r__v7) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__conv_ms_r[1U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v5) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__prefill_r[1U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__prefill_r__v7) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__prefill_r[1U] = 1U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v6) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__conv_ms_r[1U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__prefill_r__v8) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__conv_ms_r[1U] = 0U;
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__prefill_r[1U] = 1U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v7) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__conv_ms_r[1U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__prefill_r__v10) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__conv_ms_r[2U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v7) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__prefill_r[1U] = 1U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__prefill_r__v10) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__prefill_r[2U] = 1U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__conv_ms_r__v13) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__conv_ms_r[2U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__render_setpoint__DOT__conv_ms_r__v13;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__prefill_r__v12) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__conv_ms_r[2U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v9) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__prefill_r[2U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__prefill_r__v12) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__prefill_r[2U] = 1U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v10) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__conv_ms_r[2U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__prefill_r__v13) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__conv_ms_r[2U] = 0U;
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__prefill_r[2U] = 1U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v11) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__conv_ms_r[2U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__prefill_r__v15) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__conv_ms_r[3U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v11) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__prefill_r[2U] = 1U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__prefill_r__v15) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__prefill_r[3U] = 1U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__conv_ms_r__v19) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__conv_ms_r[3U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__render_setpoint__DOT__conv_ms_r__v19;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__prefill_r__v17) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__conv_ms_r[3U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v13) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__prefill_r[3U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__prefill_r__v17) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__prefill_r[3U] = 1U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v14) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__conv_ms_r[3U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__prefill_r__v18) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__conv_ms_r[3U] = 0U;
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__prefill_r[3U] = 1U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v15) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__conv_ms_r[3U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__prefill_r__v20) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__conv_ms_r[4U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v15) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__prefill_r[3U] = 1U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__prefill_r__v20) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__prefill_r[4U] = 1U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__conv_ms_r__v25) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__conv_ms_r[4U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__render_setpoint__DOT__conv_ms_r__v25;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__prefill_r__v22) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__conv_ms_r[4U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v17) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__prefill_r[4U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__prefill_r__v22) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__prefill_r[4U] = 1U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v18) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__conv_ms_r[4U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__prefill_r__v23) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__conv_ms_r[4U] = 0U;
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__prefill_r[4U] = 1U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v19) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__conv_ms_r[4U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__prefill_r__v25) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__conv_ms_r[5U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v19) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__prefill_r[4U] = 1U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__prefill_r__v25) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__prefill_r[5U] = 1U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__conv_ms_r__v31) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__conv_ms_r[5U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__render_setpoint__DOT__conv_ms_r__v31;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__prefill_r__v27) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__conv_ms_r[5U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v21) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__prefill_r[5U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__prefill_r__v27) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__prefill_r[5U] = 1U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v22) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__conv_ms_r[5U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__prefill_r__v28) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__conv_ms_r[5U] = 0U;
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__prefill_r[5U] = 1U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v23) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__conv_ms_r[5U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__prefill_r__v30) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__conv_ms_r[6U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v23) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__prefill_r[5U] = 1U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__prefill_r__v30) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__prefill_r[6U] = 1U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__conv_ms_r__v37) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__conv_ms_r[6U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__render_setpoint__DOT__conv_ms_r__v37;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__prefill_r__v32) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__conv_ms_r[6U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v25) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__prefill_r[6U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__prefill_r__v32) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__prefill_r[6U] = 1U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v26) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__conv_ms_r[6U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__prefill_r__v33) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__conv_ms_r[6U] = 0U;
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__prefill_r[6U] = 1U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v27) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__conv_ms_r[6U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__prefill_r__v35) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__conv_ms_r[7U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v27) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__prefill_r[6U] = 1U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__prefill_r__v35) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__prefill_r[7U] = 1U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__conv_ms_r__v43) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__conv_ms_r[7U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__render_setpoint__DOT__conv_ms_r__v43;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__prefill_r__v37) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__conv_ms_r[7U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v29) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__prefill_r[7U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__prefill_r__v37) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__prefill_r[7U] = 1U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v30) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__conv_ms_r[7U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__prefill_r__v38) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__conv_ms_r[7U] = 0U;
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__prefill_r[7U] = 1U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v31) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__pend_r[7U] = 0U;
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__converged_r[7U] = 0U;
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__dev_ok_r[7U] = 0U;
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__conv_ms_r[7U] = 0U;
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__prefill_r[7U] = 1U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v0) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__rptr_r[0U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v0;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v1) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__rptr_r[0U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v1;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v2) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__rptr_r[0U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v2;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v3) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__rptr_r[0U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v3;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v4) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__rptr_r[1U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v4;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v5) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__rptr_r[1U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v5;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v6) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__rptr_r[1U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v6;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v7) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__rptr_r[1U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v7;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v8) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__rptr_r[2U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v8;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v9) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__rptr_r[2U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v9;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v10) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__rptr_r[2U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v10;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v11) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__rptr_r[2U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v11;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v12) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__rptr_r[3U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v12;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v13) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__rptr_r[3U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v13;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v14) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__rptr_r[3U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v14;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v15) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__rptr_r[3U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v15;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v16) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__rptr_r[4U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v16;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v17) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__rptr_r[4U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v17;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v18) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__rptr_r[4U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v18;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v19) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__rptr_r[4U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v19;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v20) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__rptr_r[5U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v20;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v21) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__rptr_r[5U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v21;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v22) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__rptr_r[5U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v22;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v23) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__rptr_r[5U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v23;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v24) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__rptr_r[6U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v24;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v25) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__rptr_r[6U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v25;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v26) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__rptr_r[6U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v26;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v27) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__rptr_r[6U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v27;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v28) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__rptr_r[7U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v28;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v29) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__rptr_r[7U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v29;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v30) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__rptr_r[7U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v30;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v31) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__rptr_r[7U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v31;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v32) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__pend_r[0U] = 0U;
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__pend_r[1U] = 0U;
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__pend_r[2U] = 0U;
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__pend_r[3U] = 0U;
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__pend_r[4U] = 0U;
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__pend_r[5U] = 0U;
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__pend_r[6U] = 0U;
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__pend_r[7U] = 0U;
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__converged_r[0U] = 0U;
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__converged_r[1U] = 0U;
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__converged_r[2U] = 0U;
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__converged_r[3U] = 0U;
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__converged_r[4U] = 0U;
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__converged_r[5U] = 0U;
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__converged_r[6U] = 0U;
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__converged_r[7U] = 0U;
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__dev_ok_r[0U] = 0U;
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__dev_ok_r[1U] = 0U;
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__dev_ok_r[2U] = 0U;
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__dev_ok_r[3U] = 0U;
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__dev_ok_r[4U] = 0U;
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__dev_ok_r[5U] = 0U;
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__dev_ok_r[6U] = 0U;
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__dev_ok_r[7U] = 0U;
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__conv_ms_r[0U] = 0U;
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__conv_ms_r[1U] = 0U;
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__conv_ms_r[2U] = 0U;
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__conv_ms_r[3U] = 0U;
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__conv_ms_r[4U] = 0U;
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__conv_ms_r[5U] = 0U;
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__conv_ms_r[6U] = 0U;
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__conv_ms_r[7U] = 0U;
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__prefill_r[0U] = 1U;
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__prefill_r[1U] = 1U;
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__prefill_r[2U] = 1U;
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__prefill_r[3U] = 1U;
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__prefill_r[4U] = 1U;
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__prefill_r[5U] = 1U;
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__prefill_r[6U] = 1U;
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__prefill_r[7U] = 1U;
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__rptr_r[0U] = 0U;
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__rptr_r[1U] = 0U;
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__rptr_r[2U] = 0U;
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__rptr_r[3U] = 0U;
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__rptr_r[4U] = 0U;
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__rptr_r[5U] = 0U;
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__rptr_r[6U] = 0U;
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__rptr_r[7U] = 0U;
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__txc_pend_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__txc_pend_r;
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__stream_table__DOT__ovr_sid_r__v0) {
        vlSelfRef.milan_datapath__DOT__stream_table__DOT__ovr_sid_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__stream_table__DOT__ovr_sid_r__v0] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__stream_table__DOT__ovr_sid_r__v0;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__stream_table__DOT__ovr_sid_r__v1) {
        vlSelfRef.milan_datapath__DOT__stream_table__DOT__ovr_sid_r[0U] = 0ULL;
        vlSelfRef.milan_datapath__DOT__stream_table__DOT__ovr_sid_r[1U] = 0ULL;
        vlSelfRef.milan_datapath__DOT__stream_table__DOT__ovr_sid_r[2U] = 0ULL;
        vlSelfRef.milan_datapath__DOT__stream_table__DOT__ovr_sid_r[3U] = 0ULL;
        vlSelfRef.milan_datapath__DOT__stream_table__DOT__ovr_sid_r[4U] = 0ULL;
        vlSelfRef.milan_datapath__DOT__stream_table__DOT__ovr_sid_r[5U] = 0ULL;
        vlSelfRef.milan_datapath__DOT__stream_table__DOT__ovr_sid_r[6U] = 0ULL;
        vlSelfRef.milan_datapath__DOT__stream_table__DOT__ovr_sid_r[7U] = 0ULL;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__stream_table__DOT__ovr_armed_r__v0) {
        vlSelfRef.milan_datapath__DOT__stream_table__DOT__ovr_armed_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__stream_table__DOT__ovr_armed_r__v0] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__stream_table__DOT__ovr_armed_r__v0;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__stream_table__DOT__ovr_armed_r__v1) {
        vlSelfRef.milan_datapath__DOT__stream_table__DOT__ovr_armed_r[0U] = 0U;
        vlSelfRef.milan_datapath__DOT__stream_table__DOT__ovr_armed_r[1U] = 0U;
        vlSelfRef.milan_datapath__DOT__stream_table__DOT__ovr_armed_r[2U] = 0U;
        vlSelfRef.milan_datapath__DOT__stream_table__DOT__ovr_armed_r[3U] = 0U;
        vlSelfRef.milan_datapath__DOT__stream_table__DOT__ovr_armed_r[4U] = 0U;
        vlSelfRef.milan_datapath__DOT__stream_table__DOT__ovr_armed_r[5U] = 0U;
        vlSelfRef.milan_datapath__DOT__stream_table__DOT__ovr_armed_r[6U] = 0U;
        vlSelfRef.milan_datapath__DOT__stream_table__DOT__ovr_armed_r[7U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tf_wptr_r__v0) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tf_wptr_r[0U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tf_wptr_r__v0;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tf_wptr_r__v1) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tf_wptr_r[1U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tf_wptr_r__v1;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tf_wptr_r__v2) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tf_wptr_r[0U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tf_wptr_r[1U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tf_ram_r__v0) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tf_ram_r[0U][vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tf_ram_r__v0] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tf_ram_r__v0;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tf_ram_r__v1) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tf_ram_r[1U][vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tf_ram_r__v1] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tf_ram_r__v1;
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__st_tk_vld_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__st_tk_vld_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__st_tk_r[0U] 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__st_tk_r[0U];
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__st_tk_r[1U] 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__st_tk_r[1U];
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__st_tk_r[2U] 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__st_tk_r[2U];
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__st_tk_r[3U] 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__st_tk_r[3U];
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__st_tk_r[4U] 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__st_tk_r[4U];
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__st_ls_vld_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__st_ls_vld_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__st_ls_r[0U] 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__st_ls_r[0U];
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__st_ls_r[1U] 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__st_ls_r[1U];
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__st_ls_r[2U] 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__st_ls_r[2U];
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__st_ls_r[3U] 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__st_ls_r[3U];
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__st_ls_r[4U] 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__st_ls_r[4U];
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__tctx_chans_r__v0) {
        vlSelfRef.milan_datapath__DOT__tctx_chans_r[0U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__tctx_chans_r__v0;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__tctx_chans_r__v1) {
        vlSelfRef.milan_datapath__DOT__tctx_chans_r[1U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__tctx_chans_r__v1;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__tctx_chans_r__v2) {
        vlSelfRef.milan_datapath__DOT__tctx_chans_r[2U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__tctx_chans_r__v2;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__tctx_chans_r__v3) {
        vlSelfRef.milan_datapath__DOT__tctx_chans_r[3U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__tctx_chans_r__v3;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__tctx_chans_r__v4) {
        vlSelfRef.milan_datapath__DOT__tctx_chans_r[4U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__tctx_chans_r__v4;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__tctx_chans_r__v5) {
        vlSelfRef.milan_datapath__DOT__tctx_chans_r[5U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__tctx_chans_r__v5;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__tctx_chans_r__v6) {
        vlSelfRef.milan_datapath__DOT__tctx_chans_r[6U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__tctx_chans_r__v6;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__tctx_chans_r__v7) {
        vlSelfRef.milan_datapath__DOT__tctx_chans_r[7U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__tctx_chans_r__v7;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__tctx_chans_r__v8) {
        vlSelfRef.milan_datapath__DOT__tctx_chans_r[0U] = 2U;
        vlSelfRef.milan_datapath__DOT__tctx_chans_r[1U] = 2U;
        vlSelfRef.milan_datapath__DOT__tctx_chans_r[2U] = 2U;
        vlSelfRef.milan_datapath__DOT__tctx_chans_r[3U] = 2U;
        vlSelfRef.milan_datapath__DOT__tctx_chans_r[4U] = 2U;
        vlSelfRef.milan_datapath__DOT__tctx_chans_r[5U] = 2U;
        vlSelfRef.milan_datapath__DOT__tctx_chans_r[6U] = 2U;
        vlSelfRef.milan_datapath__DOT__tctx_chans_r[7U] = 2U;
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__adv_startup_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__adv_startup_r;
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__adv_st_r__v4) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__tpend_deadline_r[0U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__tpend_deadline_r__v0;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__tpend_r__v4) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__tpend_deadline_r[0U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__tpend_deadline_r__v1;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__tpend_r__v0) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__tpend_r[0U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__tpend_r__v1) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__tpend_r[0U] = 2U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__tpend_r__v2) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__tpend_r[0U] = 2U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__adv_st_r__v4) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__tpend_r[0U] = 1U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__tpend_r__v4) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__tpend_r[0U] = 1U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__adv_st_r__v5) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__tpend_r[0U] = 2U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__adv_st_r__v6) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__tpend_r[0U] = 2U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__adv_st_r__v9) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__tpend_deadline_r[0U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__tpend_r[0U] = 0U;
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__wr_ptr_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__wr_ptr_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_acmp_q__DOT__wr_ptr_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_acmp_q__DOT__wr_ptr_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_adp_q__DOT__wr_ptr_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_adp_q__DOT__wr_ptr_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_maap_q__DOT__wr_ptr_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_maap_q__DOT__wr_ptr_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_normalizer__DOT__txn_valid_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_normalizer__DOT__txn_valid_r;
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__mvrp_ram_r__v0) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__mvrp_ram_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__mvrp_ram_r__v0] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__mvrp_ram_r__v0;
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_maap_q__DOT__rd_ptr_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_maap_q__DOT__rd_ptr_r;
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_maap_q__DOT__mem_r__v0) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_maap_q__DOT__mem_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_maap_q__DOT__mem_r__v0][0U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_maap_q__DOT__mem_r__v0[0U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_maap_q__DOT__mem_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_maap_q__DOT__mem_r__v0][1U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_maap_q__DOT__mem_r__v0[1U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_maap_q__DOT__mem_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_maap_q__DOT__mem_r__v0][2U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_maap_q__DOT__mem_r__v0[2U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_maap_q__DOT__mem_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_maap_q__DOT__mem_r__v0][3U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_maap_q__DOT__mem_r__v0[3U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_maap_q__DOT__mem_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_maap_q__DOT__mem_r__v0][4U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_maap_q__DOT__mem_r__v0[4U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_maap_q__DOT__mem_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_maap_q__DOT__mem_r__v0][5U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_maap_q__DOT__mem_r__v0[5U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_maap_q__DOT__mem_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_maap_q__DOT__mem_r__v0][6U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_maap_q__DOT__mem_r__v0[6U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_maap_q__DOT__mem_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_maap_q__DOT__mem_r__v0][7U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_maap_q__DOT__mem_r__v0[7U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_maap_q__DOT__mem_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_maap_q__DOT__mem_r__v0][8U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_maap_q__DOT__mem_r__v0[8U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_maap_q__DOT__mem_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_maap_q__DOT__mem_r__v0][9U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_maap_q__DOT__mem_r__v0[9U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_maap_q__DOT__mem_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_maap_q__DOT__mem_r__v0][10U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_maap_q__DOT__mem_r__v0[10U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_maap_q__DOT__mem_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_maap_q__DOT__mem_r__v0][11U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_maap_q__DOT__mem_r__v0[11U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_maap_q__DOT__mem_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_maap_q__DOT__mem_r__v0][12U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_maap_q__DOT__mem_r__v0[12U];
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__msrp_ram_r__v0) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__msrp_ram_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__msrp_ram_r__v0][0U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__msrp_ram_r__v0[0U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__msrp_ram_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__msrp_ram_r__v0][1U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__msrp_ram_r__v0[1U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__msrp_ram_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__msrp_ram_r__v0][2U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__msrp_ram_r__v0[2U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__msrp_ram_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__msrp_ram_r__v0][3U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__msrp_ram_r__v0[3U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__msrp_ram_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__msrp_ram_r__v0][4U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__msrp_ram_r__v0[4U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__msrp_ram_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__msrp_ram_r__v0][5U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__msrp_ram_r__v0[5U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__msrp_ram_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__msrp_ram_r__v0][6U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__msrp_ram_r__v0[6U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__msrp_ram_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__msrp_ram_r__v0][7U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__msrp_ram_r__v0[7U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__msrp_ram_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__msrp_ram_r__v0][8U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__msrp_ram_r__v0[8U];
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_decoder__DOT__tp_ram__v0) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_decoder__DOT__tp_ram[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_decoder__DOT__tp_ram__v0] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_decoder__DOT__tp_ram__v0;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__rec_ram_r__v0) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__rec_ram_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__rec_ram_r__v0][0U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__rec_ram_r__v0[0U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__rec_ram_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__rec_ram_r__v0][1U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__rec_ram_r__v0[1U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__rec_ram_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__rec_ram_r__v0][2U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__rec_ram_r__v0[2U];
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__disc_rec_r__v0) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__disc_rec_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__disc_rec_r__v0] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__disc_rec_r__v0;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__vq_r__v0) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__vq_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__vq_r__v0] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__vq_r__v0;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__vq_r__v1) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__vq_r[0U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__vq_r[1U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__vq_r[2U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__vq_r[3U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__vq_r[4U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__vq_r[5U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__vq_r[6U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__vq_r[7U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__vq_r[8U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__vq_r[9U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__vq_r[10U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__vq_r[11U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__vq_r[12U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__vq_r[13U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__vq_r[14U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__vq_r[15U] = 0U;
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__vrptr_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__vrptr_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxf_vld_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxf_vld_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_prev_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_prev_r;
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__skid_addr_r__v0) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__skid_addr_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__chan_map_capture__DOT__skid_addr_r__v0] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__chan_map_capture__DOT__skid_addr_r__v0;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__skid_addr_r__v1) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__skid_addr_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__chan_map_capture__DOT__skid_addr_r__v1] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__chan_map_capture__DOT__skid_addr_r__v1;
    }
    vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__skid_rp_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__chan_map_capture__DOT__skid_rp_r;
    vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__bytes_in 
        = vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_parser__DOT__bytes_in;
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__tout_r__v0) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__tout_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__tout_r__v0] = 0x00faU;
    }
    vlSelfRef.milan_datapath__DOT__link_guard__DOT__tx_dead_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__link_guard__DOT__tx_dead_r;
    vlSelfRef.milan_datapath__DOT__link_guard__DOT__rx_dead_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__link_guard__DOT__rx_dead_r;
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__txs_r__v0) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__txs_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__txs_r__v0] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__txs_r__v0;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__4__KET____DOT__u_rx_slots__DOT__len_r__v0) {
        milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__4__KET____DOT__u_rx_slots__DOT__len_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__4__KET____DOT__u_rx_slots__DOT__len_r__v0] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__4__KET____DOT__u_rx_slots__DOT__len_r__v0;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__4__KET____DOT__u_rx_slots__DOT__len_r__v1) {
        milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__4__KET____DOT__u_rx_slots__DOT__len_r[0U] = 0U;
        milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__4__KET____DOT__u_rx_slots__DOT__len_r[1U] = 0U;
        milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__4__KET____DOT__u_rx_slots__DOT__len_r[2U] = 0U;
        milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__4__KET____DOT__u_rx_slots__DOT__len_r[3U] = 0U;
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__4__KET____DOT__u_rx_slots__DOT__wr_ptr_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__4__KET____DOT__u_rx_slots__DOT__wr_ptr_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__4__KET____DOT__u_rx_slots__DOT__wr_active_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__4__KET____DOT__u_rx_slots__DOT__wr_active_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__4__KET____DOT__u_rx_slots__DOT__occupied_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__4__KET____DOT__u_rx_slots__DOT__occupied_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__2__KET____DOT__u_rx_slots__DOT__wr_ptr_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__2__KET____DOT__u_rx_slots__DOT__wr_ptr_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__2__KET____DOT__u_rx_slots__DOT__wr_active_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__2__KET____DOT__u_rx_slots__DOT__wr_active_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__2__KET____DOT__u_rx_slots__DOT__occupied_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__2__KET____DOT__u_rx_slots__DOT__occupied_r;
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__1__KET____DOT__u_rx_slots__DOT__len_r__v0) {
        milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__1__KET____DOT__u_rx_slots__DOT__len_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__1__KET____DOT__u_rx_slots__DOT__len_r__v0] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__1__KET____DOT__u_rx_slots__DOT__len_r__v0;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__1__KET____DOT__u_rx_slots__DOT__len_r__v1) {
        milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__1__KET____DOT__u_rx_slots__DOT__len_r[0U] = 0U;
        milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__1__KET____DOT__u_rx_slots__DOT__len_r[1U] = 0U;
        milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__1__KET____DOT__u_rx_slots__DOT__len_r[2U] = 0U;
        milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__1__KET____DOT__u_rx_slots__DOT__len_r[3U] = 0U;
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__1__KET____DOT__u_rx_slots__DOT__wr_ptr_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__1__KET____DOT__u_rx_slots__DOT__wr_ptr_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__1__KET____DOT__u_rx_slots__DOT__wr_active_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__1__KET____DOT__u_rx_slots__DOT__wr_active_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__1__KET____DOT__u_rx_slots__DOT__occupied_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__1__KET____DOT__u_rx_slots__DOT__occupied_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__DOT__wr_ptr_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__DOT__wr_ptr_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__DOT__wr_active_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__DOT__wr_active_r;
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__DOT__len_r__v0) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__DOT__len_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__DOT__len_r__v0] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__DOT__len_r__v0;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__DOT__len_r__v1) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__DOT__len_r[0U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__DOT__len_r[1U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__DOT__len_r[2U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__DOT__len_r[3U] = 0U;
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__DOT__occupied_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__DOT__occupied_r;
    vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__yl_hold_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__yl_hold_r;
    vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__busy_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__busy_r;
    vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__acc_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__acc_r;
    vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__xl1_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__xl1_r;
    vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__yl1_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__yl1_r;
    vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__xr1_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__xr1_r;
    vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__yr1_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__yr1_r;
    vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__step_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__step_r;
    vlSelfRef.milan_datapath__DOT__tone_gen_media__DOT__idx_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__tone_gen_media__DOT__idx_r;
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__0__KET____DOT__u_rx_slots__DOT__len_r__v0) {
        milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__0__KET____DOT__u_rx_slots__DOT__len_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__0__KET____DOT__u_rx_slots__DOT__len_r__v0] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__0__KET____DOT__u_rx_slots__DOT__len_r__v0;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__0__KET____DOT__u_rx_slots__DOT__len_r__v1) {
        milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__0__KET____DOT__u_rx_slots__DOT__len_r[0U] = 0U;
        milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__0__KET____DOT__u_rx_slots__DOT__len_r[1U] = 0U;
        milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__0__KET____DOT__u_rx_slots__DOT__len_r[2U] = 0U;
        milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__0__KET____DOT__u_rx_slots__DOT__len_r[3U] = 0U;
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__0__KET____DOT__u_rx_slots__DOT__wr_ptr_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__0__KET____DOT__u_rx_slots__DOT__wr_ptr_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__0__KET____DOT__u_rx_slots__DOT__wr_active_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__0__KET____DOT__u_rx_slots__DOT__wr_active_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__0__KET____DOT__u_rx_slots__DOT__occupied_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__0__KET____DOT__u_rx_slots__DOT__occupied_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__set_q_r 
        = ((IData)(vlSelfRef.axis_resetn) && (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__gnt_opmut_w));
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__tslot_r__v0) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__tslot_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__tslot_r__v0] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__tslot_r__v0;
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tm_rr_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tm_rr_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__cad_pend_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__cad_pend_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tf_q_r[0U] 
        = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tf_q_r__v0;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tf_q_r[1U] 
        = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tf_q_r__v1;
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tf_rptr_r__v0) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tf_rptr_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tf_rptr_r__v0] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tf_rptr_r__v0;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tf_rptr_r__v1) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tf_rptr_r[0U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tf_cnt_r__v0) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tf_cnt_r[0U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tf_cnt_r__v0;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tf_cnt_r[1U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tf_cnt_r__v1;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tf_rptr_r__v2) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tf_rptr_r[1U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tf_cnt_r[0U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tf_cnt_r__v3) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tf_cnt_r[1U] = 0U;
    }
    vlSelfRef.milan_datapath__DOT__talker_diag__DOT__seen_f_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__talker_diag__DOT__seen_f_r;
    vlSelfRef.milan_datapath__DOT__talker_diag__DOT__seen_tu_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__talker_diag__DOT__seen_tu_r;
    vlSelfRef.milan_datapath__DOT__talker_diag__DOT__seen_mr_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__talker_diag__DOT__seen_mr_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__ld_ok_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__ld_ok_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_pend_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_pend_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_st_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_st_r;
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_trace__DOT__mem_r__v0) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_trace__DOT__mem_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_trace__DOT__mem_r__v0][0U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_trace__DOT__mem_r__v0[0U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_trace__DOT__mem_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_trace__DOT__mem_r__v0][1U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_trace__DOT__mem_r__v0[1U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_trace__DOT__mem_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_trace__DOT__mem_r__v0][2U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_trace__DOT__mem_r__v0[2U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_trace__DOT__mem_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_trace__DOT__mem_r__v0][3U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_trace__DOT__mem_r__v0[3U];
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__ival_ann_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__ival_ann_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__draw_req_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__draw_req_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__w_st_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__w_st_r;
    vlSelfRef.milan_datapath__DOT__link_guard__DOT__bounced_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__link_guard__DOT__bounced_r;
    vlSelfRef.milan_datapath__DOT__link_guard__DOT__settle_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__link_guard__DOT__settle_r;
    vlSelfRef.milan_datapath__DOT__link_guard__DOT__state_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__link_guard__DOT__state_r;
    vlSelfRef.milan_datapath__DOT__link_guard__DOT__bounce_cnt_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__link_guard__DOT__bounce_cnt_r;
    vlSelfRef.milan_datapath__DOT__src_pend_r = vlSelfRef.__Vdly__milan_datapath__DOT__src_pend_r;
    vlSelfRef.milan_datapath__DOT__src_band_ticks_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__src_band_ticks_r;
    vlSelfRef.milan_datapath__DOT__src_eng_ticks_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__src_eng_ticks_r;
    vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__active_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__active_r;
    vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__stg_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__stg_r;
    vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__samples_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__samples_r;
    vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__timeouts_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__timeouts_r;
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__last_r__v0) {
        vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__max_r[0U] = 0U;
        vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__max_r[1U] = 0U;
        vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__max_r[2U] = 0U;
        vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__last_r[0U] = 0U;
        vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__last_r[1U] = 0U;
        vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__last_r[2U] = 0U;
        vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__min_r[0U] = 0xffffU;
        vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__min_r[1U] = 0xffffU;
        vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__min_r[2U] = 0xffffU;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__max_r__v3) {
        vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__max_r[0U] 
            = __VdlyVal__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__max_r__v3;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__max_r__v4) {
        vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__max_r[1U] 
            = __VdlyVal__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__max_r__v4;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__max_r__v5) {
        vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__max_r[2U] 
            = __VdlyVal__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__max_r__v5;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__last_r__v3) {
        vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__last_r[0U] 
            = __VdlyVal__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__last_r__v3;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__last_r__v4) {
        vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__last_r[1U] 
            = __VdlyVal__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__last_r__v4;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__last_r__v5) {
        vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__last_r[2U] 
            = __VdlyVal__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__last_r__v5;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__last_r__v6) {
        vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__last_r[0U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__last_r__v7) {
        vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__last_r[1U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__last_r__v8) {
        vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__last_r[2U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__min_r__v3) {
        vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__min_r[0U] 
            = __VdlyVal__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__min_r__v3;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__min_r__v4) {
        vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__min_r[1U] 
            = __VdlyVal__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__min_r__v4;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__min_r__v5) {
        vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__min_r[2U] 
            = __VdlyVal__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__min_r__v5;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__last_r__v6) {
        vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__min_r[0U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__last_r__v7) {
        vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__min_r[1U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__last_r__v8) {
        vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__min_r[2U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__last_r__v9) {
        vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__max_r[0U] = 0U;
        vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__max_r[1U] = 0U;
        vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__max_r[2U] = 0U;
        vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__last_r[0U] = 0U;
        vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__last_r[1U] = 0U;
        vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__last_r[2U] = 0U;
        vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__min_r[0U] = 0xffffU;
        vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__min_r[1U] = 0xffffU;
        vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__min_r[2U] = 0xffffU;
    }
    vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__cyc_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__cyc_r;
    vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__active_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__active_r;
    vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__stg_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__stg_r;
    vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__samples_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__samples_r;
    vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__timeouts_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__timeouts_r;
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__last_r__v0) {
        vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__max_r[0U] = 0U;
        vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__max_r[1U] = 0U;
        vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__max_r[2U] = 0U;
        vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__last_r[0U] = 0U;
        vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__last_r[1U] = 0U;
        vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__last_r[2U] = 0U;
        vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__min_r[0U] = 0xffffU;
        vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__min_r[1U] = 0xffffU;
        vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__min_r[2U] = 0xffffU;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__max_r__v3) {
        vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__max_r[0U] 
            = __VdlyVal__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__max_r__v3;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__max_r__v4) {
        vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__max_r[1U] 
            = __VdlyVal__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__max_r__v4;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__max_r__v5) {
        vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__max_r[2U] 
            = __VdlyVal__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__max_r__v5;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__last_r__v3) {
        vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__last_r[0U] 
            = __VdlyVal__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__last_r__v3;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__last_r__v4) {
        vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__last_r[1U] 
            = __VdlyVal__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__last_r__v4;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__last_r__v5) {
        vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__last_r[2U] 
            = __VdlyVal__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__last_r__v5;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__last_r__v6) {
        vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__last_r[0U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__last_r__v7) {
        vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__last_r[1U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__last_r__v8) {
        vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__last_r[2U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__min_r__v3) {
        vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__min_r[0U] 
            = __VdlyVal__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__min_r__v3;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__min_r__v4) {
        vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__min_r[1U] 
            = __VdlyVal__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__min_r__v4;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__min_r__v5) {
        vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__min_r[2U] 
            = __VdlyVal__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__min_r__v5;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__last_r__v6) {
        vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__min_r[0U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__last_r__v7) {
        vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__min_r[1U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__last_r__v8) {
        vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__min_r[2U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__last_r__v9) {
        vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__max_r[0U] = 0U;
        vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__max_r[1U] = 0U;
        vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__max_r[2U] = 0U;
        vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__last_r[0U] = 0U;
        vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__last_r[1U] = 0U;
        vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__last_r[2U] = 0U;
        vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__min_r[0U] = 0xffffU;
        vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__min_r[1U] = 0xffffU;
        vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__min_r[2U] = 0xffffU;
    }
    vlSelfRef.milan_datapath__DOT__csr__DOT__cmrd_flush_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__csr__DOT__cmrd_flush_r;
    vlSelfRef.milan_datapath__DOT__csr__DOT__cmrd_wd_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__csr__DOT__cmrd_wd_r;
    vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tickdiv_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tickdiv_r;
    vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__timer_ms_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__timer_ms_r;
    vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__probe_left_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__probe_left_r;
    vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat_r;
    vlSelfRef.milan_datapath__DOT__maap_conflicts = vlSelfRef.__Vdly__milan_datapath__DOT__maap_conflicts;
    vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_busy_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_busy_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__rejoin_pend_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__rejoin_pend_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vj_pend_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vj_pend_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vl_pend_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vl_pend_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vj_pend_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vj_pend_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vl_pend_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vl_pend_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__done_seen_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__done_seen_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__bcnt_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__bcnt_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__plen_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__plen_r;
    vlSelfRef.milan_datapath__DOT__csr__DOT__snap_st_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__csr__DOT__snap_st_r;
    vlSelfRef.milan_datapath__DOT__csr__DOT__snap_req_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__csr__DOT__snap_req_r;
    vlSelfRef.milan_datapath__DOT__csr__DOT__snap_m8_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__csr__DOT__snap_m8_r;
    vlSelfRef.milan_datapath__DOT__csr__DOT__snap_wi_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__csr__DOT__snap_wi_r;
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__csr__DOT__snap_shadow_r__v0) {
        vlSelfRef.milan_datapath__DOT__csr__DOT__snap_shadow_r[11U] 
            = __VdlyVal__milan_datapath__DOT__csr__DOT__snap_shadow_r__v0;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__csr__DOT__snap_shadow_r__v1) {
        vlSelfRef.milan_datapath__DOT__csr__DOT__snap_shadow_r[0U] 
            = __VdlyVal__milan_datapath__DOT__csr__DOT__snap_shadow_r__v1;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__csr__DOT__snap_shadow_r__v2) {
        vlSelfRef.milan_datapath__DOT__csr__DOT__snap_shadow_r[11U] 
            = __VdlyVal__milan_datapath__DOT__csr__DOT__snap_shadow_r__v2;
        vlSelfRef.milan_datapath__DOT__csr__DOT__snap_shadow_r[0U] 
            = __VdlyVal__milan_datapath__DOT__csr__DOT__snap_shadow_r__v3;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__csr__DOT__snap_shadow_r__v4) {
        vlSelfRef.milan_datapath__DOT__csr__DOT__snap_shadow_r[__VdlyDim0__milan_datapath__DOT__csr__DOT__snap_shadow_r__v4] 
            = __VdlyVal__milan_datapath__DOT__csr__DOT__snap_shadow_r__v4;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__csr__DOT__snap_shadow_r__v5) {
        vlSelfRef.milan_datapath__DOT__csr__DOT__snap_shadow_r[0U] 
            = __VdlyVal__milan_datapath__DOT__csr__DOT__snap_shadow_r__v5;
        vlSelfRef.milan_datapath__DOT__csr__DOT__snap_shadow_r[1U] = 0xdeaddeadU;
        vlSelfRef.milan_datapath__DOT__csr__DOT__snap_shadow_r[2U] = 0xdeaddeadU;
        vlSelfRef.milan_datapath__DOT__csr__DOT__snap_shadow_r[3U] = 0xdeaddeadU;
        vlSelfRef.milan_datapath__DOT__csr__DOT__snap_shadow_r[4U] = 0xdeaddeadU;
        vlSelfRef.milan_datapath__DOT__csr__DOT__snap_shadow_r[5U] = 0xdeaddeadU;
        vlSelfRef.milan_datapath__DOT__csr__DOT__snap_shadow_r[6U] = 0xdeaddeadU;
        vlSelfRef.milan_datapath__DOT__csr__DOT__snap_shadow_r[7U] = 0xdeaddeadU;
        vlSelfRef.milan_datapath__DOT__csr__DOT__snap_shadow_r[8U] = 0xdeaddeadU;
        vlSelfRef.milan_datapath__DOT__csr__DOT__snap_shadow_r[9U] = 0xdeaddeadU;
        vlSelfRef.milan_datapath__DOT__csr__DOT__snap_shadow_r[10U] = 0xdeaddeadU;
        vlSelfRef.milan_datapath__DOT__csr__DOT__snap_shadow_r[11U] 
            = __VdlyVal__milan_datapath__DOT__csr__DOT__snap_shadow_r__v16;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__csr__DOT__snap_shadow_r__v17) {
        vlSelfRef.milan_datapath__DOT__csr__DOT__snap_shadow_r[0U] 
            = __VdlyVal__milan_datapath__DOT__csr__DOT__snap_shadow_r__v17;
        vlSelfRef.milan_datapath__DOT__csr__DOT__snap_shadow_r[1U] 
            = __VdlyVal__milan_datapath__DOT__csr__DOT__snap_shadow_r__v18;
        vlSelfRef.milan_datapath__DOT__csr__DOT__snap_shadow_r[2U] 
            = __VdlyVal__milan_datapath__DOT__csr__DOT__snap_shadow_r__v19;
        vlSelfRef.milan_datapath__DOT__csr__DOT__snap_shadow_r[3U] 
            = __VdlyVal__milan_datapath__DOT__csr__DOT__snap_shadow_r__v20;
        vlSelfRef.milan_datapath__DOT__csr__DOT__snap_shadow_r[4U] 
            = __VdlyVal__milan_datapath__DOT__csr__DOT__snap_shadow_r__v21;
        vlSelfRef.milan_datapath__DOT__csr__DOT__snap_shadow_r[5U] 
            = __VdlyVal__milan_datapath__DOT__csr__DOT__snap_shadow_r__v22;
        vlSelfRef.milan_datapath__DOT__csr__DOT__snap_shadow_r[6U] 
            = __VdlyVal__milan_datapath__DOT__csr__DOT__snap_shadow_r__v23;
        vlSelfRef.milan_datapath__DOT__csr__DOT__snap_shadow_r[7U] 
            = __VdlyVal__milan_datapath__DOT__csr__DOT__snap_shadow_r__v24;
        vlSelfRef.milan_datapath__DOT__csr__DOT__snap_shadow_r[8U] 
            = __VdlyVal__milan_datapath__DOT__csr__DOT__snap_shadow_r__v25;
        vlSelfRef.milan_datapath__DOT__csr__DOT__snap_shadow_r[9U] 
            = __VdlyVal__milan_datapath__DOT__csr__DOT__snap_shadow_r__v26;
        vlSelfRef.milan_datapath__DOT__csr__DOT__snap_shadow_r[10U] 
            = __VdlyVal__milan_datapath__DOT__csr__DOT__snap_shadow_r__v27;
        vlSelfRef.milan_datapath__DOT__csr__DOT__snap_shadow_r[11U] 
            = __VdlyVal__milan_datapath__DOT__csr__DOT__snap_shadow_r__v28;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__csr__DOT__snap_shadow_r__v29) {
        vlSelfRef.milan_datapath__DOT__csr__DOT__snap_shadow_r[1U] = 0xdeaddeadU;
        vlSelfRef.milan_datapath__DOT__csr__DOT__snap_shadow_r[2U] = 0xdeaddeadU;
        vlSelfRef.milan_datapath__DOT__csr__DOT__snap_shadow_r[3U] = 0xdeaddeadU;
        vlSelfRef.milan_datapath__DOT__csr__DOT__snap_shadow_r[4U] = 0xdeaddeadU;
        vlSelfRef.milan_datapath__DOT__csr__DOT__snap_shadow_r[5U] = 0xdeaddeadU;
        vlSelfRef.milan_datapath__DOT__csr__DOT__snap_shadow_r[6U] = 0xdeaddeadU;
        vlSelfRef.milan_datapath__DOT__csr__DOT__snap_shadow_r[7U] = 0xdeaddeadU;
        vlSelfRef.milan_datapath__DOT__csr__DOT__snap_shadow_r[8U] = 0xdeaddeadU;
        vlSelfRef.milan_datapath__DOT__csr__DOT__snap_shadow_r[9U] = 0xdeaddeadU;
        vlSelfRef.milan_datapath__DOT__csr__DOT__snap_shadow_r[10U] = 0xdeaddeadU;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__csr__DOT__snap_shadow_r__v39) {
        vlSelfRef.milan_datapath__DOT__csr__DOT__snap_shadow_r[0U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__csr__DOT__snap_shadow_r__v40) {
        vlSelfRef.milan_datapath__DOT__csr__DOT__snap_shadow_r[1U] = 0U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__snap_shadow_r[2U] = 0U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__snap_shadow_r[3U] = 0U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__snap_shadow_r[4U] = 0U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__snap_shadow_r[5U] = 0U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__snap_shadow_r[6U] = 0U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__snap_shadow_r[7U] = 0U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__snap_shadow_r[8U] = 0U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__snap_shadow_r[9U] = 0U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__snap_shadow_r[10U] = 0U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__snap_shadow_r[11U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__csr__DOT__snap_shadow_r__v51) {
        vlSelfRef.milan_datapath__DOT__csr__DOT__snap_shadow_r[0U] = 0U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__snap_shadow_r[1U] = 0U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__snap_shadow_r[2U] = 0U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__snap_shadow_r[3U] = 0U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__snap_shadow_r[4U] = 0U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__snap_shadow_r[5U] = 0U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__snap_shadow_r[6U] = 0U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__snap_shadow_r[7U] = 0U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__snap_shadow_r[8U] = 0U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__snap_shadow_r[9U] = 0U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__snap_shadow_r[10U] = 0U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__snap_shadow_r[11U] = 0U;
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__msg_open_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__msg_open_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__hold_valid_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__hold_valid_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__msg_type_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__msg_type_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__rd_idx_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__rd_idx_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_open_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_open_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_last_r[0U] 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_last_r[0U];
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_last_r[1U] 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_last_r[1U];
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_last_r[2U] 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_last_r[2U];
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_last_r[3U] 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_last_r[3U];
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_last_r[4U] 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_last_r[4U];
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_last_r[5U] 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_last_r[5U];
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_last_r[6U] 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_last_r[6U];
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_last_r[7U] 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_last_r[7U];
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_last_r[8U] 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_last_r[8U];
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__cnt_mvrp_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__cnt_mvrp_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__join_pend_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__join_pend_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_len_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_len_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__bidx_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__bidx_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__waddr_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__waddr_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_type_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_type_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__st_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__st_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxf_drop_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxf_drop_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_drop_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_drop_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__svc_drop_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__svc_drop_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__arm_drop_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__arm_drop_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__mrp_drop_w 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__mrp_drop_w;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__active_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__active_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__aecp_stall_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__aecp_stall_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__adp_stall_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__adp_stall_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__acmp_stall_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__acmp_stall_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__cnt_len_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__cnt_len_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__0__KET____DOT__u_rx_slots__DOT__ovr_cnt_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__0__KET____DOT__u_rx_slots__DOT__ovr_cnt_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__cnt_sub_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__cnt_sub_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__cnt_ver_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__cnt_ver_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__cnt_da_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__cnt_da_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__cnt_et_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__cnt_et_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__seeded_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__seeded_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_trace__DOT__wr_count_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_trace__DOT__wr_count_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_adp_q__DOT__cnt_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_adp_q__DOT__cnt_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_acmp_q__DOT__cnt_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_acmp_q__DOT__cnt_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__cnt_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__cnt_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__valid_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__valid_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__out_valid_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__out_valid_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_acmp_q__DOT__out_valid_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_acmp_q__DOT__out_valid_r;
    vlSelfRef.milan_datapath__DOT__csr__DOT__dflt_q 
        = vlSelfRef.milan_datapath__DOT__csr__DOT__dflt_rom
        [(0x000001ffU & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__sweep_cnt))];
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__arb_gnt_cnt_w[0U] 
        = (IData)((((QData)((IData)((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__cnt_r[3U]) 
                                      << 0x00000010U) 
                                     | vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__cnt_r[2U]))) 
                    << 0x00000020U) | (QData)((IData)(
                                                      (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__cnt_r[1U]) 
                                                        << 0x00000010U) 
                                                       | vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__cnt_r[0U])))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__arb_gnt_cnt_w[1U] 
        = (IData)(((((QData)((IData)((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__cnt_r[3U]) 
                                       << 0x00000010U) 
                                      | vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__cnt_r[2U]))) 
                     << 0x00000020U) | (QData)((IData)(
                                                       (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__cnt_r[1U]) 
                                                         << 0x00000010U) 
                                                        | vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__cnt_r[0U])))) 
                   >> 0x00000020U));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__arb_gnt_cnt_w[2U] 
        = (IData)((((QData)((IData)((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__cnt_r[7U]) 
                                      << 0x00000010U) 
                                     | vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__cnt_r[6U]))) 
                    << 0x00000020U) | (QData)((IData)(
                                                      (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__cnt_r[5U]) 
                                                        << 0x00000010U) 
                                                       | vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__cnt_r[4U])))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__arb_gnt_cnt_w[3U] 
        = (IData)(((((QData)((IData)((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__cnt_r[7U]) 
                                       << 0x00000010U) 
                                      | vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__cnt_r[6U]))) 
                     << 0x00000020U) | (QData)((IData)(
                                                       (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__cnt_r[5U]) 
                                                         << 0x00000010U) 
                                                        | vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__cnt_r[4U])))) 
                   >> 0x00000020U));
    vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__skid_free_w 
        = (7U & (((IData)(4U) - (IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__skid_cnt_r)) 
                 + (1U & (- (IData)((0U != (IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__skid_cnt_r)))))));
    vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pbase_w[0U] = 0U;
    vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pbase_w[1U] 
        = (0x0000003fU & ((IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pbase_w[0U]) 
                          + (7U & (vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__chans_r[0U] 
                                   >> 1U))));
    vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pbase_w[2U] 
        = (0x0000003fU & ((IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pbase_w[1U]) 
                          + (7U & (vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__chans_r[1U] 
                                   >> 1U))));
    vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pbase_w[3U] 
        = (0x0000003fU & ((IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pbase_w[2U]) 
                          + (7U & (vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__chans_r[2U] 
                                   >> 1U))));
    vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pbase_w[4U] 
        = (0x0000003fU & ((IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pbase_w[3U]) 
                          + (7U & (vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__chans_r[3U] 
                                   >> 1U))));
    vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pbase_w[5U] 
        = (0x0000003fU & ((IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pbase_w[4U]) 
                          + (7U & (vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__chans_r[4U] 
                                   >> 1U))));
    vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pbase_w[6U] 
        = (0x0000003fU & ((IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pbase_w[5U]) 
                          + (7U & (vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__chans_r[5U] 
                                   >> 1U))));
    vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pbase_w[7U] 
        = (0x0000003fU & ((IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pbase_w[6U]) 
                          + (7U & (vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__chans_r[6U] 
                                   >> 1U))));
    vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pbase_w[8U] 
        = (0x0000003fU & ((IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pbase_w[7U]) 
                          + (7U & (vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__chans_r[7U] 
                                   >> 1U))));
    vlSelfRef.milan_datapath__DOT__pp_aecp_identify_w 
        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__ident_r[0U];
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_236 = (1U 
                                                  & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__cap_att_r)));
    if ((1U & (~ (IData)(vlSelfRef.axis_resetn)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__ctl_fifo__DOT__mark_frame_reg = 0U;
    }
    vlSelfRef.media_lrclk_o = vlSelfRef.milan_datapath__DOT__media_lrclk_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__aged_w 
        = ((((((0x0aU == vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__age_r[7U]) 
               << 3U) | ((0x0aU == vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__age_r[6U]) 
                         << 2U)) | (((0x0aU == vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__age_r[5U]) 
                                     << 1U) | (0x0aU 
                                               == vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__age_r[4U]))) 
            << 4U) | ((((0x0aU == vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__age_r[3U]) 
                        << 3U) | ((0x0aU == vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__age_r[2U]) 
                                  << 2U)) | (((0x0aU 
                                               == vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__age_r[1U]) 
                                              << 1U) 
                                             | (0x0aU 
                                                == vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__age_r[0U]))));
    vlSelfRef.milan_datapath__DOT__csr__DOT__rstn_seen_r 
        = vlSelfRef.axis_resetn;
    vlSelfRef.milan_datapath__DOT__stats_counts[0U] 
        = vlSelfRef.milan_datapath__DOT__ethernet_counters__DOT____Vcellout__event_counter_gen__BRA__0__KET____DOT__counter_inst__count;
    vlSelfRef.milan_datapath__DOT__stats_counts[1U] 
        = vlSelfRef.milan_datapath__DOT__ethernet_counters__DOT____Vcellout__event_counter_gen__BRA__1__KET____DOT__counter_inst__count;
    vlSelfRef.milan_datapath__DOT__stats_counts[2U] 
        = (IData)((((QData)((IData)(vlSelfRef.milan_datapath__DOT__ethernet_counters__DOT____Vcellout__event_counter_gen__BRA__3__KET____DOT__counter_inst__count)) 
                    << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__ethernet_counters__DOT____Vcellout__event_counter_gen__BRA__2__KET____DOT__counter_inst__count))));
    vlSelfRef.milan_datapath__DOT__stats_counts[3U] 
        = (IData)(((((QData)((IData)(vlSelfRef.milan_datapath__DOT__ethernet_counters__DOT____Vcellout__event_counter_gen__BRA__3__KET____DOT__counter_inst__count)) 
                     << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__ethernet_counters__DOT____Vcellout__event_counter_gen__BRA__2__KET____DOT__counter_inst__count))) 
                   >> 0x00000020U));
    vlSelfRef.milan_datapath__DOT__stats_counts[4U] 
        = vlSelfRef.milan_datapath__DOT__ethernet_counters__DOT____Vcellout__event_counter_gen__BRA__4__KET____DOT__counter_inst__count;
    vlSelfRef.milan_datapath__DOT__stats_counts[5U] 
        = vlSelfRef.milan_datapath__DOT__ethernet_counters__DOT____Vcellout__event_counter_gen__BRA__5__KET____DOT__counter_inst__count;
    vlSelfRef.milan_datapath__DOT__stats_counts[6U] 
        = (IData)((((QData)((IData)(vlSelfRef.milan_datapath__DOT__ethernet_counters__DOT____Vcellout__event_counter_gen__BRA__7__KET____DOT__counter_inst__count)) 
                    << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__ethernet_counters__DOT____Vcellout__event_counter_gen__BRA__6__KET____DOT__counter_inst__count))));
    vlSelfRef.milan_datapath__DOT__stats_counts[7U] 
        = (IData)(((((QData)((IData)(vlSelfRef.milan_datapath__DOT__ethernet_counters__DOT____Vcellout__event_counter_gen__BRA__7__KET____DOT__counter_inst__count)) 
                     << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__ethernet_counters__DOT____Vcellout__event_counter_gen__BRA__6__KET____DOT__counter_inst__count))) 
                   >> 0x00000020U));
    vlSelfRef.milan_datapath__DOT__stats_counts[8U] 
        = vlSelfRef.milan_datapath__DOT__ethernet_counters__DOT____Vcellout__event_counter_gen__BRA__8__KET____DOT__counter_inst__count;
    vlSelfRef.milan_datapath__DOT__csr__DOT__mac_reinit_q 
        = ((IData)(vlSelfRef.axis_resetn) & (IData)(vlSelfRef.o_mac_reinit));
    vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__pop_ret_v_r 
        = ((IData)(vlSelfRef.axis_resetn) && ((IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__pop_act_w) 
                                              & (~ 
                                                 (vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__flush_clr_w 
                                                  >> 
                                                  (0x0000001fU 
                                                   & (IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__pop_idx_r))))));
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
    vlSelfRef.milan_datapath__DOT__crf_mr_toggle_p_w 
        = ((IData)(vlSelfRef.axis_resetn) && (((IData)(vlSelfRef.milan_datapath__DOT__crf_rx__DOT__w_ev_mr_w) 
                                               & (~ (IData)(vlSelfRef.milan_datapath__DOT__crf_rx__DOT__w_bind_rise_w))) 
                                              & (~ 
                                                 ((IData)(vlSelfRef.milan_datapath__DOT__acmpl_stopped_v_w) 
                                                  >> 8U))));
    vlSelfRef.milan_datapath__DOT__tkd_crflk_q_r = 
        ((IData)(vlSelfRef.axis_resetn) & (IData)(vlSelfRef.milan_datapath__DOT__crf_locked_w));
}
