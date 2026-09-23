// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vmilan_datapath.h for the primary calling header

#include "Vmilan_datapath__pch.h"

extern const VlUnpacked<CData/*4:0*/, 16> Vmilan_datapath__ConstPool__TABLE_ha6a73ec3_0;
extern const VlUnpacked<CData/*0:0*/, 32> Vmilan_datapath__ConstPool__TABLE_h5f1389fb_0;
extern const VlUnpacked<CData/*2:0*/, 32> Vmilan_datapath__ConstPool__TABLE_h6dff1152_0;
extern const VlWide<14>/*447:0*/ Vmilan_datapath__ConstPool__CONST_hb0e0ad07_0;
extern const VlWide<8>/*255:0*/ Vmilan_datapath__ConstPool__CONST_h7f3586b3_0;
extern const VlWide<10>/*319:0*/ Vmilan_datapath__ConstPool__CONST_hab76c978_0;
extern const VlWide<9>/*287:0*/ Vmilan_datapath__ConstPool__CONST_hc5471b50_0;
extern const VlWide<9>/*287:0*/ Vmilan_datapath__ConstPool__CONST_h11ab053c_0;
extern const VlUnpacked<CData/*0:0*/, 16> Vmilan_datapath__ConstPool__TABLE_h8665d168_0;
extern const VlWide<8>/*255:0*/ Vmilan_datapath__ConstPool__CONST_h9e67c271_0;

void Vmilan_datapath___024root___nba_sequent__TOP__1(Vmilan_datapath___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vmilan_datapath___024root___nba_sequent__TOP__1\n"); );
    Vmilan_datapath__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    CData/*4:0*/ __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_next__64__Vfuncout;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_next__64__Vfuncout = 0;
    CData/*4:0*/ __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_next__64__s;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_next__64__s = 0;
    SData/*15:0*/ __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__inc16__138__Vfuncout;
    __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__inc16__138__Vfuncout = 0;
    SData/*15:0*/ __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__inc16__138__v;
    __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__inc16__138__v = 0;
    IData/*31:0*/ __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__139__didx;
    __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__139__didx = 0;
    SData/*15:0*/ __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__139__meas;
    __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__139__meas = 0;
    IData/*31:0*/ __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__140__didx;
    __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__140__didx = 0;
    SData/*15:0*/ __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__140__meas;
    __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__140__meas = 0;
    IData/*31:0*/ __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__141__didx;
    __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__141__didx = 0;
    SData/*15:0*/ __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__141__meas;
    __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__141__meas = 0;
    IData/*31:0*/ __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__142__didx;
    __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__142__didx = 0;
    SData/*15:0*/ __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__142__meas;
    __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__142__meas = 0;
    IData/*31:0*/ __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__143__didx;
    __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__143__didx = 0;
    SData/*15:0*/ __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__143__meas;
    __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__143__meas = 0;
    SData/*15:0*/ __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__inc16__144__Vfuncout;
    __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__inc16__144__Vfuncout = 0;
    SData/*15:0*/ __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__inc16__144__v;
    __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__inc16__144__v = 0;
    SData/*15:0*/ __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__inc16__145__Vfuncout;
    __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__inc16__145__Vfuncout = 0;
    SData/*15:0*/ __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__inc16__145__v;
    __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__inc16__145__v = 0;
    SData/*15:0*/ __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__inc16__146__Vfuncout;
    __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__inc16__146__Vfuncout = 0;
    SData/*15:0*/ __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__inc16__146__v;
    __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__inc16__146__v = 0;
    IData/*31:0*/ __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__147__didx;
    __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__147__didx = 0;
    SData/*15:0*/ __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__147__meas;
    __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__147__meas = 0;
    IData/*31:0*/ __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__148__didx;
    __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__148__didx = 0;
    SData/*15:0*/ __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__148__meas;
    __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__148__meas = 0;
    IData/*31:0*/ __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__149__didx;
    __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__149__didx = 0;
    SData/*15:0*/ __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__149__meas;
    __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__149__meas = 0;
    IData/*31:0*/ __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__150__didx;
    __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__150__didx = 0;
    SData/*15:0*/ __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__150__meas;
    __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__150__meas = 0;
    IData/*31:0*/ __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__151__didx;
    __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__151__didx = 0;
    SData/*15:0*/ __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__151__meas;
    __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__151__meas = 0;
    SData/*15:0*/ __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__inc16__152__Vfuncout;
    __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__inc16__152__Vfuncout = 0;
    SData/*15:0*/ __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__inc16__152__v;
    __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__inc16__152__v = 0;
    SData/*15:0*/ __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__inc16__153__Vfuncout;
    __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__inc16__153__Vfuncout = 0;
    SData/*15:0*/ __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__inc16__153__v;
    __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__inc16__153__v = 0;
    QData/*47:0*/ __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_hit__207__start_a;
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_hit__207__start_a = 0;
    SData/*15:0*/ __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_hit__207__cnt_a;
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_hit__207__cnt_a = 0;
    SData/*15:0*/ __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_hit__207__our_s;
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_hit__207__our_s = 0;
    SData/*15:0*/ __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_hit__207__our_e;
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_hit__207__our_e = 0;
    SData/*15:0*/ __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_hit__207__req_s;
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_hit__207__req_s = 0;
    SData/*15:0*/ __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_hit__207__req_e;
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_hit__207__req_e = 0;
    SData/*15:0*/ __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rand_offset__208__Vfuncout;
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rand_offset__208__Vfuncout = 0;
    SData/*15:0*/ __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rand_offset__208__rnd;
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rand_offset__208__rnd = 0;
    CData/*7:0*/ __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rand_offset__208__cnt;
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rand_offset__208__cnt = 0;
    SData/*15:0*/ __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rand_offset__208__o;
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rand_offset__208__o = 0;
    QData/*47:0*/ __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__209__start_a;
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__209__start_a = 0;
    SData/*15:0*/ __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__209__cnt_a;
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__209__cnt_a = 0;
    SData/*15:0*/ __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__209__our_s;
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__209__our_s = 0;
    SData/*15:0*/ __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__209__our_e;
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__209__our_e = 0;
    SData/*15:0*/ __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__209__req_s;
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__209__req_s = 0;
    SData/*15:0*/ __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__209__req_e;
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__209__req_e = 0;
    SData/*15:0*/ __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__209__c_s;
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__209__c_s = 0;
    SData/*15:0*/ __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__209__c_c;
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__209__c_c = 0;
    QData/*47:0*/ __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__210__start_a;
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__210__start_a = 0;
    SData/*15:0*/ __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__210__cnt_a;
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__210__cnt_a = 0;
    SData/*15:0*/ __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__210__our_s;
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__210__our_s = 0;
    SData/*15:0*/ __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__210__our_e;
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__210__our_e = 0;
    SData/*15:0*/ __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__210__req_s;
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__210__req_s = 0;
    SData/*15:0*/ __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__210__req_e;
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__210__req_e = 0;
    SData/*15:0*/ __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__210__c_s;
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__210__c_s = 0;
    SData/*15:0*/ __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__210__c_c;
    __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__210__c_c = 0;
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
    CData/*7:0*/ __Vfunc_milan_datapath__DOT__avtp_rx_parser__DOT__hbyte__302__Vfuncout;
    __Vfunc_milan_datapath__DOT__avtp_rx_parser__DOT__hbyte__302__Vfuncout = 0;
    IData/*31:0*/ __Vfunc_milan_datapath__DOT__avtp_rx_parser__DOT__hbyte__302__n;
    __Vfunc_milan_datapath__DOT__avtp_rx_parser__DOT__hbyte__302__n = 0;
    IData/*23:0*/ __VdlyVal__milan_datapath__DOT__chan_map_render__DOT__cur_r__v0;
    __VdlyVal__milan_datapath__DOT__chan_map_render__DOT__cur_r__v0 = 0;
    CData/*2:0*/ __VdlyDim0__milan_datapath__DOT__chan_map_render__DOT__cur_r__v0;
    __VdlyDim0__milan_datapath__DOT__chan_map_render__DOT__cur_r__v0 = 0;
    CData/*1:0*/ __VdlyDim1__milan_datapath__DOT__chan_map_render__DOT__cur_r__v0;
    __VdlyDim1__milan_datapath__DOT__chan_map_render__DOT__cur_r__v0 = 0;
    IData/*23:0*/ __VdlyVal__milan_datapath__DOT__chan_map_render__DOT__cur_r__v1;
    __VdlyVal__milan_datapath__DOT__chan_map_render__DOT__cur_r__v1 = 0;
    CData/*2:0*/ __VdlyDim0__milan_datapath__DOT__chan_map_render__DOT__cur_r__v1;
    __VdlyDim0__milan_datapath__DOT__chan_map_render__DOT__cur_r__v1 = 0;
    CData/*1:0*/ __VdlyDim1__milan_datapath__DOT__chan_map_render__DOT__cur_r__v1;
    __VdlyDim1__milan_datapath__DOT__chan_map_render__DOT__cur_r__v1 = 0;
    CData/*1:0*/ __VdlyVal__milan_datapath__DOT__pcm_route__DOT__route_r__v0;
    __VdlyVal__milan_datapath__DOT__pcm_route__DOT__route_r__v0 = 0;
    CData/*1:0*/ __VdlyDim0__milan_datapath__DOT__pcm_route__DOT__route_r__v0;
    __VdlyDim0__milan_datapath__DOT__pcm_route__DOT__route_r__v0 = 0;
    CData/*0:0*/ __VdlyVal__milan_datapath__DOT__stream_table__DOT__ovr_en_r__v0;
    __VdlyVal__milan_datapath__DOT__stream_table__DOT__ovr_en_r__v0 = 0;
    CData/*1:0*/ __VdlyDim0__milan_datapath__DOT__stream_table__DOT__ovr_en_r__v0;
    __VdlyDim0__milan_datapath__DOT__stream_table__DOT__ovr_en_r__v0 = 0;
    QData/*47:0*/ __VdlyVal__milan_datapath__DOT__chan_map_capture__DOT__tdm_hold_r__v0;
    __VdlyVal__milan_datapath__DOT__chan_map_capture__DOT__tdm_hold_r__v0 = 0;
    // Body
    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__ld_ok_r 
        = ((IData)(vlSelfRef.axis_resetn) && (1U & 
                                              ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__gnt_opmut_w)) 
                                               & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__rebase_w)
                                                   ? 
                                                  (~ 
                                                   ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__op_mut_r) 
                                                    & (0U 
                                                       != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__st_r))))
                                                   : (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__ld_ok_r)))));
    if (vlSelfRef.axis_resetn) {
        vlSelfRef.milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__psfault_sync_r 
            = ((2U & ((IData)(vlSelfRef.milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__psfault_sync_r) 
                      << 1U)) | (IData)(vlSelfRef.milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__ps_fault_ps_r));
        vlSelfRef.__Vdly__milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__psbusy_sync_r 
            = ((2U & ((IData)(vlSelfRef.milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__psbusy_sync_r) 
                      << 1U)) | (IData)(vlSelfRef.milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__ps_busy_ps_r));
        if ((0U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pf_st_r))) {
            if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_acmp_q__DOT__out_valid_r) {
                if ((7U == (7U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_acmp_q__DOT__out_data_r[1U] 
                                  >> 0x00000019U)))) {
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pf_eid_r 
                        = (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_acmp_q__DOT__out_data_r[6U])) 
                            << 0x00000022U) | (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_acmp_q__DOT__out_data_r[5U])) 
                                                << 2U) 
                                               | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_acmp_q__DOT__out_data_r[4U])) 
                                                  >> 0x0000001eU)));
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pf_st_r = 2U;
                } else {
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pf_idx_r = 0U;
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pf_st_r = 1U;
                }
            }
        } else if ((1U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pf_st_r))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pf_idx_r 
                = (0x0000000fU & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pf_idx_r)));
            if ((0U != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pf_idx_r))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pf_eid_r 
                    = ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pf_eid_r 
                        << 8U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT____Vcellout__g_rx_pool__BRA__4__KET____DOT__u_rx_slots__rd_data_o)));
            }
            if ((8U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pf_idx_r))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pf_st_r = 2U;
            }
        } else if ((2U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pf_st_r))) {
            if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_acmp_q__DOT__out_valid_r) 
                 & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__acmp_txn_ready_w))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pf_st_r = 0U;
            }
        } else {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pf_st_r = 0U;
        }
        if (vlSelfRef.milan_datapath__DOT__rsp_tvalid_w) {
            if ((4U > (IData)(vlSelfRef.milan_datapath__DOT__rsp_tuser_w))) {
                if ((8U > (IData)(vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__chpos_r))) {
                    __VdlyVal__milan_datapath__DOT__chan_map_render__DOT__cur_r__v0 
                        = vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__smp0_w;
                    __VdlyDim0__milan_datapath__DOT__chan_map_render__DOT__cur_r__v0 
                        = (7U & (IData)(vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__chpos_r));
                    __VdlyDim1__milan_datapath__DOT__chan_map_render__DOT__cur_r__v0 
                        = (3U & (IData)(vlSelfRef.milan_datapath__DOT__rsp_tuser_w));
                    vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_render__DOT__cur_r__v0 = 1U;
                }
                if ((8U > (IData)(vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__ch1_w))) {
                    __VdlyVal__milan_datapath__DOT__chan_map_render__DOT__cur_r__v1 
                        = vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__smp1_w;
                    __VdlyDim0__milan_datapath__DOT__chan_map_render__DOT__cur_r__v1 
                        = (7U & (IData)(vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__ch1_w));
                    __VdlyDim1__milan_datapath__DOT__chan_map_render__DOT__cur_r__v1 
                        = (3U & (IData)(vlSelfRef.milan_datapath__DOT__rsp_tuser_w));
                    vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_render__DOT__cur_r__v1 = 1U;
                }
            }
        }
        if (vlSelfRef.milan_datapath__DOT__aafcap_pv_w) {
            __VdlyVal__milan_datapath__DOT__chan_map_capture__DOT__tdm_hold_r__v0 
                = (((QData)((IData)(vlSelfRef.milan_datapath__DOT__aafcap_l_w)) 
                    << 0x00000018U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__aafcap_r_w)));
            vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__tdm_hold_r__v0 = 1U;
            vlSelfRef.milan_datapath__DOT__zf_slot_w = 0U;
            vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__i2s_hold_r 
                = (((QData)((IData)(vlSelfRef.milan_datapath__DOT__aafcap_l_w)) 
                    << 0x00000018U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__aafcap_r_w)));
        } else {
            vlSelfRef.milan_datapath__DOT__zf_slot_w 
                = Vmilan_datapath__ConstPool__TABLE_ha6a73ec3_0
                [vlSelfRef.milan_datapath__DOT__pair_zero_fill__DOT__pend_r];
        }
        if (((IData)(vlSelfRef.milan_datapath__DOT__wing_route_we_r) 
             & (4U > (IData)(vlSelfRef.milan_datapath__DOT__wing_idx_r)))) {
            __VdlyVal__milan_datapath__DOT__pcm_route__DOT__route_r__v0 
                = (2U & (IData)(vlSelfRef.milan_datapath__DOT__wing_route_r));
            __VdlyDim0__milan_datapath__DOT__pcm_route__DOT__route_r__v0 
                = (3U & (IData)(vlSelfRef.milan_datapath__DOT__wing_idx_r));
            vlSelfRef.__VdlySet__milan_datapath__DOT__pcm_route__DOT__route_r__v0 = 1U;
        }
        if (((IData)(vlSelfRef.milan_datapath__DOT__wing_tbl_we_r) 
             & (4U > (IData)(vlSelfRef.milan_datapath__DOT__wing_idx_r)))) {
            __VdlyVal__milan_datapath__DOT__stream_table__DOT__ovr_en_r__v0 
                = vlSelfRef.milan_datapath__DOT__wing_en_r;
            __VdlyDim0__milan_datapath__DOT__stream_table__DOT__ovr_en_r__v0 
                = (3U & (IData)(vlSelfRef.milan_datapath__DOT__wing_idx_r));
            vlSelfRef.__VdlySet__milan_datapath__DOT__stream_table__DOT__ovr_en_r__v0 = 1U;
            vlSelfRef.__VdlyVal__milan_datapath__DOT__stream_table__DOT__ovr_sid_r__v0 
                = vlSelfRef.milan_datapath__DOT__wing_sid_r;
            vlSelfRef.__VdlyDim0__milan_datapath__DOT__stream_table__DOT__ovr_sid_r__v0 
                = (3U & (IData)(vlSelfRef.milan_datapath__DOT__wing_idx_r));
            vlSelfRef.__VdlySet__milan_datapath__DOT__stream_table__DOT__ovr_sid_r__v0 = 1U;
            vlSelfRef.__VdlyVal__milan_datapath__DOT__stream_table__DOT__ovr_armed_r__v0 
                = (1U & (~ ((~ (IData)(vlSelfRef.milan_datapath__DOT__wing_en_r)) 
                            & (0ULL == vlSelfRef.milan_datapath__DOT__wing_sid_r))));
            vlSelfRef.__VdlyDim0__milan_datapath__DOT__stream_table__DOT__ovr_armed_r__v0 
                = (3U & (IData)(vlSelfRef.milan_datapath__DOT__wing_idx_r));
            vlSelfRef.__VdlySet__milan_datapath__DOT__stream_table__DOT__ovr_armed_r__v0 = 1U;
        }
        if (((IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__pop_take_w) 
             & (0U == (IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__slot_r)))) {
            vlSelfRef.__VdlyVal__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v0 
                = (0x0000003fU & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__rptr_r[0U])));
            vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v0 = 1U;
        }
        if (((IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__pop_dry_w) 
             & (0U == (IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__slot_r)))) {
            vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__prefill_r__v0 = 1U;
        }
        if ((((0x0001869fU == vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__ms_div_r) 
              & (~ (IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__prefill_r[0U]))) 
             & vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__dev_ok_r[0U])) {
            if ((0x64U != vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__conv_ms_r[0U])) {
                vlSelfRef.__VdlyVal__milan_datapath__DOT__render_setpoint__DOT__conv_ms_r__v1 
                    = (0x0000007fU & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__conv_ms_r[0U])));
                vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__conv_ms_r__v1 = 1U;
            } else {
                vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__converged_r__v1 = 1U;
            }
        }
        if (((IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__s_ok_w) 
             & (0U == vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__idxq_r
                [vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__idxq_rp_r]))) {
            if (vlSelfRef.milan_datapath__DOT__dpkt_pcm_tlast_w) {
                if ((vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__prefill_r[0U] 
                     | vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__pend_r[0U])) {
                    if ((0x0eU <= (IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__fill_end_w))) {
                        vlSelfRef.__VdlyVal__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v1 
                            = (0x0000003fU & ((IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__wptr_nxt_w) 
                                              - (IData)(0x0eU)));
                        vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v1 = 1U;
                    } else if (vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__pend_r[0U]) {
                        vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__prefill_r__v2 = 1U;
                    }
                } else {
                    vlSelfRef.__VdlyVal__milan_datapath__DOT__render_setpoint__DOT__dev_ok_r__v2 
                        = vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__in_band_w;
                    vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__dev_ok_r__v2 = 1U;
                    if ((0x14U < (IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__fill_end_w))) {
                        vlSelfRef.__VdlyVal__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v2 
                            = (0x0000003fU & ((IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__wptr_nxt_w) 
                                              - (IData)(0x0eU)));
                        vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v2 = 1U;
                    } else if ((0x0000000eU > ((IData)(6U) 
                                               + (IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__fill_end_w)))) {
                        vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__prefill_r__v3 = 1U;
                    }
                }
            }
        }
        if (((IData)(vlSelfRef.milan_datapath__DOT__render_recentre_p_w) 
             & (~ (IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__prefill_r[0U])))) {
            vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__pend_r__v2 = 1U;
        }
        if ((1U & ((IData)(vlSelfRef.milan_datapath__DOT__strtbl_bind_fall_w) 
                   | ((IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__chans_moved_w) 
                      & (0U == vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__idxq_r
                         [vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__idxq_rp_r]))))) {
            vlSelfRef.__VdlyVal__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v3 
                = (((IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__s_ok_w) 
                    & (0U == vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__idxq_r
                       [vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__idxq_rp_r]))
                    ? (IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__wptr_nxt_w)
                    : vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__wptr_r[0U]);
            vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v3 = 1U;
        }
        if (((IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__pop_take_w) 
             & (1U == (IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__slot_r)))) {
            vlSelfRef.__VdlyVal__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v4 
                = (0x0000003fU & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__rptr_r[1U])));
            vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v4 = 1U;
        }
        if (((IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__pop_dry_w) 
             & (1U == (IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__slot_r)))) {
            vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__prefill_r__v5 = 1U;
        }
        if ((((0x0001869fU == vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__ms_div_r) 
              & (~ (IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__prefill_r[1U]))) 
             & vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__dev_ok_r[1U])) {
            if ((0x64U != vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__conv_ms_r[1U])) {
                vlSelfRef.__VdlyVal__milan_datapath__DOT__render_setpoint__DOT__conv_ms_r__v7 
                    = (0x0000007fU & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__conv_ms_r[1U])));
                vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__conv_ms_r__v7 = 1U;
            } else {
                vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__converged_r__v7 = 1U;
            }
        }
        if (((IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__s_ok_w) 
             & (1U == vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__idxq_r
                [vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__idxq_rp_r]))) {
            if (vlSelfRef.milan_datapath__DOT__dpkt_pcm_tlast_w) {
                if ((vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__prefill_r[1U] 
                     | vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__pend_r[1U])) {
                    if ((0x0eU <= (IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__fill_end_w))) {
                        vlSelfRef.__VdlyVal__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v5 
                            = (0x0000003fU & ((IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__wptr_nxt_w) 
                                              - (IData)(0x0eU)));
                        vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v5 = 1U;
                    } else if (vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__pend_r[1U]) {
                        vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__prefill_r__v7 = 1U;
                    }
                } else {
                    vlSelfRef.__VdlyVal__milan_datapath__DOT__render_setpoint__DOT__dev_ok_r__v8 
                        = vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__in_band_w;
                    vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__dev_ok_r__v8 = 1U;
                    if ((0x14U < (IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__fill_end_w))) {
                        vlSelfRef.__VdlyVal__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v6 
                            = (0x0000003fU & ((IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__wptr_nxt_w) 
                                              - (IData)(0x0eU)));
                        vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v6 = 1U;
                    } else if ((0x0000000eU > ((IData)(6U) 
                                               + (IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__fill_end_w)))) {
                        vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__prefill_r__v8 = 1U;
                    }
                }
            }
        }
        if (((IData)(vlSelfRef.milan_datapath__DOT__render_recentre_p_w) 
             & (~ (IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__prefill_r[1U])))) {
            vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__pend_r__v6 = 1U;
        }
        if ((1U & (((IData)(vlSelfRef.milan_datapath__DOT__strtbl_bind_fall_w) 
                    >> 1U) | ((IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__chans_moved_w) 
                              & (1U == vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__idxq_r
                                 [vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__idxq_rp_r]))))) {
            vlSelfRef.__VdlyVal__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v7 
                = (((IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__s_ok_w) 
                    & (1U == vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__idxq_r
                       [vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__idxq_rp_r]))
                    ? (IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__wptr_nxt_w)
                    : vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__wptr_r[1U]);
            vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v7 = 1U;
        }
        if (((IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__pop_take_w) 
             & (2U == (IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__slot_r)))) {
            vlSelfRef.__VdlyVal__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v8 
                = (0x0000003fU & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__rptr_r[2U])));
            vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v8 = 1U;
        }
        if (((IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__pop_dry_w) 
             & (2U == (IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__slot_r)))) {
            vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__prefill_r__v10 = 1U;
        }
        if ((((0x0001869fU == vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__ms_div_r) 
              & (~ (IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__prefill_r[2U]))) 
             & vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__dev_ok_r[2U])) {
            if ((0x64U != vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__conv_ms_r[2U])) {
                vlSelfRef.__VdlyVal__milan_datapath__DOT__render_setpoint__DOT__conv_ms_r__v13 
                    = (0x0000007fU & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__conv_ms_r[2U])));
                vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__conv_ms_r__v13 = 1U;
            } else {
                vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__converged_r__v13 = 1U;
            }
        }
        if (((IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__s_ok_w) 
             & (2U == vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__idxq_r
                [vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__idxq_rp_r]))) {
            if (vlSelfRef.milan_datapath__DOT__dpkt_pcm_tlast_w) {
                if ((vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__prefill_r[2U] 
                     | vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__pend_r[2U])) {
                    if ((0x0eU <= (IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__fill_end_w))) {
                        vlSelfRef.__VdlyVal__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v9 
                            = (0x0000003fU & ((IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__wptr_nxt_w) 
                                              - (IData)(0x0eU)));
                        vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v9 = 1U;
                    } else if (vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__pend_r[2U]) {
                        vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__prefill_r__v12 = 1U;
                    }
                } else {
                    vlSelfRef.__VdlyVal__milan_datapath__DOT__render_setpoint__DOT__dev_ok_r__v14 
                        = vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__in_band_w;
                    vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__dev_ok_r__v14 = 1U;
                    if ((0x14U < (IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__fill_end_w))) {
                        vlSelfRef.__VdlyVal__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v10 
                            = (0x0000003fU & ((IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__wptr_nxt_w) 
                                              - (IData)(0x0eU)));
                        vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v10 = 1U;
                    } else if ((0x0000000eU > ((IData)(6U) 
                                               + (IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__fill_end_w)))) {
                        vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__prefill_r__v13 = 1U;
                    }
                }
            }
        }
        if (((IData)(vlSelfRef.milan_datapath__DOT__render_recentre_p_w) 
             & (~ (IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__prefill_r[2U])))) {
            vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__pend_r__v10 = 1U;
        }
        if ((1U & (((IData)(vlSelfRef.milan_datapath__DOT__strtbl_bind_fall_w) 
                    >> 2U) | ((IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__chans_moved_w) 
                              & (2U == vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__idxq_r
                                 [vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__idxq_rp_r]))))) {
            vlSelfRef.__VdlyVal__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v11 
                = (((IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__s_ok_w) 
                    & (2U == vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__idxq_r
                       [vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__idxq_rp_r]))
                    ? (IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__wptr_nxt_w)
                    : vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__wptr_r[2U]);
            vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v11 = 1U;
        }
        if (((IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__pop_take_w) 
             & (3U == (IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__slot_r)))) {
            vlSelfRef.__VdlyVal__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v12 
                = (0x0000003fU & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__rptr_r[3U])));
            vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v12 = 1U;
        }
        if (((IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__pop_dry_w) 
             & (3U == (IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__slot_r)))) {
            vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__prefill_r__v15 = 1U;
        }
        if ((((0x0001869fU == vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__ms_div_r) 
              & (~ (IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__prefill_r[3U]))) 
             & vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__dev_ok_r[3U])) {
            if ((0x64U != vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__conv_ms_r[3U])) {
                vlSelfRef.__VdlyVal__milan_datapath__DOT__render_setpoint__DOT__conv_ms_r__v19 
                    = (0x0000007fU & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__conv_ms_r[3U])));
                vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__conv_ms_r__v19 = 1U;
            } else {
                vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__converged_r__v19 = 1U;
            }
        }
        if (((IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__s_ok_w) 
             & (3U == vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__idxq_r
                [vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__idxq_rp_r]))) {
            if (vlSelfRef.milan_datapath__DOT__dpkt_pcm_tlast_w) {
                if ((vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__prefill_r[3U] 
                     | vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__pend_r[3U])) {
                    if ((0x0eU <= (IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__fill_end_w))) {
                        vlSelfRef.__VdlyVal__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v13 
                            = (0x0000003fU & ((IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__wptr_nxt_w) 
                                              - (IData)(0x0eU)));
                        vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v13 = 1U;
                    } else if (vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__pend_r[3U]) {
                        vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__prefill_r__v17 = 1U;
                    }
                } else {
                    vlSelfRef.__VdlyVal__milan_datapath__DOT__render_setpoint__DOT__dev_ok_r__v20 
                        = vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__in_band_w;
                    vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__dev_ok_r__v20 = 1U;
                    if ((0x14U < (IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__fill_end_w))) {
                        vlSelfRef.__VdlyVal__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v14 
                            = (0x0000003fU & ((IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__wptr_nxt_w) 
                                              - (IData)(0x0eU)));
                        vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v14 = 1U;
                    } else if ((0x0000000eU > ((IData)(6U) 
                                               + (IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__fill_end_w)))) {
                        vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__prefill_r__v18 = 1U;
                    }
                }
            }
        }
        if (((IData)(vlSelfRef.milan_datapath__DOT__render_recentre_p_w) 
             & (~ (IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__prefill_r[3U])))) {
            vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__pend_r__v14 = 1U;
        }
        if ((1U & (((IData)(vlSelfRef.milan_datapath__DOT__strtbl_bind_fall_w) 
                    >> 3U) | ((IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__chans_moved_w) 
                              & (3U == vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__idxq_r
                                 [vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__idxq_rp_r]))))) {
            vlSelfRef.__VdlyVal__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v15 
                = (((IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__s_ok_w) 
                    & (3U == vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__idxq_r
                       [vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__idxq_rp_r]))
                    ? (IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__wptr_nxt_w)
                    : vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__wptr_r[3U]);
            vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v15 = 1U;
        }
        if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__gnt_r))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_acmp_r 
                = ((0x00e00000U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_acmp_r) 
                   | (0x001fffffU & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_acmp_r 
                                     >> 3U)));
        }
        if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_acmp_push_w) {
            if ((0x17U >= (0x0000001fU & ((IData)(3U) 
                                          * (7U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_acmp_mid_w)))))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_acmp_r 
                    = (((~ ((IData)(7U) << (0x0000001fU 
                                            & ((IData)(3U) 
                                               * (7U 
                                                  & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_acmp_mid_w)))))) 
                        & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_acmp_r) 
                       | (0x00ffffffU & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__bslot_r) 
                                         << (0x0000001fU 
                                             & ((IData)(3U) 
                                                * (7U 
                                                   & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_acmp_mid_w)))))));
            }
        }
        if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__txc_req_w))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__txc_pend_r 
                = (1U | (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__txc_pend_r));
        }
        if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__txc_req_w))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__txc_pend_r 
                = (2U | (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__txc_pend_r));
        }
        if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__txc_req_w))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__txc_pend_r 
                = (4U | (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__txc_pend_r));
        }
        if ((8U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__txc_req_w))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__txc_pend_r 
                = (8U | (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__txc_pend_r));
        }
        if ((0x00000010U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__txc_req_w))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__txc_pend_r 
                = (0x00000010U | (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__txc_pend_r));
        }
        if ((0x00000020U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__txc_req_w))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__txc_pend_r 
                = (0x00000020U | (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__txc_pend_r));
        }
        if ((0x00000040U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__txc_req_w))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__txc_pend_r 
                = (0x00000040U | (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__txc_pend_r));
        }
        if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__txc_locked_r) {
            if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__txc_alloc_wait_r) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__txc_alloc_wait_r = 0U;
            } else if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pool_alloc_req_w) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__txc_alloc_wait_r = 1U;
            }
            if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__alloc_gnt_r) {
                if ((6U >= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__txc_owner_r))) {
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__txc_pend_r 
                        = ((~ ((IData)(1U) << (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__txc_owner_r))) 
                           & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__txc_pend_r));
                }
            }
            if (((6U >= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__txc_owner_r)) 
                 && (1U & (((((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__ca_txs_wr_commit_w) 
                                << 3U) | ((7U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__w_st_r)) 
                                          << 2U)) | 
                              (((6U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__a_st_r)) 
                                << 1U) | (3U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_st_r)))) 
                             << 3U) | (((0x0eU == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__st_r)) 
                                        << 2U) | (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__lstn_txs_wr_commit_w) 
                                                   << 1U) 
                                                  | (5U 
                                                     == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__bld_st_r))))) 
                           >> (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__txc_owner_r))))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__txc_locked_r = 0U;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__txc_alloc_wait_r = 0U;
            }
            if (((6U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__txc_owner_r)) 
                 & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__ca_txs_abort_w))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__txc_pend_r 
                    = (0x3fU & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__txc_pend_r));
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__txc_locked_r = 0U;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__txc_alloc_wait_r = 0U;
            }
        } else {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__txc_alloc_wait_r = 0U;
            if ((2U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__txc_pend_r) 
                       | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__txc_req_w)))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__txc_owner_r = 1U;
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__txc_locked_r = 1U;
            } else if ((8U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__txc_pend_r) 
                              | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__txc_req_w)))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__txc_owner_r = 3U;
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__txc_locked_r = 1U;
            } else if ((0x00000010U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__txc_pend_r) 
                                       | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__txc_req_w)))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__txc_owner_r = 4U;
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__txc_locked_r = 1U;
            } else if ((0x00000040U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__txc_pend_r) 
                                       | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__txc_req_w)))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__txc_owner_r = 6U;
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__txc_locked_r = 1U;
            } else if ((4U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__txc_pend_r) 
                              | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__txc_req_w)))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__txc_owner_r = 2U;
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__txc_locked_r = 1U;
            } else if ((1U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__txc_pend_r) 
                              | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__txc_req_w)))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__txc_owner_r = 0U;
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__txc_locked_r = 1U;
            } else if ((0x00000020U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__txc_pend_r) 
                                       | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__txc_req_w)))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__txc_owner_r = 5U;
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__txc_locked_r = 1U;
            }
        }
        if ((((IData)(vlSelfRef.milan_datapath__DOT__amap_edit_owr_p_r) 
              & (0x20U > (IData)(vlSelfRef.milan_datapath__DOT__amap_edit_owr_slot_r))) 
             | ((~ (IData)(vlSelfRef.milan_datapath__DOT__amap_edit_txn_active_r)) 
                & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__lk_held_r)) 
                   & ((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__chmap_wr_p) 
                      & ((vlSelfRef.milan_datapath__DOT__csr__DOT__chmap_sel 
                          >> 8U) & ((~ (IData)(vlSelfRef.milan_datapath__DOT__amap_edit_owr_p_r)) 
                                    & (0x20U > (0x0000003fU 
                                                & vlSelfRef.milan_datapath__DOT__csr__DOT__chmap_sel))))))))) {
            if (vlSelfRef.milan_datapath__DOT__amap_edit_owr_p_r) {
                vlSelfRef.__VdlyVal__milan_datapath__DOT__chan_map_capture__DOT__map_r__v0 
                    = vlSelfRef.milan_datapath__DOT__amap_edit_owr_word_r;
                vlSelfRef.__VdlyDim0__milan_datapath__DOT__chan_map_capture__DOT__map_r__v0 
                    = (0x0000001fU & (IData)(vlSelfRef.milan_datapath__DOT__amap_edit_owr_slot_r));
            } else {
                vlSelfRef.__VdlyVal__milan_datapath__DOT__chan_map_capture__DOT__map_r__v0 
                    = vlSelfRef.milan_datapath__DOT__cfg_cmap_entry_w;
                vlSelfRef.__VdlyDim0__milan_datapath__DOT__chan_map_capture__DOT__map_r__v0 
                    = (0x0000001fU & vlSelfRef.milan_datapath__DOT__csr__DOT__chmap_sel);
            }
            vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__map_r__v0 = 1U;
        }
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__pe_pcp_r 
            = (0x0000001fU & (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__pe_pcp_r) 
                               & (~ ((3U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__disp_code_w))
                                      ? (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__clr_disp_w)
                                      : 0U))) | (- (IData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_evt_domain_change_w)))));
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__bound_hold_r 
            = ((1U != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__xs_r))
                ? ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__bound_hold_r) 
                   | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__bound_r))
                : (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__bound_r));
        if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_gate_open_w) 
             | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_gate_close_w))) {
            if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__st_tk_vld_r) {
                if ((0xffffU != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__svc_drop_r))) {
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__svc_drop_r 
                        = (0x0000ffffU & ((IData)(1U) 
                                          + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__svc_drop_r)));
                }
            } else {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__st_tk_vld_r = 1U;
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__st_tk_r[0U] 
                    = ((0xc0000000U & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__st_tk_r[0U]) 
                       | (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_gate_vlan_w) 
                           << 0x00000012U) | (0x0003fffcU 
                                              & (((IData)(0x0019U) 
                                                  + 
                                                  ((IData)(0x0018U) 
                                                   * 
                                                   (0x0000000fU 
                                                    & ((IData)(
                                                               ((0U 
                                                                 == 
                                                                 (0x70U 
                                                                  & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__tctx_wr_addr_r))) 
                                                                & (IData)(vlSelfRef.milan_datapath__DOT__tctx_w0_wr_w)))
                                                        ? 
                                                       ((2U 
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
                                                         ((vlSelfRef.milan_datapath__DOT__csr__DOT__tctx_wr_data_r 
                                                           >> 1U) 
                                                          + 
                                                          (1U 
                                                           & (vlSelfRef.milan_datapath__DOT__csr__DOT__tctx_wr_data_r 
                                                              >> 1U)))))
                                                        : vlSelfRef.milan_datapath__DOT__tctx_chans_r[0U])))) 
                                                 << 2U))));
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__st_tk_r[0U] 
                    = ((0x3fffffffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__st_tk_r[0U]) 
                       | ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_gate_da_w) 
                          << 0x0000001eU));
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__st_tk_r[1U] 
                    = (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_gate_da_w) 
                        >> 2U) | ((IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_gate_da_w 
                                           >> 0x00000020U)) 
                                  << 0x0000001eU));
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__st_tk_r[2U] 
                    = (((0x3fffc000U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_gate_sid_w) 
                                        << 0x0000000eU)) 
                        | ((IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_gate_da_w 
                                    >> 0x00000020U)) 
                           >> 2U)) | (0xc0000000U & 
                                      ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_gate_sid_w) 
                                       << 0x0000000eU)));
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__st_tk_r[3U] 
                    = ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_gate_sid_w) 
                         >> 0x00000012U) | (0x3fffc000U 
                                            & ((IData)(
                                                       (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_gate_sid_w 
                                                        >> 0x00000020U)) 
                                               << 0x0000000eU))) 
                       | (0xc0000000U & ((IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_gate_sid_w 
                                                  >> 0x00000020U)) 
                                         << 0x0000000eU)));
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__st_tk_r[4U] 
                    = ((0x03ffc000U & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__st_tk_r[4U]) 
                       | (0x03ffffffU & ((IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_gate_sid_w 
                                                  >> 0x00000020U)) 
                                         >> 0x00000012U)));
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__st_tk_r[4U] 
                    = ((0x00003fffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__st_tk_r[4U]) 
                       | (0x03ffffffU & ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_gate_open_w)
                                            ? 0U : 1U) 
                                          << 0x00000016U) 
                                         | ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_gate_src_w) 
                                            << 0x0000000eU))));
            }
        }
        if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__lstn_act_settle_w) 
             | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__lstn_act_teardown_w))) {
            if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__st_ls_vld_r) {
                if ((0xffffU != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__svc_drop_r))) {
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__svc_drop_r 
                        = (0x0000ffffU & ((IData)(1U) 
                                          + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__svc_drop_r)));
                }
            } else {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__st_ls_vld_r = 1U;
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__st_ls_r[0U] 
                    = (2U | (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__da_f_r) 
                              << 0x0000001eU) | (0x3ffc0000U 
                                                 & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__vlan_f_r) 
                                                    << 0x00000012U))));
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__st_ls_r[1U] 
                    = (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__da_f_r) 
                        >> 2U) | ((IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__da_f_r 
                                           >> 0x00000020U)) 
                                  << 0x0000001eU));
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__st_ls_r[2U] 
                    = ((0xffffc000U & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__st_ls_r[2U]) 
                       | ((IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__da_f_r 
                                   >> 0x00000020U)) 
                          >> 2U));
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__st_ls_r[2U] 
                    = ((0x00003fffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__st_ls_r[2U]) 
                       | ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__sid_f_r) 
                          << 0x0000000eU));
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__st_ls_r[3U] 
                    = (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__sid_f_r) 
                        >> 0x00000012U) | ((IData)(
                                                   (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__sid_f_r 
                                                    >> 0x00000020U)) 
                                           << 0x0000000eU));
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__st_ls_r[4U] 
                    = ((0x03ffc000U & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__st_ls_r[4U]) 
                       | (0x03ffffffU & ((IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__sid_f_r 
                                                  >> 0x00000020U)) 
                                         >> 0x00000012U)));
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__st_ls_r[4U] 
                    = ((0x00003fffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__st_ls_r[4U]) 
                       | (0x03ffffffU & ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__lstn_act_settle_w)
                                            ? 2U : 3U) 
                                          << 0x00000016U) 
                                         | ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__sink_r) 
                                            << 0x0000000eU))));
            }
        }
        if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__inflight_vld_r) {
            if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_req_valid_w) 
                 & (0U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__svc_st_r)))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_req_valid_w = 0U;
            }
            if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_rsp_valid_w) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__inflight_vld_r = 0U;
            }
        } else if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__st_tk_vld_r) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_req_valid_w = 1U;
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__inflight_r[0U] 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__st_tk_r[0U];
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__inflight_r[1U] 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__st_tk_r[1U];
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__inflight_r[2U] 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__st_tk_r[2U];
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__inflight_r[3U] 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__st_tk_r[3U];
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__inflight_r[4U] 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__st_tk_r[4U];
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__inflight_vld_r = 1U;
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__st_tk_vld_r = 0U;
        } else if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__st_ls_vld_r) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_req_valid_w = 1U;
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__inflight_r[0U] 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__st_ls_r[0U];
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__inflight_r[1U] 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__st_ls_r[1U];
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__inflight_r[2U] 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__st_ls_r[2U];
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__inflight_r[3U] 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__st_ls_r[3U];
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__inflight_r[4U] 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__st_ls_r[4U];
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__inflight_vld_r = 1U;
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__st_ls_vld_r = 0U;
        } else if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__st_svc_vld_r) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_req_valid_w = 1U;
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__inflight_r[0U] 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__st_svc_r[0U];
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__inflight_r[1U] 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__st_svc_r[1U];
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__inflight_r[2U] 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__st_svc_r[2U];
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__inflight_r[3U] 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__st_svc_r[3U];
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__inflight_r[4U] 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__st_svc_r[4U];
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__inflight_vld_r = 1U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__st_svc_vld_r = 0U;
        }
        if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__ucancel_issue_w) 
                      | ((0U == vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__tpend_r[0U]) 
                         | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__iter_port_w)))))) {
            vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__tpend_r__v0 = 1U;
        }
        if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__adv_exp_w) 
             & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__chk_slot_r)))) {
            if ((2U == vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__adv_st_r[0U])) {
                vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__adv_st_r__v0 = 1U;
            } else if ((3U == vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__adv_st_r[0U])) {
                vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__adv_st_r__v1 = 1U;
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__adv_startup_r = 0U;
            }
        }
        if (((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__txn_in_valid_q_r) 
               & ((1U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__rx_st_r)) 
                  & ((2U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__rxq_msg_r)) 
                     & ((0ULL == vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__rxq_eid_r) 
                        | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__rxq_eid_r 
                           == vlSelfRef.milan_datapath__DOT__cfg_adp_entity_id))))) 
              & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__rxq_if_r))) 
             & (3U == vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__adv_st_r[0U]))) {
            vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__adv_st_r__v2 = 1U;
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__adv_startup_r = 0U;
            vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__tpend_r__v1 = 1U;
        }
        if (((IData)(vlSelfRef.milan_datapath__DOT__pp_gm_change_p_w) 
             & (3U == vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__adv_st_r[0U]))) {
            vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__adv_st_r__v3 = 1U;
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__adv_startup_r = 0U;
            vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__tpend_r__v2 = 1U;
        }
        if (((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__adp_prng_valid_w) 
               & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__draw_act_r) 
                  & ((0U >= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__draw_if_r)) 
                     & (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__draw_kind_r) 
                         == (((0U >= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__draw_if_r)) 
                              & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__adv_startup_r) 
                                 >> (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__draw_if_r)))
                              ? 1U : 2U)) & (1U == vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__adv_st_r
                                             [vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__draw_if_r]))))) 
              & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__draw_if_r))) 
             & (1U == vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__adv_st_r[0U]))) {
            vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__adv_st_r__v4 = 1U;
            vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__tpend_deadline_r__v0 
                = (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__now_ms_r 
                   + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__prng_ms_w));
        }
        if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__bld_done_avail_w) 
              & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__bld_if_r))) 
             & (3U == vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__adv_st_r[0U]))) {
            vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__tpend_r__v4 = 1U;
            vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__tpend_deadline_r__v1 
                = ((IData)(0x00001388U) + vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__now_ms_r);
        }
        if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__link_fall_w) 
             & (0U != vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__adv_st_r[0U]))) {
            vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__adv_st_r__v5 = 1U;
        }
        if ((((IData)(vlSelfRef.milan_datapath__DOT____Vcellinp__pp_shadow__enable_i) 
              & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__enable_fall_w))) 
             & (0U == vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__adv_st_r[0U]))) {
            if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__enable_rise_w) 
                 & (IData)(vlSelfRef.milan_datapath__DOT__eff_link_w))) {
                vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__adv_st_r__v7 = 1U;
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__adv_startup_r = 1U;
            } else if ((((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__link_q_r)) 
                         & (IData)(vlSelfRef.milan_datapath__DOT__eff_link_w)) 
                        & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__enable_rise_w)))) {
                vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__adv_st_r__v8 = 1U;
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__adv_startup_r = 0U;
            }
        }
        if (((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_normalizer__DOT__txn_valid_r) 
               & (0U == (0x0000001cU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_normalizer__DOT__txn_r[11U]))) 
              & (4U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_adp_q__DOT__cnt_r))) 
             & (0xffffU != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__adp_stall_r)))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__adp_stall_r 
                = (0x0000ffffU & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__adp_stall_r)));
        }
        if (((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_normalizer__DOT__txn_valid_r) 
               & (4U == (0x0000001cU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_normalizer__DOT__txn_r[11U]))) 
              & (4U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_acmp_q__DOT__cnt_r))) 
             & (0xffffU != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__acmp_stall_r)))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__acmp_stall_r 
                = (0x0000ffffU & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__acmp_stall_r)));
        }
        vlSelfRef.milan_datapath__DOT__media_nco__DOT__trim_r 
            = (VL_LTS_III(32, 0x00007d00U, vlSelfRef.milan_datapath__DOT__media_nco__DOT__trim_sel_w)
                ? 0x00007d00U : (VL_GTS_III(32, 0xffff8300U, vlSelfRef.milan_datapath__DOT__media_nco__DOT__trim_sel_w)
                                  ? 0x00038300U : (0x0003ffffU 
                                                   & vlSelfRef.milan_datapath__DOT__media_nco__DOT__trim_sel_w)));
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__en_q_r = 0x1fU;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__ls_arm_v_w = 0U;
        if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__tsel_v_w) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__ls_arm_v_w = 1U;
        }
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tk_arm_v_w = 0U;
        if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__tsel_v_w) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tk_arm_v_w = 1U;
        }
        vlSelfRef.milan_datapath__DOT__pair_zero_fill__DOT__fed_now_r 
            = ((1U & VL_REDXOR_32((3U & ((IData)(vlSelfRef.milan_datapath__DOT__zf_tick_cdc__DOT__sync) 
                                         >> 1U)))) ? 0U
                : (IData)(vlSelfRef.milan_datapath__DOT__pair_zero_fill__DOT__fed_now_c));
        vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__s_tdata_q 
            = vlSelfRef.s_axis_mac_rx_tdata;
        vlSelfRef.milan_datapath__DOT__rsp_tdata_w 
            = (((QData)((IData)(((0x00ff0000U & (vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__smp_o_w 
                                                 << 0x00000010U)) 
                                 | ((0x0000ff00U & vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__smp_o_w) 
                                    | (0x000000ffU 
                                       & (vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__smp_o_w 
                                          >> 0x10U)))))) 
                << 0x00000020U) | (QData)((IData)((
                                                   (0x00ff0000U 
                                                    & (vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__smp_e_w 
                                                       << 0x00000010U)) 
                                                   | ((0x0000ff00U 
                                                       & vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__smp_e_w) 
                                                      | (0x000000ffU 
                                                         & (vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__smp_e_w 
                                                            >> 0x10U)))))));
        if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__aecp_sb_accept_w) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__aecp_sb_done_pending_r = 0U;
        } else if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__aecp_sb_done_w) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__aecp_sb_done_pending_r = 1U;
        }
        if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__rd_fire_w) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__out_emit_r 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__vq_r
                [(0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__vrptr_r))];
        }
        if (((IData)(vlSelfRef.milan_datapath__DOT____Vcellinp__media_clock_restart__frame_p_i) 
             & (5U > (IData)(vlSelfRef.milan_datapath__DOT____Vcellinp__media_clock_restart__frame_idx_i)))) {
            if ((4U >= (7U & (IData)(vlSelfRef.milan_datapath__DOT____Vcellinp__media_clock_restart__frame_idx_i)))) {
                vlSelfRef.milan_datapath__DOT__talker_diag__DOT__mr_q_r 
                    = (((~ ((IData)(1U) << (7U & (IData)(vlSelfRef.milan_datapath__DOT____Vcellinp__media_clock_restart__frame_idx_i)))) 
                        & (IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__mr_q_r)) 
                       | (0x1fU & ((IData)(vlSelfRef.milan_datapath__DOT____Vcellinp__media_clock_restart__frame_mr_i) 
                                   << (7U & (IData)(vlSelfRef.milan_datapath__DOT____Vcellinp__media_clock_restart__frame_idx_i)))));
            }
        }
        if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__take_rd_w) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__req_seen_r = 1U;
        }
        if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__store_rvalid_w) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__req_seen_r = 0U;
        }
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__pend_r 
            = ((0xfeU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__pend_r)) 
               | ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__arb_req_w) 
                  & (7U != (7U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__arb_slot_w))));
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__pend_r 
            = ((0xfdU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__pend_r)) 
               | (0xfffffffeU & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__arb_req_w) 
                                 & ((7U != (7U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__arb_slot_w 
                                                  >> 3U))) 
                                    << 1U))));
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__pend_r 
            = ((0xfbU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__pend_r)) 
               | (0xfffffffcU & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__arb_req_w) 
                                 & ((7U != (7U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__arb_slot_w 
                                                  >> 6U))) 
                                    << 2U))));
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__pend_r 
            = ((0xf7U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__pend_r)) 
               | (0xfffffff8U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__arb_req_w) 
                                 & ((7U != (7U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__arb_slot_w 
                                                  >> 9U))) 
                                    << 3U))));
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__pend_r 
            = ((0xefU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__pend_r)) 
               | (0xfffffff0U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__arb_req_w) 
                                 & ((7U != (7U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__arb_slot_w 
                                                  >> 0x0cU))) 
                                    << 4U))));
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__pend_r 
            = ((0xdfU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__pend_r)) 
               | (0xffffffe0U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__arb_req_w) 
                                 & ((7U != (7U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__arb_slot_w 
                                                  >> 0x0fU))) 
                                    << 5U))));
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__pend_r 
            = ((0xbfU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__pend_r)) 
               | (0xffffffc0U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__arb_req_w) 
                                 & ((7U != (7U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__arb_slot_w 
                                                  >> 0x12U))) 
                                    << 6U))));
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__pend_r 
            = ((0x7fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__pend_r)) 
               | (0xffffff80U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__arb_req_w) 
                                 & ((7U != (7U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__arb_slot_w 
                                                  >> 0x15U))) 
                                    << 7U))));
        if ((1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__rsp_open_w)))) {
            if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__accept_w) {
                if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_rb_we_w) {
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__sk_data_r 
                        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_rb_wdata_w;
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__sk_addr_r 
                        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_rb_addr_w;
                } else {
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__sk_data_r 
                        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__urb_wdata_w;
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__sk_addr_r 
                        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__urb_addr_w;
                }
            }
        }
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__byp_sink_r 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__wr_addr_w;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__byp_data_r[0U] 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__wr_data_w[0U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__byp_data_r[1U] 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__wr_data_w[1U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__byp_data_r[2U] 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__wr_data_w[2U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__byp_data_r[3U] 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__wr_data_w[3U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__byp_data_r[4U] 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__wr_data_w[4U];
        if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__acmp_sb_accept_w) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__acmp_sb_done_pending_r = 0U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__acmp_sb_id_r 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__ff_id_w;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__sb_prefer_aecp_r = 1U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__acmp_sb_active_r = 1U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__acmp_sb_slot_r 
                = (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_acmp_q__DOT__out_data_r[1U] 
                         >> 0x00000019U));
        } else if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__acmp_sb_done_w) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__acmp_sb_done_pending_r = 1U;
        }
        if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__aecp_sb_accept_w) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__aecp_sb_id_r 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__ff_id_w;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__aecp_sb_slot_r 
                = (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__out_data_r[1U] 
                         >> 0x00000019U));
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__sb_prefer_aecp_r = 0U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__aecp_sb_active_r = 1U;
        }
        if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__sb_rel_aecp_w) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__aecp_sb_done_pending_r = 0U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__aecp_sb_active_r = 0U;
        }
        if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__sb_rel_acmp_w) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__acmp_sb_done_pending_r = 0U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__acmp_sb_active_r = 0U;
        }
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_acmp_cnt_r 
            = (0x0000000fU & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_acmp_mid_w) 
                              + ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_acmp_push_w)
                                  ? 1U : 0U)));
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_adp_cnt_r 
            = (0x0000000fU & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_adp_mid_w) 
                              + ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_adp_push_w)
                                  ? 1U : 0U)));
        if ((4U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__aidx_r))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__wgrant_r = 0U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__wgslope_r[0U] = 0U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__wgslope_r[1U] = 0U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__wgslope_r[2U] = 0U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__wgslope_r[3U] = 0U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__wgslope_r[4U] = 0U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__grant_r 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__wgrant_now_w;
        } else {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__wgrant_r 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__wgrant_now_w;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__wgslope_r[0U] 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__wgslope_now_w[0U];
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__wgslope_r[1U] 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__wgslope_now_w[1U];
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__wgslope_r[2U] 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__wgslope_now_w[2U];
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__wgslope_r[3U] 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__wgslope_now_w[3U];
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__wgslope_r[4U] 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__wgslope_now_w[4U];
        }
        if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__enable_fall_w) 
             & (0U != vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__adv_st_r[0U]))) {
            vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__adv_st_r__v6 = 1U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__pend_dep_r = 1U;
        }
        if (vlSelfRef.s_axis_mac_rx_tvalid) {
            if (vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__sof) {
                vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__pass_r 
                    = vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__pass_sof;
            }
            vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__in_frame 
                = (1U & (~ (IData)(vlSelfRef.s_axis_mac_rx_tlast)));
        }
        if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxf_free_w) {
            if ((5U >= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxf_pick_ix_w))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxf_vld_r 
                    = ((~ ((IData)(1U) << (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxf_pick_ix_w))) 
                       & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxf_vld_r));
            }
        }
        if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxf_req_w))) {
            if ((1U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxf_vld_r) 
                       & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxf_free_w) 
                             & (0U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxf_pick_ix_w))))))) {
                if ((0xffffU != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxf_drop_r))) {
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxf_drop_r 
                        = (0x0000ffffU & ((IData)(1U) 
                                          + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxf_drop_r)));
                }
            } else {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxf_vld_r 
                    = (1U | (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxf_vld_r));
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxf_slot_r 
                    = ((0x0ffcU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxf_slot_r)) 
                       | (3U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxf_req_slot_w)));
            }
        }
        if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxf_req_w))) {
            if ((1U & (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxf_vld_r) 
                        >> 1U) & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxf_free_w) 
                                     & (1U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxf_pick_ix_w))))))) {
                if ((0xffffU != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxf_drop_r))) {
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxf_drop_r 
                        = (0x0000ffffU & ((IData)(1U) 
                                          + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxf_drop_r)));
                }
            } else {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxf_vld_r 
                    = (2U | (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxf_vld_r));
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxf_slot_r 
                    = ((0x0ff3U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxf_slot_r)) 
                       | (0x0000000cU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxf_req_slot_w)));
            }
        }
        if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxf_req_w))) {
            if ((1U & (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxf_vld_r) 
                        >> 2U) & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxf_free_w) 
                                     & (2U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxf_pick_ix_w))))))) {
                if ((0xffffU != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxf_drop_r))) {
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxf_drop_r 
                        = (0x0000ffffU & ((IData)(1U) 
                                          + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxf_drop_r)));
                }
            } else {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxf_vld_r 
                    = (4U | (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxf_vld_r));
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxf_slot_r 
                    = ((0x0fcfU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxf_slot_r)) 
                       | (0x00000030U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxf_req_slot_w)));
            }
        }
        if ((8U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxf_req_w))) {
            if ((1U & (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxf_vld_r) 
                        >> 3U) & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxf_free_w) 
                                     & (3U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxf_pick_ix_w))))))) {
                if ((0xffffU != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxf_drop_r))) {
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxf_drop_r 
                        = (0x0000ffffU & ((IData)(1U) 
                                          + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxf_drop_r)));
                }
            } else {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxf_vld_r 
                    = (8U | (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxf_vld_r));
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxf_slot_r 
                    = ((0x0f3fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxf_slot_r)) 
                       | (0x000000c0U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxf_req_slot_w)));
            }
        }
        if ((0x00000010U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxf_req_w))) {
            if ((1U & (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxf_vld_r) 
                        >> 4U) & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxf_free_w) 
                                     & (4U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxf_pick_ix_w))))))) {
                if ((0xffffU != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxf_drop_r))) {
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxf_drop_r 
                        = (0x0000ffffU & ((IData)(1U) 
                                          + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxf_drop_r)));
                }
            } else {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxf_vld_r 
                    = (0x00000010U | (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxf_vld_r));
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxf_slot_r 
                    = ((0x0cffU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxf_slot_r)) 
                       | (0x00000300U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxf_req_slot_w)));
            }
        }
        if ((0x00000020U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxf_req_w))) {
            if ((IData)((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxf_vld_r) 
                          >> 5U) & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxf_free_w) 
                                       & (5U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxf_pick_ix_w))))))) {
                if ((0xffffU != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxf_drop_r))) {
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxf_drop_r 
                        = (0x0000ffffU & ((IData)(1U) 
                                          + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxf_drop_r)));
                }
            } else {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxf_vld_r 
                    = (0x00000020U | (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxf_vld_r));
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxf_slot_r 
                    = ((0x03ffU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxf_slot_r)) 
                       | (0x00000c00U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxf_req_slot_w)));
            }
        }
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__c1_proj_r[0U] 
            = (IData)((((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__cap_rec_w[5U])) 
                        << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__cap_rec_w[4U]))));
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__c1_proj_r[1U] 
            = (IData)(((((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__cap_rec_w[5U])) 
                         << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__cap_rec_w[4U]))) 
                       >> 0x00000020U));
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__c1_proj_r[2U] 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__cap_rec_w[1U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__c1_proj_r[3U] 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__cap_rec_w[2U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__c1_proj_r[4U] 
            = ((0x00020000U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__cap_rec_w[0U] 
                               << 5U)) | ((0x00010000U 
                                           & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__cap_rec_w[0U] 
                                              << 3U)) 
                                          | (0x0000ffffU 
                                             & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__cap_rec_w[3U])));
        if (vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__in_acc) {
            if (vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__fire) {
                vlSelfRef.milan_datapath__DOT__avtprx_tv_bit 
                    = (1U & (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__b1));
                vlSelfRef.milan_datapath__DOT__avtprx_tu_bit 
                    = (0U != (1U & ((- (IData)((0x01bfU 
                                                >= 
                                                (0x000001ffU 
                                                 & (((IData)(0x01bfU) 
                                                     - 
                                                     (0x000001f8U 
                                                      & (((IData)(5U) 
                                                          + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__et_off)) 
                                                         << 3U))) 
                                                    - (IData)(7U)))))) 
                                    & (((0U == (0x0000001fU 
                                                & (((IData)(0x01bfU) 
                                                    - 
                                                    (0x000001f8U 
                                                     & (((IData)(5U) 
                                                         + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__et_off)) 
                                                        << 3U))) 
                                                   - (IData)(7U))))
                                         ? 0U : (vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__hdr
                                                 [(
                                                   ((IData)(7U) 
                                                    + 
                                                    (0x000001ffU 
                                                     & (((IData)(0x01bfU) 
                                                         - 
                                                         (0x000001f8U 
                                                          & (((IData)(5U) 
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
                                                        & (((IData)(5U) 
                                                            + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__et_off)) 
                                                           << 3U))) 
                                                      - (IData)(7U)))))) 
                                       | (vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__hdr
                                          [(0x0000000fU 
                                            & ((((IData)(0x01bfU) 
                                                 - 
                                                 (0x000001f8U 
                                                  & (((IData)(5U) 
                                                      + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__et_off)) 
                                                     << 3U))) 
                                                - (IData)(7U)) 
                                               >> 5U))] 
                                          >> (0x0000001fU 
                                              & (((IData)(0x01bfU) 
                                                  - 
                                                  (0x000001f8U 
                                                   & (((IData)(5U) 
                                                       + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__et_off)) 
                                                      << 3U))) 
                                                 - (IData)(7U))))))));
                vlSelfRef.milan_datapath__DOT__avtprx_fsh2 
                    = (((QData)((IData)(((((0x0000ff00U 
                                            & (((((0U 
                                                   == 
                                                   (0x0000001fU 
                                                    & (((IData)(0x01bfU) 
                                                        - 
                                                        (0x000001f8U 
                                                         & (((IData)(0x1aU) 
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
                                                           & (((IData)(0x1aU) 
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
                                                          & (((IData)(0x1aU) 
                                                              + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__et_off)) 
                                                             << 3U))) 
                                                        - (IData)(7U)))))) 
                                                 | (vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__hdr
                                                    [
                                                    (0x0000000fU 
                                                     & ((((IData)(0x01bfU) 
                                                          - 
                                                          (0x000001f8U 
                                                           & (((IData)(0x1aU) 
                                                               + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__et_off)) 
                                                              << 3U))) 
                                                         - (IData)(7U)) 
                                                        >> 5U))] 
                                                    >> 
                                                    (0x0000001fU 
                                                     & (((IData)(0x01bfU) 
                                                         - 
                                                         (0x000001f8U 
                                                          & (((IData)(0x1aU) 
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
                                                                    & (((IData)(0x1aU) 
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
                                                          & (((IData)(0x1bU) 
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
                                                            & (((IData)(0x1bU) 
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
                                                           & (((IData)(0x1bU) 
                                                               + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__et_off)) 
                                                              << 3U))) 
                                                         - (IData)(7U)))))) 
                                                  | (vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__hdr
                                                     [
                                                     (0x0000000fU 
                                                      & ((((IData)(0x01bfU) 
                                                           - 
                                                           (0x000001f8U 
                                                            & (((IData)(0x1bU) 
                                                                + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__et_off)) 
                                                               << 3U))) 
                                                          - (IData)(7U)) 
                                                         >> 5U))] 
                                                     >> 
                                                     (0x0000001fU 
                                                      & (((IData)(0x01bfU) 
                                                          - 
                                                          (0x000001f8U 
                                                           & (((IData)(0x1bU) 
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
                                                                     & (((IData)(0x1bU) 
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
                                                          & (((IData)(0x1cU) 
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
                                                            & (((IData)(0x1cU) 
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
                                                           & (((IData)(0x1cU) 
                                                               + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__et_off)) 
                                                              << 3U))) 
                                                         - (IData)(7U)))))) 
                                                  | (vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__hdr
                                                     [
                                                     (0x0000000fU 
                                                      & ((((IData)(0x01bfU) 
                                                           - 
                                                           (0x000001f8U 
                                                            & (((IData)(0x1cU) 
                                                                + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__et_off)) 
                                                               << 3U))) 
                                                          - (IData)(7U)) 
                                                         >> 5U))] 
                                                     >> 
                                                     (0x0000001fU 
                                                      & (((IData)(0x01bfU) 
                                                          - 
                                                          (0x000001f8U 
                                                           & (((IData)(0x1cU) 
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
                                                                     & (((IData)(0x1cU) 
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
                                                           & (((IData)(0x1dU) 
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
                                                             & (((IData)(0x1dU) 
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
                                                            & (((IData)(0x1dU) 
                                                                + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__et_off)) 
                                                               << 3U))) 
                                                          - (IData)(7U)))))) 
                                                   | (vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__hdr
                                                      [
                                                      (0x0000000fU 
                                                       & ((((IData)(0x01bfU) 
                                                            - 
                                                            (0x000001f8U 
                                                             & (((IData)(0x1dU) 
                                                                 + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__et_off)) 
                                                                << 3U))) 
                                                           - (IData)(7U)) 
                                                          >> 5U))] 
                                                      >> 
                                                      (0x0000001fU 
                                                       & (((IData)(0x01bfU) 
                                                           - 
                                                           (0x000001f8U 
                                                            & (((IData)(0x1dU) 
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
                                                                      & (((IData)(0x1dU) 
                                                                          + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__et_off)) 
                                                                         << 3U))) 
                                                                    - (IData)(7U)))))))))))) 
                        << 0x00000020U) | (QData)((IData)(
                                                          ((((0x0000ff00U 
                                                              & (((((0U 
                                                                     == 
                                                                     (0x0000001fU 
                                                                      & (((IData)(0x01bfU) 
                                                                          - 
                                                                          (0x000001f8U 
                                                                           & (((IData)(0x1eU) 
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
                                                                             & (((IData)(0x1eU) 
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
                                                                            & (((IData)(0x1eU) 
                                                                                + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__et_off)) 
                                                                               << 3U))) 
                                                                          - (IData)(7U)))))) 
                                                                   | (vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__hdr
                                                                      [
                                                                      (0x0000000fU 
                                                                       & ((((IData)(0x01bfU) 
                                                                            - 
                                                                            (0x000001f8U 
                                                                             & (((IData)(0x1eU) 
                                                                                + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__et_off)) 
                                                                                << 3U))) 
                                                                           - (IData)(7U)) 
                                                                          >> 5U))] 
                                                                      >> 
                                                                      (0x0000001fU 
                                                                       & (((IData)(0x01bfU) 
                                                                           - 
                                                                           (0x000001f8U 
                                                                            & (((IData)(0x1eU) 
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
                                                                                & (((IData)(0x1eU) 
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
                                                                            & (((IData)(0x1fU) 
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
                                                                              & (((IData)(0x1fU) 
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
                                                                             & (((IData)(0x1fU) 
                                                                                + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__et_off)) 
                                                                                << 3U))) 
                                                                           - (IData)(7U)))))) 
                                                                    | (vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__hdr
                                                                       [
                                                                       (0x0000000fU 
                                                                        & ((((IData)(0x01bfU) 
                                                                             - 
                                                                             (0x000001f8U 
                                                                              & (((IData)(0x1fU) 
                                                                                + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__et_off)) 
                                                                                << 3U))) 
                                                                            - (IData)(7U)) 
                                                                           >> 5U))] 
                                                                       >> 
                                                                       (0x0000001fU 
                                                                        & (((IData)(0x01bfU) 
                                                                            - 
                                                                            (0x000001f8U 
                                                                             & (((IData)(0x1fU) 
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
                                                                                & (((IData)(0x1fU) 
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
                                                                            & (((IData)(0x20U) 
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
                                                                              & (((IData)(0x20U) 
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
                                                                             & (((IData)(0x20U) 
                                                                                + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__et_off)) 
                                                                                << 3U))) 
                                                                           - (IData)(7U)))))) 
                                                                    | (vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__hdr
                                                                       [
                                                                       (0x0000000fU 
                                                                        & ((((IData)(0x01bfU) 
                                                                             - 
                                                                             (0x000001f8U 
                                                                              & (((IData)(0x20U) 
                                                                                + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__et_off)) 
                                                                                << 3U))) 
                                                                            - (IData)(7U)) 
                                                                           >> 5U))] 
                                                                       >> 
                                                                       (0x0000001fU 
                                                                        & (((IData)(0x01bfU) 
                                                                            - 
                                                                            (0x000001f8U 
                                                                             & (((IData)(0x20U) 
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
                                                                                & (((IData)(0x20U) 
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
                                                                             & (((IData)(0x21U) 
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
                                                                               & (((IData)(0x21U) 
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
                                                                              & (((IData)(0x21U) 
                                                                                + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__et_off)) 
                                                                                << 3U))) 
                                                                            - (IData)(7U)))))) 
                                                                     | (vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__hdr
                                                                        [
                                                                        (0x0000000fU 
                                                                         & ((((IData)(0x01bfU) 
                                                                              - 
                                                                              (0x000001f8U 
                                                                               & (((IData)(0x21U) 
                                                                                + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__et_off)) 
                                                                                << 3U))) 
                                                                             - (IData)(7U)) 
                                                                            >> 5U))] 
                                                                        >> 
                                                                        (0x0000001fU 
                                                                         & (((IData)(0x01bfU) 
                                                                             - 
                                                                             (0x000001f8U 
                                                                              & (((IData)(0x21U) 
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
                                                                                & (((IData)(0x21U) 
                                                                                + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__et_off)) 
                                                                                << 3U))) 
                                                                                - (IData)(7U)))))))))))));
                vlSelfRef.milan_datapath__DOT__avtprx_fsh 
                    = (((QData)((IData)(((((0x0000ff00U 
                                            & (((((0U 
                                                   == 
                                                   (0x0000001fU 
                                                    & (((IData)(0x01bfU) 
                                                        - 
                                                        (0x000001f8U 
                                                         & (((IData)(0x12U) 
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
                                                           & (((IData)(0x12U) 
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
                                                          & (((IData)(0x12U) 
                                                              + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__et_off)) 
                                                             << 3U))) 
                                                        - (IData)(7U)))))) 
                                                 | (vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__hdr
                                                    [
                                                    (0x0000000fU 
                                                     & ((((IData)(0x01bfU) 
                                                          - 
                                                          (0x000001f8U 
                                                           & (((IData)(0x12U) 
                                                               + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__et_off)) 
                                                              << 3U))) 
                                                         - (IData)(7U)) 
                                                        >> 5U))] 
                                                    >> 
                                                    (0x0000001fU 
                                                     & (((IData)(0x01bfU) 
                                                         - 
                                                         (0x000001f8U 
                                                          & (((IData)(0x12U) 
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
                                                                    & (((IData)(0x12U) 
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
                                                          & (((IData)(0x13U) 
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
                                                            & (((IData)(0x13U) 
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
                                                           & (((IData)(0x13U) 
                                                               + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__et_off)) 
                                                              << 3U))) 
                                                         - (IData)(7U)))))) 
                                                  | (vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__hdr
                                                     [
                                                     (0x0000000fU 
                                                      & ((((IData)(0x01bfU) 
                                                           - 
                                                           (0x000001f8U 
                                                            & (((IData)(0x13U) 
                                                                + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__et_off)) 
                                                               << 3U))) 
                                                          - (IData)(7U)) 
                                                         >> 5U))] 
                                                     >> 
                                                     (0x0000001fU 
                                                      & (((IData)(0x01bfU) 
                                                          - 
                                                          (0x000001f8U 
                                                           & (((IData)(0x13U) 
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
                                                                     & (((IData)(0x13U) 
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
                                                          & (((IData)(0x14U) 
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
                                                            & (((IData)(0x14U) 
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
                                                           & (((IData)(0x14U) 
                                                               + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__et_off)) 
                                                              << 3U))) 
                                                         - (IData)(7U)))))) 
                                                  | (vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__hdr
                                                     [
                                                     (0x0000000fU 
                                                      & ((((IData)(0x01bfU) 
                                                           - 
                                                           (0x000001f8U 
                                                            & (((IData)(0x14U) 
                                                                + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__et_off)) 
                                                               << 3U))) 
                                                          - (IData)(7U)) 
                                                         >> 5U))] 
                                                     >> 
                                                     (0x0000001fU 
                                                      & (((IData)(0x01bfU) 
                                                          - 
                                                          (0x000001f8U 
                                                           & (((IData)(0x14U) 
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
                                                                     & (((IData)(0x14U) 
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
                                                           & (((IData)(0x15U) 
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
                                                             & (((IData)(0x15U) 
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
                                                            & (((IData)(0x15U) 
                                                                + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__et_off)) 
                                                               << 3U))) 
                                                          - (IData)(7U)))))) 
                                                   | (vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__hdr
                                                      [
                                                      (0x0000000fU 
                                                       & ((((IData)(0x01bfU) 
                                                            - 
                                                            (0x000001f8U 
                                                             & (((IData)(0x15U) 
                                                                 + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__et_off)) 
                                                                << 3U))) 
                                                           - (IData)(7U)) 
                                                          >> 5U))] 
                                                      >> 
                                                      (0x0000001fU 
                                                       & (((IData)(0x01bfU) 
                                                           - 
                                                           (0x000001f8U 
                                                            & (((IData)(0x15U) 
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
                                                                      & (((IData)(0x15U) 
                                                                          + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__et_off)) 
                                                                         << 3U))) 
                                                                    - (IData)(7U)))))))))))) 
                        << 0x00000020U) | (QData)((IData)(
                                                          ((((0x0000ff00U 
                                                              & (((((0U 
                                                                     == 
                                                                     (0x0000001fU 
                                                                      & (((IData)(0x01bfU) 
                                                                          - 
                                                                          (0x000001f8U 
                                                                           & (((IData)(0x16U) 
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
                                                                             & (((IData)(0x16U) 
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
                                                                            & (((IData)(0x16U) 
                                                                                + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__et_off)) 
                                                                               << 3U))) 
                                                                          - (IData)(7U)))))) 
                                                                   | (vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__hdr
                                                                      [
                                                                      (0x0000000fU 
                                                                       & ((((IData)(0x01bfU) 
                                                                            - 
                                                                            (0x000001f8U 
                                                                             & (((IData)(0x16U) 
                                                                                + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__et_off)) 
                                                                                << 3U))) 
                                                                           - (IData)(7U)) 
                                                                          >> 5U))] 
                                                                      >> 
                                                                      (0x0000001fU 
                                                                       & (((IData)(0x01bfU) 
                                                                           - 
                                                                           (0x000001f8U 
                                                                            & (((IData)(0x16U) 
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
                                                                                & (((IData)(0x16U) 
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
                                                                            & (((IData)(0x17U) 
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
                                                                              & (((IData)(0x17U) 
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
                                                                             & (((IData)(0x17U) 
                                                                                + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__et_off)) 
                                                                                << 3U))) 
                                                                           - (IData)(7U)))))) 
                                                                    | (vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__hdr
                                                                       [
                                                                       (0x0000000fU 
                                                                        & ((((IData)(0x01bfU) 
                                                                             - 
                                                                             (0x000001f8U 
                                                                              & (((IData)(0x17U) 
                                                                                + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__et_off)) 
                                                                                << 3U))) 
                                                                            - (IData)(7U)) 
                                                                           >> 5U))] 
                                                                       >> 
                                                                       (0x0000001fU 
                                                                        & (((IData)(0x01bfU) 
                                                                            - 
                                                                            (0x000001f8U 
                                                                             & (((IData)(0x17U) 
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
                                                                                & (((IData)(0x17U) 
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
                                                                            & (((IData)(0x18U) 
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
                                                                              & (((IData)(0x18U) 
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
                                                                             & (((IData)(0x18U) 
                                                                                + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__et_off)) 
                                                                                << 3U))) 
                                                                           - (IData)(7U)))))) 
                                                                    | (vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__hdr
                                                                       [
                                                                       (0x0000000fU 
                                                                        & ((((IData)(0x01bfU) 
                                                                             - 
                                                                             (0x000001f8U 
                                                                              & (((IData)(0x18U) 
                                                                                + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__et_off)) 
                                                                                << 3U))) 
                                                                            - (IData)(7U)) 
                                                                           >> 5U))] 
                                                                       >> 
                                                                       (0x0000001fU 
                                                                        & (((IData)(0x01bfU) 
                                                                            - 
                                                                            (0x000001f8U 
                                                                             & (((IData)(0x18U) 
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
                                                                                & (((IData)(0x18U) 
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
                                                                             & (((IData)(0x19U) 
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
                                                                               & (((IData)(0x19U) 
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
                                                                              & (((IData)(0x19U) 
                                                                                + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__et_off)) 
                                                                                << 3U))) 
                                                                            - (IData)(7U)))))) 
                                                                     | (vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__hdr
                                                                        [
                                                                        (0x0000000fU 
                                                                         & ((((IData)(0x01bfU) 
                                                                              - 
                                                                              (0x000001f8U 
                                                                               & (((IData)(0x19U) 
                                                                                + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__et_off)) 
                                                                                << 3U))) 
                                                                             - (IData)(7U)) 
                                                                            >> 5U))] 
                                                                        >> 
                                                                        (0x0000001fU 
                                                                         & (((IData)(0x01bfU) 
                                                                             - 
                                                                             (0x000001f8U 
                                                                              & (((IData)(0x19U) 
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
                                                                                & (((IData)(0x19U) 
                                                                                + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__et_off)) 
                                                                                << 3U))) 
                                                                                - (IData)(7U)))))))))))));
                vlSelfRef.milan_datapath__DOT__avtprx_ts 
                    = ((((0x0000ff00U & (((((0U == 
                                             (0x0000001fU 
                                              & (((IData)(0x01bfU) 
                                                  - 
                                                  (0x000001f8U 
                                                   & (((IData)(0x0eU) 
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
                                                        & (((IData)(0x0eU) 
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
                                                       & (((IData)(0x0eU) 
                                                           + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__et_off)) 
                                                          << 3U))) 
                                                     - (IData)(7U)))))) 
                                           | (vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__hdr
                                              [(0x0000000fU 
                                                & ((((IData)(0x01bfU) 
                                                     - 
                                                     (0x000001f8U 
                                                      & (((IData)(0x0eU) 
                                                          + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__et_off)) 
                                                         << 3U))) 
                                                    - (IData)(7U)) 
                                                   >> 5U))] 
                                              >> (0x0000001fU 
                                                  & (((IData)(0x01bfU) 
                                                      - 
                                                      (0x000001f8U 
                                                       & (((IData)(0x0eU) 
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
                                                              & (((IData)(0x0eU) 
                                                                  + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__et_off)) 
                                                                 << 3U))) 
                                                            - (IData)(7U))))))) 
                                         << 8U)) | 
                         (0x000000ffU & ((((0U == (0x0000001fU 
                                                   & (((IData)(0x01bfU) 
                                                       - 
                                                       (0x000001f8U 
                                                        & (((IData)(0x0fU) 
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
                                                       & (((IData)(0x0fU) 
                                                           + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__et_off)) 
                                                          << 3U))) 
                                                     - (IData)(7U)))) 
                                              >> 5U)] 
                                            << ((IData)(0x00000020U) 
                                                - (0x0000001fU 
                                                   & (((IData)(0x01bfU) 
                                                       - 
                                                       (0x000001f8U 
                                                        & (((IData)(0x0fU) 
                                                            + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__et_off)) 
                                                           << 3U))) 
                                                      - (IData)(7U)))))) 
                                          | (vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__hdr
                                             [(0x0000000fU 
                                               & ((((IData)(0x01bfU) 
                                                    - 
                                                    (0x000001f8U 
                                                     & (((IData)(0x0fU) 
                                                         + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__et_off)) 
                                                        << 3U))) 
                                                   - (IData)(7U)) 
                                                  >> 5U))] 
                                             >> (0x0000001fU 
                                                 & (((IData)(0x01bfU) 
                                                     - 
                                                     (0x000001f8U 
                                                      & (((IData)(0x0fU) 
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
                                                             & (((IData)(0x0fU) 
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
                                                         & (((IData)(0x10U) 
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
                                                           & (((IData)(0x10U) 
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
                                                          & (((IData)(0x10U) 
                                                              + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__et_off)) 
                                                             << 3U))) 
                                                        - (IData)(7U)))))) 
                                                 | (vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__hdr
                                                    [
                                                    (0x0000000fU 
                                                     & ((((IData)(0x01bfU) 
                                                          - 
                                                          (0x000001f8U 
                                                           & (((IData)(0x10U) 
                                                               + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__et_off)) 
                                                              << 3U))) 
                                                         - (IData)(7U)) 
                                                        >> 5U))] 
                                                    >> 
                                                    (0x0000001fU 
                                                     & (((IData)(0x01bfU) 
                                                         - 
                                                         (0x000001f8U 
                                                          & (((IData)(0x10U) 
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
                                                                    & (((IData)(0x10U) 
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
                                                          & (((IData)(0x11U) 
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
                                                            & (((IData)(0x11U) 
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
                                                           & (((IData)(0x11U) 
                                                               + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__et_off)) 
                                                              << 3U))) 
                                                         - (IData)(7U)))))) 
                                                  | (vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__hdr
                                                     [
                                                     (0x0000000fU 
                                                      & ((((IData)(0x01bfU) 
                                                           - 
                                                           (0x000001f8U 
                                                            & (((IData)(0x11U) 
                                                                + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__et_off)) 
                                                               << 3U))) 
                                                          - (IData)(7U)) 
                                                         >> 5U))] 
                                                     >> 
                                                     (0x0000001fU 
                                                      & (((IData)(0x01bfU) 
                                                          - 
                                                          (0x000001f8U 
                                                           & (((IData)(0x11U) 
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
                                                                     & (((IData)(0x11U) 
                                                                         + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__et_off)) 
                                                                        << 3U))) 
                                                                   - (IData)(7U))))))))));
                __Vfunc_milan_datapath__DOT__avtp_rx_parser__DOT__hbyte__302__n 
                    = ((IData)(3U) + (0x0000003fU & 
                                      ((IData)(2U) 
                                       + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__et_off))));
                __Vfunc_milan_datapath__DOT__avtp_rx_parser__DOT__hbyte__302__Vfuncout 
                    = ((0x01bfU >= (0x000001ffU & (
                                                   ((IData)(0x01bfU) 
                                                    - 
                                                    (__Vfunc_milan_datapath__DOT__avtp_rx_parser__DOT__hbyte__302__n 
                                                     << 3U)) 
                                                   - (IData)(7U))))
                        ? (0x000000ffU & (((0U == (0x0000001fU 
                                                   & (((IData)(0x01bfU) 
                                                       - 
                                                       (__Vfunc_milan_datapath__DOT__avtp_rx_parser__DOT__hbyte__302__n 
                                                        << 3U)) 
                                                      - (IData)(7U))))
                                            ? 0U : 
                                           (vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__hdr
                                            [(((IData)(7U) 
                                               + (0x000001ffU 
                                                  & (((IData)(0x01bfU) 
                                                      - 
                                                      (__Vfunc_milan_datapath__DOT__avtp_rx_parser__DOT__hbyte__302__n 
                                                       << 3U)) 
                                                     - (IData)(7U)))) 
                                              >> 5U)] 
                                            << ((IData)(0x00000020U) 
                                                - (0x0000001fU 
                                                   & (((IData)(0x01bfU) 
                                                       - 
                                                       (__Vfunc_milan_datapath__DOT__avtp_rx_parser__DOT__hbyte__302__n 
                                                        << 3U)) 
                                                      - (IData)(7U)))))) 
                                          | (vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__hdr
                                             [(0x0000000fU 
                                               & ((((IData)(0x01bfU) 
                                                    - 
                                                    (__Vfunc_milan_datapath__DOT__avtp_rx_parser__DOT__hbyte__302__n 
                                                     << 3U)) 
                                                   - (IData)(7U)) 
                                                  >> 5U))] 
                                             >> (0x0000001fU 
                                                 & (((IData)(0x01bfU) 
                                                     - 
                                                     (__Vfunc_milan_datapath__DOT__avtp_rx_parser__DOT__hbyte__302__n 
                                                      << 3U)) 
                                                    - (IData)(7U))))))
                        : 0U);
                vlSelfRef.milan_datapath__DOT__avtprx_b3 
                    = __Vfunc_milan_datapath__DOT__avtp_rx_parser__DOT__hbyte__302__Vfuncout;
                vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__parsed = 1U;
            }
            if ((0x38U > (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__bytes_in))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_parser__DOT__hdr[0U] 
                    = (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__beat_be);
                vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_parser__DOT__hdr[1U] 
                    = (IData)((vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__beat_be 
                               >> 0x00000020U));
                vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_parser__DOT__hdr[2U] 
                    = vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__hdr[0U];
                vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_parser__DOT__hdr[3U] 
                    = vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__hdr[1U];
                vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_parser__DOT__hdr[4U] 
                    = vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__hdr[2U];
                vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_parser__DOT__hdr[5U] 
                    = vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__hdr[3U];
                vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_parser__DOT__hdr[6U] 
                    = vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__hdr[4U];
                vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_parser__DOT__hdr[7U] 
                    = vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__hdr[5U];
                vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_parser__DOT__hdr[8U] 
                    = vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__hdr[6U];
                vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_parser__DOT__hdr[9U] 
                    = vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__hdr[7U];
                vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_parser__DOT__hdr[10U] 
                    = vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__hdr[8U];
                vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_parser__DOT__hdr[11U] 
                    = vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__hdr[9U];
                vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_parser__DOT__hdr[12U] 
                    = vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__hdr[10U];
                vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_parser__DOT__hdr[13U] 
                    = vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__hdr[11U];
            }
            if (vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__s_tlast_q) {
                vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__parsed = 0U;
            }
        }
        if (vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__leg_hit_w) {
            if ((0x00000010U & (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ram_waddr_w))) {
                if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ram_waddr_w) 
                              >> 3U)))) {
                    if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ram_waddr_w))) {
                        if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ram_waddr_w) 
                                      >> 1U)))) {
                            if ((1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ram_waddr_w)))) {
                                vlSelfRef.milan_datapath__DOT__avtprx_mreset_c 
                                    = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ram_wdata_w;
                            }
                            if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ram_waddr_w))) {
                                vlSelfRef.milan_datapath__DOT__avtprx_tu_c 
                                    = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ram_wdata_w;
                            }
                        }
                        if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ram_waddr_w))) {
                            if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ram_waddr_w))) {
                                vlSelfRef.milan_datapath__DOT__avtprx_late_c 
                                    = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ram_wdata_w;
                            }
                            if ((1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ram_waddr_w)))) {
                                vlSelfRef.milan_datapath__DOT__avtprx_unsupp_c 
                                    = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ram_wdata_w;
                            }
                        }
                    }
                    if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ram_waddr_w) 
                                  >> 2U)))) {
                        if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ram_waddr_w))) {
                            if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ram_waddr_w))) {
                                vlSelfRef.milan_datapath__DOT__avtprx_seqmm_c 
                                    = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ram_wdata_w;
                            }
                            if ((1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ram_waddr_w)))) {
                                vlSelfRef.milan_datapath__DOT__avtprx_intr_c 
                                    = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ram_wdata_w;
                            }
                        }
                        if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ram_waddr_w) 
                                      >> 1U)))) {
                            if ((1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ram_waddr_w)))) {
                                vlSelfRef.milan_datapath__DOT__avtprx_locked_c 
                                    = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ram_wdata_w;
                            }
                            if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ram_waddr_w))) {
                                vlSelfRef.milan_datapath__DOT__avtprx_unlocked_c 
                                    = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ram_wdata_w;
                            }
                        }
                    }
                }
                if ((8U & (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ram_waddr_w))) {
                    if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ram_waddr_w) 
                                  >> 2U)))) {
                        if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ram_waddr_w) 
                                      >> 1U)))) {
                            if ((1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ram_waddr_w)))) {
                                vlSelfRef.milan_datapath__DOT__avtprx_early_c 
                                    = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ram_wdata_w;
                            }
                            if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ram_waddr_w))) {
                                vlSelfRef.milan_datapath__DOT__avtprx_frx_c 
                                    = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ram_wdata_w;
                            }
                        }
                    }
                }
            }
            if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ram_waddr_w) 
                          >> 4U)))) {
                if ((8U & (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ram_waddr_w))) {
                    if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ram_waddr_w) 
                                  >> 2U)))) {
                        if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ram_waddr_w) 
                                      >> 1U)))) {
                            if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ram_waddr_w))) {
                                vlSelfRef.milan_datapath__DOT__avtprx_last_ts 
                                    = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ram_wdata_w;
                            }
                        }
                        if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ram_waddr_w))) {
                            if ((1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ram_waddr_w)))) {
                                vlSelfRef.milan_datapath__DOT__avtprx_last_tsd 
                                    = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__ram_wdata_w;
                            }
                        }
                    }
                }
            }
        }
        if (vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__push_ram_w) {
            if ((0U >= vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__skid_addr_r
                 [vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__skid_rp_r])) {
                vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_fed_r 
                    = ((IData)(vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_fed_r) 
                       | (1U & ((IData)(1U) << vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__skid_addr_r
                                [vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__skid_rp_r])));
            }
        }
        if (vlSelfRef.milan_datapath__DOT____Vcellinp__chan_map_capture__lb_flush_i) {
            vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_fed_r = 0U;
        }
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__lsn_q_r 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_out_w;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_org_cnt_r 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_org_next_cnt_w;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_lstn_reg_change_w = 0U;
        if (((3U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_out_w)) 
             != (3U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_prev_r)))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_prev_r 
                = ((0x03fcU & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_prev_r)) 
                   | (3U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_out_w)));
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_lstn_reg_change_w 
                = (1U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_lstn_reg_change_w));
        }
        if (((3U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_out_w) 
                    >> 2U)) != (3U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_prev_r) 
                                      >> 2U)))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_prev_r 
                = ((0x03f3U & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_prev_r)) 
                   | (0x0000000cU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_out_w)));
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_lstn_reg_change_w 
                = (2U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_lstn_reg_change_w));
        }
        if (((3U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_out_w) 
                    >> 4U)) != (3U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_prev_r) 
                                      >> 4U)))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_prev_r 
                = ((0x03cfU & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_prev_r)) 
                   | (0x00000030U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_out_w)));
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_lstn_reg_change_w 
                = (4U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_lstn_reg_change_w));
        }
        if (((3U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_out_w) 
                    >> 6U)) != (3U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_prev_r) 
                                      >> 6U)))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_prev_r 
                = ((0x033fU & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_prev_r)) 
                   | (0x000000c0U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_out_w)));
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_lstn_reg_change_w 
                = (8U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_lstn_reg_change_w));
        }
        if (((3U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_out_w) 
                    >> 8U)) != (3U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_prev_r) 
                                      >> 8U)))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_prev_r 
                = ((0x00ffU & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_prev_r)) 
                   | (0x00000300U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_out_w)));
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_lstn_reg_change_w 
                = (0x00000010U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_lstn_reg_change_w));
        }
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_evt_tk_reg_w = 0U;
        if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_rx_hit_w) 
             & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rx_registering_w))) {
            if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__ind_reg_w))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_evt_tk_reg_w 
                    = (1U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_evt_tk_reg_w));
            }
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rtype_r 
                = ((0x1eU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rtype_r)) 
                   | (2U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_attr_type_w)));
            if ((2U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_attr_type_w))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__fcode_r 
                    = ((0x000000ffffffff00ULL & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__fcode_r) 
                       | (IData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_fail_code_w)));
            }
        }
        if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_rx_hit_w) 
              >> 1U) & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rx_registering_w))) {
            if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__ind_reg_w))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_evt_tk_reg_w 
                    = (2U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_evt_tk_reg_w));
            }
        }
        if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_rx_hit_w) 
              >> 2U) & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rx_registering_w))) {
            if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__ind_reg_w))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_evt_tk_reg_w 
                    = (4U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_evt_tk_reg_w));
            }
        }
        if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_rx_hit_w) 
              >> 3U) & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rx_registering_w))) {
            if ((8U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__ind_reg_w))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_evt_tk_reg_w 
                    = (8U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_evt_tk_reg_w));
            }
        }
        if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT____Vcellinp__u_notify__ev_amap_i) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__amap_type_r 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cfg_ix_r;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__amap_index_r 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__desc_ix_r;
        }
        if (vlSelfRef.s_axi_awready) {
            vlSelfRef.milan_datapath__DOT__csr__DOT__b_valid = 1U;
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
                                                                            vlSelfRef.milan_datapath__DOT__csr__DOT__mac_ifg 
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
                                                                            vlSelfRef.milan_datapath__DOT__csr__DOT__mac_ctrl 
                                                                                = vlSelfRef.s_axi_wdata;
                                                                        }
                                                                    }
                                                                }
                                                            }
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
                                                                            vlSelfRef.milan_datapath__DOT__csr__DOT__mac_ahi 
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
                                                                            vlSelfRef.milan_datapath__DOT__csr__DOT__mac_alo 
                                                                                = vlSelfRef.s_axi_wdata;
                                                                        }
                                                                    }
                                                                }
                                                            }
                                                        }
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
                                                                            vlSelfRef.milan_datapath__DOT__csr__DOT__mc_hi 
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
                                                                            vlSelfRef.milan_datapath__DOT__csr__DOT__mc_lo 
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
                                                                            vlSelfRef.milan_datapath__DOT__csr__DOT__irq_mask 
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
                                                                            vlSelfRef.milan_datapath__DOT__csr__DOT__lpf_ctrl 
                                                                                = vlSelfRef.s_axi_wdata;
                                                                        }
                                                                    }
                                                                }
                                                            }
                                                        }
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
                                                                            vlSelfRef.milan_datapath__DOT__csr__DOT__crf_sidlo 
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
                                                                            vlSelfRef.milan_datapath__DOT__csr__DOT__crf_ctrl 
                                                                                = vlSelfRef.s_axi_wdata;
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
                                                                            vlSelfRef.milan_datapath__DOT__csr__DOT__tcam_ctrl 
                                                                                = vlSelfRef.s_axi_wdata;
                                                                        }
                                                                    }
                                                                }
                                                            }
                                                        }
                                                    }
                                                }
                                                if (
                                                    (0x00000040U 
                                                     & (IData)(vlSelfRef.s_axi_awaddr))) {
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
                                                                            vlSelfRef.milan_datapath__DOT__csr__DOT__crft_dmhi 
                                                                                = vlSelfRef.s_axi_wdata;
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
                                                                            vlSelfRef.milan_datapath__DOT__csr__DOT__crft_dmlo 
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
                                                                            vlSelfRef.milan_datapath__DOT__csr__DOT__crft_sidhi 
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
                                                                            vlSelfRef.milan_datapath__DOT__csr__DOT__crft_sidlo 
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
                                                                            vlSelfRef.milan_datapath__DOT__csr__DOT__crft_ctrl 
                                                                                = vlSelfRef.s_axi_wdata;
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
                                                                            vlSelfRef.milan_datapath__DOT__csr__DOT__crf_sidhi 
                                                                                = vlSelfRef.s_axi_wdata;
                                                                        }
                                                                    }
                                                                }
                                                            }
                                                        }
                                                    }
                                                }
                                            }
                                            if ((0x00000080U 
                                                 & (IData)(vlSelfRef.s_axi_awaddr))) {
                                                if (
                                                    (1U 
                                                     & (~ 
                                                        ((IData)(vlSelfRef.s_axi_awaddr) 
                                                         >> 6U)))) {
                                                    if (
                                                        (0x00000020U 
                                                         & (IData)(vlSelfRef.s_axi_awaddr))) {
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
                                                                            if (
                                                                                ((vlSelfRef.s_axi_wdata 
                                                                                >> 0x0000001fU) 
                                                                                & (~ (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rest_pend_r)))) {
                                                                                vlSelfRef.milan_datapath__DOT__csr__DOT__rest_pend_r = 1U;
                                                                                vlSelfRef.milan_datapath__DOT__csr__DOT__rest_done_r = 0U;
                                                                                vlSelfRef.milan_datapath__DOT__csr__DOT__rest_stat_r = 0U;
                                                                                vlSelfRef.milan_datapath__DOT__csr__DOT__rest_idx_r 
                                                                                = 
                                                                                (0x0000000fU 
                                                                                & vlSelfRef.s_axi_wdata);
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
                                                                            vlSelfRef.milan_datapath__DOT__csr__DOT__adp_ctrl 
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
                                                                            vlSelfRef.milan_datapath__DOT__csr__DOT__adp_eidlo 
                                                                                = vlSelfRef.s_axi_wdata;
                                                                        }
                                                                    }
                                                                }
                                                            }
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
                                                                            vlSelfRef.milan_datapath__DOT__csr__DOT__adp_midlo 
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
                                                                            vlSelfRef.milan_datapath__DOT__csr__DOT__adp_eidhi 
                                                                                = vlSelfRef.s_axi_wdata;
                                                                        }
                                                                    }
                                                                }
                                                            }
                                                        }
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
                                                                            vlSelfRef.milan_datapath__DOT__csr__DOT__adp_midhi 
                                                                                = vlSelfRef.s_axi_wdata;
                                                                        }
                                                                    }
                                                                }
                                                            }
                                                        }
                                                    }
                                                    if (
                                                        (0x00000020U 
                                                         & (IData)(vlSelfRef.s_axi_awaddr))) {
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
                                                                            vlSelfRef.milan_datapath__DOT__csr__DOT__adp_idx0 
                                                                                = vlSelfRef.s_axi_wdata;
                                                                        }
                                                                    }
                                                                }
                                                            }
                                                        }
                                                    }
                                                }
                                            }
                                            if ((0x00000080U 
                                                 & (IData)(vlSelfRef.s_axi_awaddr))) {
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
                                                                            vlSelfRef.milan_datapath__DOT__csr__DOT__lwsrp_vid 
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
                                                                            vlSelfRef.milan_datapath__DOT__csr__DOT__strm_lsn0_r 
                                                                                = 
                                                                                (1U 
                                                                                & (vlSelfRef.s_axi_wdata 
                                                                                >> 9U));
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
            if ((0x0920U != (IData)(vlSelfRef.s_axi_awaddr))) {
                if ((0x0934U != (IData)(vlSelfRef.s_axi_awaddr))) {
                    if ((0x0938U == (IData)(vlSelfRef.s_axi_awaddr))) {
                        vlSelfRef.milan_datapath__DOT__csr__DOT__g_pp_csr__DOT__pp_nvm_waddr_r 
                            = vlSelfRef.milan_datapath__DOT__csr__DOT__g_pp_csr__DOT__pp_nvm_sel_r;
                    } else if ((0x093cU == (IData)(vlSelfRef.s_axi_awaddr))) {
                        vlSelfRef.milan_datapath__DOT__csr__DOT__g_pp_csr__DOT__pp_nvm_waddr_r = 4U;
                    }
                }
            }
        } else if (vlSelfRef.s_axi_bready) {
            vlSelfRef.milan_datapath__DOT__csr__DOT__b_valid = 0U;
        }
        vlSelfRef.milan_datapath__DOT__mon_wire_chans_w 
            = vlSelfRef.milan_datapath__DOT__avtp_rx_monitor__DOT__chans_sh_r
            [(3U & (IData)(vlSelfRef.milan_datapath__DOT__route_render_sel_w))];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_org_r 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_org_next_w;
        vlSelfRef.milan_datapath__DOT__lb_skip_cnt_w 
            = ((0x00010000U & vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__skip_sum_w)
                ? 0x0000ffffU : (0x0000ffffU & vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__skip_sum_w));
        if (vlSelfRef.milan_datapath__DOT__csr__DOT__cmrd_go_w) {
            vlSelfRef.milan_datapath__DOT__csr__DOT__cmrd_armed_r = 1U;
            vlSelfRef.milan_datapath__DOT__csr__DOT__cmrd_unsup_r = 0U;
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
        vlSelfRef.milan_datapath__DOT__lb_dup_cnt_w 
            = ((0x00010000U & vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__dup_sum_w)
                ? 0x0000ffffU : (0x0000ffffU & vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__dup_sum_w));
        if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__vd_push_w) 
             & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__vq_full_w)))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__vpushed_r = 1U;
        }
        if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__ser_busy_r) {
            if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__end_w) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__vpushed_r = 0U;
            }
        }
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_release_merge__DOT__pending_r 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_release_merge__DOT__available_w;
        if (Vmilan_datapath__ConstPool__TABLE_h5f1389fb_0
            [vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_release_merge__DOT__available_w]) {
            if ((4U >= Vmilan_datapath__ConstPool__TABLE_h6dff1152_0
                 [vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_release_merge__DOT__available_w])) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_release_merge__DOT__pending_r 
                    = ((~ ((IData)(1U) << Vmilan_datapath__ConstPool__TABLE_h6dff1152_0
                           [vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_release_merge__DOT__available_w])) 
                       & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_release_merge__DOT__pending_r));
            }
        }
        if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__maap_accept_w) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__maap_busy_r = 1U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__maap_t0_r 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__now_ms_r;
        } else if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__maap_rsp_live_w) 
                    | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__maap_rsp_tmo_w))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__maap_busy_r = 0U;
        }
        if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__arm_w) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__arm_ref_r 
                = (1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__arm_ok_w)));
        }
        if (vlSelfRef.milan_datapath__DOT__crf_rx__DOT__w_hit) {
            if (vlSelfRef.milan_datapath__DOT__crf_rx__DOT__w_fmt_ok) {
                vlSelfRef.milan_datapath__DOT__crf_delta_w 
                    = vlSelfRef.milan_datapath__DOT__crf_rx__DOT__w_tsd;
                vlSelfRef.milan_datapath__DOT__crf_rx__DOT__prev_mr_r 
                    = vlSelfRef.milan_datapath__DOT__avtprx_mr_bit;
            }
        }
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__rd_data_r 
            = ((2U == (0x0000000fU & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__st_addr_w 
                                      >> 0x00000010U)))
                ? vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__vld_w
                : vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__val_w);
        if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__take_wr_w) {
            if ((0U == (0x00001fffU & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__st_addr_w 
                                       >> 3U)))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__cfg_v_r = 1U;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__cfg_r 
                    = (0x0000ffffU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__opa_e_r));
            }
            if ((0U != (0x00001fffU & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__st_addr_w 
                                       >> 3U)))) {
                if ((1U != (0x00001fffU & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__st_addr_w 
                                           >> 3U)))) {
                    if ((2U == (0x00001fffU & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__st_addr_w 
                                               >> 3U)))) {
                        if ((0U >= (1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT____Vcellinp__u_dyn__desc_index_i)))) {
                            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__clksrc_v_r 
                                = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__clksrc_v_r) 
                                   | (1U & ((IData)(1U) 
                                            << (1U 
                                                & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT____Vcellinp__u_dyn__desc_index_i)))));
                        }
                    }
                    if ((2U != (0x00001fffU & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__st_addr_w 
                                               >> 3U)))) {
                        if ((3U != (0x00001fffU & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__st_addr_w 
                                                   >> 3U)))) {
                            if ((4U != (0x00001fffU 
                                        & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__st_addr_w 
                                           >> 3U)))) {
                                if ((5U != (0x00001fffU 
                                            & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__st_addr_w 
                                               >> 3U)))) {
                                    if ((7U == (0x00001fffU 
                                                & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__st_addr_w 
                                                   >> 3U)))) {
                                        if ((0U >= 
                                             (1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT____Vcellinp__u_dyn__desc_index_i)))) {
                                            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__ident_v_r 
                                                = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__ident_v_r) 
                                                   | (1U 
                                                      & ((IData)(1U) 
                                                         << 
                                                         (1U 
                                                          & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT____Vcellinp__u_dyn__desc_index_i)))));
                                        }
                                    }
                                }
                                if ((5U == (0x00001fffU 
                                            & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__st_addr_w 
                                               >> 3U)))) {
                                    if ((4U >= (7U 
                                                & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT____Vcellinp__u_dyn__desc_index_i)))) {
                                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__ptoff_v_r 
                                            = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__ptoff_v_r) 
                                               | (0x1fU 
                                                  & ((IData)(1U) 
                                                     << 
                                                     (7U 
                                                      & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT____Vcellinp__u_dyn__desc_index_i)))));
                                    }
                                }
                            }
                        }
                    }
                }
                if ((1U == (0x00001fffU & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__st_addr_w 
                                           >> 3U)))) {
                    if ((0U >= (1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT____Vcellinp__u_dyn__desc_index_i)))) {
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__rate_v_r 
                            = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__rate_v_r) 
                               | (1U & ((IData)(1U) 
                                        << (1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT____Vcellinp__u_dyn__desc_index_i)))));
                    }
                }
            }
        }
        if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__commit_ack_w) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__ack_ref_r 
                = (1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__ack_ok_w)));
        } else if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__arm_ok_w) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__ack_ref_r = 0U;
        }
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__adp_evt_valid_w = 0U;
        if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__iter_evt_w) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__adp_evt_valid_w = 1U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__adp_evt_departed_w 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__ev_dep_w;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__adp_evt_sink_w 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__sink_r;
        } else if ((5U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__rx_st_r))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__adp_evt_valid_w = 1U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__adp_evt_departed_w = 0U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__adp_evt_sink_w 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__sink_r;
        } else if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__drain_any_w) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__adp_evt_valid_w = 1U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__adp_evt_departed_w = 1U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__adp_evt_sink_w 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__drain_sink_w;
        }
        if (vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__s_ok_w) {
            vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__evt_drop_r 
                = vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__drop1_w;
        }
        if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__reload_ok_w) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__ld_acc_r = 1U;
        }
        if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__reload_w) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__rl_ref_r 
                = (1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__reload_ok_w)));
        }
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__org_arm_valid_w = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__org_send_valid_w = 0U;
        if ((((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__link_up_q_r)) 
              & (IData)(vlSelfRef.milan_datapath__DOT__eff_link_w)) 
             & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__seeded_r)))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_r 
                = ((0ULL == vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__seed_w)
                    ? 1ULL : vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__seed_w);
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__seeded_r = 1U;
        } else {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_r 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_next_w;
        }
        if (vlSelfRef.milan_datapath__DOT__link_guard__DOT__tx_trans_w) {
            vlSelfRef.__Vdly__milan_datapath__DOT__link_guard__DOT__tx_dead_r = 0U;
        } else if ((0x1000U != (IData)(vlSelfRef.milan_datapath__DOT__link_guard__DOT__tx_dead_r))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__link_guard__DOT__tx_dead_r 
                = (0x00001fffU & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__link_guard__DOT__tx_dead_r)));
        }
        vlSelfRef.milan_datapath__DOT__link_guard__DOT__tx_alive_r 
            = (1U & (((~ (IData)(vlSelfRef.milan_datapath__DOT__link_guard__DOT__tx_armed_r)) 
                      | (0x1000U != (IData)(vlSelfRef.milan_datapath__DOT__link_guard__DOT__tx_dead_r))) 
                     | (IData)(vlSelfRef.milan_datapath__DOT__link_guard__DOT__tx_trans_w)));
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__arm_q_slot_r 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tmr_arm_slot_w;
        if ((vlSelfRef.milan_datapath__DOT__crft_count_w 
             != vlSelfRef.milan_datapath__DOT__tkd_crfq_r)) {
            vlSelfRef.milan_datapath__DOT__tkd_crf_pend_r = 1U;
        } else if (vlSelfRef.milan_datapath__DOT__tkd_crf_p_w) {
            vlSelfRef.milan_datapath__DOT__tkd_crf_pend_r = 0U;
        }
        if (vlSelfRef.milan_datapath__DOT__link_guard__DOT__rx_trans_w) {
            vlSelfRef.__Vdly__milan_datapath__DOT__link_guard__DOT__rx_dead_r = 0U;
        } else if ((0x1000U != (IData)(vlSelfRef.milan_datapath__DOT__link_guard__DOT__rx_dead_r))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__link_guard__DOT__rx_dead_r 
                = (0x00001fffU & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__link_guard__DOT__rx_dead_r)));
        }
        vlSelfRef.milan_datapath__DOT__link_guard__DOT__rx_alive_r 
            = (1U & (((~ (IData)(vlSelfRef.milan_datapath__DOT__link_guard__DOT__rx_armed_r)) 
                      | (0x1000U != (IData)(vlSelfRef.milan_datapath__DOT__link_guard__DOT__rx_dead_r))) 
                     | (IData)(vlSelfRef.milan_datapath__DOT__link_guard__DOT__rx_trans_w)));
        if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__deliver_w) {
            __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_next__64__s 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__sel_r;
            __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_next__64__Vfuncout 
                = ((0x13U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_next__64__s))
                    ? 0U : (0x0000001fU & ((IData)(1U) 
                                           + (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_next__64__s))));
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__ptr_r 
                = __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_next__64__Vfuncout;
        }
        if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__adv_exp_w) 
              & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__chk_slot_r))) 
             & (2U == vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__adv_st_r[0U]))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__pend_avail_r = 1U;
        }
        if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__enable_fall_w) 
             & (0U != vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__adv_st_r[0U]))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__pend_avail_r = 0U;
        }
        if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__link_fall_w) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__pend_avail_r = 0U;
        }
        if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__bld_take_w) 
             & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__pick_if_w)))) {
            if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__pick_dep_w) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__pend_dep_r = 0U;
            }
            if ((1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__pick_dep_w)))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__pend_avail_r = 0U;
            }
        }
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__org_resend_valid_w = 0U;
        if ((1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__ev_rsp_w)))) {
            if ((1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__ev_cancel_w)))) {
                if ((1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__ev_accept_w)))) {
                    if ((1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__ev_exp_w)))) {
                        if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__ev_iss_w) {
                            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__org_send_valid_w = 1U;
                            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__org_send_slot_w 
                                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_ca_builder__DOT__slot_r;
                        }
                    }
                    if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__ev_exp_w) {
                        if ((1U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__valid_r) 
                                   >> (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__pend_ix_w)))) {
                            if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__retried_r) 
                                          >> (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__pend_ix_w))))) {
                                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__org_resend_valid_w = 1U;
                                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__org_resend_slot_w 
                                    = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__txs_r
                                    [vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__pend_ix_w];
                            }
                        }
                    }
                }
            }
        }
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__org_release_valid_w = 0U;
        if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__ntfy_ca_cancel_valid_w) 
             & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__cancel_hit_w))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__cancel_pend_r 
                = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__cancel_pend_r) 
                   | (0x0000ffffU & ((IData)(1U) << (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__cancel_ix_w))));
        }
        if (((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_pend2) 
             | (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rds_done_w))) {
            vlSelfRef.milan_datapath__DOT__csr__DOT__r_valid = 1U;
        } else if (vlSelfRef.s_axi_rready) {
            vlSelfRef.milan_datapath__DOT__csr__DOT__r_valid = 0U;
        }
        if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__exp_fire_w) 
             & ((0x20U <= (0x000000ffU & (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__sweep_rdata_r 
                                                  >> 0x00000020U)))) 
                & (0x25U > (0x000000ffU & (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__sweep_rdata_r 
                                                   >> 0x00000020U))))))) {
            if ((4U >= (7U & (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__sweep_rdata_r 
                                      >> 0x00000020U))))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__pendexp_r 
                    = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__pendexp_r) 
                       | (0x1fU & ((IData)(1U) << (7U 
                                                   & (IData)(
                                                             (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__sweep_rdata_r 
                                                              >> 0x00000020U))))));
            }
        }
        if (((8U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__xs_r)) 
             & ((0x0aU == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__cur_act_w)) 
                & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__apend_r 
                   >> 0x0000000aU)))) {
            if ((4U >= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__sink_r))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__pendexp_r 
                    = ((~ ((IData)(1U) << (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__sink_r))) 
                       & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__pendexp_r));
            }
        }
        if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__pend_any_w) 
             & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_213))) {
            if ((4U >= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__pend_sink_w))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__pendexp_r 
                    = ((~ ((IData)(1U) << (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__pend_sink_w))) 
                       & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__pendexp_r));
            }
        }
        if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT____Vcellout__g_rx_pool__BRA__4__KET____DOT__u_rx_slots__alloc_gnt_o) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__4__KET____DOT__u_rx_slots__DOT__writing_r 
                = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__4__KET____DOT__u_rx_slots__DOT__writing_r) 
                   | (0x0fU & ((IData)(1U) << (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__4__KET____DOT__u_rx_slots__DOT__ff_slot_w))));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__4__KET____DOT__u_rx_slots__DOT__wr_active_r = 1U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__4__KET____DOT__u_rx_slots__DOT__wr_closed_r = 0U;
        }
        if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__4__KET____DOT__u_rx_slots__DOT__wr_active_r) 
             & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__abort_pend_r))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__4__KET____DOT__u_rx_slots__DOT__writing_r 
                = ((~ ((IData)(1U) << (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__4__KET____DOT__u_rx_slots__DOT__cur_slot_r))) 
                   & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__4__KET____DOT__u_rx_slots__DOT__writing_r));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__4__KET____DOT__u_rx_slots__DOT__wr_active_r = 0U;
        } else if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__4__KET____DOT__u_rx_slots__DOT__wr_active_r) 
                    & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__cp_r) 
                       >> 1U))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__4__KET____DOT__u_rx_slots__DOT__writing_r 
                = ((~ ((IData)(1U) << (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__4__KET____DOT__u_rx_slots__DOT__cur_slot_r))) 
                   & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__4__KET____DOT__u_rx_slots__DOT__writing_r));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__4__KET____DOT__u_rx_slots__DOT__occupied_r 
                = ((IData)(vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__4__KET____DOT__u_rx_slots__DOT__occupied_r) 
                   | (0x0fU & ((IData)(1U) << (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__4__KET____DOT__u_rx_slots__DOT__cur_slot_r))));
            vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__4__KET____DOT__u_rx_slots__DOT__len_r__v0 
                = (0x000003ffU & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__4__KET____DOT__u_rx_slots__DOT__wr_ptr_r) 
                                  + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__4__KET____DOT__u_rx_slots__DOT__byte_acc_w)));
            vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__4__KET____DOT__u_rx_slots__DOT__len_r__v0 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__4__KET____DOT__u_rx_slots__DOT__cur_slot_r;
            vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__4__KET____DOT__u_rx_slots__DOT__len_r__v0 = 1U;
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__4__KET____DOT__u_rx_slots__DOT__wr_active_r = 0U;
        }
        if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxf_free_w) 
             & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__4__KET____DOT__u_rx_slots__DOT__occupied_r) 
                >> (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxf_free_slot_w)))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__4__KET____DOT__u_rx_slots__DOT__occupied_r 
                = ((~ ((IData)(1U) << (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxf_free_slot_w))) 
                   & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__4__KET____DOT__u_rx_slots__DOT__occupied_r));
        }
        if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT____Vcellout__g_rx_pool__BRA__2__KET____DOT__u_rx_slots__alloc_gnt_o) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__2__KET____DOT__u_rx_slots__DOT__writing_r 
                = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__2__KET____DOT__u_rx_slots__DOT__writing_r) 
                   | (0x0fU & ((IData)(1U) << (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__2__KET____DOT__u_rx_slots__DOT__ff_slot_w))));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__2__KET____DOT__u_rx_slots__DOT__wr_active_r = 1U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__2__KET____DOT__u_rx_slots__DOT__wr_closed_r = 0U;
        }
        if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__2__KET____DOT__u_rx_slots__DOT__wr_active_r) 
             & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__abort_pend_r))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__2__KET____DOT__u_rx_slots__DOT__writing_r 
                = ((~ ((IData)(1U) << (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__2__KET____DOT__u_rx_slots__DOT__cur_slot_r))) 
                   & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__2__KET____DOT__u_rx_slots__DOT__writing_r));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__2__KET____DOT__u_rx_slots__DOT__wr_active_r = 0U;
        } else if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__2__KET____DOT__u_rx_slots__DOT__wr_active_r) 
                    & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__cp_r) 
                       >> 1U))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__2__KET____DOT__u_rx_slots__DOT__writing_r 
                = ((~ ((IData)(1U) << (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__2__KET____DOT__u_rx_slots__DOT__cur_slot_r))) 
                   & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__2__KET____DOT__u_rx_slots__DOT__writing_r));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__2__KET____DOT__u_rx_slots__DOT__occupied_r 
                = ((IData)(vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__2__KET____DOT__u_rx_slots__DOT__occupied_r) 
                   | (0x0fU & ((IData)(1U) << (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__2__KET____DOT__u_rx_slots__DOT__cur_slot_r))));
            vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__2__KET____DOT__u_rx_slots__DOT__len_r__v0 
                = (0x000003ffU & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__2__KET____DOT__u_rx_slots__DOT__wr_ptr_r) 
                                  + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__2__KET____DOT__u_rx_slots__DOT__byte_acc_w)));
            vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__2__KET____DOT__u_rx_slots__DOT__len_r__v0 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__2__KET____DOT__u_rx_slots__DOT__cur_slot_r;
            vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__2__KET____DOT__u_rx_slots__DOT__len_r__v0 = 1U;
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__2__KET____DOT__u_rx_slots__DOT__wr_active_r = 0U;
        }
        if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxf_free_w) 
             & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__2__KET____DOT__u_rx_slots__DOT__occupied_r) 
                >> (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxf_free_slot_w)))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__2__KET____DOT__u_rx_slots__DOT__occupied_r 
                = ((~ ((IData)(1U) << (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxf_free_slot_w))) 
                   & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__2__KET____DOT__u_rx_slots__DOT__occupied_r));
        }
        if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT____Vcellout__g_rx_pool__BRA__1__KET____DOT__u_rx_slots__alloc_gnt_o) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__1__KET____DOT__u_rx_slots__DOT__writing_r 
                = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__1__KET____DOT__u_rx_slots__DOT__writing_r) 
                   | (0x0fU & ((IData)(1U) << (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__1__KET____DOT__u_rx_slots__DOT__ff_slot_w))));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__1__KET____DOT__u_rx_slots__DOT__wr_active_r = 1U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__1__KET____DOT__u_rx_slots__DOT__wr_closed_r = 0U;
        }
        if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__1__KET____DOT__u_rx_slots__DOT__wr_active_r) 
             & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__abort_pend_r))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__1__KET____DOT__u_rx_slots__DOT__writing_r 
                = ((~ ((IData)(1U) << (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__1__KET____DOT__u_rx_slots__DOT__cur_slot_r))) 
                   & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__1__KET____DOT__u_rx_slots__DOT__writing_r));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__1__KET____DOT__u_rx_slots__DOT__wr_active_r = 0U;
        } else if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__1__KET____DOT__u_rx_slots__DOT__wr_active_r) 
                    & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__cp_r) 
                       >> 1U))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__1__KET____DOT__u_rx_slots__DOT__writing_r 
                = ((~ ((IData)(1U) << (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__1__KET____DOT__u_rx_slots__DOT__cur_slot_r))) 
                   & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__1__KET____DOT__u_rx_slots__DOT__writing_r));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__1__KET____DOT__u_rx_slots__DOT__occupied_r 
                = ((IData)(vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__1__KET____DOT__u_rx_slots__DOT__occupied_r) 
                   | (0x0fU & ((IData)(1U) << (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__1__KET____DOT__u_rx_slots__DOT__cur_slot_r))));
            vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__1__KET____DOT__u_rx_slots__DOT__len_r__v0 
                = (0x000003ffU & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__1__KET____DOT__u_rx_slots__DOT__wr_ptr_r) 
                                  + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__1__KET____DOT__u_rx_slots__DOT__byte_acc_w)));
            vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__1__KET____DOT__u_rx_slots__DOT__len_r__v0 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__1__KET____DOT__u_rx_slots__DOT__cur_slot_r;
            vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__1__KET____DOT__u_rx_slots__DOT__len_r__v0 = 1U;
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__1__KET____DOT__u_rx_slots__DOT__wr_active_r = 0U;
        }
        if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxf_free_w) 
             & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__1__KET____DOT__u_rx_slots__DOT__occupied_r) 
                >> (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxf_free_slot_w)))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__1__KET____DOT__u_rx_slots__DOT__occupied_r 
                = ((~ ((IData)(1U) << (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxf_free_slot_w))) 
                   & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__1__KET____DOT__u_rx_slots__DOT__occupied_r));
        }
        if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT____Vcellout__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__alloc_gnt_o) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__DOT__writing_r 
                = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__DOT__writing_r) 
                   | (0x0fU & ((IData)(1U) << (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__DOT__ff_slot_w))));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__DOT__wr_active_r = 1U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__DOT__wr_closed_r = 0U;
        }
        if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__DOT__wr_active_r) 
             & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__abort_pend_r))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__DOT__writing_r 
                = ((~ ((IData)(1U) << (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__DOT__cur_slot_r))) 
                   & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__DOT__writing_r));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__DOT__wr_active_r = 0U;
        } else if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__DOT__wr_active_r) 
                    & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__cp_r) 
                       >> 1U))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__DOT__writing_r 
                = ((~ ((IData)(1U) << (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__DOT__cur_slot_r))) 
                   & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__DOT__writing_r));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__DOT__occupied_r 
                = ((IData)(vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__DOT__occupied_r) 
                   | (0x0fU & ((IData)(1U) << (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__DOT__cur_slot_r))));
            vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__DOT__len_r__v0 
                = (0x000003ffU & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__DOT__wr_ptr_r) 
                                  + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__DOT__byte_acc_w)));
            vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__DOT__len_r__v0 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__DOT__cur_slot_r;
            vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__DOT__len_r__v0 = 1U;
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__DOT__wr_active_r = 0U;
        }
        if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxf_free_w) 
             & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__DOT__occupied_r) 
                >> (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxf_free_slot_w)))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__DOT__occupied_r 
                = ((~ ((IData)(1U) << (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxf_free_slot_w))) 
                   & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__DOT__occupied_r));
        }
        if (((IData)(vlSelfRef.milan_datapath__DOT__rend_pcm_tvalid_w) 
             & (~ (IData)(vlSelfRef.milan_datapath__DOT__pcm_lpf_active)))) {
            vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__xl2_r 
                = vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__xl1_r;
            vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__yl2_r 
                = vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__yl1_r;
            vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__xr2_r 
                = vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__xr1_r;
            vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__yr2_r 
                = vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__yr1_r;
            vlSelfRef.__Vdly__milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__xl1_r 
                = vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__xl_in;
            vlSelfRef.__Vdly__milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__yl1_r 
                = vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__xl_in;
            vlSelfRef.__Vdly__milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__xr1_r 
                = vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__xr_in;
            vlSelfRef.__Vdly__milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__yr1_r 
                = vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__xr_in;
        }
        if (vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__bpop_w) {
            vlSelfRef.__Vdly__milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__busy_r = 1U;
            vlSelfRef.__Vdly__milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__step_r = 0U;
            vlSelfRef.__Vdly__milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__acc_r = 0ULL;
        } else if (vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__busy_r) {
            if (((IData)(vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__busy_r) 
                 & (5U == (IData)(vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__step_r)))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__step_r 
                    = (0x0000000fU & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__step_r)));
                vlSelfRef.__Vdly__milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__yl_hold_r 
                    = vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__yfin_w;
                vlSelfRef.__Vdly__milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__acc_r 
                    = (0x00000fffffffffffULL & ((IData)(vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__sub_w)
                                                 ? 
                                                (- 
                                                 VL_EXTENDS_QQ(44,41, vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__prod_w))
                                                 : 
                                                VL_EXTENDS_QQ(44,41, vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__prod_w)));
            } else if (((IData)(vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__busy_r) 
                        & (0x0aU == (IData)(vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__step_r)))) {
                vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__xl2_r 
                    = vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__xl1_r;
                vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__yl2_r 
                    = vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__yl1_r;
                vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__xr2_r 
                    = vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__xr1_r;
                vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__yr2_r 
                    = vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__yr1_r;
                vlSelfRef.__Vdly__milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__busy_r = 0U;
                vlSelfRef.__Vdly__milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__xl1_r 
                    = vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__curl_r;
                vlSelfRef.__Vdly__milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__yl1_r 
                    = vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__yl_hold_r;
                vlSelfRef.__Vdly__milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__xr1_r 
                    = vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__curr_r;
                vlSelfRef.__Vdly__milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__yr1_r 
                    = vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__yfin_w;
            } else {
                vlSelfRef.__Vdly__milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__acc_r 
                    = (0x00000fffffffffffULL & (vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__acc_r 
                                                + ((IData)(vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__sub_w)
                                                    ? 
                                                   (- 
                                                    VL_EXTENDS_QQ(44,41, vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__prod_w))
                                                    : 
                                                   VL_EXTENDS_QQ(44,41, vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__prod_w))));
                vlSelfRef.__Vdly__milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__step_r 
                    = (0x0000000fU & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__step_r)));
            }
        }
        if ((1U & vlSelfRef.milan_datapath__DOT__csr__DOT__tone_ctrl)) {
            if (vlSelfRef.milan_datapath__DOT__media_tick_p) {
                vlSelfRef.__Vdly__milan_datapath__DOT__tone_gen_media__DOT__idx_r 
                    = ((0x2fU == (IData)(vlSelfRef.milan_datapath__DOT__tone_gen_media__DOT__idx_r))
                        ? 0U : (0x0000003fU & ((IData)(1U) 
                                               + (IData)(vlSelfRef.milan_datapath__DOT__tone_gen_media__DOT__idx_r))));
                vlSelfRef.milan_datapath__DOT__tone_smp_media 
                    = (0x00ffffffU & VL_SHIFTRS_III(24,24,3, 
                                                    ((0x2fU 
                                                      >= (IData)(vlSelfRef.milan_datapath__DOT__tone_gen_media__DOT__idx_r))
                                                      ? vlSelfRef.milan_datapath__DOT__tone_gen_media__DOT__TONE_TAB_C
                                                     [vlSelfRef.milan_datapath__DOT__tone_gen_media__DOT__idx_r]
                                                      : 0U), 
                                                    (7U 
                                                     & (vlSelfRef.milan_datapath__DOT__csr__DOT__tone_ctrl 
                                                        >> 1U))));
            }
        } else {
            vlSelfRef.__Vdly__milan_datapath__DOT__tone_gen_media__DOT__idx_r = 0U;
            vlSelfRef.milan_datapath__DOT__tone_smp_media = 0U;
        }
        if (vlSelfRef.milan_datapath__DOT__ptp_sync__DOT__tod_rd_valid_reg) {
            vlSelfRef.milan_datapath__DOT__csr__DOT__ptp_tod_rd 
                = vlSelfRef.milan_datapath__DOT__ptp_sync__DOT__tod_rd_reg;
        }
        if (((IData)(vlSelfRef.milan_datapath__DOT__avtprx_parse_p) 
             & (~ ((IData)(vlSelfRef.milan_datapath__DOT__avtprx_subtype) 
                   >> 7U)))) {
            vlSelfRef.milan_datapath__DOT__g_aprb__DOT__aprb_subtype_r 
                = vlSelfRef.milan_datapath__DOT__avtprx_subtype;
            vlSelfRef.milan_datapath__DOT__g_aprb__DOT__aprb_sid_r 
                = vlSelfRef.milan_datapath__DOT__avtprx_sid_frame;
            vlSelfRef.milan_datapath__DOT__g_aprb__DOT__aprb_hit_r 
                = vlSelfRef.milan_datapath__DOT__avtprx_match;
            vlSelfRef.milan_datapath__DOT__g_aprb__DOT__aprb_idx_r 
                = vlSelfRef.milan_datapath__DOT__avtprx_idx;
        }
        if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__v_alloc_gnt_w) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__0__KET____DOT__u_rx_slots__DOT__writing_r 
                = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__0__KET____DOT__u_rx_slots__DOT__writing_r) 
                   | (0x0fU & ((IData)(1U) << (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__0__KET____DOT__u_rx_slots__DOT__ff_slot_w))));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__0__KET____DOT__u_rx_slots__DOT__wr_active_r = 1U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__0__KET____DOT__u_rx_slots__DOT__wr_closed_r = 0U;
        }
        if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__0__KET____DOT__u_rx_slots__DOT__wr_active_r) 
             & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__abort_pend_r))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__0__KET____DOT__u_rx_slots__DOT__writing_r 
                = ((~ ((IData)(1U) << (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__0__KET____DOT__u_rx_slots__DOT__cur_slot_r))) 
                   & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__0__KET____DOT__u_rx_slots__DOT__writing_r));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__0__KET____DOT__u_rx_slots__DOT__wr_active_r = 0U;
        } else if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__0__KET____DOT__u_rx_slots__DOT__wr_active_r) 
                    & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__cp_r) 
                       >> 1U))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__0__KET____DOT__u_rx_slots__DOT__writing_r 
                = ((~ ((IData)(1U) << (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__0__KET____DOT__u_rx_slots__DOT__cur_slot_r))) 
                   & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__0__KET____DOT__u_rx_slots__DOT__writing_r));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__0__KET____DOT__u_rx_slots__DOT__occupied_r 
                = ((IData)(vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__0__KET____DOT__u_rx_slots__DOT__occupied_r) 
                   | (0x0fU & ((IData)(1U) << (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__0__KET____DOT__u_rx_slots__DOT__cur_slot_r))));
            vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__0__KET____DOT__u_rx_slots__DOT__len_r__v0 
                = (0x000003ffU & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__0__KET____DOT__u_rx_slots__DOT__wr_ptr_r) 
                                  + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__0__KET____DOT__u_rx_slots__DOT__byte_acc_w)));
            vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__0__KET____DOT__u_rx_slots__DOT__len_r__v0 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__0__KET____DOT__u_rx_slots__DOT__cur_slot_r;
            vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__0__KET____DOT__u_rx_slots__DOT__len_r__v0 = 1U;
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__0__KET____DOT__u_rx_slots__DOT__wr_active_r = 0U;
        }
        if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxf_free_w) 
             & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__0__KET____DOT__u_rx_slots__DOT__occupied_r) 
                >> (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxf_free_slot_w)))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__0__KET____DOT__u_rx_slots__DOT__occupied_r 
                = ((~ ((IData)(1U) << (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxf_free_slot_w))) 
                   & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__0__KET____DOT__u_rx_slots__DOT__occupied_r));
        }
        vlSelfRef.milan_datapath__DOT__tkd_dirty_p_w = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__talker_diag__DOT__seen_f_r 
            = ((IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__seen_f_r) 
               | (IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__ev_f_w));
        vlSelfRef.__Vdly__milan_datapath__DOT__talker_diag__DOT__seen_tu_r 
            = ((IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__seen_tu_r) 
               | (IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__ev_tu_w));
        vlSelfRef.__Vdly__milan_datapath__DOT__talker_diag__DOT__seen_tu_r 
            = ((IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__seen_tu_r) 
               | (IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__ev_tu_w));
        vlSelfRef.__Vdly__milan_datapath__DOT__talker_diag__DOT__seen_tu_r 
            = ((IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__seen_tu_r) 
               | (IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__ev_tu_w));
        vlSelfRef.__Vdly__milan_datapath__DOT__talker_diag__DOT__seen_tu_r 
            = ((IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__seen_tu_r) 
               | (IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__ev_tu_w));
        vlSelfRef.__Vdly__milan_datapath__DOT__talker_diag__DOT__seen_tu_r 
            = ((IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__seen_tu_r) 
               | (IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__ev_tu_w));
        vlSelfRef.__Vdly__milan_datapath__DOT__talker_diag__DOT__seen_mr_r 
            = ((IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__seen_mr_r) 
               | (IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__ev_mr_w));
        if (vlSelfRef.milan_datapath__DOT__talker_diag__DOT__tick_p_r) {
            if ((1U & ((IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__seen_f_r) 
                       | (IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__ev_f_w)))) {
                vlSelfRef.__VdlyVal__milan_datapath__DOT__talker_diag__DOT__ftx_r__v0 
                    = ((IData)(1U) + vlSelfRef.milan_datapath__DOT__talker_diag__DOT__ftx_r[0U]);
                vlSelfRef.__VdlySet__milan_datapath__DOT__talker_diag__DOT__ftx_r__v0 = 1U;
            }
            if ((1U & ((IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__seen_tu_r) 
                       | (IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__ev_tu_w)))) {
                vlSelfRef.__VdlyVal__milan_datapath__DOT__talker_diag__DOT__tuiv_r__v0 
                    = ((IData)(1U) + vlSelfRef.milan_datapath__DOT__talker_diag__DOT__tuiv_r[0U]);
                vlSelfRef.__VdlySet__milan_datapath__DOT__talker_diag__DOT__tuiv_r__v0 = 1U;
            }
            if ((1U & ((IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__seen_mr_r) 
                       | (IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__ev_mr_w)))) {
                vlSelfRef.__VdlyVal__milan_datapath__DOT__talker_diag__DOT__mreset_r__v0 
                    = ((IData)(1U) + vlSelfRef.milan_datapath__DOT__talker_diag__DOT__mreset_r[0U]);
                vlSelfRef.__VdlySet__milan_datapath__DOT__talker_diag__DOT__mreset_r__v0 = 1U;
            }
            if ((1U & ((((IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__seen_f_r) 
                         | (IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__ev_f_w)) 
                        | ((IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__seen_tu_r) 
                           | (IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__ev_tu_w))) 
                       | ((IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__seen_mr_r) 
                          | (IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__ev_mr_w))))) {
                vlSelfRef.milan_datapath__DOT__tkd_dirty_p_w 
                    = (1U | (IData)(vlSelfRef.milan_datapath__DOT__tkd_dirty_p_w));
            }
            if ((2U & ((IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__seen_f_r) 
                       | (IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__ev_f_w)))) {
                vlSelfRef.__VdlyVal__milan_datapath__DOT__talker_diag__DOT__ftx_r__v1 
                    = ((IData)(1U) + vlSelfRef.milan_datapath__DOT__talker_diag__DOT__ftx_r[1U]);
                vlSelfRef.__VdlySet__milan_datapath__DOT__talker_diag__DOT__ftx_r__v1 = 1U;
            }
            if ((2U & ((IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__seen_tu_r) 
                       | (IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__ev_tu_w)))) {
                vlSelfRef.__VdlyVal__milan_datapath__DOT__talker_diag__DOT__tuiv_r__v1 
                    = ((IData)(1U) + vlSelfRef.milan_datapath__DOT__talker_diag__DOT__tuiv_r[1U]);
                vlSelfRef.__VdlySet__milan_datapath__DOT__talker_diag__DOT__tuiv_r__v1 = 1U;
            }
            if ((2U & ((IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__seen_mr_r) 
                       | (IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__ev_mr_w)))) {
                vlSelfRef.__VdlyVal__milan_datapath__DOT__talker_diag__DOT__mreset_r__v1 
                    = ((IData)(1U) + vlSelfRef.milan_datapath__DOT__talker_diag__DOT__mreset_r[1U]);
                vlSelfRef.__VdlySet__milan_datapath__DOT__talker_diag__DOT__mreset_r__v1 = 1U;
            }
            if ((2U & ((((IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__seen_f_r) 
                         | (IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__ev_f_w)) 
                        | ((IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__seen_tu_r) 
                           | (IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__ev_tu_w))) 
                       | ((IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__seen_mr_r) 
                          | (IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__ev_mr_w))))) {
                vlSelfRef.milan_datapath__DOT__tkd_dirty_p_w 
                    = (2U | (IData)(vlSelfRef.milan_datapath__DOT__tkd_dirty_p_w));
            }
            if ((4U & ((IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__seen_f_r) 
                       | (IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__ev_f_w)))) {
                vlSelfRef.__VdlyVal__milan_datapath__DOT__talker_diag__DOT__ftx_r__v2 
                    = ((IData)(1U) + vlSelfRef.milan_datapath__DOT__talker_diag__DOT__ftx_r[2U]);
                vlSelfRef.__VdlySet__milan_datapath__DOT__talker_diag__DOT__ftx_r__v2 = 1U;
            }
            if ((4U & ((IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__seen_tu_r) 
                       | (IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__ev_tu_w)))) {
                vlSelfRef.__VdlyVal__milan_datapath__DOT__talker_diag__DOT__tuiv_r__v2 
                    = ((IData)(1U) + vlSelfRef.milan_datapath__DOT__talker_diag__DOT__tuiv_r[2U]);
                vlSelfRef.__VdlySet__milan_datapath__DOT__talker_diag__DOT__tuiv_r__v2 = 1U;
            }
            if ((4U & ((IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__seen_mr_r) 
                       | (IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__ev_mr_w)))) {
                vlSelfRef.__VdlyVal__milan_datapath__DOT__talker_diag__DOT__mreset_r__v2 
                    = ((IData)(1U) + vlSelfRef.milan_datapath__DOT__talker_diag__DOT__mreset_r[2U]);
                vlSelfRef.__VdlySet__milan_datapath__DOT__talker_diag__DOT__mreset_r__v2 = 1U;
            }
            if ((4U & ((((IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__seen_f_r) 
                         | (IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__ev_f_w)) 
                        | ((IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__seen_tu_r) 
                           | (IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__ev_tu_w))) 
                       | ((IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__seen_mr_r) 
                          | (IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__ev_mr_w))))) {
                vlSelfRef.milan_datapath__DOT__tkd_dirty_p_w 
                    = (4U | (IData)(vlSelfRef.milan_datapath__DOT__tkd_dirty_p_w));
            }
            if ((8U & ((IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__seen_f_r) 
                       | (IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__ev_f_w)))) {
                vlSelfRef.__VdlyVal__milan_datapath__DOT__talker_diag__DOT__ftx_r__v3 
                    = ((IData)(1U) + vlSelfRef.milan_datapath__DOT__talker_diag__DOT__ftx_r[3U]);
                vlSelfRef.__VdlySet__milan_datapath__DOT__talker_diag__DOT__ftx_r__v3 = 1U;
            }
            if ((8U & ((IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__seen_tu_r) 
                       | (IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__ev_tu_w)))) {
                vlSelfRef.__VdlyVal__milan_datapath__DOT__talker_diag__DOT__tuiv_r__v3 
                    = ((IData)(1U) + vlSelfRef.milan_datapath__DOT__talker_diag__DOT__tuiv_r[3U]);
                vlSelfRef.__VdlySet__milan_datapath__DOT__talker_diag__DOT__tuiv_r__v3 = 1U;
            }
            if ((8U & ((IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__seen_mr_r) 
                       | (IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__ev_mr_w)))) {
                vlSelfRef.__VdlyVal__milan_datapath__DOT__talker_diag__DOT__mreset_r__v3 
                    = ((IData)(1U) + vlSelfRef.milan_datapath__DOT__talker_diag__DOT__mreset_r[3U]);
                vlSelfRef.__VdlySet__milan_datapath__DOT__talker_diag__DOT__mreset_r__v3 = 1U;
            }
            if ((8U & ((((IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__seen_f_r) 
                         | (IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__ev_f_w)) 
                        | ((IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__seen_tu_r) 
                           | (IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__ev_tu_w))) 
                       | ((IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__seen_mr_r) 
                          | (IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__ev_mr_w))))) {
                vlSelfRef.milan_datapath__DOT__tkd_dirty_p_w 
                    = (8U | (IData)(vlSelfRef.milan_datapath__DOT__tkd_dirty_p_w));
            }
            if ((0x00000010U & ((IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__seen_f_r) 
                                | (IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__ev_f_w)))) {
                vlSelfRef.__VdlyVal__milan_datapath__DOT__talker_diag__DOT__ftx_r__v4 
                    = ((IData)(1U) + vlSelfRef.milan_datapath__DOT__talker_diag__DOT__ftx_r[4U]);
                vlSelfRef.__VdlySet__milan_datapath__DOT__talker_diag__DOT__ftx_r__v4 = 1U;
            }
            if ((0x00000010U & ((IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__seen_tu_r) 
                                | (IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__ev_tu_w)))) {
                vlSelfRef.__VdlyVal__milan_datapath__DOT__talker_diag__DOT__tuiv_r__v4 
                    = ((IData)(1U) + vlSelfRef.milan_datapath__DOT__talker_diag__DOT__tuiv_r[4U]);
                vlSelfRef.__VdlySet__milan_datapath__DOT__talker_diag__DOT__tuiv_r__v4 = 1U;
            }
            if ((0x00000010U & ((IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__seen_mr_r) 
                                | (IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__ev_mr_w)))) {
                vlSelfRef.__VdlyVal__milan_datapath__DOT__talker_diag__DOT__mreset_r__v4 
                    = ((IData)(1U) + vlSelfRef.milan_datapath__DOT__talker_diag__DOT__mreset_r[4U]);
                vlSelfRef.__VdlySet__milan_datapath__DOT__talker_diag__DOT__mreset_r__v4 = 1U;
            }
            if ((0x00000010U & ((((IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__seen_f_r) 
                                  | (IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__ev_f_w)) 
                                 | ((IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__seen_tu_r) 
                                    | (IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__ev_tu_w))) 
                                | ((IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__seen_mr_r) 
                                   | (IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__ev_mr_w))))) {
                vlSelfRef.milan_datapath__DOT__tkd_dirty_p_w 
                    = (0x00000010U | (IData)(vlSelfRef.milan_datapath__DOT__tkd_dirty_p_w));
            }
            vlSelfRef.__Vdly__milan_datapath__DOT__talker_diag__DOT__seen_f_r = 0U;
            vlSelfRef.__Vdly__milan_datapath__DOT__talker_diag__DOT__seen_tu_r = 0U;
            vlSelfRef.__Vdly__milan_datapath__DOT__talker_diag__DOT__seen_mr_r = 0U;
        }
        if ((1U & ((IData)(vlSelfRef.milan_datapath__DOT__tkd_streaming_w) 
                   & (~ (IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__strm_q_r))))) {
            vlSelfRef.__VdlyVal__milan_datapath__DOT__talker_diag__DOT__start_r__v0 
                = ((IData)(1U) + vlSelfRef.milan_datapath__DOT__talker_diag__DOT__start_r[0U]);
            vlSelfRef.__VdlySet__milan_datapath__DOT__talker_diag__DOT__start_r__v0 = 1U;
            vlSelfRef.__Vdly__milan_datapath__DOT__talker_diag__DOT__seen_f_r 
                = ((0x1eU & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__talker_diag__DOT__seen_f_r)) 
                   | (1U & (IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__ev_f_w)));
            vlSelfRef.__Vdly__milan_datapath__DOT__talker_diag__DOT__seen_tu_r 
                = ((0x1eU & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__talker_diag__DOT__seen_tu_r)) 
                   | (1U & (IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__ev_tu_w)));
            vlSelfRef.__Vdly__milan_datapath__DOT__talker_diag__DOT__seen_mr_r 
                = ((0x1eU & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__talker_diag__DOT__seen_mr_r)) 
                   | (1U & (IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__ev_mr_w)));
            vlSelfRef.milan_datapath__DOT__tkd_dirty_p_w 
                = (1U | (IData)(vlSelfRef.milan_datapath__DOT__tkd_dirty_p_w));
        } else if ((1U & ((~ (IData)(vlSelfRef.milan_datapath__DOT__tkd_streaming_w)) 
                          & (IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__strm_q_r)))) {
            vlSelfRef.__VdlyVal__milan_datapath__DOT__talker_diag__DOT__stop_r__v0 
                = ((IData)(1U) + vlSelfRef.milan_datapath__DOT__talker_diag__DOT__stop_r[0U]);
            vlSelfRef.__VdlySet__milan_datapath__DOT__talker_diag__DOT__stop_r__v0 = 1U;
            vlSelfRef.milan_datapath__DOT__tkd_dirty_p_w 
                = (1U | (IData)(vlSelfRef.milan_datapath__DOT__tkd_dirty_p_w));
        }
        if ((1U & (((IData)(vlSelfRef.milan_datapath__DOT__tkd_streaming_w) 
                    >> 1U) & (~ ((IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__strm_q_r) 
                                 >> 1U))))) {
            vlSelfRef.__VdlyVal__milan_datapath__DOT__talker_diag__DOT__start_r__v1 
                = ((IData)(1U) + vlSelfRef.milan_datapath__DOT__talker_diag__DOT__start_r[1U]);
            vlSelfRef.__VdlySet__milan_datapath__DOT__talker_diag__DOT__start_r__v1 = 1U;
            vlSelfRef.__Vdly__milan_datapath__DOT__talker_diag__DOT__seen_f_r 
                = ((0x1dU & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__talker_diag__DOT__seen_f_r)) 
                   | (2U & (IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__ev_f_w)));
            vlSelfRef.__Vdly__milan_datapath__DOT__talker_diag__DOT__seen_tu_r 
                = ((0x1dU & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__talker_diag__DOT__seen_tu_r)) 
                   | (2U & (IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__ev_tu_w)));
            vlSelfRef.__Vdly__milan_datapath__DOT__talker_diag__DOT__seen_mr_r 
                = ((0x1dU & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__talker_diag__DOT__seen_mr_r)) 
                   | (2U & (IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__ev_mr_w)));
            vlSelfRef.milan_datapath__DOT__tkd_dirty_p_w 
                = (2U | (IData)(vlSelfRef.milan_datapath__DOT__tkd_dirty_p_w));
        } else if ((1U & ((~ ((IData)(vlSelfRef.milan_datapath__DOT__tkd_streaming_w) 
                              >> 1U)) & ((IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__strm_q_r) 
                                         >> 1U)))) {
            vlSelfRef.__VdlyVal__milan_datapath__DOT__talker_diag__DOT__stop_r__v1 
                = ((IData)(1U) + vlSelfRef.milan_datapath__DOT__talker_diag__DOT__stop_r[1U]);
            vlSelfRef.__VdlySet__milan_datapath__DOT__talker_diag__DOT__stop_r__v1 = 1U;
            vlSelfRef.milan_datapath__DOT__tkd_dirty_p_w 
                = (2U | (IData)(vlSelfRef.milan_datapath__DOT__tkd_dirty_p_w));
        }
        if ((1U & (((IData)(vlSelfRef.milan_datapath__DOT__tkd_streaming_w) 
                    >> 2U) & (~ ((IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__strm_q_r) 
                                 >> 2U))))) {
            vlSelfRef.__VdlyVal__milan_datapath__DOT__talker_diag__DOT__start_r__v2 
                = ((IData)(1U) + vlSelfRef.milan_datapath__DOT__talker_diag__DOT__start_r[2U]);
            vlSelfRef.__VdlySet__milan_datapath__DOT__talker_diag__DOT__start_r__v2 = 1U;
            vlSelfRef.__Vdly__milan_datapath__DOT__talker_diag__DOT__seen_f_r 
                = ((0x1bU & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__talker_diag__DOT__seen_f_r)) 
                   | (4U & (IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__ev_f_w)));
            vlSelfRef.__Vdly__milan_datapath__DOT__talker_diag__DOT__seen_tu_r 
                = ((0x1bU & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__talker_diag__DOT__seen_tu_r)) 
                   | (4U & (IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__ev_tu_w)));
            vlSelfRef.__Vdly__milan_datapath__DOT__talker_diag__DOT__seen_mr_r 
                = ((0x1bU & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__talker_diag__DOT__seen_mr_r)) 
                   | (4U & (IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__ev_mr_w)));
            vlSelfRef.milan_datapath__DOT__tkd_dirty_p_w 
                = (4U | (IData)(vlSelfRef.milan_datapath__DOT__tkd_dirty_p_w));
        } else if ((1U & ((~ ((IData)(vlSelfRef.milan_datapath__DOT__tkd_streaming_w) 
                              >> 2U)) & ((IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__strm_q_r) 
                                         >> 2U)))) {
            vlSelfRef.__VdlyVal__milan_datapath__DOT__talker_diag__DOT__stop_r__v2 
                = ((IData)(1U) + vlSelfRef.milan_datapath__DOT__talker_diag__DOT__stop_r[2U]);
            vlSelfRef.__VdlySet__milan_datapath__DOT__talker_diag__DOT__stop_r__v2 = 1U;
            vlSelfRef.milan_datapath__DOT__tkd_dirty_p_w 
                = (4U | (IData)(vlSelfRef.milan_datapath__DOT__tkd_dirty_p_w));
        }
        if ((1U & (((IData)(vlSelfRef.milan_datapath__DOT__tkd_streaming_w) 
                    >> 3U) & (~ ((IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__strm_q_r) 
                                 >> 3U))))) {
            vlSelfRef.__VdlyVal__milan_datapath__DOT__talker_diag__DOT__start_r__v3 
                = ((IData)(1U) + vlSelfRef.milan_datapath__DOT__talker_diag__DOT__start_r[3U]);
            vlSelfRef.__VdlySet__milan_datapath__DOT__talker_diag__DOT__start_r__v3 = 1U;
            vlSelfRef.__Vdly__milan_datapath__DOT__talker_diag__DOT__seen_f_r 
                = ((0x17U & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__talker_diag__DOT__seen_f_r)) 
                   | (8U & (IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__ev_f_w)));
            vlSelfRef.__Vdly__milan_datapath__DOT__talker_diag__DOT__seen_tu_r 
                = ((0x17U & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__talker_diag__DOT__seen_tu_r)) 
                   | (8U & (IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__ev_tu_w)));
            vlSelfRef.__Vdly__milan_datapath__DOT__talker_diag__DOT__seen_mr_r 
                = ((0x17U & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__talker_diag__DOT__seen_mr_r)) 
                   | (8U & (IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__ev_mr_w)));
            vlSelfRef.milan_datapath__DOT__tkd_dirty_p_w 
                = (8U | (IData)(vlSelfRef.milan_datapath__DOT__tkd_dirty_p_w));
        } else if ((1U & ((~ ((IData)(vlSelfRef.milan_datapath__DOT__tkd_streaming_w) 
                              >> 3U)) & ((IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__strm_q_r) 
                                         >> 3U)))) {
            vlSelfRef.__VdlyVal__milan_datapath__DOT__talker_diag__DOT__stop_r__v3 
                = ((IData)(1U) + vlSelfRef.milan_datapath__DOT__talker_diag__DOT__stop_r[3U]);
            vlSelfRef.__VdlySet__milan_datapath__DOT__talker_diag__DOT__stop_r__v3 = 1U;
            vlSelfRef.milan_datapath__DOT__tkd_dirty_p_w 
                = (8U | (IData)(vlSelfRef.milan_datapath__DOT__tkd_dirty_p_w));
        }
        if ((IData)((((IData)(vlSelfRef.milan_datapath__DOT__tkd_streaming_w) 
                      >> 4U) & (~ ((IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__strm_q_r) 
                                   >> 4U))))) {
            vlSelfRef.__VdlyVal__milan_datapath__DOT__talker_diag__DOT__start_r__v4 
                = ((IData)(1U) + vlSelfRef.milan_datapath__DOT__talker_diag__DOT__start_r[4U]);
            vlSelfRef.__VdlySet__milan_datapath__DOT__talker_diag__DOT__start_r__v4 = 1U;
            vlSelfRef.__Vdly__milan_datapath__DOT__talker_diag__DOT__seen_f_r 
                = ((0x0fU & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__talker_diag__DOT__seen_f_r)) 
                   | (0x00000010U & (IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__ev_f_w)));
            vlSelfRef.__Vdly__milan_datapath__DOT__talker_diag__DOT__seen_tu_r 
                = ((0x0fU & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__talker_diag__DOT__seen_tu_r)) 
                   | (0x00000010U & (IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__ev_tu_w)));
            vlSelfRef.__Vdly__milan_datapath__DOT__talker_diag__DOT__seen_mr_r 
                = ((0x0fU & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__talker_diag__DOT__seen_mr_r)) 
                   | (0x00000010U & (IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__ev_mr_w)));
            vlSelfRef.milan_datapath__DOT__tkd_dirty_p_w 
                = (0x00000010U | (IData)(vlSelfRef.milan_datapath__DOT__tkd_dirty_p_w));
        } else if ((IData)(((~ ((IData)(vlSelfRef.milan_datapath__DOT__tkd_streaming_w) 
                                >> 4U)) & ((IData)(vlSelfRef.milan_datapath__DOT__talker_diag__DOT__strm_q_r) 
                                           >> 4U)))) {
            vlSelfRef.__VdlyVal__milan_datapath__DOT__talker_diag__DOT__stop_r__v4 
                = ((IData)(1U) + vlSelfRef.milan_datapath__DOT__talker_diag__DOT__stop_r[4U]);
            vlSelfRef.__VdlySet__milan_datapath__DOT__talker_diag__DOT__stop_r__v4 = 1U;
            vlSelfRef.milan_datapath__DOT__tkd_dirty_p_w 
                = (0x00000010U | (IData)(vlSelfRef.milan_datapath__DOT__tkd_dirty_p_w));
        }
        if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__reg_we_w) {
            if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_nvm_csr_addr_w) 
                          >> 4U)))) {
                if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_nvm_csr_addr_w) 
                              >> 3U)))) {
                    if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_nvm_csr_addr_w) 
                                  >> 2U)))) {
                        if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__pp_nvm_csr_addr_w))) {
                            if ((1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_nvm_csr_addr_w)))) {
                                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__seq_r 
                                    = vlSelfRef.milan_datapath__DOT__csr__DOT__g_pp_csr__DOT__pp_nvm_wdata_r;
                            }
                            if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_nvm_csr_addr_w))) {
                                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__verdict_r 
                                    = (0x0000000fU 
                                       & vlSelfRef.milan_datapath__DOT__csr__DOT__g_pp_csr__DOT__pp_nvm_wdata_r);
                            }
                        }
                    }
                }
            }
        }
        if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__p_periodic_r) 
              & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_grant_w))) 
             & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w)) 
                | (0x0aU != (0x0000000fU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w))))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_pend_r 
                = (1U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_pend_r));
        } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_grant_w))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_pend_r 
                = (0x1eU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_pend_r));
        }
        if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__p_periodic_r) 
              & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_grant_w) 
                    >> 1U))) & ((~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w) 
                                    >> 1U)) | (0x0aU 
                                               != (0x0000000fU 
                                                   & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w 
                                                      >> 4U)))))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_pend_r 
                = (2U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_pend_r));
        } else if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_grant_w))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_pend_r 
                = (0x1dU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_pend_r));
        }
        if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__p_periodic_r) 
              & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_grant_w) 
                    >> 2U))) & ((~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w) 
                                    >> 2U)) | (0x0aU 
                                               != (0x0000000fU 
                                                   & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w 
                                                      >> 8U)))))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_pend_r 
                = (4U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_pend_r));
        } else if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_grant_w))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_pend_r 
                = (0x1bU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_pend_r));
        }
        if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__p_periodic_r) 
              & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_grant_w) 
                    >> 3U))) & ((~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w) 
                                    >> 3U)) | (0x0aU 
                                               != (0x0000000fU 
                                                   & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w 
                                                      >> 0x0cU)))))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_pend_r 
                = (8U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_pend_r));
        } else if ((8U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_grant_w))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_pend_r 
                = (0x17U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_pend_r));
        }
        if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__p_periodic_r) 
              & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_grant_w) 
                    >> 4U))) & ((~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w) 
                                    >> 4U)) | (0x0aU 
                                               != (0x0000000fU 
                                                   & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w 
                                                      >> 0x10U)))))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_pend_r 
                = (0x00000010U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_pend_r));
        } else if ((0x00000010U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_grant_w))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_pend_r 
                = (0x0fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_pend_r));
        }
        if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__exp_fire_w) 
              & (0x000000c000000000ULL == (0x000000f000000000ULL 
                                           & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__sweep_rdata_r))) 
             & (((4U > (0x0000000fU & (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__sweep_rdata_r 
                                               >> 0x00000020U)))) 
                 & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__valid_r) 
                    >> (0x0000000fU & (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__sweep_rdata_r 
                                               >> 0x00000020U))))) 
                & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__chk_slot_r) 
                   == vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__tslot_r
                   [(0x0000000fU & (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__sweep_rdata_r 
                                            >> 0x00000020U)))])))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__exp_pend_r 
                = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__exp_pend_r) 
                   | (0x0000ffffU & ((IData)(1U) << 
                                     (0x0000000fU & (IData)(
                                                            (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__sweep_rdata_r 
                                                             >> 0x00000020U))))));
        }
        if ((1U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__bound_fall_w) 
                   & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__disc_st_r)))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__ucancel_pend_r 
                = (1U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__ucancel_pend_r));
        }
        if ((2U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__bound_fall_w) 
                   & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__disc_st_r)))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__ucancel_pend_r 
                = (2U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__ucancel_pend_r));
        }
        if ((4U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__bound_fall_w) 
                   & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__disc_st_r)))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__ucancel_pend_r 
                = (4U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__ucancel_pend_r));
        }
        if ((8U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__bound_fall_w) 
                   & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__disc_st_r)))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__ucancel_pend_r 
                = (8U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__ucancel_pend_r));
        }
        if ((0x00000010U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__bound_fall_w) 
                            & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__disc_st_r)))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__ucancel_pend_r 
                = (0x00000010U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__ucancel_pend_r));
        }
        if (((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__iter_port_w)) 
             & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__ucancel_issue_w))) {
            if ((4U >= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__ucancel_sink_w))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__ucancel_pend_r 
                    = ((~ ((IData)(1U) << (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__ucancel_sink_w))) 
                       & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__ucancel_pend_r));
            }
        }
        if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__p_periodic_r) 
              & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__per_grant_w))) 
             & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_ev_v_w)) 
                | (0x0aU != (0x0000000fU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_ev_w))))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__per_pend_r 
                = (1U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__per_pend_r));
        } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__per_grant_w))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__per_pend_r 
                = (0x1eU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__per_pend_r));
        }
        if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__p_periodic_r) 
              & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__per_grant_w) 
                    >> 1U))) & ((~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_ev_v_w) 
                                    >> 1U)) | (0x0aU 
                                               != (0x0000000fU 
                                                   & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_ev_w 
                                                      >> 4U)))))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__per_pend_r 
                = (2U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__per_pend_r));
        } else if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__per_grant_w))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__per_pend_r 
                = (0x1dU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__per_pend_r));
        }
        if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__p_periodic_r) 
              & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__per_grant_w) 
                    >> 2U))) & ((~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_ev_v_w) 
                                    >> 2U)) | (0x0aU 
                                               != (0x0000000fU 
                                                   & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_ev_w 
                                                      >> 8U)))))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__per_pend_r 
                = (4U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__per_pend_r));
        } else if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__per_grant_w))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__per_pend_r 
                = (0x1bU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__per_pend_r));
        }
        if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__p_periodic_r) 
              & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__per_grant_w) 
                    >> 3U))) & ((~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_ev_v_w) 
                                    >> 3U)) | (0x0aU 
                                               != (0x0000000fU 
                                                   & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_ev_w 
                                                      >> 0x0cU)))))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__per_pend_r 
                = (8U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__per_pend_r));
        } else if ((8U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__per_grant_w))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__per_pend_r 
                = (0x17U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__per_pend_r));
        }
        if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__p_periodic_r) 
              & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__per_grant_w) 
                    >> 4U))) & ((~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_ev_v_w) 
                                    >> 4U)) | (0x0aU 
                                               != (0x0000000fU 
                                                   & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_ev_w 
                                                      >> 0x10U)))))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__per_pend_r 
                = (0x00000010U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__per_pend_r));
        } else if ((0x00000010U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__per_grant_w))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__per_pend_r 
                = (0x0fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__per_pend_r));
        }
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_arm_valid_w = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_draw_req_w = 0U;
        vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tf_cnt_r__v0 
            = (0x0000003fU & (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tf_cnt_r[0U]) 
                               + (1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tf_push_w))) 
                              - (1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tf_pop_w))));
        vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tf_cnt_r__v0 = 1U;
        vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tf_cnt_r__v1 
            = (0x0000003fU & (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tf_cnt_r[1U]) 
                               + (1U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tf_push_w) 
                                        >> 1U))) - 
                              (1U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tf_pop_w) 
                                     >> 1U))));
        if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tm_st_r) {
            vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tf_rptr_r__v0 
                = (0x0000001fU & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tf_rptr_r
                                                        [vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tm_sel_r])));
            vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tf_rptr_r__v0 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tm_sel_r;
            vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tf_rptr_r__v0 = 1U;
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tm_rr_r 
                = (1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tm_rr_r)));
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_arm_valid_w = 1U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_arm_cancel_w 
                = (1U & (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tf_q_r
                                 [vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tm_sel_r] 
                                 >> 0x0000002fU)));
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_arm_slot_w 
                = (0x0000007fU & (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tf_q_r
                                          [vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tm_sel_r] 
                                          >> 0x00000028U)));
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_arm_owner_w 
                = (0x000000ffU & (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tf_q_r
                                          [vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tm_sel_r] 
                                          >> 0x00000020U)));
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_arm_deadline_w 
                = (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tf_q_r
                          [vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tm_sel_r]);
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tm_st_r = 0U;
        } else if (((0U != vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tf_cnt_r[0U]) 
                    & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tm_rr_r)) 
                       | (0U == vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tf_cnt_r[1U])))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tm_sel_r = 0U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tm_st_r = 1U;
        } else if ((0U != vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tf_cnt_r[1U])) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tm_sel_r = 1U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tm_st_r = 1U;
        } else if ((0U != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__cad_pend_r))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_arm_valid_w = 1U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_arm_cancel_w = 0U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_arm_slot_w 
                = (0x0000007fU & ((IData)(0x3bU) + Vmilan_datapath__ConstPool__TABLE_h6dff1152_0
                                  [vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__cad_pend_r]));
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_arm_owner_w 
                = (0x000000ffU & ((IData)(0x80U) + Vmilan_datapath__ConstPool__TABLE_h6dff1152_0
                                  [vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__cad_pend_r]));
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_arm_deadline_w 
                = ((0x9fU >= (0x000000ffU & (Vmilan_datapath__ConstPool__TABLE_h6dff1152_0
                                             [vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__cad_pend_r] 
                                             << 5U)))
                    ? vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__cad_dl_r
                   [(7U & Vmilan_datapath__ConstPool__TABLE_h6dff1152_0
                     [vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__cad_pend_r])]
                    : 0U);
            if ((4U >= Vmilan_datapath__ConstPool__TABLE_h6dff1152_0
                 [vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__cad_pend_r])) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__cad_pend_r 
                    = ((~ ((IData)(1U) << Vmilan_datapath__ConstPool__TABLE_h6dff1152_0
                           [vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__cad_pend_r])) 
                       & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__cad_pend_r));
            }
        }
        if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dr_inflight_r) {
            if (((3U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pr_owner_r)) 
                 & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_11))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dr_inflight_r = 0U;
                if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dr_app_r) {
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__cad_pend_r 
                        = (0x00000010U | (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__cad_pend_r));
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__cad_dl_r[4U] 
                        = (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__now_ms_r 
                           + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__prng_ms_w));
                } else {
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__cad_pend_r 
                        = (8U | (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__cad_pend_r));
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__cad_dl_r[3U] 
                        = (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__now_ms_r 
                           + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__prng_ms_w));
                }
            }
        } else if (((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__adp_prng_busy_w)) 
                    & (0U != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__need_draw_r)))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_draw_req_w = 1U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dr_inflight_r = 1U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dr_app_r 
                = (1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__need_draw_r)));
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__need_draw_r 
                = ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__need_draw_r))
                    ? (2U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__need_draw_r))
                    : (1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__need_draw_r)));
        }
        if ((1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__init_done_r)))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__cad_pend_r 
                = (1U | (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__cad_pend_r));
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__need_draw_r = 3U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__init_done_r = 1U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__cad_dl_r[0U] 
                = ((IData)(0x000000c8U) + vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__now_ms_r);
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__cad_pend_r 
                = (2U | (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__cad_pend_r));
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__cad_dl_r[1U] 
                = ((IData)(0x000000c8U) + vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__now_ms_r);
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__cad_pend_r 
                = (4U | (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__cad_pend_r));
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__cad_dl_r[2U] 
                = ((IData)(0x000003e8U) + vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__now_ms_r);
        }
        if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__cad_hit_w) {
            if ((4U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__chk_slot_r) 
                       - (IData)(0x0000003bU)))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__need_draw_r 
                    = (2U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__need_draw_r));
            } else if ((2U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__chk_slot_r) 
                              - (IData)(0x0000003bU)))) {
                if ((1U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__chk_slot_r) 
                           - (IData)(1U)))) {
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__need_draw_r 
                        = (1U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__need_draw_r));
                } else {
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__cad_pend_r 
                        = (4U | (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__cad_pend_r));
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__cad_dl_r[2U] 
                        = ((IData)(0x000003e8U) + vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__now_ms_r);
                }
            } else if ((1U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__chk_slot_r) 
                              - (IData)(1U)))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__cad_pend_r 
                    = (2U | (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__cad_pend_r));
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__cad_dl_r[1U] 
                    = ((IData)(0x000000c8U) + vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__now_ms_r);
            } else {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__cad_pend_r 
                    = (1U | (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__cad_pend_r));
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__cad_dl_r[0U] 
                    = ((IData)(0x000000c8U) + vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__now_ms_r);
            }
        }
        if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__gnt_r) 
              >> 7U) & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__accept_hit_w))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__accept_pend_r 
                = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__accept_pend_r) 
                   | (0x0000ffffU & ((IData)(1U) << (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__accept_ix_w))));
        }
        if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__ev_rsp_w) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__org_arm_valid_w = 1U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__org_arm_cancel_w = 1U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__org_arm_owner_w 
                = (0x000000c0U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__hit_ix_w));
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__org_arm_slot_w 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__tslot_r
                [vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__hit_ix_w];
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__org_arm_deadline_w = 0U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__org_release_valid_w = 1U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__cancel_pend_r 
                = ((~ ((IData)(1U) << (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__hit_ix_w))) 
                   & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__cancel_pend_r));
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__org_release_slot_w 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__txs_r
                [vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__hit_ix_w];
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__exp_pend_r 
                = ((~ ((IData)(1U) << (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__hit_ix_w))) 
                   & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__exp_pend_r));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__valid_r 
                = ((~ ((IData)(1U) << (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__hit_ix_w))) 
                   & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__valid_r));
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__await_tx_r 
                = ((~ ((IData)(1U) << (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__hit_ix_w))) 
                   & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__await_tx_r));
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__accept_pend_r 
                = ((~ ((IData)(1U) << (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__hit_ix_w))) 
                   & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__accept_pend_r));
        } else if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__ev_cancel_w) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__org_arm_valid_w = 1U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__org_arm_cancel_w = 1U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__org_arm_owner_w 
                = (0x000000c0U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__cancel_pend_ix_w));
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__org_arm_slot_w 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__tslot_r
                [vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__cancel_pend_ix_w];
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__org_arm_deadline_w = 0U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__org_release_valid_w = 1U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__cancel_pend_r 
                = ((~ ((IData)(1U) << (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__cancel_pend_ix_w))) 
                   & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__cancel_pend_r));
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__org_release_slot_w 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__txs_r
                [vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__cancel_pend_ix_w];
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__exp_pend_r 
                = ((~ ((IData)(1U) << (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__cancel_pend_ix_w))) 
                   & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__exp_pend_r));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__valid_r 
                = ((~ ((IData)(1U) << (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__cancel_pend_ix_w))) 
                   & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__valid_r));
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__await_tx_r 
                = ((~ ((IData)(1U) << (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__cancel_pend_ix_w))) 
                   & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__await_tx_r));
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__accept_pend_r 
                = ((~ ((IData)(1U) << (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__cancel_pend_ix_w))) 
                   & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__accept_pend_r));
        } else {
            if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__ev_accept_w) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__org_arm_valid_w = 1U;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__org_arm_cancel_w = 0U;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__org_arm_owner_w 
                    = (0x000000c0U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__accept_pend_ix_w));
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__org_arm_slot_w 
                    = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__tslot_r
                    [vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__accept_pend_ix_w];
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__org_arm_deadline_w 
                    = (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__now_ms_r 
                       + vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__tout_r
                       [vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__accept_pend_ix_w]);
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__await_tx_r 
                    = ((~ ((IData)(1U) << (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__accept_pend_ix_w))) 
                       & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__await_tx_r));
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__accept_pend_r 
                    = ((~ ((IData)(1U) << (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__accept_pend_ix_w))) 
                       & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__accept_pend_r));
            } else if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__ev_exp_w) {
                if ((1U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__valid_r) 
                           >> (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__pend_ix_w)))) {
                    if ((1U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__retried_r) 
                               >> (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__pend_ix_w)))) {
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__valid_r 
                            = ((~ ((IData)(1U) << (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__pend_ix_w))) 
                               & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__valid_r));
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__await_tx_r 
                            = ((~ ((IData)(1U) << (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__pend_ix_w))) 
                               & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__await_tx_r));
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__accept_pend_r 
                            = ((~ ((IData)(1U) << (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__pend_ix_w))) 
                               & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__accept_pend_r));
                    } else {
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__retried_r 
                            = ((IData)(vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__retried_r) 
                               | (0x0000ffffU & ((IData)(1U) 
                                                 << (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__pend_ix_w))));
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__await_tx_r 
                            = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__await_tx_r) 
                               | (0x0000ffffU & ((IData)(1U) 
                                                 << (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__pend_ix_w))));
                    }
                }
            } else if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__ev_iss_w) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__valid_r 
                    = ((IData)(vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__valid_r) 
                       | (0x0000ffffU & ((IData)(1U) 
                                         << (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__free_ix_w))));
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__retried_r 
                    = ((~ ((IData)(1U) << (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__free_ix_w))) 
                       & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__retried_r));
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__await_tx_r 
                    = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__await_tx_r) 
                       | (0x0000ffffU & ((IData)(1U) 
                                         << (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__free_ix_w))));
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__accept_pend_r 
                    = ((~ ((IData)(1U) << (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__free_ix_w))) 
                       & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__accept_pend_r));
            }
            if ((1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__ev_accept_w)))) {
                if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__ev_exp_w) {
                    if ((1U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__valid_r) 
                               >> (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__pend_ix_w)))) {
                        if ((1U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__retried_r) 
                                   >> (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__pend_ix_w)))) {
                            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__org_release_valid_w = 1U;
                            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__org_release_slot_w 
                                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__txs_r
                                [vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__pend_ix_w];
                        }
                    }
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__exp_pend_r 
                        = ((~ ((IData)(1U) << (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__pend_ix_w))) 
                           & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__exp_pend_r));
                } else if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__ev_iss_w) {
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__exp_pend_r 
                        = ((~ ((IData)(1U) << (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__free_ix_w))) 
                           & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__exp_pend_r));
                }
            }
        }
        if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__exp_fire_w) {
            if ((0x4bU >= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__chk_slot_r))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__armed_r[((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__chk_slot_r) 
                                                                                >> 5U)] 
                    = ((~ ((IData)(1U) << (0x0000001fU 
                                           & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__chk_slot_r)))) 
                       & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__armed_r
                       [((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__chk_slot_r) 
                         >> 5U)]);
            }
        }
        if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tmr_arm_valid_w) {
            if ((0x4bU >= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tmr_arm_slot_w))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__armed_r[((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tmr_arm_slot_w) 
                                                                                >> 5U)] 
                    = (((~ ((IData)(1U) << (0x0000001fU 
                                            & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tmr_arm_slot_w)))) 
                        & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__armed_r
                        [((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tmr_arm_slot_w) 
                          >> 5U)]) | ((1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tmr_arm_cancel_w))) 
                                      << (0x0000001fU 
                                          & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tmr_arm_slot_w))));
            }
        }
        if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__noadp_exp_w) 
             & ((4U >= (7U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__chk_slot_r) 
                              - (IData)(1U)))) && (1U 
                                                   & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__disc_st_r) 
                                                      >> 
                                                      (7U 
                                                       & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__chk_slot_r) 
                                                          - (IData)(1U)))))))) {
            if ((4U >= (7U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__chk_slot_r) 
                              - (IData)(1U))))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__pend_dep_evt_r 
                    = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__pend_dep_evt_r) 
                       | (0x1fU & ((IData)(1U) << (7U 
                                                   & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__chk_slot_r) 
                                                      - (IData)(1U))))));
            }
        }
        if ((1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__iter_evt_w)))) {
            if ((5U != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__rx_st_r))) {
                if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__drain_any_w) {
                    if ((4U >= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__drain_sink_w))) {
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__pend_dep_evt_r 
                            = ((~ ((IData)(1U) << (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__drain_sink_w))) 
                               & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__pend_dep_evt_r));
                    }
                }
            }
        }
        if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__reload_ok_w) 
             | ((~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__ld_ok_r) 
                    | (0U == vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__img_len_r))) 
                & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__gnt_now_w)))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__ld_pend_r = 0U;
        }
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
                                      & (- (IData)((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_79)))));
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
                       & (- (QData)((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_79))));
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_tkeid_r 
                    = (vlSelfRef.milan_datapath__DOT__cfg_adp_entity_id 
                       & (- (QData)((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_79))));
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_lseid_r 
                    = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_resp_lseid_w;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_tkuid_r 
                    = (0x0000ffffU & (((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__txn_r[2U] 
                                        << 4U) | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__txn_r[1U] 
                                                  >> 0x0000001cU)) 
                                      & (- (IData)((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_79)))));
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_lsuid_r 
                    = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_resp_lsuid_w;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_cc_r = 0U;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_seq_r 
                    = (0x0000ffffU & (((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__txn_r[4U] 
                                        << 0x00000012U) 
                                       | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__txn_r[4U] 
                                          >> 0x0000000eU)) 
                                      & (- (IData)((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_79)))));
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
                         & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_11))) {
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
                    __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__inc16__146__v 
                        = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__timeouts_r;
                    __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__inc16__146__Vfuncout 
                        = (0x0000ffffU & ((0x0000ffffU 
                                           == (IData)(__Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__inc16__146__v))
                                           ? (IData)(__Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__inc16__146__v)
                                           : ((IData)(1U) 
                                              + (IData)(__Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__inc16__146__v))));
                    vlSelfRef.__Vdly__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__active_r = 0U;
                    vlSelfRef.__Vdly__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__timeouts_r 
                        = __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__inc16__146__Vfuncout;
                } else {
                    vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__to_r 
                        = (0x0000ffffU & ((IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__to_r) 
                                          - (IData)(1U)));
                    if ((0U != (IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__nadv_w))) {
                        if (((0U >= (IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__didx_w)) 
                             & (0U < ((IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__didx_w) 
                                      + (IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__nadv_w))))) {
                            __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__147__meas 
                                = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__dsat_w;
                            __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__148__meas 
                                = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__dsat_w;
                            __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__150__meas 
                                = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__dsat_w;
                            __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__147__didx 
                                = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__didx_w;
                            __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__148__didx 
                                = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__didx_w;
                            __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__150__didx 
                                = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__didx_w;
                            vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT____VlemCall_0__hopd 
                                = ((0U == __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__147__didx)
                                    ? (IData)(__Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__147__meas)
                                    : 0U);
                            vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT____VlemCall_1__hopd 
                                = ((0U == __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__148__didx)
                                    ? (IData)(__Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__148__meas)
                                    : 0U);
                            vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT____VlemCall_3__hopd 
                                = ((0U == __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__150__didx)
                                    ? (IData)(__Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__150__meas)
                                    : 0U);
                            vlSelfRef.__VdlyVal__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__last_r__v3 
                                = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT____VlemCall_0__hopd;
                            vlSelfRef.__VdlySet__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__last_r__v3 = 1U;
                            if (((IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT____VlemCall_1__hopd) 
                                 < vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__min_r[0U])) {
                                __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__149__meas 
                                    = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__dsat_w;
                                __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__149__didx 
                                    = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__didx_w;
                                vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT____VlemCall_2__hopd 
                                    = ((0U == __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__149__didx)
                                        ? (IData)(__Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__149__meas)
                                        : 0U);
                                vlSelfRef.__VdlyVal__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__min_r__v3 
                                    = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT____VlemCall_2__hopd;
                                vlSelfRef.__VdlySet__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__min_r__v3 = 1U;
                            }
                            if (((IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT____VlemCall_3__hopd) 
                                 > vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__max_r[0U])) {
                                __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__151__meas 
                                    = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__dsat_w;
                                __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__151__didx 
                                    = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__didx_w;
                                vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT____VlemCall_4__hopd 
                                    = ((0U == __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__151__didx)
                                        ? (IData)(__Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__151__meas)
                                        : 0U);
                                vlSelfRef.__VdlyVal__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__max_r__v3 
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
                            __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__inc16__152__v 
                                = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__samples_r;
                            __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__inc16__152__Vfuncout 
                                = (0x0000ffffU & ((0x0000ffffU 
                                                   == (IData)(__Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__inc16__152__v))
                                                   ? (IData)(__Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__inc16__152__v)
                                                   : 
                                                  ((IData)(1U) 
                                                   + (IData)(__Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__inc16__152__v))));
                            vlSelfRef.__Vdly__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__active_r = 0U;
                            vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__epoch_r 
                                = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__epoch_pend_r;
                            vlSelfRef.__Vdly__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__samples_r 
                                = __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__inc16__152__Vfuncout;
                        } else {
                            vlSelfRef.__Vdly__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__stg_r 
                                = (3U & ((IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__stg_r) 
                                         + (IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__nadv_w)));
                        }
                        if (((1U >= (IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__didx_w)) 
                             & (1U < ((IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__didx_w) 
                                      + (IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__nadv_w))))) {
                            __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__147__meas 
                                = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__dsat_w;
                            __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__148__meas 
                                = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__dsat_w;
                            __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__150__meas 
                                = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__dsat_w;
                            __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__147__didx 
                                = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__didx_w;
                            __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__148__didx 
                                = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__didx_w;
                            __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__150__didx 
                                = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__didx_w;
                            vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT____VlemCall_0__hopd 
                                = ((1U == __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__147__didx)
                                    ? (IData)(__Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__147__meas)
                                    : 0U);
                            vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT____VlemCall_1__hopd 
                                = ((1U == __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__148__didx)
                                    ? (IData)(__Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__148__meas)
                                    : 0U);
                            vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT____VlemCall_3__hopd 
                                = ((1U == __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__150__didx)
                                    ? (IData)(__Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__150__meas)
                                    : 0U);
                            vlSelfRef.__VdlyVal__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__last_r__v4 
                                = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT____VlemCall_0__hopd;
                            vlSelfRef.__VdlySet__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__last_r__v4 = 1U;
                            if (((IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT____VlemCall_1__hopd) 
                                 < vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__min_r[1U])) {
                                __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__149__meas 
                                    = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__dsat_w;
                                __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__149__didx 
                                    = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__didx_w;
                                vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT____VlemCall_2__hopd 
                                    = ((1U == __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__149__didx)
                                        ? (IData)(__Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__149__meas)
                                        : 0U);
                                vlSelfRef.__VdlyVal__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__min_r__v4 
                                    = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT____VlemCall_2__hopd;
                                vlSelfRef.__VdlySet__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__min_r__v4 = 1U;
                            }
                            if (((IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT____VlemCall_3__hopd) 
                                 > vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__max_r[1U])) {
                                __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__151__meas 
                                    = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__dsat_w;
                                __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__151__didx 
                                    = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__didx_w;
                                vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT____VlemCall_4__hopd 
                                    = ((1U == __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__151__didx)
                                        ? (IData)(__Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__151__meas)
                                        : 0U);
                                vlSelfRef.__VdlyVal__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__max_r__v4 
                                    = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT____VlemCall_4__hopd;
                                vlSelfRef.__VdlySet__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__max_r__v4 = 1U;
                            }
                        }
                        if (((2U >= (IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__didx_w)) 
                             & (2U < ((IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__didx_w) 
                                      + (IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__nadv_w))))) {
                            __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__147__meas 
                                = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__dsat_w;
                            __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__148__meas 
                                = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__dsat_w;
                            __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__150__meas 
                                = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__dsat_w;
                            __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__147__didx 
                                = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__didx_w;
                            __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__148__didx 
                                = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__didx_w;
                            __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__150__didx 
                                = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__didx_w;
                            vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT____VlemCall_0__hopd 
                                = ((2U == __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__147__didx)
                                    ? (IData)(__Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__147__meas)
                                    : 0U);
                            vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT____VlemCall_1__hopd 
                                = ((2U == __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__148__didx)
                                    ? (IData)(__Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__148__meas)
                                    : 0U);
                            vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT____VlemCall_3__hopd 
                                = ((2U == __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__150__didx)
                                    ? (IData)(__Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__150__meas)
                                    : 0U);
                            vlSelfRef.__VdlyVal__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__last_r__v5 
                                = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT____VlemCall_0__hopd;
                            vlSelfRef.__VdlySet__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__last_r__v5 = 1U;
                            if (((IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT____VlemCall_1__hopd) 
                                 < vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__min_r[2U])) {
                                __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__149__meas 
                                    = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__dsat_w;
                                __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__149__didx 
                                    = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__didx_w;
                                vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT____VlemCall_2__hopd 
                                    = ((2U == __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__149__didx)
                                        ? (IData)(__Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__149__meas)
                                        : 0U);
                                vlSelfRef.__VdlyVal__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__min_r__v5 
                                    = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT____VlemCall_2__hopd;
                                vlSelfRef.__VdlySet__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__min_r__v5 = 1U;
                            }
                            if (((IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT____VlemCall_3__hopd) 
                                 > vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__max_r[2U])) {
                                __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__151__meas 
                                    = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__dsat_w;
                                __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__151__didx 
                                    = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__didx_w;
                                vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT____VlemCall_4__hopd 
                                    = ((2U == __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__151__didx)
                                        ? (IData)(__Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__hopd__151__meas)
                                        : 0U);
                                vlSelfRef.__VdlyVal__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__max_r__v5 
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
                        __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__inc16__153__v 
                            = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__samples_r;
                        __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__inc16__153__Vfuncout 
                            = (0x0000ffffU & ((0x0000ffffU 
                                               == (IData)(__Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__inc16__153__v))
                                               ? (IData)(__Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__inc16__153__v)
                                               : ((IData)(1U) 
                                                  + (IData)(__Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__inc16__153__v))));
                        vlSelfRef.__Vdly__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__active_r = 0U;
                        vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__epoch_r 
                            = ((vlSelfRef.milan_datapath__DOT__ts_counter__DOT__acc[1U] 
                                << 8U) | (vlSelfRef.milan_datapath__DOT__ts_counter__DOT__acc[0U] 
                                          >> 0x00000018U));
                        vlSelfRef.__Vdly__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__samples_r 
                            = __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__inc16__153__Vfuncout;
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
                    __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__inc16__138__v 
                        = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__timeouts_r;
                    __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__inc16__138__Vfuncout 
                        = (0x0000ffffU & ((0x0000ffffU 
                                           == (IData)(__Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__inc16__138__v))
                                           ? (IData)(__Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__inc16__138__v)
                                           : ((IData)(1U) 
                                              + (IData)(__Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__inc16__138__v))));
                    vlSelfRef.__Vdly__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__active_r = 0U;
                    vlSelfRef.__Vdly__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__timeouts_r 
                        = __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__inc16__138__Vfuncout;
                } else {
                    vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__to_r 
                        = (0x0000ffffU & ((IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__to_r) 
                                          - (IData)(1U)));
                    if ((0U != (IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__nadv_w))) {
                        if (((0U >= (IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__didx_w)) 
                             & (0U < ((IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__didx_w) 
                                      + (IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__nadv_w))))) {
                            __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__139__meas 
                                = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__dsat_w;
                            __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__140__meas 
                                = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__dsat_w;
                            __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__142__meas 
                                = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__dsat_w;
                            __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__139__didx 
                                = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__didx_w;
                            __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__140__didx 
                                = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__didx_w;
                            __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__142__didx 
                                = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__didx_w;
                            vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT____VlemCall_0__hopd 
                                = ((0U == __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__139__didx)
                                    ? (IData)(__Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__139__meas)
                                    : 0U);
                            vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT____VlemCall_1__hopd 
                                = ((0U == __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__140__didx)
                                    ? (IData)(__Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__140__meas)
                                    : 0U);
                            vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT____VlemCall_3__hopd 
                                = ((0U == __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__142__didx)
                                    ? (IData)(__Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__142__meas)
                                    : 0U);
                            vlSelfRef.__VdlyVal__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__last_r__v3 
                                = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT____VlemCall_0__hopd;
                            vlSelfRef.__VdlySet__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__last_r__v3 = 1U;
                            if (((IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT____VlemCall_1__hopd) 
                                 < vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__min_r[0U])) {
                                __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__141__meas 
                                    = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__dsat_w;
                                __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__141__didx 
                                    = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__didx_w;
                                vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT____VlemCall_2__hopd 
                                    = ((0U == __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__141__didx)
                                        ? (IData)(__Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__141__meas)
                                        : 0U);
                                vlSelfRef.__VdlyVal__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__min_r__v3 
                                    = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT____VlemCall_2__hopd;
                                vlSelfRef.__VdlySet__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__min_r__v3 = 1U;
                            }
                            if (((IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT____VlemCall_3__hopd) 
                                 > vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__max_r[0U])) {
                                __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__143__meas 
                                    = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__dsat_w;
                                __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__143__didx 
                                    = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__didx_w;
                                vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT____VlemCall_4__hopd 
                                    = ((0U == __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__143__didx)
                                        ? (IData)(__Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__143__meas)
                                        : 0U);
                                vlSelfRef.__VdlyVal__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__max_r__v3 
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
                            __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__inc16__144__v 
                                = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__samples_r;
                            __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__inc16__144__Vfuncout 
                                = (0x0000ffffU & ((0x0000ffffU 
                                                   == (IData)(__Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__inc16__144__v))
                                                   ? (IData)(__Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__inc16__144__v)
                                                   : 
                                                  ((IData)(1U) 
                                                   + (IData)(__Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__inc16__144__v))));
                            vlSelfRef.__Vdly__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__active_r = 0U;
                            vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__epoch_r 
                                = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__epoch_pend_r;
                            vlSelfRef.__Vdly__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__samples_r 
                                = __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__inc16__144__Vfuncout;
                        } else {
                            vlSelfRef.__Vdly__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__stg_r 
                                = (3U & ((IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__stg_r) 
                                         + (IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__nadv_w)));
                        }
                        if (((1U >= (IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__didx_w)) 
                             & (1U < ((IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__didx_w) 
                                      + (IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__nadv_w))))) {
                            __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__139__meas 
                                = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__dsat_w;
                            __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__140__meas 
                                = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__dsat_w;
                            __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__142__meas 
                                = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__dsat_w;
                            __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__139__didx 
                                = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__didx_w;
                            __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__140__didx 
                                = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__didx_w;
                            __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__142__didx 
                                = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__didx_w;
                            vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT____VlemCall_0__hopd 
                                = ((1U == __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__139__didx)
                                    ? (IData)(__Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__139__meas)
                                    : 0U);
                            vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT____VlemCall_1__hopd 
                                = ((1U == __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__140__didx)
                                    ? (IData)(__Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__140__meas)
                                    : 0U);
                            vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT____VlemCall_3__hopd 
                                = ((1U == __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__142__didx)
                                    ? (IData)(__Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__142__meas)
                                    : 0U);
                            vlSelfRef.__VdlyVal__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__last_r__v4 
                                = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT____VlemCall_0__hopd;
                            vlSelfRef.__VdlySet__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__last_r__v4 = 1U;
                            if (((IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT____VlemCall_1__hopd) 
                                 < vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__min_r[1U])) {
                                __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__141__meas 
                                    = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__dsat_w;
                                __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__141__didx 
                                    = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__didx_w;
                                vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT____VlemCall_2__hopd 
                                    = ((1U == __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__141__didx)
                                        ? (IData)(__Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__141__meas)
                                        : 0U);
                                vlSelfRef.__VdlyVal__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__min_r__v4 
                                    = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT____VlemCall_2__hopd;
                                vlSelfRef.__VdlySet__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__min_r__v4 = 1U;
                            }
                            if (((IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT____VlemCall_3__hopd) 
                                 > vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__max_r[1U])) {
                                __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__143__meas 
                                    = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__dsat_w;
                                __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__143__didx 
                                    = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__didx_w;
                                vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT____VlemCall_4__hopd 
                                    = ((1U == __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__143__didx)
                                        ? (IData)(__Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__143__meas)
                                        : 0U);
                                vlSelfRef.__VdlyVal__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__max_r__v4 
                                    = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT____VlemCall_4__hopd;
                                vlSelfRef.__VdlySet__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__max_r__v4 = 1U;
                            }
                        }
                        if (((2U >= (IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__didx_w)) 
                             & (2U < ((IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__didx_w) 
                                      + (IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__nadv_w))))) {
                            __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__139__meas 
                                = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__dsat_w;
                            __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__140__meas 
                                = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__dsat_w;
                            __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__142__meas 
                                = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__dsat_w;
                            __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__139__didx 
                                = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__didx_w;
                            __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__140__didx 
                                = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__didx_w;
                            __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__142__didx 
                                = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__didx_w;
                            vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT____VlemCall_0__hopd 
                                = ((2U == __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__139__didx)
                                    ? (IData)(__Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__139__meas)
                                    : 0U);
                            vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT____VlemCall_1__hopd 
                                = ((2U == __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__140__didx)
                                    ? (IData)(__Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__140__meas)
                                    : 0U);
                            vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT____VlemCall_3__hopd 
                                = ((2U == __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__142__didx)
                                    ? (IData)(__Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__142__meas)
                                    : 0U);
                            vlSelfRef.__VdlyVal__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__last_r__v5 
                                = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT____VlemCall_0__hopd;
                            vlSelfRef.__VdlySet__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__last_r__v5 = 1U;
                            if (((IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT____VlemCall_1__hopd) 
                                 < vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__min_r[2U])) {
                                __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__141__meas 
                                    = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__dsat_w;
                                __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__141__didx 
                                    = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__didx_w;
                                vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT____VlemCall_2__hopd 
                                    = ((2U == __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__141__didx)
                                        ? (IData)(__Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__141__meas)
                                        : 0U);
                                vlSelfRef.__VdlyVal__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__min_r__v5 
                                    = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT____VlemCall_2__hopd;
                                vlSelfRef.__VdlySet__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__min_r__v5 = 1U;
                            }
                            if (((IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT____VlemCall_3__hopd) 
                                 > vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__max_r[2U])) {
                                __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__143__meas 
                                    = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__dsat_w;
                                __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__143__didx 
                                    = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__didx_w;
                                vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT____VlemCall_4__hopd 
                                    = ((2U == __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__143__didx)
                                        ? (IData)(__Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__hopd__143__meas)
                                        : 0U);
                                vlSelfRef.__VdlyVal__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__max_r__v5 
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
                        __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__inc16__145__v 
                            = vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__samples_r;
                        __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__inc16__145__Vfuncout 
                            = (0x0000ffffU & ((0x0000ffffU 
                                               == (IData)(__Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__inc16__145__v))
                                               ? (IData)(__Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__inc16__145__v)
                                               : ((IData)(1U) 
                                                  + (IData)(__Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__inc16__145__v))));
                        vlSelfRef.__Vdly__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__active_r = 0U;
                        vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__epoch_r 
                            = ((vlSelfRef.milan_datapath__DOT__ts_counter__DOT__acc[1U] 
                                << 8U) | (vlSelfRef.milan_datapath__DOT__ts_counter__DOT__acc[0U] 
                                          >> 0x00000018U));
                        vlSelfRef.__Vdly__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__samples_r 
                            = __Vfunc_milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__inc16__145__Vfuncout;
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
        if (vlSelfRef.milan_datapath__DOT__evt_link_change) {
            vlSelfRef.milan_datapath__DOT__csr__DOT__irq_status 
                = (2U | vlSelfRef.milan_datapath__DOT__csr__DOT__irq_status);
        }
        if (vlSelfRef.milan_datapath__DOT__ethernet_counters__DOT__rollover_r) {
            vlSelfRef.milan_datapath__DOT__csr__DOT__irq_status 
                = (4U | vlSelfRef.milan_datapath__DOT__csr__DOT__irq_status);
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
        if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_la_msrp_w) 
              & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_grant_w))) 
             & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w)) 
                | (9U != (0x0000000fU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w))))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_pend_r 
                = (1U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_pend_r));
        } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_grant_w))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_pend_r 
                = (0x1eU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_pend_r));
        }
        if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_la_msrp_w) 
              & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_grant_w) 
                    >> 1U))) & ((~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w) 
                                    >> 1U)) | (9U != 
                                               (0x0000000fU 
                                                & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w 
                                                   >> 4U)))))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_pend_r 
                = (2U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_pend_r));
        } else if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_grant_w))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_pend_r 
                = (0x1dU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_pend_r));
        }
        if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_la_msrp_w) 
              & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_grant_w) 
                    >> 2U))) & ((~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w) 
                                    >> 2U)) | (9U != 
                                               (0x0000000fU 
                                                & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w 
                                                   >> 8U)))))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_pend_r 
                = (4U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_pend_r));
        } else if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_grant_w))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_pend_r 
                = (0x1bU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_pend_r));
        }
        if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_la_msrp_w) 
              & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_grant_w) 
                    >> 3U))) & ((~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w) 
                                    >> 3U)) | (9U != 
                                               (0x0000000fU 
                                                & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w 
                                                   >> 0x0cU)))))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_pend_r 
                = (8U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_pend_r));
        } else if ((8U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_grant_w))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_pend_r 
                = (0x17U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_pend_r));
        }
        if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_la_msrp_w) 
              & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_grant_w) 
                    >> 4U))) & ((~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w) 
                                    >> 4U)) | (9U != 
                                               (0x0000000fU 
                                                & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w 
                                                   >> 0x10U)))))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_pend_r 
                = (0x00000010U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_pend_r));
        } else if ((0x00000010U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_grant_w))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_pend_r 
                = (0x0fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_pend_r));
        }
        if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_la_msrp_w) 
              & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rla_grant_w))) 
             & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_ev_v_w)) 
                | (9U != (0x0000000fU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_ev_w))))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rla_pend_r 
                = (1U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rla_pend_r));
        } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rla_grant_w))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rla_pend_r 
                = (0x1eU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rla_pend_r));
        }
        if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_la_msrp_w) 
              & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rla_grant_w) 
                    >> 1U))) & ((~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_ev_v_w) 
                                    >> 1U)) | (9U != 
                                               (0x0000000fU 
                                                & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_ev_w 
                                                   >> 4U)))))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rla_pend_r 
                = (2U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rla_pend_r));
        } else if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rla_grant_w))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rla_pend_r 
                = (0x1dU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rla_pend_r));
        }
        if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_la_msrp_w) 
              & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rla_grant_w) 
                    >> 2U))) & ((~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_ev_v_w) 
                                    >> 2U)) | (9U != 
                                               (0x0000000fU 
                                                & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_ev_w 
                                                   >> 8U)))))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rla_pend_r 
                = (4U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rla_pend_r));
        } else if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rla_grant_w))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rla_pend_r 
                = (0x1bU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rla_pend_r));
        }
        if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_la_msrp_w) 
              & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rla_grant_w) 
                    >> 3U))) & ((~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_ev_v_w) 
                                    >> 3U)) | (9U != 
                                               (0x0000000fU 
                                                & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_ev_w 
                                                   >> 0x0cU)))))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rla_pend_r 
                = (8U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rla_pend_r));
        } else if ((8U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rla_grant_w))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rla_pend_r 
                = (0x17U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rla_pend_r));
        }
        if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_la_msrp_w) 
              & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rla_grant_w) 
                    >> 4U))) & ((~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_ev_v_w) 
                                    >> 4U)) | (9U != 
                                               (0x0000000fU 
                                                & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_ev_w 
                                                   >> 0x10U)))))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rla_pend_r 
                = (0x00000010U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rla_pend_r));
        } else if ((0x00000010U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rla_grant_w))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rla_pend_r 
                = (0x0fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rla_pend_r));
        }
        if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__ctl_acc_w) 
             & (0U == (7U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r))))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rtype_r 
                = (0x1eU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rtype_r));
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__fcode_r 
                = (0x000000ffffffff00ULL & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__fcode_r);
        }
        if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_rx_hit_w) 
              >> 1U) & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rx_registering_w))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rtype_r 
                = ((0x1dU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rtype_r)) 
                   | ((2U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_attr_type_w)) 
                      << 1U));
            if ((2U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_attr_type_w))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__fcode_r 
                    = ((0x000000ffffff00ffULL & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__fcode_r) 
                       | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_fail_code_w)) 
                          << 8U));
            }
        }
        if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__ctl_acc_w) 
             & (1U == (7U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r))))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rtype_r 
                = (0x1dU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rtype_r));
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__fcode_r 
                = (0x000000ffffff00ffULL & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__fcode_r);
        }
        if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_rx_hit_w) 
              >> 2U) & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rx_registering_w))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rtype_r 
                = ((0x1bU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rtype_r)) 
                   | ((2U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_attr_type_w)) 
                      << 2U));
            if ((2U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_attr_type_w))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__fcode_r 
                    = ((0x000000ffff00ffffULL & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__fcode_r) 
                       | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_fail_code_w)) 
                          << 0x00000010U));
            }
        }
        if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__ctl_acc_w) 
             & (2U == (7U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r))))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rtype_r 
                = (0x1bU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rtype_r));
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__fcode_r 
                = (0x000000ffff00ffffULL & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__fcode_r);
        }
        if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_rx_hit_w) 
              >> 3U) & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rx_registering_w))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rtype_r 
                = ((0x17U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rtype_r)) 
                   | ((2U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_attr_type_w)) 
                      << 3U));
            if ((2U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_attr_type_w))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__fcode_r 
                    = ((0x000000ff00ffffffULL & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__fcode_r) 
                       | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_fail_code_w)) 
                          << 0x00000018U));
            }
        }
        if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__ctl_acc_w) 
             & (3U == (7U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r))))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rtype_r 
                = (0x17U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rtype_r));
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__fcode_r 
                = (0x000000ff00ffffffULL & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__fcode_r);
        }
        if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_rx_hit_w) 
              >> 4U) & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rx_registering_w))) {
            if ((0x00000010U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__ind_reg_w))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_evt_tk_reg_w 
                    = (0x00000010U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_evt_tk_reg_w));
            }
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rtype_r 
                = ((0x0fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rtype_r)) 
                   | ((2U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_attr_type_w)) 
                      << 4U));
            if ((2U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_attr_type_w))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__fcode_r 
                    = ((0x00000000ffffffffULL & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__fcode_r) 
                       | ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_fail_code_w)) 
                          << 0x00000020U));
            }
        }
        if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__ctl_acc_w) 
             & (4U == (7U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r))))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rtype_r 
                = (0x0fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rtype_r));
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__fcode_r 
                = (0x00000000ffffffffULL & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__fcode_r);
        }
        if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__DOT__byte_acc_w) {
            if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__p2_l_r) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__DOT__wr_closed_r = 1U;
            }
        }
        if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__4__KET____DOT__u_rx_slots__DOT__byte_acc_w) {
            if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__p2_l_r) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__4__KET____DOT__u_rx_slots__DOT__wr_closed_r = 1U;
            }
        }
        if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__2__KET____DOT__u_rx_slots__DOT__byte_acc_w) {
            if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__p2_l_r) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__2__KET____DOT__u_rx_slots__DOT__wr_closed_r = 1U;
            }
        }
        if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__1__KET____DOT__u_rx_slots__DOT__byte_acc_w) {
            if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__p2_l_r) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__1__KET____DOT__u_rx_slots__DOT__wr_closed_r = 1U;
            }
        }
        if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__0__KET____DOT__u_rx_slots__DOT__byte_acc_w) {
            if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__p2_l_r) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__0__KET____DOT__u_rx_slots__DOT__wr_closed_r = 1U;
            }
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
                if ((4U >= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vsel_ix_w))) {
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vj_pend_r 
                        = ((~ ((IData)(1U) << (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vsel_ix_w))) 
                           & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vj_pend_r));
                }
            } else if ((4U >= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vsel_ix_w))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vl_pend_r 
                    = ((~ ((IData)(1U) << (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vsel_ix_w))) 
                       & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vl_pend_r));
            }
        }
        if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__ctl_acc_w) {
            if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_open_r) {
                if ((4U >= (7U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r)))) {
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__armed_r 
                        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__armed_r) 
                           | (0x1fU & ((IData)(1U) 
                                       << (7U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r)))));
                }
                if ((0xefU >= (0x000000ffU & ((IData)(0x00000030U) 
                                              * (7U 
                                                 & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r)))))) {
                    VL_ASSIGNSEL_WQ(240, 48, (0x000000ffU 
                                              & ((IData)(0x00000030U) 
                                                 * 
                                                 (7U 
                                                  & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r)))), vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__da_r, vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_da_r);
                }
                if (((((4U >= (7U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r))) 
                       && (1U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vl_pend_r) 
                                 >> (7U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r))))) 
                      & (((0x3bU >= (0x0000003fU & 
                                     ((IData)(0x0000000cU) 
                                      * (7U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r)))))
                           ? (0x00000fffU & (IData)(
                                                    (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vl_vid_r 
                                                     >> 
                                                     (0x0000003fU 
                                                      & ((IData)(0x0000000cU) 
                                                         * 
                                                         (7U 
                                                          & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r)))))))
                           : 0U) == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_vid_r))) 
                     & (~ ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vsel_v_w) 
                             & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__ls_user_ready_w)) 
                            & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vsel_join_w))) 
                           & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vsel_ix_w) 
                              == (7U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r))))))) {
                    if ((4U >= (7U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r)))) {
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vl_pend_r 
                            = ((~ ((IData)(1U) << (7U 
                                                   & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r)))) 
                               & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vl_pend_r));
                    }
                } else {
                    if ((4U >= (7U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r)))) {
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vj_pend_r 
                            = ((IData)(vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vj_pend_r) 
                               | (0x1fU & ((IData)(1U) 
                                           << (7U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r)))));
                    }
                    if ((0x3bU >= (0x0000003fU & ((IData)(0x0000000cU) 
                                                  * 
                                                  (7U 
                                                   & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r)))))) {
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vj_vid_r 
                            = (((~ (0x0000000000000fffULL 
                                    << (0x0000003fU 
                                        & ((IData)(0x0000000cU) 
                                           * (7U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r)))))) 
                                & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vj_vid_r) 
                               | (0x0fffffffffffffffULL 
                                  & ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_vid_r)) 
                                     << (0x0000003fU 
                                         & ((IData)(0x0000000cU) 
                                            * (7U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r)))))));
                    }
                }
            } else {
                if ((4U >= (7U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r)))) {
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__armed_r 
                        = ((~ ((IData)(1U) << (7U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r)))) 
                           & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__armed_r));
                }
                if ((((4U >= (7U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r))) 
                      && (1U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vj_pend_r) 
                                >> (7U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r))))) 
                     & (~ ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vsel_v_w) 
                             & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__ls_user_ready_w)) 
                            & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vsel_join_w)) 
                           & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vsel_ix_w) 
                              == (7U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r))))))) {
                    if ((4U >= (7U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r)))) {
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vj_pend_r 
                            = ((~ ((IData)(1U) << (7U 
                                                   & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r)))) 
                               & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vj_pend_r));
                    }
                } else {
                    if ((4U >= (7U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r)))) {
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vl_pend_r 
                            = ((IData)(vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vl_pend_r) 
                               | (0x1fU & ((IData)(1U) 
                                           << (7U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r)))));
                    }
                    if ((0x3bU >= (0x0000003fU & ((IData)(0x0000000cU) 
                                                  * 
                                                  (7U 
                                                   & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r)))))) {
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vl_vid_r 
                            = (((~ (0x0000000000000fffULL 
                                    << (0x0000003fU 
                                        & ((IData)(0x0000000cU) 
                                           * (7U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r)))))) 
                                & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vl_vid_r) 
                               | (0x0fffffffffffffffULL 
                                  & ((QData)((IData)(
                                                     ((0x3bU 
                                                       >= 
                                                       (0x0000003fU 
                                                        & ((IData)(0x0000000cU) 
                                                           * 
                                                           (7U 
                                                            & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r)))))
                                                       ? 
                                                      (0x00000fffU 
                                                       & (IData)(
                                                                 (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vid_r 
                                                                  >> 
                                                                  (0x0000003fU 
                                                                   & ((IData)(0x0000000cU) 
                                                                      * 
                                                                      (7U 
                                                                       & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r)))))))
                                                       : 0U))) 
                                     << (0x0000003fU 
                                         & ((IData)(0x0000000cU) 
                                            * (7U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r)))))));
                    }
                }
            }
        }
        if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vsel_v_w) 
             & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tk_user_ready_w))) {
            if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vsel_join_w) {
                if ((4U >= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vsel_ix_w))) {
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vj_pend_r 
                        = ((~ ((IData)(1U) << (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vsel_ix_w))) 
                           & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vj_pend_r));
                }
            } else if ((4U >= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vsel_ix_w))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vl_pend_r 
                    = ((~ ((IData)(1U) << (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vsel_ix_w))) 
                       & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vl_pend_r));
            }
        }
        if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__gate_acc_w) {
            if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_open_r) {
                if (((((4U >= (7U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r))) 
                       && (1U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vl_pend_r) 
                                 >> (7U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r))))) 
                      & (((0x3bU >= (0x0000003fU & 
                                     ((IData)(0x0000000cU) 
                                      * (7U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r)))))
                           ? (0x00000fffU & (IData)(
                                                    (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vl_vid_r 
                                                     >> 
                                                     (0x0000003fU 
                                                      & ((IData)(0x0000000cU) 
                                                         * 
                                                         (7U 
                                                          & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r)))))))
                           : 0U) == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_vid_r))) 
                     & (~ ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vsel_v_w) 
                             & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tk_user_ready_w)) 
                            & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vsel_join_w))) 
                           & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vsel_ix_w) 
                              == (7U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r))))))) {
                    if ((4U >= (7U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r)))) {
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vl_pend_r 
                            = ((~ ((IData)(1U) << (7U 
                                                   & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r)))) 
                               & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vl_pend_r));
                    }
                } else {
                    if ((4U >= (7U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r)))) {
                        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vj_pend_r 
                            = ((IData)(vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vj_pend_r) 
                               | (0x1fU & ((IData)(1U) 
                                           << (7U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r)))));
                    }
                    if ((0x3bU >= (0x0000003fU & ((IData)(0x0000000cU) 
                                                  * 
                                                  (7U 
                                                   & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r)))))) {
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vj_vid_r 
                            = (((~ (0x0000000000000fffULL 
                                    << (0x0000003fU 
                                        & ((IData)(0x0000000cU) 
                                           * (7U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r)))))) 
                                & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vj_vid_r) 
                               | (0x0fffffffffffffffULL 
                                  & ((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_vid_r)) 
                                     << (0x0000003fU 
                                         & ((IData)(0x0000000cU) 
                                            * (7U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r)))))));
                    }
                }
            } else if ((((4U >= (7U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r))) 
                         && (1U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vj_pend_r) 
                                   >> (7U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r))))) 
                        & (~ ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vsel_v_w) 
                                & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tk_user_ready_w)) 
                               & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vsel_join_w)) 
                              & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vsel_ix_w) 
                                 == (7U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r))))))) {
                if ((4U >= (7U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r)))) {
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vj_pend_r 
                        = ((~ ((IData)(1U) << (7U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r)))) 
                           & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vj_pend_r));
                }
            } else {
                if ((4U >= (7U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r)))) {
                    vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vl_pend_r 
                        = ((IData)(vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vl_pend_r) 
                           | (0x1fU & ((IData)(1U) 
                                       << (7U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r)))));
                }
                if ((0x3bU >= (0x0000003fU & ((IData)(0x0000000cU) 
                                              * (7U 
                                                 & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r)))))) {
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vl_vid_r 
                        = (((~ (0x0000000000000fffULL 
                                << (0x0000003fU & ((IData)(0x0000000cU) 
                                                   * 
                                                   (7U 
                                                    & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r)))))) 
                            & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vl_vid_r) 
                           | (0x0fffffffffffffffULL 
                              & ((QData)((IData)(((0x3bU 
                                                   >= 
                                                   (0x0000003fU 
                                                    & ((IData)(0x0000000cU) 
                                                       * 
                                                       (7U 
                                                        & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r)))))
                                                   ? 
                                                  (0x00000fffU 
                                                   & (IData)(
                                                             (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vid_r 
                                                              >> 
                                                              (0x0000003fU 
                                                               & ((IData)(0x0000000cU) 
                                                                  * 
                                                                  (7U 
                                                                   & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r)))))))
                                                   : 0U))) 
                                 << (0x0000003fU & 
                                     ((IData)(0x0000000cU) 
                                      * (7U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r)))))));
                }
            }
        }
        if ((0x9fU >= (0x000000ffU & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__cidx_q2_r) 
                                      << 5U)))) {
            VL_ASSIGNSEL_WI(160, 32, (0x000000ffU & 
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
        if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_rx_hit_w) 
             & (((0U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_mrp_event_w)) 
                 | (1U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_mrp_event_w))) 
                | (3U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_mrp_event_w))))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_val_r 
                = ((0x03fcU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_val_r)) 
                   | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_fourpacked_w));
        }
        if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__gate_acc_w) 
              & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_open_r)) 
             & (0U == (7U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r))))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_val_r 
                = (0x03fcU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_val_r));
        }
        if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_rx_hit_w) 
              >> 1U) & (((0U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_mrp_event_w)) 
                         | (1U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_mrp_event_w))) 
                        | (3U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_mrp_event_w))))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_val_r 
                = ((0x03f3U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_val_r)) 
                   | ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_fourpacked_w) 
                      << 2U));
        }
        if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__gate_acc_w) 
              & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_open_r)) 
             & (1U == (7U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r))))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_val_r 
                = (0x03f3U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_val_r));
        }
        if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_rx_hit_w) 
              >> 2U) & (((0U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_mrp_event_w)) 
                         | (1U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_mrp_event_w))) 
                        | (3U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_mrp_event_w))))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_val_r 
                = ((0x03cfU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_val_r)) 
                   | ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_fourpacked_w) 
                      << 4U));
        }
        if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__gate_acc_w) 
              & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_open_r)) 
             & (2U == (7U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r))))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_val_r 
                = (0x03cfU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_val_r));
        }
        if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_rx_hit_w) 
              >> 3U) & (((0U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_mrp_event_w)) 
                         | (1U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_mrp_event_w))) 
                        | (3U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_mrp_event_w))))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_val_r 
                = ((0x033fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_val_r)) 
                   | ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_fourpacked_w) 
                      << 6U));
        }
        if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__gate_acc_w) 
              & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_open_r)) 
             & (3U == (7U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r))))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_val_r 
                = (0x033fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_val_r));
        }
        if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_rx_hit_w) 
              >> 4U) & (((0U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_mrp_event_w)) 
                         | (1U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_mrp_event_w))) 
                        | (3U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_mrp_event_w))))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_val_r 
                = ((0x00ffU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_val_r)) 
                   | ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_fourpacked_w) 
                      << 8U));
        }
        if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__gate_acc_w) 
              & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_open_r)) 
             & (4U == (7U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r))))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_val_r 
                = (0x00ffU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_val_r));
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
                __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_hit__207__cnt_a 
                    = vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rx_req_cnt_r;
                __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_hit__207__start_a 
                    = vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rx_req_start_r;
                __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_hit__207__our_s 
                    = vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__offset_r;
                __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_hit__207__our_e 
                    = (0x0000ffffU & ((IData)(vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__offset_r) 
                                      + (0x000000ffU 
                                         & (vlSelfRef.milan_datapath__DOT__csr__DOT__maap_ctrl 
                                            >> 8U))));
                __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_hit__207__req_s 
                    = (0x0000ffffU & (IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_hit__207__start_a));
                __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_hit__207__req_e 
                    = (0x0000ffffU & ((IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_hit__207__req_s) 
                                      + (IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_hit__207__cnt_a)));
                vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT____VlemCall_21__conflict_hit 
                    = ((0x91e0f000U == (IData)((__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_hit__207__start_a 
                                                >> 0x10U))) 
                       & ((((IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_hit__207__our_s) 
                            >= (IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_hit__207__req_s)) 
                           & ((IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_hit__207__our_s) 
                              <= (IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_hit__207__req_e))) 
                          | (((IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_hit__207__req_s) 
                              >= (IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_hit__207__our_s)) 
                             & ((IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_hit__207__req_s) 
                                <= (IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_hit__207__our_e)))));
                if (vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT____VlemCall_21__conflict_hit) {
                    if ((1U == (IData)(vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__state_r))) {
                        __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rand_offset__208__cnt 
                            = (0x000000ffU & (vlSelfRef.milan_datapath__DOT__csr__DOT__maap_ctrl 
                                              >> 8U));
                        __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rand_offset__208__rnd 
                            = vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lfsr_r;
                        vlSelfRef.__Vdly__milan_datapath__DOT__maap_conflicts 
                            = (0x000000ffU & ((0x000000ffU 
                                               == (IData)(vlSelfRef.milan_datapath__DOT__maap_conflicts))
                                               ? (IData)(vlSelfRef.milan_datapath__DOT__maap_conflicts)
                                               : ((IData)(1U) 
                                                  + (IData)(vlSelfRef.milan_datapath__DOT__maap_conflicts))));
                        __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rand_offset__208__o 
                            = (0x0000ffffU & ((0xfe00U 
                                               <= (IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rand_offset__208__rnd))
                                               ? ((IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rand_offset__208__rnd) 
                                                  - (IData)(0xfe00U))
                                               : (IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rand_offset__208__rnd)));
                        vlSelfRef.__Vdly__milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__probe_left_r = 3U;
                        vlSelfRef.__Vdly__milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__timer_ms_r 
                            = (0x0000ffffU & ((IData)(0x01f4U) 
                                              + (0x0000007fU 
                                                 & (IData)(vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lfsr_r))));
                        if (((IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rand_offset__208__o) 
                             > (0x0000ffffU & ((IData)(0xfe00U) 
                                               - (IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rand_offset__208__cnt))))) {
                            __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rand_offset__208__o 
                                = (0x0000ffffU & ((IData)(0xfe00U) 
                                                  - (IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rand_offset__208__cnt)));
                        }
                        __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rand_offset__208__Vfuncout 
                            = __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rand_offset__208__o;
                        vlSelfRef.__Vdly__milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__offset_r 
                            = __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rand_offset__208__Vfuncout;
                    } else if ((1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_busy_r)))) {
                        __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__209__cnt_a 
                            = vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rx_req_cnt_r;
                        __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__209__start_a 
                            = vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rx_req_start_r;
                        vlSelfRef.milan_datapath__DOT__maap_defends 
                            = (0x000000ffU & ((0x000000ffU 
                                               == (IData)(vlSelfRef.milan_datapath__DOT__maap_defends))
                                               ? (IData)(vlSelfRef.milan_datapath__DOT__maap_defends)
                                               : ((IData)(1U) 
                                                  + (IData)(vlSelfRef.milan_datapath__DOT__maap_defends))));
                        __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__209__our_s 
                            = vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__offset_r;
                        vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_msg_r = 2U;
                        vlSelfRef.__Vdly__milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_busy_r = 1U;
                        __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__209__our_e 
                            = (0x0000ffffU & ((IData)(vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__offset_r) 
                                              + (0x000000ffU 
                                                 & (vlSelfRef.milan_datapath__DOT__csr__DOT__maap_ctrl 
                                                    >> 8U))));
                        __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__209__req_s 
                            = (0x0000ffffU & (IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__209__start_a));
                        __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__209__req_e 
                            = (0x0000ffffU & ((IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__209__req_s) 
                                              + (IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__209__cnt_a)));
                        if ((((IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__209__our_s) 
                              >= (IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__209__req_s)) 
                             & ((IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__209__our_s) 
                                <= (IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__209__req_e)))) {
                            __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__209__c_s 
                                = __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__209__our_s;
                            __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__209__c_c 
                                = (0x0000ffffU & ((
                                                   ((IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__209__our_e) 
                                                    < (IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__209__req_e))
                                                    ? (IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__209__our_e)
                                                    : (IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__209__req_e)) 
                                                  - (IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__209__our_s)));
                        } else {
                            __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__209__c_s 
                                = __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__209__req_s;
                            __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__209__c_c 
                                = (0x0000ffffU & ((
                                                   ((IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__209__req_e) 
                                                    < (IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__209__our_e))
                                                    ? (IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__209__req_e)
                                                    : (IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__209__our_e)) 
                                                  - (IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__209__req_s)));
                        }
                        vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT____VlemCall_22__conflict_range 
                            = (((IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__209__c_s) 
                                << 0x00000010U) | (IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__209__c_c));
                        vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_conf_start_r 
                            = (vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT____VlemCall_22__conflict_range 
                               >> 0x00000010U);
                        __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__210__cnt_a 
                            = vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rx_req_cnt_r;
                        __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__210__start_a 
                            = vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rx_req_start_r;
                        __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__210__our_s 
                            = vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__offset_r;
                        __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__210__our_e 
                            = (0x0000ffffU & ((IData)(vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__offset_r) 
                                              + (0x000000ffU 
                                                 & (vlSelfRef.milan_datapath__DOT__csr__DOT__maap_ctrl 
                                                    >> 8U))));
                        __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__210__req_s 
                            = (0x0000ffffU & (IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__210__start_a));
                        __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__210__req_e 
                            = (0x0000ffffU & ((IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__210__req_s) 
                                              + (IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__210__cnt_a)));
                        if ((((IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__210__our_s) 
                              >= (IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__210__req_s)) 
                             & ((IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__210__our_s) 
                                <= (IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__210__req_e)))) {
                            __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__210__c_s 
                                = __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__210__our_s;
                            __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__210__c_c 
                                = (0x0000ffffU & ((
                                                   ((IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__210__our_e) 
                                                    < (IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__210__req_e))
                                                    ? (IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__210__our_e)
                                                    : (IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__210__req_e)) 
                                                  - (IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__210__our_s)));
                        } else {
                            __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__210__c_s 
                                = __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__210__req_s;
                            __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__210__c_c 
                                = (0x0000ffffU & ((
                                                   ((IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__210__req_e) 
                                                    < (IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__210__our_e))
                                                    ? (IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__210__req_e)
                                                    : (IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__210__our_e)) 
                                                  - (IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__210__req_s)));
                        }
                        vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT____VlemCall_23__conflict_range 
                            = (((IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__210__c_s) 
                                << 0x00000010U) | (IData)(__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_range__210__c_c));
                        vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_conf_cnt_r 
                            = (0x0000ffffU & vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT____VlemCall_23__conflict_range);
                    }
                }
            } else if (((2U == (IData)(vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rx_msg_r)) 
                        || (3U == (IData)(vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rx_msg_r)))) {
                __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_hit__211__cnt_a 
                    = vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rx_conf_cnt_r;
                __Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__conflict_hit__211__start_a 
                    = vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rx_conf_start_r;
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
                vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT____VlemCall_24__conflict_hit 
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
                if (vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT____VlemCall_24__conflict_hit) {
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
                    vlSelfRef.__Vdly__milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__state_r = 1U;
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
            if ((0x013fU >= (0x000001ffU & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__sink_r) 
                                            << 6U)))) {
                VL_ASSIGNSEL_WQ(320, 64, (0x000001ffU 
                                          & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__sink_r) 
                                             << 6U)), vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__bound_sid_r, vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__sid_f_r);
            }
        }
        if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__lstn_disc_disarm_w) {
            if ((0x013fU >= (0x000001ffU & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__sink_r) 
                                            << 6U)))) {
                VL_ASSIGNSEL_WQ(320, 64, (0x000001ffU 
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
                    vlSelfRef.__VdlyVal__milan_datapath__DOT__csr__DOT__snap_shadow_r__v0 
                        = vlSelfRef.milan_datapath__DOT__tctx_rd_data_w;
                    vlSelfRef.__VdlySet__milan_datapath__DOT__csr__DOT__snap_shadow_r__v0 = 1U;
                    vlSelfRef.milan_datapath__DOT__csr__DOT__snap_rden_r = 0U;
                    vlSelfRef.__Vdly__milan_datapath__DOT__csr__DOT__snap_req_r = 0U;
                    vlSelfRef.__Vdly__milan_datapath__DOT__csr__DOT__snap_st_r = 1U;
                    vlSelfRef.__VdlyVal__milan_datapath__DOT__csr__DOT__snap_shadow_r__v1 
                        = (((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__snap_srp9_w) 
                            << 0x00000013U) | ((((2U 
                                                  & (((IData)(vlSelfRef.milan_datapath__DOT__aaf_stream_en_w) 
                                                      >> 
                                                      (7U 
                                                       & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__snap_idx_r))) 
                                                     << 1U)) 
                                                 | (1U 
                                                    & (((((2U 
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
                                                                    & vlSelfRef.milan_datapath__DOT__csr__DOT__lwsrp_ctrl))))) 
                                                       >> 
                                                       (7U 
                                                        & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__snap_idx_r))))) 
                                                << 2U) 
                                               | (2U 
                                                  & (((0x0000000fU 
                                                       & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__declaring_r)) 
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
                        vlSelfRef.__VdlyVal__milan_datapath__DOT__csr__DOT__snap_shadow_r__v2 
                            = vlSelfRef.milan_datapath__DOT__lctx_rd_data_w;
                        vlSelfRef.__VdlySet__milan_datapath__DOT__csr__DOT__snap_shadow_r__v2 = 1U;
                        vlSelfRef.__VdlyVal__milan_datapath__DOT__csr__DOT__snap_shadow_r__v3 
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
                        vlSelfRef.__VdlyVal__milan_datapath__DOT__csr__DOT__snap_shadow_r__v4 
                            = vlSelfRef.milan_datapath__DOT__lctx_rd_data_w;
                        vlSelfRef.__VdlyDim0__milan_datapath__DOT__csr__DOT__snap_shadow_r__v4 
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
                      : ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_182) 
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
                    & (vlSelfRef.s_axi_wdata & ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_181) 
                                                & (0x0804U 
                                                   == (IData)(vlSelfRef.s_axi_awaddr)))))) {
            vlSelfRef.milan_datapath__DOT__csr__DOT__snap_busy_r = 1U;
            vlSelfRef.milan_datapath__DOT__csr__DOT__snap_dir_r 
                = vlSelfRef.milan_datapath__DOT__csr__DOT__strm_dir_r;
            vlSelfRef.milan_datapath__DOT__csr__DOT__snap_idx_r 
                = vlSelfRef.milan_datapath__DOT__csr__DOT__strm_idx_r;
            if ((4U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__strm_idx_r))) {
                if ((0U == (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__strm_idx_r))) {
                    if (vlSelfRef.milan_datapath__DOT__csr__DOT__strm_dir_r) {
                        vlSelfRef.__VdlyVal__milan_datapath__DOT__csr__DOT__snap_shadow_r__v5 
                            = ((0x0ff80000U & (vlSelfRef.milan_datapath__DOT____Vcellinp__csr__i_lwsrp_status 
                                               << 0x00000013U)) 
                               | ((((IData)(vlSelfRef.milan_datapath__DOT__aaf_gate) 
                                    << 3U) | (4U & 
                                              (vlSelfRef.milan_datapath__DOT__csr__DOT__acmp_lobs 
                                               << 2U))) 
                                  | (2U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__declaring_r) 
                                           << 1U))));
                        vlSelfRef.__VdlySet__milan_datapath__DOT__csr__DOT__snap_shadow_r__v5 = 1U;
                        vlSelfRef.__VdlyVal__milan_datapath__DOT__csr__DOT__snap_shadow_r__v16 
                            = vlSelfRef.milan_datapath__DOT__aaf_frames_w;
                    } else {
                        vlSelfRef.__VdlyVal__milan_datapath__DOT__csr__DOT__snap_shadow_r__v17 
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
                        vlSelfRef.__VdlyVal__milan_datapath__DOT__csr__DOT__snap_shadow_r__v18 
                            = vlSelfRef.milan_datapath__DOT____Vcellinp__csr__i_avtprx_cnt10[0U];
                        vlSelfRef.__VdlyVal__milan_datapath__DOT__csr__DOT__snap_shadow_r__v19 
                            = vlSelfRef.milan_datapath__DOT____Vcellinp__csr__i_avtprx_cnt10[1U];
                        vlSelfRef.__VdlyVal__milan_datapath__DOT__csr__DOT__snap_shadow_r__v20 
                            = vlSelfRef.milan_datapath__DOT____Vcellinp__csr__i_avtprx_cnt10[2U];
                        vlSelfRef.__VdlyVal__milan_datapath__DOT__csr__DOT__snap_shadow_r__v21 
                            = vlSelfRef.milan_datapath__DOT____Vcellinp__csr__i_avtprx_cnt10[3U];
                        vlSelfRef.__VdlyVal__milan_datapath__DOT__csr__DOT__snap_shadow_r__v22 
                            = vlSelfRef.milan_datapath__DOT____Vcellinp__csr__i_avtprx_cnt10[4U];
                        vlSelfRef.__VdlyVal__milan_datapath__DOT__csr__DOT__snap_shadow_r__v23 
                            = vlSelfRef.milan_datapath__DOT____Vcellinp__csr__i_avtprx_cnt10[5U];
                        vlSelfRef.__VdlyVal__milan_datapath__DOT__csr__DOT__snap_shadow_r__v24 
                            = vlSelfRef.milan_datapath__DOT____Vcellinp__csr__i_avtprx_cnt10[6U];
                        vlSelfRef.__VdlyVal__milan_datapath__DOT__csr__DOT__snap_shadow_r__v25 
                            = vlSelfRef.milan_datapath__DOT____Vcellinp__csr__i_avtprx_cnt10[7U];
                        vlSelfRef.__VdlyVal__milan_datapath__DOT__csr__DOT__snap_shadow_r__v26 
                            = vlSelfRef.milan_datapath__DOT____Vcellinp__csr__i_avtprx_cnt10[8U];
                        vlSelfRef.__VdlyVal__milan_datapath__DOT__csr__DOT__snap_shadow_r__v27 
                            = vlSelfRef.milan_datapath__DOT____Vcellinp__csr__i_avtprx_cnt10[9U];
                        vlSelfRef.__VdlyVal__milan_datapath__DOT__csr__DOT__snap_shadow_r__v28 
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
                                ? ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_130) 
                                   & ((0x0000ffffU 
                                       & ((IData)(1U) 
                                          + vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_last_r[8U])) 
                                      == (0x0000ffffU 
                                          & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__cap_val_w[8U])))
                                : (((1U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_type_r)) 
                                    | (2U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_type_r)))
                                    ? ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_281) 
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
                                           & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_281))
                                        : ((4U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_type_r)) 
                                           & ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_130) 
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
                                          & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_snk_fail_code_w)))
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
                        : ((0x9fU >= (0x000000e0U & 
                                      (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__hb_addr_r 
                                       << 5U))) ? vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__lat_r
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
                                                  ((0x03000000U 
                                                    & (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__fourpack_r) 
                                                        << 0x00000010U) 
                                                       & ((- (IData)(
                                                                     (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rec_valid_r) 
                                                                       >> 4U) 
                                                                      & ((1U 
                                                                          == 
                                                                          (0x0000000fU 
                                                                           & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_r 
                                                                              >> 0x00000010U))) 
                                                                         | ((2U 
                                                                             == 
                                                                             (0x0000000fU 
                                                                              & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_r 
                                                                                >> 0x00000010U))) 
                                                                            | ((3U 
                                                                                == 
                                                                                (0x0000000fU 
                                                                                & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_r 
                                                                                >> 0x00000010U))) 
                                                                               | ((4U 
                                                                                == 
                                                                                (0x0000000fU 
                                                                                & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_r 
                                                                                >> 0x00000010U))) 
                                                                                | ((5U 
                                                                                == 
                                                                                (0x0000000fU 
                                                                                & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_r 
                                                                                >> 0x00000010U))) 
                                                                                | ((9U 
                                                                                == 
                                                                                (0x0000000fU 
                                                                                & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_r 
                                                                                >> 0x00000010U))) 
                                                                                | (0x0aU 
                                                                                == 
                                                                                (0x0000000fU 
                                                                                & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_r 
                                                                                >> 0x00000010U)))))))))))) 
                                                          << 0x00000018U))) 
                                                   | ((((0x0000000cU 
                                                         & (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__fourpack_r) 
                                                             >> 4U) 
                                                            & ((- (IData)(
                                                                          (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rec_valid_r) 
                                                                            >> 3U) 
                                                                           & ((1U 
                                                                               == 
                                                                               (0x0000000fU 
                                                                                & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_r 
                                                                                >> 0x0000000cU))) 
                                                                              | ((2U 
                                                                                == 
                                                                                (0x0000000fU 
                                                                                & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_r 
                                                                                >> 0x0000000cU))) 
                                                                                | ((3U 
                                                                                == 
                                                                                (0x0000000fU 
                                                                                & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_r 
                                                                                >> 0x0000000cU))) 
                                                                                | ((4U 
                                                                                == 
                                                                                (0x0000000fU 
                                                                                & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_r 
                                                                                >> 0x0000000cU))) 
                                                                                | ((5U 
                                                                                == 
                                                                                (0x0000000fU 
                                                                                & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_r 
                                                                                >> 0x0000000cU))) 
                                                                                | ((9U 
                                                                                == 
                                                                                (0x0000000fU 
                                                                                & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_r 
                                                                                >> 0x0000000cU))) 
                                                                                | (0x0aU 
                                                                                == 
                                                                                (0x0000000fU 
                                                                                & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_r 
                                                                                >> 0x0000000cU)))))))))))) 
                                                               << 2U))) 
                                                        | (3U 
                                                           & (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__fourpack_r) 
                                                               >> 4U) 
                                                              & (- (IData)(
                                                                           (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rec_valid_r) 
                                                                             >> 2U) 
                                                                            & ((1U 
                                                                                == 
                                                                                (0x0000000fU 
                                                                                & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_r 
                                                                                >> 8U))) 
                                                                               | ((2U 
                                                                                == 
                                                                                (0x0000000fU 
                                                                                & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_r 
                                                                                >> 8U))) 
                                                                                | ((3U 
                                                                                == 
                                                                                (0x0000000fU 
                                                                                & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_r 
                                                                                >> 8U))) 
                                                                                | ((4U 
                                                                                == 
                                                                                (0x0000000fU 
                                                                                & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_r 
                                                                                >> 8U))) 
                                                                                | ((5U 
                                                                                == 
                                                                                (0x0000000fU 
                                                                                & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_r 
                                                                                >> 8U))) 
                                                                                | ((9U 
                                                                                == 
                                                                                (0x0000000fU 
                                                                                & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_r 
                                                                                >> 8U))) 
                                                                                | (0x0aU 
                                                                                == 
                                                                                (0x0000000fU 
                                                                                & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_r 
                                                                                >> 8U))))))))))))))) 
                                                       << 0x00000014U) 
                                                      | ((0x000c0000U 
                                                          & (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__fourpack_r) 
                                                              << 0x00000010U) 
                                                             & ((- (IData)(
                                                                           (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rec_valid_r) 
                                                                             >> 1U) 
                                                                            & ((1U 
                                                                                == 
                                                                                (0x0000000fU 
                                                                                & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_r 
                                                                                >> 4U))) 
                                                                               | ((2U 
                                                                                == 
                                                                                (0x0000000fU 
                                                                                & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_r 
                                                                                >> 4U))) 
                                                                                | ((3U 
                                                                                == 
                                                                                (0x0000000fU 
                                                                                & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_r 
                                                                                >> 4U))) 
                                                                                | ((4U 
                                                                                == 
                                                                                (0x0000000fU 
                                                                                & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_r 
                                                                                >> 4U))) 
                                                                                | ((5U 
                                                                                == 
                                                                                (0x0000000fU 
                                                                                & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_r 
                                                                                >> 4U))) 
                                                                                | ((9U 
                                                                                == 
                                                                                (0x0000000fU 
                                                                                & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_r 
                                                                                >> 4U))) 
                                                                                | (0x0aU 
                                                                                == 
                                                                                (0x0000000fU 
                                                                                & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_r 
                                                                                >> 4U)))))))))))) 
                                                                << 0x00000012U))) 
                                                         | ((0x00030000U 
                                                             & (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__fourpack_r) 
                                                                 & (- (IData)(
                                                                              ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rec_valid_r) 
                                                                               & ((1U 
                                                                                == 
                                                                                (0x0000000fU 
                                                                                & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_r)) 
                                                                                | ((2U 
                                                                                == 
                                                                                (0x0000000fU 
                                                                                & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_r)) 
                                                                                | ((3U 
                                                                                == 
                                                                                (0x0000000fU 
                                                                                & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_r)) 
                                                                                | ((4U 
                                                                                == 
                                                                                (0x0000000fU 
                                                                                & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_r)) 
                                                                                | ((5U 
                                                                                == 
                                                                                (0x0000000fU 
                                                                                & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_r)) 
                                                                                | ((9U 
                                                                                == 
                                                                                (0x0000000fU 
                                                                                & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_r)) 
                                                                                | (0x0aU 
                                                                                == 
                                                                                (0x0000000fU 
                                                                                & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_r)))))))))))) 
                                                                << 0x00000010U)) 
                                                            | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__active_r))))))
                                               : ((1U 
                                                   & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__hb_addr_r)
                                                   ? 
                                                  (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_tk_decl_state_w) 
                                                    << 0x00000010U) 
                                                   | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_out_w))
                                                   : 
                                                  (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__adm_admitted_w) 
                                                    << 0x00000018U) 
                                                   | (((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_234) 
                                                       << 0x00000014U) 
                                                      | ((((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_235) 
                                                           << 0x00000013U) 
                                                          | ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_236) 
                                                             << 0x00000012U)) 
                                                         | (((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_237) 
                                                             << 0x00000011U) 
                                                            | (((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_238) 
                                                                << 0x00000010U) 
                                                               | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_tk_reg_state_w))))))))
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
                                                   ? 0x05050404U
                                                   : 0x4b4c5050U))))));
    } else {
        vlSelfRef.milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__psfault_sync_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__psbusy_sync_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pf_st_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pf_idx_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pf_eid_r = 0ULL;
        vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_render__DOT__cur_r__v2 = 1U;
        vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__tdm_hold_r__v1 = 1U;
        vlSelfRef.__VdlySet__milan_datapath__DOT__pcm_route__DOT__route_r__v1 = 1U;
        vlSelfRef.__VdlySet__milan_datapath__DOT__stream_table__DOT__ovr_en_r__v1 = 1U;
        vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v16 = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_acmp_r = 0U;
        vlSelfRef.__VdlySet__milan_datapath__DOT__stream_table__DOT__ovr_sid_r__v1 = 1U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__txc_pend_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__txc_alloc_wait_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__txc_owner_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__txc_locked_r = 0U;
        vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__map_r__v1 = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__pe_pcp_r = 0U;
        vlSelfRef.__VdlySet__milan_datapath__DOT__stream_table__DOT__ovr_armed_r__v1 = 1U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__bound_hold_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_req_valid_w = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__st_tk_r[0U] = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__st_tk_r[1U] = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__st_tk_r[2U] = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__st_tk_r[3U] = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__st_tk_r[4U] = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__st_tk_vld_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__st_ls_r[0U] = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__st_ls_r[1U] = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__st_ls_r[2U] = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__st_ls_r[3U] = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__st_ls_r[4U] = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__st_ls_vld_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__st_svc_vld_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__inflight_r[0U] = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__inflight_r[1U] = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__inflight_r[2U] = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__inflight_r[3U] = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__inflight_r[4U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__inflight_vld_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__svc_drop_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__adv_startup_r = 0U;
        vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__adv_st_r__v9 = 1U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__adp_stall_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__acmp_stall_r = 0U;
        vlSelfRef.milan_datapath__DOT__media_nco__DOT__trim_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__en_q_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__ls_arm_v_w = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tk_arm_v_w = 0U;
        vlSelfRef.milan_datapath__DOT__pair_zero_fill__DOT__fed_now_r = 0U;
        vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__s_tdata_q = 0ULL;
        vlSelfRef.milan_datapath__DOT__rsp_tdata_w = 0ULL;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__aecp_sb_done_pending_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__out_emit_r = 0U;
        vlSelfRef.milan_datapath__DOT__talker_diag__DOT__mr_q_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__req_seen_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__pend_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__sk_data_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__byp_sink_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__byp_data_r[0U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__byp_data_r[1U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__byp_data_r[2U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__byp_data_r[3U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__byp_data_r[4U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__acmp_sb_done_pending_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_acmp_cnt_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_adp_cnt_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__wgrant_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__pend_dep_r = 0U;
        vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__pass_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__wgslope_r[0U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__wgslope_r[1U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__wgslope_r[2U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__wgslope_r[3U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__wgslope_r[4U] = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxf_vld_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxf_slot_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxf_drop_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__c1_proj_r[0U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__c1_proj_r[1U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__c1_proj_r[2U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__c1_proj_r[3U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__c1_proj_r[4U] = 0U;
        vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__in_frame = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__sk_addr_r = 0U;
        vlSelfRef.milan_datapath__DOT__avtprx_tv_bit = 0U;
        vlSelfRef.milan_datapath__DOT__avtprx_mreset_c = 0U;
        vlSelfRef.milan_datapath__DOT__avtprx_late_c = 0U;
        vlSelfRef.milan_datapath__DOT__avtprx_early_c = 0U;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_fed_r = 0U;
        vlSelfRef.milan_datapath__DOT__zf_slot_w = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__lsn_q_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_org_cnt_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_prev_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_lstn_reg_change_w = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__aecp_sb_id_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__acmp_sb_id_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_evt_tk_reg_w = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__amap_type_r = 0U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__b_valid = 0U;
        vlSelfRef.milan_datapath__DOT__avtprx_tu_bit = 0U;
        vlSelfRef.milan_datapath__DOT__avtprx_fsh2 = 0ULL;
        vlSelfRef.milan_datapath__DOT__mon_wire_chans_w = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_org_r = 0U;
        vlSelfRef.milan_datapath__DOT__lb_skip_cnt_w = 0U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__cmrd_armed_r = 0U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__cmrd_unsup_r = 0U;
        vlSelfRef.milan_datapath__DOT__lb_dup_cnt_w = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__vpushed_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_release_merge__DOT__pending_r = 0U;
        vlSelfRef.milan_datapath__DOT__avtprx_fsh = 0ULL;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__maap_busy_r = 0U;
        vlSelfRef.milan_datapath__DOT__avtprx_ts = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__arm_ref_r = 0U;
        vlSelfRef.milan_datapath__DOT__crf_delta_w = 0U;
        vlSelfRef.milan_datapath__DOT__avtprx_last_ts = 0U;
        vlSelfRef.milan_datapath__DOT__avtprx_last_tsd = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__rd_data_r = 0ULL;
        vlSelfRef.milan_datapath__DOT__avtprx_tu_c = 0U;
        vlSelfRef.milan_datapath__DOT__avtprx_unsupp_c = 0U;
        vlSelfRef.milan_datapath__DOT__avtprx_frx_c = 0U;
        vlSelfRef.milan_datapath__DOT__avtprx_seqmm_c = 0U;
        vlSelfRef.milan_datapath__DOT__avtprx_locked_c = 0U;
        vlSelfRef.milan_datapath__DOT__avtprx_unlocked_c = 0U;
        vlSelfRef.milan_datapath__DOT__avtprx_intr_c = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__cfg_v_r = 0U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__mac_ifg = 0x0000000cU;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__amap_index_r = 0U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__lpf_ctrl = 1U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__irq_mask = 0U;
        VL_ASSIGN_W(448, vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_parser__DOT__hdr, Vmilan_datapath__ConstPool__CONST_hb0e0ad07_0);
        vlSelfRef.milan_datapath__DOT__avtprx_b3 = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__ack_ref_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__adp_evt_valid_w = 0U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__strm_lsn0_r = 0U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__tcam_ctrl = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__adp_evt_departed_w = 0U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__mc_hi = 0U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__mc_lo = 0U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__adp_ctrl = 0x00000a00U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__crft_dmhi = 0U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__crft_dmlo = 0U;
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__evt_drop_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__clksrc_v_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__rate_v_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__ident_v_r = 0U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__crf_sidlo = 0U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__crf_sidhi = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__maap_t0_r = 0U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__crft_sidlo = 0U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__crft_sidhi = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__ptoff_v_r = 0U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__mac_ctrl = 0x00000013U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__ld_acc_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__rl_ref_r = 0U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__lwsrp_vid = 2U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__adp_midhi = 0U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__adp_idx0 = 0U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__adp_midlo = 0U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__crf_ctrl = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__adp_evt_sink_w = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__cfg_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__org_arm_valid_w = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__org_arm_cancel_w = 0U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__crft_ctrl = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__org_send_valid_w = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__org_send_slot_w = 0U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__rest_pend_r = 0U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__rest_done_r = 0U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__rest_stat_r = 0U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__rest_idx_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__org_arm_owner_w = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__org_arm_slot_w = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__org_arm_deadline_w = 0U;
        vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__parsed = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_r = 1ULL;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__seeded_r = 0U;
        vlSelfRef.milan_datapath__DOT__crf_rx__DOT__prev_mr_r = 0U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__mac_ahi = 0U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__mac_alo = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__link_guard__DOT__tx_dead_r = 0U;
        vlSelfRef.milan_datapath__DOT__link_guard__DOT__tx_alive_r = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__arm_q_slot_r = 0U;
        vlSelfRef.milan_datapath__DOT__tkd_crf_pend_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__link_guard__DOT__rx_dead_r = 0U;
        vlSelfRef.milan_datapath__DOT__link_guard__DOT__rx_alive_r = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__ptr_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__pend_avail_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__aecp_sb_slot_r = 0U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__adp_eidlo = 0U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__adp_eidhi = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__org_resend_valid_w = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__org_resend_slot_w = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__org_release_valid_w = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__cancel_pend_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__armed_r = 0U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__r_valid = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__pendexp_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__sb_prefer_aecp_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__4__KET____DOT__u_rx_slots__DOT__occupied_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__4__KET____DOT__u_rx_slots__DOT__wr_active_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__4__KET____DOT__u_rx_slots__DOT__writing_r = 0U;
        vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__4__KET____DOT__u_rx_slots__DOT__len_r__v1 = 1U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__2__KET____DOT__u_rx_slots__DOT__occupied_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__2__KET____DOT__u_rx_slots__DOT__wr_active_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__2__KET____DOT__u_rx_slots__DOT__writing_r = 0U;
        vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__2__KET____DOT__u_rx_slots__DOT__len_r__v1 = 1U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__1__KET____DOT__u_rx_slots__DOT__occupied_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__1__KET____DOT__u_rx_slots__DOT__wr_active_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__1__KET____DOT__u_rx_slots__DOT__writing_r = 0U;
        vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__1__KET____DOT__u_rx_slots__DOT__len_r__v1 = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__aecp_sb_active_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__org_release_slot_w = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__DOT__occupied_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__DOT__wr_active_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__DOT__writing_r = 0U;
        vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__DOT__len_r__v1 = 1U;
        vlSelfRef.__Vdly__milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__step_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__busy_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__acc_r = 0ULL;
        vlSelfRef.__Vdly__milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__yl_hold_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__xl1_r = 0U;
        vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__xl2_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__yl1_r = 0U;
        vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__yl2_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__xr1_r = 0U;
        vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__xr2_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__yr1_r = 0U;
        vlSelfRef.milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__yr2_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__tone_gen_media__DOT__idx_r = 0U;
        vlSelfRef.milan_datapath__DOT__tone_smp_media = 0U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__ptp_tod_rd = 0ULL;
        vlSelfRef.milan_datapath__DOT__g_aprb__DOT__aprb_subtype_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__0__KET____DOT__u_rx_slots__DOT__occupied_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__0__KET____DOT__u_rx_slots__DOT__wr_active_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__0__KET____DOT__u_rx_slots__DOT__writing_r = 0U;
        vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__0__KET____DOT__u_rx_slots__DOT__len_r__v1 = 1U;
        vlSelfRef.__VdlySet__milan_datapath__DOT__talker_diag__DOT__start_r__v5 = 1U;
        vlSelfRef.__Vdly__milan_datapath__DOT__talker_diag__DOT__seen_f_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__talker_diag__DOT__seen_tu_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__talker_diag__DOT__seen_mr_r = 0U;
        vlSelfRef.milan_datapath__DOT__tkd_dirty_p_w = 0U;
        vlSelfRef.__VdlySet__milan_datapath__DOT__talker_diag__DOT__mreset_r__v11 = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__seq_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__verdict_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__grant_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_pend_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__acmp_sb_active_r = 0U;
        vlSelfRef.milan_datapath__DOT__g_aprb__DOT__aprb_sid_r = 0ULL;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__exp_pend_r = 0U;
        vlSelfRef.milan_datapath__DOT__g_aprb__DOT__aprb_hit_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__ucancel_pend_r = 0U;
        vlSelfRef.milan_datapath__DOT__g_aprb__DOT__aprb_idx_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__per_pend_r = 0U;
        vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tf_rptr_r__v1 = 1U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tm_rr_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__cad_pend_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__need_draw_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_arm_valid_w = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_arm_cancel_w = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_arm_slot_w = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_arm_owner_w = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_arm_deadline_w = 0U;
        vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tf_rptr_r__v2 = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tm_st_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tm_sel_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__init_done_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__cad_dl_r[0U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__cad_dl_r[1U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__cad_dl_r[2U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__cad_dl_r[3U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__cad_dl_r[4U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dr_inflight_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dr_app_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_draw_req_w = 0U;
        vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tf_cnt_r__v3 = 1U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__valid_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__retried_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__await_tx_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__accept_pend_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__armed_r[0U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__armed_r[1U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__armed_r[2U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__pend_dep_evt_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__ld_pend_r = 1U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__g_pp_csr__DOT__pp_nvm_waddr_r = 0U;
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
        vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__pos_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__acmp_sb_slot_r = 0U;
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
        VL_ASSIGN_W(240, vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__da_r, Vmilan_datapath__ConstPool__CONST_h7f3586b3_0);
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_cnt_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_pend_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rla_pend_r = 0U;
        vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__lhold_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rtype_r = 0U;
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
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__i2s_hold_r = 0ULL;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vj_pend_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vl_pend_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vj_vid_r = 0ULL;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vl_vid_r = 0ULL;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vj_pend_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vl_pend_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vj_vid_r = 0ULL;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vl_vid_r = 0ULL;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__fcode_r = 0ULL;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__slope_q_r[0U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__slope_q_r[1U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__slope_q_r[2U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__slope_q_r[3U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__slope_q_r[4U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_val_r = 0U;
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
        VL_ASSIGN_W(320, vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__bound_sid_r, Vmilan_datapath__ConstPool__CONST_hab76c978_0);
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
    }
    if (vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__stg_we_w) {
        vlSelfRef.__VdlyVal__milan_datapath__DOT__aaf_packetizer__DOT__stg_r__v0 
            = (((QData)((IData)(((1U & vlSelfRef.milan_datapath__DOT__csr__DOT__chmap_ctrl)
                                  ? vlSelfRef.milan_datapath__DOT__cmap_l_w
                                  : vlSelfRef.milan_datapath__DOT__zf_l_w))) 
                << 0x00000018U) | (QData)((IData)((
                                                   (1U 
                                                    & vlSelfRef.milan_datapath__DOT__csr__DOT__chmap_ctrl)
                                                    ? vlSelfRef.milan_datapath__DOT__cmap_r_w
                                                    : vlSelfRef.milan_datapath__DOT__zf_r_w))));
        vlSelfRef.__VdlyDim0__milan_datapath__DOT__aaf_packetizer__DOT__stg_r__v0 
            = (((((IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pown_t_w) 
                  << 1U) | vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__wbank_r
                 [vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pown_t_w]) 
                << 5U) | (((IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__nsamp_r
                                   [vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pown_t_w]) 
                           << 2U) | (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__pown_o_w)));
        vlSelfRef.__VdlySet__milan_datapath__DOT__aaf_packetizer__DOT__stg_r__v0 = 1U;
    }
    if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__push_msrp_w) {
        if ((0x0bU >= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__cnt_msrp_r))) {
            vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__msrp_ram_r__v0[0U] 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__enc_ev_value_w[0U];
            vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__msrp_ram_r__v0[1U] 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__enc_ev_value_w[1U];
            vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__msrp_ram_r__v0[2U] 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__enc_ev_value_w[2U];
            vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__msrp_ram_r__v0[3U] 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__enc_ev_value_w[3U];
            vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__msrp_ram_r__v0[4U] 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__enc_ev_value_w[4U];
            vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__msrp_ram_r__v0[5U] 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__enc_ev_value_w[5U];
            vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__msrp_ram_r__v0[6U] 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__enc_ev_value_w[6U];
            vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__msrp_ram_r__v0[7U] 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__enc_ev_value_w[7U];
            vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__msrp_ram_r__v0[8U] 
                = ((0x1fff0000U & vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__msrp_ram_r__v0[8U]) 
                   | (0x1fffffffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__enc_ev_value_w[8U]));
            vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__msrp_ram_r__v0[8U] 
                = ((0x0000ffffU & vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__msrp_ram_r__v0[8U]) 
                   | (0x1fffffffU & (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__enc_ev_type_w) 
                                      << 0x00000015U) 
                                     | (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__enc_ev_event_w) 
                                         << 0x00000012U) 
                                        | (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_domain__DOT__q0_valid_r)
                                             ? 0U : 
                                            ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__vlan_ev_valid_w)
                                              ? 0U : 
                                             ((2U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__walk_r))
                                               ? 0U
                                               : ((2U 
                                                   == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__walk_r))
                                                   ? (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__push_fp_r)
                                                   : 0U)))) 
                                           << 0x00000010U)))));
            vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__msrp_ram_r__v0 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__cnt_msrp_r;
            vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__msrp_ram_r__v0 = 1U;
        }
    }
    if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tf_push_w))) {
        vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tf_ram_r__v0 
            = (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tk_arm_cancel_w)) 
                << 0x0000002fU) | (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tk_arm_slot_w)) 
                                    << 0x00000028U) 
                                   | (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tk_arm_owner_w)) 
                                       << 0x00000020U) 
                                      | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tk_arm_dl_w)))));
        vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tf_ram_r__v0 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tf_wptr_r[0U];
        vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tf_ram_r__v0 = 1U;
    }
    if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tf_push_w))) {
        vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tf_ram_r__v1 
            = (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__ls_arm_cancel_w)) 
                << 0x0000002fU) | (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__ls_arm_slot_w)) 
                                    << 0x00000028U) 
                                   | (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__ls_arm_owner_w)) 
                                       << 0x00000020U) 
                                      | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__ls_arm_dl_w)))));
        vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tf_ram_r__v1 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tf_wptr_r[1U];
        vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tf_ram_r__v1 = 1U;
    }
    if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__wr_en_r) {
        vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__rows_r__v0[0U] 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__wr_row_r[0U];
        vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__rows_r__v0[1U] 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__wr_row_r[1U];
        vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__rows_r__v0[2U] 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__wr_row_r[2U];
        vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__rows_r__v0[3U] 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__wr_row_r[3U];
        vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__rows_r__v0 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__wr_ix_r;
        vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__rows_r__v0 = 1U;
    }
    if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__push_w) {
        vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__mem_r__v0[0U] 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_normalizer__DOT__txn_r[0U];
        vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__mem_r__v0[1U] 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_normalizer__DOT__txn_r[1U];
        vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__mem_r__v0[2U] 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_normalizer__DOT__txn_r[2U];
        vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__mem_r__v0[3U] 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_normalizer__DOT__txn_r[3U];
        vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__mem_r__v0[4U] 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_normalizer__DOT__txn_r[4U];
        vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__mem_r__v0[5U] 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_normalizer__DOT__txn_r[5U];
        vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__mem_r__v0[6U] 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_normalizer__DOT__txn_r[6U];
        vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__mem_r__v0[7U] 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_normalizer__DOT__txn_r[7U];
        vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__mem_r__v0[8U] 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_normalizer__DOT__txn_r[8U];
        vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__mem_r__v0[9U] 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_normalizer__DOT__txn_r[9U];
        vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__mem_r__v0[10U] 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_normalizer__DOT__txn_r[10U];
        vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__mem_r__v0[11U] 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_normalizer__DOT__txn_r[11U];
        vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__mem_r__v0[12U] 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_normalizer__DOT__txn_r[12U];
        vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__mem_r__v0 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__wr_ptr_r;
        vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__mem_r__v0 = 1U;
    }
    if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_acmp_q__DOT__push_w) {
        vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_acmp_q__DOT__mem_r__v0[0U] 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_normalizer__DOT__txn_r[0U];
        vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_acmp_q__DOT__mem_r__v0[1U] 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_normalizer__DOT__txn_r[1U];
        vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_acmp_q__DOT__mem_r__v0[2U] 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_normalizer__DOT__txn_r[2U];
        vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_acmp_q__DOT__mem_r__v0[3U] 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_normalizer__DOT__txn_r[3U];
        vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_acmp_q__DOT__mem_r__v0[4U] 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_normalizer__DOT__txn_r[4U];
        vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_acmp_q__DOT__mem_r__v0[5U] 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_normalizer__DOT__txn_r[5U];
        vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_acmp_q__DOT__mem_r__v0[6U] 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_normalizer__DOT__txn_r[6U];
        vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_acmp_q__DOT__mem_r__v0[7U] 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_normalizer__DOT__txn_r[7U];
        vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_acmp_q__DOT__mem_r__v0[8U] 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_normalizer__DOT__txn_r[8U];
        vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_acmp_q__DOT__mem_r__v0[9U] 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_normalizer__DOT__txn_r[9U];
        vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_acmp_q__DOT__mem_r__v0[10U] 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_normalizer__DOT__txn_r[10U];
        vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_acmp_q__DOT__mem_r__v0[11U] 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_normalizer__DOT__txn_r[11U];
        vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_acmp_q__DOT__mem_r__v0[12U] 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_normalizer__DOT__txn_r[12U];
        vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_acmp_q__DOT__mem_r__v0 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_acmp_q__DOT__wr_ptr_r;
        vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_acmp_q__DOT__mem_r__v0 = 1U;
    }
    if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_adp_q__DOT__push_w) {
        vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_adp_q__DOT__mem_r__v0[0U] 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_normalizer__DOT__txn_r[0U];
        vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_adp_q__DOT__mem_r__v0[1U] 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_normalizer__DOT__txn_r[1U];
        vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_adp_q__DOT__mem_r__v0[2U] 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_normalizer__DOT__txn_r[2U];
        vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_adp_q__DOT__mem_r__v0[3U] 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_normalizer__DOT__txn_r[3U];
        vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_adp_q__DOT__mem_r__v0[4U] 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_normalizer__DOT__txn_r[4U];
        vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_adp_q__DOT__mem_r__v0[5U] 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_normalizer__DOT__txn_r[5U];
        vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_adp_q__DOT__mem_r__v0[6U] 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_normalizer__DOT__txn_r[6U];
        vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_adp_q__DOT__mem_r__v0[7U] 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_normalizer__DOT__txn_r[7U];
        vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_adp_q__DOT__mem_r__v0[8U] 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_normalizer__DOT__txn_r[8U];
        vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_adp_q__DOT__mem_r__v0[9U] 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_normalizer__DOT__txn_r[9U];
        vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_adp_q__DOT__mem_r__v0[10U] 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_normalizer__DOT__txn_r[10U];
        vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_adp_q__DOT__mem_r__v0[11U] 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_normalizer__DOT__txn_r[11U];
        vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_adp_q__DOT__mem_r__v0[12U] 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_normalizer__DOT__txn_r[12U];
        vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_adp_q__DOT__mem_r__v0 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_adp_q__DOT__wr_ptr_r;
        vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_adp_q__DOT__mem_r__v0 = 1U;
    }
    if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_maap_q__DOT__push_w) {
        vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_maap_q__DOT__mem_r__v0[0U] 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_normalizer__DOT__txn_r[0U];
        vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_maap_q__DOT__mem_r__v0[1U] 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_normalizer__DOT__txn_r[1U];
        vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_maap_q__DOT__mem_r__v0[2U] 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_normalizer__DOT__txn_r[2U];
        vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_maap_q__DOT__mem_r__v0[3U] 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_normalizer__DOT__txn_r[3U];
        vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_maap_q__DOT__mem_r__v0[4U] 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_normalizer__DOT__txn_r[4U];
        vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_maap_q__DOT__mem_r__v0[5U] 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_normalizer__DOT__txn_r[5U];
        vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_maap_q__DOT__mem_r__v0[6U] 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_normalizer__DOT__txn_r[6U];
        vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_maap_q__DOT__mem_r__v0[7U] 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_normalizer__DOT__txn_r[7U];
        vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_maap_q__DOT__mem_r__v0[8U] 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_normalizer__DOT__txn_r[8U];
        vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_maap_q__DOT__mem_r__v0[9U] 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_normalizer__DOT__txn_r[9U];
        vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_maap_q__DOT__mem_r__v0[10U] 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_normalizer__DOT__txn_r[10U];
        vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_maap_q__DOT__mem_r__v0[11U] 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_normalizer__DOT__txn_r[11U];
        vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_maap_q__DOT__mem_r__v0[12U] 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_normalizer__DOT__txn_r[12U];
        vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_maap_q__DOT__mem_r__v0 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_maap_q__DOT__wr_ptr_r;
        vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_maap_q__DOT__mem_r__v0 = 1U;
    }
    if ((0x0bU >= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__rd_idx_r))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__mvrp_q_r 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__mvrp_ram_r
            [vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__rd_idx_r];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__msrp_q_r[0U] 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__msrp_ram_r
            [vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__rd_idx_r][0U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__msrp_q_r[1U] 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__msrp_ram_r
            [vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__rd_idx_r][1U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__msrp_q_r[2U] 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__msrp_ram_r
            [vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__rd_idx_r][2U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__msrp_q_r[3U] 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__msrp_ram_r
            [vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__rd_idx_r][3U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__msrp_q_r[4U] 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__msrp_ram_r
            [vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__rd_idx_r][4U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__msrp_q_r[5U] 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__msrp_ram_r
            [vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__rd_idx_r][5U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__msrp_q_r[6U] 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__msrp_ram_r
            [vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__rd_idx_r][6U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__msrp_q_r[7U] 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__msrp_ram_r
            [vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__rd_idx_r][7U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__msrp_q_r[8U] 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__msrp_ram_r
            [vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__rd_idx_r][8U];
    } else {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__mvrp_q_r = 0U;
        VL_ASSIGN_W(285, vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__msrp_q_r, Vmilan_datapath__ConstPool__CONST_h11ab053c_0);
    }
    if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_maap_q__DOT__rd_en_w) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_maap_q__DOT__out_data_r[0U] 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_maap_q__DOT__mem_r
            [vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_maap_q__DOT__rd_ptr_r][0U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_maap_q__DOT__out_data_r[1U] 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_maap_q__DOT__mem_r
            [vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_maap_q__DOT__rd_ptr_r][1U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_maap_q__DOT__out_data_r[2U] 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_maap_q__DOT__mem_r
            [vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_maap_q__DOT__rd_ptr_r][2U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_maap_q__DOT__out_data_r[3U] 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_maap_q__DOT__mem_r
            [vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_maap_q__DOT__rd_ptr_r][3U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_maap_q__DOT__out_data_r[4U] 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_maap_q__DOT__mem_r
            [vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_maap_q__DOT__rd_ptr_r][4U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_maap_q__DOT__out_data_r[5U] 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_maap_q__DOT__mem_r
            [vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_maap_q__DOT__rd_ptr_r][5U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_maap_q__DOT__out_data_r[6U] 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_maap_q__DOT__mem_r
            [vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_maap_q__DOT__rd_ptr_r][6U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_maap_q__DOT__out_data_r[7U] 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_maap_q__DOT__mem_r
            [vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_maap_q__DOT__rd_ptr_r][7U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_maap_q__DOT__out_data_r[8U] 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_maap_q__DOT__mem_r
            [vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_maap_q__DOT__rd_ptr_r][8U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_maap_q__DOT__out_data_r[9U] 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_maap_q__DOT__mem_r
            [vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_maap_q__DOT__rd_ptr_r][9U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_maap_q__DOT__out_data_r[10U] 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_maap_q__DOT__mem_r
            [vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_maap_q__DOT__rd_ptr_r][10U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_maap_q__DOT__out_data_r[11U] 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_maap_q__DOT__mem_r
            [vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_maap_q__DOT__rd_ptr_r][11U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_maap_q__DOT__out_data_r[12U] 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_maap_q__DOT__mem_r
            [vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_maap_q__DOT__rd_ptr_r][12U];
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_decoder__DOT__tp_rdata_r 
        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_decoder__DOT__tp_ram
        [(0x000003ffU & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_decoder__DOT__tp_rd_byte_r) 
                         + ((0x0dU == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_decoder__DOT__state_r)) 
                            & (2U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_decoder__DOT__tp_rd_dig_r)))))];
    if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__rd_fire_w) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__od_last_r 
            = (1U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__mrp_mem_r
                     [(0x0000003fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__rptr_r))] 
                     >> 8U));
    }
    vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__under_sync_r 
        = vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__under_meta_r;
    if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__rec_re_w) {
        if ((4U >= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__rec_raddr_w))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__rec_q_r[0U] 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__rec_ram_r
                [vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__rec_raddr_w][0U];
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__rec_q_r[1U] 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__rec_ram_r
                [vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__rec_raddr_w][1U];
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__rec_q_r[2U] 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__rec_ram_r
                [vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__rec_raddr_w][2U];
        } else {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__rec_q_r[0U] = 0U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__rec_q_r[1U] = 0U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__rec_q_r[2U] = 0U;
        }
    }
    vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__s_tready_q 
        = vlSelfRef.axis_resetn;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__sp_ctrl_rvalid_r 
        = ((IData)(vlSelfRef.axis_resetn) && (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__sp_ctrl_req_w));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__sp_trace_rvalid_r 
        = ((IData)(vlSelfRef.axis_resetn) && (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__trc_rd_en_w));
    if ((1U & (~ (IData)(vlSelfRef.axis_resetn)))) {
        vlSelfRef.milan_datapath__DOT__csr__DOT__acmp_flags_q_r = 0U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__acmp_sid_q_r = 0ULL;
        vlSelfRef.milan_datapath__DOT__csr__DOT__acmp_dmac_q_r = 0ULL;
        vlSelfRef.milan_datapath__DOT__csr__DOT__acmp_ctlr_q_r = 0ULL;
        vlSelfRef.milan_datapath__DOT__csr__DOT__acmp_tuid_q_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__offset_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__def_conf_start_r = 0ULL;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__def_req_cnt_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__def_da_r = 0ULL;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__def_req_start_r = 0ULL;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__def_conf_cnt_r = 0U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__adp_disc_seen_cnt_r = 0U;
    }
    vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__s_tvalid_q 
        = ((IData)(vlSelfRef.axis_resetn) && (IData)(vlSelfRef.s_axis_mac_rx_tvalid));
    if ((3U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__rx_st_r))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__disc_rec_q_r 
            = ((4U >= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__sink_r))
                ? vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__disc_rec_r
               [vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__sink_r]
                : 0ULL);
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__enable_q_r 
        = ((IData)(vlSelfRef.axis_resetn) && (IData)(vlSelfRef.milan_datapath__DOT____Vcellinp__pp_shadow__enable_i));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__out_valid_r 
        = ((IData)(vlSelfRef.axis_resetn) && (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__rd_fire_w));
    vlSelfRef.milan_datapath__DOT__crf_rx__DOT__en_q 
        = ((IData)(vlSelfRef.axis_resetn) && (IData)(vlSelfRef.milan_datapath__DOT____Vcellinp__crf_rx__en_i));
    vlSelfRef.milan_datapath__DOT__zf_pv_w = ((IData)(vlSelfRef.axis_resetn) 
                                              && ((IData)(vlSelfRef.milan_datapath__DOT__aafcap_pv_w) 
                                                  || Vmilan_datapath__ConstPool__TABLE_h8665d168_0
                                                  [vlSelfRef.milan_datapath__DOT__pair_zero_fill__DOT__pend_r]));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__byp_v_r 
        = ((IData)(vlSelfRef.axis_resetn) && (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__wr_en_w));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_domain__DOT__link_q_r 
        = ((IData)(vlSelfRef.axis_resetn) && (IData)(vlSelfRef.milan_datapath__DOT__eff_link_w));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__c1_v_r 
        = ((IData)(vlSelfRef.axis_resetn) && (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__cap_active_w));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__link_q_r 
        = ((IData)(vlSelfRef.axis_resetn) & (IData)(vlSelfRef.milan_datapath__DOT__eff_link_w));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__backed_r 
        = ((IData)(vlSelfRef.axis_resetn) && (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__backed_n_w));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__rd_pend_r 
        = ((IData)(vlSelfRef.axis_resetn) && ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT____Vcellinp__u_dyn__st_req_i) 
                                              & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__st_we_w))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__dirty_live_r 
        = ((IData)(vlSelfRef.axis_resetn) && (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__dirty_live_n_w));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__dirty_cap_r 
        = ((IData)(vlSelfRef.axis_resetn) && (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__dirty_cap_n_w));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__mut_defer_r 
        = ((IData)(vlSelfRef.axis_resetn) & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__nvm_req_w) 
                                             & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__mut_req_w) 
                                                & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__gnt_now_w)) 
                                                   & (0U 
                                                      == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__st_r))))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__p2_en_r 
        = ((IData)(vlSelfRef.axis_resetn) && (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__p1_en_r));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__arm_q_valid_r 
        = ((IData)(vlSelfRef.axis_resetn) && (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tmr_arm_valid_w));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__open_r[0U] 
        = ((vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__open_r[0U] 
            & vlSelfRef.__VdlyMask__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__open_r[0U]) 
           | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__open_r[0U] 
              & (~ vlSelfRef.__VdlyMask__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__open_r[0U])));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__open_r[1U] 
        = ((vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__open_r[1U] 
            & vlSelfRef.__VdlyMask__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__open_r[1U]) 
           | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__open_r[1U] 
              & (~ vlSelfRef.__VdlyMask__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__open_r[1U])));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__open_r[2U] 
        = ((vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__open_r[2U] 
            & vlSelfRef.__VdlyMask__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__open_r[2U]) 
           | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__open_r[2U] 
              & (~ vlSelfRef.__VdlyMask__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__open_r[2U])));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__open_r[3U] 
        = ((vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__open_r[3U] 
            & vlSelfRef.__VdlyMask__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__open_r[3U]) 
           | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__open_r[3U] 
              & (~ vlSelfRef.__VdlyMask__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__open_r[3U])));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__open_r[4U] 
        = ((vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__open_r[4U] 
            & vlSelfRef.__VdlyMask__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__open_r[4U]) 
           | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__open_r[4U] 
              & (~ vlSelfRef.__VdlyMask__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__open_r[4U])));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__open_r[5U] 
        = ((vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__open_r[5U] 
            & vlSelfRef.__VdlyMask__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__open_r[5U]) 
           | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__open_r[5U] 
              & (~ vlSelfRef.__VdlyMask__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__open_r[5U])));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__open_r[6U] 
        = ((vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__open_r[6U] 
            & vlSelfRef.__VdlyMask__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__open_r[6U]) 
           | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__open_r[6U] 
              & (~ vlSelfRef.__VdlyMask__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__open_r[6U])));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__open_r[7U] 
        = ((vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__open_r[7U] 
            & vlSelfRef.__VdlyMask__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__open_r[7U]) 
           | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__open_r[7U] 
              & (~ vlSelfRef.__VdlyMask__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__open_r[7U])));
    VL_ASSIGN_W(256, vlSelfRef.__VdlyMask__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__open_r, Vmilan_datapath__ConstPool__CONST_h9e67c271_0);
    vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__dbgf_sync_r 
        = vlSelfRef.milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__dbgf_meta_r;
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
                                                      & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_24))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__sp_dbg_rvalid_r 
        = ((IData)(vlSelfRef.axis_resetn) && (IData)(
                                                     ((0x00010000U 
                                                       == 
                                                       (0x000f0000U 
                                                        & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__hb_addr_r)) 
                                                      & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_24))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__sp_snap_rvalid_r 
        = ((IData)(vlSelfRef.axis_resetn) && (IData)(
                                                     ((0x00020000U 
                                                       == 
                                                       (0x000f0000U 
                                                        & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__hb_addr_r)) 
                                                      & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_24))));
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
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__q_wr_r__v0) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_wr_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__chan_map_capture__DOT__q_wr_r__v0] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__chan_map_capture__DOT__q_wr_r__v0;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__q_wr_r__v1) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_wr_r[0U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__q_wr_r__v2) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_wr_r[0U] = 0U;
    }
    vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__skid_cnt_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__chan_map_capture__DOT__skid_cnt_r;
    vlSelfRef.milan_datapath__DOT__link_guard__DOT__act_sync_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__link_guard__DOT__act_sync_r;
    vlSelfRef.milan_datapath__DOT__link_guard__DOT__act_age_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__link_guard__DOT__act_age_r;
    vlSelfRef.milan_datapath__DOT__ptp_clock_validity__DOT__ival_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__ptp_clock_validity__DOT__ival_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__deb_open_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__deb_open_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__deb_cnt_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__deb_cnt_r;
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__q_rd_r__v0) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_rd_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__chan_map_capture__DOT__q_rd_r__v0] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__chan_map_capture__DOT__q_rd_r__v0;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__q_rd_r__v1) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_rd_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__chan_map_capture__DOT__q_rd_r__v1] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__chan_map_capture__DOT__q_rd_r__v1;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__q_rd_r__v2) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_rd_r[0U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__q_rd_r__v3) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_rd_r[0U] = 0U;
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__maap_stale_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__maap_stale_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__hold_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__hold_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__cap_hold_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__cap_hold_r;
    vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_tvalid_pipe_reg 
        = vlSelfRef.__Vdly__milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_tvalid_pipe_reg;
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
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r[0U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__aaf_packetizer__DOT__chans_r__v0) {
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__chans_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__aaf_packetizer__DOT__chans_r__v0] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__aaf_packetizer__DOT__chans_r__v0;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__aaf_packetizer__DOT__chans_r__v1) {
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__chans_r[0U] = 2U;
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__chans_r[1U] = 2U;
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__chans_r[2U] = 2U;
        vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__chans_r[3U] = 2U;
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
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__commit_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__commit_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__ms_div_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__ms_div_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__commit_busy_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__commit_busy_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__cap_valid_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__cap_valid_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__cap_open_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__cap_open_r;
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
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_mrp_strip__DOT__wr_tent_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_mrp_strip__DOT__wr_tent_r;
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
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__chans_q_r[0U] = 0U;
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__chans_q_r[1U] = 0U;
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__chans_q_r[2U] = 0U;
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__chans_q_r[3U] = 0U;
    }
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
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r__v0) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r__v0] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r__v0;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r__v1) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r[0U] = 0ULL;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r__v2) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r[0U] = 0ULL;
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
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_mask__v0) {
        vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_mask[vlSelfRef.__VdlyDim0__milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_mask__v0] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_mask__v0;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_key__v0) {
        vlSelfRef.milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_key[vlSelfRef.__VdlyDim0__milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_key__v0] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_key__v0;
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_r;
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
        vlSelfRef.milan_datapath__DOT__media_clock_restart__DOT__hold_r[0U] = 8U;
        vlSelfRef.milan_datapath__DOT__media_clock_restart__DOT__hold_r[1U] = 8U;
        vlSelfRef.milan_datapath__DOT__media_clock_restart__DOT__hold_r[2U] = 8U;
        vlSelfRef.milan_datapath__DOT__media_clock_restart__DOT__hold_r[3U] = 8U;
        vlSelfRef.milan_datapath__DOT__media_clock_restart__DOT__hold_r[4U] = 8U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__mapo_pref_r__v0) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__mapo_pref_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__mapo_pref_r__v0] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__mapo_pref_r__v0;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__mapi_pref_r__v0) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__mapi_pref_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__mapi_pref_r__v0] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__mapi_pref_r__v0;
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
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__mapo_len_r__v0) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__mapo_len_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__mapo_len_r__v0] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__mapo_len_r__v0;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__mapi_len_r__v0) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__mapi_len_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__mapi_len_r__v0] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__mapi_len_r__v0;
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
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_render__DOT__cur_r__v0) {
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__cur_r[__VdlyDim1__milan_datapath__DOT__chan_map_render__DOT__cur_r__v0][__VdlyDim0__milan_datapath__DOT__chan_map_render__DOT__cur_r__v0] 
            = __VdlyVal__milan_datapath__DOT__chan_map_render__DOT__cur_r__v0;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_render__DOT__cur_r__v1) {
        vlSelfRef.milan_datapath__DOT__chan_map_render__DOT__cur_r[__VdlyDim1__milan_datapath__DOT__chan_map_render__DOT__cur_r__v1][__VdlyDim0__milan_datapath__DOT__chan_map_render__DOT__cur_r__v1] 
            = __VdlyVal__milan_datapath__DOT__chan_map_render__DOT__cur_r__v1;
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
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__tdm_hold_r__v0) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__tdm_hold_r[0U] 
            = __VdlyVal__milan_datapath__DOT__chan_map_capture__DOT__tdm_hold_r__v0;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__tdm_hold_r__v1) {
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__tdm_hold_r[0U] = 0ULL;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__tdm_hold_r[1U] = 0ULL;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__tdm_hold_r[2U] = 0ULL;
        vlSelfRef.milan_datapath__DOT__chan_map_capture__DOT__tdm_hold_r[3U] = 0ULL;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pcm_route__DOT__route_r__v0) {
        vlSelfRef.milan_datapath__DOT__pcm_route__DOT__route_r[__VdlyDim0__milan_datapath__DOT__pcm_route__DOT__route_r__v0] 
            = __VdlyVal__milan_datapath__DOT__pcm_route__DOT__route_r__v0;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pcm_route__DOT__route_r__v1) {
        vlSelfRef.milan_datapath__DOT__pcm_route__DOT__route_r[0U] = 2U;
        vlSelfRef.milan_datapath__DOT__pcm_route__DOT__route_r[1U] = 0U;
        vlSelfRef.milan_datapath__DOT__pcm_route__DOT__route_r[2U] = 0U;
        vlSelfRef.milan_datapath__DOT__pcm_route__DOT__route_r[3U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__stream_table__DOT__ovr_en_r__v0) {
        vlSelfRef.milan_datapath__DOT__stream_table__DOT__ovr_en_r[__VdlyDim0__milan_datapath__DOT__stream_table__DOT__ovr_en_r__v0] 
            = __VdlyVal__milan_datapath__DOT__stream_table__DOT__ovr_en_r__v0;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__stream_table__DOT__ovr_en_r__v1) {
        vlSelfRef.milan_datapath__DOT__stream_table__DOT__ovr_en_r[0U] = 0U;
        vlSelfRef.milan_datapath__DOT__stream_table__DOT__ovr_en_r[1U] = 0U;
        vlSelfRef.milan_datapath__DOT__stream_table__DOT__ovr_en_r[2U] = 0U;
        vlSelfRef.milan_datapath__DOT__stream_table__DOT__ovr_en_r[3U] = 0U;
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
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__wptr_r[0U] = 0U;
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__wptr_r[1U] = 0U;
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__wptr_r[2U] = 0U;
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__wptr_r[3U] = 0U;
    }
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__render_setpoint__DOT__prefill_r__v0) {
        vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__converged_r[0U] = 0U;
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
}
