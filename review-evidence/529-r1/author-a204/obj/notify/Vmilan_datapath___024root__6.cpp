// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vmilan_datapath.h for the primary calling header

#include "Vmilan_datapath__pch.h"

extern const VlWide<16>/*511:0*/ Vmilan_datapath__ConstPool__CONST_hfd3d218a_0;
extern const VlWide<12>/*383:0*/ Vmilan_datapath__ConstPool__CONST_h997e551f_0;
extern const VlUnpacked<CData/*0:0*/, 32> Vmilan_datapath__ConstPool__TABLE_h5f1389fb_0;
extern const VlUnpacked<CData/*2:0*/, 32> Vmilan_datapath__ConstPool__TABLE_h6dff1152_0;

void Vmilan_datapath___024root___nba_sequent__TOP__10(Vmilan_datapath___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vmilan_datapath___024root___nba_sequent__TOP__10\n"); );
    Vmilan_datapath__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    CData/*0:0*/ milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__acmp_sb_grant_w;
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__acmp_sb_grant_w = 0;
    CData/*0:0*/ milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__aecp_sb_grant_w;
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__aecp_sb_grant_w = 0;
    CData/*7:0*/ milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__org_withdraw_slot_mask_w;
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__org_withdraw_slot_mask_w = 0;
    CData/*0:0*/ milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_arm_cancel_w;
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_arm_cancel_w = 0;
    CData/*5:0*/ milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_arm_slot_w;
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_arm_slot_w = 0;
    CData/*7:0*/ milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_arm_owner_w;
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_arm_owner_w = 0;
    IData/*31:0*/ milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_arm_deadline_w;
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_arm_deadline_w = 0;
    CData/*0:0*/ milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT____Vcellinp__u_talker__txn_valid_i;
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT____Vcellinp__u_talker__txn_valid_i = 0;
    CData/*0:0*/ milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__sb_pick_acmp_w;
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__sb_pick_acmp_w = 0;
    CData/*1:0*/ milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_rx_hit_w;
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_rx_hit_w = 0;
    CData/*0:0*/ milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__dyn_ready_w;
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__dyn_ready_w = 0;
    CData/*0:0*/ milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__sol_pend_w;
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__sol_pend_w = 0;
    CData/*7:0*/ milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__elig_w;
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__elig_w = 0;
    CData/*2:0*/ milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__selection__DOT__key_w;
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__selection__DOT__key_w = 0;
    CData/*2:0*/ milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__selection__DOT__best_w;
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__selection__DOT__best_w = 0;
    SData/*10:0*/ milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pend_after_w;
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pend_after_w = 0;
    CData/*3:0*/ milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__base_w;
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__base_w = 0;
    IData/*31:0*/ milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx;
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx = 0;
    CData/*0:0*/ milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__fsm_wr_req_w;
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__fsm_wr_req_w = 0;
    CData/*0:0*/ milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ping_w;
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ping_w = 0;
    VlWide<3>/*83:0*/ milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__txn_rec2_w;
    VL_ZERO_W(84, milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__txn_rec2_w);
    CData/*0:0*/ milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__txn_open_w;
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__txn_open_w = 0;
    CData/*0:0*/ milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__txn_initset_w;
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__txn_initset_w = 0;
    CData/*0:0*/ milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__settled_w;
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__settled_w = 0;
    CData/*0:0*/ milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__conflict_any_w;
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__conflict_any_w = 0;
    CData/*0:0*/ milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__drop_w;
    milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__drop_w = 0;
    CData/*0:0*/ milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw;
    CData/*3:0*/ __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__a_cls;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__a_cls = 0;
    SData/*15:0*/ __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__a_key;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__a_key = 0;
    CData/*3:0*/ __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__b_cls;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__b_cls = 0;
    SData/*15:0*/ __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__b_key;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__b_key = 0;
    CData/*7:0*/ __VdfgRegularize_h6e95ff9d_0_120;
    __VdfgRegularize_h6e95ff9d_0_120 = 0;
    CData/*0:0*/ __VdfgRegularize_h6e95ff9d_0_195;
    __VdfgRegularize_h6e95ff9d_0_195 = 0;
    CData/*0:0*/ __VdfgRegularize_h6e95ff9d_0_196;
    __VdfgRegularize_h6e95ff9d_0_196 = 0;
    CData/*0:0*/ __VdfgRegularize_h6e95ff9d_0_246;
    __VdfgRegularize_h6e95ff9d_0_246 = 0;
    CData/*0:0*/ __VdfgRegularize_h6e95ff9d_0_247;
    __VdfgRegularize_h6e95ff9d_0_247 = 0;
    CData/*0:0*/ __VdfgRegularize_h6e95ff9d_0_257;
    __VdfgRegularize_h6e95ff9d_0_257 = 0;
    VlWide<5>/*159:0*/ __Vtemp_18;
    // Body
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_resp_da_w = 0ULL;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_resp_vlan_w = 0U;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_resp_sid_w = 0ULL;
    if (((4U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__state_r)) 
         & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__talker_cmd_w))) {
        if ((0U == (0x0000000fU & ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__txn_r[11U] 
                                    << 2U) | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__txn_r[10U] 
                                              >> 0x0000001eU))))) {
            if ((2U > (0x0000ffffU & ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__txn_r[2U] 
                                       << 4U) | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__txn_r[1U] 
                                                 >> 0x0000001cU))))) {
                if ((0U == (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__txn_r[12U] 
                                  >> 5U)))) {
                    if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__da_ok_w) {
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_resp_da_w 
                            = (0x0000ffffffffffffULL 
                               & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__rec_q_r[1U])) 
                                   << 0x00000020U) 
                                  | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__rec_q_r[0U]))));
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_resp_vlan_w 
                            = (0x00000fffU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_domain__DOT__decl_vid_r));
                        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__src_sid_f__99__s 
                            = (1U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__txn_r[1U] 
                                     >> 0x0000001cU));
                        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__src_sid_f__99__Vfuncout 
                            = (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_src_sid_w
                                                [(((IData)(0x0000003fU) 
                                                   + 
                                                   (0x0000007fU 
                                                    & ((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__src_sid_f__99__s) 
                                                       << 6U))) 
                                                  >> 5U)])) 
                                << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_src_sid_w
                                                                  [
                                                                  (2U 
                                                                   & ((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__src_sid_f__99__s) 
                                                                      << 1U))])));
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_resp_sid_w 
                            = vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__src_sid_f__99__Vfuncout;
                    }
                }
            }
        } else if ((2U != (0x0000000fU & ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__txn_r[11U] 
                                           << 2U) | 
                                          (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__txn_r[10U] 
                                           >> 0x0000001eU))))) {
            if ((4U == (0x0000000fU & ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__txn_r[11U] 
                                        << 2U) | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__txn_r[10U] 
                                                  >> 0x0000001eU))))) {
                if ((2U > (0x0000ffffU & ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__txn_r[2U] 
                                           << 4U) | 
                                          (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__txn_r[1U] 
                                           >> 0x0000001cU))))) {
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_resp_da_w 
                        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__da_ok_w)
                            ? (0x0000ffffffffffffULL 
                               & (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__rec_q_r[1U])) 
                                   << 0x00000020U) 
                                  | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__rec_q_r[0U]))))
                            : 0ULL);
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_resp_vlan_w 
                        = (0x00000fffU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_domain__DOT__decl_vid_r));
                    vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__src_sid_f__100__s 
                        = (1U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__txn_r[1U] 
                                 >> 0x0000001cU));
                    vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__src_sid_f__100__Vfuncout 
                        = (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_src_sid_w
                                            [(((IData)(0x0000003fU) 
                                               + (0x0000007fU 
                                                  & ((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__src_sid_f__100__s) 
                                                     << 6U))) 
                                              >> 5U)])) 
                            << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_src_sid_w
                                                              [
                                                              (2U 
                                                               & ((IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__src_sid_f__100__s) 
                                                                  << 1U))])));
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_resp_sid_w 
                        = vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__src_sid_f__100__Vfuncout;
                }
            }
        }
    }
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ping_w 
        = (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__talker_cmd_w) 
            & (0U == (0x0060U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__txn_r[12U]))) 
           & ((0U == (0x0000000fU & ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__txn_r[11U] 
                                      << 2U) | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__txn_r[10U] 
                                                >> 0x0000001eU)))) 
              & (2U > (0x0000ffffU & ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__txn_r[2U] 
                                       << 4U) | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__txn_r[1U] 
                                                 >> 0x0000001cU))))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__ev_cancel_w 
        = ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__ev_rsp_w)) 
           & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__cancel_pend_ok_w));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_acmp_q__DOT__rd_ptr_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_acmp_q__DOT__rd_ptr_r;
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_acmp_q__DOT__mem_r__v0) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_acmp_q__DOT__mem_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_acmp_q__DOT__mem_r__v0][0U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_acmp_q__DOT__mem_r__v0[0U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_acmp_q__DOT__mem_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_acmp_q__DOT__mem_r__v0][1U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_acmp_q__DOT__mem_r__v0[1U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_acmp_q__DOT__mem_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_acmp_q__DOT__mem_r__v0][2U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_acmp_q__DOT__mem_r__v0[2U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_acmp_q__DOT__mem_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_acmp_q__DOT__mem_r__v0][3U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_acmp_q__DOT__mem_r__v0[3U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_acmp_q__DOT__mem_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_acmp_q__DOT__mem_r__v0][4U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_acmp_q__DOT__mem_r__v0[4U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_acmp_q__DOT__mem_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_acmp_q__DOT__mem_r__v0][5U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_acmp_q__DOT__mem_r__v0[5U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_acmp_q__DOT__mem_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_acmp_q__DOT__mem_r__v0][6U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_acmp_q__DOT__mem_r__v0[6U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_acmp_q__DOT__mem_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_acmp_q__DOT__mem_r__v0][7U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_acmp_q__DOT__mem_r__v0[7U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_acmp_q__DOT__mem_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_acmp_q__DOT__mem_r__v0][8U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_acmp_q__DOT__mem_r__v0[8U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_acmp_q__DOT__mem_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_acmp_q__DOT__mem_r__v0][9U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_acmp_q__DOT__mem_r__v0[9U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_acmp_q__DOT__mem_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_acmp_q__DOT__mem_r__v0][10U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_acmp_q__DOT__mem_r__v0[10U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_acmp_q__DOT__mem_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_acmp_q__DOT__mem_r__v0][11U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_acmp_q__DOT__mem_r__v0[11U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_acmp_q__DOT__mem_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_acmp_q__DOT__mem_r__v0][12U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_acmp_q__DOT__mem_r__v0[12U];
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__nvm_wready_w 
        = ((5U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__st_r)) 
           | (8U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__st_r)));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__nvm_rvalid_w 
        = ((4U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__st_r)) 
           | (1U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__st_r)));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__fl_arm_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__fl_arm_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__fl_any_w = 0U;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__fl_pick_w = 0U;
    if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__dirty_r))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__fl_any_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__fl_pick_w = 0U;
    }
    if (((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__fl_any_w)) 
         & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__dirty_r) 
            >> 1U))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__fl_any_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__fl_pick_w = 1U;
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__fl_retry_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__fl_retry_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__rcrc_rx_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__rcrc_rx_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__rplen_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__rplen_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__state_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__state_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pool_wr_valid_w = 0U;
    vlSelfRef.milan_datapath__DOT__avtprx_stopped_w = 0U;
    if ((0U == (IData)(vlSelfRef.milan_datapath__DOT__avtprx_accept_idx_w))) {
        vlSelfRef.milan_datapath__DOT__avtprx_stopped_w 
            = (1U & (IData)(vlSelfRef.milan_datapath__DOT__acmpl_stopped_v_w));
    }
    if ((1U == (IData)(vlSelfRef.milan_datapath__DOT__avtprx_accept_idx_w))) {
        vlSelfRef.milan_datapath__DOT__avtprx_stopped_w 
            = (1U & ((IData)(vlSelfRef.milan_datapath__DOT__acmpl_stopped_v_w) 
                     >> 1U));
    }
    if (vlSelfRef.milan_datapath__DOT__crf_rx__DOT__w_acc) {
        vlSelfRef.milan_datapath__DOT__crf_rx__DOT__hist_old_r 
            = vlSelfRef.milan_datapath__DOT__crf_rx__DOT__ts_hist_r
            [vlSelfRef.milan_datapath__DOT__crf_rx__DOT__hidx_r];
    }
    if (vlSelfRef.axis_resetn) {
        if ((0xffU <= (IData)(vlSelfRef.milan_datapath__DOT__crf_rx__DOT__iv_div_r))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__crf_rx__DOT__iv_div_r = 0U;
            vlSelfRef.milan_datapath__DOT__crf_rx__DOT__iv_tick_r = 1U;
        } else {
            vlSelfRef.__Vdly__milan_datapath__DOT__crf_rx__DOT__iv_div_r 
                = (0x000000ffU & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__crf_rx__DOT__iv_div_r)));
            vlSelfRef.milan_datapath__DOT__crf_rx__DOT__iv_tick_r = 0U;
        }
        if (vlSelfRef.milan_datapath__DOT__crf_rx__DOT__w_hit) {
            if (vlSelfRef.milan_datapath__DOT__crf_rx__DOT__w_fmt_ok) {
                vlSelfRef.milan_datapath__DOT__crf_rx__DOT__ts_new_r 
                    = (IData)(vlSelfRef.milan_datapath__DOT__crf_rx__DOT__w_crf_ts);
                vlSelfRef.milan_datapath__DOT__crf_rx__DOT__exp_seq_r 
                    = (0x000000ffU & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__avtprx_seq)));
            }
        }
        vlSelfRef.milan_datapath__DOT__g_aif_i2s__DOT__aaf_capture__DOT__u_tcdc__DOT__wgray_r1_r 
            = vlSelfRef.milan_datapath__DOT__g_aif_i2s__DOT__aaf_capture__DOT__u_tcdc__DOT__wptr_gray_r;
        if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_mrp_strip__DOT__avail_w) 
             & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_mrp_strip__DOT__space_w))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_mrp_strip__DOT__ram_q_r 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_mrp_strip__DOT__ram_r
                [(0x000007ffU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_mrp_strip__DOT__rd_ptr_r))];
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_mrp_strip__DOT__rd_ptr_r 
                = (0x00000fffU & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_mrp_strip__DOT__rd_ptr_r)));
        }
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__prng_req_w = 0U;
        if ((1U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pr_req_w) 
                   & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pr_inflight_r) 
                         & (0U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pr_owner_r))))))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pr_pend_r 
                = (1U | (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pr_pend_r));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pr_kind_r 
                = ((0x0003fff8U & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pr_kind_r) 
                   | (7U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pr_kind_w));
        }
        if ((1U & (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pr_req_w) 
                    >> 1U) & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pr_inflight_r) 
                                 & (1U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pr_owner_r))))))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pr_pend_r 
                = (2U | (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pr_pend_r));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pr_kind_r 
                = ((0x0003ffc7U & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pr_kind_r) 
                   | (0x00000038U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pr_kind_w));
        }
        if ((1U & (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pr_req_w) 
                    >> 2U) & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pr_inflight_r) 
                                 & (2U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pr_owner_r))))))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pr_pend_r 
                = (4U | (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pr_pend_r));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pr_kind_r 
                = ((0x0003fe3fU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pr_kind_r) 
                   | (0x000001c0U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pr_kind_w));
        }
        if ((1U & (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pr_req_w) 
                    >> 3U) & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pr_inflight_r) 
                                 & (3U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pr_owner_r))))))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pr_pend_r 
                = (8U | (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pr_pend_r));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pr_kind_r 
                = ((0x0003f1ffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pr_kind_r) 
                   | (0x00000e00U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pr_kind_w));
        }
        if ((1U & (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pr_req_w) 
                    >> 4U) & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pr_inflight_r) 
                                 & (4U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pr_owner_r))))))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pr_pend_r 
                = (0x00000010U | (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pr_pend_r));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pr_kind_r 
                = ((0x00038fffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pr_kind_r) 
                   | (0x00007000U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pr_kind_w));
        }
        if ((IData)((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pr_req_w) 
                      >> 5U) & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pr_inflight_r) 
                                   & (5U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pr_owner_r))))))) {
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pr_pend_r 
                = (0x00000020U | (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pr_pend_r));
            vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pr_kind_r 
                = ((0x00007fffU & vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pr_kind_r) 
                   | (0x00038000U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pr_kind_w));
        }
        if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pr_inflight_r) {
            if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__prng_valid_w) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pr_inflight_r = 0U;
            }
        } else if ((1U & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__busy_r)) 
                          & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__prng_req_w))))) {
            if ((1U & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pr_inflight_r)) 
                       & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pr_pend_r)))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__prng_req_w = 1U;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__prng_kind_w 
                    = (7U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pr_kind_r);
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pr_owner_r = 0U;
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pr_pend_r 
                    = (0x3eU & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pr_pend_r));
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pr_inflight_r = 1U;
            }
            if ((1U & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pr_inflight_r)) 
                       & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pr_pend_r) 
                          >> 1U)))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__prng_req_w = 1U;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__prng_kind_w 
                    = (7U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pr_kind_r 
                             >> 3U));
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pr_owner_r = 1U;
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pr_pend_r 
                    = (0x3dU & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pr_pend_r));
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pr_inflight_r = 1U;
            }
            if ((1U & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pr_inflight_r)) 
                       & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pr_pend_r) 
                          >> 2U)))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__prng_req_w = 1U;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__prng_kind_w 
                    = (7U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pr_kind_r 
                             >> 6U));
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pr_owner_r = 2U;
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pr_pend_r 
                    = (0x3bU & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pr_pend_r));
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pr_inflight_r = 1U;
            }
            if ((1U & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pr_inflight_r)) 
                       & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pr_pend_r) 
                          >> 3U)))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__prng_req_w = 1U;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__prng_kind_w 
                    = (7U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pr_kind_r 
                             >> 9U));
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pr_owner_r = 3U;
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pr_pend_r 
                    = (0x37U & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pr_pend_r));
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pr_inflight_r = 1U;
            }
            if ((1U & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pr_inflight_r)) 
                       & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pr_pend_r) 
                          >> 4U)))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__prng_req_w = 1U;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__prng_kind_w 
                    = (7U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pr_kind_r 
                             >> 0x0cU));
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pr_owner_r = 4U;
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pr_pend_r 
                    = (0x2fU & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pr_pend_r));
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pr_inflight_r = 1U;
            }
            if (((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pr_inflight_r)) 
                 & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pr_pend_r) 
                    >> 5U))) {
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__prng_req_w = 1U;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__prng_kind_w 
                    = (7U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pr_kind_r 
                             >> 0x0fU));
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pr_owner_r = 5U;
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pr_pend_r 
                    = (0x1fU & (IData)(vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pr_pend_r));
                vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pr_inflight_r = 1U;
            }
        }
        if (vlSelfRef.s_axi_awready) {
            if ((0x0920U == (IData)(vlSelfRef.s_axi_awaddr))) {
                vlSelfRef.milan_datapath__DOT__csr__DOT__g_pp_csr__DOT__pp_ctrl_r 
                    = vlSelfRef.s_axi_wdata;
            }
        }
        if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__rs_torn_w) {
            if ((1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__touched_r)))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__valid_r 
                    = (2U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__valid_r));
            }
            if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__touched_r) 
                          >> 1U)))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__valid_r 
                    = (1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__valid_r));
            }
        }
        if (((4U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__hs_r)) 
             & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__fsm_wr_gnt_w))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__valid_r 
                = (((~ ((IData)(1U) << (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__rs_k_r))) 
                    & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__valid_r)) 
                   | (3U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__rvld_q_r) 
                            << (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__rs_k_r))));
        }
        if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__rs_complete_w) 
              & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__rrec_ok_w))) 
             & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__touched_r) 
                   >> (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__rs_k_r))))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__valid_r 
                = ((~ ((IData)(1U) << (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__rs_k_r))) 
                   & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__valid_r));
        }
        if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__rs_empty_w) 
             & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__touched_r) 
                   >> (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__rs_k_r))))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__valid_r 
                = ((~ ((IData)(1U) << (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__rs_k_r))) 
                   & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__valid_r));
        }
        if (vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__in_acc) {
            if (vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__fire) {
                vlSelfRef.milan_datapath__DOT__avtprx_seq 
                    = (0x000000ffU & ((((0U == (0x0000001fU 
                                                & (((IData)(0x01bfU) 
                                                    - 
                                                    (0x000001f8U 
                                                     & (((IData)(4U) 
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
                                                          & (((IData)(4U) 
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
                                                        & (((IData)(4U) 
                                                            + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__et_off)) 
                                                           << 3U))) 
                                                      - (IData)(7U)))))) 
                                       | (vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__hdr
                                          [(0x0000000fU 
                                            & ((((IData)(0x01bfU) 
                                                 - 
                                                 (0x000001f8U 
                                                  & (((IData)(4U) 
                                                      + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__et_off)) 
                                                     << 3U))) 
                                                - (IData)(7U)) 
                                               >> 5U))] 
                                          >> (0x0000001fU 
                                              & (((IData)(0x01bfU) 
                                                  - 
                                                  (0x000001f8U 
                                                   & (((IData)(4U) 
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
                                                          & (((IData)(4U) 
                                                              + (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__et_off)) 
                                                             << 3U))) 
                                                        - (IData)(7U))))))));
            }
        }
        if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__go_take_w) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__touched_r = 0U;
        }
        if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__c1_wr_w) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__valid_r 
                = (((~ ((IData)(1U) << (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__c1_sink_r))) 
                    & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__valid_r)) 
                   | (3U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__c1_vld_r) 
                            << (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__c1_sink_r))));
            if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__go_take_w) 
                 | (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_260))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__touched_r 
                    = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__touched_r) 
                       | (3U & ((IData)(1U) << (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__c1_sink_r))));
            }
        }
    } else {
        vlSelfRef.__Vdly__milan_datapath__DOT__crf_rx__DOT__iv_div_r = 0U;
        vlSelfRef.milan_datapath__DOT__crf_rx__DOT__iv_tick_r = 0U;
        vlSelfRef.milan_datapath__DOT__crf_rx__DOT__ts_new_r = 0U;
        vlSelfRef.milan_datapath__DOT__crf_rx__DOT__exp_seq_r = 0U;
        vlSelfRef.milan_datapath__DOT__g_aif_i2s__DOT__aaf_capture__DOT__u_tcdc__DOT__wgray_r1_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_mrp_strip__DOT__rd_ptr_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_mrp_strip__DOT__ram_q_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pr_pend_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pr_kind_r = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__prng_req_w = 0U;
        vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pr_inflight_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pr_owner_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__prng_kind_w = 0U;
        vlSelfRef.milan_datapath__DOT__csr__DOT__g_pp_csr__DOT__pp_ctrl_r = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__valid_r = 0U;
        vlSelfRef.milan_datapath__DOT__avtprx_seq = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__touched_r = 0U;
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__void_hard_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__reload_ok_w) 
           | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__rebase_w));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__sb_rel_acmp_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__acmp_sb_active_r) 
           & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__acmp_sb_done_pending_r) 
              | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__acmp_sb_done_w)));
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
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_decoder__DOT__len_ok_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_decoder__DOT__app_msrp_r)
            ? ((1U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_decoder__DOT__attr_type_r))
                ? (0x19U == (0x000000ffU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_mrp_strip__DOT__out_ent_r)))
                : ((2U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_decoder__DOT__attr_type_r))
                    ? (0x22U == (0x000000ffU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_mrp_strip__DOT__out_ent_r)))
                    : ((3U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_decoder__DOT__attr_type_r))
                        ? (8U == (0x000000ffU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_mrp_strip__DOT__out_ent_r)))
                        : ((4U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_decoder__DOT__attr_type_r)) 
                           & (4U == (0x000000ffU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_mrp_strip__DOT__out_ent_r)))))))
            : ((1U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_decoder__DOT__attr_type_r)) 
               & (2U == (0x000000ffU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_mrp_strip__DOT__out_ent_r)))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_decoder__DOT__accept_w 
        = ((~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_265)) 
           & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_mrp_strip__DOT__out_vld_r));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_mrp_strip__DOT__fetch_r 
        = ((IData)(vlSelfRef.axis_resetn) && ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_mrp_strip__DOT__avail_w) 
                                              & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_mrp_strip__DOT__space_w)));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__ntfy_stri_in_w 
        = ((2U & ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__sink_r) 
                    & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_244)) 
                   | ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_243) 
                      >> 1U)) << 1U)) | (1U & (((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__sink_r)) 
                                                & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_244)) 
                                               | (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_243))));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_121 = (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__rec_r[5U])) 
                                                   << 0x00000020U) 
                                                  | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__rec_r[4U])));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__b_cc_w = 0U;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__b_flags_w = 0U;
    if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__bk_r))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__b_flags_w = 2U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__b_tkuid_w 
            = (0x0000ffffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__rec_r[3U]);
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__b_tkeid_w 
            = (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__rec_r[2U])) 
                << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__rec_r[1U])));
    } else if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__bk_r))) {
        if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__bk_r))) {
            if ((0x00000800U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__rec_r[0U])) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__b_flags_w 
                    = (2U | (((0x00002000U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__rec_r[0U])
                               ? 8U : 0U) | ((IData)(
                                                     (0x00010007U 
                                                      == 
                                                      (0x00010007U 
                                                       & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__rec_r[0U])))
                                              ? 0x0040U
                                              : 0U)));
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__b_tkuid_w 
                    = (0x0000ffffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__rec_r[3U]);
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__b_tkeid_w 
                    = (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__rec_r[2U])) 
                        << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__rec_r[1U])));
            } else {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__b_flags_w = 0U;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__b_tkuid_w 
                    = (0x0000ffffU & 0U);
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__b_tkeid_w = 0ULL;
            }
        } else {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__b_tkuid_w 
                = (0x0000ffffU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__tk_uid_f_r));
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__b_tkeid_w 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__tk_eid_f_r;
        }
    } else {
        if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__bk_r))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__b_flags_w 
                = (8U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__flags_f_r));
        }
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__b_tkuid_w 
            = (0x0000ffffU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__tk_uid_f_r));
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__b_tkeid_w 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__tk_eid_f_r;
    }
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_197 = (1U 
                                                  & ((~ 
                                                      (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__rec_r[0U] 
                                                       >> 0x00000012U)) 
                                                     & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__trom_rdata_r 
                                                        >> 0x00000016U)));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_122 = (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__tk_eid_f_r 
                                                  == 
                                                  (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__rec_r[2U])) 
                                                    << 0x00000020U) 
                                                   | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__rec_r[1U]))));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_123 = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__tk_uid_f_r) 
                                                  == 
                                                  (0x0000ffffU 
                                                   & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__rec_r[3U]));
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__settled_w 
        = ((6U == (7U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__rec_r[0U])) 
           | (7U == (7U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__rec_r[0U])));
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
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__cmp_z_w 
        = ((3U == (7U & (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__uop_e_r 
                                 >> 0x0000001cU))))
            ? (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__opa_e_r 
               == vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__b_or_imm_w)
            : (0U == (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_115)));
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
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__rec_we_w = 0U;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__rec_waddr_w = 0U;
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__txn_initset_w = 0U;
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__txn_rec2_w[0U] 
        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__rec_q_r[0U];
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__txn_rec2_w[1U] 
        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__rec_q_r[1U];
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__txn_rec2_w[2U] 
        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__rec_q_r[2U];
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__txn_open_w = 0U;
    if (milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ping_w) {
        if ((0U == (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__rec_q_r[2U] 
                          >> 0x00000012U)))) {
            milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__txn_initset_w = 1U;
        }
        milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__txn_rec2_w[1U] 
            = ((0x0000ffffU & milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__txn_rec2_w[1U]) 
               | ((IData)((0x0000000100000000ULL | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__now_ms_r)))) 
                  << 0x00000010U));
        milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__txn_rec2_w[2U] 
            = ((0x000e0000U & milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__txn_rec2_w[2U]) 
               | (0x000fffffU & (((IData)((0x0000000100000000ULL 
                                           | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__now_ms_r)))) 
                                  >> 0x00000010U) | 
                                 ((IData)(((0x0000000100000000ULL 
                                            | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__now_ms_r))) 
                                           >> 0x00000020U)) 
                                  << 0x00000010U))));
        if ((IData)(((0x00040000U == (0x000c0000U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__rec_q_r[2U])) 
                     & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__da_ok_w)))) {
            milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__txn_rec2_w[2U] 
                = (0x00080000U | (0x0003ffffU & milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__txn_rec2_w[2U]));
            milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__txn_open_w = 1U;
        }
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_arm_valid_w = 0U;
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_arm_cancel_w = 0U;
    if ((1U & (~ (((4U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__state_r)) 
                   & (IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ping_w)) 
                  & (3U != (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__rec_q_r[2U] 
                                  >> 0x00000012U))))))) {
        if ((6U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__state_r))) {
            if ((1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_arm_fresh_w)))) {
                if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_cancel_w) {
                    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_arm_cancel_w = 1U;
                }
            }
        }
    }
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_arm_deadline_w = 0U;
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_arm_owner_w = 0U;
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_arm_slot_w = 0U;
    if ((((4U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__state_r)) 
          & (IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ping_w)) 
         & (3U != (3U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__rec_q_r[2U] 
                         >> 0x00000012U))))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_arm_valid_w = 1U;
        milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_arm_deadline_w 
            = ((IData)(0x00003a98U) + vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__now_ms_r);
        milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_arm_owner_w 
            = (0x000000ffU & ((IData)(0x50U) + (1U 
                                                & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__txn_r[1U] 
                                                   >> 0x0000001cU))));
        milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_arm_slot_w 
            = (0x0000003fU & ((IData)(5U) + (1U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__txn_r[1U] 
                                                   >> 0x0000001cU))));
    } else if ((6U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__state_r))) {
        if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_arm_fresh_w) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_arm_valid_w = 1U;
            milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_arm_deadline_w 
                = ((IData)(0x00003a98U) + ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__rec_q_r[2U] 
                                            << 0x00000010U) 
                                           | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__rec_q_r[1U] 
                                              >> 0x00000010U)));
            milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_arm_owner_w 
                = (0x000000ffU & ((IData)(0x50U) + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_src_r)));
            milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_arm_slot_w 
                = (0x0000003fU & ((IData)(5U) + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_src_r)));
        } else if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_cancel_w) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_arm_valid_w = 1U;
            milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_arm_owner_w 
                = (0x000000ffU & ((IData)(0x50U) + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_src_r)));
            milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_arm_slot_w 
                = (0x0000003fU & ((IData)(5U) + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_src_r)));
        }
    } else if ((9U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__state_r))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_arm_valid_w = 1U;
        milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_arm_deadline_w 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__arm_deadline_r;
        milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_arm_owner_w 
            = (0x000000ffU & ((IData)(0x50U) + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_src_r)));
        milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_arm_slot_w 
            = (0x0000003fU & ((IData)(5U) + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_src_r)));
    }
    __VdfgRegularize_h6e95ff9d_0_196 = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__ev_cancel_w) 
                                        | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__ev_rsp_w));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__ca_txs_gnt_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__txc_locked_r) 
           & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__alloc_gnt_r) 
              & (6U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__txc_owner_r))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_txs_gnt_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__txc_locked_r) 
           & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__alloc_gnt_r) 
              & (2U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__txc_owner_r))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__evr_pay_w 
        = (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r
           [vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__sel_r] 
           & (- (IData)((0x0aU >= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__sel_r)))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__lstn_evt_tk_valid_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__valid_r) 
           & (5U >= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__sel_r)));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_73 = (0x0000ffffffffffffULL 
                                                 & (((QData)((IData)(Vmilan_datapath__ConstPool__CONST_hfd3d218a_0
                                                                     [
                                                                     (((IData)(0x0000002fU) 
                                                                       + 
                                                                       ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__kind_r) 
                                                                        << 6U)) 
                                                                      >> 5U)])) 
                                                     << 0x00000020U) 
                                                    | (QData)((IData)(Vmilan_datapath__ConstPool__CONST_hfd3d218a_0
                                                                      [
                                                                      (0x07fffffeU 
                                                                       & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__kind_r) 
                                                                          << 1U))]))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__txn_in_w[0U] 
        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_acmp_q__DOT__out_data_r[0U];
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__txn_in_w[1U] 
        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_acmp_q__DOT__out_data_r[1U];
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__txn_in_w[2U] 
        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_acmp_q__DOT__out_data_r[2U];
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__txn_in_w[3U] 
        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_acmp_q__DOT__out_data_r[3U];
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__txn_in_w[4U] 
        = (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pf_eid_r) 
            << 0x0000001eU) | (0x3fffffffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_acmp_q__DOT__out_data_r[4U]));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__txn_in_w[5U] 
        = (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pf_eid_r) 
            >> 2U) | ((IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pf_eid_r 
                               >> 0x00000020U)) << 0x0000001eU));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__txn_in_w[6U] 
        = ((0xc0000000U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_acmp_q__DOT__out_data_r[6U]) 
           | ((IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pf_eid_r 
                       >> 0x00000020U)) >> 2U));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__txn_in_w[7U] 
        = ((0x3fffffffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_acmp_q__DOT__out_data_r[7U]) 
           | (0xc0000000U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_acmp_q__DOT__out_data_r[7U]));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__txn_in_w[8U] 
        = ((0x3fffffffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_acmp_q__DOT__out_data_r[8U]) 
           | (0xc0000000U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_acmp_q__DOT__out_data_r[8U]));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__txn_in_w[9U] 
        = ((0x3fffffffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_acmp_q__DOT__out_data_r[9U]) 
           | (0xc0000000U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_acmp_q__DOT__out_data_r[9U]));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__txn_in_w[10U] 
        = ((0x3fffffffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_acmp_q__DOT__out_data_r[10U]) 
           | (0xc0000000U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_acmp_q__DOT__out_data_r[10U]));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__txn_in_w[11U] 
        = ((0x3fffffffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_acmp_q__DOT__out_data_r[11U]) 
           | (0xc0000000U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_acmp_q__DOT__out_data_r[11U]));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__txn_in_w[12U] 
        = (0x000001ffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_acmp_q__DOT__out_data_r[12U]);
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__acmp_is_tkr_w 
        = ((0U == (0x0000000fU & ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_acmp_q__DOT__out_data_r[11U] 
                                   << 2U) | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_acmp_q__DOT__out_data_r[10U] 
                                             >> 0x0000001eU)))) 
           | ((2U == (0x0000000fU & ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_acmp_q__DOT__out_data_r[11U] 
                                      << 2U) | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_acmp_q__DOT__out_data_r[10U] 
                                                >> 0x0000001eU)))) 
              | ((4U == (0x0000000fU & ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_acmp_q__DOT__out_data_r[11U] 
                                         << 2U) | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_acmp_q__DOT__out_data_r[10U] 
                                                   >> 0x0000001eU)))) 
                 | (0x0cU == (0x0000000fU & ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_acmp_q__DOT__out_data_r[11U] 
                                              << 2U) 
                                             | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_acmp_q__DOT__out_data_r[10U] 
                                                >> 0x0000001eU)))))));
    __VdfgRegularize_h6e95ff9d_0_120 = (0x000000ffU 
                                        & ((0x14U > (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__fl_sidx_r))
                                            ? (((0U 
                                                 == 
                                                 (0x0000001fU 
                                                  & ((IData)(0x00000040U) 
                                                     + 
                                                     (0x00000038U 
                                                      & (((IData)(3U) 
                                                          - (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__fl_sidx_r)) 
                                                         << 3U)))))
                                                 ? 0U
                                                 : 
                                                (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__fl_fields_r
                                                 [(
                                                   ((IData)(0x00000047U) 
                                                    + 
                                                    (0x00000038U 
                                                     & (((IData)(3U) 
                                                         - (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__fl_sidx_r)) 
                                                        << 3U))) 
                                                   >> 5U)] 
                                                 << 
                                                 ((IData)(0x00000020U) 
                                                  - 
                                                  (0x0000001fU 
                                                   & ((IData)(0x00000040U) 
                                                      + 
                                                      (0x00000038U 
                                                       & (((IData)(3U) 
                                                           - (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__fl_sidx_r)) 
                                                          << 3U))))))) 
                                               | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__fl_fields_r
                                                  [
                                                  (((IData)(0x00000040U) 
                                                    + 
                                                    (0x00000038U 
                                                     & (((IData)(3U) 
                                                         - (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__fl_sidx_r)) 
                                                        << 3U))) 
                                                   >> 5U)] 
                                                  >> 
                                                  (0x0000001fU 
                                                   & ((IData)(0x00000040U) 
                                                      + 
                                                      (0x00000038U 
                                                       & (((IData)(3U) 
                                                           - (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__fl_sidx_r)) 
                                                          << 3U))))))
                                            : (((0U 
                                                 == 
                                                 (0x00000018U 
                                                  & (((IData)(3U) 
                                                      - (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__fl_sidx_r)) 
                                                     << 3U)))
                                                 ? 0U
                                                 : 
                                                (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__fl_fields_r
                                                 [(
                                                   ((IData)(7U) 
                                                    + 
                                                    (0x00000038U 
                                                     & (((IData)(3U) 
                                                         - (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__fl_sidx_r)) 
                                                        << 3U))) 
                                                   >> 5U)] 
                                                 << 
                                                 ((IData)(0x00000020U) 
                                                  - 
                                                  (0x00000018U 
                                                   & (((IData)(3U) 
                                                       - (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__fl_sidx_r)) 
                                                      << 3U))))) 
                                               | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__fl_fields_r
                                                  [
                                                  (1U 
                                                   & (((IData)(3U) 
                                                       - (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__fl_sidx_r)) 
                                                      >> 2U))] 
                                                  >> 
                                                  (0x00000018U 
                                                   & (((IData)(3U) 
                                                       - (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__fl_sidx_r)) 
                                                      << 3U))))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__nvm_busy_w 
        = ((0U != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__state_r)) 
           & (0x0fU != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__state_r)));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__nvm_rdata_w 
        = ((0x0bU == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__state_r))
            ? vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__hdr_r
           [vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__hidx_r]
            : (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__nvm_rdata_w));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__nvm_req_w 
        = ((2U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__state_r)) 
           | ((4U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__state_r)) 
              | ((8U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__state_r)) 
                 | (0x0cU == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__state_r)))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__nvm_err_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__err_r) 
           & (0x0fU == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__state_r)));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__nvm_done_w 
        = ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__err_r)) 
           & (0x0fU == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__state_r)));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__nvm_offset_w = 0U;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__nvm_len_w = 0U;
    if ((8U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__state_r))) {
        if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__state_r))) {
            if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__state_r) 
                          >> 1U)))) {
                if ((1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__state_r)))) {
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__nvm_offset_w = 8U;
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__nvm_len_w 
                        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__plen_r;
                }
            }
        } else if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__state_r) 
                             >> 1U)))) {
            if ((1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__state_r)))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__nvm_len_w = 8U;
            }
        }
    } else if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__state_r))) {
        if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__state_r) 
                      >> 1U)))) {
            if ((1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__state_r)))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__nvm_len_w 
                    = (0x0000ffffU & ((IData)(8U) + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__plen_r)));
            }
        }
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__nvm_op_w = 0U;
    if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__state_r) 
                  >> 3U)))) {
        if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__state_r))) {
            if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__state_r) 
                          >> 1U)))) {
                if ((1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__state_r)))) {
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__nvm_op_w = 1U;
                }
            }
        } else if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__state_r))) {
            if ((1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__state_r)))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__nvm_op_w = 2U;
            }
        }
    }
    if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__cap_active_w) 
         | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__fsm_rd_req_w))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__shw_rdata_r[0U] 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__shw_ram_r
            [((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__cap_active_w)
               ? (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__recwr_addr_w)
               : ((5U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__hs_r))
                   ? (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__rp_k_r)
                   : (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__fl_sink_r)))][0U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__shw_rdata_r[1U] 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__shw_ram_r
            [((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__cap_active_w)
               ? (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__recwr_addr_w)
               : ((5U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__hs_r))
                   ? (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__rp_k_r)
                   : (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__fl_sink_r)))][1U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__shw_rdata_r[2U] 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__shw_ram_r
            [((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__cap_active_w)
               ? (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__recwr_addr_w)
               : ((5U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__hs_r))
                   ? (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__rp_k_r)
                   : (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__fl_sink_r)))][2U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__shw_rdata_r[3U] 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__shw_ram_r
            [((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__cap_active_w)
               ? (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__recwr_addr_w)
               : ((5U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__hs_r))
                   ? (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__rp_k_r)
                   : (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__fl_sink_r)))][3U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__shw_rdata_r[4U] 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__shw_ram_r
            [((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__cap_active_w)
               ? (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__recwr_addr_w)
               : ((5U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__hs_r))
                   ? (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__rp_k_r)
                   : (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__fl_sink_r)))][4U];
    }
    vlSelfRef.milan_datapath__DOT__avtprx_accept_p 
        = ((~ (IData)(vlSelfRef.milan_datapath__DOT__avtprx_stopped_w)) 
           & (IData)(vlSelfRef.milan_datapath__DOT__avtprx_accept_p_w));
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__crf_rx__DOT__ts_hist_r__v0) {
        vlSelfRef.milan_datapath__DOT__crf_rx__DOT__ts_hist_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__crf_rx__DOT__ts_hist_r__v0] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__crf_rx__DOT__ts_hist_r__v0;
    }
    vlSelfRef.milan_datapath__DOT__crf_rx__DOT__hidx_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__crf_rx__DOT__hidx_r;
    vlSelfRef.milan_datapath__DOT__crf_rx__DOT__iv_div_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__crf_rx__DOT__iv_div_r;
    vlSelfRef.milan_datapath__DOT__crf_rx__DOT__w_crf_ts 
        = (((QData)((IData)(vlSelfRef.milan_datapath__DOT__avtprx_fsh)) 
            << 0x00000020U) | (QData)((IData)((vlSelfRef.milan_datapath__DOT__avtprx_fsh2 
                                               >> 0x00000020U))));
    vlSelfRef.milan_datapath__DOT__crf_rx__DOT__w_fmt_ok 
        = (IData)((((1U == (IData)(vlSelfRef.milan_datapath__DOT__avtprx_b3)) 
                    & (0x0000bb80U == vlSelfRef.milan_datapath__DOT__avtprx_ts)) 
                   & (0x0008006000000000ULL == (0xffffffff00000000ULL 
                                                & vlSelfRef.milan_datapath__DOT__avtprx_fsh))));
    vlSelfRef.milan_datapath__DOT__crf_rx__DOT__w_hit 
        = ((IData)(vlSelfRef.milan_datapath__DOT__avtprx_parse_p) 
           & ((IData)(vlSelfRef.milan_datapath__DOT____Vcellinp__crf_rx__en_i) 
              & ((4U == (IData)(vlSelfRef.milan_datapath__DOT__avtprx_subtype)) 
                 & (vlSelfRef.milan_datapath__DOT__avtprx_sid_frame 
                    == ((2U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__bound_hold_r))
                         ? (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__bound_sid_r[3U])) 
                             << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__bound_sid_r[2U])))
                         : (((QData)((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__crf_sidhi)) 
                             << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__crf_sidlo))))))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__close_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__cap_open_r) 
           & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__release_w) 
              | (((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_193) 
                  & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__commit_ack_w)) 
                 | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__void_hard_w))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__arm_ok_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__arm_w) 
           & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__img_live_w) 
              & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__void_hard_w)) 
                 & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__cap_open_r)) 
                    & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__mut_defer_r)) 
                       & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__ld_acc_r))))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__ack_ok_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__commit_ack_w) 
           & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__cap_open_r) 
              & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__cap_att_r) 
                 & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__cap_valid_r) 
                    & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__void_hard_w)) 
                       & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_193))))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__sb_rel_id_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__sb_rel_acmp_w)
            ? (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__acmp_sb_id_r)
            : (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__aecp_sb_id_r));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__sb_rel_aecp_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__aecp_sb_active_r) 
           & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__sb_rel_acmp_w)) 
              & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__aecp_sb_done_pending_r) 
                 | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__aecp_sb_done_w))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__ind_reg_w 
        = (((((0U == (3U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r) 
                            >> 2U))) | ((2U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_attr_type_w)) 
                                        != (1U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rtype_r) 
                                                  >> 1U)))) 
             & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_235)) 
            << 1U) | (((0U == (3U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r))) 
                       | ((2U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_attr_type_w)) 
                          != (1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rtype_r)))) 
                      & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_236)));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__ind_unreg_w 
        = ((((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__exp_hit_w) 
               & (8U == (0x0cU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r)))) 
              & ((1U == ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__chk_slot_r) 
                         - (IData)(0x0000003bU))) & 
                 (~ ((1U == (3U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__tpend_r) 
                                   >> 2U))) | (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_235))))) 
             | (((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_67) 
                 & (5U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_mrp_event_w))) 
                & (4U == (0x0cU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r))))) 
            << 1U) | (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__exp_hit_w) 
                       & ((0U == ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__chk_slot_r) 
                                  - (IData)(0x0000003bU))) 
                          & ((~ ((1U == (3U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__tpend_r))) 
                                 | (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_236))) 
                             & (2U == (3U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r)))))) 
                      | ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_68) 
                         & ((5U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_mrp_event_w)) 
                            & (1U == (3U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r)))))));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_15 = ((~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_38)) 
                                                 & ((~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_65)) 
                                                    & ((~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_64)) 
                                                       & ((~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_49)) 
                                                          & ((~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_37)) 
                                                             & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_63))))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__adm_grant_w 
        = ((((~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_22)) 
             & ((~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_36)) 
                & ((~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_35)) 
                   & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_30)))) 
            << 1U) | ((~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_38)) 
                      & ((~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_65)) 
                         & ((~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_64)) 
                            & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_49)))));
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_rx_hit_w 
        = (((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_22) 
            << 1U) | (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_38));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__per_grant_w 
        = ((((~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_22)) 
             & ((~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_36)) 
                & ((~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_35)) 
                   & ((~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_30)) 
                      & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_34))))) 
            << 1U) | ((~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_38)) 
                      & ((~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_65)) 
                         & ((~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_64)) 
                            & ((~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_49)) 
                               & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_37))))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_ev_v_w 
        = ((((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_22) 
             | ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_36) 
                | ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_35) 
                   | ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_30) 
                      | ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_58) 
                         | (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_34)))))) 
            << 1U) | ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_38) 
                      | ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_65) 
                         | ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_49) 
                            | ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_37) 
                               | ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_63) 
                                  | (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_64)))))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_ev_w 
        = ((0x000000f0U & (((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_22)
                             ? ((IData)(3U) + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_mrp_event_w))
                             : ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_36)
                                 ? ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_open_r)
                                     ? (1U & (- (IData)(
                                                        (1U 
                                                         & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rec_valid_r) 
                                                            >> 1U)))))
                                     : 2U) : ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_35)
                                               ? 9U
                                               : (((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_34)
                                                    ? 0x0aU
                                                    : 
                                                   ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_58)
                                                     ? 
                                                    ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__wtxla_r)
                                                      ? 0x0cU
                                                      : 0x0bU)
                                                     : 3U)) 
                                                  & (- (IData)(
                                                               (1U 
                                                                & (~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_30))))))))) 
                           << 4U)) | (0x0000000fU & 
                                      ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_38)
                                        ? ((IData)(3U) 
                                           + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_mrp_event_w))
                                        : ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_65)
                                            ? ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_open_r)
                                                ? (1U 
                                                   & (- (IData)(
                                                                (1U 
                                                                 & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rec_valid_r)))))
                                                : 2U)
                                            : ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_64)
                                                ? 9U
                                                : (
                                                   ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_37)
                                                     ? 0x0aU
                                                     : 
                                                    ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_63)
                                                      ? 
                                                     ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__wtxla_r)
                                                       ? 0x0cU
                                                       : 0x0bU)
                                                      : 3U)) 
                                                   & (- (IData)(
                                                                (1U 
                                                                 & (~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_49)))))))))));
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_mrp_strip__DOT__ram_r__v0) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_mrp_strip__DOT__ram_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_mrp_strip__DOT__ram_r__v0] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_mrp_strip__DOT__ram_r__v0;
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__res_acts_w 
        = (0x0001ffffU & ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_197)
                           ? (0x00010000U | ((0x0000f000U 
                                              & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__trom_rdata_r 
                                                 >> 3U)) 
                                             | (0x000007ffU 
                                                & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__trom_rdata_r 
                                                   >> 3U))))
                           : (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__trom_rdata_r 
                              >> 3U)));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__evt_w 
        = (0x0000000fU & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__src_txn_r)
                           ? ((6U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__msg_x_r))
                               ? (1U & (- (IData)((1U 
                                                   & (~ 
                                                      ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_122) 
                                                       & ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_123) 
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
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__b_vlan_w = 0U;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__b_da_w = 0ULL;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__b_sid_w = 0ULL;
    if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__bk_r) 
                  >> 2U)))) {
        if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__bk_r))) {
            if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__bk_r))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__b_cc_w 
                    = ((0x00000800U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__rec_r[0U])
                        ? 1U : 0U);
                if (milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__settled_w) {
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
        } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__bk_r))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__b_cc_w = 1U;
        }
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__br_taken_w = 0U;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__take_wr_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT____Vcellinp__u_store__st_req_i) 
           & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__st_we_w) 
              & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__store_ready_w)));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__take_rd_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT____Vcellinp__u_store__st_req_i) 
           & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__st_we_w)) 
              & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__req_seen_r)) 
                 & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__store_ready_w))));
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__dyn_ready_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__st_we_w) 
           & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT____Vcellinp__u_dyn__st_req_i));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__set_init_w = 0U;
    if ((1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__en_q_r)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__set_init_w 
            = (1U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__set_init_w));
    }
    if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__en_q_r) 
                  >> 1U)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__set_init_w 
            = (2U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__set_init_w));
    }
    if (((4U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__state_r)) 
         & (IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__txn_initset_w))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__set_init_w 
            = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__set_init_w) 
               | (3U & ((IData)(1U) << (1U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__txn_r[1U] 
                                              >> 0x0000001cU)))));
    }
    if (((6U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__state_r)) 
         & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_initset_w))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__set_init_w 
            = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__set_init_w) 
               | (3U & ((IData)(1U) << (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_src_r))));
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__rec_wdata_w[0U] = 0U;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__rec_wdata_w[1U] = 0U;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__rec_wdata_w[2U] = 0U;
    if ((0U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__state_r))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__rec_we_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__rec_waddr_w 
            = (1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__init_ix_r));
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__rec_wdata_w[0U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__rec_wdata_w[1U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__rec_wdata_w[2U] = 0U;
    } else if ((1U != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__state_r))) {
        if ((4U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__state_r))) {
            if (milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ping_w) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__rec_we_w = 1U;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__rec_waddr_w 
                    = (1U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__txn_r[1U] 
                             >> 0x0000001cU));
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__rec_wdata_w[0U] 
                    = milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__txn_rec2_w[0U];
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__rec_wdata_w[1U] 
                    = milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__txn_rec2_w[1U];
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__rec_wdata_w[2U] 
                    = milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__txn_rec2_w[2U];
            }
        } else if ((6U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__state_r))) {
            if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_we_w) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__rec_we_w = 1U;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__rec_waddr_w 
                    = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_src_r;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__rec_wdata_w[0U] 
                    = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_rec2_w[0U];
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__rec_wdata_w[1U] 
                    = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_rec2_w[1U];
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__rec_wdata_w[2U] 
                    = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_rec2_w[2U];
            }
        }
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_gate_open_w = 0U;
    if ((4U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__state_r))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_gate_open_w 
            = milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__txn_open_w;
    } else if ((6U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__state_r))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_gate_open_w 
            = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_open_w;
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_vld_w 
        = ((((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__ntfy_mon_arm_valid_w) 
               << 3U) | ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__ntfy_arm_valid_w) 
                         << 2U)) | (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__arm_v_r) 
                                     << 1U) | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__org_arm_valid_w))) 
            << 4U) | ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_arm_valid_w) 
                        << 3U) | ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__adp_arm_valid_w) 
                                  << 2U)) | (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_arm_valid_w) 
                                              << 1U) 
                                             | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__lstn_arm_valid_w))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_push_ok_w 
        = (((((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__ntfy_mon_arm_valid_w) 
                & (4U != (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_273))) 
               << 3U) | (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__ntfy_arm_valid_w) 
                          & (4U != (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_272))) 
                         << 2U)) | ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__arm_v_r) 
                                      & (4U != (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_271))) 
                                     << 1U) | ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__org_arm_valid_w) 
                                               & (4U 
                                                  != (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_270))))) 
            << 4U) | (((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_arm_valid_w) 
                         & (4U != (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_269))) 
                        << 3U) | (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__adp_arm_valid_w) 
                                   & (4U != (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_268))) 
                                  << 2U)) | ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_arm_valid_w) 
                                               & (4U 
                                                  != (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_267))) 
                                              << 1U) 
                                             | ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__lstn_arm_valid_w) 
                                                & (4U 
                                                   != (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_266))))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__clr_arm_w = 0U;
    if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_arm_valid_w) 
         & (2U > ((IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_arm_slot_w) 
                  - (IData)(5U))))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__clr_arm_w 
            = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__clr_arm_w) 
               | (3U & ((IData)(1U) << (1U & ((IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_arm_slot_w) 
                                              - (IData)(1U))))));
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[0U] 
        = (IData)((((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__lstn_arm_cancel_w)) 
                    << 0x0000002eU) | (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__lstn_arm_slot_w)) 
                                        << 0x00000028U) 
                                       | (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__lstn_arm_owner_w)) 
                                           << 0x00000020U) 
                                          | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__lstn_arm_deadline_w))))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[1U] 
        = ((0xffff8000U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[1U]) 
           | (IData)(((((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__lstn_arm_cancel_w)) 
                        << 0x0000002eU) | (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__lstn_arm_slot_w)) 
                                            << 0x00000028U) 
                                           | (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__lstn_arm_owner_w)) 
                                               << 0x00000020U) 
                                              | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__lstn_arm_deadline_w))))) 
                      >> 0x00000020U)));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[1U] 
        = ((0x00007fffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[1U]) 
           | ((IData)((((QData)((IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_arm_cancel_w)) 
                        << 0x0000002eU) | (((QData)((IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_arm_slot_w)) 
                                            << 0x00000028U) 
                                           | (((QData)((IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_arm_owner_w)) 
                                               << 0x00000020U) 
                                              | (QData)((IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_arm_deadline_w)))))) 
              << 0x0000000fU));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[2U] 
        = ((0xc0000000U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[2U]) 
           | (((IData)((((QData)((IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_arm_cancel_w)) 
                         << 0x0000002eU) | (((QData)((IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_arm_slot_w)) 
                                             << 0x00000028U) 
                                            | (((QData)((IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_arm_owner_w)) 
                                                << 0x00000020U) 
                                               | (QData)((IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_arm_deadline_w)))))) 
               >> 0x00000011U) | ((IData)(((((QData)((IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_arm_cancel_w)) 
                                             << 0x0000002eU) 
                                            | (((QData)((IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_arm_slot_w)) 
                                                << 0x00000028U) 
                                               | (((QData)((IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_arm_owner_w)) 
                                                   << 0x00000020U) 
                                                  | (QData)((IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_arm_deadline_w))))) 
                                           >> 0x00000020U)) 
                                  << 0x0000000fU)));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[2U] 
        = ((0x3fffffffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[2U]) 
           | ((IData)((((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__adp_arm_cancel_w)) 
                        << 0x0000002eU) | (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__adp_arm_slot_w)) 
                                            << 0x00000028U) 
                                           | (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__adp_arm_slot_w)) 
                                               << 0x00000020U) 
                                              | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__adp_arm_deadline_w)))))) 
              << 0x0000001eU));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[3U] 
        = (((IData)((((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__adp_arm_cancel_w)) 
                      << 0x0000002eU) | (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__adp_arm_slot_w)) 
                                          << 0x00000028U) 
                                         | (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__adp_arm_slot_w)) 
                                             << 0x00000020U) 
                                            | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__adp_arm_deadline_w)))))) 
            >> 2U) | ((IData)(((((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__adp_arm_cancel_w)) 
                                 << 0x0000002eU) | 
                                (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__adp_arm_slot_w)) 
                                  << 0x00000028U) | 
                                 (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__adp_arm_slot_w)) 
                                   << 0x00000020U) 
                                  | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__adp_arm_deadline_w))))) 
                               >> 0x00000020U)) << 0x0000001eU));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[4U] 
        = ((0xffffe000U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[4U]) 
           | ((IData)(((((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__adp_arm_cancel_w)) 
                         << 0x0000002eU) | (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__adp_arm_slot_w)) 
                                             << 0x00000028U) 
                                            | (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__adp_arm_slot_w)) 
                                                << 0x00000020U) 
                                               | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__adp_arm_deadline_w))))) 
                       >> 0x00000020U)) >> 2U));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[4U] 
        = ((0x00001fffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[4U]) 
           | ((IData)((((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_arm_cancel_w)) 
                        << 0x0000002eU) | (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_arm_slot_w)) 
                                            << 0x00000028U) 
                                           | (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_arm_owner_w)) 
                                               << 0x00000020U) 
                                              | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_arm_deadline_w)))))) 
              << 0x0000000dU));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[5U] 
        = ((0xf0000000U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[5U]) 
           | (((IData)((((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_arm_cancel_w)) 
                         << 0x0000002eU) | (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_arm_slot_w)) 
                                             << 0x00000028U) 
                                            | (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_arm_owner_w)) 
                                                << 0x00000020U) 
                                               | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_arm_deadline_w)))))) 
               >> 0x00000013U) | ((IData)(((((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_arm_cancel_w)) 
                                             << 0x0000002eU) 
                                            | (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_arm_slot_w)) 
                                                << 0x00000028U) 
                                               | (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_arm_owner_w)) 
                                                   << 0x00000020U) 
                                                  | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_arm_deadline_w))))) 
                                           >> 0x00000020U)) 
                                  << 0x0000000dU)));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[5U] 
        = ((0x0fffffffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[5U]) 
           | ((IData)((((QData)((IData)((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__org_arm_cancel_w) 
                                          << 6U) | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__org_arm_slot_w)))) 
                        << 0x00000028U) | (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__org_arm_owner_w)) 
                                            << 0x00000020U) 
                                           | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__org_arm_deadline_w))))) 
              << 0x0000001cU));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[6U] 
        = (((IData)((((QData)((IData)((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__org_arm_cancel_w) 
                                        << 6U) | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__org_arm_slot_w)))) 
                      << 0x00000028U) | (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__org_arm_owner_w)) 
                                          << 0x00000020U) 
                                         | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__org_arm_deadline_w))))) 
            >> 4U) | ((IData)(((((QData)((IData)((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__org_arm_cancel_w) 
                                                   << 6U) 
                                                  | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__org_arm_slot_w)))) 
                                 << 0x00000028U) | 
                                (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__org_arm_owner_w)) 
                                  << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__org_arm_deadline_w)))) 
                               >> 0x00000020U)) << 0x0000001cU));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[7U] 
        = (((0x0ffff800U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__arm_dl_r 
                            << 0x0000000bU)) | ((IData)(
                                                        ((((QData)((IData)(
                                                                           (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__org_arm_cancel_w) 
                                                                             << 6U) 
                                                                            | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__org_arm_slot_w)))) 
                                                           << 0x00000028U) 
                                                          | (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__org_arm_owner_w)) 
                                                              << 0x00000020U) 
                                                             | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__org_arm_deadline_w)))) 
                                                         >> 0x00000020U)) 
                                                >> 4U)) 
           | (0xf0000000U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__arm_dl_r 
                             << 0x0000000bU)));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[8U] 
        = ((0xfffff800U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[8U]) 
           | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__arm_dl_r 
              >> 0x00000015U));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[8U] 
        = ((0xfc0007ffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[8U]) 
           | (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__arm_c_r) 
               << 0x00000019U) | ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__arm_ann_r)
                                     ? 0x31U : 0x30U) 
                                   << 0x00000013U) 
                                  | (0x0007f800U & 
                                     (((IData)(0x90U) 
                                       + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__arm_ann_r)) 
                                      << 0x0000000bU)))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[8U] 
        = ((0x03ffffffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[8U]) 
           | ((IData)((((QData)((IData)((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__ntfy_arm_cancel_w) 
                                          << 6U) | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__ntfy_arm_slot_w)))) 
                        << 0x00000028U) | (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__ntfy_arm_owner_w)) 
                                            << 0x00000020U) 
                                           | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__ntfy_arm_deadline_w))))) 
              << 0x0000001aU));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[9U] 
        = (((IData)((((QData)((IData)((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__ntfy_arm_cancel_w) 
                                        << 6U) | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__ntfy_arm_slot_w)))) 
                      << 0x00000028U) | (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__ntfy_arm_owner_w)) 
                                          << 0x00000020U) 
                                         | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__ntfy_arm_deadline_w))))) 
            >> 6U) | ((IData)(((((QData)((IData)((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__ntfy_arm_cancel_w) 
                                                   << 6U) 
                                                  | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__ntfy_arm_slot_w)))) 
                                 << 0x00000028U) | 
                                (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__ntfy_arm_owner_w)) 
                                  << 0x00000020U) | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__ntfy_arm_deadline_w)))) 
                               >> 0x00000020U)) << 0x0000001aU));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[10U] 
        = (((0x03fffe00U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__ntfy_mon_arm_deadline_w 
                            << 9U)) | ((IData)(((((QData)((IData)(
                                                                  (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__ntfy_arm_cancel_w) 
                                                                    << 6U) 
                                                                   | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__ntfy_arm_slot_w)))) 
                                                  << 0x00000028U) 
                                                 | (((QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__ntfy_arm_owner_w)) 
                                                     << 0x00000020U) 
                                                    | (QData)((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__ntfy_arm_deadline_w)))) 
                                                >> 0x00000020U)) 
                                       >> 6U)) | (0xfc000000U 
                                                  & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__ntfy_mon_arm_deadline_w 
                                                     << 9U)));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[11U] 
        = ((0x00fffe00U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[11U]) 
           | (0x00ffffffU & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__ntfy_mon_arm_deadline_w 
                             >> 0x00000017U)));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[11U] 
        = ((0x000001ffU & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w[11U]) 
           | (0x00ffffffU & (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__ntfy_mon_arm_cancel_w) 
                              << 0x00000017U) | (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__ntfy_mon_arm_slot_w) 
                                                  << 0x00000011U) 
                                                 | ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__ntfy_mon_arm_owner_w) 
                                                    << 9U)))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__ev_accept_w 
        = ((~ (IData)(__VdfgRegularize_h6e95ff9d_0_196)) 
           & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__accept_ok_w));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_txs_alloc_req_w 
        = ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_txs_gnt_w)) 
           & (1U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__st_r)));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__span_w 
        = (0x0000ffffU & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_r) 
                          & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_73)));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pr_kind_w 
        = (0x00020618U | (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__draw_kind_r) 
                           << 0x0000000cU) | ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__draw_req_kind_r) 
                                              << 6U)));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pr_kind_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pr_kind_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__prng_req_w 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__prng_req_w;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__prng_valid_w 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__prng_valid_w;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pr_pend_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pr_pend_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__busy_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__busy_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pr_inflight_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pr_inflight_r;
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
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__nvm_wdata_w 
        = (0x000000ffU & ((0x00000010U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__fl_sidx_r))
                           ? (IData)(__VdfgRegularize_h6e95ff9d_0_120)
                           : ((8U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__fl_sidx_r))
                               ? ((4U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__fl_sidx_r))
                                   ? (IData)(__VdfgRegularize_h6e95ff9d_0_120)
                                   : ((2U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__fl_sidx_r))
                                       ? ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__fl_sidx_r))
                                           ? vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__fl_fields_r[4U]
                                           : ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__fl_fields_r[4U] 
                                               << 0x00000018U) 
                                              | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__fl_fields_r[4U] 
                                                 >> 8U)))
                                       : ((- (IData)(
                                                     (1U 
                                                      & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__fl_sidx_r))))) 
                                          & ((4U & 
                                              (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__fl_fields_r[4U] 
                                               >> 0x0000000eU)) 
                                             | ((2U 
                                                 & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__fl_fields_r[4U] 
                                                    >> 0x00000010U)) 
                                                | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__fl_vld_r))))))
                               : ((4U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__fl_sidx_r))
                                   ? ((2U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__fl_sidx_r))
                                       ? ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__fl_sidx_r))
                                           ? (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__fl_crc_r)
                                           : ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__fl_crc_r) 
                                              >> 8U))
                                       : (0x14U & (- (IData)(
                                                             (1U 
                                                              & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__fl_sidx_r))))))
                                   : ((2U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__fl_sidx_r))
                                       ? ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__fl_sidx_r))
                                           ? (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__nvm_record_id_w)
                                           : 2U) : 
                                      ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__fl_sidx_r))
                                        ? 0x22U : 0x17U))))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__mut_req_w 
        = ((2U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__nvm_op_w)) 
           | (1U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__nvm_op_w)));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__eff_len_w 
        = (((2U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__nvm_op_w)) 
            & (0U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__nvm_len_w)))
            ? (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__rec_len_w)
            : (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__nvm_len_w));
    if (vlSelfRef.__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__shw_ram_r__v0) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__shw_ram_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__shw_ram_r__v0][0U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__shw_ram_r__v0[0U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__shw_ram_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__shw_ram_r__v0][1U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__shw_ram_r__v0[1U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__shw_ram_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__shw_ram_r__v0][2U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__shw_ram_r__v0[2U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__shw_ram_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__shw_ram_r__v0][3U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__shw_ram_r__v0[3U];
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__shw_ram_r[vlSelfRef.__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__shw_ram_r__v0][4U] 
            = vlSelfRef.__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__shw_ram_r__v0[4U];
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__rp_k_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__rp_k_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__fl_sink_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__fl_sink_r;
    vlSelfRef.s_axi_awready = ((IData)(vlSelfRef.s_axi_awvalid) 
                               & ((~ ((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__b_valid) 
                                      | ((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__sweep_busy) 
                                         | ((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__lctx_wr_p_r) 
                                            | (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__tctx_wr_p_r))))) 
                                  & (IData)(vlSelfRef.s_axi_wvalid)));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__rvld_q_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__rvld_q_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__rrec_ok_w 
        = ((2U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__rver_r)) 
           & (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__nvm_record_id_w) 
               == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__rrid_r)) 
              & ((0x0014U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__rplen_r)) 
                 & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__rcrc_acc_r) 
                    == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__rcrc_rx_r)))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__rs_k_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__rs_k_r;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__hs_r 
        = vlSelfRef.__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__hs_r;
    vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__fw_user 
        = (1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__good_r) 
                    | (IData)(vlSelfRef.milan_datapath__DOT__avtprx_accept_p))));
    vlSelfRef.milan_datapath__DOT__crf_rx__DOT__w_ev_uf_w 
        = ((~ (IData)(vlSelfRef.milan_datapath__DOT__crf_rx__DOT__w_fmt_ok)) 
           & (IData)(vlSelfRef.milan_datapath__DOT__crf_rx__DOT__w_hit));
    vlSelfRef.milan_datapath__DOT__crf_rx__DOT__w_acc 
        = ((IData)(vlSelfRef.milan_datapath__DOT__crf_rx__DOT__w_hit) 
           & (IData)(vlSelfRef.milan_datapath__DOT__crf_rx__DOT__w_fmt_ok));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__loss_ev_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__alarm_r) 
           | (((0U == vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__ms_div_r) 
               & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__hb_kick_w)) 
                  & (1U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__alive_r)))) 
              | (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__commit_busy_r) 
                  & ((0U == vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__ms_div_r) 
                     & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__ack_ok_w)) 
                        & ((~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__release_w) 
                               | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__commit_start_w))) 
                           & (1U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__commit_r)))))) 
                 | ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__reg_we_w) 
                    & ((3U == (0x0000001fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_nvm_csr_addr_w))) 
                       & ((0x0bU <= (0x0000000fU & vlSelfRef.milan_datapath__DOT__csr__DOT__g_pp_csr__DOT__pp_nvm_wdata_r)) 
                          & (0x0dU >= (0x0000000fU 
                                       & vlSelfRef.milan_datapath__DOT__csr__DOT__g_pp_csr__DOT__pp_nvm_wdata_r))))))));
    milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__drop_w 
        = ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__ack_ok_w)) 
           & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__close_w));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rla_grant_w 
        = (2U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rla_grant_w));
    if ((1U & (~ (IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_rx_hit_w)))) {
        if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__gate_acc_w) 
                      & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r)))))) {
            if ((1U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rla_pend_r) 
                       | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_la_msrp_w)))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rla_grant_w 
                    = (1U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rla_grant_w));
            }
        }
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rla_grant_w 
        = (1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rla_grant_w));
    if ((1U & (~ ((IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_rx_hit_w) 
                  >> 1U)))) {
        if ((1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__gate_acc_w) 
                      & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r))))) {
            if ((IData)((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rla_pend_r) 
                          >> 1U) | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_la_msrp_w)))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rla_grant_w 
                    = (2U | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rla_grant_w));
            }
        }
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_mrp_strip__DOT__space_w 
        = (1U & (~ (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_mrp_strip__DOT__out_vld_r) 
                     & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_mrp_strip__DOT__skid_vld_r)) 
                    | (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_mrp_strip__DOT__skid_vld_r) 
                        & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_mrp_strip__DOT__fetch_r)) 
                       | ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_mrp_strip__DOT__out_vld_r) 
                          & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_mrp_strip__DOT__fetch_r) 
                             & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_265)))))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_mrp_strip__DOT__avail_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_mrp_strip__DOT__rd_ptr_r) 
           != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_mrp_strip__DOT__wr_cmt_r));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__take_wr_w 
        = (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__in_range_w) 
            & (0x00010000U == (0x000f0000U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__st_addr_w))) 
           & (IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__dyn_ready_w));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__stall_e_w = 0U;
    if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__vld_e_r) {
        if ((1U & (~ (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__uop_e_r 
                              >> 0x0000002fU))))) {
            if ((1U & (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__uop_e_r 
                               >> 0x0000002eU)))) {
                if ((1U & (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__uop_e_r 
                                   >> 0x0000002dU)))) {
                    if ((1U & (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__uop_e_r 
                                       >> 0x0000002cU)))) {
                        if ((1U & (~ (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__uop_e_r 
                                              >> 0x0000002bU))))) {
                            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__br_taken_w 
                                = (1U & (~ ((1U & (IData)(
                                                          (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__uop_e_r 
                                                           >> 0x0000001aU)))
                                             ? (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__cmp_z_w)
                                             : ((1U 
                                                 & (IData)(
                                                           (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__uop_e_r 
                                                            >> 0x00000019U)))
                                                 ? 
                                                ((1U 
                                                  & (IData)(
                                                            (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__uop_e_r 
                                                             >> 0x00000018U)))
                                                  ? 
                                                 (~ (IData)(
                                                            (vlSelfRef.__VdfgRegularize_h6e95ff9d_0_115 
                                                             >> 0x00000020U)))
                                                  : (IData)(
                                                            (vlSelfRef.__VdfgRegularize_h6e95ff9d_0_115 
                                                             >> 0x00000020U)))
                                                 : 
                                                ((1U 
                                                  & (IData)(
                                                            (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__uop_e_r 
                                                             >> 0x00000018U)))
                                                  ? 
                                                 (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__cmp_z_w))
                                                  : (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__cmp_z_w))))));
                        }
                    } else if ((1U & (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__uop_e_r 
                                              >> 0x0000002bU)))) {
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__br_taken_w 
                            = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__lk_held_r) 
                               & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__lk_ctlr_r 
                                  != vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__opa_e_r));
                    }
                }
            } else if ((1U & (~ (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__uop_e_r 
                                         >> 0x0000002dU))))) {
                if ((1U & (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__uop_e_r 
                                   >> 0x0000002cU)))) {
                    if ((1U & (~ (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__uop_e_r 
                                          >> 0x0000002bU))))) {
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__br_taken_w 
                            = ((~ (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__uop_e_r 
                                           >> 0x0000001bU))) 
                               & ((1U & (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__uop_e_r 
                                                 >> 0x0000001aU)))
                                   ? (IData)(((0ULL 
                                               == (0x0000000003000000ULL 
                                                   & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__uop_e_r)) 
                                              & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__ovf_r)))
                                   : ((1U & (IData)(
                                                    (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__uop_e_r 
                                                     >> 0x00000019U)))
                                       ? ((1U & (IData)(
                                                        (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__uop_e_r 
                                                         >> 0x00000018U)))
                                           ? (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__lt_r)
                                           : (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__z_r))
                                       : ((1U & (IData)(
                                                        (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__uop_e_r 
                                                         >> 0x00000018U)))
                                           ? ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__iter_cnt_r) 
                                              == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__iter_idx_r))
                                           : (0U != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__status_r))))));
                    }
                } else if ((1U & (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__uop_e_r 
                                          >> 0x0000002bU)))) {
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__br_taken_w = 1U;
                }
            }
        }
        if ((IData)((((0x0000780000000000ULL == (0x0000f80000000000ULL 
                                                 & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__uop_e_r)) 
                      & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gxr_valid_r)) 
                     & (~ vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gxr_data_r)))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__br_taken_w = 1U;
        }
        if ((1U & (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__uop_e_r 
                           >> 0x0000002fU)))) {
            if ((1U & (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__uop_e_r 
                               >> 0x0000002eU)))) {
                if ((1U & (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__uop_e_r 
                                   >> 0x0000002dU)))) {
                    if ((1U & (~ (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__uop_e_r 
                                          >> 0x0000002cU))))) {
                        if ((1U & (~ (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__uop_e_r 
                                              >> 0x0000002bU))))) {
                            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__stall_e_w = 0U;
                        }
                    }
                } else if ((1U & (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__uop_e_r 
                                          >> 0x0000002cU)))) {
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__stall_e_w 
                        = ((1U & (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__uop_e_r 
                                          >> 0x0000002bU)))
                            ? ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__is_q_field_w) 
                               & (0U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__eseq_r)))
                            : (2U != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__eseq_r)));
                }
            } else if ((1U & (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__uop_e_r 
                                      >> 0x0000002dU)))) {
                if ((1U & (~ (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__uop_e_r 
                                      >> 0x0000002cU))))) {
                    if ((1U & (~ (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__uop_e_r 
                                          >> 0x0000002bU))))) {
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__stall_e_w 
                            = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__is_q_field_w) 
                               & (0U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__eseq_r)));
                    }
                }
            } else if ((1U & (~ (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__uop_e_r 
                                         >> 0x0000002cU))))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__stall_e_w 
                    = (1U & ((1U & (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__uop_e_r 
                                            >> 0x0000002bU)))
                              ? (4U != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__eseq_r))
                              : (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gxr_valid_r))));
            }
        } else if ((1U & (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__uop_e_r 
                                  >> 0x0000002eU)))) {
            if ((1U & (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__uop_e_r 
                               >> 0x0000002dU)))) {
                if ((1U & (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__uop_e_r 
                                   >> 0x0000002cU)))) {
                    if ((1U & (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__uop_e_r 
                                       >> 0x0000002bU)))) {
                        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__stall_e_w 
                            = (1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gxr_valid_r)));
                    }
                } else if ((1U & (~ (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__uop_e_r 
                                             >> 0x0000002bU))))) {
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__stall_e_w 
                        = (1U & (((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__copy_go_r)) 
                                  | (0U != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__copy_left_r))) 
                                 | (0U != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__eseq_r))));
                }
            } else {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__stall_e_w 
                    = (1U & ((1U & (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__uop_e_r 
                                            >> 0x0000002bU)))
                              ? (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__strq_sel_w)
                                     ? (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__strq_done_r)
                                     : ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__dyn_sel_w)
                                         ? (IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__dyn_ready_w)
                                         : (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__store_ready_w))))
                              : (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__st_rvalid_w))));
            }
        } else if ((1U & (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__uop_e_r 
                                  >> 0x0000002dU)))) {
            if ((1U & (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__uop_e_r 
                               >> 0x0000002cU)))) {
                if ((1U & (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__uop_e_r 
                                   >> 0x0000002bU)))) {
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__stall_e_w 
                        = (1U & (~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__st_rvalid_w)));
                }
            }
        }
        if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__rb_hold_w) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__stall_e_w = 1U;
        }
    }
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_86 = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_gate_open_w) 
                                                 | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_gate_close_w));
    __VdfgRegularize_h6e95ff9d_0_195 = (1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__ev_accept_w) 
                                                 | (IData)(__VdfgRegularize_h6e95ff9d_0_196))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__txc_req_w 
        = ((((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__ca_txs_alloc_req_w) 
               << 3U) | ((4U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__w_st_r)) 
                         << 2U)) | (((4U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__a_st_r)) 
                                     << 1U) | (1U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_st_r)))) 
            << 3U) | (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_txs_alloc_req_w) 
                       << 2U) | (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__lstn_txs_alloc_req_w) 
                                  << 1U) | (2U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__bld_st_r)))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pool_alloc_req_w = 0U;
    if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__txc_locked_r) {
        if ((4U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__txc_owner_r))) {
            if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__txc_owner_r))) {
                if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__txc_owner_r))) {
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pool_wr_valid_w 
                        = (2U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_st_r));
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pool_alloc_req_w 
                        = (1U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_st_r));
                } else {
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pool_wr_valid_w 
                        = ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_ca_builder__DOT__cancel_hit_w)) 
                           & (2U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_ca_builder__DOT__c_st_r)));
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pool_alloc_req_w 
                        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__ca_txs_alloc_req_w;
                }
            } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__txc_owner_r))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pool_wr_valid_w 
                    = (6U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__w_st_r));
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pool_alloc_req_w 
                    = (4U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__w_st_r));
            } else {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pool_wr_valid_w 
                    = ((5U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__a_st_r)) 
                       & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__byte_ok_w));
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pool_alloc_req_w 
                    = (4U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__a_st_r));
            }
        } else if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__txc_owner_r))) {
            if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__txc_owner_r))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pool_wr_valid_w 
                    = (2U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_st_r));
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pool_alloc_req_w 
                    = (1U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_st_r));
            } else {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pool_wr_valid_w 
                    = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__wr_valid_w;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pool_alloc_req_w 
                    = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_txs_alloc_req_w;
            }
        } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__txc_owner_r))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pool_wr_valid_w 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__lstn_txs_wr_valid_w;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pool_alloc_req_w 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__lstn_txs_alloc_req_w;
        } else {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pool_wr_valid_w 
                = (4U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__bld_st_r));
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pool_alloc_req_w 
                = (2U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__bld_st_r));
        }
        if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__txc_alloc_wait_r) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pool_alloc_req_w = 0U;
        }
    }
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_12 = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__prng_valid_w) 
                                                 & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pr_inflight_r));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__adp_prng_busy_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pr_inflight_r) 
           | ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__busy_r) 
              | (0U != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pr_pend_r))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__acmp_sb_candidate_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_acmp_q__DOT__out_valid_r) 
           & ((2U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pf_st_r)) 
              & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__acmp_sb_active_r)) 
                 & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_84))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__gnt_now_w 
        = ((0U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__st_r)) 
           & ((~ (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__cap_hold_r) 
                   | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__arm_ok_w)) 
                  & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__mut_req_w))) 
              & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__nvm_req_w)));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_192 = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__eff_len_w) 
                                                  + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__nvm_offset_w));
    vlSelfRef.s_axi_wready = vlSelfRef.s_axi_awready;
    vlSelfRef.milan_datapath__DOT__csr__DOT__win_alias_ctrl_w 
        = (((0x0810U == (IData)(vlSelfRef.s_axi_awaddr)) 
            & (IData)(vlSelfRef.s_axi_awready)) & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_54));
    vlSelfRef.milan_datapath__DOT__csr__DOT__win_alias_dmlo_w 
        = ((IData)(vlSelfRef.s_axi_awready) & ((0x081cU 
                                                == (IData)(vlSelfRef.s_axi_awaddr)) 
                                               & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_54)));
    vlSelfRef.milan_datapath__DOT__csr__DOT__win_alias_dmhi_w 
        = ((IData)(vlSelfRef.s_axi_awready) & ((0x0820U 
                                                == (IData)(vlSelfRef.s_axi_awaddr)) 
                                               & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_54)));
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
        vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a 
            = vlSelfRef.s_axi_awaddr;
        milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw = 0U;
        if ((0x00008000U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
            if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)) 
                 & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) {
                milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                    = ((((0U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) 
                         | (4U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                        | (8U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                       | (0x0cU == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))));
            }
        } else if ((0x00004000U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
            if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)) 
                 & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) {
                milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                    = ((((0U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) 
                         | (4U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                        | (8U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                       | (0x0cU == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))));
            }
        } else if ((0x00002000U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
            if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)) 
                 & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) {
                milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                    = ((((0U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) 
                         | (4U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                        | (8U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                       | (0x0cU == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))));
            }
        } else if ((0x00001000U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
            if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)) 
                 & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) {
                milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                    = ((((0U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) 
                         | (4U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                        | (8U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                       | (0x0cU == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))));
            }
        } else if ((0x00000800U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
            if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)) 
                 & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) {
                milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                    = ((((0U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) 
                         | (4U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                        | (8U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                       | (0x0cU == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))));
            }
        } else if ((0x00000400U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
            if ((0x00000200U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
                if ((0x00000100U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
                    if ((0x00000080U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
                        if ((0x00000040U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
                            if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)) 
                                 & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) {
                                milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                    = ((((0U == (0x0000001fU 
                                                 & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) 
                                         | (4U == (0x0000001fU 
                                                   & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                        | (8U == (0x0000001fU 
                                                  & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                       | (0x0cU == 
                                          (0x0000001fU 
                                           & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))));
                            }
                        } else if ((0x00000020U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
                            if ((0x00000010U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
                                if ((8U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
                                    if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)) 
                                         & (0x04a0U 
                                            > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) {
                                        milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                            = ((((0U 
                                                  == 
                                                  (0x0000001fU 
                                                   & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) 
                                                 | (4U 
                                                    == 
                                                    (0x0000001fU 
                                                     & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                                | (8U 
                                                   == 
                                                   (0x0000001fU 
                                                    & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                               | (0x0cU 
                                                  == 
                                                  (0x0000001fU 
                                                   & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))));
                                    }
                                } else if ((4U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
                                    if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)) 
                                         & (0x04a0U 
                                            > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) {
                                        milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                            = ((((0U 
                                                  == 
                                                  (0x0000001fU 
                                                   & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) 
                                                 | (4U 
                                                    == 
                                                    (0x0000001fU 
                                                     & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                                | (8U 
                                                   == 
                                                   (0x0000001fU 
                                                    & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                               | (0x0cU 
                                                  == 
                                                  (0x0000001fU 
                                                   & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))));
                                    }
                                } else if ((2U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
                                    if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)) 
                                         & (0x04a0U 
                                            > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) {
                                        milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                            = ((((0U 
                                                  == 
                                                  (0x0000001fU 
                                                   & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) 
                                                 | (4U 
                                                    == 
                                                    (0x0000001fU 
                                                     & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                                | (8U 
                                                   == 
                                                   (0x0000001fU 
                                                    & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                               | (0x0cU 
                                                  == 
                                                  (0x0000001fU 
                                                   & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))));
                                    }
                                } else if ((1U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
                                    if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)) 
                                         & (0x04a0U 
                                            > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) {
                                        milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                            = ((((0U 
                                                  == 
                                                  (0x0000001fU 
                                                   & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) 
                                                 | (4U 
                                                    == 
                                                    (0x0000001fU 
                                                     & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                                | (8U 
                                                   == 
                                                   (0x0000001fU 
                                                    & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                               | (0x0cU 
                                                  == 
                                                  (0x0000001fU 
                                                   & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))));
                                    }
                                } else {
                                    milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw = 1U;
                                }
                            } else if ((2U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
                                if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)) 
                                     & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) {
                                    milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                        = ((((0U == 
                                              (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) 
                                             | (4U 
                                                == 
                                                (0x0000001fU 
                                                 & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                            | (8U == 
                                               (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                           | (0x0cU 
                                              == (0x0000001fU 
                                                  & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))));
                                }
                            } else if ((1U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
                                if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)) 
                                     & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) {
                                    milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                        = ((((0U == 
                                              (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) 
                                             | (4U 
                                                == 
                                                (0x0000001fU 
                                                 & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                            | (8U == 
                                               (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                           | (0x0cU 
                                              == (0x0000001fU 
                                                  & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))));
                                }
                            } else {
                                milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw = 1U;
                            }
                        } else if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)) 
                                    & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) {
                            milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                = ((((0U == (0x0000001fU 
                                             & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) 
                                     | (4U == (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                    | (8U == (0x0000001fU 
                                              & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                   | (0x0cU == (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))));
                        }
                    } else if ((0x00000040U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
                        if ((0x00000020U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
                            if ((0x00000010U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
                                if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)) 
                                     & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) {
                                    milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                        = ((((0U == 
                                              (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) 
                                             | (4U 
                                                == 
                                                (0x0000001fU 
                                                 & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                            | (8U == 
                                               (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                           | (0x0cU 
                                              == (0x0000001fU 
                                                  & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))));
                                }
                            } else if ((8U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
                                if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)) 
                                     & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) {
                                    milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                        = ((((0U == 
                                              (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) 
                                             | (4U 
                                                == 
                                                (0x0000001fU 
                                                 & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                            | (8U == 
                                               (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                           | (0x0cU 
                                              == (0x0000001fU 
                                                  & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))));
                                }
                            } else if ((4U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
                                if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)) 
                                     & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) {
                                    milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                        = ((((0U == 
                                              (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) 
                                             | (4U 
                                                == 
                                                (0x0000001fU 
                                                 & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                            | (8U == 
                                               (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                           | (0x0cU 
                                              == (0x0000001fU 
                                                  & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))));
                                }
                            } else if ((2U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
                                if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)) 
                                     & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) {
                                    milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                        = ((((0U == 
                                              (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) 
                                             | (4U 
                                                == 
                                                (0x0000001fU 
                                                 & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                            | (8U == 
                                               (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                           | (0x0cU 
                                              == (0x0000001fU 
                                                  & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))));
                                }
                            } else if ((1U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
                                if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)) 
                                     & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) {
                                    milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                        = ((((0U == 
                                              (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) 
                                             | (4U 
                                                == 
                                                (0x0000001fU 
                                                 & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                            | (8U == 
                                               (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                           | (0x0cU 
                                              == (0x0000001fU 
                                                  & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))));
                                }
                            } else {
                                milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw = 1U;
                            }
                        } else if ((0x00000010U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
                            if ((8U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
                                if ((2U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
                                    if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)) 
                                         & (0x04a0U 
                                            > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) {
                                        milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                            = ((((0U 
                                                  == 
                                                  (0x0000001fU 
                                                   & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) 
                                                 | (4U 
                                                    == 
                                                    (0x0000001fU 
                                                     & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                                | (8U 
                                                   == 
                                                   (0x0000001fU 
                                                    & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                               | (0x0cU 
                                                  == 
                                                  (0x0000001fU 
                                                   & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))));
                                    }
                                } else if ((1U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
                                    if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)) 
                                         & (0x04a0U 
                                            > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) {
                                        milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                            = ((((0U 
                                                  == 
                                                  (0x0000001fU 
                                                   & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) 
                                                 | (4U 
                                                    == 
                                                    (0x0000001fU 
                                                     & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                                | (8U 
                                                   == 
                                                   (0x0000001fU 
                                                    & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                               | (0x0cU 
                                                  == 
                                                  (0x0000001fU 
                                                   & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))));
                                    }
                                } else {
                                    milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw = 1U;
                                }
                            } else if ((4U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
                                if ((2U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
                                    if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)) 
                                         & (0x04a0U 
                                            > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) {
                                        milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                            = ((((0U 
                                                  == 
                                                  (0x0000001fU 
                                                   & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) 
                                                 | (4U 
                                                    == 
                                                    (0x0000001fU 
                                                     & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                                | (8U 
                                                   == 
                                                   (0x0000001fU 
                                                    & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                               | (0x0cU 
                                                  == 
                                                  (0x0000001fU 
                                                   & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))));
                                    }
                                } else if ((1U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
                                    if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)) 
                                         & (0x04a0U 
                                            > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) {
                                        milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                            = ((((0U 
                                                  == 
                                                  (0x0000001fU 
                                                   & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) 
                                                 | (4U 
                                                    == 
                                                    (0x0000001fU 
                                                     & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                                | (8U 
                                                   == 
                                                   (0x0000001fU 
                                                    & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                               | (0x0cU 
                                                  == 
                                                  (0x0000001fU 
                                                   & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))));
                                    }
                                } else {
                                    milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw = 1U;
                                }
                            } else if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)) 
                                        & (0x04a0U 
                                           > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) {
                                milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                    = ((((0U == (0x0000001fU 
                                                 & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) 
                                         | (4U == (0x0000001fU 
                                                   & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                        | (8U == (0x0000001fU 
                                                  & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                       | (0x0cU == 
                                          (0x0000001fU 
                                           & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))));
                            }
                        } else if ((8U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
                            if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)) 
                                 & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) {
                                milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                    = ((((0U == (0x0000001fU 
                                                 & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) 
                                         | (4U == (0x0000001fU 
                                                   & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                        | (8U == (0x0000001fU 
                                                  & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                       | (0x0cU == 
                                          (0x0000001fU 
                                           & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))));
                            }
                        } else if ((4U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
                            if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)) 
                                 & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) {
                                milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                    = ((((0U == (0x0000001fU 
                                                 & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) 
                                         | (4U == (0x0000001fU 
                                                   & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                        | (8U == (0x0000001fU 
                                                  & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                       | (0x0cU == 
                                          (0x0000001fU 
                                           & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))));
                            }
                        } else if ((2U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
                            if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)) 
                                 & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) {
                                milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                    = ((((0U == (0x0000001fU 
                                                 & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) 
                                         | (4U == (0x0000001fU 
                                                   & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                        | (8U == (0x0000001fU 
                                                  & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                       | (0x0cU == 
                                          (0x0000001fU 
                                           & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))));
                            }
                        } else if ((1U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
                            if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)) 
                                 & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) {
                                milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                    = ((((0U == (0x0000001fU 
                                                 & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) 
                                         | (4U == (0x0000001fU 
                                                   & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                        | (8U == (0x0000001fU 
                                                  & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                       | (0x0cU == 
                                          (0x0000001fU 
                                           & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))));
                            }
                        } else {
                            milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw = 1U;
                        }
                    } else if ((0x00000020U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
                        if ((0x00000010U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
                            if ((8U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
                                if ((4U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
                                    if ((2U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
                                        if (((0x0400U 
                                              <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)) 
                                             & (0x04a0U 
                                                > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) {
                                            milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                                = (
                                                   (((0U 
                                                      == 
                                                      (0x0000001fU 
                                                       & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) 
                                                     | (4U 
                                                        == 
                                                        (0x0000001fU 
                                                         & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                                    | (8U 
                                                       == 
                                                       (0x0000001fU 
                                                        & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                                   | (0x0cU 
                                                      == 
                                                      (0x0000001fU 
                                                       & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))));
                                        }
                                    } else if ((1U 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
                                        if (((0x0400U 
                                              <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)) 
                                             & (0x04a0U 
                                                > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) {
                                            milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                                = (
                                                   (((0U 
                                                      == 
                                                      (0x0000001fU 
                                                       & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) 
                                                     | (4U 
                                                        == 
                                                        (0x0000001fU 
                                                         & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                                    | (8U 
                                                       == 
                                                       (0x0000001fU 
                                                        & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                                   | (0x0cU 
                                                      == 
                                                      (0x0000001fU 
                                                       & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))));
                                        }
                                    } else {
                                        milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw = 1U;
                                    }
                                } else if (((0x0400U 
                                             <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)) 
                                            & (0x04a0U 
                                               > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) {
                                    milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                        = ((((0U == 
                                              (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) 
                                             | (4U 
                                                == 
                                                (0x0000001fU 
                                                 & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                            | (8U == 
                                               (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                           | (0x0cU 
                                              == (0x0000001fU 
                                                  & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))));
                                }
                            } else if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)) 
                                        & (0x04a0U 
                                           > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) {
                                milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                    = ((((0U == (0x0000001fU 
                                                 & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) 
                                         | (4U == (0x0000001fU 
                                                   & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                        | (8U == (0x0000001fU 
                                                  & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                       | (0x0cU == 
                                          (0x0000001fU 
                                           & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))));
                            }
                        } else if ((8U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
                            if ((2U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
                                if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)) 
                                     & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) {
                                    milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                        = ((((0U == 
                                              (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) 
                                             | (4U 
                                                == 
                                                (0x0000001fU 
                                                 & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                            | (8U == 
                                               (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                           | (0x0cU 
                                              == (0x0000001fU 
                                                  & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))));
                                }
                            } else if ((1U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
                                if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)) 
                                     & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) {
                                    milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                        = ((((0U == 
                                              (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) 
                                             | (4U 
                                                == 
                                                (0x0000001fU 
                                                 & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                            | (8U == 
                                               (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                           | (0x0cU 
                                              == (0x0000001fU 
                                                  & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))));
                                }
                            } else {
                                milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw = 1U;
                            }
                        } else if ((4U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
                            if ((2U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
                                if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)) 
                                     & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) {
                                    milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                        = ((((0U == 
                                              (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) 
                                             | (4U 
                                                == 
                                                (0x0000001fU 
                                                 & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                            | (8U == 
                                               (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                           | (0x0cU 
                                              == (0x0000001fU 
                                                  & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))));
                                }
                            } else if ((1U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
                                if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)) 
                                     & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) {
                                    milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                        = ((((0U == 
                                              (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) 
                                             | (4U 
                                                == 
                                                (0x0000001fU 
                                                 & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                            | (8U == 
                                               (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                           | (0x0cU 
                                              == (0x0000001fU 
                                                  & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))));
                                }
                            } else {
                                milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw = 1U;
                            }
                        } else if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)) 
                                    & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) {
                            milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                = ((((0U == (0x0000001fU 
                                             & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) 
                                     | (4U == (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                    | (8U == (0x0000001fU 
                                              & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                   | (0x0cU == (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))));
                        }
                    } else if ((0x00000010U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
                        if ((8U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
                            if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)) 
                                 & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) {
                                milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                    = ((((0U == (0x0000001fU 
                                                 & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) 
                                         | (4U == (0x0000001fU 
                                                   & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                        | (8U == (0x0000001fU 
                                                  & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                       | (0x0cU == 
                                          (0x0000001fU 
                                           & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))));
                            }
                        } else if ((2U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
                            if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)) 
                                 & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) {
                                milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                    = ((((0U == (0x0000001fU 
                                                 & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) 
                                         | (4U == (0x0000001fU 
                                                   & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                        | (8U == (0x0000001fU 
                                                  & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                       | (0x0cU == 
                                          (0x0000001fU 
                                           & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))));
                            }
                        } else if ((1U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
                            if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)) 
                                 & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) {
                                milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                    = ((((0U == (0x0000001fU 
                                                 & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) 
                                         | (4U == (0x0000001fU 
                                                   & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                        | (8U == (0x0000001fU 
                                                  & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                       | (0x0cU == 
                                          (0x0000001fU 
                                           & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))));
                            }
                        } else {
                            milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw = 1U;
                        }
                    } else if ((2U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
                        if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)) 
                             & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) {
                            milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                = ((((0U == (0x0000001fU 
                                             & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) 
                                     | (4U == (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                    | (8U == (0x0000001fU 
                                              & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                   | (0x0cU == (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))));
                        }
                    } else if ((1U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
                        if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)) 
                             & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) {
                            milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                = ((((0U == (0x0000001fU 
                                             & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) 
                                     | (4U == (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                    | (8U == (0x0000001fU 
                                              & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                   | (0x0cU == (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))));
                        }
                    } else {
                        milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw = 1U;
                    }
                } else if ((0x00000080U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
                    if ((0x00000040U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
                        if ((0x00000020U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
                            if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)) 
                                 & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) {
                                milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                    = ((((0U == (0x0000001fU 
                                                 & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) 
                                         | (4U == (0x0000001fU 
                                                   & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                        | (8U == (0x0000001fU 
                                                  & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                       | (0x0cU == 
                                          (0x0000001fU 
                                           & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))));
                            }
                        } else if ((8U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
                            if ((4U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
                                if ((2U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
                                    if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)) 
                                         & (0x04a0U 
                                            > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) {
                                        milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                            = ((((0U 
                                                  == 
                                                  (0x0000001fU 
                                                   & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) 
                                                 | (4U 
                                                    == 
                                                    (0x0000001fU 
                                                     & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                                | (8U 
                                                   == 
                                                   (0x0000001fU 
                                                    & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                               | (0x0cU 
                                                  == 
                                                  (0x0000001fU 
                                                   & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))));
                                    }
                                } else if ((1U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
                                    if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)) 
                                         & (0x04a0U 
                                            > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) {
                                        milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                            = ((((0U 
                                                  == 
                                                  (0x0000001fU 
                                                   & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) 
                                                 | (4U 
                                                    == 
                                                    (0x0000001fU 
                                                     & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                                | (8U 
                                                   == 
                                                   (0x0000001fU 
                                                    & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                               | (0x0cU 
                                                  == 
                                                  (0x0000001fU 
                                                   & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))));
                                    }
                                } else {
                                    milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw = 1U;
                                }
                            } else if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)) 
                                        & (0x04a0U 
                                           > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) {
                                milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                    = ((((0U == (0x0000001fU 
                                                 & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) 
                                         | (4U == (0x0000001fU 
                                                   & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                        | (8U == (0x0000001fU 
                                                  & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                       | (0x0cU == 
                                          (0x0000001fU 
                                           & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))));
                            }
                        } else if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)) 
                                    & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) {
                            milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                = ((((0U == (0x0000001fU 
                                             & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) 
                                     | (4U == (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                    | (8U == (0x0000001fU 
                                              & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                   | (0x0cU == (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))));
                        }
                    } else if ((0x00000020U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
                        if ((0x00000010U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
                            if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)) 
                                 & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) {
                                milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                    = ((((0U == (0x0000001fU 
                                                 & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) 
                                         | (4U == (0x0000001fU 
                                                   & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                        | (8U == (0x0000001fU 
                                                  & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                       | (0x0cU == 
                                          (0x0000001fU 
                                           & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))));
                            }
                        } else if ((8U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
                            if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)) 
                                 & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) {
                                milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                    = ((((0U == (0x0000001fU 
                                                 & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) 
                                         | (4U == (0x0000001fU 
                                                   & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                        | (8U == (0x0000001fU 
                                                  & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                       | (0x0cU == 
                                          (0x0000001fU 
                                           & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))));
                            }
                        } else if ((4U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
                            if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)) 
                                 & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) {
                                milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                    = ((((0U == (0x0000001fU 
                                                 & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) 
                                         | (4U == (0x0000001fU 
                                                   & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                        | (8U == (0x0000001fU 
                                                  & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                       | (0x0cU == 
                                          (0x0000001fU 
                                           & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))));
                            }
                        } else if ((2U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
                            if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)) 
                                 & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) {
                                milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                    = ((((0U == (0x0000001fU 
                                                 & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) 
                                         | (4U == (0x0000001fU 
                                                   & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                        | (8U == (0x0000001fU 
                                                  & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                       | (0x0cU == 
                                          (0x0000001fU 
                                           & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))));
                            }
                        } else if ((1U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
                            if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)) 
                                 & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) {
                                milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                    = ((((0U == (0x0000001fU 
                                                 & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) 
                                         | (4U == (0x0000001fU 
                                                   & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                        | (8U == (0x0000001fU 
                                                  & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                       | (0x0cU == 
                                          (0x0000001fU 
                                           & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))));
                            }
                        } else {
                            milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw = 1U;
                        }
                    } else if ((0x00000010U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
                        if ((8U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
                            if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)) 
                                 & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) {
                                milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                    = ((((0U == (0x0000001fU 
                                                 & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) 
                                         | (4U == (0x0000001fU 
                                                   & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                        | (8U == (0x0000001fU 
                                                  & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                       | (0x0cU == 
                                          (0x0000001fU 
                                           & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))));
                            }
                        } else if ((4U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
                            if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)) 
                                 & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) {
                                milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                    = ((((0U == (0x0000001fU 
                                                 & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) 
                                         | (4U == (0x0000001fU 
                                                   & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                        | (8U == (0x0000001fU 
                                                  & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                       | (0x0cU == 
                                          (0x0000001fU 
                                           & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))));
                            }
                        } else if ((2U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
                            if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)) 
                                 & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) {
                                milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                    = ((((0U == (0x0000001fU 
                                                 & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) 
                                         | (4U == (0x0000001fU 
                                                   & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                        | (8U == (0x0000001fU 
                                                  & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                       | (0x0cU == 
                                          (0x0000001fU 
                                           & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))));
                            }
                        } else if ((1U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
                            if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)) 
                                 & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) {
                                milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                    = ((((0U == (0x0000001fU 
                                                 & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) 
                                         | (4U == (0x0000001fU 
                                                   & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                        | (8U == (0x0000001fU 
                                                  & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                       | (0x0cU == 
                                          (0x0000001fU 
                                           & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))));
                            }
                        } else {
                            milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw = 1U;
                        }
                    } else if ((2U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
                        if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)) 
                             & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) {
                            milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                = ((((0U == (0x0000001fU 
                                             & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) 
                                     | (4U == (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                    | (8U == (0x0000001fU 
                                              & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                   | (0x0cU == (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))));
                        }
                    } else if ((1U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
                        if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)) 
                             & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) {
                            milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                = ((((0U == (0x0000001fU 
                                             & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) 
                                     | (4U == (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                    | (8U == (0x0000001fU 
                                              & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                   | (0x0cU == (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))));
                        }
                    } else {
                        milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw = 1U;
                    }
                } else if ((0x00000040U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
                    if ((0x00000020U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
                        if ((0x00000010U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
                            if ((8U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
                                if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)) 
                                     & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) {
                                    milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                        = ((((0U == 
                                              (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) 
                                             | (4U 
                                                == 
                                                (0x0000001fU 
                                                 & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                            | (8U == 
                                               (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                           | (0x0cU 
                                              == (0x0000001fU 
                                                  & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))));
                                }
                            } else if ((4U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
                                if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)) 
                                     & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) {
                                    milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                        = ((((0U == 
                                              (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) 
                                             | (4U 
                                                == 
                                                (0x0000001fU 
                                                 & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                            | (8U == 
                                               (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                           | (0x0cU 
                                              == (0x0000001fU 
                                                  & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))));
                                }
                            } else if ((2U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
                                if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)) 
                                     & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) {
                                    milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                        = ((((0U == 
                                              (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) 
                                             | (4U 
                                                == 
                                                (0x0000001fU 
                                                 & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                            | (8U == 
                                               (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                           | (0x0cU 
                                              == (0x0000001fU 
                                                  & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))));
                                }
                            } else if ((1U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
                                if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)) 
                                     & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) {
                                    milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                        = ((((0U == 
                                              (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) 
                                             | (4U 
                                                == 
                                                (0x0000001fU 
                                                 & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                            | (8U == 
                                               (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                           | (0x0cU 
                                              == (0x0000001fU 
                                                  & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))));
                                }
                            } else {
                                milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw = 1U;
                            }
                        } else if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)) 
                                    & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) {
                            milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                = ((((0U == (0x0000001fU 
                                             & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) 
                                     | (4U == (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                    | (8U == (0x0000001fU 
                                              & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                   | (0x0cU == (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))));
                        }
                    } else if ((0x00000010U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
                        if ((8U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
                            if ((2U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
                                if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)) 
                                     & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) {
                                    milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                        = ((((0U == 
                                              (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) 
                                             | (4U 
                                                == 
                                                (0x0000001fU 
                                                 & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                            | (8U == 
                                               (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                           | (0x0cU 
                                              == (0x0000001fU 
                                                  & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))));
                                }
                            } else if ((1U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
                                if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)) 
                                     & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) {
                                    milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                        = ((((0U == 
                                              (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) 
                                             | (4U 
                                                == 
                                                (0x0000001fU 
                                                 & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                            | (8U == 
                                               (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                           | (0x0cU 
                                              == (0x0000001fU 
                                                  & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))));
                                }
                            } else {
                                milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw = 1U;
                            }
                        } else if ((4U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
                            if ((2U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
                                if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)) 
                                     & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) {
                                    milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                        = ((((0U == 
                                              (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) 
                                             | (4U 
                                                == 
                                                (0x0000001fU 
                                                 & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                            | (8U == 
                                               (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                           | (0x0cU 
                                              == (0x0000001fU 
                                                  & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))));
                                }
                            } else if ((1U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
                                if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)) 
                                     & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) {
                                    milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                        = ((((0U == 
                                              (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) 
                                             | (4U 
                                                == 
                                                (0x0000001fU 
                                                 & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                            | (8U == 
                                               (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                           | (0x0cU 
                                              == (0x0000001fU 
                                                  & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))));
                                }
                            } else {
                                milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw = 1U;
                            }
                        } else if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)) 
                                    & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) {
                            milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                = ((((0U == (0x0000001fU 
                                             & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) 
                                     | (4U == (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                    | (8U == (0x0000001fU 
                                              & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                   | (0x0cU == (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))));
                        }
                    } else if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)) 
                                & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) {
                        milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                            = ((((0U == (0x0000001fU 
                                         & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) 
                                 | (4U == (0x0000001fU 
                                           & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                | (8U == (0x0000001fU 
                                          & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                               | (0x0cU == (0x0000001fU 
                                            & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))));
                    }
                } else if ((0x00000020U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
                    if ((0x00000010U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
                        if ((2U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
                            if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)) 
                                 & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) {
                                milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                    = ((((0U == (0x0000001fU 
                                                 & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) 
                                         | (4U == (0x0000001fU 
                                                   & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                        | (8U == (0x0000001fU 
                                                  & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                       | (0x0cU == 
                                          (0x0000001fU 
                                           & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))));
                            }
                        } else if ((1U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
                            if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)) 
                                 & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) {
                                milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                    = ((((0U == (0x0000001fU 
                                                 & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) 
                                         | (4U == (0x0000001fU 
                                                   & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                        | (8U == (0x0000001fU 
                                                  & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                       | (0x0cU == 
                                          (0x0000001fU 
                                           & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))));
                            }
                        } else {
                            milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw = 1U;
                        }
                    } else if ((8U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
                        if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)) 
                             & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) {
                            milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                = ((((0U == (0x0000001fU 
                                             & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) 
                                     | (4U == (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                    | (8U == (0x0000001fU 
                                              & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                   | (0x0cU == (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))));
                        }
                    } else if ((4U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
                        if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)) 
                             & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) {
                            milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                = ((((0U == (0x0000001fU 
                                             & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) 
                                     | (4U == (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                    | (8U == (0x0000001fU 
                                              & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                   | (0x0cU == (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))));
                        }
                    } else if ((2U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
                        if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)) 
                             & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) {
                            milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                = ((((0U == (0x0000001fU 
                                             & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) 
                                     | (4U == (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                    | (8U == (0x0000001fU 
                                              & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                   | (0x0cU == (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))));
                        }
                    } else if ((1U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
                        if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)) 
                             & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) {
                            milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                = ((((0U == (0x0000001fU 
                                             & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) 
                                     | (4U == (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                    | (8U == (0x0000001fU 
                                              & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                   | (0x0cU == (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))));
                        }
                    } else {
                        milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw = 1U;
                    }
                } else if ((0x00000010U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
                    if ((8U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
                        if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)) 
                             & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) {
                            milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                = ((((0U == (0x0000001fU 
                                             & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) 
                                     | (4U == (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                    | (8U == (0x0000001fU 
                                              & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                   | (0x0cU == (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))));
                        }
                    } else if ((2U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
                        if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)) 
                             & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) {
                            milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                = ((((0U == (0x0000001fU 
                                             & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) 
                                     | (4U == (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                    | (8U == (0x0000001fU 
                                              & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                   | (0x0cU == (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))));
                        }
                    } else if ((1U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
                        if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)) 
                             & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) {
                            milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                = ((((0U == (0x0000001fU 
                                             & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) 
                                     | (4U == (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                    | (8U == (0x0000001fU 
                                              & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                   | (0x0cU == (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))));
                        }
                    } else {
                        milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw = 1U;
                    }
                } else if ((2U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
                    if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)) 
                         & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) {
                        milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                            = ((((0U == (0x0000001fU 
                                         & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) 
                                 | (4U == (0x0000001fU 
                                           & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                | (8U == (0x0000001fU 
                                          & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                               | (0x0cU == (0x0000001fU 
                                            & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))));
                    }
                } else if ((1U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
                    if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)) 
                         & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) {
                        milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                            = ((((0U == (0x0000001fU 
                                         & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) 
                                 | (4U == (0x0000001fU 
                                           & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                | (8U == (0x0000001fU 
                                          & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                               | (0x0cU == (0x0000001fU 
                                            & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))));
                    }
                } else {
                    milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw = 1U;
                }
            } else if ((0x00000100U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
                if ((0x00000080U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
                    if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)) 
                         & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) {
                        milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                            = ((((0U == (0x0000001fU 
                                         & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) 
                                 | (4U == (0x0000001fU 
                                           & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                | (8U == (0x0000001fU 
                                          & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                               | (0x0cU == (0x0000001fU 
                                            & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))));
                    }
                } else if ((0x00000040U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
                    if ((0x00000020U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
                        if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)) 
                             & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) {
                            milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                = ((((0U == (0x0000001fU 
                                             & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) 
                                     | (4U == (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                    | (8U == (0x0000001fU 
                                              & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                   | (0x0cU == (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))));
                        }
                    } else if ((0x00000010U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
                        if ((8U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
                            if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)) 
                                 & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) {
                                milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                    = ((((0U == (0x0000001fU 
                                                 & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) 
                                         | (4U == (0x0000001fU 
                                                   & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                        | (8U == (0x0000001fU 
                                                  & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                       | (0x0cU == 
                                          (0x0000001fU 
                                           & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))));
                            }
                        } else if ((4U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
                            if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)) 
                                 & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) {
                                milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                    = ((((0U == (0x0000001fU 
                                                 & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) 
                                         | (4U == (0x0000001fU 
                                                   & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                        | (8U == (0x0000001fU 
                                                  & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                       | (0x0cU == 
                                          (0x0000001fU 
                                           & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))));
                            }
                        } else if ((2U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
                            if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)) 
                                 & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) {
                                milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                    = ((((0U == (0x0000001fU 
                                                 & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) 
                                         | (4U == (0x0000001fU 
                                                   & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                        | (8U == (0x0000001fU 
                                                  & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                       | (0x0cU == 
                                          (0x0000001fU 
                                           & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))));
                            }
                        } else if ((1U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
                            if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)) 
                                 & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) {
                                milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                    = ((((0U == (0x0000001fU 
                                                 & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) 
                                         | (4U == (0x0000001fU 
                                                   & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                        | (8U == (0x0000001fU 
                                                  & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                       | (0x0cU == 
                                          (0x0000001fU 
                                           & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))));
                            }
                        } else {
                            milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw = 1U;
                        }
                    } else if ((8U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
                        if ((4U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
                            if ((2U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
                                if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)) 
                                     & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) {
                                    milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                        = ((((0U == 
                                              (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) 
                                             | (4U 
                                                == 
                                                (0x0000001fU 
                                                 & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                            | (8U == 
                                               (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                           | (0x0cU 
                                              == (0x0000001fU 
                                                  & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))));
                                }
                            } else if ((1U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
                                if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)) 
                                     & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) {
                                    milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                        = ((((0U == 
                                              (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) 
                                             | (4U 
                                                == 
                                                (0x0000001fU 
                                                 & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                            | (8U == 
                                               (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                           | (0x0cU 
                                              == (0x0000001fU 
                                                  & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))));
                                }
                            } else {
                                milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw = 1U;
                            }
                        } else if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)) 
                                    & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) {
                            milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                = ((((0U == (0x0000001fU 
                                             & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) 
                                     | (4U == (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                    | (8U == (0x0000001fU 
                                              & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                   | (0x0cU == (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))));
                        }
                    } else if ((2U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
                        if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)) 
                             & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) {
                            milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                = ((((0U == (0x0000001fU 
                                             & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) 
                                     | (4U == (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                    | (8U == (0x0000001fU 
                                              & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                   | (0x0cU == (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))));
                        }
                    } else if ((1U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
                        if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)) 
                             & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) {
                            milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                = ((((0U == (0x0000001fU 
                                             & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) 
                                     | (4U == (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                    | (8U == (0x0000001fU 
                                              & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                   | (0x0cU == (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))));
                        }
                    } else {
                        milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw = 1U;
                    }
                } else if ((0x00000020U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
                    if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)) 
                         & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) {
                        milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                            = ((((0U == (0x0000001fU 
                                         & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) 
                                 | (4U == (0x0000001fU 
                                           & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                | (8U == (0x0000001fU 
                                          & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                               | (0x0cU == (0x0000001fU 
                                            & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))));
                    }
                } else if ((0x00000010U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
                    if ((2U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
                        if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)) 
                             & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) {
                            milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                = ((((0U == (0x0000001fU 
                                             & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) 
                                     | (4U == (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                    | (8U == (0x0000001fU 
                                              & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                   | (0x0cU == (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))));
                        }
                    } else if ((1U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
                        if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)) 
                             & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) {
                            milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                = ((((0U == (0x0000001fU 
                                             & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) 
                                     | (4U == (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                    | (8U == (0x0000001fU 
                                              & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                   | (0x0cU == (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))));
                        }
                    } else {
                        milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw = 1U;
                    }
                } else if ((8U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
                    if ((4U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
                        if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)) 
                             & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) {
                            milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                = ((((0U == (0x0000001fU 
                                             & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) 
                                     | (4U == (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                    | (8U == (0x0000001fU 
                                              & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                   | (0x0cU == (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))));
                        }
                    } else if ((2U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
                        if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)) 
                             & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) {
                            milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                = ((((0U == (0x0000001fU 
                                             & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) 
                                     | (4U == (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                    | (8U == (0x0000001fU 
                                              & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                   | (0x0cU == (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))));
                        }
                    } else if ((1U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
                        if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)) 
                             & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) {
                            milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                = ((((0U == (0x0000001fU 
                                             & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) 
                                     | (4U == (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                    | (8U == (0x0000001fU 
                                              & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                   | (0x0cU == (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))));
                        }
                    } else {
                        milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw = 1U;
                    }
                } else if ((2U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
                    if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)) 
                         & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) {
                        milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                            = ((((0U == (0x0000001fU 
                                         & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) 
                                 | (4U == (0x0000001fU 
                                           & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                | (8U == (0x0000001fU 
                                          & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                               | (0x0cU == (0x0000001fU 
                                            & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))));
                    }
                } else if ((1U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
                    if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)) 
                         & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) {
                        milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                            = ((((0U == (0x0000001fU 
                                         & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) 
                                 | (4U == (0x0000001fU 
                                           & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                | (8U == (0x0000001fU 
                                          & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                               | (0x0cU == (0x0000001fU 
                                            & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))));
                    }
                } else {
                    milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw = 1U;
                }
            } else if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)) 
                        & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) {
                milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                    = ((((0U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) 
                         | (4U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                        | (8U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                       | (0x0cU == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))));
            }
        } else if ((0x00000200U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
            if ((0x00000100U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
                if ((0x00000080U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
                    if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)) 
                         & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) {
                        milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                            = ((((0U == (0x0000001fU 
                                         & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) 
                                 | (4U == (0x0000001fU 
                                           & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                | (8U == (0x0000001fU 
                                          & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                               | (0x0cU == (0x0000001fU 
                                            & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))));
                    }
                } else if ((0x00000040U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
                    if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)) 
                         & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) {
                        milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                            = ((((0U == (0x0000001fU 
                                         & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) 
                                 | (4U == (0x0000001fU 
                                           & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                | (8U == (0x0000001fU 
                                          & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                               | (0x0cU == (0x0000001fU 
                                            & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))));
                    }
                } else if ((0x00000020U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
                    if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)) 
                         & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) {
                        milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                            = ((((0U == (0x0000001fU 
                                         & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) 
                                 | (4U == (0x0000001fU 
                                           & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                | (8U == (0x0000001fU 
                                          & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                               | (0x0cU == (0x0000001fU 
                                            & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))));
                    }
                } else if ((0x00000010U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
                    if ((8U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
                        if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)) 
                             & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) {
                            milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                = ((((0U == (0x0000001fU 
                                             & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) 
                                     | (4U == (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                    | (8U == (0x0000001fU 
                                              & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                   | (0x0cU == (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))));
                        }
                    } else if ((4U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
                        if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)) 
                             & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) {
                            milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                = ((((0U == (0x0000001fU 
                                             & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) 
                                     | (4U == (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                    | (8U == (0x0000001fU 
                                              & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                   | (0x0cU == (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))));
                        }
                    } else if ((2U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
                        if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)) 
                             & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) {
                            milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                = ((((0U == (0x0000001fU 
                                             & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) 
                                     | (4U == (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                    | (8U == (0x0000001fU 
                                              & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                   | (0x0cU == (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))));
                        }
                    } else if ((1U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
                        if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)) 
                             & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) {
                            milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                = ((((0U == (0x0000001fU 
                                             & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) 
                                     | (4U == (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                    | (8U == (0x0000001fU 
                                              & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                   | (0x0cU == (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))));
                        }
                    } else {
                        milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw = 1U;
                    }
                } else if ((2U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
                    if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)) 
                         & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) {
                        milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                            = ((((0U == (0x0000001fU 
                                         & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) 
                                 | (4U == (0x0000001fU 
                                           & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                | (8U == (0x0000001fU 
                                          & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                               | (0x0cU == (0x0000001fU 
                                            & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))));
                    }
                } else if ((1U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
                    if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)) 
                         & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) {
                        milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                            = ((((0U == (0x0000001fU 
                                         & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) 
                                 | (4U == (0x0000001fU 
                                           & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                | (8U == (0x0000001fU 
                                          & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                               | (0x0cU == (0x0000001fU 
                                            & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))));
                    }
                } else {
                    milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw = 1U;
                }
            } else if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)) 
                        & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) {
                milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                    = ((((0U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) 
                         | (4U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                        | (8U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                       | (0x0cU == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))));
            }
        } else if ((0x00000100U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
            if ((0x00000080U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
                if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)) 
                     & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) {
                    milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                        = ((((0U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) 
                             | (4U == (0x0000001fU 
                                       & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                            | (8U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                           | (0x0cU == (0x0000001fU 
                                        & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))));
                }
            } else if ((0x00000040U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
                if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)) 
                     & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) {
                    milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                        = ((((0U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) 
                             | (4U == (0x0000001fU 
                                       & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                            | (8U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                           | (0x0cU == (0x0000001fU 
                                        & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))));
                }
            } else if ((0x00000020U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
                if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)) 
                     & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) {
                    milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                        = ((((0U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) 
                             | (4U == (0x0000001fU 
                                       & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                            | (8U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                           | (0x0cU == (0x0000001fU 
                                        & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))));
                }
            } else if ((0x00000010U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
                if ((8U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
                    if ((4U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
                        if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)) 
                             & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) {
                            milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                = ((((0U == (0x0000001fU 
                                             & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) 
                                     | (4U == (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                    | (8U == (0x0000001fU 
                                              & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                   | (0x0cU == (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))));
                        }
                    } else if ((2U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
                        if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)) 
                             & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) {
                            milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                = ((((0U == (0x0000001fU 
                                             & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) 
                                     | (4U == (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                    | (8U == (0x0000001fU 
                                              & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                   | (0x0cU == (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))));
                        }
                    } else if ((1U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
                        if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)) 
                             & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) {
                            milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                = ((((0U == (0x0000001fU 
                                             & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) 
                                     | (4U == (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                    | (8U == (0x0000001fU 
                                              & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                   | (0x0cU == (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))));
                        }
                    } else {
                        milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw = 1U;
                    }
                } else if ((4U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
                    if ((2U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
                        if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)) 
                             & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) {
                            milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                = ((((0U == (0x0000001fU 
                                             & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) 
                                     | (4U == (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                    | (8U == (0x0000001fU 
                                              & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                   | (0x0cU == (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))));
                        }
                    } else if ((1U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
                        if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)) 
                             & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) {
                            milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                                = ((((0U == (0x0000001fU 
                                             & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) 
                                     | (4U == (0x0000001fU 
                                               & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                    | (8U == (0x0000001fU 
                                              & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                   | (0x0cU == (0x0000001fU 
                                                & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))));
                        }
                    } else {
                        milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw = 1U;
                    }
                } else if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)) 
                            & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) {
                    milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                        = ((((0U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) 
                             | (4U == (0x0000001fU 
                                       & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                            | (8U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                           | (0x0cU == (0x0000001fU 
                                        & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))));
                }
            } else if ((2U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
                if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)) 
                     & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) {
                    milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                        = ((((0U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) 
                             | (4U == (0x0000001fU 
                                       & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                            | (8U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                           | (0x0cU == (0x0000001fU 
                                        & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))));
                }
            } else if ((1U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
                if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)) 
                     & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) {
                    milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                        = ((((0U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) 
                             | (4U == (0x0000001fU 
                                       & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                            | (8U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                           | (0x0cU == (0x0000001fU 
                                        & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))));
                }
            } else {
                milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw = 1U;
            }
        } else if ((0x00000080U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
            if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)) 
                 & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) {
                milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                    = ((((0U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) 
                         | (4U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                        | (8U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                       | (0x0cU == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))));
            }
        } else if ((0x00000040U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
            if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)) 
                 & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) {
                milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                    = ((((0U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) 
                         | (4U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                        | (8U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                       | (0x0cU == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))));
            }
        } else if ((0x00000020U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
            if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)) 
                 & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) {
                milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                    = ((((0U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) 
                         | (4U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                        | (8U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                       | (0x0cU == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))));
            }
        } else if ((0x00000010U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
            if ((8U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
                if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)) 
                     & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) {
                    milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                        = ((((0U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) 
                             | (4U == (0x0000001fU 
                                       & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                            | (8U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                           | (0x0cU == (0x0000001fU 
                                        & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))));
                }
            } else if ((4U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
                if ((2U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
                    if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)) 
                         & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) {
                        milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                            = ((((0U == (0x0000001fU 
                                         & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) 
                                 | (4U == (0x0000001fU 
                                           & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                | (8U == (0x0000001fU 
                                          & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                               | (0x0cU == (0x0000001fU 
                                            & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))));
                    }
                } else if ((1U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
                    if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)) 
                         & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) {
                        milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                            = ((((0U == (0x0000001fU 
                                         & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) 
                                 | (4U == (0x0000001fU 
                                           & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                | (8U == (0x0000001fU 
                                          & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                               | (0x0cU == (0x0000001fU 
                                            & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))));
                    }
                } else {
                    milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw = 1U;
                }
            } else if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)) 
                        & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) {
                milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                    = ((((0U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) 
                         | (4U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                        | (8U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                       | (0x0cU == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))));
            }
        } else if ((8U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
            if ((4U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
                if ((2U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
                    if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)) 
                         & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) {
                        milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                            = ((((0U == (0x0000001fU 
                                         & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) 
                                 | (4U == (0x0000001fU 
                                           & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                | (8U == (0x0000001fU 
                                          & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                               | (0x0cU == (0x0000001fU 
                                            & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))));
                    }
                } else if ((1U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) {
                    if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)) 
                         & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) {
                        milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                            = ((((0U == (0x0000001fU 
                                         & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) 
                                 | (4U == (0x0000001fU 
                                           & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                                | (8U == (0x0000001fU 
                                          & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                               | (0x0cU == (0x0000001fU 
                                            & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))));
                    }
                } else {
                    milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw = 1U;
                }
            } else if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)) 
                        & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) {
                milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                    = ((((0U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) 
                         | (4U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                        | (8U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                       | (0x0cU == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))));
            }
        } else if (((0x0400U <= (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)) 
                    & (0x04a0U > (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) {
            milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw 
                = ((((0U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))) 
                     | (4U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                    | (8U == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a)))) 
                   | (0x0cU == (0x0000001fU & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a))));
        }
    }
    vlSelfRef.milan_datapath__DOT__csr__DOT__shadow_axi_we 
        = milan_datapath__DOT__csr__DOT____VlemCall_1__is_plain_rw;
    vlSelfRef.milan_datapath__DOT____Vcellinp__pp_shadow__enable_i 
        = (1U & (vlSelfRef.milan_datapath__DOT__csr__DOT__g_pp_csr__DOT__pp_ctrl_r 
                 | vlSelfRef.milan_datapath__DOT__csr__DOT__adp_ctrl));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__nvm_wvalid_w 
        = ((5U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__state_r)) 
           | ((6U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__state_r)) 
              & (0x0eU == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__hs_r))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__nvm_rready_w 
        = ((9U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__state_r)) 
           | ((0x0dU == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__state_r)) 
              & (3U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__hs_r))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__fl_giveup_w 
        = ((2U <= vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__fl_retry_r) 
           & (((0x0fU == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__hs_r)) 
               | (0x0eU == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__hs_r))) 
              & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__nvm_err_w)));
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
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__fsm_rd_req_w 
        = ((5U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__hs_r)) 
           | (0x0aU == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__hs_r)));
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
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__cap_active_w 
        = ((0U != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__hs_r)) 
           & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__recwr_en_w));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__c1_vld_r 
        = ((IData)(vlSelfRef.axis_resetn) && (1U & 
                                              (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__cap_rec_w[0U] 
                                               >> 0x0000000bU)));
    vlSelfRef.milan_datapath__DOT__crf_rx__DOT__w_ev_tu_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__avtprx_tv_bit) 
           & (IData)(vlSelfRef.milan_datapath__DOT__crf_rx__DOT__w_acc));
    vlSelfRef.milan_datapath__DOT__crf_rx__DOT__w_ev_mr_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__crf_rx__DOT__w_acc) 
           & ((IData)(vlSelfRef.milan_datapath__DOT__crf_rx__DOT__mr_seeded_r) 
              & ((IData)(vlSelfRef.milan_datapath__DOT__avtprx_mr_bit) 
                 != (IData)(vlSelfRef.milan_datapath__DOT__crf_rx__DOT__prev_mr_r))));
    vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__in_acc 
        = ((IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__s_tvalid_q) 
           & (IData)(vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__s_tready_q));
    vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__hdr[0U] 
        = vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_parser__DOT__hdr[0U];
    vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__hdr[1U] 
        = vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_parser__DOT__hdr[1U];
    vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__hdr[2U] 
        = vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_parser__DOT__hdr[2U];
    vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__hdr[3U] 
        = vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_parser__DOT__hdr[3U];
    vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__hdr[4U] 
        = vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_parser__DOT__hdr[4U];
    vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__hdr[5U] 
        = vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_parser__DOT__hdr[5U];
    vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__hdr[6U] 
        = vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_parser__DOT__hdr[6U];
    vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__hdr[7U] 
        = vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_parser__DOT__hdr[7U];
    vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__hdr[8U] 
        = vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_parser__DOT__hdr[8U];
    vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__hdr[9U] 
        = vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_parser__DOT__hdr[9U];
    vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__hdr[10U] 
        = vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_parser__DOT__hdr[10U];
    vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__hdr[11U] 
        = vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_parser__DOT__hdr[11U];
    vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__hdr[12U] 
        = vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_parser__DOT__hdr[12U];
    vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__hdr[13U] 
        = vlSelfRef.__Vdly__milan_datapath__DOT__avtp_rx_parser__DOT__hdr[13U];
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__backed_n_w 
        = ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__loss_ev_w)) 
           & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__backed_r) 
              | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__hb_kick_w)));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__dirty_live_n_w 
        = (((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__reload_ok_w)) 
            & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__arm_ok_w)) 
               & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__dirty_live_r) 
                  | ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__dirty_cap_r) 
                     & (IData)(milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__drop_w))))) 
           | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__rec_close_w));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__dirty_cap_n_w 
        = ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__reload_ok_w)) 
           & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__arm_ok_w)
               ? (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__dirty_live_r)
               : ((~ ((IData)(milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__drop_w) 
                      | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__ack_ok_w))) 
                  & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__dirty_cap_r))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__advance_e_w 
        = ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__stall_e_w)) 
           & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__vld_e_r));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__ntfy_stri_out_w 
        = ((2U & ((0xfffffffeU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_lstn_reg_change_w)) 
                  | (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_gate_src_w) 
                      & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_86)) 
                     << 1U))) | (1U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_lstn_reg_change_w) 
                                       | ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_gate_src_w)) 
                                          & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_86)))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__ev_iss_w 
        = ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_ca_builder__DOT__cancel_hit_w)) 
           & ((IData)(__VdfgRegularize_h6e95ff9d_0_195) 
              & ((4U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_ca_builder__DOT__c_st_r)) 
                 & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__pend_ok_w)) 
                    & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__free_ok_w)))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__ev_exp_w 
        = ((IData)(__VdfgRegularize_h6e95ff9d_0_195) 
           & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__pend_ok_w));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__grant_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pool_alloc_req_w) 
           & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__pick_ok_w));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__adp_prng_valid_w 
        = ((2U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pr_owner_r)) 
           & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_12));
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
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__sb_pick_aecp_w 
        = (((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__acmp_sb_candidate_w)) 
            | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__sb_prefer_aecp_r)) 
           & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__aecp_sb_candidate_w));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__span_ok_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__rec_hit_w) 
           & ((vlSelfRef.__VdfgRegularize_h6e95ff9d_0_192 
               <= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__rec_len_w)) 
              & ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__rec_base_w 
                  + vlSelfRef.__VdfgRegularize_h6e95ff9d_0_192) 
                 <= vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__img_len_r)));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__enable_rise_w 
        = ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__enable_q_r)) 
           & (IData)(vlSelfRef.milan_datapath__DOT____Vcellinp__pp_shadow__enable_i));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__enable_fall_w 
        = ((~ (IData)(vlSelfRef.milan_datapath__DOT____Vcellinp__pp_shadow__enable_i)) 
           & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__enable_q_r));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__fsm_rd_gnt_w 
        = ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__cap_active_w)) 
           & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__fsm_rd_req_w));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__go_take_w 
        = ((1U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__hs_r)) 
           & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__go_pend_r) 
              | (vlSelfRef.milan_datapath__DOT__csr__DOT__g_pp_csr__DOT__pp_ctrl_r 
                 >> 1U)));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_260 = ((3U 
                                                   == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__hs_r)) 
                                                  | ((4U 
                                                      == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__hs_r)) 
                                                     | ((5U 
                                                         == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__hs_r)) 
                                                        | ((2U 
                                                            == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__hs_r)) 
                                                           | ((6U 
                                                               == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__hs_r)) 
                                                              | (7U 
                                                                 == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__hs_r)))))));
    vlSelfRef.milan_datapath__DOT__crf_rx__DOT__w_ev_sm_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__crf_rx__DOT__w_acc) 
           & ((IData)(vlSelfRef.milan_datapath__DOT__crf_rx__DOT__have_seq_r) 
              & ((IData)(vlSelfRef.milan_datapath__DOT__avtprx_seq) 
                 != (IData)(vlSelfRef.milan_datapath__DOT__crf_rx__DOT__exp_seq_r))));
    vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__et_off 
        = ((IData)((0x81000000U == (0xffff0000U & vlSelfRef.milan_datapath__DOT__avtp_rx_parser__DOT__hdr[10U])))
            ? 0x10U : 0x0cU);
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__resp_send_w 
        = (IData)(((0x0000e00000000000ULL == (0x0000f80000000000ULL 
                                              & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__uop_e_r)) 
                   & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__advance_e_w)));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__aecp_eff_notify_stb_nc_w 
        = (IData)(((0x0000b80000000000ULL == (0x0000f80000000000ULL 
                                              & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__uop_e_r)) 
                   & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__advance_e_w)));
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__org_withdraw_slot_mask_w = 0U;
    if ((1U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__cancel_work_w) 
               & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__valid_r)))) {
        milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__org_withdraw_slot_mask_w 
            = ((IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__org_withdraw_slot_mask_w) 
               | (0x00ffU & ((IData)(1U) << vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__txs_r[0U])));
    }
    if ((2U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__cancel_work_w) 
               & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__valid_r)))) {
        milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__org_withdraw_slot_mask_w 
            = ((IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__org_withdraw_slot_mask_w) 
               | (0x00ffU & ((IData)(1U) << vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__txs_r[1U])));
    }
    if ((4U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__cancel_work_w) 
               & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__valid_r)))) {
        milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__org_withdraw_slot_mask_w 
            = ((IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__org_withdraw_slot_mask_w) 
               | (0x00ffU & ((IData)(1U) << vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__txs_r[2U])));
    }
    if ((8U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__cancel_work_w) 
               & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__valid_r)))) {
        milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__org_withdraw_slot_mask_w 
            = ((IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__org_withdraw_slot_mask_w) 
               | (0x00ffU & ((IData)(1U) << vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__txs_r[3U])));
    }
    if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__ev_rsp_w) {
        milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__org_withdraw_slot_mask_w 
            = ((IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__org_withdraw_slot_mask_w) 
               | (0x00ffU & ((IData)(1U) << vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__txs_r
                             [vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__hit_ix_w])));
    }
    if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__ev_exp_w) 
          & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__valid_r) 
             >> (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__pend_ix_w))) 
         & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__retried_r) 
            >> (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__pend_ix_w)))) {
        milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__org_withdraw_slot_mask_w 
            = ((IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__org_withdraw_slot_mask_w) 
               | (0x00ffU & ((IData)(1U) << vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__txs_r
                             [vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__pend_ix_w])));
    }
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__sb_pick_acmp_w 
        = ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__sb_pick_aecp_w)) 
           & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__acmp_sb_candidate_w));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__gnt_opmut_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__gnt_now_w) 
           & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__mut_req_w) 
              & ((0U != vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__img_len_r) 
                 & ((0U != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__eff_len_w)) 
                    & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__span_ok_w)))));
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__fsm_wr_req_w 
        = (((0U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__hs_r)) 
            & (2U > (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__init_cnt_r))) 
           | ((~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__touched_r) 
                  >> (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__rs_k_r))) 
              & (4U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__hs_r))));
    vlSelfRef.milan_datapath__DOT__pp_restore_busy_w 
        = ((8U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__hs_r)) 
           | (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_260));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__c1_sink_r 
        = ((IData)(vlSelfRef.axis_resetn) && (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__recwr_addr_w));
    if ((0U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__xs_r))) {
        VL_ASSIGN_W(384, vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__cap_rec_w, Vmilan_datapath__ConstPool__CONST_h997e551f_0);
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__recwr_addr_w 
            = (1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__init_cnt_r));
    } else {
        if ((2U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__xs_r))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__cap_rec_w[0U] 
                = (0x00000809U | (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__preL_sw_r) 
                                   << 0x0000000dU) 
                                  | ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__preL_started_r) 
                                     << 0x0000000cU)));
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__cap_rec_w[1U] 
                = (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__preL_talker_eid_r);
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__cap_rec_w[2U] 
                = (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__preL_talker_eid_r 
                           >> 0x00000020U));
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__cap_rec_w[3U] 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__preL_talker_uid_r;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__cap_rec_w[4U] 
                = (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__preL_ctlr_eid_r);
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__cap_rec_w[5U] 
                = (IData)((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__preL_ctlr_eid_r 
                           >> 0x00000020U));
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__cap_rec_w[6U] = 0U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__cap_rec_w[7U] = 0U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__cap_rec_w[8U] = 0U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__cap_rec_w[9U] = 0U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__cap_rec_w[10U] = 0U;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__cap_rec_w[11U] 
                = (0x0000ff00U & (((IData)(3U) + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__sink_r)) 
                                  << 8U));
        } else {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__cap_rec_w[0U] 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__rec_r[0U];
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__cap_rec_w[1U] 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__rec_r[1U];
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__cap_rec_w[2U] 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__rec_r[2U];
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__cap_rec_w[3U] 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__rec_r[3U];
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__cap_rec_w[4U] 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__rec_r[4U];
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__cap_rec_w[5U] 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__rec_r[5U];
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__cap_rec_w[6U] 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__rec_r[6U];
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__cap_rec_w[7U] 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__rec_r[7U];
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__cap_rec_w[8U] 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__rec_r[8U];
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__cap_rec_w[9U] 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__rec_r[9U];
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__cap_rec_w[10U] 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__rec_r[10U];
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__cap_rec_w[11U] 
                = ((0xffff0000U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__rec_r[11U]) 
                   | ((0x0000ff00U & (((IData)(3U) 
                                       + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__sink_r)) 
                                      << 8U)) | (0x000000ffU 
                                                 & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__rec_r[11U])));
        }
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__recwr_addr_w 
            = (1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__sink_r));
    }
    vlSelfRef.milan_datapath__DOT__crf_rx__DOT__w_ev_si_w 
        = ((2U <= (0x000000ffU & ((IData)(vlSelfRef.milan_datapath__DOT__avtprx_seq) 
                                  - (IData)(vlSelfRef.milan_datapath__DOT__crf_rx__DOT__exp_seq_r)))) 
           & (IData)(vlSelfRef.milan_datapath__DOT__crf_rx__DOT__w_ev_sm_w));
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
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__rsp_seal_w 
        = ((0x0fU == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__a_st_r)) 
           | ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__ucpu_done_w) 
              & ((3U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__a_st_r)) 
                 & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gdi_r)) 
                    & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__sent_r) 
                       | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__resp_send_w))))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT____Vcellinp__u_notify__ev_amap_i 
        = ((6U == (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__uop_e_r))) 
           & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__aecp_eff_notify_stb_nc_w));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__cmd_push_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__aecp_eff_notify_stb_nc_w) 
           & ((0x10U > (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__cmdq_count_r)) 
              & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__cmd_class_ok_w)));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__arb_start_abort_w 
        = (1U & (((IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__org_withdraw_slot_mask_w) 
                  >> (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__slot_r)) 
                 | (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_69)));
    __VdfgRegularize_h6e95ff9d_0_257 = ((0U != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_org_cnt_r)) 
                                        & (((IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__org_withdraw_slot_mask_w) 
                                            >> (7U 
                                                & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_org_r)) 
                                           | (Vmilan_datapath__ConstPool__TABLE_h5f1389fb_0
                                              [vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_release_merge__DOT__available_w] 
                                              & ((7U 
                                                  & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_org_r) 
                                                 == Vmilan_datapath__ConstPool__TABLE_h6dff1152_0
                                                 [vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_release_merge__DOT__available_w]))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__sb_adm_req_w 
        = ((IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__sb_pick_acmp_w) 
           | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__sb_pick_aecp_w));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__sb_adm_key_w = 0U;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__sb_adm_class_w = 0U;
    if (milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__sb_pick_acmp_w) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__sb_adm_key_w 
            = (0x0000ffffU & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_acmp_q__DOT__out_data_r[1U] 
                              >> 5U));
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__sb_adm_class_w 
            = (0x0000000fU & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_acmp_q__DOT__out_data_r[1U] 
                              >> 0x00000015U));
    } else if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__sb_pick_aecp_w) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__sb_adm_key_w 
            = (0x0000ffffU & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__out_data_r[1U] 
                              >> 5U));
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__sb_adm_class_w 
            = (0x0000000fU & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__out_data_r[1U] 
                              >> 0x00000015U));
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__void_grant_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__gnt_opmut_w) 
           & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__cap_att_r)) 
              & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__cap_open_r)));
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
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__accept_w 
        = ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__arb_start_abort_w)) 
           & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_201));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_259 = ((1U 
                                                   == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__arb_st_r)) 
                                                  & (((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__arb_start_abort_w)) 
                                                      | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__start_sent_r)) 
                                                     & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__run_r)) 
                                                        & (2U 
                                                           == vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__st_r
                                                           [vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__slot_r]))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_org_next_w = 0U;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_org_next_cnt_w = 0U;
    if (((((0U < (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_org_cnt_r)) 
           & (~ (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__gnt_r) 
                  >> 7U) | ((0U != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_org_cnt_r)) 
                            & ((~ (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_242)) 
                               | (IData)(__VdfgRegularize_h6e95ff9d_0_257)))))) 
          & (~ (Vmilan_datapath__ConstPool__TABLE_h5f1389fb_0
                [vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_release_merge__DOT__available_w] 
                & ((7U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_org_r) 
                   == Vmilan_datapath__ConstPool__TABLE_h6dff1152_0
                   [vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_release_merge__DOT__available_w])))) 
         & (~ ((IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__org_withdraw_slot_mask_w) 
               >> (7U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_org_r))))) {
        if ((0x17U >= (0x0000001fU & ((IData)(3U) * 
                                      (7U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_org_next_cnt_w)))))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_org_next_w 
                = (((~ ((IData)(7U) << (0x0000001fU 
                                        & ((IData)(3U) 
                                           * (7U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_org_next_cnt_w)))))) 
                    & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_org_next_w) 
                   | (0x00ffffffU & ((7U & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_org_r) 
                                     << (0x0000001fU 
                                         & ((IData)(3U) 
                                            * (7U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_org_next_cnt_w)))))));
        }
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_org_next_cnt_w 
            = (0x0000000fU & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_org_next_cnt_w)));
    }
    if ((((1U < (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_org_cnt_r)) 
          & (~ (Vmilan_datapath__ConstPool__TABLE_h5f1389fb_0
                [vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_release_merge__DOT__available_w] 
                & ((7U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_org_r 
                          >> 3U)) == Vmilan_datapath__ConstPool__TABLE_h6dff1152_0
                   [vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_release_merge__DOT__available_w])))) 
         & (~ ((IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__org_withdraw_slot_mask_w) 
               >> (7U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_org_r 
                         >> 3U)))))) {
        if ((0x17U >= (0x0000001fU & ((IData)(3U) * 
                                      (7U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_org_next_cnt_w)))))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_org_next_w 
                = (((~ ((IData)(7U) << (0x0000001fU 
                                        & ((IData)(3U) 
                                           * (7U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_org_next_cnt_w)))))) 
                    & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_org_next_w) 
                   | (0x00ffffffU & ((7U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_org_r 
                                            >> 3U)) 
                                     << (0x0000001fU 
                                         & ((IData)(3U) 
                                            * (7U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_org_next_cnt_w)))))));
        }
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_org_next_cnt_w 
            = (0x0000000fU & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_org_next_cnt_w)));
    }
    if ((((2U < (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_org_cnt_r)) 
          & (~ (Vmilan_datapath__ConstPool__TABLE_h5f1389fb_0
                [vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_release_merge__DOT__available_w] 
                & ((7U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_org_r 
                          >> 6U)) == Vmilan_datapath__ConstPool__TABLE_h6dff1152_0
                   [vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_release_merge__DOT__available_w])))) 
         & (~ ((IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__org_withdraw_slot_mask_w) 
               >> (7U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_org_r 
                         >> 6U)))))) {
        if ((0x17U >= (0x0000001fU & ((IData)(3U) * 
                                      (7U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_org_next_cnt_w)))))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_org_next_w 
                = (((~ ((IData)(7U) << (0x0000001fU 
                                        & ((IData)(3U) 
                                           * (7U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_org_next_cnt_w)))))) 
                    & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_org_next_w) 
                   | (0x00ffffffU & ((7U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_org_r 
                                            >> 6U)) 
                                     << (0x0000001fU 
                                         & ((IData)(3U) 
                                            * (7U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_org_next_cnt_w)))))));
        }
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_org_next_cnt_w 
            = (0x0000000fU & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_org_next_cnt_w)));
    }
    if ((((3U < (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_org_cnt_r)) 
          & (~ (Vmilan_datapath__ConstPool__TABLE_h5f1389fb_0
                [vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_release_merge__DOT__available_w] 
                & ((7U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_org_r 
                          >> 9U)) == Vmilan_datapath__ConstPool__TABLE_h6dff1152_0
                   [vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_release_merge__DOT__available_w])))) 
         & (~ ((IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__org_withdraw_slot_mask_w) 
               >> (7U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_org_r 
                         >> 9U)))))) {
        if ((0x17U >= (0x0000001fU & ((IData)(3U) * 
                                      (7U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_org_next_cnt_w)))))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_org_next_w 
                = (((~ ((IData)(7U) << (0x0000001fU 
                                        & ((IData)(3U) 
                                           * (7U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_org_next_cnt_w)))))) 
                    & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_org_next_w) 
                   | (0x00ffffffU & ((7U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_org_r 
                                            >> 9U)) 
                                     << (0x0000001fU 
                                         & ((IData)(3U) 
                                            * (7U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_org_next_cnt_w)))))));
        }
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_org_next_cnt_w 
            = (0x0000000fU & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_org_next_cnt_w)));
    }
    if ((((4U < (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_org_cnt_r)) 
          & (~ (Vmilan_datapath__ConstPool__TABLE_h5f1389fb_0
                [vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_release_merge__DOT__available_w] 
                & ((7U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_org_r 
                          >> 0x0cU)) == Vmilan_datapath__ConstPool__TABLE_h6dff1152_0
                   [vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_release_merge__DOT__available_w])))) 
         & (~ ((IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__org_withdraw_slot_mask_w) 
               >> (7U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_org_r 
                         >> 0x0cU)))))) {
        if ((0x17U >= (0x0000001fU & ((IData)(3U) * 
                                      (7U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_org_next_cnt_w)))))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_org_next_w 
                = (((~ ((IData)(7U) << (0x0000001fU 
                                        & ((IData)(3U) 
                                           * (7U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_org_next_cnt_w)))))) 
                    & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_org_next_w) 
                   | (0x00ffffffU & ((7U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_org_r 
                                            >> 0x0cU)) 
                                     << (0x0000001fU 
                                         & ((IData)(3U) 
                                            * (7U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_org_next_cnt_w)))))));
        }
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_org_next_cnt_w 
            = (0x0000000fU & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_org_next_cnt_w)));
    }
    if ((((5U < (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_org_cnt_r)) 
          & (~ (Vmilan_datapath__ConstPool__TABLE_h5f1389fb_0
                [vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_release_merge__DOT__available_w] 
                & ((7U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_org_r 
                          >> 0x0fU)) == Vmilan_datapath__ConstPool__TABLE_h6dff1152_0
                   [vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_release_merge__DOT__available_w])))) 
         & (~ ((IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__org_withdraw_slot_mask_w) 
               >> (7U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_org_r 
                         >> 0x0fU)))))) {
        if ((0x17U >= (0x0000001fU & ((IData)(3U) * 
                                      (7U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_org_next_cnt_w)))))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_org_next_w 
                = (((~ ((IData)(7U) << (0x0000001fU 
                                        & ((IData)(3U) 
                                           * (7U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_org_next_cnt_w)))))) 
                    & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_org_next_w) 
                   | (0x00ffffffU & ((7U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_org_r 
                                            >> 0x0fU)) 
                                     << (0x0000001fU 
                                         & ((IData)(3U) 
                                            * (7U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_org_next_cnt_w)))))));
        }
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_org_next_cnt_w 
            = (0x0000000fU & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_org_next_cnt_w)));
    }
    if ((((6U < (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_org_cnt_r)) 
          & (~ (Vmilan_datapath__ConstPool__TABLE_h5f1389fb_0
                [vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_release_merge__DOT__available_w] 
                & ((7U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_org_r 
                          >> 0x12U)) == Vmilan_datapath__ConstPool__TABLE_h6dff1152_0
                   [vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_release_merge__DOT__available_w])))) 
         & (~ ((IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__org_withdraw_slot_mask_w) 
               >> (7U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_org_r 
                         >> 0x12U)))))) {
        if ((0x17U >= (0x0000001fU & ((IData)(3U) * 
                                      (7U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_org_next_cnt_w)))))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_org_next_w 
                = (((~ ((IData)(7U) << (0x0000001fU 
                                        & ((IData)(3U) 
                                           * (7U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_org_next_cnt_w)))))) 
                    & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_org_next_w) 
                   | (0x00ffffffU & ((7U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_org_r 
                                            >> 0x12U)) 
                                     << (0x0000001fU 
                                         & ((IData)(3U) 
                                            * (7U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_org_next_cnt_w)))))));
        }
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_org_next_cnt_w 
            = (0x0000000fU & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_org_next_cnt_w)));
    }
    if ((((7U < (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_org_cnt_r)) 
          & (~ (Vmilan_datapath__ConstPool__TABLE_h5f1389fb_0
                [vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_release_merge__DOT__available_w] 
                & ((7U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_org_r 
                          >> 0x15U)) == Vmilan_datapath__ConstPool__TABLE_h6dff1152_0
                   [vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_release_merge__DOT__available_w])))) 
         & (~ ((IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__org_withdraw_slot_mask_w) 
               >> (7U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_org_r 
                         >> 0x15U)))))) {
        if ((0x17U >= (0x0000001fU & ((IData)(3U) * 
                                      (7U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_org_next_cnt_w)))))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_org_next_w 
                = (((~ ((IData)(7U) << (0x0000001fU 
                                        & ((IData)(3U) 
                                           * (7U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_org_next_cnt_w)))))) 
                    & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_org_next_w) 
                   | (0x00ffffffU & ((7U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_org_r 
                                            >> 0x15U)) 
                                     << (0x0000001fU 
                                         & ((IData)(3U) 
                                            * (7U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_org_next_cnt_w)))))));
        }
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_org_next_cnt_w 
            = (0x0000000fU & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_org_next_cnt_w)));
    }
    if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__org_send_valid_w) 
          | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__org_resend_valid_w)) 
         & (8U != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_org_next_cnt_w)))) {
        if ((0x17U >= (0x0000001fU & ((IData)(3U) * 
                                      (7U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_org_next_cnt_w)))))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_org_next_w 
                = (((~ ((IData)(7U) << (0x0000001fU 
                                        & ((IData)(3U) 
                                           * (7U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_org_next_cnt_w)))))) 
                    & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_org_next_w) 
                   | (0x00ffffffU & (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__org_resend_valid_w)
                                       ? (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__org_resend_slot_w)
                                       : (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__org_send_slot_w)) 
                                     << (0x0000001fU 
                                         & ((IData)(3U) 
                                            * (7U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_org_next_cnt_w)))))));
        }
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_org_next_cnt_w 
            = (0x0000000fU & ((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_org_next_cnt_w)));
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__arb_req_w 
        = (((((((0U != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_org_cnt_r)) 
                & ((~ (IData)(__VdfgRegularize_h6e95ff9d_0_257)) 
                   & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_242))) 
               << 3U) | ((8U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__w_st_r)) 
                         << 2U)) | (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_lane_valid_r) 
                                     << 1U) | (0x0fU 
                                               == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__st_r)))) 
            << 4U) | ((((0U != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_adp_cnt_r)) 
                        << 3U) | ((0U != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_acmp_cnt_r)) 
                                  << 2U)) | ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__uns_r) 
                                               & (7U 
                                                  == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__a_st_r))) 
                                              << 1U) 
                                             | ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__uns_r)) 
                                                & (7U 
                                                   == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__a_st_r))))));
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__conflict_any_w = 0U;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__b_key 
        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__key_r[0U];
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__b_cls 
        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__cls_r[0U];
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__a_key 
        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__sb_adm_key_w;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__a_cls 
        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__sb_adm_class_w;
    {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT____VlemCall_0__hz_conflict = 0;
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__same_key_v = 0;
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__other_v = 0;
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__same_key_v 
            = ((IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__a_key) 
               == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__b_key));
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__other_v 
            = ((6U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__a_cls))
                ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__b_cls)
                : (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__a_cls));
        if (((1U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__a_cls)) 
             | (1U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__b_cls)))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT____VlemCall_0__hz_conflict = 1U;
            goto __Vlabel0;
        }
        if (((0U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__a_cls)) 
             & (0U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__b_cls)))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT____VlemCall_0__hz_conflict = 0U;
            goto __Vlabel0;
        }
        if (((0U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__a_cls)) 
             | (0U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__b_cls)))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT____VlemCall_0__hz_conflict 
                = vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__same_key_v;
            goto __Vlabel0;
        }
        if (((6U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__a_cls)) 
             | (6U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__b_cls)))) {
            vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_is_lockprot__133__c 
                = vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__other_v;
            vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_is_lockprot__133__Vfuncout = 0;
            vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_is_lockprot__133__Vfuncout 
                = ((((((1U == (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_is_lockprot__133__c)) 
                       | (2U == (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_is_lockprot__133__c))) 
                      | (3U == (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_is_lockprot__133__c))) 
                     | (4U == (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_is_lockprot__133__c))) 
                    | (5U == (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_is_lockprot__133__c))) 
                   | (8U == (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_is_lockprot__133__c)));
            vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132____VlefCall_0__hz_is_lockprot 
                = vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_is_lockprot__133__Vfuncout;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT____VlemCall_0__hz_conflict 
                = ((6U == (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__other_v)) 
                   | (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132____VlefCall_0__hz_is_lockprot));
            goto __Vlabel0;
        }
        if (((IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__a_cls) 
             == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__b_cls))) {
            if (((7U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__a_cls)) 
                 | (8U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__a_cls)))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT____VlemCall_0__hz_conflict = 1U;
                goto __Vlabel0;
            }
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT____VlemCall_0__hz_conflict 
                = vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__same_key_v;
            goto __Vlabel0;
        }
        if ((((2U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__a_cls)) 
              & (3U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__b_cls))) 
             | ((3U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__a_cls)) 
                & (2U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__b_cls))))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT____VlemCall_0__hz_conflict = 1U;
            goto __Vlabel0;
        }
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT____VlemCall_0__hz_conflict = 0U;
        __Vlabel0: ;
    }
    if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__valid_r) 
         & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT____VlemCall_0__hz_conflict))) {
        milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__conflict_any_w = 1U;
    }
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__b_key 
        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__key_r[1U];
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__b_cls 
        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__cls_r[1U];
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__a_key 
        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__sb_adm_key_w;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__a_cls 
        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__sb_adm_class_w;
    {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT____VlemCall_0__hz_conflict = 0;
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__same_key_v = 0;
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__other_v = 0;
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__same_key_v 
            = ((IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__a_key) 
               == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__b_key));
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__other_v 
            = ((6U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__a_cls))
                ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__b_cls)
                : (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__a_cls));
        if (((1U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__a_cls)) 
             | (1U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__b_cls)))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT____VlemCall_0__hz_conflict = 1U;
            goto __Vlabel1;
        }
        if (((0U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__a_cls)) 
             & (0U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__b_cls)))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT____VlemCall_0__hz_conflict = 0U;
            goto __Vlabel1;
        }
        if (((0U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__a_cls)) 
             | (0U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__b_cls)))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT____VlemCall_0__hz_conflict 
                = vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__same_key_v;
            goto __Vlabel1;
        }
        if (((6U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__a_cls)) 
             | (6U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__b_cls)))) {
            vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_is_lockprot__133__c 
                = vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__other_v;
            vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_is_lockprot__133__Vfuncout = 0;
            vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_is_lockprot__133__Vfuncout 
                = ((((((1U == (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_is_lockprot__133__c)) 
                       | (2U == (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_is_lockprot__133__c))) 
                      | (3U == (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_is_lockprot__133__c))) 
                     | (4U == (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_is_lockprot__133__c))) 
                    | (5U == (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_is_lockprot__133__c))) 
                   | (8U == (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_is_lockprot__133__c)));
            vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132____VlefCall_0__hz_is_lockprot 
                = vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_is_lockprot__133__Vfuncout;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT____VlemCall_0__hz_conflict 
                = ((6U == (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__other_v)) 
                   | (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132____VlefCall_0__hz_is_lockprot));
            goto __Vlabel1;
        }
        if (((IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__a_cls) 
             == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__b_cls))) {
            if (((7U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__a_cls)) 
                 | (8U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__a_cls)))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT____VlemCall_0__hz_conflict = 1U;
                goto __Vlabel1;
            }
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT____VlemCall_0__hz_conflict 
                = vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__same_key_v;
            goto __Vlabel1;
        }
        if ((((2U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__a_cls)) 
              & (3U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__b_cls))) 
             | ((3U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__a_cls)) 
                & (2U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__b_cls))))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT____VlemCall_0__hz_conflict = 1U;
            goto __Vlabel1;
        }
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT____VlemCall_0__hz_conflict = 0U;
        __Vlabel1: ;
    }
    if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__valid_r) 
          >> 1U) & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT____VlemCall_0__hz_conflict))) {
        milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__conflict_any_w = 1U;
    }
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__b_key 
        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__key_r[2U];
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__b_cls 
        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__cls_r[2U];
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__a_key 
        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__sb_adm_key_w;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__a_cls 
        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__sb_adm_class_w;
    {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT____VlemCall_0__hz_conflict = 0;
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__same_key_v = 0;
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__other_v = 0;
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__same_key_v 
            = ((IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__a_key) 
               == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__b_key));
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__other_v 
            = ((6U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__a_cls))
                ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__b_cls)
                : (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__a_cls));
        if (((1U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__a_cls)) 
             | (1U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__b_cls)))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT____VlemCall_0__hz_conflict = 1U;
            goto __Vlabel2;
        }
        if (((0U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__a_cls)) 
             & (0U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__b_cls)))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT____VlemCall_0__hz_conflict = 0U;
            goto __Vlabel2;
        }
        if (((0U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__a_cls)) 
             | (0U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__b_cls)))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT____VlemCall_0__hz_conflict 
                = vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__same_key_v;
            goto __Vlabel2;
        }
        if (((6U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__a_cls)) 
             | (6U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__b_cls)))) {
            vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_is_lockprot__133__c 
                = vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__other_v;
            vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_is_lockprot__133__Vfuncout = 0;
            vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_is_lockprot__133__Vfuncout 
                = ((((((1U == (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_is_lockprot__133__c)) 
                       | (2U == (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_is_lockprot__133__c))) 
                      | (3U == (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_is_lockprot__133__c))) 
                     | (4U == (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_is_lockprot__133__c))) 
                    | (5U == (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_is_lockprot__133__c))) 
                   | (8U == (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_is_lockprot__133__c)));
            vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132____VlefCall_0__hz_is_lockprot 
                = vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_is_lockprot__133__Vfuncout;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT____VlemCall_0__hz_conflict 
                = ((6U == (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__other_v)) 
                   | (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132____VlefCall_0__hz_is_lockprot));
            goto __Vlabel2;
        }
        if (((IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__a_cls) 
             == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__b_cls))) {
            if (((7U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__a_cls)) 
                 | (8U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__a_cls)))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT____VlemCall_0__hz_conflict = 1U;
                goto __Vlabel2;
            }
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT____VlemCall_0__hz_conflict 
                = vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__same_key_v;
            goto __Vlabel2;
        }
        if ((((2U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__a_cls)) 
              & (3U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__b_cls))) 
             | ((3U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__a_cls)) 
                & (2U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__b_cls))))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT____VlemCall_0__hz_conflict = 1U;
            goto __Vlabel2;
        }
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT____VlemCall_0__hz_conflict = 0U;
        __Vlabel2: ;
    }
    if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__valid_r) 
          >> 2U) & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT____VlemCall_0__hz_conflict))) {
        milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__conflict_any_w = 1U;
    }
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__b_key 
        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__key_r[3U];
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__b_cls 
        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__cls_r[3U];
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__a_key 
        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__sb_adm_key_w;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__a_cls 
        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__sb_adm_class_w;
    {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT____VlemCall_0__hz_conflict = 0;
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__same_key_v = 0;
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__other_v = 0;
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__same_key_v 
            = ((IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__a_key) 
               == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__b_key));
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__other_v 
            = ((6U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__a_cls))
                ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__b_cls)
                : (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__a_cls));
        if (((1U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__a_cls)) 
             | (1U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__b_cls)))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT____VlemCall_0__hz_conflict = 1U;
            goto __Vlabel3;
        }
        if (((0U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__a_cls)) 
             & (0U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__b_cls)))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT____VlemCall_0__hz_conflict = 0U;
            goto __Vlabel3;
        }
        if (((0U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__a_cls)) 
             | (0U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__b_cls)))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT____VlemCall_0__hz_conflict 
                = vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__same_key_v;
            goto __Vlabel3;
        }
        if (((6U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__a_cls)) 
             | (6U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__b_cls)))) {
            vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_is_lockprot__133__c 
                = vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__other_v;
            vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_is_lockprot__133__Vfuncout = 0;
            vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_is_lockprot__133__Vfuncout 
                = ((((((1U == (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_is_lockprot__133__c)) 
                       | (2U == (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_is_lockprot__133__c))) 
                      | (3U == (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_is_lockprot__133__c))) 
                     | (4U == (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_is_lockprot__133__c))) 
                    | (5U == (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_is_lockprot__133__c))) 
                   | (8U == (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_is_lockprot__133__c)));
            vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132____VlefCall_0__hz_is_lockprot 
                = vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_is_lockprot__133__Vfuncout;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT____VlemCall_0__hz_conflict 
                = ((6U == (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__other_v)) 
                   | (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132____VlefCall_0__hz_is_lockprot));
            goto __Vlabel3;
        }
        if (((IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__a_cls) 
             == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__b_cls))) {
            if (((7U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__a_cls)) 
                 | (8U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__a_cls)))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT____VlemCall_0__hz_conflict = 1U;
                goto __Vlabel3;
            }
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT____VlemCall_0__hz_conflict 
                = vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__same_key_v;
            goto __Vlabel3;
        }
        if ((((2U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__a_cls)) 
              & (3U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__b_cls))) 
             | ((3U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__a_cls)) 
                & (2U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__b_cls))))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT____VlemCall_0__hz_conflict = 1U;
            goto __Vlabel3;
        }
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT____VlemCall_0__hz_conflict = 0U;
        __Vlabel3: ;
    }
    if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__valid_r) 
          >> 3U) & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT____VlemCall_0__hz_conflict))) {
        milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__conflict_any_w = 1U;
    }
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__b_key 
        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__key_r[4U];
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__b_cls 
        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__cls_r[4U];
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__a_key 
        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__sb_adm_key_w;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__a_cls 
        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__sb_adm_class_w;
    {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT____VlemCall_0__hz_conflict = 0;
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__same_key_v = 0;
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__other_v = 0;
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__same_key_v 
            = ((IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__a_key) 
               == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__b_key));
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__other_v 
            = ((6U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__a_cls))
                ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__b_cls)
                : (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__a_cls));
        if (((1U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__a_cls)) 
             | (1U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__b_cls)))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT____VlemCall_0__hz_conflict = 1U;
            goto __Vlabel4;
        }
        if (((0U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__a_cls)) 
             & (0U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__b_cls)))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT____VlemCall_0__hz_conflict = 0U;
            goto __Vlabel4;
        }
        if (((0U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__a_cls)) 
             | (0U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__b_cls)))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT____VlemCall_0__hz_conflict 
                = vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__same_key_v;
            goto __Vlabel4;
        }
        if (((6U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__a_cls)) 
             | (6U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__b_cls)))) {
            vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_is_lockprot__133__c 
                = vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__other_v;
            vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_is_lockprot__133__Vfuncout = 0;
            vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_is_lockprot__133__Vfuncout 
                = ((((((1U == (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_is_lockprot__133__c)) 
                       | (2U == (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_is_lockprot__133__c))) 
                      | (3U == (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_is_lockprot__133__c))) 
                     | (4U == (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_is_lockprot__133__c))) 
                    | (5U == (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_is_lockprot__133__c))) 
                   | (8U == (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_is_lockprot__133__c)));
            vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132____VlefCall_0__hz_is_lockprot 
                = vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_is_lockprot__133__Vfuncout;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT____VlemCall_0__hz_conflict 
                = ((6U == (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__other_v)) 
                   | (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132____VlefCall_0__hz_is_lockprot));
            goto __Vlabel4;
        }
        if (((IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__a_cls) 
             == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__b_cls))) {
            if (((7U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__a_cls)) 
                 | (8U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__a_cls)))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT____VlemCall_0__hz_conflict = 1U;
                goto __Vlabel4;
            }
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT____VlemCall_0__hz_conflict 
                = vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__same_key_v;
            goto __Vlabel4;
        }
        if ((((2U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__a_cls)) 
              & (3U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__b_cls))) 
             | ((3U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__a_cls)) 
                & (2U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__b_cls))))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT____VlemCall_0__hz_conflict = 1U;
            goto __Vlabel4;
        }
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT____VlemCall_0__hz_conflict = 0U;
        __Vlabel4: ;
    }
    if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__valid_r) 
          >> 4U) & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT____VlemCall_0__hz_conflict))) {
        milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__conflict_any_w = 1U;
    }
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__b_key 
        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__key_r[5U];
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__b_cls 
        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__cls_r[5U];
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__a_key 
        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__sb_adm_key_w;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__a_cls 
        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__sb_adm_class_w;
    {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT____VlemCall_0__hz_conflict = 0;
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__same_key_v = 0;
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__other_v = 0;
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__same_key_v 
            = ((IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__a_key) 
               == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__b_key));
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__other_v 
            = ((6U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__a_cls))
                ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__b_cls)
                : (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__a_cls));
        if (((1U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__a_cls)) 
             | (1U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__b_cls)))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT____VlemCall_0__hz_conflict = 1U;
            goto __Vlabel5;
        }
        if (((0U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__a_cls)) 
             & (0U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__b_cls)))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT____VlemCall_0__hz_conflict = 0U;
            goto __Vlabel5;
        }
        if (((0U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__a_cls)) 
             | (0U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__b_cls)))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT____VlemCall_0__hz_conflict 
                = vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__same_key_v;
            goto __Vlabel5;
        }
        if (((6U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__a_cls)) 
             | (6U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__b_cls)))) {
            vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_is_lockprot__133__c 
                = vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__other_v;
            vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_is_lockprot__133__Vfuncout = 0;
            vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_is_lockprot__133__Vfuncout 
                = ((((((1U == (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_is_lockprot__133__c)) 
                       | (2U == (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_is_lockprot__133__c))) 
                      | (3U == (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_is_lockprot__133__c))) 
                     | (4U == (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_is_lockprot__133__c))) 
                    | (5U == (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_is_lockprot__133__c))) 
                   | (8U == (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_is_lockprot__133__c)));
            vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132____VlefCall_0__hz_is_lockprot 
                = vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_is_lockprot__133__Vfuncout;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT____VlemCall_0__hz_conflict 
                = ((6U == (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__other_v)) 
                   | (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132____VlefCall_0__hz_is_lockprot));
            goto __Vlabel5;
        }
        if (((IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__a_cls) 
             == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__b_cls))) {
            if (((7U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__a_cls)) 
                 | (8U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__a_cls)))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT____VlemCall_0__hz_conflict = 1U;
                goto __Vlabel5;
            }
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT____VlemCall_0__hz_conflict 
                = vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__same_key_v;
            goto __Vlabel5;
        }
        if ((((2U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__a_cls)) 
              & (3U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__b_cls))) 
             | ((3U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__a_cls)) 
                & (2U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__b_cls))))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT____VlemCall_0__hz_conflict = 1U;
            goto __Vlabel5;
        }
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT____VlemCall_0__hz_conflict = 0U;
        __Vlabel5: ;
    }
    if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__valid_r) 
          >> 5U) & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT____VlemCall_0__hz_conflict))) {
        milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__conflict_any_w = 1U;
    }
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__b_key 
        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__key_r[6U];
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__b_cls 
        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__cls_r[6U];
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__a_key 
        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__sb_adm_key_w;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__a_cls 
        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__sb_adm_class_w;
    {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT____VlemCall_0__hz_conflict = 0;
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__same_key_v = 0;
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__other_v = 0;
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__same_key_v 
            = ((IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__a_key) 
               == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__b_key));
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__other_v 
            = ((6U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__a_cls))
                ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__b_cls)
                : (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__a_cls));
        if (((1U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__a_cls)) 
             | (1U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__b_cls)))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT____VlemCall_0__hz_conflict = 1U;
            goto __Vlabel6;
        }
        if (((0U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__a_cls)) 
             & (0U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__b_cls)))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT____VlemCall_0__hz_conflict = 0U;
            goto __Vlabel6;
        }
        if (((0U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__a_cls)) 
             | (0U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__b_cls)))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT____VlemCall_0__hz_conflict 
                = vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__same_key_v;
            goto __Vlabel6;
        }
        if (((6U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__a_cls)) 
             | (6U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__b_cls)))) {
            vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_is_lockprot__133__c 
                = vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__other_v;
            vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_is_lockprot__133__Vfuncout = 0;
            vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_is_lockprot__133__Vfuncout 
                = ((((((1U == (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_is_lockprot__133__c)) 
                       | (2U == (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_is_lockprot__133__c))) 
                      | (3U == (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_is_lockprot__133__c))) 
                     | (4U == (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_is_lockprot__133__c))) 
                    | (5U == (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_is_lockprot__133__c))) 
                   | (8U == (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_is_lockprot__133__c)));
            vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132____VlefCall_0__hz_is_lockprot 
                = vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_is_lockprot__133__Vfuncout;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT____VlemCall_0__hz_conflict 
                = ((6U == (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__other_v)) 
                   | (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132____VlefCall_0__hz_is_lockprot));
            goto __Vlabel6;
        }
        if (((IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__a_cls) 
             == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__b_cls))) {
            if (((7U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__a_cls)) 
                 | (8U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__a_cls)))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT____VlemCall_0__hz_conflict = 1U;
                goto __Vlabel6;
            }
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT____VlemCall_0__hz_conflict 
                = vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__same_key_v;
            goto __Vlabel6;
        }
        if ((((2U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__a_cls)) 
              & (3U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__b_cls))) 
             | ((3U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__a_cls)) 
                & (2U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__b_cls))))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT____VlemCall_0__hz_conflict = 1U;
            goto __Vlabel6;
        }
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT____VlemCall_0__hz_conflict = 0U;
        __Vlabel6: ;
    }
    if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__valid_r) 
          >> 6U) & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT____VlemCall_0__hz_conflict))) {
        milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__conflict_any_w = 1U;
    }
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__b_key 
        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__key_r[7U];
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__b_cls 
        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__cls_r[7U];
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__a_key 
        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__sb_adm_key_w;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__a_cls 
        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__sb_adm_class_w;
    {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT____VlemCall_0__hz_conflict = 0;
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__same_key_v = 0;
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__other_v = 0;
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__same_key_v 
            = ((IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__a_key) 
               == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__b_key));
        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__other_v 
            = ((6U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__a_cls))
                ? (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__b_cls)
                : (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__a_cls));
        if (((1U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__a_cls)) 
             | (1U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__b_cls)))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT____VlemCall_0__hz_conflict = 1U;
            goto __Vlabel7;
        }
        if (((0U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__a_cls)) 
             & (0U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__b_cls)))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT____VlemCall_0__hz_conflict = 0U;
            goto __Vlabel7;
        }
        if (((0U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__a_cls)) 
             | (0U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__b_cls)))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT____VlemCall_0__hz_conflict 
                = vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__same_key_v;
            goto __Vlabel7;
        }
        if (((6U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__a_cls)) 
             | (6U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__b_cls)))) {
            vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_is_lockprot__133__c 
                = vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__other_v;
            vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_is_lockprot__133__Vfuncout = 0;
            vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_is_lockprot__133__Vfuncout 
                = ((((((1U == (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_is_lockprot__133__c)) 
                       | (2U == (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_is_lockprot__133__c))) 
                      | (3U == (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_is_lockprot__133__c))) 
                     | (4U == (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_is_lockprot__133__c))) 
                    | (5U == (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_is_lockprot__133__c))) 
                   | (8U == (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_is_lockprot__133__c)));
            vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132____VlefCall_0__hz_is_lockprot 
                = vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_is_lockprot__133__Vfuncout;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT____VlemCall_0__hz_conflict 
                = ((6U == (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__other_v)) 
                   | (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132____VlefCall_0__hz_is_lockprot));
            goto __Vlabel7;
        }
        if (((IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__a_cls) 
             == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__b_cls))) {
            if (((7U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__a_cls)) 
                 | (8U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__a_cls)))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT____VlemCall_0__hz_conflict = 1U;
                goto __Vlabel7;
            }
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT____VlemCall_0__hz_conflict 
                = vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__same_key_v;
            goto __Vlabel7;
        }
        if ((((2U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__a_cls)) 
              & (3U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__b_cls))) 
             | ((3U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__a_cls)) 
                & (2U == (IData)(__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__b_cls))))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT____VlemCall_0__hz_conflict = 1U;
            goto __Vlabel7;
        }
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT____VlemCall_0__hz_conflict = 0U;
        __Vlabel7: ;
    }
    if ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__valid_r) 
          >> 7U) & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT____VlemCall_0__hz_conflict))) {
        milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__conflict_any_w = 1U;
    }
    if (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__byp_v_r) 
         & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__byp_sink_r) 
            == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__c1_sink_r)))) {
        __Vtemp_18[0U] = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__byp_data_r[0U];
        __Vtemp_18[1U] = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__byp_data_r[1U];
        __Vtemp_18[2U] = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__byp_data_r[2U];
        __Vtemp_18[3U] = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__byp_data_r[3U];
        __Vtemp_18[4U] = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__byp_data_r[4U];
    } else {
        __Vtemp_18[0U] = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__shw_rdata_r[0U];
        __Vtemp_18[1U] = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__shw_rdata_r[1U];
        __Vtemp_18[2U] = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__shw_rdata_r[2U];
        __Vtemp_18[3U] = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__shw_rdata_r[3U];
        __Vtemp_18[4U] = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__shw_rdata_r[4U];
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__c1_wr_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__c1_v_r) 
           & ((0U != (((((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__c1_proj_r[0U] 
                          ^ __Vtemp_18[0U]) | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__c1_proj_r[1U] 
                                               ^ __Vtemp_18[1U])) 
                        | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__c1_proj_r[2U] 
                           ^ __Vtemp_18[2U])) | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__c1_proj_r[3U] 
                                                 ^ __Vtemp_18[3U])) 
                      | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__c1_proj_r[4U] 
                         ^ __Vtemp_18[4U]))) | ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__c1_vld_r) 
                                                != 
                                                (1U 
                                                 & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__valid_r) 
                                                    >> (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__c1_sink_r))))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__ser_start_w 
        = ((~ ((0U == vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__len_r
                [vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__slot_r]) 
               | (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_69))) 
           & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_259));
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
              & ((~ (IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__conflict_any_w)) 
                 & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__barrier_pend_r)) 
                    | (1U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__sb_adm_class_w))))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__fsm_wr_gnt_w 
        = ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__c1_wr_w)) 
           & (IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__fsm_wr_req_w));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__wr_en_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__c1_wr_w) 
           | (IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__fsm_wr_req_w));
    if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__c1_wr_w) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__wr_addr_w 
            = (1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__c1_sink_r));
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
            = (1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__init_cnt_r));
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__wr_data_w[0U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__wr_data_w[1U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__wr_data_w[2U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__wr_data_w[3U] = 0U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__wr_data_w[4U] = 0U;
    } else {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__wr_addr_w 
            = (1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__rs_k_r));
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
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__aecp_sb_grant_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__sb_pick_aecp_w) 
           & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__sb_gnt_w));
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__acmp_sb_grant_w 
        = ((IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__sb_pick_acmp_w) 
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
    __VdfgRegularize_h6e95ff9d_0_247 = ((2U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pf_st_r)) 
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
           & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_204));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__acmp_txn_ready_w 
        = ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_84) 
           & (IData)(__VdfgRegularize_h6e95ff9d_0_247));
    __VdfgRegularize_h6e95ff9d_0_246 = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_acmp_q__DOT__out_valid_r) 
                                        & (IData)(__VdfgRegularize_h6e95ff9d_0_247));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_acmp_q__DOT__rd_en_w 
        = ((0U != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_acmp_q__DOT__cnt_r)) 
           & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_acmp_q__DOT__out_valid_r)) 
              | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__acmp_txn_ready_w)));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT____Vcellinp__u_listener__txn_valid_i 
        = ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__acmp_is_tkr_w)) 
           & (IData)(__VdfgRegularize_h6e95ff9d_0_246));
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT____Vcellinp__u_talker__txn_valid_i 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__acmp_is_tkr_w) 
           & (IData)(__VdfgRegularize_h6e95ff9d_0_246));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_198 = ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT____Vcellinp__u_listener__txn_valid_i)) 
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
                    vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__76__v 
                        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__pe_off_r;
                    vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__76__Vfuncout = 0U;
                    if ((2U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__76__v))) {
                        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__76__Vfuncout = 1U;
                    }
                    if ((1U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__76__v))) {
                        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__76__Vfuncout = 0U;
                    }
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__disp_src_w 
                        = vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__76__Vfuncout;
                } else if ((0U != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__pe_conflict_r))) {
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__disp_code_w = 2U;
                    vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__77__v 
                        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__pe_conflict_r;
                    vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__77__Vfuncout = 0U;
                    if ((2U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__77__v))) {
                        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__77__Vfuncout = 1U;
                    }
                    if ((1U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__77__v))) {
                        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__77__Vfuncout = 0U;
                    }
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__disp_src_w 
                        = vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__77__Vfuncout;
                } else if ((0U != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__pe_pcp_r))) {
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__disp_code_w = 3U;
                    vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__78__v 
                        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__pe_pcp_r;
                    vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__78__Vfuncout = 0U;
                    if ((2U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__78__v))) {
                        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__78__Vfuncout = 1U;
                    }
                    if ((1U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__78__v))) {
                        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__78__Vfuncout = 0U;
                    }
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__disp_src_w 
                        = vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__78__Vfuncout;
                } else if ((0U != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__pe_tmr_r))) {
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__disp_code_w = 4U;
                    vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__79__v 
                        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__pe_tmr_r;
                    vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__79__Vfuncout = 0U;
                    if ((2U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__79__v))) {
                        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__79__Vfuncout = 1U;
                    }
                    if ((1U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__79__v))) {
                        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__79__Vfuncout = 0U;
                    }
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__disp_src_w 
                        = vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__79__Vfuncout;
                } else if ((0U != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__pe_lsn_r))) {
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__disp_code_w = 5U;
                    vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__80__v 
                        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__pe_lsn_r;
                    vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__80__Vfuncout = 0U;
                    if ((2U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__80__v))) {
                        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__80__Vfuncout = 1U;
                    }
                    if ((1U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__80__v))) {
                        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__80__Vfuncout = 0U;
                    }
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__disp_src_w 
                        = vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__80__Vfuncout;
                } else if ((0U != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__pe_rel_r))) {
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__disp_code_w = 7U;
                    vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__81__v 
                        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__pe_rel_r;
                    vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__81__Vfuncout = 0U;
                    if ((2U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__81__v))) {
                        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__81__Vfuncout = 1U;
                    }
                    if ((1U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__81__v))) {
                        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__81__Vfuncout = 0U;
                    }
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__disp_src_w 
                        = vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__81__Vfuncout;
                } else if ((0U != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__pe_init_r))) {
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__disp_code_w = 6U;
                    vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__82__v 
                        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__pe_init_r;
                    vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__82__Vfuncout = 0U;
                    if ((2U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__82__v))) {
                        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__82__Vfuncout = 1U;
                    }
                    if ((1U & (IData)(vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__82__v))) {
                        vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__82__Vfuncout = 0U;
                    }
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__disp_src_w 
                        = vlSelfRef.__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__82__Vfuncout;
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
           & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_198));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__rec_re_w = 0U;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__clr_disp_w = 0U;
    if (((1U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__state_r)) 
         & (2U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__disp_kind_w)))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__clr_disp_w 
            = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__clr_disp_w) 
               | (3U & ((IData)(1U) << (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__disp_src_w))));
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__rec_raddr_w = 0U;
    if ((0U != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__state_r))) {
        if ((1U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__state_r))) {
            if ((1U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__disp_kind_w))) {
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__rec_re_w = 1U;
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__rec_raddr_w 
                    = (1U & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__txn_in_w[1U] 
                             >> 0x0000001cU));
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
        if ((0x0aU >= (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__sel_r))) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__delivered_w 
                = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__delivered_w) 
                   | (0x07ffU & ((IData)(1U) << (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__sel_r))));
            milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pend_after_w 
                = ((~ ((IData)(1U) << (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__sel_r))) 
                   & (IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pend_after_w));
        }
        milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__base_w 
            = (0x0000000fU & (((IData)(1U) + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__sel_r)) 
                              & (- (IData)((0x0aU != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__sel_r))))));
    } else {
        milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__base_w 
            = (0x0000000fU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__ptr_r));
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__gnt_found_w = 0U;
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__gnt_src_w = 0U;
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx 
        = milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__base_w;
    if ((0x0000000bU <= milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx)) {
        milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx 
            = (milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx 
               - (IData)(0x0000000bU));
    }
    if (((0x0aU >= (0x0000000fU & milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx)) 
         && (1U & ((IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pend_after_w) 
                   >> (0x0000000fU & milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx))))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__gnt_found_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__gnt_src_w 
            = (0x0000000fU & milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx);
    }
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx 
        = ((IData)(1U) + (IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__base_w));
    if ((0x0000000bU <= milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx)) {
        milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx 
            = (milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx 
               - (IData)(0x0000000bU));
    }
    if (((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__gnt_found_w)) 
         & ((0x0aU >= (0x0000000fU & milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx)) 
            && (1U & ((IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pend_after_w) 
                      >> (0x0000000fU & milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx)))))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__gnt_found_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__gnt_src_w 
            = (0x0000000fU & milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx);
    }
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx 
        = ((IData)(2U) + (IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__base_w));
    if ((0x0000000bU <= milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx)) {
        milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx 
            = (milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx 
               - (IData)(0x0000000bU));
    }
    if (((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__gnt_found_w)) 
         & ((0x0aU >= (0x0000000fU & milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx)) 
            && (1U & ((IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pend_after_w) 
                      >> (0x0000000fU & milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx)))))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__gnt_found_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__gnt_src_w 
            = (0x0000000fU & milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx);
    }
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx 
        = ((IData)(3U) + (IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__base_w));
    if ((0x0000000bU <= milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx)) {
        milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx 
            = (milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx 
               - (IData)(0x0000000bU));
    }
    if (((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__gnt_found_w)) 
         & ((0x0aU >= (0x0000000fU & milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx)) 
            && (1U & ((IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pend_after_w) 
                      >> (0x0000000fU & milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx)))))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__gnt_found_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__gnt_src_w 
            = (0x0000000fU & milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx);
    }
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx 
        = ((IData)(4U) + (IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__base_w));
    if ((0x0000000bU <= milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx)) {
        milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx 
            = (milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx 
               - (IData)(0x0000000bU));
    }
    if (((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__gnt_found_w)) 
         & ((0x0aU >= (0x0000000fU & milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx)) 
            && (1U & ((IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pend_after_w) 
                      >> (0x0000000fU & milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx)))))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__gnt_found_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__gnt_src_w 
            = (0x0000000fU & milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx);
    }
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx 
        = ((IData)(5U) + (IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__base_w));
    if ((0x0000000bU <= milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx)) {
        milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx 
            = (milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx 
               - (IData)(0x0000000bU));
    }
    if (((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__gnt_found_w)) 
         & ((0x0aU >= (0x0000000fU & milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx)) 
            && (1U & ((IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pend_after_w) 
                      >> (0x0000000fU & milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx)))))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__gnt_found_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__gnt_src_w 
            = (0x0000000fU & milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx);
    }
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx 
        = ((IData)(6U) + (IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__base_w));
    if ((0x0000000bU <= milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx)) {
        milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx 
            = (milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx 
               - (IData)(0x0000000bU));
    }
    if (((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__gnt_found_w)) 
         & ((0x0aU >= (0x0000000fU & milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx)) 
            && (1U & ((IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pend_after_w) 
                      >> (0x0000000fU & milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx)))))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__gnt_found_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__gnt_src_w 
            = (0x0000000fU & milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx);
    }
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx 
        = ((IData)(7U) + (IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__base_w));
    if ((0x0000000bU <= milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx)) {
        milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx 
            = (milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx 
               - (IData)(0x0000000bU));
    }
    if (((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__gnt_found_w)) 
         & ((0x0aU >= (0x0000000fU & milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx)) 
            && (1U & ((IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pend_after_w) 
                      >> (0x0000000fU & milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx)))))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__gnt_found_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__gnt_src_w 
            = (0x0000000fU & milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx);
    }
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx 
        = ((IData)(8U) + (IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__base_w));
    if ((0x0000000bU <= milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx)) {
        milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx 
            = (milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx 
               - (IData)(0x0000000bU));
    }
    if (((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__gnt_found_w)) 
         & ((0x0aU >= (0x0000000fU & milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx)) 
            && (1U & ((IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pend_after_w) 
                      >> (0x0000000fU & milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx)))))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__gnt_found_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__gnt_src_w 
            = (0x0000000fU & milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx);
    }
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx 
        = ((IData)(9U) + (IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__base_w));
    if ((0x0000000bU <= milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx)) {
        milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx 
            = (milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx 
               - (IData)(0x0000000bU));
    }
    if (((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__gnt_found_w)) 
         & ((0x0aU >= (0x0000000fU & milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx)) 
            && (1U & ((IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pend_after_w) 
                      >> (0x0000000fU & milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx)))))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__gnt_found_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__gnt_src_w 
            = (0x0000000fU & milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx);
    }
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx 
        = ((IData)(0x0000000aU) + (IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__base_w));
    if ((0x0000000bU <= milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx)) {
        milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx 
            = (milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx 
               - (IData)(0x0000000bU));
    }
    if (((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__gnt_found_w)) 
         & ((0x0aU >= (0x0000000fU & milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx)) 
            && (1U & ((IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pend_after_w) 
                      >> (0x0000000fU & milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx)))))) {
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__gnt_found_w = 1U;
        vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__gnt_src_w 
            = (0x0000000fU & milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__rr_scan__DOT__unnamedblk1__DOT__unnamedblk2__DOT__idx);
    }
}
