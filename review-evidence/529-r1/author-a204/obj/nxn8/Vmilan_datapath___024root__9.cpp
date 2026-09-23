// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vmilan_datapath.h for the primary calling header

#include "Vmilan_datapath__pch.h"

void Vmilan_datapath___024root___nba_sequent__TOP__13(Vmilan_datapath___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vmilan_datapath___024root___nba_sequent__TOP__13\n"); );
    Vmilan_datapath__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    CData/*0:0*/ milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__acmp_sb_grant_w;
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__acmp_sb_grant_w = 0;
    CData/*0:0*/ milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__aecp_sb_grant_w;
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__aecp_sb_grant_w = 0;
    CData/*0:0*/ milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT____Vcellinp__u_talker__txn_valid_i;
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT____Vcellinp__u_talker__txn_valid_i = 0;
    CData/*0:0*/ milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__sol_pend_w;
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__sol_pend_w = 0;
    CData/*7:0*/ milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__elig_w;
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__elig_w = 0;
    CData/*2:0*/ milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__selection__DOT__key_w;
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__selection__DOT__key_w = 0;
    CData/*2:0*/ milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__selection__DOT__best_w;
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__selection__DOT__best_w = 0;
    IData/*31:0*/ milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pend_after_w;
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pend_after_w = 0;
    CData/*4:0*/ milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__base_w;
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__base_w = 0;
    IData/*31:0*/ milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx;
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx = 0;
    CData/*3:0*/ __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__139__a_cls;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__139__a_cls = 0;
    SData/*15:0*/ __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__139__a_key;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__139__a_key = 0;
    CData/*3:0*/ __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__139__b_cls;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__139__b_cls = 0;
    SData/*15:0*/ __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__139__b_key;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__139__b_key = 0;
    CData/*0:0*/ __VdfgRegularize_h6e95ff9d_0_24;
    __VdfgRegularize_h6e95ff9d_0_24 = 0;
    CData/*0:0*/ __VdfgRegularize_h6e95ff9d_0_383;
    __VdfgRegularize_h6e95ff9d_0_383 = 0;
    CData/*0:0*/ __VdfgRegularize_h6e95ff9d_0_384;
    __VdfgRegularize_h6e95ff9d_0_384 = 0;
    VlWide<5>/*159:0*/ __Vtemp_1;
    // Body
    if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__valid_r) 
          >> 5U) & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT____VlemCall_0__hz_conflict))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__conflict_any_w = 1U;
    }
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__139__b_key 
        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__key_r[6U];
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__139__b_cls 
        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__cls_r[6U];
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__139__a_key 
        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__sb_adm_key_w;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__139__a_cls 
        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__sb_adm_class_w;
    {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT____VlemCall_0__hz_conflict = 0;
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__139__same_key_v = 0;
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__139__other_v = 0;
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__139__same_key_v 
            = ((IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__139__a_key) 
               == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__139__b_key));
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__139__other_v 
            = ((6U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__139__a_cls))
                ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__139__b_cls)
                : (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__139__a_cls));
        if (((1U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__139__a_cls)) 
             | (1U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__139__b_cls)))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT____VlemCall_0__hz_conflict = 1U;
            goto __Vlabel0;
        }
        if (((0U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__139__a_cls)) 
             & (0U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__139__b_cls)))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT____VlemCall_0__hz_conflict = 0U;
            goto __Vlabel0;
        }
        if (((0U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__139__a_cls)) 
             | (0U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__139__b_cls)))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT____VlemCall_0__hz_conflict 
                = vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__139__same_key_v;
            goto __Vlabel0;
        }
        if (((6U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__139__a_cls)) 
             | (6U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__139__b_cls)))) {
            vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_is_lockprot__140__c 
                = vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__139__other_v;
            vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_is_lockprot__140__Vfuncout = 0;
            vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_is_lockprot__140__Vfuncout 
                = ((((((1U == (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_is_lockprot__140__c)) 
                       | (2U == (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_is_lockprot__140__c))) 
                      | (3U == (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_is_lockprot__140__c))) 
                     | (4U == (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_is_lockprot__140__c))) 
                    | (5U == (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_is_lockprot__140__c))) 
                   | (8U == (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_is_lockprot__140__c)));
            vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__139____VlefCall_0__hz_is_lockprot 
                = vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_is_lockprot__140__Vfuncout;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT____VlemCall_0__hz_conflict 
                = ((6U == (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__139__other_v)) 
                   | (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__139____VlefCall_0__hz_is_lockprot));
            goto __Vlabel0;
        }
        if (((IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__139__a_cls) 
             == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__139__b_cls))) {
            if (((7U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__139__a_cls)) 
                 | (8U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__139__a_cls)))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT____VlemCall_0__hz_conflict = 1U;
                goto __Vlabel0;
            }
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT____VlemCall_0__hz_conflict 
                = vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__139__same_key_v;
            goto __Vlabel0;
        }
        if ((((2U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__139__a_cls)) 
              & (3U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__139__b_cls))) 
             | ((3U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__139__a_cls)) 
                & (2U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__139__b_cls))))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT____VlemCall_0__hz_conflict = 1U;
            goto __Vlabel0;
        }
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT____VlemCall_0__hz_conflict = 0U;
        __Vlabel0: ;
    }
    if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__valid_r) 
          >> 6U) & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT____VlemCall_0__hz_conflict))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__conflict_any_w = 1U;
    }
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__139__b_key 
        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__key_r[7U];
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__139__b_cls 
        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__cls_r[7U];
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__139__a_key 
        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__sb_adm_key_w;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__139__a_cls 
        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__sb_adm_class_w;
    {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT____VlemCall_0__hz_conflict = 0;
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__139__same_key_v = 0;
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__139__other_v = 0;
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__139__same_key_v 
            = ((IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__139__a_key) 
               == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__139__b_key));
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__139__other_v 
            = ((6U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__139__a_cls))
                ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__139__b_cls)
                : (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__139__a_cls));
        if (((1U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__139__a_cls)) 
             | (1U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__139__b_cls)))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT____VlemCall_0__hz_conflict = 1U;
            goto __Vlabel1;
        }
        if (((0U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__139__a_cls)) 
             & (0U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__139__b_cls)))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT____VlemCall_0__hz_conflict = 0U;
            goto __Vlabel1;
        }
        if (((0U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__139__a_cls)) 
             | (0U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__139__b_cls)))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT____VlemCall_0__hz_conflict 
                = vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__139__same_key_v;
            goto __Vlabel1;
        }
        if (((6U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__139__a_cls)) 
             | (6U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__139__b_cls)))) {
            vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_is_lockprot__140__c 
                = vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__139__other_v;
            vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_is_lockprot__140__Vfuncout = 0;
            vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_is_lockprot__140__Vfuncout 
                = ((((((1U == (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_is_lockprot__140__c)) 
                       | (2U == (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_is_lockprot__140__c))) 
                      | (3U == (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_is_lockprot__140__c))) 
                     | (4U == (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_is_lockprot__140__c))) 
                    | (5U == (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_is_lockprot__140__c))) 
                   | (8U == (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_is_lockprot__140__c)));
            vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__139____VlefCall_0__hz_is_lockprot 
                = vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_is_lockprot__140__Vfuncout;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT____VlemCall_0__hz_conflict 
                = ((6U == (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__139__other_v)) 
                   | (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__139____VlefCall_0__hz_is_lockprot));
            goto __Vlabel1;
        }
        if (((IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__139__a_cls) 
             == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__139__b_cls))) {
            if (((7U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__139__a_cls)) 
                 | (8U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__139__a_cls)))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT____VlemCall_0__hz_conflict = 1U;
                goto __Vlabel1;
            }
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT____VlemCall_0__hz_conflict 
                = vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__139__same_key_v;
            goto __Vlabel1;
        }
        if ((((2U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__139__a_cls)) 
              & (3U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__139__b_cls))) 
             | ((3U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__139__a_cls)) 
                & (2U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__139__b_cls))))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT____VlemCall_0__hz_conflict = 1U;
            goto __Vlabel1;
        }
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT____VlemCall_0__hz_conflict = 0U;
        __Vlabel1: ;
    }
    if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__valid_r) 
          >> 7U) & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT____VlemCall_0__hz_conflict))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__conflict_any_w = 1U;
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__rd_addr_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__cap_active_w)
            ? (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__recwr_addr_w)
            : ((5U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__hs_r))
                ? (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__rp_k_r)
                : (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__fl_sink_r)));
    if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__byp_v_r) 
         & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__byp_sink_r) 
            == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__c1_sink_r)))) {
        __Vtemp_1[0U] = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__byp_data_r[0U];
        __Vtemp_1[1U] = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__byp_data_r[1U];
        __Vtemp_1[2U] = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__byp_data_r[2U];
        __Vtemp_1[3U] = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__byp_data_r[3U];
        __Vtemp_1[4U] = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__byp_data_r[4U];
    } else {
        __Vtemp_1[0U] = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__shw_rdata_r[0U];
        __Vtemp_1[1U] = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__shw_rdata_r[1U];
        __Vtemp_1[2U] = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__shw_rdata_r[2U];
        __Vtemp_1[3U] = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__shw_rdata_r[3U];
        __Vtemp_1[4U] = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__shw_rdata_r[4U];
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__c1_wr_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__c1_v_r) 
           & ((0U != (((((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__c1_proj_r[0U] 
                          ^ __Vtemp_1[0U]) | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__c1_proj_r[1U] 
                                              ^ __Vtemp_1[1U])) 
                        | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__c1_proj_r[2U] 
                           ^ __Vtemp_1[2U])) | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__c1_proj_r[3U] 
                                                ^ __Vtemp_1[3U])) 
                      | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__c1_proj_r[4U] 
                         ^ __Vtemp_1[4U]))) | ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__c1_vld_r) 
                                               != (
                                                   (8U 
                                                    >= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__c1_sink_r)) 
                                                   & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__valid_r) 
                                                      >> (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__c1_sink_r))))));
    __VdfgRegularize_h6e95ff9d_0_24 = ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_38)
                                        ? (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_23)
                                        : ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_75)
                                            ? (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_23)
                                            : ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_74)
                                                ? (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_23)
                                                : ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_51)
                                                    ? (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_23)
                                                    : 
                                                   ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_73)
                                                     ? (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_23)
                                                     : 
                                                    ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_23) 
                                                     | (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_101)))))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__ser_start_w 
        = ((~ ((0U == vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__len_r
                [vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__slot_r]) 
               | (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_153))) 
           & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_401));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__pend_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__pend_r) 
           & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__arb_req_w));
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__sol_pend_w 
        = (0U != (0xa5U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__pend_w)));
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__elig_w 
        = (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__pace_nonsol_r) 
            & (IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__sol_pend_w))
            ? (0xa5U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__pend_w))
            : (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__pend_w));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__pick_ok_w = 0U;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__pick_w = 0U;
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__selection__DOT__best_w = 7U;
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__selection__DOT__key_w 
        = (1U | (4U & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__aged_w)) 
                       << 2U)));
    if ((1U & (IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__elig_w))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__pick_ok_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__pick_w = 0U;
        milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__selection__DOT__best_w 
            = milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__selection__DOT__key_w;
    }
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__selection__DOT__key_w 
        = (2U | (4U & ((~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__aged_w) 
                           >> 1U)) << 2U)));
    if ((1U & (((IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__elig_w) 
                >> 1U) & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__pick_ok_w)) 
                          | ((IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__selection__DOT__key_w) 
                             < (IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__selection__DOT__best_w)))))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__pick_ok_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__pick_w = 1U;
        milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__selection__DOT__best_w 
            = milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__selection__DOT__key_w;
    }
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__selection__DOT__key_w 
        = (4U & ((~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__aged_w) 
                     >> 2U)) << 2U));
    if ((1U & (((IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__elig_w) 
                >> 2U) & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__pick_ok_w)) 
                          | ((IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__selection__DOT__key_w) 
                             < (IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__selection__DOT__best_w)))))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__pick_ok_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__pick_w = 2U;
        milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__selection__DOT__best_w 
            = milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__selection__DOT__key_w;
    }
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__selection__DOT__key_w 
        = (3U | (4U & ((~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__aged_w) 
                           >> 3U)) << 2U)));
    if ((1U & (((IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__elig_w) 
                >> 3U) & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__pick_ok_w)) 
                          | ((IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__selection__DOT__key_w) 
                             < (IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__selection__DOT__best_w)))))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__pick_ok_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__pick_w = 3U;
        milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__selection__DOT__best_w 
            = milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__selection__DOT__key_w;
    }
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__selection__DOT__key_w 
        = (2U | (4U & ((~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__aged_w) 
                           >> 4U)) << 2U)));
    if ((1U & (((IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__elig_w) 
                >> 4U) & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__pick_ok_w)) 
                          | ((IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__selection__DOT__key_w) 
                             < (IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__selection__DOT__best_w)))))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__pick_ok_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__pick_w = 4U;
        milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__selection__DOT__best_w 
            = milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__selection__DOT__key_w;
    }
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__selection__DOT__key_w 
        = (1U | (4U & ((~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__aged_w) 
                           >> 5U)) << 2U)));
    if ((1U & (((IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__elig_w) 
                >> 5U) & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__pick_ok_w)) 
                          | ((IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__selection__DOT__key_w) 
                             < (IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__selection__DOT__best_w)))))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__pick_ok_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__pick_w = 5U;
        milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__selection__DOT__best_w 
            = milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__selection__DOT__key_w;
    }
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__selection__DOT__key_w 
        = (3U | (4U & ((~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__aged_w) 
                           >> 6U)) << 2U)));
    if ((1U & (((IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__elig_w) 
                >> 6U) & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__pick_ok_w)) 
                          | ((IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__selection__DOT__key_w) 
                             < (IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__selection__DOT__best_w)))))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__pick_ok_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__pick_w = 6U;
        milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__selection__DOT__best_w 
            = milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__selection__DOT__key_w;
    }
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__selection__DOT__key_w 
        = (1U | (4U & ((~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__aged_w) 
                           >> 7U)) << 2U)));
    if ((IData)((((IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__elig_w) 
                  >> 7U) & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__pick_ok_w)) 
                            | ((IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__selection__DOT__key_w) 
                               < (IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__selection__DOT__best_w)))))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__pick_ok_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__pick_w = 7U;
        milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__selection__DOT__best_w 
            = milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__selection__DOT__key_w;
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__sb_gnt_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__sb_adm_req_w) 
           & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__ff_valid_w) 
              & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__conflict_any_w)) 
                 & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__barrier_pend_r)) 
                    | (1U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__sb_adm_class_w))))));
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
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_25 = ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_37)
                                                  ? (IData)(__VdfgRegularize_h6e95ff9d_0_24)
                                                  : 
                                                 ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_72)
                                                   ? (IData)(__VdfgRegularize_h6e95ff9d_0_24)
                                                   : 
                                                  ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_71)
                                                    ? (IData)(__VdfgRegularize_h6e95ff9d_0_24)
                                                    : 
                                                   ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_50)
                                                     ? (IData)(__VdfgRegularize_h6e95ff9d_0_24)
                                                     : 
                                                    ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_70)
                                                      ? (IData)(__VdfgRegularize_h6e95ff9d_0_24)
                                                      : 
                                                     ((IData)(__VdfgRegularize_h6e95ff9d_0_24) 
                                                      | (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_102)))))));
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__aecp_sb_grant_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__sb_pick_aecp_w) 
           & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__sb_gnt_w));
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__acmp_sb_grant_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__sb_pick_acmp_w) 
           & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__sb_gnt_w));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__aecp_sb_accept_w 
        = ((IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__aecp_sb_grant_w) 
           & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__aecp_sb_candidate_w));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__aecp_txn_ready_w 
        = ((IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__aecp_sb_grant_w) 
           & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__aecp_eng_ready_w));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT____Vcellinp__u_aecp__txn_valid_i 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__out_valid_r) 
           & (IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__aecp_sb_grant_w));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__acmp_sb_accept_w 
        = ((IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__acmp_sb_grant_w) 
           & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__acmp_sb_candidate_w));
    __VdfgRegularize_h6e95ff9d_0_384 = ((2U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pf_st_r)) 
                                        & (IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__acmp_sb_grant_w));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__rd_en_w 
        = ((0U != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__cnt_r)) 
           & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__out_valid_r)) 
              | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__aecp_txn_ready_w)));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__rsp_open_w 
        = (((((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT____Vcellinp__u_aecp__txn_valid_i)) 
              | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__ntfy_amap_busy_w)) 
             & (6U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__n_st_r))) 
            | ((~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__drop_w) 
                   | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__ntfy_amap_busy_w))) 
               & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT____Vcellinp__u_aecp__txn_valid_i))) 
           & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_286));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__acmp_txn_ready_w 
        = ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_167) 
           & (IData)(__VdfgRegularize_h6e95ff9d_0_384));
    __VdfgRegularize_h6e95ff9d_0_383 = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_acmp_q__DOT__out_valid_r) 
                                        & (IData)(__VdfgRegularize_h6e95ff9d_0_384));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_acmp_q__DOT__rd_en_w 
        = ((0U != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_acmp_q__DOT__cnt_r)) 
           & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_acmp_q__DOT__out_valid_r)) 
              | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__acmp_txn_ready_w)));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT____Vcellinp__u_listener__txn_valid_i 
        = ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__acmp_is_tkr_w)) 
           & (IData)(__VdfgRegularize_h6e95ff9d_0_383));
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT____Vcellinp__u_talker__txn_valid_i 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__acmp_is_tkr_w) 
           & (IData)(__VdfgRegularize_h6e95ff9d_0_383));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_279 = ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT____Vcellinp__u_listener__txn_valid_i)) 
                                                  & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__lstn_txn_ready_w));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__disp_code_w = 0U;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__disp_kind_w = 0U;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__disp_src_w = 0U;
    if ((1U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__state_r))) {
        if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__gp_valid_r) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__disp_code_w = 0U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__disp_kind_w = 2U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__disp_src_w 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__gp_src_r;
        } else {
            if ((1U & (~ (IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT____Vcellinp__u_talker__txn_valid_i)))) {
                if ((0U != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__pe_off_r))) {
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__disp_code_w = 1U;
                    vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__83__v 
                        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__pe_off_r;
                    vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__83__Vfuncout = 0U;
                    if ((0x00000100U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__83__v))) {
                        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__83__Vfuncout = 8U;
                    }
                    if ((0x00000080U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__83__v))) {
                        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__83__Vfuncout = 7U;
                    }
                    if ((0x00000040U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__83__v))) {
                        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__83__Vfuncout = 6U;
                    }
                    if ((0x00000020U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__83__v))) {
                        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__83__Vfuncout = 5U;
                    }
                    if ((0x00000010U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__83__v))) {
                        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__83__Vfuncout = 4U;
                    }
                    if ((8U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__83__v))) {
                        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__83__Vfuncout = 3U;
                    }
                    if ((4U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__83__v))) {
                        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__83__Vfuncout = 2U;
                    }
                    if ((2U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__83__v))) {
                        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__83__Vfuncout = 1U;
                    }
                    if ((1U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__83__v))) {
                        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__83__Vfuncout = 0U;
                    }
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__disp_src_w 
                        = vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__83__Vfuncout;
                } else if ((0U != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__pe_conflict_r))) {
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__disp_code_w = 2U;
                    vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__84__v 
                        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__pe_conflict_r;
                    vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__84__Vfuncout = 0U;
                    if ((0x00000100U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__84__v))) {
                        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__84__Vfuncout = 8U;
                    }
                    if ((0x00000080U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__84__v))) {
                        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__84__Vfuncout = 7U;
                    }
                    if ((0x00000040U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__84__v))) {
                        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__84__Vfuncout = 6U;
                    }
                    if ((0x00000020U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__84__v))) {
                        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__84__Vfuncout = 5U;
                    }
                    if ((0x00000010U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__84__v))) {
                        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__84__Vfuncout = 4U;
                    }
                    if ((8U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__84__v))) {
                        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__84__Vfuncout = 3U;
                    }
                    if ((4U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__84__v))) {
                        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__84__Vfuncout = 2U;
                    }
                    if ((2U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__84__v))) {
                        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__84__Vfuncout = 1U;
                    }
                    if ((1U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__84__v))) {
                        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__84__Vfuncout = 0U;
                    }
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__disp_src_w 
                        = vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__84__Vfuncout;
                } else if ((0U != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__pe_pcp_r))) {
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__disp_code_w = 3U;
                    vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__85__v 
                        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__pe_pcp_r;
                    vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__85__Vfuncout = 0U;
                    if ((0x00000100U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__85__v))) {
                        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__85__Vfuncout = 8U;
                    }
                    if ((0x00000080U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__85__v))) {
                        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__85__Vfuncout = 7U;
                    }
                    if ((0x00000040U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__85__v))) {
                        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__85__Vfuncout = 6U;
                    }
                    if ((0x00000020U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__85__v))) {
                        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__85__Vfuncout = 5U;
                    }
                    if ((0x00000010U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__85__v))) {
                        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__85__Vfuncout = 4U;
                    }
                    if ((8U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__85__v))) {
                        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__85__Vfuncout = 3U;
                    }
                    if ((4U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__85__v))) {
                        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__85__Vfuncout = 2U;
                    }
                    if ((2U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__85__v))) {
                        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__85__Vfuncout = 1U;
                    }
                    if ((1U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__85__v))) {
                        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__85__Vfuncout = 0U;
                    }
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__disp_src_w 
                        = vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__85__Vfuncout;
                } else if ((0U != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__pe_tmr_r))) {
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__disp_code_w = 4U;
                    vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__86__v 
                        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__pe_tmr_r;
                    vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__86__Vfuncout = 0U;
                    if ((0x00000100U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__86__v))) {
                        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__86__Vfuncout = 8U;
                    }
                    if ((0x00000080U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__86__v))) {
                        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__86__Vfuncout = 7U;
                    }
                    if ((0x00000040U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__86__v))) {
                        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__86__Vfuncout = 6U;
                    }
                    if ((0x00000020U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__86__v))) {
                        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__86__Vfuncout = 5U;
                    }
                    if ((0x00000010U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__86__v))) {
                        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__86__Vfuncout = 4U;
                    }
                    if ((8U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__86__v))) {
                        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__86__Vfuncout = 3U;
                    }
                    if ((4U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__86__v))) {
                        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__86__Vfuncout = 2U;
                    }
                    if ((2U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__86__v))) {
                        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__86__Vfuncout = 1U;
                    }
                    if ((1U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__86__v))) {
                        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__86__Vfuncout = 0U;
                    }
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__disp_src_w 
                        = vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__86__Vfuncout;
                } else if ((0U != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__pe_lsn_r))) {
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__disp_code_w = 5U;
                    vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__87__v 
                        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__pe_lsn_r;
                    vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__87__Vfuncout = 0U;
                    if ((0x00000100U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__87__v))) {
                        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__87__Vfuncout = 8U;
                    }
                    if ((0x00000080U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__87__v))) {
                        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__87__Vfuncout = 7U;
                    }
                    if ((0x00000040U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__87__v))) {
                        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__87__Vfuncout = 6U;
                    }
                    if ((0x00000020U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__87__v))) {
                        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__87__Vfuncout = 5U;
                    }
                    if ((0x00000010U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__87__v))) {
                        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__87__Vfuncout = 4U;
                    }
                    if ((8U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__87__v))) {
                        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__87__Vfuncout = 3U;
                    }
                    if ((4U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__87__v))) {
                        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__87__Vfuncout = 2U;
                    }
                    if ((2U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__87__v))) {
                        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__87__Vfuncout = 1U;
                    }
                    if ((1U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__87__v))) {
                        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__87__Vfuncout = 0U;
                    }
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__disp_src_w 
                        = vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__87__Vfuncout;
                } else if ((0U != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__pe_rel_r))) {
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__disp_code_w = 7U;
                    vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__88__v 
                        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__pe_rel_r;
                    vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__88__Vfuncout = 0U;
                    if ((0x00000100U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__88__v))) {
                        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__88__Vfuncout = 8U;
                    }
                    if ((0x00000080U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__88__v))) {
                        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__88__Vfuncout = 7U;
                    }
                    if ((0x00000040U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__88__v))) {
                        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__88__Vfuncout = 6U;
                    }
                    if ((0x00000020U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__88__v))) {
                        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__88__Vfuncout = 5U;
                    }
                    if ((0x00000010U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__88__v))) {
                        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__88__Vfuncout = 4U;
                    }
                    if ((8U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__88__v))) {
                        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__88__Vfuncout = 3U;
                    }
                    if ((4U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__88__v))) {
                        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__88__Vfuncout = 2U;
                    }
                    if ((2U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__88__v))) {
                        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__88__Vfuncout = 1U;
                    }
                    if ((1U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__88__v))) {
                        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__88__Vfuncout = 0U;
                    }
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__disp_src_w 
                        = vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__88__Vfuncout;
                } else if ((0U != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__pe_init_r))) {
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__disp_code_w = 6U;
                    vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__89__v 
                        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__pe_init_r;
                    vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__89__Vfuncout = 0U;
                    if ((0x00000100U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__89__v))) {
                        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__89__Vfuncout = 8U;
                    }
                    if ((0x00000080U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__89__v))) {
                        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__89__Vfuncout = 7U;
                    }
                    if ((0x00000040U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__89__v))) {
                        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__89__Vfuncout = 6U;
                    }
                    if ((0x00000020U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__89__v))) {
                        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__89__Vfuncout = 5U;
                    }
                    if ((0x00000010U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__89__v))) {
                        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__89__Vfuncout = 4U;
                    }
                    if ((8U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__89__v))) {
                        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__89__Vfuncout = 3U;
                    }
                    if ((4U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__89__v))) {
                        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__89__Vfuncout = 2U;
                    }
                    if ((2U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__89__v))) {
                        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__89__Vfuncout = 1U;
                    }
                    if ((1U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__89__v))) {
                        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__89__Vfuncout = 0U;
                    }
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__disp_src_w 
                        = vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__89__Vfuncout;
                }
            }
            if (milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT____Vcellinp__u_talker__txn_valid_i) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__disp_kind_w = 1U;
            } else if ((0U != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__pe_off_r))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__disp_kind_w = 2U;
            } else if ((0U != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__pe_conflict_r))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__disp_kind_w = 2U;
            } else if ((0U != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__pe_pcp_r))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__disp_kind_w = 2U;
            } else if ((0U != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__pe_tmr_r))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__disp_kind_w = 2U;
            } else if ((0U != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__pe_lsn_r))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__disp_kind_w = 2U;
            } else if ((0U != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__pe_rel_r))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__disp_kind_w = 2U;
            } else if ((0U != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__pe_init_r))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__disp_kind_w = 2U;
            }
        }
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__lstn_evt_tk_ready_w 
        = ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__pend_any_w)) 
           & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_279));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__rec_re_w = 0U;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__clr_disp_w = 0U;
    if (((1U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__state_r)) 
         & (2U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__disp_kind_w)))) {
        if ((8U >= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__disp_src_w))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__clr_disp_w 
                = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__clr_disp_w) 
                   | (0x01ffU & ((IData)(1U) << (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__disp_src_w))));
        }
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__rec_raddr_w = 0U;
    if ((0U != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__state_r))) {
        if ((1U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__state_r))) {
            if ((1U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__disp_kind_w))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__rec_re_w = 1U;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__rec_raddr_w 
                    = (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__txn_in_w[1U] 
                       >> 0x0000001cU);
            } else if ((2U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__disp_kind_w))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__rec_re_w = 1U;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__rec_raddr_w 
                    = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__disp_src_w;
            }
        }
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__deliver_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__valid_r) 
           & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__lstn_evt_tk_valid_w)
               ? (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__lstn_evt_tk_ready_w)
               : (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__valid_r)));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__delivered_w = 0U;
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pend_after_w 
        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r;
    if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__deliver_w) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__delivered_w 
            = (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__delivered_w 
               | (0x00000000ffffffffULL & ((IData)(1U) 
                                           << (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__sel_r))));
        milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pend_after_w 
            = ((~ ((IData)(1U) << (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__sel_r))) 
               & milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pend_after_w);
        milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__base_w 
            = (0x0000001fU & (((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__sel_r)) 
                              & (- (IData)((0x1fU != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__sel_r))))));
    } else {
        milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__base_w 
            = (0x0000001fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__ptr_r));
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__gnt_found_w = 0U;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__gnt_src_w = 0U;
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx 
        = milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__base_w;
    if ((0x00000020U <= milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx)) {
        milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx 
            = (milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx 
               - (IData)(0x00000020U));
    }
    if ((1U & (milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pend_after_w 
               >> (0x0000001fU & milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__gnt_found_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__gnt_src_w 
            = (0x0000001fU & milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx);
    }
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx 
        = ((IData)(1U) + (IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__base_w));
    if ((0x00000020U <= milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx)) {
        milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx 
            = (milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx 
               - (IData)(0x00000020U));
    }
    if ((1U & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__gnt_found_w)) 
               & (milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pend_after_w 
                  >> (0x0000001fU & milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx))))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__gnt_found_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__gnt_src_w 
            = (0x0000001fU & milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx);
    }
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx 
        = ((IData)(2U) + (IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__base_w));
    if ((0x00000020U <= milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx)) {
        milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx 
            = (milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx 
               - (IData)(0x00000020U));
    }
    if ((1U & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__gnt_found_w)) 
               & (milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pend_after_w 
                  >> (0x0000001fU & milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx))))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__gnt_found_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__gnt_src_w 
            = (0x0000001fU & milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx);
    }
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx 
        = ((IData)(3U) + (IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__base_w));
    if ((0x00000020U <= milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx)) {
        milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx 
            = (milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx 
               - (IData)(0x00000020U));
    }
    if ((1U & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__gnt_found_w)) 
               & (milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pend_after_w 
                  >> (0x0000001fU & milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx))))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__gnt_found_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__gnt_src_w 
            = (0x0000001fU & milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx);
    }
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx 
        = ((IData)(4U) + (IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__base_w));
    if ((0x00000020U <= milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx)) {
        milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx 
            = (milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx 
               - (IData)(0x00000020U));
    }
    if ((1U & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__gnt_found_w)) 
               & (milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pend_after_w 
                  >> (0x0000001fU & milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx))))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__gnt_found_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__gnt_src_w 
            = (0x0000001fU & milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx);
    }
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx 
        = ((IData)(5U) + (IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__base_w));
    if ((0x00000020U <= milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx)) {
        milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx 
            = (milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx 
               - (IData)(0x00000020U));
    }
    if ((1U & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__gnt_found_w)) 
               & (milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pend_after_w 
                  >> (0x0000001fU & milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx))))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__gnt_found_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__gnt_src_w 
            = (0x0000001fU & milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx);
    }
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx 
        = ((IData)(6U) + (IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__base_w));
    if ((0x00000020U <= milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx)) {
        milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx 
            = (milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx 
               - (IData)(0x00000020U));
    }
    if ((1U & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__gnt_found_w)) 
               & (milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pend_after_w 
                  >> (0x0000001fU & milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx))))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__gnt_found_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__gnt_src_w 
            = (0x0000001fU & milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx);
    }
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx 
        = ((IData)(7U) + (IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__base_w));
    if ((0x00000020U <= milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx)) {
        milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx 
            = (milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx 
               - (IData)(0x00000020U));
    }
    if ((1U & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__gnt_found_w)) 
               & (milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pend_after_w 
                  >> (0x0000001fU & milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx))))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__gnt_found_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__gnt_src_w 
            = (0x0000001fU & milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx);
    }
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx 
        = ((IData)(8U) + (IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__base_w));
    if ((0x00000020U <= milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx)) {
        milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx 
            = (milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx 
               - (IData)(0x00000020U));
    }
    if ((1U & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__gnt_found_w)) 
               & (milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pend_after_w 
                  >> (0x0000001fU & milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx))))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__gnt_found_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__gnt_src_w 
            = (0x0000001fU & milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx);
    }
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx 
        = ((IData)(9U) + (IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__base_w));
    if ((0x00000020U <= milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx)) {
        milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx 
            = (milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx 
               - (IData)(0x00000020U));
    }
    if ((1U & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__gnt_found_w)) 
               & (milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pend_after_w 
                  >> (0x0000001fU & milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx))))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__gnt_found_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__gnt_src_w 
            = (0x0000001fU & milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx);
    }
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx 
        = ((IData)(0x0000000aU) + (IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__base_w));
    if ((0x00000020U <= milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx)) {
        milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx 
            = (milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx 
               - (IData)(0x00000020U));
    }
    if ((1U & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__gnt_found_w)) 
               & (milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pend_after_w 
                  >> (0x0000001fU & milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx))))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__gnt_found_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__gnt_src_w 
            = (0x0000001fU & milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx);
    }
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx 
        = ((IData)(0x0000000bU) + (IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__base_w));
    if ((0x00000020U <= milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx)) {
        milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx 
            = (milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx 
               - (IData)(0x00000020U));
    }
    if ((1U & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__gnt_found_w)) 
               & (milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pend_after_w 
                  >> (0x0000001fU & milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx))))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__gnt_found_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__gnt_src_w 
            = (0x0000001fU & milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx);
    }
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx 
        = ((IData)(0x0000000cU) + (IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__base_w));
    if ((0x00000020U <= milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx)) {
        milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx 
            = (milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx 
               - (IData)(0x00000020U));
    }
    if ((1U & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__gnt_found_w)) 
               & (milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pend_after_w 
                  >> (0x0000001fU & milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx))))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__gnt_found_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__gnt_src_w 
            = (0x0000001fU & milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx);
    }
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx 
        = ((IData)(0x0000000dU) + (IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__base_w));
    if ((0x00000020U <= milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx)) {
        milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx 
            = (milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx 
               - (IData)(0x00000020U));
    }
    if ((1U & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__gnt_found_w)) 
               & (milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pend_after_w 
                  >> (0x0000001fU & milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx))))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__gnt_found_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__gnt_src_w 
            = (0x0000001fU & milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx);
    }
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx 
        = ((IData)(0x0000000eU) + (IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__base_w));
    if ((0x00000020U <= milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx)) {
        milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx 
            = (milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx 
               - (IData)(0x00000020U));
    }
    if ((1U & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__gnt_found_w)) 
               & (milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pend_after_w 
                  >> (0x0000001fU & milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx))))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__gnt_found_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__gnt_src_w 
            = (0x0000001fU & milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx);
    }
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx 
        = ((IData)(0x0000000fU) + (IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__base_w));
    if ((0x00000020U <= milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx)) {
        milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx 
            = (milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx 
               - (IData)(0x00000020U));
    }
    if ((1U & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__gnt_found_w)) 
               & (milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pend_after_w 
                  >> (0x0000001fU & milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx))))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__gnt_found_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__gnt_src_w 
            = (0x0000001fU & milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx);
    }
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx 
        = ((IData)(0x00000010U) + (IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__base_w));
    if ((0x00000020U <= milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx)) {
        milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx 
            = (milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx 
               - (IData)(0x00000020U));
    }
    if ((1U & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__gnt_found_w)) 
               & (milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pend_after_w 
                  >> (0x0000001fU & milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx))))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__gnt_found_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__gnt_src_w 
            = (0x0000001fU & milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx);
    }
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx 
        = ((IData)(0x00000011U) + (IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__base_w));
    if ((0x00000020U <= milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx)) {
        milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx 
            = (milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx 
               - (IData)(0x00000020U));
    }
    if ((1U & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__gnt_found_w)) 
               & (milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pend_after_w 
                  >> (0x0000001fU & milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx))))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__gnt_found_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__gnt_src_w 
            = (0x0000001fU & milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx);
    }
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx 
        = ((IData)(0x00000012U) + (IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__base_w));
    if ((0x00000020U <= milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx)) {
        milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx 
            = (milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx 
               - (IData)(0x00000020U));
    }
    if ((1U & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__gnt_found_w)) 
               & (milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pend_after_w 
                  >> (0x0000001fU & milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx))))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__gnt_found_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__gnt_src_w 
            = (0x0000001fU & milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx);
    }
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx 
        = ((IData)(0x00000013U) + (IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__base_w));
    if ((0x00000020U <= milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx)) {
        milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx 
            = (milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx 
               - (IData)(0x00000020U));
    }
    if ((1U & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__gnt_found_w)) 
               & (milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pend_after_w 
                  >> (0x0000001fU & milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx))))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__gnt_found_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__gnt_src_w 
            = (0x0000001fU & milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx);
    }
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx 
        = ((IData)(0x00000014U) + (IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__base_w));
    if ((0x00000020U <= milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx)) {
        milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx 
            = (milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx 
               - (IData)(0x00000020U));
    }
    if ((1U & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__gnt_found_w)) 
               & (milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pend_after_w 
                  >> (0x0000001fU & milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx))))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__gnt_found_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__gnt_src_w 
            = (0x0000001fU & milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx);
    }
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx 
        = ((IData)(0x00000015U) + (IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__base_w));
    if ((0x00000020U <= milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx)) {
        milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx 
            = (milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx 
               - (IData)(0x00000020U));
    }
    if ((1U & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__gnt_found_w)) 
               & (milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pend_after_w 
                  >> (0x0000001fU & milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx))))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__gnt_found_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__gnt_src_w 
            = (0x0000001fU & milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx);
    }
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx 
        = ((IData)(0x00000016U) + (IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__base_w));
    if ((0x00000020U <= milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx)) {
        milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx 
            = (milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx 
               - (IData)(0x00000020U));
    }
    if ((1U & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__gnt_found_w)) 
               & (milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pend_after_w 
                  >> (0x0000001fU & milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx))))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__gnt_found_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__gnt_src_w 
            = (0x0000001fU & milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx);
    }
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx 
        = ((IData)(0x00000017U) + (IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__base_w));
    if ((0x00000020U <= milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx)) {
        milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx 
            = (milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx 
               - (IData)(0x00000020U));
    }
    if ((1U & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__gnt_found_w)) 
               & (milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pend_after_w 
                  >> (0x0000001fU & milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx))))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__gnt_found_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__gnt_src_w 
            = (0x0000001fU & milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx);
    }
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx 
        = ((IData)(0x00000018U) + (IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__base_w));
    if ((0x00000020U <= milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx)) {
        milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx 
            = (milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx 
               - (IData)(0x00000020U));
    }
    if ((1U & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__gnt_found_w)) 
               & (milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pend_after_w 
                  >> (0x0000001fU & milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx))))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__gnt_found_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__gnt_src_w 
            = (0x0000001fU & milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx);
    }
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx 
        = ((IData)(0x00000019U) + (IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__base_w));
    if ((0x00000020U <= milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx)) {
        milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx 
            = (milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx 
               - (IData)(0x00000020U));
    }
    if ((1U & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__gnt_found_w)) 
               & (milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pend_after_w 
                  >> (0x0000001fU & milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx))))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__gnt_found_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__gnt_src_w 
            = (0x0000001fU & milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx);
    }
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx 
        = ((IData)(0x0000001aU) + (IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__base_w));
    if ((0x00000020U <= milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx)) {
        milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx 
            = (milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx 
               - (IData)(0x00000020U));
    }
    if ((1U & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__gnt_found_w)) 
               & (milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pend_after_w 
                  >> (0x0000001fU & milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx))))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__gnt_found_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__gnt_src_w 
            = (0x0000001fU & milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx);
    }
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx 
        = ((IData)(0x0000001bU) + (IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__base_w));
    if ((0x00000020U <= milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx)) {
        milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx 
            = (milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx 
               - (IData)(0x00000020U));
    }
    if ((1U & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__gnt_found_w)) 
               & (milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pend_after_w 
                  >> (0x0000001fU & milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx))))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__gnt_found_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__gnt_src_w 
            = (0x0000001fU & milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx);
    }
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx 
        = ((IData)(0x0000001cU) + (IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__base_w));
    if ((0x00000020U <= milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx)) {
        milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx 
            = (milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx 
               - (IData)(0x00000020U));
    }
    if ((1U & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__gnt_found_w)) 
               & (milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pend_after_w 
                  >> (0x0000001fU & milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx))))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__gnt_found_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__gnt_src_w 
            = (0x0000001fU & milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx);
    }
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx 
        = ((IData)(0x0000001dU) + (IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__base_w));
    if ((0x00000020U <= milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx)) {
        milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx 
            = (milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx 
               - (IData)(0x00000020U));
    }
    if ((1U & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__gnt_found_w)) 
               & (milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pend_after_w 
                  >> (0x0000001fU & milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx))))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__gnt_found_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__gnt_src_w 
            = (0x0000001fU & milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx);
    }
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx 
        = ((IData)(0x0000001eU) + (IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__base_w));
    if ((0x00000020U <= milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx)) {
        milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx 
            = (milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx 
               - (IData)(0x00000020U));
    }
    if ((1U & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__gnt_found_w)) 
               & (milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pend_after_w 
                  >> (0x0000001fU & milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx))))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__gnt_found_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__gnt_src_w 
            = (0x0000001fU & milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx);
    }
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx 
        = ((IData)(0x0000001fU) + (IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__base_w));
    if ((0x00000020U <= milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx)) {
        milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx 
            = (milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx 
               - (IData)(0x00000020U));
    }
    if ((1U & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__gnt_found_w)) 
               & (milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pend_after_w 
                  >> (0x0000001fU & milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx))))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__gnt_found_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__gnt_src_w 
            = (0x0000001fU & milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx);
    }
}

void Vmilan_datapath___024root___nba_comb__TOP__0(Vmilan_datapath___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vmilan_datapath___024root___nba_comb__TOP__0\n"); );
    Vmilan_datapath__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    SData/*15:0*/ milan_datapath__DOT__csr__DOT__read_mux__DOT__soff;
    milan_datapath__DOT__csr__DOT__read_mux__DOT__soff = 0;
    SData/*15:0*/ milan_datapath__DOT__csr__DOT__read_mux__DOT__loff;
    milan_datapath__DOT__csr__DOT__read_mux__DOT__loff = 0;
    SData/*15:0*/ milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff;
    milan_datapath__DOT__csr__DOT__read_mux__DOT__aoff = 0;
    // Body
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__maap_swallow_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_maap_shim__DOT__rsp_valid_r) 
           & (0U != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__maap_stale_r)));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_405 = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__ser_busy_r) 
                                                  & (0U 
                                                     == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__fr_st_r)));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__push_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__ser_busy_r) 
           & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__wptr_r) 
              != (0x40U ^ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__rptr_r))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__pdu_byte_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__ser_busy_r) 
           & ((1U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__fr_st_r)) 
              & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__slot_now_w) 
                 & (0x000eU <= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__idx_r)))));
    vlSelfRef.milan_datapath__DOT__talker_diag__DOT__ev_tu_w = 0U;
    if (((IData)(vlSelfRef.milan_datapath__DOT____Vcellinp__media_clock_restart__frame_p_i) 
         & (9U > (IData)(vlSelfRef.milan_datapath__DOT__media_clock_restart__DOT__fidx_w)))) {
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
    vlSelfRef.milan_datapath__DOT____Vcellinp__media_clock_restart__frame_mr_i 
        = ((IData)(vlSelfRef.milan_datapath__DOT__aaf_frame_p_w)
            ? (IData)(vlSelfRef.milan_datapath__DOT__aaf_frame_mr_w)
            : (IData)(vlSelfRef.milan_datapath__DOT__crft_mr_last_w));
    vlSelfRef.milan_datapath__DOT__crf_dp_mux__DOT__active 
        = ((IData)(vlSelfRef.milan_datapath__DOT__crf_dp_mux__DOT__locked_r) 
           | ((IData)(vlSelfRef.milan_datapath__DOT__crf_tx__DOT__st_r) 
              | (3U == (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__est_r))));
    vlSelfRef.milan_datapath__DOT__crf_dp_mux__DOT__gsel 
        = (1U & ((IData)(vlSelfRef.milan_datapath__DOT__crf_dp_mux__DOT__locked_r)
                  ? (IData)(vlSelfRef.milan_datapath__DOT__crf_dp_mux__DOT__sel_r)
                  : (((IData)(vlSelfRef.milan_datapath__DOT__crf_tx__DOT__st_r) 
                      & (3U == (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__est_r)))
                      ? (~ (IData)(vlSelfRef.milan_datapath__DOT__crf_dp_mux__DOT__last_grant_r))
                      : (IData)(vlSelfRef.milan_datapath__DOT__crf_tx__DOT__st_r))));
    vlSelfRef.milan_datapath__DOT__ctl_tx_mux__DOT__active 
        = ((IData)(vlSelfRef.milan_datapath__DOT__ctl_tx_mux__DOT__locked_r) 
           | ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__txp_valid_r) 
              | (IData)(vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_busy_r)));
    vlSelfRef.milan_datapath__DOT__ctl_tx_mux__DOT__gsel 
        = (1U & ((IData)(vlSelfRef.milan_datapath__DOT__ctl_tx_mux__DOT__locked_r)
                  ? (IData)(vlSelfRef.milan_datapath__DOT__ctl_tx_mux__DOT__sel_r)
                  : (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__txp_valid_r) 
                      & (IData)(vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_busy_r))
                      ? (~ (IData)(vlSelfRef.milan_datapath__DOT__ctl_tx_mux__DOT__last_grant_r))
                      : (IData)(vlSelfRef.milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_busy_r))));
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
    vlSelfRef.milan_datapath__DOT__gsi_lreg_w = (3U 
                                                 & ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_out_w 
                                                     >> 
                                                     (0x0000001eU 
                                                      & ((IData)(vlSelfRef.milan_datapath__DOT__gsiq_index_r) 
                                                         << 1U))) 
                                                    & (- (IData)(
                                                                 (0x11U 
                                                                  >= 
                                                                  (0x0000001eU 
                                                                   & ((IData)(vlSelfRef.milan_datapath__DOT__gsiq_index_r) 
                                                                      << 1U)))))));
    vlSelfRef.milan_datapath__DOT__gsi_decl_w = ((8U 
                                                  >= 
                                                  (0x0000000fU 
                                                   & (IData)(vlSelfRef.milan_datapath__DOT__gsiq_index_r))) 
                                                 & (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__declaring_r) 
                                                     >> 
                                                     (0x0000000fU 
                                                      & (IData)(vlSelfRef.milan_datapath__DOT__gsiq_index_r))) 
                                                    & (IData)(vlSelfRef.milan_datapath__DOT__gsi_out_w)));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_side_port__DOT__accept_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__hb_pend_r) 
           & (0U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_side_port__DOT__state_r)));
    vlSelfRef.milan_datapath__DOT__sfv_base_ok_w = 
        ((~ (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__setval_r 
                     >> 0x00000034U))) & ((0xffefffff003fffffULL 
                                           & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__setval_r) 
                                          == (0xffefffff003fffffULL 
                                              & vlSelfRef.milan_datapath__DOT__sfv_decl_w)));
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
    vlSelfRef.milan_datapath__DOT__ctr_avb_link_edge_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__ctr_link_q_r) 
           != (IData)(vlSelfRef.milan_datapath__DOT__eff_link_w));
    vlSelfRef.milan_datapath__DOT__gsi_ofail_w = ((2U 
                                                   == 
                                                   (3U 
                                                    & ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_tk_decl_state_w 
                                                        >> 
                                                        (0x0000001eU 
                                                         & ((IData)(vlSelfRef.milan_datapath__DOT__gsiq_index_r) 
                                                            << 1U))) 
                                                       & (- (IData)(
                                                                    (0x11U 
                                                                     >= 
                                                                     (0x0000001eU 
                                                                      & ((IData)(vlSelfRef.milan_datapath__DOT__gsiq_index_r) 
                                                                         << 1U)))))))) 
                                                  & (IData)(vlSelfRef.milan_datapath__DOT__gsi_out_w));
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
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__fw_valid_w 
        = ((0U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__fw_S))
            ? (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__beat_w)
            : ((1U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__fw_S))
                ? (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__beat_w)
                : ((2U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__fw_S)) 
                   && (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__beat_w))));
    vlSelfRef.milan_datapath__DOT____Vcellinp__chan_map_render__map_wr_data_i 
        = ((IData)(vlSelfRef.milan_datapath__DOT__amap_edit_iwr_p_r)
            ? (IData)(vlSelfRef.milan_datapath__DOT__amap_edit_iwr_word_r)
            : ((((2U & (vlSelfRef.milan_datapath__DOT__csr__DOT__chmap_word 
                        >> 0x0000000eU)) | (1U & (vlSelfRef.milan_datapath__DOT__csr__DOT__chmap_word 
                                                  >> 0x0000000cU))) 
                << 6U) | ((0x00000038U & (vlSelfRef.milan_datapath__DOT__csr__DOT__chmap_word 
                                          >> 1U)) | 
                          (7U & vlSelfRef.milan_datapath__DOT__csr__DOT__chmap_word))));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_394 = ((~ (IData)(vlSelfRef.milan_datapath__DOT__gsi_req_q_r)) 
                                                  & (IData)(vlSelfRef.milan_datapath__DOT__pp_gsi_req_w));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__arb_tx_ready_w 
        = ((0U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__sh_st_r))
            ? ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__out_valid_r) 
                         & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__sh_need_r)))) 
               && (1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__txp_valid_r))))
            : ((1U != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__sh_st_r)) 
               && (1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__txp_valid_r)))));
    vlSelfRef.milan_datapath__DOT__gsi_sel_match_w 
        = (((IData)(vlSelfRef.milan_datapath__DOT__gsiq_kind_r) 
            == (IData)(vlSelfRef.milan_datapath__DOT__pp_gsi_kind_w)) 
           & (((IData)(vlSelfRef.milan_datapath__DOT__gsiq_type_r) 
               == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cfg_ix_r)) 
              & (((IData)(vlSelfRef.milan_datapath__DOT__gsiq_index_r) 
                  == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__desc_ix_r)) 
                 & (((IData)(vlSelfRef.milan_datapath__DOT__gsiq_sel_r) 
                     == (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gx_sel_w))) 
                    & ((IData)(vlSelfRef.milan_datapath__DOT__gsiq_ord_r) 
                       == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_rec_r))))));
    vlSelfRef.milan_datapath__DOT__gsi_bnd_w = ((8U 
                                                 >= 
                                                 (0x0000000fU 
                                                  & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__desc_ix_r))) 
                                                & (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__bound_hold_r) 
                                                    >> 
                                                    (0x0000000fU 
                                                     & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__desc_ix_r))) 
                                                   & (IData)(vlSelfRef.milan_datapath__DOT__gsi_in_w)));
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
    vlSelfRef.milan_datapath__DOT__gsi_tkfail_w = (
                                                   (2U 
                                                    == (IData)(vlSelfRef.milan_datapath__DOT__gsi_tkreg_w)) 
                                                   & (IData)(vlSelfRef.milan_datapath__DOT__gsi_in_w));
    vlSelfRef.milan_datapath__DOT__gsi_reging_w = (
                                                   (0U 
                                                    != (IData)(vlSelfRef.milan_datapath__DOT__gsi_tkreg_w)) 
                                                   & (IData)(vlSelfRef.milan_datapath__DOT__gsi_in_w));
    vlSelfRef.milan_datapath__DOT__aaf_stream_en_w 
        = ((~ (IData)(vlSelfRef.milan_datapath__DOT__amap_edit_out_resv_r)) 
           & (IData)(vlSelfRef.milan_datapath__DOT__aaf_stream_en_raw_w));
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
            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                                                    (0x2000U 
                                                                     == 
                                                                     (0x6000U 
                                                                      & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__cmrd_data_r)))) 
                                                            << 0x00000012U) 
                                                           | ((0x00030000U 
                                                               & ((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__cmrd_data_r) 
                                                                  << 3U)) 
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
                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                                } else if (((0x0900U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x0940U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                                }
                            } else {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = vlSelfRef.milan_datapath__DOT__mcsrv_stat_w;
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
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                    } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                & (0x0940U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                            } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x0940U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                            }
                        } else {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = (((IData)(vlSelfRef.milan_datapath__DOT__tdm_skip_cnt_w) 
                                    << 0x00000010U) 
                                   | (IData)(vlSelfRef.milan_datapath__DOT__tdm_dup_cnt_w));
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
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                            } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x0940U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                            }
                        } else {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = (((IData)(vlSelfRef.milan_datapath__DOT__lb_skip_cnt_w) 
                                    << 0x00000010U) 
                                   | (IData)(vlSelfRef.milan_datapath__DOT__lb_dup_cnt_w));
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
                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                        } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x0940U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                        }
                    } else {
                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                            = ((((((- (IData)((IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__active_r))) 
                                   & (IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__stg_r)) 
                                  << 0x0000000dU) | 
                                 ((IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__active_r) 
                                  << 0x0000000cU)) 
                                | ((((- (IData)((IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__active_r))) 
                                     & (IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__stg_r)) 
                                    << 9U) | ((IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__active_r) 
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
                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
        } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                    & (0x0940U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
        }
    } else if ((0x00000400U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
        if ((0x00000200U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
            if ((0x00000100U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                if ((0x00000080U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                    if ((0x00000040U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                        if ((0x00000020U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                            if ((0x00000010U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                                if ((8U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
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
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                                    } else if (((0x0900U 
                                                 <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                & (0x0940U 
                                                   > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                                    }
                                } else if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
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
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                                    } else if (((0x0900U 
                                                 <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                & (0x0940U 
                                                   > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                                    } else if (((0x0900U 
                                                 <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                & (0x0940U 
                                                   > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                                    }
                                } else {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                                }
                            } else if ((8U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
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
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                                    } else if (((0x0900U 
                                                 <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                & (0x0940U 
                                                   > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                                    }
                                } else {
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
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                                    } else if (((0x0900U 
                                                 <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                & (0x0940U 
                                                   > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                                    }
                                } else {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                        = (((IData)(vlSelfRef.milan_datapath__DOT__asp_gen_w) 
                                            << 4U) 
                                           | (IData)(vlSelfRef.milan_datapath__DOT__asp_count_w));
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
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                                } else if (((0x0900U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x0940U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                                }
                            } else {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                            }
                        } else if ((0x00000010U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
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
                                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                                        } else if (
                                                   ((0x0900U 
                                                     <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                    & (0x0940U 
                                                       > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                                        }
                                    } else {
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                                    } else if (((0x0900U 
                                                 <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                & (0x0940U 
                                                   > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                                    }
                                } else {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                        = vlSelfRef.milan_datapath__DOT__csr__DOT__eth_guard;
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
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                                    } else if (((0x0900U 
                                                 <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                & (0x0940U 
                                                   > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                                    }
                                } else {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                            } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x0940U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
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
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                            } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x0940U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                            }
                        } else {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                        }
                    } else if ((0x00000020U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                        if ((0x00000010U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                            if ((8U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                                if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
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
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                                    } else if (((0x0900U 
                                                 <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                & (0x0940U 
                                                   > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                                    } else if (((0x0900U 
                                                 <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                & (0x0940U 
                                                   > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                                    }
                                } else {
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
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                        } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x0940U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                            } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x0940U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                            }
                        } else {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_domain__DOT__adopted_r) 
                                    << 0x00000018U) 
                                   | ((0x00070000U 
                                       & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_domain__DOT__decl_prio_r) 
                                          << 0x00000010U)) 
                                      | (0x00000fffU 
                                         & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_domain__DOT__decl_vid_r))));
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
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                            } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x0940U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                            }
                        } else {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = (0xa7000000U | (((IData)(vlSelfRef.milan_datapath__DOT__txarb_stall_sticky_r) 
                                                   << 0x00000010U) 
                                                  | (((IData)(vlSelfRef.milan_datapath__DOT__txarb_abort_sticky_r) 
                                                      << 8U) 
                                                     | (((IData)(vlSelfRef.milan_datapath__DOT__adp_tx_mux__DOT__locked_r) 
                                                         << 3U) 
                                                        | (((IData)(vlSelfRef.milan_datapath__DOT__crf_dp_mux__DOT__locked_r) 
                                                            << 2U) 
                                                           | (IData)(vlSelfRef.milan_datapath__DOT__ctl_tx_mux__DOT__locked_r))))));
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
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                                        } else if (
                                                   ((0x0900U 
                                                     <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                    & (0x0940U 
                                                       > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                                        }
                                    } else {
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                            = (1U | 
                                               ((0U 
                                                 != (IData)(vlSelfRef.milan_datapath__DOT__ptp_clock_validity__DOT__hold_r)) 
                                                << 3U));
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
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                                    } else if (((0x0900U 
                                                 <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                & (0x0940U 
                                                   > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                                    }
                                } else {
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
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                                } else if (((0x0900U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x0940U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                                }
                            } else {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                            }
                        } else if ((8U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
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
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                                } else if (((0x0900U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x0940U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                                }
                            } else {
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
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                            } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x0940U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                            }
                        } else {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = ((((IData)(vlSelfRef.milan_datapath__DOT__crft_pcp_w) 
                                     & (- (IData)((0U 
                                                   != (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_57))))) 
                                    << 0x00000014U) 
                                   | ((((IData)(vlSelfRef.milan_datapath__DOT__crft_vid_w) 
                                        & (- (IData)(
                                                     (0U 
                                                      != (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_57))))) 
                                       << 8U) | (((IData)(vlSelfRef.milan_datapath__DOT__crft_emit_en_w) 
                                                  << 7U) 
                                                 | ((0x00000040U 
                                                     & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__adm_admitted_w) 
                                                        >> 2U)) 
                                                    | (((0U 
                                                         != (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_57)) 
                                                        << 5U) 
                                                       | (3U 
                                                          & vlSelfRef.milan_datapath__DOT__csr__DOT__crft_ctrl))))));
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
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                                } else if (((0x0900U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x0940U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                                }
                            } else {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = ((vlSelfRef.milan_datapath__DOT__crf_pducnt_w 
                                        << 0x00000010U) 
                                       | ((0x0000ff00U 
                                           & (vlSelfRef.milan_datapath__DOT__crf_fmterr_w 
                                              << 8U)) 
                                          | (0x000000ffU 
                                             & vlSelfRef.milan_datapath__DOT__crf_seqerr_w)));
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
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                            } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x0940U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                            }
                        } else {
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
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                        } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x0940U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                        }
                    } else {
                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                            = vlSelfRef.milan_datapath__DOT__csr__DOT__rst_epoch_r;
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
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                                } else if (((0x0900U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x0940U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                                }
                            } else {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = vlSelfRef.milan_datapath__DOT__csr__DOT__link_ctrl;
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
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                                    } else if (((0x0900U 
                                                 <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                                & (0x0940U 
                                                   > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                                    }
                                } else {
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
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                                } else if (((0x0900U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x0940U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                                }
                            } else {
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
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                                } else if (((0x0900U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x0940U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                                }
                            } else {
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
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                                } else if (((0x0900U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x0940U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                                }
                            } else {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = ((IData)(vlSelfRef.milan_datapath__DOT__lwsrp_ta_fail_code) 
                                       << 0x00000010U);
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
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                            } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x0940U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                            }
                        } else {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                        }
                    } else if ((8U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
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
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                            } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x0940U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                            }
                        } else {
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
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                                } else if (((0x0900U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x0940U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                                }
                            } else {
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
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                            } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x0940U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                            }
                        } else {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__sum_r;
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
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                            } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x0940U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
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
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                                } else if (((0x0900U 
                                             <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                            & (0x0940U 
                                               > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                                }
                            } else {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                                    = ((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__adp_disc_seen_cnt_r) 
                                       << 0x00000010U);
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
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                       | (2U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__declaring_r) 
                                                << 1U)));
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
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                            } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x0940U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                            }
                        } else {
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
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                        } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x0940U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                        }
                    } else {
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
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                            } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x0940U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                            }
                        } else {
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
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                        } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x0940U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                        }
                    } else {
                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                            = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__lk_held_r) 
                               << 0x00000010U);
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
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                        } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x0940U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                        }
                    } else {
                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                            = vlSelfRef.milan_datapath__DOT__pp_cd_adp_avail_index_w;
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
                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                            & (0x0940U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                }
            } else if ((0x00000020U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                if ((0x00000010U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
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
                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                    } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                & (0x0940U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                    }
                } else if ((8U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
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
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                        } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x0940U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                        }
                    } else {
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
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                        } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x0940U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                        }
                    } else {
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
                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                            & (0x0940U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                }
            } else if ((0x00000040U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                if ((0x00000020U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
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
                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                    } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                & (0x0940U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                    }
                } else if ((0x00000010U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
                    if ((8U & (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))) {
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
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                            } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x0940U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                            }
                        } else {
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
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                            } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                        & (0x0940U 
                                           > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                            }
                        } else {
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
                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                    } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                & (0x0940U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                        } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x0940U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                        }
                    } else {
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
                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                        } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                                    & (0x0940U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
                            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
                        }
                    } else {
                        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
                            = vlSelfRef.milan_datapath__DOT__csr__DOT__phy_rst;
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
                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                    vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
            vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
                vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
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
        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
    } else if (((0x0900U <= (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)) 
                & (0x0940U > (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q)))) {
        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux = 0U;
    }
}
