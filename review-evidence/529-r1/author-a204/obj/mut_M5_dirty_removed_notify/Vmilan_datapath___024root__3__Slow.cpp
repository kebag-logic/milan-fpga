// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vmilan_datapath.h for the primary calling header

#include "Vmilan_datapath__pch.h"

extern const VlUnpacked<CData/*0:0*/, 32> Vmilan_datapath__ConstPool__TABLE_h5f1389fb_0;
extern const VlUnpacked<CData/*2:0*/, 32> Vmilan_datapath__ConstPool__TABLE_h6dff1152_0;

VL_ATTR_COLD void Vmilan_datapath___024root___stl_sequent__TOP__3(Vmilan_datapath___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vmilan_datapath___024root___stl_sequent__TOP__3\n"); );
    Vmilan_datapath__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    CData/*0:0*/ milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__acmp_sb_grant_w;
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__acmp_sb_grant_w = 0;
    CData/*0:0*/ milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__aecp_sb_grant_w;
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__aecp_sb_grant_w = 0;
    CData/*7:0*/ milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__org_withdraw_slot_mask_w;
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__org_withdraw_slot_mask_w = 0;
    CData/*0:0*/ milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT____Vcellinp__u_talker__txn_valid_i;
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT____Vcellinp__u_talker__txn_valid_i = 0;
    CData/*0:0*/ milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__sb_pick_acmp_w;
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__sb_pick_acmp_w = 0;
    CData/*0:0*/ milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pool_wr_commit_w;
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pool_wr_commit_w = 0;
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
    CData/*0:0*/ milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__conflict_any_w;
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__conflict_any_w = 0;
    CData/*0:0*/ milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__drop_w;
    milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__drop_w = 0;
    CData/*0:0*/ milan_datapath__DOT__render_setpoint__DOT__adv0_w;
    milan_datapath__DOT__render_setpoint__DOT__adv0_w = 0;
    CData/*0:0*/ milan_datapath__DOT__render_setpoint__DOT__st0_w;
    milan_datapath__DOT__render_setpoint__DOT__st0_w = 0;
    CData/*0:0*/ milan_datapath__DOT__render_setpoint__DOT__pend_in_w;
    milan_datapath__DOT__render_setpoint__DOT__pend_in_w = 0;
    CData/*0:0*/ milan_datapath__DOT__render_setpoint__DOT__prefill_in_w;
    milan_datapath__DOT__render_setpoint__DOT__prefill_in_w = 0;
    CData/*3:0*/ __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__a_cls;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__a_cls = 0;
    SData/*15:0*/ __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__a_key;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__a_key = 0;
    CData/*3:0*/ __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__b_cls;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__b_cls = 0;
    SData/*15:0*/ __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__b_key;
    __Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__b_key = 0;
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
    CData/*6:0*/ __VdfgRegularize_h6e95ff9d_0_274;
    __VdfgRegularize_h6e95ff9d_0_274 = 0;
    CData/*0:0*/ __VdfgRegularize_h6e95ff9d_0_275;
    __VdfgRegularize_h6e95ff9d_0_275 = 0;
    CData/*5:0*/ __VdfgRegularize_h6e95ff9d_0_276;
    __VdfgRegularize_h6e95ff9d_0_276 = 0;
    CData/*0:0*/ __VdfgRegularize_h6e95ff9d_0_277;
    __VdfgRegularize_h6e95ff9d_0_277 = 0;
    CData/*4:0*/ __VdfgRegularize_h6e95ff9d_0_278;
    __VdfgRegularize_h6e95ff9d_0_278 = 0;
    CData/*0:0*/ __VdfgRegularize_h6e95ff9d_0_279;
    __VdfgRegularize_h6e95ff9d_0_279 = 0;
    CData/*0:0*/ __VdfgRegularize_h6e95ff9d_0_299;
    __VdfgRegularize_h6e95ff9d_0_299 = 0;
    // Body
    if (vlSelfRef.milan_datapath__DOT__csr__DOT__pp_rd_hit_w) {
        vlSelfRef.milan_datapath__DOT__csr__DOT__live_mux 
            = (((0x0920U == (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))
                 ? vlSelfRef.milan_datapath__DOT__csr__DOT__g_pp_csr__DOT__pp_ctrl_r
                 : ((0x0924U == (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))
                     ? (0x5b000000U | ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__verdict_r) 
                                         << 0x0000000cU) 
                                        | (((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__pend_w) 
                                              << 3U) 
                                             | ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__img_valid_r) 
                                                << 2U)) 
                                            | (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__stale_r) 
                                                << 1U) 
                                               | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__dirty_img_w))) 
                                           << 8U)) 
                                       | (((((((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__any_rec_r)) 
                                               & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__done_r)) 
                                              << 3U) 
                                             | ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__backed_r) 
                                                << 2U)) 
                                            | (((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__g_pp_csr__DOT__pp_err_r) 
                                                << 1U) 
                                               | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__alarm_r))) 
                                           << 4U) | 
                                          (((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__fail_r) 
                                              | ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__walk_blind_r) 
                                                 & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__done_r))) 
                                             << 3U) 
                                            | ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__done_r) 
                                               << 2U)) 
                                           | (((IData)(vlSelfRef.milan_datapath__DOT__pp_restore_busy_w) 
                                               << 1U) 
                                              | (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__g_pp_csr__DOT__pp_busy_r))))))
                     : ((0x0928U == (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))
                         ? vlSelfRef.milan_datapath__DOT__csr__DOT__g_pp_csr__DOT__pp_spaddr_r
                         : ((0x092cU == (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))
                             ? vlSelfRef.milan_datapath__DOT__csr__DOT__g_pp_csr__DOT__pp_sprdata_r
                             : ((0x0930U == (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))
                                 ? (((IData)(vlSelfRef.milan_datapath__DOT__pp_tx_frames_w) 
                                     << 0x00000010U) 
                                    | (((IData)(vlSelfRef.milan_datapath__DOT__pp_rx_drops_w) 
                                        << 8U) | (0x000000ffU 
                                                  & (IData)(vlSelfRef.milan_datapath__DOT__pp_rx_frames_w))))
                                 : ((0x0934U == (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__rd_addr_q))
                                     ? (IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__g_pp_csr__DOT__pp_nvm_sel_r)
                                     : ((0x00000020U 
                                         & (IData)(vlSelfRef.milan_datapath__DOT__pp_nvm_csr_addr_w))
                                         ? ((0x00000010U 
                                             & (IData)(vlSelfRef.milan_datapath__DOT__pp_nvm_csr_addr_w))
                                             ? (((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__mapo_len_r
                                                  [
                                                  (1U 
                                                   & (IData)(vlSelfRef.milan_datapath__DOT__pp_nvm_csr_addr_w))] 
                                                  & (- (IData)(
                                                               (0U 
                                                                >= 
                                                                (1U 
                                                                 & (IData)(vlSelfRef.milan_datapath__DOT__pp_nvm_csr_addr_w)))))) 
                                                 << 0x00000010U) 
                                                | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__mapo_pref_r
                                                   [
                                                   (1U 
                                                    & (IData)(vlSelfRef.milan_datapath__DOT__pp_nvm_csr_addr_w))] 
                                                   & (- (IData)(
                                                                (0U 
                                                                 >= 
                                                                 (1U 
                                                                  & (IData)(vlSelfRef.milan_datapath__DOT__pp_nvm_csr_addr_w)))))))
                                             : (((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__mapi_len_r
                                                  [
                                                  (1U 
                                                   & (IData)(vlSelfRef.milan_datapath__DOT__pp_nvm_csr_addr_w))] 
                                                  & (- (IData)(
                                                               (0U 
                                                                >= 
                                                                (1U 
                                                                 & (IData)(vlSelfRef.milan_datapath__DOT__pp_nvm_csr_addr_w)))))) 
                                                 << 0x00000010U) 
                                                | (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__mapi_pref_r
                                                   [
                                                   (1U 
                                                    & (IData)(vlSelfRef.milan_datapath__DOT__pp_nvm_csr_addr_w))] 
                                                   & (- (IData)(
                                                                (0U 
                                                                 >= 
                                                                 (1U 
                                                                  & (IData)(vlSelfRef.milan_datapath__DOT__pp_nvm_csr_addr_w))))))))
                                         : ((1U == 
                                             (3U & 
                                              ((IData)(vlSelfRef.milan_datapath__DOT__pp_nvm_csr_addr_w) 
                                               >> 3U)))
                                             ? vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__open_r
                                            [(7U & (IData)(vlSelfRef.milan_datapath__DOT__pp_nvm_csr_addr_w))]
                                             : ((- (IData)(
                                                           (1U 
                                                            & (~ 
                                                               ((IData)(vlSelfRef.milan_datapath__DOT__pp_nvm_csr_addr_w) 
                                                                >> 3U))))) 
                                                & (((4U 
                                                     & (IData)(vlSelfRef.milan_datapath__DOT__pp_nvm_csr_addr_w))
                                                     ? 
                                                    ((- (IData)((IData)(
                                                                        (1U 
                                                                         == 
                                                                         (3U 
                                                                          & (IData)(vlSelfRef.milan_datapath__DOT__pp_nvm_csr_addr_w)))))) 
                                                     & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__cap_id_r))
                                                     : 
                                                    ((2U 
                                                      & (IData)(vlSelfRef.milan_datapath__DOT__pp_nvm_csr_addr_w))
                                                      ? 
                                                     ((1U 
                                                       & (IData)(vlSelfRef.milan_datapath__DOT__pp_nvm_csr_addr_w))
                                                       ? 
                                                      (0xc3000000U 
                                                       | (((((((0U 
                                                                != 
                                                                (((((((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__open_r[0U] 
                                                                       | vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__open_r[1U]) 
                                                                      | vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__open_r[2U]) 
                                                                     | vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__open_r[3U]) 
                                                                    | vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__open_r[4U]) 
                                                                   | vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__open_r[5U]) 
                                                                  | vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__open_r[6U]) 
                                                                 | vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__open_r[7U])) 
                                                               << 3U) 
                                                              | ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__pend_w) 
                                                                 << 2U)) 
                                                             | (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__arm_ref_r) 
                                                                 << 1U) 
                                                                | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__ack_ref_r))) 
                                                            << 0x00000014U) 
                                                           | (((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__cap_att_r) 
                                                                 << 3U) 
                                                                | ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__cap_valid_r) 
                                                                   << 2U)) 
                                                               | (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__cap_hold_r) 
                                                                   << 1U) 
                                                                  | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__cap_open_r))) 
                                                              << 0x00000010U)) 
                                                          | ((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__verdict_r) 
                                                               << 0x0000000cU) 
                                                              | (((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__rl_ref_r) 
                                                                    << 3U) 
                                                                   | ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__commit_busy_r) 
                                                                      << 2U)) 
                                                                  | (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__stale_r) 
                                                                      << 1U) 
                                                                     | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__dirty_img_w))) 
                                                                 << 8U)) 
                                                             | ((((((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__img_valid_r) 
                                                                    << 3U) 
                                                                   | ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__backed_r) 
                                                                      << 2U)) 
                                                                  | (((0U 
                                                                       != vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__img_len_r) 
                                                                      << 1U) 
                                                                     | (0U 
                                                                        != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__st_r)))) 
                                                                 << 4U) 
                                                                | (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__ld_pend_r) 
                                                                    << 3U) 
                                                                   | ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__ld_acc_r) 
                                                                      << 2U))))))
                                                       : vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__seq_r)
                                                      : 
                                                     ((1U 
                                                       & (IData)(vlSelfRef.milan_datapath__DOT__pp_nvm_csr_addr_w))
                                                       ? vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__img_len_r
                                                       : vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__img_base_r))) 
                                                   & (- (IData)(
                                                                (1U 
                                                                 & (~ 
                                                                    ((IData)(vlSelfRef.milan_datapath__DOT__pp_nvm_csr_addr_w) 
                                                                     >> 4U))))))))))))))) 
               & (- (IData)((IData)(vlSelfRef.milan_datapath__DOT__csr__DOT__pp_rd_hit_w))));
    }
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__sb_pick_acmp_w 
        = ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__sb_pick_aecp_w)) 
           & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__acmp_sb_candidate_w));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_269 = (7U 
                                                  & ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_cnt_r 
                                                      >> 9U) 
                                                     - 
                                                     (1U 
                                                      & (- (IData)((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_283))))));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_280 = (((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_283) 
                                                   << 3U) 
                                                  | (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_282));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__fail_now_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__ver_fail_w) 
           | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__sub_fail_w));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__fw_valid_w 
        = ((0U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__fw_S))
            ? (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__beat_w)
            : ((1U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__fw_S))
                ? (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__beat_w)
                : ((2U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__fw_S)) 
                   && (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__beat_w))));
    vlSelfRef.milan_datapath__DOT__ctl_ifg__DOT__beat_acc 
        = ((IData)(vlSelfRef.milan_datapath__DOT__ctlh_tx_tvalid) 
           & (IData)(vlSelfRef.milan_datapath__DOT__ctlh_tx_tready));
    vlSelfRef.milan_datapath__DOT__crf_dp_mux__DOT__beat_accepted 
        = ((IData)(vlSelfRef.milan_datapath__DOT__dpcrf_tvalid) 
           & (IData)(vlSelfRef.milan_datapath__DOT__dpcrf_tready));
    vlSelfRef.milan_datapath__DOT__aaf_tx_tready = 
        ((IData)(vlSelfRef.milan_datapath__DOT__crf_dp_mux__DOT__active) 
         & ((~ ((IData)(vlSelfRef.milan_datapath__DOT__crf_dp_mux__DOT__flush_r) 
                | (IData)(vlSelfRef.milan_datapath__DOT__crf_dp_mux__DOT__gsel))) 
            & (IData)(vlSelfRef.milan_datapath__DOT__dpcrf_tready)));
    vlSelfRef.m_axis_mac_tx_tvalid = ((IData)(vlSelfRef.milan_datapath__DOT__adp_tx_mux__DOT__flush_r) 
                                      | ((IData)(vlSelfRef.milan_datapath__DOT__adp_tx_mux__DOT__src_tvalid_w) 
                                         & (IData)(vlSelfRef.milan_datapath__DOT__adp_tx_mux__DOT__active)));
    vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__ovr0_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__drop0_w) 
           & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_301));
    milan_datapath__DOT__render_setpoint__DOT__st0_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__s_ok_w) 
           & ((~ (IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__drop0_w)) 
              & (8U > (IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__chpos_r))));
    milan_datapath__DOT__render_setpoint__DOT__adv0_w 
        = ((~ (IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__drop0_w)) 
           & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_301));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__resp_send_w 
        = (IData)(((0x0000e00000000000ULL == (0x0000f80000000000ULL 
                                              & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__uop_e_r)) 
                   & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__advance_e_w)));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__aecp_eff_notify_stb_nc_w 
        = (IData)(((0x0000b80000000000ULL == (0x0000f80000000000ULL 
                                              & vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__uop_e_r)) 
                   & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__advance_e_w)));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__reload_ok_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__reload_w) 
           & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__ld_pend_r) 
              & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__ld_ok_r)));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__ntfy_stri_out_w 
        = ((2U & ((0xfffffffeU & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_lstn_reg_change_w)) 
                  | (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_gate_src_w) 
                      & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_86)) 
                     << 1U))) | (1U & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_lstn_reg_change_w) 
                                       | ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_gate_src_w)) 
                                          & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_86)))));
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pool_wr_commit_w = 0U;
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
                    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pool_wr_commit_w 
                        = (3U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_st_r));
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pool_alloc_req_w 
                        = (1U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_st_r));
                } else {
                    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pool_wr_commit_w 
                        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__ca_txs_wr_commit_w;
                    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pool_alloc_req_w 
                        = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__ca_txs_alloc_req_w;
                }
            } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__txc_owner_r))) {
                milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pool_wr_commit_w 
                    = (7U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__w_st_r));
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pool_alloc_req_w 
                    = (4U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__w_st_r));
            } else {
                milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pool_wr_commit_w 
                    = (6U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__a_st_r));
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pool_alloc_req_w 
                    = (4U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__a_st_r));
            }
        } else if ((2U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__txc_owner_r))) {
            if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__txc_owner_r))) {
                milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pool_wr_commit_w 
                    = (3U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_st_r));
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pool_alloc_req_w 
                    = (1U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_st_r));
            } else {
                milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pool_wr_commit_w 
                    = (0x0eU == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__st_r));
                vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pool_alloc_req_w 
                    = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_txs_alloc_req_w;
            }
        } else if ((1U & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__txc_owner_r))) {
            milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pool_wr_commit_w 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__lstn_txs_wr_commit_w;
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pool_alloc_req_w 
                = vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__lstn_txs_alloc_req_w;
        } else {
            milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pool_wr_commit_w 
                = (5U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__bld_st_r));
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pool_alloc_req_w 
                = (2U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__bld_st_r));
        }
        if (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__txc_alloc_wait_r) {
            vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pool_alloc_req_w = 0U;
        }
    }
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__ev_cancel_w 
        = ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__ev_rsp_w)) 
           & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__cancel_pend_ok_w));
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
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_281 = ((0U 
                                                   != 
                                                   (7U 
                                                    & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_cnt_r 
                                                       >> 0x0000000cU))) 
                                                  & (0U 
                                                     == (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_280)));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__wr_en_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__pdu_byte_w) 
           & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__fail_now_w)) 
              & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__in_budget_w)));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_264 = ((1U 
                                                   == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__fr_st_r)) 
                                                  & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__fail_now_w)) 
                                                     & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__slot_now_w)));
    vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__aaf_tx_acc_w 
        = ((3U == (IData)(vlSelfRef.milan_datapath__DOT__aaf_packetizer__DOT__est_r)) 
           & (IData)(vlSelfRef.milan_datapath__DOT__aaf_tx_tready));
    vlSelfRef.milan_datapath__DOT__adp_tx_mux__DOT__beat_accepted 
        = ((IData)(vlSelfRef.m_axis_mac_tx_tready) 
           & (IData)(vlSelfRef.m_axis_mac_tx_tvalid));
    vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__h1_sel0_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__chpos_r) 
           & (IData)(milan_datapath__DOT__render_setpoint__DOT__st0_w));
    __VdfgRegularize_h6e95ff9d_0_299 = ((~ (IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__chpos_r)) 
                                        & (IData)(milan_datapath__DOT__render_setpoint__DOT__st0_w));
    vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__row1_w 
        = (0x0000001fU & ((IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__wptr_in_w) 
                          + (IData)(milan_datapath__DOT__render_setpoint__DOT__adv0_w)));
    vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__drop1_w 
        = ((0U == (IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__ch1_w))
            ? (0x20U == (0x0000003fU & ((IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__fill_in_w) 
                                        + (IData)(milan_datapath__DOT__render_setpoint__DOT__adv0_w))))
            : (IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__drop0_w));
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
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__void_hard_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__reload_ok_w) 
           | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__rebase_w));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__commit_w 
        = ((IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pool_wr_commit_w) 
           & (1U == vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__st_r
              [vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pool_wr_slot_w]));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__grant_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pool_alloc_req_w) 
           & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__pick_ok_w));
    __VdfgRegularize_h6e95ff9d_0_196 = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__ev_cancel_w) 
                                        | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__ev_rsp_w));
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
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_270 = (7U 
                                                  & ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_cnt_r 
                                                      >> 0x0000000cU) 
                                                     - 
                                                     (1U 
                                                      & (- (IData)((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_281))))));
    __VdfgRegularize_h6e95ff9d_0_278 = (((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_281) 
                                         << 4U) | (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_280));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__v1_pass_w 
        = ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_264) 
           & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__cdl_known_r) 
              & (((0x00000fffU & ((IData)(1U) + (0x000007ffU 
                                                 & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__idx_r) 
                                                    - (IData)(0x000eU))))) 
                  >= (0x00000fffU & ((IData)(0x000cU) 
                                     + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__cdl_r)))) 
                 & (0x0240U >= (0x00000fffU & ((IData)(0x000cU) 
                                               + (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__cdl_r)))))));
    vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__ltap_txmac_w 
        = ((IData)(vlSelfRef.m_axis_mac_tx_tlast) & (IData)(vlSelfRef.milan_datapath__DOT__adp_tx_mux__DOT__beat_accepted));
    vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__h0e_sel0_w 
        = ((~ (IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__wptr_in_w)) 
           & (IData)(__VdfgRegularize_h6e95ff9d_0_299));
    vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__h0o_sel0_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__wptr_in_w) 
           & (IData)(__VdfgRegularize_h6e95ff9d_0_299));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_297 = (0x0000003fU 
                                                  & ((0x0000003cU 
                                                      & ((vlSelfRef.__VdfgRegularize_h6e95ff9d_0_292 
                                                          + 
                                                          ((IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__row1_w) 
                                                           >> 1U)) 
                                                         << 2U)) 
                                                     + 
                                                     (7U 
                                                      & ((IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__ch1_w) 
                                                         >> 1U))));
    vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__ovr1_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__drop1_w) 
           & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_300));
    vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__st1_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__s_ok_w) 
           & ((~ (IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__drop1_w)) 
              & (8U > (IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__ch1_w))));
    vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__wptr_nxt_w 
        = (0x0000003fU & ((IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__wptr_in_w) 
                          + (((~ (IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__drop1_w)) 
                              & (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_300)) 
                             + (IData)(milan_datapath__DOT__render_setpoint__DOT__adv0_w))));
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
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__ev_accept_w 
        = ((~ (IData)(__VdfgRegularize_h6e95ff9d_0_196)) 
           & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__accept_ok_w));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__sb_gnt_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__sb_adm_req_w) 
           & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__ff_valid_w) 
              & ((~ (IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__conflict_any_w)) 
                 & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__barrier_pend_r)) 
                    | (1U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__sb_adm_class_w))))));
    __VdfgRegularize_h6e95ff9d_0_279 = ((0U != (7U 
                                                & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_cnt_r 
                                                   >> 0x0000000fU))) 
                                        & (0U == (IData)(__VdfgRegularize_h6e95ff9d_0_278)));
    vlSelfRef.milan_datapath__DOT__mac_events_w = (
                                                   (((IData)(vlSelfRef.milan_datapath__DOT__rx_mac_good_w) 
                                                     << 8U) 
                                                    | (0x000000f0U 
                                                       & (IData)(vlSelfRef.i_mac_events))) 
                                                   | (((IData)(vlSelfRef.milan_datapath__DOT__aaf_latency_tap_bank__DOT__ltap_txmac_w) 
                                                       << 3U) 
                                                      | (7U 
                                                         & (IData)(vlSelfRef.i_mac_events))));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_298 = ((~ (IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__ch1_w)) 
                                                  & (IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__st1_w));
    vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__fill_end_w 
        = (0x0000003fU & ((IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__wptr_nxt_w) 
                          - (IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__rptr_eff_in_w)));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__gnt_now_w 
        = ((0U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__st_r)) 
           & ((~ (((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__cap_hold_r) 
                   | (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__arm_ok_w)) 
                  & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__mut_req_w))) 
              & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__nvm_req_w)));
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
    __VdfgRegularize_h6e95ff9d_0_195 = (1U & (~ ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__ev_accept_w) 
                                                 | (IData)(__VdfgRegularize_h6e95ff9d_0_196))));
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__aecp_sb_grant_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__sb_pick_aecp_w) 
           & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__sb_gnt_w));
    milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__acmp_sb_grant_w 
        = ((IData)(milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__sb_pick_acmp_w) 
           & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__sb_gnt_w));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_271 = (7U 
                                                  & ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_cnt_r 
                                                      >> 0x0000000fU) 
                                                     - 
                                                     (1U 
                                                      & (- (IData)((IData)(__VdfgRegularize_h6e95ff9d_0_279))))));
    __VdfgRegularize_h6e95ff9d_0_276 = (((IData)(__VdfgRegularize_h6e95ff9d_0_279) 
                                         << 5U) | (IData)(__VdfgRegularize_h6e95ff9d_0_278));
    milan_datapath__DOT__render_setpoint__DOT__pend_in_w = 0U;
    milan_datapath__DOT__render_setpoint__DOT__prefill_in_w = 1U;
    if ((0U == vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__idxq_r
         [vlSelfRef.milan_datapath__DOT__aaf_rx_depkt__DOT__idxq_rp_r])) {
        milan_datapath__DOT__render_setpoint__DOT__pend_in_w 
            = vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__pend_r[0U];
        milan_datapath__DOT__render_setpoint__DOT__prefill_in_w 
            = vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__prefill_r[0U];
    }
    vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__recentre_p_w 
        = (((IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__pdu_end_w) 
            & (IData)(milan_datapath__DOT__render_setpoint__DOT__pend_in_w)) 
           & (~ (IData)(milan_datapath__DOT__render_setpoint__DOT__prefill_in_w)));
    vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__rail_p_w 
        = ((((IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__pdu_end_w) 
             & (~ (IData)(milan_datapath__DOT__render_setpoint__DOT__pend_in_w))) 
            & (~ (IData)(milan_datapath__DOT__render_setpoint__DOT__prefill_in_w))) 
           & ((0x14U < (IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__fill_end_w)) 
              | (0x0000000eU > ((IData)(6U) + (IData)(vlSelfRef.milan_datapath__DOT__render_setpoint__DOT__fill_end_w)))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__gnt_opmut_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__gnt_now_w) 
           & ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__mut_req_w) 
              & ((0U != vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__img_len_r) 
                 & ((0U != (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__eff_len_w)) 
                    & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__span_ok_w)))));
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
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__ev_iss_w 
        = ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_ca_builder__DOT__cancel_hit_w)) 
           & ((IData)(__VdfgRegularize_h6e95ff9d_0_195) 
              & ((4U == (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_ca_builder__DOT__c_st_r)) 
                 & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__pend_ok_w)) 
                    & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__free_ok_w)))));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__ev_exp_w 
        = ((IData)(__VdfgRegularize_h6e95ff9d_0_195) 
           & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__pend_ok_w));
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
    __VdfgRegularize_h6e95ff9d_0_277 = ((0U != (7U 
                                                & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_cnt_r 
                                                   >> 0x00000012U))) 
                                        & (0U == (IData)(__VdfgRegularize_h6e95ff9d_0_276)));
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__void_grant_w 
        = ((IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__gnt_opmut_w) 
           & ((~ (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__cap_att_r)) 
              & (IData)(vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__cap_open_r)));
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
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_272 = (7U 
                                                  & ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_cnt_r 
                                                      >> 0x00000012U) 
                                                     - 
                                                     (1U 
                                                      & (- (IData)((IData)(__VdfgRegularize_h6e95ff9d_0_277))))));
    __VdfgRegularize_h6e95ff9d_0_274 = (((IData)(__VdfgRegularize_h6e95ff9d_0_277) 
                                         << 6U) | (IData)(__VdfgRegularize_h6e95ff9d_0_276));
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
    __VdfgRegularize_h6e95ff9d_0_275 = ((0U != (7U 
                                                & (vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_cnt_r 
                                                   >> 0x00000015U))) 
                                        & (0U == (IData)(__VdfgRegularize_h6e95ff9d_0_274)));
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
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_pop_w 
        = (((IData)(__VdfgRegularize_h6e95ff9d_0_275) 
            << 7U) | (IData)(__VdfgRegularize_h6e95ff9d_0_274));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_273 = (7U 
                                                  & ((vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_cnt_r 
                                                      >> 0x00000015U) 
                                                     - 
                                                     (1U 
                                                      & (- (IData)((IData)(__VdfgRegularize_h6e95ff9d_0_275))))));
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
    vlSelfRef.milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_mid_w 
        = ((((((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_273) 
               << 9U) | ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_272) 
                         << 6U)) | (((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_271) 
                                     << 3U) | (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_270))) 
            << 0x0000000cU) | ((((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_269) 
                                 << 9U) | ((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_268) 
                                           << 6U)) 
                               | (((IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_267) 
                                   << 3U) | (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_266))));
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

#ifdef VL_DEBUG
VL_ATTR_COLD void Vmilan_datapath___024root___dump_triggers__stl(const VlUnpacked<QData/*63:0*/, 1> &triggers, const std::string &tag);
#endif  // VL_DEBUG
VL_ATTR_COLD bool Vmilan_datapath___024root___trigger_anySet__stl(const VlUnpacked<QData/*63:0*/, 1> &in);
VL_ATTR_COLD void Vmilan_datapath___024root___stl_sequent__TOP__0(Vmilan_datapath___024root* vlSelf);
VL_ATTR_COLD void Vmilan_datapath___024root___stl_sequent__TOP__1(Vmilan_datapath___024root* vlSelf);
VL_ATTR_COLD void Vmilan_datapath___024root___stl_sequent__TOP__2(Vmilan_datapath___024root* vlSelf);

VL_ATTR_COLD bool Vmilan_datapath___024root___eval_phase__stl(Vmilan_datapath___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vmilan_datapath___024root___eval_phase__stl\n"); );
    Vmilan_datapath__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    CData/*0:0*/ __VstlExecute;
    // Body
    {
        // Inlined CFunc: _eval_triggers_vec__stl
        vlSelfRef.__VstlTriggered[0U] = ((0xfffffffffffffffeULL 
                                          & vlSelfRef.__VstlTriggered[0U]) 
                                         | (IData)((IData)(vlSelfRef.__VstlFirstIteration)));
    }
#ifdef VL_DEBUG
    if (VL_UNLIKELY(vlSymsp->_vm_contextp__->debug())) {
        Vmilan_datapath___024root___dump_triggers__stl(vlSelfRef.__VstlTriggered, "stl"s);
    }
#endif
    __VstlExecute = Vmilan_datapath___024root___trigger_anySet__stl(vlSelfRef.__VstlTriggered);
    if (__VstlExecute) {
        {
            // Inlined CFunc: _eval_stl
            if ((1ULL & vlSelfRef.__VstlTriggered[0U])) {
                Vmilan_datapath___024root___stl_sequent__TOP__0(vlSelf);
                Vmilan_datapath___024root___stl_sequent__TOP__1(vlSelf);
                Vmilan_datapath___024root___stl_sequent__TOP__2(vlSelf);
                Vmilan_datapath___024root___stl_sequent__TOP__3(vlSelf);
            }
        }
    }
    return (__VstlExecute);
}

bool Vmilan_datapath___024root___trigger_anySet__ico(const VlUnpacked<QData/*63:0*/, 3> &in);

#ifdef VL_DEBUG
VL_ATTR_COLD void Vmilan_datapath___024root___dump_triggers__ico(const VlUnpacked<QData/*63:0*/, 3> &triggers, const std::string &tag) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vmilan_datapath___024root___dump_triggers__ico\n"); );
    // Body
    if ((1U & (~ (IData)(Vmilan_datapath___024root___trigger_anySet__ico(triggers))))) {
        VL_DBG_MSGS("         No '" + tag + "' region triggers active\n");
    }
    if ((1U & (IData)(triggers[0U]))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 0 is active: @( i_desc_mem_req_ready)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 1U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 1 is active: @( i_desc_mem_rsp_valid)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 2U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 2 is active: @( i_desc_mem_rsp_data)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 3U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 3 is active: @( i_desc_mem_rsp_last)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 4U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 4 is active: @( i_desc_mem_rsp_err)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 5U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 5 is active: @( i_resp_mem_req_ready)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 6U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 6 is active: @( i_resp_mem_rsp_valid)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 7U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 7 is active: @( i_resp_mem_rsp_data)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 8U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 8 is active: @( i_resp_mem_rsp_last)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 9U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 9 is active: @( i_resp_mem_rsp_err)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x0000000aU)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 10 is active: @( i_resp_mem_wr_ready)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x0000000bU)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 11 is active: @( i_resp_mem_wr_done)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x0000000cU)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 12 is active: @( i_resp_mem_wr_err)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x0000000dU)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 13 is active: @( i_nvm_mem_req_ready)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x0000000eU)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 14 is active: @( i_nvm_mem_rsp_valid)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x0000000fU)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 15 is active: @( i_nvm_mem_rsp_data)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x00000010U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 16 is active: @( i_nvm_mem_rsp_last)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x00000011U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 17 is active: @( i_nvm_mem_rsp_err)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x00000012U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 18 is active: @( i_nvm_mem_wr_ready)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x00000013U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 19 is active: @( i_nvm_mem_wr_done)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x00000014U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 20 is active: @( i_nvm_mem_wr_err)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x00000015U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 21 is active: @( axis_clk)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x00000016U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 22 is active: @( clk_audio_i)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x00000017U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 23 is active: @( clk_tdm_i)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x00000018U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 24 is active: @( axis_resetn)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x00000019U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 25 is active: @( gtx_clk)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x0000001aU)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 26 is active: @( gtx_resetn)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x0000001bU)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 27 is active: @( s_axi_awaddr)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x0000001cU)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 28 is active: @( s_axi_awvalid)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x0000001dU)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 29 is active: @( s_axi_wdata)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x0000001eU)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 30 is active: @( s_axi_wstrb)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x0000001fU)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 31 is active: @( s_axi_wvalid)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x00000020U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 32 is active: @( s_axi_bready)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x00000021U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 33 is active: @( s_axi_araddr)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x00000022U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 34 is active: @( s_axi_arvalid)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x00000023U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 35 is active: @( s_axi_rready)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x00000024U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 36 is active: @( i2s_sdout_i)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x00000025U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 37 is active: @( tdm_bclk_i)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x00000026U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 38 is active: @( tdm_fsync_i)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x00000027U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 39 is active: @( tdm_data_i)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x00000028U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 40 is active: @( m_axis_mac_tx_tready)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x00000029U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 41 is active: @( s_axis_mac_rx_tdata)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x0000002aU)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 42 is active: @( s_axis_mac_rx_tkeep)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x0000002bU)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 43 is active: @( s_axis_mac_rx_tvalid)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x0000002cU)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 44 is active: @( s_axis_mac_rx_tlast)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x0000002dU)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 45 is active: @( i_mac_speed)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x0000002eU)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 46 is active: @( i_link_up)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x0000002fU)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 47 is active: @( i_full_duplex)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x00000030U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 48 is active: @( i_ethrx_tgl)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x00000031U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 49 is active: @( i_ethtx_tgl)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x00000032U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 50 is active: @( i_ethact_tgl)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x00000033U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 51 is active: @( i_gptp_txrec_valid)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x00000034U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 52 is active: @( i_gptp_txrec_kind)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x00000035U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 53 is active: @( i_gptp_txrec_oidx)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x00000036U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 54 is active: @( i_gptp_txrec_gen)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x00000037U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 55 is active: @( i_gptp_txrec_type)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x00000038U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 56 is active: @( i_gptp_txrec_seq)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x00000039U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 57 is active: @( i_gptp_txrec_delta)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x0000003aU)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 58 is active: @( i_gptp_txrec_abort)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x0000003bU)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 59 is active: @( i_gptp_txseal_ack)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x0000003cU)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 60 is active: @( i_mac_events)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x0000003dU)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 61 is active: @( i_mac_events_cap)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x0000003eU)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 62 is active: @( i_ps_clk)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x0000003fU)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 63 is active: @( i_mmcm_drp_do)\n");
    }
    if ((1U & (IData)(triggers[1U]))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 64 is active: @( i_mmcm_drp_rdy)\n");
    }
    if ((1U & (IData)((triggers[1U] >> 1U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 65 is active: @( i_mmcm_locked)\n");
    }
    if ((1U & (IData)((triggers[1U] >> 2U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 66 is active: @( i_mmcm_ps_done)\n");
    }
    if ((1U & (IData)(triggers[2U]))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 128 is active: Internal 'ico' trigger - first iteration\n");
    }
}
#endif  // VL_DEBUG

bool Vmilan_datapath___024root___trigger_anySet__act(const VlUnpacked<QData/*63:0*/, 1> &in);

#ifdef VL_DEBUG
VL_ATTR_COLD void Vmilan_datapath___024root___dump_triggers__act(const VlUnpacked<QData/*63:0*/, 1> &triggers, const std::string &tag) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vmilan_datapath___024root___dump_triggers__act\n"); );
    // Body
    if ((1U & (~ (IData)(Vmilan_datapath___024root___trigger_anySet__act(triggers))))) {
        VL_DBG_MSGS("         No '" + tag + "' region triggers active\n");
    }
    if ((1U & (IData)(triggers[0U]))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 0 is active: @(posedge axis_clk)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 1U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 1 is active: @(posedge clk_audio_i)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 2U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 2 is active: @(negedge axis_resetn)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 3U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 3 is active: @(posedge i_ps_clk)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 4U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 4 is active: @(posedge gtx_clk)\n");
    }
}
#endif  // VL_DEBUG

VL_ATTR_COLD void Vmilan_datapath___024root___ctor_var_reset(Vmilan_datapath___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vmilan_datapath___024root___ctor_var_reset\n"); );
    Vmilan_datapath__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    const uint64_t __VscopeHash = VL_MURMUR64_HASH(vlSelf->vlNamep);
    vlSelf->o_desc_mem_req_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2667050038079292831ull);
    vlSelf->i_desc_mem_req_ready = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8868677312643362022ull);
    vlSelf->o_desc_mem_req_addr = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 9154476205237090934ull);
    vlSelf->o_desc_mem_req_beats = VL_SCOPED_RAND_RESET_I(9, __VscopeHash, 14760006347966961773ull);
    vlSelf->i_desc_mem_rsp_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 730705032975086585ull);
    vlSelf->o_desc_mem_rsp_ready = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16765505437643319423ull);
    vlSelf->i_desc_mem_rsp_data = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 15455013581529207224ull);
    vlSelf->i_desc_mem_rsp_last = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15050997520097779221ull);
    vlSelf->i_desc_mem_rsp_err = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10213290467115729483ull);
    vlSelf->o_resp_mem_req_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7307116329899304106ull);
    vlSelf->i_resp_mem_req_ready = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6161005380651978299ull);
    vlSelf->o_resp_mem_req_addr = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 16996936742912076912ull);
    vlSelf->o_resp_mem_req_beats = VL_SCOPED_RAND_RESET_I(9, __VscopeHash, 16057460621739218637ull);
    vlSelf->i_resp_mem_rsp_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 617622351816625060ull);
    vlSelf->o_resp_mem_rsp_ready = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4180124356250260656ull);
    vlSelf->i_resp_mem_rsp_data = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 13329204055210235547ull);
    vlSelf->i_resp_mem_rsp_last = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17996531957437589366ull);
    vlSelf->i_resp_mem_rsp_err = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17381019176809597223ull);
    vlSelf->o_resp_mem_wr_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8835795758083461948ull);
    vlSelf->i_resp_mem_wr_ready = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 444606988175206172ull);
    vlSelf->o_resp_mem_wr_addr = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 15146019400605179493ull);
    vlSelf->o_resp_mem_wr_data = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 16662905933462982873ull);
    vlSelf->o_resp_mem_wr_strb = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 1611320332159165967ull);
    vlSelf->i_resp_mem_wr_done = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4991736589475621811ull);
    vlSelf->i_resp_mem_wr_err = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13890876695204014545ull);
    vlSelf->o_nvm_mem_req_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14749165182062124657ull);
    vlSelf->i_nvm_mem_req_ready = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8105560425128454488ull);
    vlSelf->o_nvm_mem_req_addr = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 1588381474527891421ull);
    vlSelf->o_nvm_mem_req_beats = VL_SCOPED_RAND_RESET_I(9, __VscopeHash, 5962403736747625192ull);
    vlSelf->i_nvm_mem_rsp_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5795094307770893648ull);
    vlSelf->o_nvm_mem_rsp_ready = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17621516931727933874ull);
    vlSelf->i_nvm_mem_rsp_data = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 5573397802105033447ull);
    vlSelf->i_nvm_mem_rsp_last = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5047924574147241584ull);
    vlSelf->i_nvm_mem_rsp_err = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14542347680951931127ull);
    vlSelf->o_nvm_mem_wr_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4842354538128773164ull);
    vlSelf->i_nvm_mem_wr_ready = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15009415739509385685ull);
    vlSelf->o_nvm_mem_wr_addr = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 10615181036089806191ull);
    vlSelf->o_nvm_mem_wr_data = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 13972138878913115676ull);
    vlSelf->o_nvm_mem_wr_strb = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 3185497887845176648ull);
    vlSelf->i_nvm_mem_wr_done = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5274391649416581747ull);
    vlSelf->i_nvm_mem_wr_err = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10337202336906502982ull);
    vlSelf->axis_clk = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6077951788264469019ull);
    vlSelf->clk_audio_i = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1594742816405956070ull);
    vlSelf->clk_tdm_i = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7413527665814040540ull);
    vlSelf->axis_resetn = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13353824713052781882ull);
    vlSelf->gtx_clk = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5173468789992344027ull);
    vlSelf->gtx_resetn = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2680759800423739578ull);
    vlSelf->s_axi_awaddr = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 7303631981020876172ull);
    vlSelf->s_axi_awvalid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13986037914296269070ull);
    vlSelf->s_axi_awready = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14099717354022636468ull);
    vlSelf->s_axi_wdata = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 11311253403970331505ull);
    vlSelf->s_axi_wstrb = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 18112015138521062007ull);
    vlSelf->s_axi_wvalid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12168530306759773544ull);
    vlSelf->s_axi_wready = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17608475915581965368ull);
    vlSelf->s_axi_bresp = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 15162762900795686431ull);
    vlSelf->s_axi_bvalid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9334582144896637853ull);
    vlSelf->s_axi_bready = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15653039750784194130ull);
    vlSelf->s_axi_araddr = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 8722301305194254610ull);
    vlSelf->s_axi_arvalid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17746383479076595557ull);
    vlSelf->s_axi_arready = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17791137924766170856ull);
    vlSelf->s_axi_rdata = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 12866136205313389248ull);
    vlSelf->s_axi_rresp = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 14929039895447920609ull);
    vlSelf->s_axi_rvalid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15026938065200214434ull);
    vlSelf->s_axi_rready = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1794163653381394343ull);
    vlSelf->i2s_mclk_o = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5423347039955195428ull);
    vlSelf->i2s_sclk_o = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12336826856301995358ull);
    vlSelf->i2s_lrck_o = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12702184149590278752ull);
    vlSelf->i2s_sdout_i = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12609160700012968368ull);
    vlSelf->tdm_bclk_i = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5699283679770343600ull);
    vlSelf->tdm_fsync_i = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10282997290289300815ull);
    vlSelf->tdm_bclk_o = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6965329311526475437ull);
    vlSelf->tdm_fsync_o = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16814085176203882082ull);
    vlSelf->media_lrclk_o = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14267257203422007242ull);
    vlSelf->pps_o = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 494722626202832635ull);
    vlSelf->tdm_mclk_o = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10274639198335473810ull);
    vlSelf->tdm_dout_o = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10075644028125443285ull);
    vlSelf->tdm_data_i = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 249104219551189225ull);
    vlSelf->i2s_dac_mclk_o = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15991117030507183412ull);
    vlSelf->i2s_dac_sclk_o = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6188101327151889509ull);
    vlSelf->i2s_dac_lrck_o = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15109550057939289842ull);
    vlSelf->i2s_dac_sdin_o = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12092247001711845357ull);
    vlSelf->m_axis_mac_tx_tdata = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 15143801499840899111ull);
    vlSelf->m_axis_mac_tx_tkeep = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 738608253460617607ull);
    vlSelf->m_axis_mac_tx_tvalid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5400468824722945811ull);
    vlSelf->m_axis_mac_tx_tlast = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10639951793926383514ull);
    vlSelf->m_axis_mac_tx_tready = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9083978707389035195ull);
    vlSelf->s_axis_mac_rx_tdata = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 12209863760678251275ull);
    vlSelf->s_axis_mac_rx_tkeep = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 16585703592530200061ull);
    vlSelf->s_axis_mac_rx_tvalid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14244922896429315029ull);
    vlSelf->s_axis_mac_rx_tlast = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2220400039292505466ull);
    vlSelf->s_axis_mac_rx_tready = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13317654005310498863ull);
    vlSelf->o_mac_tx_en = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15037823534458705414ull);
    vlSelf->o_mac_rx_en = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5063602202964203523ull);
    vlSelf->o_mac_promisc = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4670518256112370292ull);
    vlSelf->o_mac_allmulti = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10925070383356420001ull);
    vlSelf->o_mac_is_1g = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4966978584655898513ull);
    vlSelf->o_mac_ifg = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 12558639081818450165ull);
    vlSelf->o_mac_addr = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 1090671019676852888ull);
    vlSelf->o_mc_hash = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 5755992057034942001ull);
    vlSelf->o_phy_reset_n = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5522851275748308250ull);
    vlSelf->i_mac_speed = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 8070410579128174512ull);
    vlSelf->i_link_up = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11482461471016620714ull);
    vlSelf->o_mac_reinit = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3309491463662001815ull);
    vlSelf->o_eth_rst = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11540013861626318719ull);
    vlSelf->o_eth_guard = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2846586284369606220ull);
    vlSelf->i_full_duplex = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8284182092553005671ull);
    vlSelf->i_ethrx_tgl = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13779400073553134942ull);
    vlSelf->i_ethtx_tgl = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6328850538460614146ull);
    vlSelf->i_ethact_tgl = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8350416218769883425ull);
    vlSelf->i_gptp_txrec_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17927859408229061853ull);
    vlSelf->i_gptp_txrec_kind = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6205025331623544110ull);
    vlSelf->i_gptp_txrec_oidx = VL_SCOPED_RAND_RESET_I(12, __VscopeHash, 18085584948308783970ull);
    vlSelf->i_gptp_txrec_gen = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 9311691543024383326ull);
    vlSelf->i_gptp_txrec_type = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 896769271273832208ull);
    vlSelf->i_gptp_txrec_seq = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 9388902819427754282ull);
    vlSelf->i_gptp_txrec_delta = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 9557481146414525941ull);
    vlSelf->i_gptp_txrec_abort = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5043601533688620292ull);
    vlSelf->o_gptp_txseal_req = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14765613486937856141ull);
    vlSelf->o_gptp_txseal_gen = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 5683378379347307202ull);
    vlSelf->i_gptp_txseal_ack = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3790354108914465164ull);
    vlSelf->i_mac_events = VL_SCOPED_RAND_RESET_I(9, __VscopeHash, 15629906174150829998ull);
    vlSelf->i_mac_events_cap = VL_SCOPED_RAND_RESET_I(9, __VscopeHash, 3340822992242150149ull);
    vlSelf->o_irq_csr = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6225454987077696020ull);
    vlSelf->o_identify = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 18283969343321504074ull);
    vlSelf->i_ps_clk = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6937211462614486023ull);
    vlSelf->o_mmcm_drp_addr = VL_SCOPED_RAND_RESET_I(7, __VscopeHash, 9865487830482611112ull);
    vlSelf->o_mmcm_drp_en = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 18272286907461658735ull);
    vlSelf->o_mmcm_drp_we = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14416325893219994434ull);
    vlSelf->o_mmcm_drp_di = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 10469714080661564417ull);
    vlSelf->i_mmcm_drp_do = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 16827613955313012702ull);
    vlSelf->i_mmcm_drp_rdy = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6419347779287378628ull);
    vlSelf->o_mmcm_rst = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9755853081830159184ull);
    vlSelf->i_mmcm_locked = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16896774293450154370ull);
    vlSelf->o_mmcm_ps_en = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5587911038871228330ull);
    vlSelf->o_mmcm_ps_incdec = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3062487017950512122ull);
    vlSelf->i_mmcm_ps_done = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16029815512320568101ull);
    vlSelf->milan_datapath__DOT__pp_aecp_clk_src_index_w = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 12732346862404923393ull);
    vlSelf->milan_datapath__DOT__crf_clk_selected_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16305538096605785029ull);
    vlSelf->milan_datapath__DOT__media_clk_src_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 17805483368745373658ull);
    vlSelf->milan_datapath__DOT__media_tick_p = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11265168358881453983ull);
    vlSelf->milan_datapath__DOT__media_tick_phase_w = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 17283678665267530740ull);
    vlSelf->milan_datapath__DOT__mnco_servo_trim_w = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 10701292644256787574ull);
    vlSelf->milan_datapath__DOT__mnco_servo_en_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16619856078398723073ull);
    vlSelf->milan_datapath__DOT__media_lrclk_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12478434427747648455ull);
    vlSelf->milan_datapath__DOT__aafcap_pv_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11497447767300903891ull);
    vlSelf->milan_datapath__DOT__aafcap_l_w = VL_SCOPED_RAND_RESET_I(24, __VscopeHash, 2540879576097001706ull);
    vlSelf->milan_datapath__DOT__aafcap_r_w = VL_SCOPED_RAND_RESET_I(24, __VscopeHash, 3334977953252108941ull);
    vlSelf->milan_datapath__DOT__cmap_pv_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8426201612662789099ull);
    vlSelf->milan_datapath__DOT__cmap_slot_w = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 10857960519165212280ull);
    vlSelf->milan_datapath__DOT__cmap_l_w = VL_SCOPED_RAND_RESET_I(24, __VscopeHash, 15823033237472017079ull);
    vlSelf->milan_datapath__DOT__cmap_r_w = VL_SCOPED_RAND_RESET_I(24, __VscopeHash, 10996773100535320075ull);
    vlSelf->milan_datapath__DOT__amap_edit_owr_p_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16495982688575345680ull);
    vlSelf->milan_datapath__DOT__amap_edit_owr_slot_r = VL_SCOPED_RAND_RESET_I(6, __VscopeHash, 5112761950495957837ull);
    vlSelf->milan_datapath__DOT__amap_edit_owr_word_r = VL_SCOPED_RAND_RESET_I(13, __VscopeHash, 3199295146721637708ull);
    vlSelf->milan_datapath__DOT__amap_edit_txn_active_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16889369414864133809ull);
    vlSelf->milan_datapath__DOT__lb_tap_tvalid_w = 0U;
    ;
    vlSelf->milan_datapath__DOT__lb_tap_tlast_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1541039286991494199ull);
    vlSelf->milan_datapath__DOT__lb_tap_tuser_w = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 8901795246303674702ull);
    vlSelf->milan_datapath__DOT__lb_dup_cnt_w = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 17143530683147925035ull);
    vlSelf->milan_datapath__DOT__lb_skip_cnt_w = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 4142069658456470266ull);
    vlSelf->milan_datapath__DOT__tdm_dup_cnt_w = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 1813592009671874202ull);
    vlSelf->milan_datapath__DOT__tdm_skip_cnt_w = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 12283677046952499785ull);
    VL_SCOPED_RAND_RESET_W(104, vlSelf->milan_datapath__DOT__cmap_flat_w, __VscopeHash, 18309937019074612431ull);
    vlSelf->milan_datapath__DOT__amap_out_owner_v_r = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 9794984670796475197ull);
    VL_SCOPED_RAND_RESET_W(128, vlSelf->milan_datapath__DOT__amap_out_owner_r, __VscopeHash, 4615230875682556248ull);
    VL_SCOPED_RAND_RESET_W(128, vlSelf->milan_datapath__DOT__amap_out_cluster_r, __VscopeHash, 15371633750755554623ull);
    vlSelf->milan_datapath__DOT____Vcellinp__chan_map_capture__map_rd_en_i = 0;
    vlSelf->milan_datapath__DOT____Vcellinp__aaf_packetizer__transit_ns_i = 0;
    VL_SCOPED_RAND_RESET_W(288, vlSelf->milan_datapath__DOT__stats_counts, __VscopeHash, 10706589549752702121ull);
    vlSelf->milan_datapath__DOT__cfg_adp_entity_id = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 12778838654269787552ull);
    vlSelf->milan_datapath__DOT__lwsrp_listener_ready = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11281255878166338913ull);
    vlSelf->milan_datapath__DOT__lwsrp_listener_decl = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 3671276769258653978ull);
    vlSelf->milan_datapath__DOT__lwsrp_ta_fail_code = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 11149421810067148588ull);
    vlSelf->milan_datapath__DOT__avtprx_match = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9581928488041677097ull);
    vlSelf->milan_datapath__DOT__avtprx_tu_bit = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15750408439100639188ull);
    vlSelf->milan_datapath__DOT__avtprx_tv_bit = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17263965647936818071ull);
    vlSelf->milan_datapath__DOT__avtprx_mr_bit = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 18164154069689068399ull);
    vlSelf->milan_datapath__DOT__avtprx_subtype = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 15517962545694870490ull);
    vlSelf->milan_datapath__DOT__avtprx_seq = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 15318652276024131232ull);
    vlSelf->milan_datapath__DOT__avtprx_parse_p = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17471729444664175489ull);
    vlSelf->milan_datapath__DOT__avtprx_b3 = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 6854776964281988079ull);
    vlSelf->milan_datapath__DOT__avtprx_sid_frame = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 9357593800724767191ull);
    vlSelf->milan_datapath__DOT__avtprx_fsh2 = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 13813041616072532820ull);
    vlSelf->milan_datapath__DOT__crf_delta_w = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 11585917338666239029ull);
    vlSelf->milan_datapath__DOT__crf_rate_w = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 14603279414965205478ull);
    vlSelf->milan_datapath__DOT__mcsrv_stat_w = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 9228740808070464820ull);
    vlSelf->milan_datapath__DOT__amap_edit_iwr_p_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17204675762029697724ull);
    vlSelf->milan_datapath__DOT__amap_edit_iwr_addr_r = VL_SCOPED_RAND_RESET_I(6, __VscopeHash, 9324200136997891979ull);
    vlSelf->milan_datapath__DOT__amap_edit_iwr_word_r = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 7541918286861598196ull);
    vlSelf->milan_datapath__DOT__cmap_rd_data_w = VL_SCOPED_RAND_RESET_I(15, __VscopeHash, 2072824648919118899ull);
    vlSelf->milan_datapath__DOT__cmap_rd_valid_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6545621321986456474ull);
    vlSelf->milan_datapath__DOT__rmap_rd_data_w = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 16740915263080753453ull);
    vlSelf->milan_datapath__DOT__rmap_rd_valid_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1959725660008616375ull);
    vlSelf->milan_datapath__DOT__crf_pducnt_w = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 10817382443418001049ull);
    vlSelf->milan_datapath__DOT__crf_fmterr_w = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 8743435823925351606ull);
    vlSelf->milan_datapath__DOT__crf_seqerr_w = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 12301550503346426821ull);
    vlSelf->milan_datapath__DOT__crf_locked_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14272717680748612485ull);
    vlSelf->milan_datapath__DOT__crf_lockcnt_w = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 4737469866778718827ull);
    vlSelf->milan_datapath__DOT__crf_unlockcnt_w = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 4793504279497291166ull);
    vlSelf->milan_datapath__DOT__crf_intrcnt_w = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 8560755476963996974ull);
    vlSelf->milan_datapath__DOT__crf_mrcnt_w = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 1407852506008524172ull);
    vlSelf->milan_datapath__DOT__crf_tucnt_w = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 8242915332473816102ull);
    vlSelf->milan_datapath__DOT__crf_latecnt_w = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 14768685362625846368ull);
    vlSelf->milan_datapath__DOT__crf_earlycnt_w = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 16657145348266901610ull);
    vlSelf->milan_datapath__DOT__crf_mr_toggle_p_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7168775977513731891ull);
    vlSelf->milan_datapath__DOT__cfg_crft_sid = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 3719907576149270471ull);
    vlSelf->milan_datapath__DOT__cfg_crft_dmac = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 9316951305529298624ull);
    vlSelf->milan_datapath__DOT__crft_count_w = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 10242208974377535130ull);
    vlSelf->milan_datapath__DOT__crft_tu_last_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12244388762294906327ull);
    vlSelf->milan_datapath__DOT__crft_mr_last_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 18396061250015690919ull);
    vlSelf->milan_datapath__DOT__avtprx_fsh = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 12124802238740490791ull);
    vlSelf->milan_datapath__DOT__aecp_in0_fmt = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 11405417124878832838ull);
    vlSelf->milan_datapath__DOT__avtprx_locked_c = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 10220531439738838723ull);
    vlSelf->milan_datapath__DOT__avtprx_unlocked_c = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 3610443356898165884ull);
    vlSelf->milan_datapath__DOT__avtprx_intr_c = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 12867675969829508175ull);
    vlSelf->milan_datapath__DOT__avtprx_seqmm_c = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 9497827592088147795ull);
    vlSelf->milan_datapath__DOT__avtprx_tu_c = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 2830501567389268452ull);
    vlSelf->milan_datapath__DOT__avtprx_unsupp_c = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 9723216014700180783ull);
    vlSelf->milan_datapath__DOT__avtprx_frx_c = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 14931353203232863924ull);
    vlSelf->milan_datapath__DOT__avtprx_locked = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14348297884874342533ull);
    vlSelf->milan_datapath__DOT__avtprx_dirty_p_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10283625846283653757ull);
    vlSelf->milan_datapath__DOT__avtprx_accept_p = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10207851488838004655ull);
    vlSelf->milan_datapath__DOT__avtprx_ts = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 8506778929196827176ull);
    vlSelf->milan_datapath__DOT__avtprx_last_ts = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 799081269505565408ull);
    vlSelf->milan_datapath__DOT__avtprx_last_tsd = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 5367327513087317926ull);
    vlSelf->milan_datapath__DOT__pcmrx_pdus = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 10063322807260198664ull);
    vlSelf->milan_datapath__DOT__pcmrx_drops = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 15777613349304698758ull);
    vlSelf->milan_datapath__DOT__i2spb_overruns = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 4055730579710252853ull);
    vlSelf->milan_datapath__DOT__avtprx_mreset_c = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 8002412835173788800ull);
    vlSelf->milan_datapath__DOT__avtprx_late_c = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 17866018677138587934ull);
    vlSelf->milan_datapath__DOT__avtprx_early_c = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 17285264507100190796ull);
    vlSelf->milan_datapath__DOT__tone_smp = VL_SCOPED_RAND_RESET_I(24, __VscopeHash, 16772839412458705638ull);
    vlSelf->milan_datapath__DOT__tone_smp_media = VL_SCOPED_RAND_RESET_I(24, __VscopeHash, 1201802839305259502ull);
    vlSelf->milan_datapath__DOT__maap_conflicts = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 18441516264322472447ull);
    vlSelf->milan_datapath__DOT__maap_defends = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 1591325562359595527ull);
    vlSelf->milan_datapath__DOT__maap_tx_tdata = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 641374759029110921ull);
    vlSelf->milan_datapath__DOT__eff_crft_dmac_w = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 3863360558293694943ull);
    vlSelf->milan_datapath__DOT__eff_crft_sid_w = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 3698678806625628442ull);
    vlSelf->milan_datapath__DOT__clkv_tu_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16340567062227817511ull);
    vlSelf->milan_datapath__DOT__amap_edit_out_resv_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8591594800934624661ull);
    vlSelf->milan_datapath__DOT__aaf_stream_en_raw_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4260562301886086193ull);
    vlSelf->milan_datapath__DOT__aaf_stream_en_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5162039671192246409ull);
    vlSelf->milan_datapath__DOT__aaf_frames_w = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 9527180539345585902ull);
    vlSelf->milan_datapath__DOT__aaf_pairs_w = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 15192115273525669703ull);
    vlSelf->milan_datapath__DOT__aaf_tx_tlast = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5423823035082437557ull);
    vlSelf->milan_datapath__DOT__aaf_tx_tready = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7661987217693464025ull);
    VL_SCOPED_RAND_RESET_W(448, vlSelf->milan_datapath__DOT__asp_path_w, __VscopeHash, 17140761664179065961ull);
    vlSelf->milan_datapath__DOT__asp_count_w = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 17916527853700675626ull);
    vlSelf->milan_datapath__DOT__asp_gen_w = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 1747285976709627250ull);
    vlSelf->milan_datapath__DOT__pcm_lpf_active = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5439123634673765252ull);
    vlSelf->milan_datapath__DOT__eff_link_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16817596118108666834ull);
    vlSelf->milan_datapath__DOT__speed_meta = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 4837278814806877417ull);
    vlSelf->milan_datapath__DOT__speed_sync = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 6272108155055891160ull);
    vlSelf->milan_datapath__DOT__speed_q = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 9158718518922404271ull);
    vlSelf->milan_datapath__DOT__evt_link_change = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10946406234754321371ull);
    vlSelf->milan_datapath__DOT__csr_lctx_rd_addr_w = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 10366479045102901933ull);
    vlSelf->milan_datapath__DOT__lctx_rd_data_w = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 13827211125096639787ull);
    vlSelf->milan_datapath__DOT__lctx_rd_valid_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 116946274760354784ull);
    vlSelf->milan_datapath__DOT__lctx_wr_data_sane_w = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 10320536541165763343ull);
    vlSelf->milan_datapath__DOT__csr_tctx_rd_addr_w = VL_SCOPED_RAND_RESET_I(7, __VscopeHash, 2693209302874803307ull);
    vlSelf->milan_datapath__DOT__tctx_rd_data_w = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 10637310815187602338ull);
    vlSelf->milan_datapath__DOT__tctx_rd_valid_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14633195025871186257ull);
    vlSelf->milan_datapath__DOT__tctx_wr_rdy_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15699263573784844206ull);
    VL_SCOPED_RAND_RESET_W(512, vlSelf->milan_datapath__DOT__ltap_regs_w, __VscopeHash, 2531630792937749745ull);
    VL_SCOPED_RAND_RESET_W(160, vlSelf->milan_datapath__DOT__aprb_regs_w, __VscopeHash, 15465088788055703711ull);
    vlSelf->milan_datapath__DOT__aprb_parsed_w = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 7391203514751151266ull);
    vlSelf->milan_datapath__DOT__aprb_matched_w = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 10366795533886555106ull);
    vlSelf->milan_datapath__DOT__pp_rdata_w = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 9064469494029779492ull);
    vlSelf->milan_datapath__DOT__pp_ack_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9610563667194263571ull);
    vlSelf->milan_datapath__DOT__pp_err_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17073219134359055063ull);
    vlSelf->milan_datapath__DOT__pp_restore_busy_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12878064151452578464ull);
    vlSelf->milan_datapath__DOT__pp_nvm_csr_sel_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4908178297213449620ull);
    vlSelf->milan_datapath__DOT__pp_nvm_csr_addr_w = VL_SCOPED_RAND_RESET_I(6, __VscopeHash, 12129850853464444436ull);
    vlSelf->milan_datapath__DOT__pp_rx_frames_w = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 11132658092797946645ull);
    vlSelf->milan_datapath__DOT__pp_tx_frames_w = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 3657775367789560848ull);
    vlSelf->milan_datapath__DOT__pp_rx_drops_w = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 12070018830214475850ull);
    VL_SCOPED_RAND_RESET_W(128, vlSelf->milan_datapath__DOT__pp_src_sid_w, __VscopeHash, 14665222200873159812ull);
    vlSelf->milan_datapath__DOT__pp_gm_id_q_r = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 6045710277741359080ull);
    vlSelf->milan_datapath__DOT__pp_gm_dom_q_r = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 10843908314582095475ull);
    vlSelf->milan_datapath__DOT__pp_gm_change_p_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3292366609428558518ull);
    vlSelf->milan_datapath__DOT__pp_gm_id_change_p_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3690030223481160817ull);
    vlSelf->milan_datapath__DOT__pp_cd_acmp_declaring_w = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 9202623410512817950ull);
    vlSelf->milan_datapath__DOT__pp_cd_acmp_bound_w = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 14517919695759599807ull);
    vlSelf->milan_datapath__DOT__pp_cd_adp_avail_index_w = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 4903251907467725134ull);
    vlSelf->milan_datapath__DOT__pp_maap_req_valid_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15851910464415039332ull);
    vlSelf->milan_datapath__DOT__pp_maap_req_ready_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17233450334892396080ull);
    vlSelf->milan_datapath__DOT__pp_maap_req_release_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4249471307555093908ull);
    vlSelf->milan_datapath__DOT__pp_maap_rsp_valid_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10353457647762051548ull);
    vlSelf->milan_datapath__DOT__pp_maap_rsp_ok_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 228503664110903734ull);
    vlSelf->milan_datapath__DOT__pp_maap_rsp_da_w = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 13862931638725248077ull);
    vlSelf->milan_datapath__DOT__pp_maap_confl_src_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13975339467147505820ull);
    vlSelf->milan_datapath__DOT____Vcellinp__csr__i_pcmrx_cnt = 0;
    VL_ZERO_RESET_W(320, vlSelf->milan_datapath__DOT____Vcellinp__csr__i_avtprx_cnt10);
    vlSelf->milan_datapath__DOT____Vcellinp__csr__i_avtprx_stat = 0;
    vlSelf->milan_datapath__DOT____Vcellinp__csr__i_acmpl_state = 0;
    vlSelf->milan_datapath__DOT____Vcellinp__csr__i_lwsrp_status = 0;
    vlSelf->milan_datapath__DOT__aaf_frame_p_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8194287604016912902ull);
    vlSelf->milan_datapath__DOT__aaf_frame_idx_w = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 13568086263833277174ull);
    vlSelf->milan_datapath__DOT__aaf_frame_tu_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15924998629405381290ull);
    vlSelf->milan_datapath__DOT__aaf_frame_mr_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10959778562954603781ull);
    vlSelf->milan_datapath__DOT__aecp_diag_idx_w = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 6827267527311550867ull);
    vlSelf->milan_datapath__DOT__tkd_dirty_p_w = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 12028245846128152033ull);
    vlSelf->milan_datapath__DOT__pp_ctr_req_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2313353902963702072ull);
    vlSelf->milan_datapath__DOT__pp_ctr_word_w = VL_SCOPED_RAND_RESET_I(6, __VscopeHash, 3639632834903965319ull);
    vlSelf->milan_datapath__DOT__pp_amap_req_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10663125864641491923ull);
    vlSelf->milan_datapath__DOT__pp_amap_sel_w = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 1689702088880196293ull);
    vlSelf->milan_datapath__DOT__pp_amap_edit_req_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 712798399531885156ull);
    vlSelf->milan_datapath__DOT__pp_amap_edit_phase_w = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 5643030023140553252ull);
    vlSelf->milan_datapath__DOT__pp_amap_edit_data_w = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 17714671286737184739ull);
    vlSelf->milan_datapath__DOT__pp_gsi_req_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 18062835306821771544ull);
    vlSelf->milan_datapath__DOT__pp_gsi_kind_w = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 11450309956641771612ull);
    vlSelf->milan_datapath__DOT__tkd_crfq_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 728874270301053323ull);
    vlSelf->milan_datapath__DOT__tkd_crf_pend_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13100405196424847648ull);
    vlSelf->milan_datapath__DOT__tkd_crf_p_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11091641088012514478ull);
    vlSelf->milan_datapath__DOT__tkd_streaming_w = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 7503956593502142891ull);
    vlSelf->milan_datapath__DOT__tkd_crflk_q_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1889448120179409672ull);
    vlSelf->milan_datapath__DOT__mcr_streaming_w = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 12566178896326354513ull);
    vlSelf->milan_datapath__DOT__mcr_mr_v_w = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 10642544374476583564ull);
    vlSelf->milan_datapath__DOT____Vcellinp__media_clock_restart__frame_mr_i = 0;
    vlSelf->milan_datapath__DOT____Vcellinp__media_clock_restart__frame_idx_i = 0;
    vlSelf->milan_datapath__DOT____Vcellinp__media_clock_restart__frame_p_i = 0;
    VL_SCOPED_RAND_RESET_W(128, vlSelf->milan_datapath__DOT__pp_aecp_fmt_in_w, __VscopeHash, 12355869383489277935ull);
    VL_SCOPED_RAND_RESET_W(128, vlSelf->milan_datapath__DOT__pp_aecp_fmt_out_w, __VscopeHash, 11416757532938221936ull);
    vlSelf->milan_datapath__DOT__ctrq_type_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 3894347103673530085ull);
    vlSelf->milan_datapath__DOT__ctrq_index_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 10558652490352130186ull);
    vlSelf->milan_datapath__DOT__ctrq_word_r = VL_SCOPED_RAND_RESET_I(6, __VscopeHash, 1142233535940584811ull);
    vlSelf->milan_datapath__DOT__ctr_srv1_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10161774526133219023ull);
    vlSelf->milan_datapath__DOT__ctr_srv2_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1043713360515298127ull);
    vlSelf->milan_datapath__DOT__ctr_data_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 13261292619891962317ull);
    vlSelf->milan_datapath__DOT__ctr_sel_match_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3891290705942723830ull);
    vlSelf->milan_datapath__DOT__ctr_sin_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12022672356776944007ull);
    vlSelf->milan_datapath__DOT__ctr_link_q_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9680737439694076771ull);
    vlSelf->milan_datapath__DOT__ctr_mclk_q_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7149543142884456606ull);
    vlSelf->milan_datapath__DOT__ctr_avb_link_edge_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14388524729868392528ull);
    vlSelf->milan_datapath__DOT__ctr_ckd_lock_edge_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9396910019921335864ull);
    vlSelf->milan_datapath__DOT__ctr_linkup_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 18077557426963547912ull);
    vlSelf->milan_datapath__DOT__ctr_linkdn_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 3207007532840614764ull);
    vlSelf->milan_datapath__DOT__ctr_gmchg_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 7093554526290473953ull);
    vlSelf->milan_datapath__DOT__ctr_mlock_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 1109613923927317197ull);
    vlSelf->milan_datapath__DOT__ctr_munlock_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 3508050122740908397ull);
    vlSelf->milan_datapath__DOT__amap_in_store_r = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 1255239124146240105ull);
    vlSelf->milan_datapath__DOT__amapq_type_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 15626825772505118760ull);
    vlSelf->milan_datapath__DOT__amapq_index_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 7840493193137406627ull);
    vlSelf->milan_datapath__DOT__amapq_map_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 3384220462263366845ull);
    vlSelf->milan_datapath__DOT__amapq_sel_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 9173014902519146410ull);
    vlSelf->milan_datapath__DOT__amapq_rec_r = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 10574979630866570041ull);
    vlSelf->milan_datapath__DOT__amap_data_r = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 10261322723203262105ull);
    vlSelf->milan_datapath__DOT__amap_sel_match_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4192138190063759488ull);
    vlSelf->milan_datapath__DOT__amap_walk_j_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 10535722630523507478ull);
    vlSelf->milan_datapath__DOT__amap_walk_jq_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 3758992334206302273ull);
    vlSelf->milan_datapath__DOT__amap_stageb_v_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14575829069785467513ull);
    vlSelf->milan_datapath__DOT__amap_in_ent_q_r = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 6518650173126285366ull);
    vlSelf->milan_datapath__DOT__amap_out_owner_v_q_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 557667772530177929ull);
    vlSelf->milan_datapath__DOT__amap_out_owner_q_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 243664845874841789ull);
    vlSelf->milan_datapath__DOT__amap_out_cluster_q_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 423377588594376082ull);
    vlSelf->milan_datapath__DOT__amap_done_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13946896696214156585ull);
    vlSelf->milan_datapath__DOT__amap_seen_r = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 5398611613871710028ull);
    vlSelf->milan_datapath__DOT__amap_cnt_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 9641217679674261942ull);
    vlSelf->milan_datapath__DOT__amap_rec_r2 = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 13641441681989286668ull);
    vlSelf->milan_datapath__DOT__amap_in_ent_w = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 14793559406320826905ull);
    vlSelf->milan_datapath__DOT__amap_spo_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12783048306606164769ull);
    vlSelf->milan_datapath__DOT__amap_srv_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11777780524568823805ull);
    vlSelf->milan_datapath__DOT__amap_spi_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2486090019177844942ull);
    vlSelf->milan_datapath__DOT__amap_page_ok_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16200003105209591538ull);
    vlSelf->milan_datapath__DOT__amap_in_rec_w = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 8811612234311503441ull);
    vlSelf->milan_datapath__DOT__amap_opage_ok_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12501577408727626168ull);
    vlSelf->milan_datapath__DOT__amap_out_hit_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10680374718028881347ull);
    vlSelf->milan_datapath__DOT__amap_out_rec_w = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 440406151933965237ull);
    vlSelf->milan_datapath__DOT__amap_edit_seen_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7670343294583411917ull);
    vlSelf->milan_datapath__DOT__amap_edit_seen_phase_r = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 10456896258567884038ull);
    vlSelf->milan_datapath__DOT__amap_edit_seen_rec_r = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 8705827995010072769ull);
    vlSelf->milan_datapath__DOT__amap_edit_remove_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10426841880937965032ull);
    vlSelf->milan_datapath__DOT__amap_edit_type_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 11843001038095087057ull);
    vlSelf->milan_datapath__DOT__amap_edit_index_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 17696887278009422436ull);
    vlSelf->milan_datapath__DOT__amap_edit_count_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 9264157733308669981ull);
    vlSelf->milan_datapath__DOT__amap_edit_changed_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4498829176295110224ull);
    vlSelf->milan_datapath__DOT__amap_edit_iclaim_v_r = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 17110788249340285809ull);
    vlSelf->milan_datapath__DOT__amap_edit_iclaim_word_r = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 6440927659625804577ull);
    vlSelf->milan_datapath__DOT__amap_edit_iclaim_expect_r = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 8532018973115998191ull);
    vlSelf->milan_datapath__DOT__amap_edit_oclaim_v_r = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 5925099072362103388ull);
    VL_SCOPED_RAND_RESET_W(104, vlSelf->milan_datapath__DOT__amap_edit_oclaim_word_r, __VscopeHash, 11908643340256746726ull);
    VL_SCOPED_RAND_RESET_W(104, vlSelf->milan_datapath__DOT__amap_edit_oclaim_expect_r, __VscopeHash, 15703789682207972415ull);
    VL_SCOPED_RAND_RESET_W(128, vlSelf->milan_datapath__DOT__amap_edit_oclaim_cluster_r, __VscopeHash, 306975278792067905ull);
    vlSelf->milan_datapath__DOT__amap_edit_context_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7925135874158532657ull);
    vlSelf->milan_datapath__DOT__amap_edit_dynamic_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12335764079813741676ull);
    vlSelf->milan_datapath__DOT__amap_edit_commit_ok_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12881657596796736442ull);
    vlSelf->milan_datapath__DOT__amap_edit_accept_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7711761482288752291ull);
    vlSelf->milan_datapath__DOT__amap_edit_in_key_v_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 726654650802639319ull);
    vlSelf->milan_datapath__DOT__amap_edit_out_key_v_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5846739257091494223ull);
    vlSelf->milan_datapath__DOT__amap_edit_in_key_w = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 6556012038098788937ull);
    vlSelf->milan_datapath__DOT__amap_edit_out_key_w = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 15282441741056954138ull);
    vlSelf->milan_datapath__DOT__amap_edit_in_word_w = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 15179277182671967327ull);
    vlSelf->milan_datapath__DOT__amap_edit_in_live_w = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 13419611525826535199ull);
    vlSelf->milan_datapath__DOT__amap_edit_out_word_w = VL_SCOPED_RAND_RESET_I(13, __VscopeHash, 15600867103479625348ull);
    vlSelf->milan_datapath__DOT__amap_edit_out_live_w = VL_SCOPED_RAND_RESET_I(13, __VscopeHash, 6605434877211051672ull);
    vlSelf->milan_datapath__DOT__amap_edit_out_owner_v_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2387040985925930684ull);
    vlSelf->milan_datapath__DOT__amap_edit_out_owner_w = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 217015895686596189ull);
    vlSelf->milan_datapath__DOT__amap_edit_out_cluster_w = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 9263566162425744301ull);
    vlSelf->milan_datapath__DOT__cfg_cmap_entry_w = VL_SCOPED_RAND_RESET_I(13, __VscopeHash, 17294851892396911006ull);
    vlSelf->milan_datapath__DOT__cfg_cmap_cluster_w = VL_SCOPED_RAND_RESET_I(17, __VscopeHash, 3288548447120301978ull);
    vlSelf->milan_datapath__DOT__gsiq_kind_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 5823305694760005098ull);
    vlSelf->milan_datapath__DOT__gsiq_type_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 16433194145238780839ull);
    vlSelf->milan_datapath__DOT__gsiq_index_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 5063531609001291678ull);
    vlSelf->milan_datapath__DOT__gsiq_sel_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 1779357990937880306ull);
    vlSelf->milan_datapath__DOT__gsiq_ord_r = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 17622276979861265518ull);
    vlSelf->milan_datapath__DOT__gsi_srv1_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3434475990161064122ull);
    vlSelf->milan_datapath__DOT__gsi_srv2_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8782560122634135266ull);
    vlSelf->milan_datapath__DOT__gsi_data_r = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 1646595863757426857ull);
    vlSelf->milan_datapath__DOT__gsi_req_q_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9572557851554521487ull);
    vlSelf->milan_datapath__DOT__asp_resp_gm_r = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 2158197486988188180ull);
    vlSelf->milan_datapath__DOT__asp_resp_count_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 719150708060474902ull);
    VL_SCOPED_RAND_RESET_W(448, vlSelf->milan_datapath__DOT__asp_resp_path_r, __VscopeHash, 13277439380891986845ull);
    vlSelf->milan_datapath__DOT__gsi_gm_snap_r = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 11424349881594171734ull);
    vlSelf->milan_datapath__DOT__gsi_pdelay_snap_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 10142423414970270225ull);
    vlSelf->milan_datapath__DOT__gsi_domain_snap_r = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 13399983501459726245ull);
    vlSelf->milan_datapath__DOT__gsi_link_snap_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16405669562354580261ull);
    vlSelf->milan_datapath__DOT__gsi_ascap_snap_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12286346392219772459ull);
    vlSelf->milan_datapath__DOT__gsi_prio_snap_r = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 10856348787218144903ull);
    vlSelf->milan_datapath__DOT__gsi_vid_snap_r = VL_SCOPED_RAND_RESET_I(12, __VscopeHash, 5685539066398892841ull);
    vlSelf->milan_datapath__DOT__asp_resp_capture_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14661384024793326258ull);
    vlSelf->milan_datapath__DOT__gsi_avb_capture_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14545429828818641991ull);
    vlSelf->milan_datapath__DOT__asp_resp_entry_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3174500233908671250ull);
    vlSelf->milan_datapath__DOT__gsi_sel_match_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15716671164134767971ull);
    vlSelf->milan_datapath__DOT__gsi_in_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6404789387266032789ull);
    vlSelf->milan_datapath__DOT__gsi_out_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11938994987405139498ull);
    vlSelf->milan_datapath__DOT__gsi_bnd_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8898131703366308637ull);
    vlSelf->milan_datapath__DOT__gsi_sid_w = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 13395814034346769972ull);
    vlSelf->milan_datapath__DOT__gsi_setl_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2623957437631189862ull);
    vlSelf->milan_datapath__DOT__gsi_tkreg_w = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 13446569234307603499ull);
    vlSelf->milan_datapath__DOT__gsi_tkfail_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7028627330326983081ull);
    vlSelf->milan_datapath__DOT__gsi_reging_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9485659663002491062ull);
    vlSelf->milan_datapath__DOT__gsi_decl_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7563394530596522996ull);
    vlSelf->milan_datapath__DOT__gsi_lreg_w = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 15911954409082403002ull);
    vlSelf->milan_datapath__DOT__gsi_ofail_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14407705396851747872ull);
    vlSelf->milan_datapath__DOT__gsi_flags_w = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 16765484216519308790ull);
    vlSelf->milan_datapath__DOT__gsi_flags_ex_w = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 8107107774959549126ull);
    vlSelf->milan_datapath__DOT__pp_aecp_strm_started_w = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 1518435321541443499ull);
    vlSelf->milan_datapath__DOT__sfv_decl_w = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 883986434961593543ull);
    vlSelf->milan_datapath__DOT__sfv_base_ok_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7220660182147438483ull);
    vlSelf->milan_datapath__DOT__sfv_crf_row_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2962208371293520897ull);
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->milan_datapath__DOT__sfv_need_in_r[__Vi0] = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 8931571398152012951ull);
    }
    vlSelf->milan_datapath__DOT__sfv_need_out_w = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 3961518357866943469ull);
    vlSelf->milan_datapath__DOT__sfv_cur_r = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 12197544526860498864ull);
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->milan_datapath__DOT__sfv_acc_r[__Vi0] = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 3847739349997189034ull);
    }
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->milan_datapath__DOT__sfv_nxt_w[__Vi0] = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 15979709815664622264ull);
    }
    vlSelf->milan_datapath__DOT__asp_served_entry_w = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 14658675197634114609ull);
    vlSelf->milan_datapath__DOT__gsi_ascap_q_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10933365498989783642ull);
    vlSelf->milan_datapath__DOT__gsi_asp_gm_q_r = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 14359800275768171852ull);
    vlSelf->milan_datapath__DOT__gsi_asp_count_q_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 11449653859523643840ull);
    VL_SCOPED_RAND_RESET_W(448, vlSelf->milan_datapath__DOT__gsi_asp_path_q_r, __VscopeHash, 77172286780275183ull);
    vlSelf->milan_datapath__DOT__gsi_snap_v_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5193550633235680563ull);
    vlSelf->milan_datapath__DOT__gsi_gm_q_r = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 9469101997342550915ull);
    vlSelf->milan_datapath__DOT__gsi_pdly_q_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 10595260228537184060ull);
    vlSelf->milan_datapath__DOT__gsi_dom_q_r = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 15603722483629099812ull);
    vlSelf->milan_datapath__DOT__acmpl_stopped_v_w = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 1824913209965234019ull);
    vlSelf->milan_datapath__DOT__strtbl_sid_w = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 2197151249041805420ull);
    vlSelf->milan_datapath__DOT__strtbl_en_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2415354827475649420ull);
    vlSelf->milan_datapath__DOT__strtbl_bind_rise_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10631870050422074585ull);
    vlSelf->milan_datapath__DOT__strtbl_bind_fall_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14150543403560105222ull);
    vlSelf->milan_datapath__DOT__avtprx_idx = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7253558521628751539ull);
    vlSelf->milan_datapath__DOT__wing_sid_lo_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 6822039806007354170ull);
    vlSelf->milan_datapath__DOT__wing_sid_hi_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 7561302499200290245ull);
    vlSelf->milan_datapath__DOT__wing_tbl_we_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2522355131957675015ull);
    vlSelf->milan_datapath__DOT__wing_route_we_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9896004326696419040ull);
    vlSelf->milan_datapath__DOT__wing_idx_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 13371789636650930020ull);
    vlSelf->milan_datapath__DOT__wing_sid_r = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 13282963973772837908ull);
    vlSelf->milan_datapath__DOT__wing_en_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4096128156033715318ull);
    vlSelf->milan_datapath__DOT__wing_route_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 16829449398551260536ull);
    vlSelf->milan_datapath__DOT__wing_stg_idx_r = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 12651530673605954376ull);
    vlSelf->milan_datapath__DOT__wing_stg_vld_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13673431677608847409ull);
    vlSelf->milan_datapath__DOT__wing_stg_hit_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6617029147642252770ull);
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->milan_datapath__DOT__tctx_chans_r[__Vi0] = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 8350233718241234744ull);
    }
    vlSelf->milan_datapath__DOT__tctx_w0_wr_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4469228481413523085ull);
    vlSelf->milan_datapath__DOT__crft_pcp_w = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 10704422739492881895ull);
    vlSelf->milan_datapath__DOT__crft_vid_w = VL_SCOPED_RAND_RESET_I(12, __VscopeHash, 7050275627992907917ull);
    vlSelf->milan_datapath__DOT__crft_emit_en_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2512226048138812415ull);
    vlSelf->milan_datapath__DOT____Vcellinp__crf_rx__en_i = 0;
    vlSelf->milan_datapath__DOT__mga_engaged_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13863951519403898406ull);
    vlSelf->milan_datapath__DOT__mga_err_w = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 4472711476643246838ull);
    vlSelf->milan_datapath__DOT____Vcellinp__crf_tx__transit_ns_i = 0;
    vlSelf->milan_datapath__DOT__mon_wire_chans_w = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 14997162187788332156ull);
    vlSelf->milan_datapath__DOT__mon_wire_chans_all_w = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 1579744739283457856ull);
    vlSelf->milan_datapath__DOT__avtprx_accept_p_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3677133579513647104ull);
    vlSelf->milan_datapath__DOT__avtprx_accept_idx_w = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 1414169440209116727ull);
    vlSelf->milan_datapath__DOT__pcmrx_pdu_p_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11547547182200947428ull);
    vlSelf->milan_datapath__DOT__pcmrx_pdu_idx_w = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 8145486983957448768ull);
    vlSelf->milan_datapath__DOT__avtprx_stopped_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8099007440205114961ull);
    vlSelf->milan_datapath__DOT__dpkt_pcm_tdata_w = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 8554004855514103865ull);
    vlSelf->milan_datapath__DOT__dpkt_pcm_tlast_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16695059841158857999ull);
    vlSelf->milan_datapath__DOT__rend_pcm_tvalid_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14431392197082314153ull);
    vlSelf->milan_datapath__DOT__gm_recentre_q_r = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 12046789076708284443ull);
    vlSelf->milan_datapath__DOT__gm_recentre_p_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1586585723982194471ull);
    vlSelf->milan_datapath__DOT__src_recentre_q_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 6776162385908515351ull);
    vlSelf->milan_datapath__DOT__src_pend_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11414183050501992239ull);
    vlSelf->milan_datapath__DOT__mga_engaged_q_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9791088104757586881ull);
    vlSelf->milan_datapath__DOT__src_band_ticks_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 16910540585762524580ull);
    vlSelf->milan_datapath__DOT__src_eng_ticks_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 5426197812741892292ull);
    vlSelf->milan_datapath__DOT__src_recentre_p_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5932710427866436610ull);
    vlSelf->milan_datapath__DOT__render_recentre_p_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16773427805761901566ull);
    VL_SCOPED_RAND_RESET_W(240, vlSelf->milan_datapath__DOT__chmap_phys_w, __VscopeHash, 3677016458347152428ull);
    vlSelf->milan_datapath__DOT__chmap_phys_v_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1999757154879253284ull);
    vlSelf->milan_datapath__DOT__rsp_tdata_w = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 9512959067186274422ull);
    vlSelf->milan_datapath__DOT__rsp_tvalid_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1825958150064481536ull);
    vlSelf->milan_datapath__DOT__rsp_tlast_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14500393541406041796ull);
    vlSelf->milan_datapath__DOT__rsp_tuser_w = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 9769119338917292051ull);
    vlSelf->milan_datapath__DOT__rsp_render_tick_p_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11711293304943277410ull);
    vlSelf->milan_datapath__DOT__rsp_pop_p_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3744351886559970922ull);
    vlSelf->milan_datapath__DOT__rsp_fill_w = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 1896466446547107985ull);
    vlSelf->milan_datapath__DOT__rsp_prefill_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1703575120057341794ull);
    vlSelf->milan_datapath__DOT__rsp_converged_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6700995962345312978ull);
    vlSelf->milan_datapath__DOT__rsp_underruns_w = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 18066894388102195590ull);
    vlSelf->milan_datapath__DOT__rsp_overruns_w = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 17016576162597131653ull);
    vlSelf->milan_datapath__DOT__rsp_rails_w = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 14368254377693409659ull);
    vlSelf->milan_datapath__DOT__rsp_recentres_w = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 1374485331205783326ull);
    VL_SCOPED_RAND_RESET_W(80, vlSelf->milan_datapath__DOT__rmap_flat_w, __VscopeHash, 10034405863292592644ull);
    vlSelf->milan_datapath__DOT____Vcellinp__chan_map_render__map_wr_data_i = 0;
    vlSelf->milan_datapath__DOT____Vcellinp__chan_map_render__map_wr_addr_i = 0;
    vlSelf->milan_datapath__DOT____Vcellinp__chan_map_render__map_wr_en_i = 0;
    vlSelf->milan_datapath__DOT__tdmr_frames_w = 0U;
    ;
    vlSelf->milan_datapath__DOT__tdmr_underruns_w = 0U;
    ;
    vlSelf->milan_datapath__DOT__tdmr_skips_w = 0U;
    ;
    vlSelf->milan_datapath__DOT__tdmr_overruns_w = 0U;
    ;
    vlSelf->milan_datapath__DOT__tdmr_epochs_w = 0U;
    ;
    vlSelf->milan_datapath__DOT__tdmr_commit_en_w = 0U;
    ;
    vlSelf->milan_datapath__DOT__tdmr_commit_p_w = 0U;
    ;
    vlSelf->milan_datapath__DOT__tdmr_frame_p_w = 0U;
    ;
    vlSelf->milan_datapath__DOT__tdmr_adopt_p_w = 0U;
    ;
    vlSelf->milan_datapath__DOT__tdmr_lane_streams_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12223830203103223114ull);
    vlSelf->milan_datapath__DOT__ctlh_tx_tvalid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14372429060308740682ull);
    vlSelf->milan_datapath__DOT__ctlh_tx_tlast = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12742594518137470220ull);
    vlSelf->milan_datapath__DOT__ctlh_tx_tready = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11453844930191532468ull);
    vlSelf->milan_datapath__DOT____Vcellout__ctl_tx_mux__stall_evt_o = 0;
    vlSelf->milan_datapath__DOT____Vcellout__ctl_tx_mux__abort_evt_o = 0;
    vlSelf->milan_datapath__DOT__dpcrf_tvalid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2972672093548872413ull);
    vlSelf->milan_datapath__DOT__dpcrf_tlast = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3910787324050117696ull);
    vlSelf->milan_datapath__DOT__dpcrf_tready = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1390320617332859170ull);
    vlSelf->milan_datapath__DOT____Vcellout__crf_dp_mux__stall_evt_o = 0;
    vlSelf->milan_datapath__DOT____Vcellout__crf_dp_mux__abort_evt_o = 0;
    vlSelf->milan_datapath__DOT____Vcellout__adp_tx_mux__stall_evt_o = 0;
    vlSelf->milan_datapath__DOT____Vcellout__adp_tx_mux__abort_evt_o = 0;
    vlSelf->milan_datapath__DOT__txarb_abort_sticky_r = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 12764547473306245297ull);
    vlSelf->milan_datapath__DOT__txarb_stall_sticky_r = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 13207794353983786697ull);
    vlSelf->milan_datapath__DOT__rx_mac_good_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9818600552637486117ull);
    vlSelf->milan_datapath__DOT__mac_events_w = VL_SCOPED_RAND_RESET_I(9, __VscopeHash, 6308855516434980455ull);
    vlSelf->milan_datapath__DOT__pp_gm_id_edge_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12038044921550914614ull);
    vlSelf->milan_datapath__DOT__pp_aecp_cur_config_w = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 10912267880493528187ull);
    vlSelf->milan_datapath__DOT__pp_aecp_identify_w = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 4017184080974419819ull);
    vlSelf->milan_datapath__DOT__pp_aecp_dyn_dirty_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5476199073262844021ull);
    vlSelf->milan_datapath__DOT__pp_ctr_sin_pend_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 15065455534121173835ull);
    vlSelf->milan_datapath__DOT__pp_ctr_sin_pend_n = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 1724577719514226146ull);
    vlSelf->milan_datapath__DOT__pp_ctr_sout_pend_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 1724146611903672800ull);
    vlSelf->milan_datapath__DOT__pp_ctr_sout_pend_n = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 9551050500356773293ull);
    vlSelf->milan_datapath__DOT__pp_ctr_avb_pend_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3707547087480179657ull);
    vlSelf->milan_datapath__DOT__pp_ctr_ckd_pend_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15309416833003450914ull);
    vlSelf->milan_datapath__DOT__pp_ctr_rr_r = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 893755760370202510ull);
    vlSelf->milan_datapath__DOT__pp_ctr_all_pend_w = VL_SCOPED_RAND_RESET_I(6, __VscopeHash, 11320399314666498699ull);
    vlSelf->milan_datapath__DOT__pp_ctr_evt_valid_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2479000443641794712ull);
    vlSelf->milan_datapath__DOT__pp_ctr_evt_type_w = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 12171123943342801133ull);
    vlSelf->milan_datapath__DOT__pp_ctr_evt_index_w = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 6983868374042519130ull);
    vlSelf->milan_datapath__DOT____Vcellinp__pp_shadow__enable_i = 0;
    vlSelf->milan_datapath__DOT__g_aprb__DOT__aprb_sid_r = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 18272509978141516235ull);
    vlSelf->milan_datapath__DOT__g_aprb__DOT__aprb_subtype_r = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 16100427104175377894ull);
    vlSelf->milan_datapath__DOT__g_aprb__DOT__aprb_hit_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9288296126996639556ull);
    vlSelf->milan_datapath__DOT__g_aprb__DOT__aprb_idx_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 8004492033824097461ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__beat_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11335715965522202082ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__da_num_w = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 6990155222696310832ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__etype_w = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 18245804717655855941ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__fw_S = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 11415137057556216801ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__da_r = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 13675895451625469190ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__fw_valid_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14670492449905130073ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__fw_last_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8192153576853626564ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__fw_user_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12284751155196331144ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__accept_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15912707743640024417ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__ser_data_r = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 14946965507260630192ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__ser_keep_r = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 5420356370323497117ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__ser_last_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7324287531995963638ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__ser_busy_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2526865762587411342ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__ser_idx_r = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 698442045121016314ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__pp_rx_data_w = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 9668164524548804052ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__nvm_req_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1919610435701381796ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__nvm_wvalid_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11273167605484043176ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__nvm_wready_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5179438218538329953ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__nvm_rvalid_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7853569127781022632ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__nvm_rready_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4405585384037853258ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__nvm_op_w = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 16245536738023461216ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__nvm_rdata_w = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 18162677272213862725ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__nvm_offset_w = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 2442059300379438578ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__nvm_len_w = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 14939489579482251692ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__restore_busy_q = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9797162708907601728ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__walk_blind_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6178043852613040557ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__aecp_mark_pend_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16944398307044898245ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__pp_tx_valid_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7868772050926810197ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__pp_tx_eof_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5112827557871383015ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__pp_host_rvalid_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3466878446843081049ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__pp_host_err_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3424209673779958270ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__hb_pend_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1711206540091935297ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__hb_we_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13043687077833923253ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__hb_addr_r = VL_SCOPED_RAND_RESET_I(20, __VscopeHash, 6713303344717506152ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__hb_wdata_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 7835282861654765450ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__txp_data_r = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 16569686755404946730ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__txp_keep_r = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 4346797733574294677ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__txp_valid_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11444927982600976289ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__txp_last_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10619234490094816375ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__txp_idx_r = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 18296906000889890279ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__pp_tx_ready_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4245581187309946582ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tmr_arm_valid_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3115154228229067025ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tmr_arm_cancel_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 18018875915129711883ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tmr_arm_slot_w = VL_SCOPED_RAND_RESET_I(6, __VscopeHash, 967932548133909146ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tmr_arm_owner_w = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 8142723597646162605ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tmr_arm_deadline_w = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 11378409838779202023ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__bound_hold_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 6545269287358637751ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__prng_req_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5798791225189308444ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__prng_kind_w = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 4966311637339827372ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__prng_valid_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17241661160458465140ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__prng_ms_w = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 7353095643735806281ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__sb_adm_req_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4334646797071606938ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__sb_gnt_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9484751873831786388ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__sb_adm_class_w = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 2159785533159146477ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__sb_adm_key_w = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 11920020328831821230ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__sb_rel_id_w = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 17580562858626670811ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__acmp_sb_active_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2120409788444811373ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__aecp_sb_active_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5573185691944675876ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__acmp_sb_done_pending_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3691443860113102010ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__aecp_sb_done_pending_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7361171627837451638ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__sb_prefer_aecp_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8602698369797876476ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__acmp_sb_id_r = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 6265110853551876771ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__aecp_sb_id_r = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 13254033403015146730ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__acmp_sb_slot_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 8337508001112725076ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__aecp_sb_slot_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 12838917188895511492ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__aecp_eng_ready_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13441326852708487917ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__trc_rd_en_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4506455345623959212ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__trc_rd_data_w = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 7397027231376658752ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__org_rt_valid_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7009253909237131022ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__org_fail_valid_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11191143101039435324ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__org_rt_owner_w = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 5838096524950269623ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__org_fail_owner_w = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 298478843339529835ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__org_send_valid_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10499169311769823398ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__org_resend_valid_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15263332605968173491ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__org_send_slot_w = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 7817997940047840021ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__org_resend_slot_w = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 2722004120983131638ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__org_hold_valid_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4399700253810833466ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__org_release_valid_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 99530236803920742ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__org_hold_slot_w = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 14268086533841423599ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__org_release_slot_w = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 17024728194668799025ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__org_arm_valid_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14712289689825755144ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__org_arm_cancel_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17515488489567239615ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__org_arm_slot_w = VL_SCOPED_RAND_RESET_I(6, __VscopeHash, 2054703924388611722ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__org_arm_owner_w = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 9724373714492360007ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__org_arm_deadline_w = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 14789241898475799582ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__ntfy_ca_cancel_valid_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5556021051841593584ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__ca_txs_alloc_req_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11943999667537206238ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__ca_txs_gnt_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 28224461945083855ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__ca_txs_wr_commit_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1267364668470542072ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__ca_txs_abort_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6400638579361136328ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__ca_txs_wr_data_w = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 6651258796753974955ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__ca_cancel_release_valid_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1622015714662333266ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__ca_cancel_release_slot_w = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 12483887864846884297ull);
    VL_ZERO_RESET_W(112, vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT____Vcellinp__u_originator__rsp_key_i);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__v_mrp_valid_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13580483000994362177ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__v_mrp_last_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9982387377778836063ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__v_alloc_gnt_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6013450565390597900ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxf_vld_r = VL_SCOPED_RAND_RESET_I(6, __VscopeHash, 9638950070870990126ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxf_slot_r = VL_SCOPED_RAND_RESET_I(12, __VscopeHash, 247387386245769367ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxf_drop_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 10974063080286254852ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxf_free_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5923980770866178823ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxf_free_slot_w = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 17377427892701209479ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxf_pick_ix_w = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 9414202327117806513ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxf_req_w = VL_SCOPED_RAND_RESET_I(6, __VscopeHash, 17298200486638200663ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxf_req_slot_w = VL_SCOPED_RAND_RESET_I(12, __VscopeHash, 15119405056909854440ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__lstn_rxs_free_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7201399433472663901ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__aecp_rxs_free_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13241824509182551377ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxp_rd_en_w__BRA__1__KET__ = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7207633893268395454ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxp_rd_data_w__BRA__7__03a0__KET__ = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 15455615619699421239ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__hdr_vld_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17824858331231063898ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__hdr_protocol_r = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 9966396051950249831ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__hdr_msg_type_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 11978806030416797557ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__hdr_status_r = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 7712447982483648723ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__hdr_cdl_r = VL_SCOPED_RAND_RESET_I(11, __VscopeHash, 477396249200880344ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__hdr_src_mac_r = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 11241286857460629021ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__hdr_ctlr_eid_r = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 9957591110498712661ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__hdr_target_eid_r = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 8124841385927753475ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__hdr_seq_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 13776970391114732803ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__hdr_opcode_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 18276926422083042570ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__hdr_u_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4902993632797534186ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__hdr_cr_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11020629558333397724ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__hdr_operands_r = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 16949583742756163589ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__hdr_rx_slot_r = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 723732028524196316ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__hdr_drop_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 5545762550174087262ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__nrm_txn_ready_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14124239166596383368ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__acmp_txn_ready_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1364266746992375102ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__aecp_txn_ready_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6425013779488493887ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__maap_txn_ready_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10789662841708868613ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__acmp_is_tkr_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4642987442325006573ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__lstn_txn_ready_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7385394363723212347ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pf_st_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 13550147098069565909ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pf_idx_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 3247415030212773229ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pf_eid_r = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 14197455690655127813ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__bound_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 14703488193264239943ull);
    VL_SCOPED_RAND_RESET_W(128, vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__bound_sid_r, __VscopeHash, 10370664867901619110ull);
    VL_SCOPED_RAND_RESET_W(96, vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__bound_dmac_r, __VscopeHash, 15155475482555870812ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__bound_vlan_r = VL_SCOPED_RAND_RESET_I(24, __VscopeHash, 14850578640550461420ull);
    VL_SCOPED_RAND_RESET_W(128, vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__bound_eid_r, __VscopeHash, 5150913884257583030ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__lstn_disc_arm_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9975646837590949935ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__lstn_disc_disarm_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15993457824520887241ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__lstn_disc_eid_w = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 7849322230610433438ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__adp_prng_busy_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13250832616365925707ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__adp_prng_valid_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4473909615546843697ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__adp_arm_valid_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9018679536921433398ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__adp_arm_cancel_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7631892133843170367ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__adp_arm_slot_w = VL_SCOPED_RAND_RESET_I(6, __VscopeHash, 179123173735158203ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__adp_arm_deadline_w = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 12718711247006988536ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__adp_txs_wr_data_w = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 1407146794402012057ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__adp_evt_valid_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 18039737927452582034ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__adp_evt_departed_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13442225035814250667ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__adp_evt_sink_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9277993788149285328ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__lstn_evt_tk_valid_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17321850829327965304ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__lstn_evt_tk_ready_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16812285484297431758ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__lstn_arm_valid_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5139656715549396461ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__lstn_arm_cancel_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9189751764383133056ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__lstn_arm_slot_w = VL_SCOPED_RAND_RESET_I(6, __VscopeHash, 4525115448880647529ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__lstn_arm_owner_w = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 6211875787569486337ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__lstn_arm_deadline_w = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 12529630760261740755ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__lstn_draw_req_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5001865462715566947ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__lstn_txs_alloc_req_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16606315037782380065ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__lstn_txs_wr_addr_w = VL_SCOPED_RAND_RESET_I(11, __VscopeHash, 16165905717588944171ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__lstn_txs_wr_len_w = VL_SCOPED_RAND_RESET_I(11, __VscopeHash, 6558403390170060291ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__lstn_txs_wr_valid_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11771744323498351722ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__lstn_txs_wr_commit_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6912881536695526728ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__lstn_txs_wr_data_w = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 3111057887812961585ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__lstn_txreq_valid_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9747428166678921803ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__lstn_act_settle_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11681524507090599894ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__lstn_act_teardown_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1969600862021325140ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__strm_set_valid_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4403719927909218019ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__lstn_act_strt_chg_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17307270827276590102ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__lstn_act_strt_cmd_chg_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 865423727685326593ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT____Vcellinp__u_listener__txn_valid_i = 0;
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_resp_valid_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16047092527325077515ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_resp_status_w = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 707631203838944826ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_resp_sid_w = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 8224409023518870563ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_resp_lseid_w = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 4336791979015597417ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_resp_lsuid_w = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 14562670019572507712ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_resp_flags_w = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 7226059732318404003ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_resp_vlan_w = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 9665405105526735648ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_resp_da_w = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 10430267684701007835ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_gate_open_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12159288737577971909ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_gate_close_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15578281849218842974ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_gate_src_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16704210463527021509ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_gate_sid_w = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 10300605902008383670ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_gate_da_w = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 15610658784898929861ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_gate_vlan_w = VL_SCOPED_RAND_RESET_I(12, __VscopeHash, 17908807652869375402ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkr_arm_valid_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4713371175243950406ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_tk_decl_state_w = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 7259763527353316648ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_tk_reg_state_w = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 10560241570247532285ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_snk_fail_code_w = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 10451502134189566144ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_evt_domain_change_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10046981696458974486ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__maapeng_txs_wr_data_w = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 2762266966500543721ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__mrp_drop_w = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 17242230948297360514ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_req_valid_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5972041892399683816ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_rsp_valid_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5485062623878177882ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_txs_alloc_req_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10837363647436506939ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_arm_valid_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8667575670673903041ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_arm_cancel_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13147987511356332547ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_arm_slot_w = VL_SCOPED_RAND_RESET_I(6, __VscopeHash, 13736052980659770005ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_arm_owner_w = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 16087611702636813090ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_arm_deadline_w = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 6817374007624880447ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_draw_req_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15529077561766487776ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_evt_tk_reg_w = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 8774034674918987937ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_evt_tk_unreg_w = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 4005835368922217854ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_lstn_reg_change_w = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 8933249590998212211ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_txs_gnt_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4490734891910452015ull);
    VL_SCOPED_RAND_RESET_W(154, vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__st_tk_r, __VscopeHash, 7183744385761318804ull);
    VL_SCOPED_RAND_RESET_W(154, vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__st_ls_r, __VscopeHash, 5466148413669313406ull);
    VL_SCOPED_RAND_RESET_W(154, vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__st_svc_r, __VscopeHash, 7190331711056238031ull);
    VL_SCOPED_RAND_RESET_W(154, vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__inflight_r, __VscopeHash, 2966344965059216662ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__st_tk_vld_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16956863959633473010ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__st_ls_vld_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12146475668403228593ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__st_svc_vld_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6385558034233109900ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__inflight_vld_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11935080949780293469ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__svc_drop_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 9509614461728593887ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__nvm_req_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9173388679007153456ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__nvm_we_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8994789151327126097ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__nvm_record_id_w = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 10260811003988352987ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__nvm_wdata_w = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 3625210434172270128ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__nvm_rdata_w = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 2374345599362818375ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__nvm_busy_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6148374358257911950ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__nvm_done_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4738621211570545491ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__nvm_err_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3973384264252538538ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_vld_w = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 3156445826820471240ull);
    VL_SCOPED_RAND_RESET_W(376, vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_in_w, __VscopeHash, 4602733885342359712ull);
    VL_SCOPED_RAND_RESET_W(1504, vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r, __VscopeHash, 15303496700941232401ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_cnt_r = VL_SCOPED_RAND_RESET_I(24, __VscopeHash, 11556239628239234644ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__arm_drop_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 1579793768365815925ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_pop_w = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 3791348258180231608ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_mid_w = VL_SCOPED_RAND_RESET_I(24, __VscopeHash, 16296286120610203935ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_push_ok_w = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 3600911829691863316ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pr_pend_r = VL_SCOPED_RAND_RESET_I(6, __VscopeHash, 5236376247475252363ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pr_kind_r = VL_SCOPED_RAND_RESET_I(18, __VscopeHash, 3957284358403855524ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pr_inflight_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3662520298169315179ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pr_owner_r = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 7892264514419060718ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pr_req_w = VL_SCOPED_RAND_RESET_I(6, __VscopeHash, 10127640134968572491ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pr_kind_w = VL_SCOPED_RAND_RESET_I(18, __VscopeHash, 17701365435278697495ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__evr_strobe_w = VL_SCOPED_RAND_RESET_I(11, __VscopeHash, 4392990147666484522ull);
    VL_SCOPED_RAND_RESET_W(176, vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__evr_payload_w, __VscopeHash, 12642060929166372206ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__evr_pay_w = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 17935022543013750508ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__link_q_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3285042822689750262ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_st_r = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 9525403127660807734ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_pend_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17722618208625621728ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_msg_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 16137403584291340915ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_status_r = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 12990894273541236116ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_sid_r = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 2259653861796460083ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_ctlr_r = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 17941903720925260234ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_tkeid_r = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 14772516094264116760ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_lseid_r = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 7355696644033682096ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_tkuid_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 971815592997729481ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_lsuid_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 18440263447406448114ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_cc_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 13469120272903413016ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_seq_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 18092501727297728262ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_flags_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 7148322414895500435ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_vlan_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 5385821074747790027ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_da_r = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 6957800301488721519ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_drop_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 6345232014089535598ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_slot_r = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 12569700740356418558ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_bidx_r = VL_SCOPED_RAND_RESET_I(6, __VscopeHash, 3479076522770017583ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_lane_valid_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6042329051567625508ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_pdu_byte_w = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 12759973847005266325ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__aecp_rgy_req_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1173435447611731242ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__aecp_rgy_op_w = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 5113803051651573926ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__ntfy_amap_busy_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12058194521477147614ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__ntfy_arm_valid_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13049015166752248915ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__ntfy_arm_cancel_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16108542450683768937ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__ntfy_arm_slot_w = VL_SCOPED_RAND_RESET_I(6, __VscopeHash, 6496201849859996122ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__ntfy_arm_owner_w = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 15442901053035315411ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__ntfy_arm_deadline_w = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 12955816816112701019ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__ntfy_mon_arm_valid_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7807348067287903586ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__ntfy_mon_arm_cancel_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1152990201399384327ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__ntfy_mon_arm_slot_w = VL_SCOPED_RAND_RESET_I(6, __VscopeHash, 7769333700913927306ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__ntfy_mon_arm_owner_w = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 14237901759465292564ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__ntfy_mon_arm_deadline_w = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 17964179998015100246ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__ntfy_prng_req_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15557554501031994688ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__ntfy_stri_in_w = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 8485600947861182253ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__ntfy_stri_out_w = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 6013198282379379367ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__aecp_eff_notify_stb_nc_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10572438372340366943ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__aecp_eff_notify_arg0_w = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 15318252728324998255ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__aecp_eff_notify_arg1_w = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 7849428708125928925ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__acmp_sb_candidate_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12783406761159960554ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__aecp_sb_candidate_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9570549489088410566ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__sb_pick_aecp_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3923866930700032993ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__acmp_sb_accept_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5043364615272097364ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__aecp_sb_accept_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9789958896332503002ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__acmp_sb_done_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15628604926013641350ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__aecp_sb_done_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16629999815878973382ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__sb_rel_acmp_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2405165190613971575ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__sb_rel_aecp_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4790094222366193839ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT____Vcellinp__u_aecp__txn_valid_i = 0;
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT____Vcellinp__u_notify__rx_cmd_valid_i = 0;
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT____Vcellinp__u_notify__ev_amap_i = 0;
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__txc_req_w = VL_SCOPED_RAND_RESET_I(7, __VscopeHash, 2184887038066193998ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__txc_pend_r = VL_SCOPED_RAND_RESET_I(7, __VscopeHash, 11414844095953149836ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__txc_owner_r = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 4769041421195985895ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__txc_locked_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12464385182424448672ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__txc_alloc_wait_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1624313751972868273ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pool_alloc_req_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7817894360300348293ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pool_oversize_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15155167350443539989ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pool_wr_valid_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3365130363760920632ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pool_wr_slot_w = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 12816128027010120927ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pool_wr_addr_w = VL_SCOPED_RAND_RESET_I(11, __VscopeHash, 13589089623787286584ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pool_wr_len_w = VL_SCOPED_RAND_RESET_I(11, __VscopeHash, 1304055107715902835ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pool_wr_data_w = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 8700088757390031753ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__txs_free_w = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 17455114318872481596ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_adp_r = VL_SCOPED_RAND_RESET_I(24, __VscopeHash, 15194614050221451391ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_acmp_r = VL_SCOPED_RAND_RESET_I(24, __VscopeHash, 3016697387037525698ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_org_r = VL_SCOPED_RAND_RESET_I(24, __VscopeHash, 13382728349271939459ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_org_next_w = VL_SCOPED_RAND_RESET_I(24, __VscopeHash, 9792454272596708743ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_adp_cnt_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 17802582666335978428ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_acmp_cnt_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 17468701727639436295ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_org_cnt_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 8447923705880276185ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_adp_mid_w = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 13260468694899162488ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_acmp_mid_w = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 7783282173515440885ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_org_next_cnt_w = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 17014959184440662385ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_adp_push_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 623581363340494773ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__laneq_acmp_push_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1068979646691831656ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__arb_req_w = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 380809787376595196ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__arb_slot_w = VL_SCOPED_RAND_RESET_I(24, __VscopeHash, 16872855617597267790ull);
    VL_SCOPED_RAND_RESET_W(128, vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__arb_gnt_cnt_w, __VscopeHash, 15489854352930273513ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__arb_tx_eof_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2840468687659100206ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__arb_tx_ready_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10067198503491254675ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__arb_start_abort_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12888623971611748413ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__sh_st_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 14882902137488229291ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__sh_need_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1639866174499493022ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__sh_idx_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 7668224281576065571ull);
    VL_SCOPED_RAND_RESET_W(112, vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__sh_hdr_w, __VscopeHash, 5327015086211025509ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__sp_img_rvalid_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3261949414438357981ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__sp_dbg_rvalid_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7750708670528753257ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__sp_snap_rdata_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 5065500884453057660ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__sp_snap_rvalid_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14858913387506697657ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__sp_ctrl_req_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10438599900318375508ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__sp_ctrl_rdata_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 13691432065375185835ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__sp_ctrl_rvalid_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7063396866195322754ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__sp_trace_rvalid_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5969265163311285489ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__ctrl_scratch_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 11454457929318258418ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT____Vcellout__g_rx_pool__BRA__1__KET____DOT__u_rx_slots__rd_data_o = 0;
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT____Vcellout__g_rx_pool__BRA__1__KET____DOT__u_rx_slots__alloc_gnt_o = 0;
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT____Vcellout__g_rx_pool__BRA__2__KET____DOT__u_rx_slots__rd_data_o = 0;
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT____Vcellout__g_rx_pool__BRA__2__KET____DOT__u_rx_slots__alloc_gnt_o = 0;
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT____Vcellout__g_rx_pool__BRA__4__KET____DOT__u_rx_slots__rd_data_o = 0;
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT____Vcellout__g_rx_pool__BRA__4__KET____DOT__u_rx_slots__alloc_gnt_o = 0;
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT____Vcellout__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__rd_data_o = 0;
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT____Vcellout__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__alloc_gnt_o = 0;
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_valid_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17678036661385398419ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_msrp_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 709688701445799633ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_attr_type_w = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 11021742854850438779ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_stream_id_w = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 9482258423241479060ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_da_w = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 10233257982808450783ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_vid_w = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 155605035780567756ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_mrp_event_w = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 3337535439679942752ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_fourpacked_w = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 9623978773465039528ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_priority_w = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 17170072405130719309ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_acc_latency_w = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 16911036155419824826ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_fail_code_w = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 8322638319461995258ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_class_id_w = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 9095458839972870102ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_evt_class_a_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5814610189370783322ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_la_msrp_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16744655175148502774ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dec_la_mvrp_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6538196639272405527ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__p_join_fsm_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17923578187193542894ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__p_periodic_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8531666111619014925ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__p_la_msrp_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14243966873726041620ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__p_la_mvrp_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3032710144179361277ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__enc_join_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 11528360981462973349ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__enc_la_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 3280284716072957745ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__vlan_user_valid_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9572583564175080184ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__vlan_ev_valid_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10121138296924981528ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__vlan_ev_ready_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 18271382043709015053ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tk_user_vid_w = VL_SCOPED_RAND_RESET_I(12, __VscopeHash, 14379427859758780876ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__ls_user_vid_w = VL_SCOPED_RAND_RESET_I(12, __VscopeHash, 15238031803431826205ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__vu_sel_ls_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7730553758566962127ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__vrr_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11481377354779351265ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__adm_req_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 4356167698627700824ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__adm_mfs_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 1608192971578916618ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__adm_mif_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 944870698846689604ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__adm_admitted_w = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 8713218604821944904ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__adm_round_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15484936994100663338ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__opt_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 18159546288095722855ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__opt_cnt_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 15460969545342947337ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__sr_adm_fsm_w = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 9908876323627282748ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tk_txop_done_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2957666504433890833ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tk_user_ready_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5155997378957050186ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tk_arm_v_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16983642162981535282ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tk_arm_cancel_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14706826675752006826ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tk_arm_slot_w = VL_SCOPED_RAND_RESET_I(6, __VscopeHash, 15498044988732499851ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tk_arm_owner_w = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 11907798380684619835ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tk_arm_dl_w = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 9425594196093676193ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 13475786015493673230ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_sid_r = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 12356438815835596796ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_da_r = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 6878426503318697402ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_vid_r = VL_SCOPED_RAND_RESET_I(12, __VscopeHash, 16722634393039224207ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_mfs_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 12197190552410519614ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_mif_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 18040465438907504988ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_open_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2092191379773014988ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__ls_txop_done_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17780862348392568088ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__ls_user_ready_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1881440595259553772ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__ls_arm_v_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13421786130616430681ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__ls_arm_cancel_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12376695708518012010ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__ls_arm_slot_w = VL_SCOPED_RAND_RESET_I(6, __VscopeHash, 4458021650600416046ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__ls_arm_owner_w = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 8241869662129926494ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__ls_arm_dl_w = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 12853656869955940637ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__enc_ev_valid_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 900298470388958864ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__enc_ev_app_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8792765898275932679ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__enc_ev_type_w = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 7539549850434402932ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__enc_ev_event_w = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 12732810124670482823ull);
    VL_SCOPED_RAND_RESET_W(272, vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__enc_ev_value_w, __VscopeHash, 13512893316813257716ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__svc_st_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 393100351356343217ull);
    for (int __Vi0 = 0; __Vi0 < 2; ++__Vi0) {
        for (int __Vi1 = 0; __Vi1 < 32; ++__Vi1) {
            vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tf_ram_r[__Vi0][__Vi1] = VL_SCOPED_RAND_RESET_Q(47, __VscopeHash, 17037273079048259837ull);
        }
    }
    for (int __Vi0 = 0; __Vi0 < 2; ++__Vi0) {
        vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tf_q_r[__Vi0] = VL_SCOPED_RAND_RESET_Q(47, __VscopeHash, 9564050279682951237ull);
    }
    for (int __Vi0 = 0; __Vi0 < 2; ++__Vi0) {
        vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tf_wptr_r[__Vi0] = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 3834280873747293813ull);
    }
    for (int __Vi0 = 0; __Vi0 < 2; ++__Vi0) {
        vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tf_rptr_r[__Vi0] = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 3880795776903249787ull);
    }
    for (int __Vi0 = 0; __Vi0 < 2; ++__Vi0) {
        vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tf_cnt_r[__Vi0] = VL_SCOPED_RAND_RESET_I(6, __VscopeHash, 17114690760995153419ull);
    }
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tf_push_w = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 12052883784196390229ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tf_pop_w = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 10484330840945629334ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tm_st_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5515749532884852422ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tm_sel_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17157712324311507766ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tm_rr_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17144685189449174072ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__init_done_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1128973856697096895ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__cad_pend_r = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 11072452104053947375ull);
    VL_SCOPED_RAND_RESET_W(160, vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__cad_dl_r, __VscopeHash, 6816276515208400397ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__need_draw_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 8503314974757677410ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dr_inflight_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4562230856233363455ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__dr_app_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12988781598287825654ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__rnd_act_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3840800516839286402ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__td_tk_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9929295967629327701ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__td_ls_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12330278702436916997ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__hw_full_q_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 18033640239408515441ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__cad_hit_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8195874423063622948ull);
    for (int __Vi0 = 0; __Vi0 < 12; ++__Vi0) {
        VL_SCOPED_RAND_RESET_W(285, vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__msrp_ram_r[__Vi0], __VscopeHash, 14056918038835086003ull);
    }
    for (int __Vi0 = 0; __Vi0 < 12; ++__Vi0) {
        vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__mvrp_ram_r[__Vi0] = VL_SCOPED_RAND_RESET_I(19, __VscopeHash, 16813024687784763617ull);
    }
    VL_SCOPED_RAND_RESET_W(285, vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__msrp_q_r, __VscopeHash, 1109732250556261575ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__mvrp_q_r = VL_SCOPED_RAND_RESET_I(19, __VscopeHash, 598687227284459097ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__cnt_msrp_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 5419988598945453793ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__cnt_mvrp_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 18127530336748381012ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__rd_idx_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 8268423061948921816ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__st_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 18160479083279591199ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__cur_app_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13885132404970058686ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__drain_n_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 1851521635976948985ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__slot_r = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 16132595712630899061ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__waddr_r = VL_SCOPED_RAND_RESET_I(11, __VscopeHash, 9591776442082378779ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__bidx_r = VL_SCOPED_RAND_RESET_I(6, __VscopeHash, 9448152296924709078ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__ll_addr_r = VL_SCOPED_RAND_RESET_I(11, __VscopeHash, 13368984851473221208ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__msg_open_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4309278063077408148ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__msg_type_r = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 1324781631926213242ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__first_vec_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8024637473852402375ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__close_for_pdu_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17076962123175950218ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_open_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15251760285963714322ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_type_r = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 9631612704272013910ull);
    VL_SCOPED_RAND_RESET_W(272, vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_first_r, __VscopeHash, 6095400329351984381ull);
    VL_SCOPED_RAND_RESET_W(272, vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_last_r, __VscopeHash, 9192590471598430350ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_len_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 12385506962684644687ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_ev_r = VL_SCOPED_RAND_RESET_Q(36, __VscopeHash, 4157267495528554899ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_fp_r = VL_SCOPED_RAND_RESET_I(24, __VscopeHash, 15387594646291291967ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__hold_valid_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 542668043275388425ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__hold_type_r = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 380811995878039291ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__hold_ev_r = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 2688958332119355023ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__hold_fp_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 10675623802175946963ull);
    VL_SCOPED_RAND_RESET_W(272, vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__hold_val_r, __VscopeHash, 12924699903006267419ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__join_pend_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 2907009889372666028ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__la_pend_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 5039071076081321899ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__push_msrp_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11339149633035743861ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__push_mvrp_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9803835744556793452ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__start0_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10774256932877649472ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__start1_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13093361591277740538ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__cap_type_w = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 6108577493220361888ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__cap_ev_w = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 11470349890823134143ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__cap_fp_w = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 4712108470914001510ull);
    VL_SCOPED_RAND_RESET_W(272, vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__cap_val_w, __VscopeHash, 11950098593731238320ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__open_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15692384319684536168ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__wr_valid_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7057831011066616875ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__wr_data_w = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 8596375889519913349ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__last_byte_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10806761994172360676ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__alen_w = VL_SCOPED_RAND_RESET_I(6, __VscopeHash, 14654730904262811437ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__ll_val_w = VL_SCOPED_RAND_RESET_I(11, __VscopeHash, 14938884124097080445ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rec_valid_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 1410132905695141246ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__armed_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 14976577799942528282ull);
    VL_SCOPED_RAND_RESET_W(128, vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__sid_r, __VscopeHash, 9325947269699916847ull);
    VL_SCOPED_RAND_RESET_W(96, vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__da_r, __VscopeHash, 8172318143276913359ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vid_r = VL_SCOPED_RAND_RESET_I(24, __VscopeHash, 9427258348728113289ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_r = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 6770334062564137919ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__fourpack_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 232888208897206283ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__decl_pend_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 12563100984541399046ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__decl_fp_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 10288975146063934606ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_pend_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 10436045732011346159ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_pend_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 10918542598622043294ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__walk_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 12880949565708376232ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__wsrc_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8596882483540652464ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__wtxla_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17302188750902356703ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__tick_pend_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17779178194979626795ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__laown_pend_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 224903445942624413ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__push_code_r = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 9895937668297610451ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__push_fp_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 2223138182540777415ull);
    VL_SCOPED_RAND_RESET_W(272, vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__push_val_r, __VscopeHash, 14552495007902054884ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 12052239756704942551ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rtype_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 16565823836095551039ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__lat_r = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 14989427126289894094ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__fcode_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 10641286180080939373ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__tpend_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 8312870736455650937ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vj_pend_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 5081709036564509524ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vl_pend_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 11897822169383290736ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vj_vid_r = VL_SCOPED_RAND_RESET_I(24, __VscopeHash, 8797819170777660896ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vl_vid_r = VL_SCOPED_RAND_RESET_I(24, __VscopeHash, 3081599926125261157ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_rx_hit_w = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 5909536968307406469ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_rx_hit_w = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 2852501359354640146ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rx_registering_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4267419344500946090ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__leaveall_any_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5842279746804301414ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__exp_hit_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 18215608912934481601ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__ind_reg_w = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 12914202330591245624ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__ind_unreg_w = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 12675829931667966561ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__ctl_acc_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14323989255853424553ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_v_w = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 13600140543945344948ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_ev_w = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 17969394653377455362ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__decl_grant_w = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 13654456212126543700ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__rla_grant_w = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 17032096198552323585ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__per_grant_w = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 14376856903437591353ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__walk_grant_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13766146517062977992ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__wmsg_w = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 17400954099577397301ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__tsel_v_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3386108296404257717ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__tsel_ix_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14420067369307003576ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vsel_v_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9815721353004667680ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vsel_join_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16537796271334906510ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vsel_ix_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2515677718233233176ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rec_valid_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 971041368037036570ull);
    VL_SCOPED_RAND_RESET_W(128, vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__sid_r, __VscopeHash, 10026060905665802475ull);
    VL_SCOPED_RAND_RESET_W(96, vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__da_r, __VscopeHash, 8429240935236558558ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vid_r = VL_SCOPED_RAND_RESET_I(24, __VscopeHash, 12664005979834263831ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__mfs_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 6710759923524977778ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__mif_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 8156124981141328622ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__prio_r = VL_SCOPED_RAND_RESET_I(6, __VscopeHash, 14994830590320035693ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rank_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 133175141411052667ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lat_r = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 4257598565921319404ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_r = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 9141496070779606948ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__fail_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 6759039244987993373ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rla_pend_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 6712237996847737382ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__per_pend_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 14898422271507854818ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__walk_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 8435178834858057815ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__wsrc_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11616156944263921896ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__wtxla_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5485234199609496571ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__tick_pend_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7210717416153715590ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__laown_pend_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2344047456235099169ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__push_code_r = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 8218828940896499982ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__push_type_r = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 3017133423023726346ull);
    VL_SCOPED_RAND_RESET_W(272, vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__push_val_r, __VscopeHash, 15508091828495275023ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 3680632173973996234ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_val_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 10960965281016327052ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_prev_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 7239326545903669152ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__tpend_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 18027092435626167676ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vj_pend_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 14298916006109846001ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vl_pend_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 3068137734882280586ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vj_vid_r = VL_SCOPED_RAND_RESET_I(24, __VscopeHash, 1069506789528237142ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vl_vid_r = VL_SCOPED_RAND_RESET_I(24, __VscopeHash, 5934166092461119952ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_rx_hit_w = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 10342084202229418200ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__gate_acc_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11957851266829381170ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_ev_v_w = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 6115133066140785525ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_ev_w = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 2401660070954642339ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__adm_grant_w = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 13566436022859396453ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__rla_grant_w = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 11347170529710050777ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__per_grant_w = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 10072583720385605350ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__wmsg_w = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 12402514698062709528ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__exp_hit_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 18348694708706772317ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_out_w = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 14169122299605642660ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__tsel_v_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9370679115894236369ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__tsel_ix_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3507319441650984386ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vsel_v_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16392648130112871854ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vsel_join_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2848267574194780960ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vsel_ix_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1694818704625388545ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__cidx_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6698266571209102822ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__cidx_q1_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16749470535475143909ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__cidx_q2_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16562625091273680412ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__frame_bytes_r = VL_SCOPED_RAND_RESET_I(17, __VscopeHash, 14005217878522695018ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__iv_bytes_r = VL_SCOPED_RAND_RESET_Q(33, __VscopeHash, 6781705893827111596ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__slope_q_r = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 15163995632131947837ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__f_raw_w = VL_SCOPED_RAND_RESET_I(17, __VscopeHash, 17047892637930603819ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__aidx_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14580427875027275337ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__acc_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 2599924325867421136ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__over_acc_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7074296046938588115ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__wgrant_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 1851104590785246900ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__wgslope_r = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 13679577522916570687ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__grant_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 3260855104024351585ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__gslope_r = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 3674888825803475415ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__sum_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 4774344857379869112ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__over_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15631411269139414502ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__cand_w = VL_SCOPED_RAND_RESET_Q(33, __VscopeHash, 18107062061865027816ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__fit_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12468567897886883879ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__refuse_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2044471568100279959ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__wgrant_now_w = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 7617278450172749057ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__wgslope_now_w = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 5696572343720178102ull);
    for (int __Vi0 = 0; __Vi0 < 4; ++__Vi0) {
        vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__tbl_r[__Vi0] = VL_SCOPED_RAND_RESET_I(17, __VscopeHash, 13547029787175518705ull);
    }
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__tbl_q_r = VL_SCOPED_RAND_RESET_I(17, __VscopeHash, 8232505598115131755ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__active_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 2713800013450977133ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__tbl_we_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3048546232123222137ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__tbl_wix_w = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 12034642367288535689ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__tbl_wdat_w = VL_SCOPED_RAND_RESET_I(17, __VscopeHash, 15450189266521677029ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__st_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 14544925585494973537ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__op_join_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5005861147654398519ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__op_vid_r = VL_SCOPED_RAND_RESET_I(12, __VscopeHash, 979405528265061419ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__scan_ix_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 15363099442587603156ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__chk_ix_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 3620993108505063569ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__chk_v_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9313652696878126163ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__found_v_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13987849311397005530ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__found_ix_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 5092880734726132626ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__found_cnt_r = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 8375294459103870522ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__free_v_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15457672540582906089ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__free_ix_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 13093947064839156013ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__ridx_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 9975005716234506799ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__rejoin_pend_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16019128910734555430ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__ev_code_r = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 8045944630240422320ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__ev_vid_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 13889199457149536589ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_domain__DOT__decl_prio_r = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 16679135930081044829ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_domain__DOT__decl_vid_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 4740881463613171839ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_domain__DOT__adopted_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17300244526290066734ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_domain__DOT__declared_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1603937490293373521ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_domain__DOT__link_q_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17366353651780823444ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_domain__DOT__q0_valid_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13076677055623127948ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_domain__DOT__q1_valid_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5825994110377039093ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_domain__DOT__q0_ev_r = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 13804776602553416793ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_domain__DOT__q1_ev_r = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 17380590276074612170ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_domain__DOT__q0_val_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 13782931858968160949ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_domain__DOT__q1_val_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 13451939187361836995ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_domain__DOT__rx_pend_v_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 70363332040788359ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_domain__DOT__rx_pend_prio_r = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 8598183384263370438ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_domain__DOT__rx_pend_vid_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 3097449493479846697ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_domain__DOT__rejoin_pend_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8105055523510182774ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_domain__DOT__surf_prio_w = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 14446189942296720831ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_domain__DOT__link_rise_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8852854020378269989ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_domain__DOT__link_fall_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10486339404783966885ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_domain__DOT__q_empty_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14366021978838321609ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_decoder__DOT__state_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 8649650737315335181ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_decoder__DOT__app_msrp_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16264709260826136053ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_decoder__DOT__attr_type_r = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 2245637490885852838ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_decoder__DOT__attr_len_r = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 9612539259274079702ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_decoder__DOT__listlen_cnt_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 4258924038503572846ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_decoder__DOT__vhdr1_r = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 9839167620269598220ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_decoder__DOT__values_left_r = VL_SCOPED_RAND_RESET_I(13, __VscopeHash, 11160132053534521270ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_decoder__DOT__fv_idx_r = VL_SCOPED_RAND_RESET_I(6, __VscopeHash, 1082641193708507710ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_decoder__DOT__last_seen_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4396011913285755674ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_decoder__DOT__sid_r = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 17896712795855962429ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_decoder__DOT__da_r = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 18331412461918168178ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_decoder__DOT__vid_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 17868076142334949824ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_decoder__DOT__mfs_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 17692244008173207293ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_decoder__DOT__mif_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 17576012543268735593ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_decoder__DOT__pr_r = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 3730401426426962158ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_decoder__DOT__lat_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 15375918340914270817ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_decoder__DOT__sysid_r = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 12786097582479287680ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_decoder__DOT__fcode_r = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 2820124287103314185ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_decoder__DOT__dcid_r = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 12288145094717878036ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_decoder__DOT__dprio_r = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 6705595734750273115ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_decoder__DOT__pend_byte_r = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 3607824094913134989ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_decoder__DOT__fp_byte_r = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 4312494681391218857ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_decoder__DOT__idx_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 13152456206281549122ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_decoder__DOT__slot_left_r = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 6078308660552256301ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_decoder__DOT__store_left_r = VL_SCOPED_RAND_RESET_I(13, __VscopeHash, 13488820428688213100ull);
    for (int __Vi0 = 0; __Vi0 < 1024; ++__Vi0) {
        vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_decoder__DOT__tp_ram[__Vi0] = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 5160688524251619039ull);
    }
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_decoder__DOT__tp_wptr_r = VL_SCOPED_RAND_RESET_I(11, __VscopeHash, 176532489837841790ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_decoder__DOT__tp_rd_byte_r = VL_SCOPED_RAND_RESET_I(10, __VscopeHash, 16049453688574406084ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_decoder__DOT__tp_rd_dig_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 14238990808255302095ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_decoder__DOT__tp_rdata_r = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 503826932650060367ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_decoder__DOT__accept_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 18290665428911035966ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_decoder__DOT__len_ok_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13699879424544134422ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_decoder__DOT__is_domain_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5844455544125715977ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_decoder__DOT__cur_digit_w = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 7270893984022688196ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__adp_stall_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 13473074570910533608ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__acmp_stall_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 3700142739542853195ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__aecp_stall_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 17541142288017592748ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__wr_ptr_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 10940215975724644379ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__rd_ptr_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 11753792097058283745ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__cnt_r = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 1073714924795440826ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__out_valid_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12762119178165531634ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__push_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6992302199133814032ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__rd_en_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6408301019967467379ull);
    for (int __Vi0 = 0; __Vi0 < 4; ++__Vi0) {
        VL_SCOPED_RAND_RESET_W(393, vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__mem_r[__Vi0], __VscopeHash, 18166022739465841971ull);
    }
    VL_SCOPED_RAND_RESET_W(393, vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__out_data_r, __VscopeHash, 11272928216636951804ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_acmp_q__DOT__wr_ptr_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 13986475761324051480ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_acmp_q__DOT__rd_ptr_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 864341020123784119ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_acmp_q__DOT__cnt_r = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 15819944644577965358ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_acmp_q__DOT__out_valid_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14862041329072280082ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_acmp_q__DOT__push_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5042064135303893074ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_acmp_q__DOT__rd_en_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9363120168760408918ull);
    for (int __Vi0 = 0; __Vi0 < 4; ++__Vi0) {
        VL_SCOPED_RAND_RESET_W(393, vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_acmp_q__DOT__mem_r[__Vi0], __VscopeHash, 4371539334914126388ull);
    }
    VL_SCOPED_RAND_RESET_W(393, vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_acmp_q__DOT__out_data_r, __VscopeHash, 3165011051853604865ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_adp_q__DOT__wr_ptr_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 17676458755450182547ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_adp_q__DOT__rd_ptr_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 12330396065084954191ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_adp_q__DOT__cnt_r = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 17120328095664313446ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_adp_q__DOT__out_valid_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1520841846770950985ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_adp_q__DOT__push_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9402169953942654601ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_adp_q__DOT__rd_en_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 18155298325990668374ull);
    for (int __Vi0 = 0; __Vi0 < 4; ++__Vi0) {
        VL_SCOPED_RAND_RESET_W(393, vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_adp_q__DOT__mem_r[__Vi0], __VscopeHash, 8927472333528011559ull);
    }
    VL_SCOPED_RAND_RESET_W(393, vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_adp_q__DOT__out_data_r, __VscopeHash, 3245386070860159722ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_maap_q__DOT__wr_ptr_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9583796058150328254ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_maap_q__DOT__rd_ptr_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 53219398432647049ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_maap_q__DOT__cnt_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 9395432840390307504ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_maap_q__DOT__out_valid_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11492068676638564601ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_maap_q__DOT__push_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12652553399462576925ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_maap_q__DOT__rd_en_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16271063851271089332ull);
    for (int __Vi0 = 0; __Vi0 < 2; ++__Vi0) {
        VL_SCOPED_RAND_RESET_W(393, vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_maap_q__DOT__mem_r[__Vi0], __VscopeHash, 7836748619359077188ull);
    }
    VL_SCOPED_RAND_RESET_W(393, vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_maap_q__DOT__out_data_r, __VscopeHash, 7411660193936249063ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_rb_we_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10993341743207506433ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__urb_addr_w = VL_SCOPED_RAND_RESET_I(10, __VscopeHash, 11646302874069230620ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_rb_addr_w = VL_SCOPED_RAND_RESET_I(10, __VscopeHash, 4869318726069107900ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__urb_wdata_w = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 17774214500654690051ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_rb_wdata_w = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 12063859281967364523ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__urb_wstrb_w = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 4394659806500968749ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_rb_wstrb_w = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 9457092509427128322ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__rsp_open_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16530738074725647970ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__rsp_seal_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3200150626305925087ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__rsp_seal_len_w = VL_SCOPED_RAND_RESET_I(11, __VscopeHash, 4154071429714858436ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__rsp_rd_valid_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8233936722156830819ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__rsp_rd_data_w = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 14517854964850429865ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__rsp_busy_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3717011354681855044ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__a_st_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 14587966794707483642ull);
    VL_SCOPED_RAND_RESET_W(393, vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cmd_r, __VscopeHash, 7232975388665223906ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__raw_ct_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 6396898638479909853ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cfg_ix_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 912044401482175679ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__desc_ty_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 13352814154499812620ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__desc_ix_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 14114270128535900841ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__name_ix_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 436819372140406060ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__name_cfg_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 15995133053283756441ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__pld_cmd_r = VL_SCOPED_RAND_RESET_I(11, __VscopeHash, 13276923692860750658ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__pld_r = VL_SCOPED_RAND_RESET_I(11, __VscopeHash, 14356689365063323863ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__walk_r = VL_SCOPED_RAND_RESET_I(11, __VscopeHash, 11629316777601228903ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__pid_lo_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 2285494010009139542ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__echo_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16486584535962819929ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__sent_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9033112756741375803ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__ctrs_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9247192717741682858ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2194337898265523303ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_edit_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6728895994050520889ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_remove_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7205424149651582206ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_uns_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16448584899955082229ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__regun_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3880181234843481929ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__acq_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3509008575518262700ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__lockc_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11942170176937124870ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gstri_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7037789763661582661ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gavb_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11357049045776696095ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gasp_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 455250719635718690ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__eavl_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12213890036306054977ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gcfg_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2098709005111316436ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gsfmt_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11488548075230667725ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gsrate_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12331153620825026885ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gclks_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17595373388098230186ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__ssrate_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5467477966269339531ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__sclks_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14070930542690366116ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__ssfmt_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16195446865809517935ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__ssinfo_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11360085489342674122ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gctrl_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15467999231253982698ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__sctrl_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10878673773668513026ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gname_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13673327283371788738ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__sname_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11080933286146260247ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__scfg_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10544233926860404256ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__strt_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17175053233807650825ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__stop_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13984192909522126600ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__strm_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12199226760200772385ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__setc_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14957120101793479068ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gdi_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16163767807811031237ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__setval_r = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 11776108468732001961ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__silat_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 1970355091812739398ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__lock_ent_ok_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2913000266542228353ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__uns_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1216068108771582194ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_rec_r = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 16674951481540316826ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__upc_r = VL_SCOPED_RAND_RESET_I(11, __VscopeHash, 6943463874162593161ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__status_r = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 378212369030761503ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__bidx_r = VL_SCOPED_RAND_RESET_I(11, __VscopeHash, 340409702497358590ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__frame_len_r = VL_SCOPED_RAND_RESET_I(11, __VscopeHash, 6688008009469533274ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__err_mode_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6083480143686821886ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__tx_slot_r = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 4064215570796469945ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cmd_cnt_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 17682086137923324720ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__resp_cnt_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 1625217024997646087ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__drop_cnt_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 17320520089087663683ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__rerr_cnt_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 7874289577703736657ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_scan_started_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 175949114192728178ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_rd_pending_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4720722675876449043ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_load_data_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17404779424015327370ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_hdr_ix_r = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 4551823565757147528ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_wr_phase_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 17519679527825149220ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_total_r = VL_SCOPED_RAND_RESET_I(11, __VscopeHash, 5598136342531160912ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_rd_pos_r = VL_SCOPED_RAND_RESET_I(11, __VscopeHash, 2837424064403895432ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_data_ix_r = VL_SCOPED_RAND_RESET_I(11, __VscopeHash, 15692120261596443186ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_data_start_r = VL_SCOPED_RAND_RESET_I(11, __VscopeHash, 3728425806482314048ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_next_pos_r = VL_SCOPED_RAND_RESET_I(11, __VscopeHash, 2246480004064929270ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_out_r = VL_SCOPED_RAND_RESET_I(11, __VscopeHash, 13520158744785900804ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_rec_rlen_r = VL_SCOPED_RAND_RESET_I(11, __VscopeHash, 174350975048463790ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_sub_end_r = VL_SCOPED_RAND_RESET_I(11, __VscopeHash, 7219256060411580836ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_scan_len_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 11830764485512421715ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_scan_cmd_hi_r = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 2559537228282465861ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_rec_len_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 2223429184527023344ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_rec_cmd_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 8796575091656208602ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_rec_cmd_status_r = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 11204908581418104970ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_data_head_r = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 2324227456562682289ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_rec_exec_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12024603627048027086ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_rec_status_r = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 125421324953412983ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_shape_fault_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17447832194203424172ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_sub_exec_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 803203182061100652ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_sub_rlen_w = VL_SCOPED_RAND_RESET_I(11, __VscopeHash, 1038634125864224455ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_sub_upc_w = VL_SCOPED_RAND_RESET_I(11, __VscopeHash, 32537836715338593ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_sub_status_w = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 15719942630481558188ull);
    for (int __Vi0 = 0; __Vi0 < 256; ++__Vi0) {
        vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_stage_r[__Vi0] = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 13291230737424509681ull);
    }
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_stage_q_r = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 4448726968794317575ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_stage_assem_r = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 12260348852677490480ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_stage_ready_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7504987757353154844ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_rsp_count_r = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 10089093359046378517ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_edit_pld_w = VL_SCOPED_RAND_RESET_I(11, __VscopeHash, 18043138608657114228ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_stage_ser_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11531479593229172700ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__upc_w = VL_SCOPED_RAND_RESET_I(11, __VscopeHash, 7301597864167325096ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__echo_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8799599321510184641ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__ctrs_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9670583326534868996ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6597762885748904949ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__aem_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9394265118067164470ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gdi_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7636122128121890951ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__drop_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7152467800036585136ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__ssrate_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 18365224000129199936ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__sclks_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9940712434174241828ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__sctrl_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2756217933048119052ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__ssfmt_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3235041065079433971ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__ssinfo_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2180489264729031064ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__strt_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17922330779595398425ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__stop_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1808873567343531163ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__uns_ct_w = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 5795369086115007949ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__uns_upc_w = VL_SCOPED_RAND_RESET_I(11, __VscopeHash, 9767311675853881600ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__pld_cap_w = VL_SCOPED_RAND_RESET_I(11, __VscopeHash, 14711079809892738333ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__pld_trim_w = VL_SCOPED_RAND_RESET_I(11, __VscopeHash, 3893223925462111304ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__disp_valid_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2834429909599974432ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__ucpu_done_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12986200605984335638ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__resp_send_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13361363920530726615ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__run_this_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10299643970737662936ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__ix26_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1861284381266162739ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__tix_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15719167886593240010ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__opd0_r = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 2986171472564303573ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__opd1_r = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 1961393420966736868ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__opd2_r = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 9788047600412736935ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__st_req_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3552990536439171484ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__st_we_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10206313517038322494ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__st_name_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7463003877669296448ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__st_addr_w = VL_SCOPED_RAND_RESET_I(20, __VscopeHash, 14787708782439773628ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__st_rdata_w = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 7624090965218294788ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__st_rvalid_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16121720640874293128ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__st_err_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7812332377635658227ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__dyn_sel_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14193459839837200550ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__strq_sel_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15495910313363948438ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__store_ready_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 519868981261098370ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__store_rvalid_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5429504655503592317ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gx_req_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15870400218380997933ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gx_sel_w = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 4980098478480361518ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT____Vcellinp__u_store__st_req_i = 0;
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT____Vcellinp__u_dyn__desc_index_i = 0;
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT____Vcellinp__u_dyn__st_req_i = 0;
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gsi_any_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6381721610945061834ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__rgy_any_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3268572661267169112ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__strm_state_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9831147618112306212ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gxf_tmo_r = VL_SCOPED_RAND_RESET_I(13, __VscopeHash, 4254942535269352124ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gxf_fail_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10570821951279379382ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__ctr_hold_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6353375297001417723ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_hold_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7932048135139205636ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_edit_hold_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 599398893542863720ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__name_hold_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 465386798931691432ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__rgy_hold_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8917003686265840999ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gsi_hold_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12647598098626879287ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gxr_valid_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3075326138250938537ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gxr_data_r = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 6490045114985703755ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__pay_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12597035746269964375ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_emit_count_w = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 2552820413225514975ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__byte_ok_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10031533373397420707ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__pad_len_w = VL_SCOPED_RAND_RESET_I(11, __VscopeHash, 11794817463410343008ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__rsp_fail_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12164360498415782730ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__lane_d_r = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 15947876954235959407ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__lane_s_r = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 14256705995058223115ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__lane_ix_r = VL_SCOPED_RAND_RESET_I(7, __VscopeHash, 14801645243350382114ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__lane_open_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7193410573965384457ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__st_r = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 6672310616537313920ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__seal_pend_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 987305281293286549ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__len_r = VL_SCOPED_RAND_RESET_I(11, __VscopeHash, 15818701332174903132ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__served_r = VL_SCOPED_RAND_RESET_I(11, __VscopeHash, 12242744371918871196ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__rlane_r = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 17732050943721727515ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__rvalid_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8460253095385107247ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__roff_r = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 17830392882708626290ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__fault_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16999685597226599678ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__fcode_r = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 8852494922758810386ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__lanewr_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 14043087075812001237ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__burst_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 15249229853748736904ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__drop_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 12122154147264366685ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__sk_valid_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13795470468792500990ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__sk_addr_r = VL_SCOPED_RAND_RESET_I(10, __VscopeHash, 18340142835377067368ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__sk_data_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 2894417192986585829ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__sk_strb_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 13435581193476284991ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__bix_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 8332277891297617306ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__wr_ready_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11323733770811698669ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__wreq_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17321929499579743122ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__wbusy_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3264939643920674607ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__rreq_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 449737718363437836ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__rbusy_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4778540241588223751ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__tmo_r = VL_SCOPED_RAND_RESET_I(13, __VscopeHash, 5240859485601610763ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__beat_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4249958918786800948ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__accept_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3277681973863682257ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__babs_w = VL_SCOPED_RAND_RESET_I(11, __VscopeHash, 2109335144577175450ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__bval_w = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 14167845547320768775ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__keep_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13127091661154321396ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__need_flush_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8398713481022766419ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__cfg_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 12380529117519230707ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__cfg_v_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2222987609765796174ull);
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__rate_r[__Vi0] = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 10139892733801933565ull);
    }
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__rate_v_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12100174438065422543ull);
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__clksrc_r[__Vi0] = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 3679776142744977086ull);
    }
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__clksrc_v_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 50276012191688908ull);
    for (int __Vi0 = 0; __Vi0 < 2; ++__Vi0) {
        vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__fmtin_r[__Vi0] = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 10770930121024125875ull);
    }
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__fmtin_v_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 12865873317738357170ull);
    for (int __Vi0 = 0; __Vi0 < 2; ++__Vi0) {
        vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__fmtout_r[__Vi0] = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 3077603209510633266ull);
    }
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__fmtout_v_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 14536751759516683991ull);
    for (int __Vi0 = 0; __Vi0 < 2; ++__Vi0) {
        vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__ptoff_r[__Vi0] = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 8518635912975473460ull);
    }
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__ptoff_v_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 14355502674129783021ull);
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__ident_r[__Vi0] = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 7851208967044511893ull);
    }
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__ident_v_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3948953811795233911ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__in_range_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12840714235097764617ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__val_w = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 2327775003272936982ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__vld_w = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 16985361848301373655ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__rd_pend_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7653267510757595404ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__rd_data_r = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 10339766594887096064ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__take_wr_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8492610173886558511ull);
    for (int __Vi0 = 0; __Vi0 < 32; ++__Vi0) {
        VL_SCOPED_RAND_RESET_W(128, vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__idx_r[__Vi0], __VscopeHash, 10470091030048144810ull);
    }
    VL_SCOPED_RAND_RESET_W(128, vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__idx_q_r, __VscopeHash, 2449529252693349034ull);
    for (int __Vi0 = 0; __Vi0 < 72; ++__Vi0) {
        vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__line_r[__Vi0] = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 16016881095818995866ull);
    }
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__line_q_r = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 9423360637076527479ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__line_waddr_w = VL_SCOPED_RAND_RESET_I(7, __VscopeHash, 16900828644347967660ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__line_raddr_w = VL_SCOPED_RAND_RESET_I(7, __VscopeHash, 16613253561306193049ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__line_wdata_w = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 10857421568483118023ull);
    for (int __Vi0 = 0; __Vi0 < 304; ++__Vi0) {
        vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__name_r[__Vi0] = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 2673144568874274704ull);
    }
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__name_q_r = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 11180687370161391390ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__name_waddr_w = VL_SCOPED_RAND_RESET_I(9, __VscopeHash, 17291141359334591432ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__name_raddr_w = VL_SCOPED_RAND_RESET_I(9, __VscopeHash, 14368400352307729779ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__name_wdata_w = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 13333406357247209368ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__name_wstrb_w = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 3927169099241200884ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__hdr_n_config_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 10302085852687319892ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__hdr_n_entries_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 9944312857574372187ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__hdr_n_names_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 5074163327289237872ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__hdr_desc_max_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 12937949864773350578ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__hdr_index_off_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 1277262751037604681ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__hdr_names_off_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 13348735514511267680ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__cksum_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 2093267252163672052ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__hdr_b0_r = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 2056349345972395093ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__idx_b0_r = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 14757121595382705478ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__st_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 13466403094170923841ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__img_valid_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5738454821745295107ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__fault_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 4270566946249712393ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__miss_cnt_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 443408225959273976ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__fetch_cnt_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 7268638856621402401ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__rowr_cnt_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 13701853775063377204ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__mreq_addr_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 10951005305329566217ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__mreq_beats_r = VL_SCOPED_RAND_RESET_I(9, __VscopeHash, 3298703742159287614ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__mreq_valid_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16032202588241590025ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__beat_ix_r = VL_SCOPED_RAND_RESET_I(9, __VscopeHash, 8632151980551820233ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__name_load_lane_r = VL_SCOPED_RAND_RESET_I(20, __VscopeHash, 13808610834604931345ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__tmo_r = VL_SCOPED_RAND_RESET_I(13, __VscopeHash, 18439391388049526640ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__mem_busy_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15961559794817380539ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__name_total_lanes_w = VL_SCOPED_RAND_RESET_I(20, __VscopeHash, 11710981044011339287ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__name_lanes_left_w = VL_SCOPED_RAND_RESET_I(20, __VscopeHash, 5658239995792376513ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__beat_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 18053158548461788216ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__accept_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11705096214946739324ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__key_cfg_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 6574431088211918596ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__key_type_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 16769328448826409681ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__key_index_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 4725837344297572166ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__desc_len_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 13104613737624418620ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__desc_nbase_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 17863702027928399677ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__desc_off_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 17520576176403900507ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__ans_err_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 680995077508073366ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__ans_data_r = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 13272140982590912812ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__rd_reg_r = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 2530736677586076201ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__ans_pend_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15653055073146378468ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__rd_pipe_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12567312466819517005ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__req_seen_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4824648096675318335ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__rd_kind_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 14998670199594559037ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__scan_rd_r = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 12165540178437623867ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__scan_cmp_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 1638146590623534641ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__scan_rdy_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11038638786488237061ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__scan_base_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 7219763641820953697ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__heal_pend_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3039456276204942901ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__heal_kind_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4888716375711283707ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__patch_answer_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2879114748381538474ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__patch_name_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 280618801935938677ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__patch_byte_r = VL_SCOPED_RAND_RESET_I(6, __VscopeHash, 17867161137932607429ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__e_usable_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5817006493325260571ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__type_hit_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9370380432948840698ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__last_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4258410262407660911ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__rel_w = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 3999179995072509266ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__take_rd_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12245420948997128157ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__take_wr_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4345684984620064437ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__len_lanes_w = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 4364961775097223110ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__patch_abs_byte_w = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 17437482407904463014ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__patch_data_w = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 14750544267344049950ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__name_lookup_entry_w = VL_SCOPED_RAND_RESET_I(17, __VscopeHash, 12570781262871293184ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__hdr_ok_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10496691514248023955ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__hdr_fault_w = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 2175084822559279050ull);
    for (int __Vi0 = 0; __Vi0 < 2048; ++__Vi0) {
        vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__rom_r[__Vi0] = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 5168612555586776086ull);
    }
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__rom_q_r = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 15796026840166533424ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__upc_r = VL_SCOPED_RAND_RESET_I(11, __VscopeHash, 5601258088396211612ull);
    for (int __Vi0 = 0; __Vi0 < 16; ++__Vi0) {
        vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__rf_r[__Vi0] = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 12298024905670714357ull);
    }
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__rf_waddr_w = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 13748726667365864720ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__rf_wdata_w = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 16767364011286760758ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__rf_we_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16381415189931841558ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__ms_r = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 14503492174645095591ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__vld_d_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6299005459110820056ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__uop_e_r = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 10341943963357000908ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__vld_e_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13392426024819558012ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__opa_e_r = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 16609575562342214965ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__opb_e_r = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 2371815042072152301ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__opd_e_r = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 1328913085166533780ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__wb_rd_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 7311528473005075807ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__wb_data_r = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 7147003281448716986ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__wb_we_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13076362244598120856ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__status_r = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 14181412916060456118ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__z_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14673943426353668893ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__lt_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 820882334910981762ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__ovf_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16664866428259773564ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__desc_base_r = VL_SCOPED_RAND_RESET_I(20, __VscopeHash, 16048032901628217818ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__iter_cnt_r = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 3519259410267488844ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__iter_idx_r = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 5152295185891625372ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__cursor_r = VL_SCOPED_RAND_RESET_I(10, __VscopeHash, 5598434706720203408ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__resp_len_r = VL_SCOPED_RAND_RESET_I(11, __VscopeHash, 13491630224752929410ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__batch_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9097635122699226908ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__eseq_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 17678850754268337270ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__copy_go_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5923930055089393315ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__copy_left_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 267496033821813120ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__copy_idx_r = VL_SCOPED_RAND_RESET_I(13, __VscopeHash, 7656709415899952829ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__copy_lane_r = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 14492960045347740459ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__raw_d_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16991221910564320560ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__a_fmt_w = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 17262174233755796669ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__b_or_imm_w = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 15618294167985625284ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__cmp_z_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12701850642001822446ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__fld_len_w = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 13664495875123550513ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__copy_adv1_w = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 7969715205611316465ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__copy_adv2_w = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 18097133536038090138ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__append_skip_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17886094613078528845ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__is_q_field_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17980306480474789893ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__rb_hold_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10039963568127249310ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__stall_e_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4952910382441855409ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__br_taken_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7543326732901250296ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__end_op_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2779482345416469277ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__advance_e_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9870194442209665769ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__DOT__writing_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 8406262026100818404ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__DOT__occupied_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 13798421436504419719ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__DOT__cur_slot_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 16028513894532561832ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__DOT__wr_active_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7837512943258705324ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__DOT__wr_closed_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13712314866739408546ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__DOT__wr_ptr_r = VL_SCOPED_RAND_RESET_I(10, __VscopeHash, 15372463127036004035ull);
    for (int __Vi0 = 0; __Vi0 < 4; ++__Vi0) {
        vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__DOT__len_r[__Vi0] = VL_SCOPED_RAND_RESET_I(10, __VscopeHash, 8491290296818427562ull);
    }
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__DOT__ff_valid_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 18208704711857664582ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__DOT__ff_slot_w = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 17303858229327089871ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__DOT__byte_acc_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2308035025987465291ull);
    for (int __Vi0 = 0; __Vi0 < 2304; ++__Vi0) {
        vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__DOT__mem_r[__Vi0] = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 4070238877029267903ull);
    }
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__DOT__wr_maddr_w = VL_SCOPED_RAND_RESET_I(12, __VscopeHash, 2767717317566257924ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__DOT__rd_maddr_w = VL_SCOPED_RAND_RESET_I(12, __VscopeHash, 5732829387836738930ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__4__KET____DOT__u_rx_slots__DOT__writing_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 15060909667222442173ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__4__KET____DOT__u_rx_slots__DOT__occupied_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 17217181680232526467ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__4__KET____DOT__u_rx_slots__DOT__cur_slot_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 8447842739672238625ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__4__KET____DOT__u_rx_slots__DOT__wr_active_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12493497079239212925ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__4__KET____DOT__u_rx_slots__DOT__wr_closed_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11685955801110073807ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__4__KET____DOT__u_rx_slots__DOT__wr_ptr_r = VL_SCOPED_RAND_RESET_I(10, __VscopeHash, 12447641574479539059ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__4__KET____DOT__u_rx_slots__DOT__ff_valid_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9575373522373897963ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__4__KET____DOT__u_rx_slots__DOT__ff_slot_w = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 13827194517137702895ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__4__KET____DOT__u_rx_slots__DOT__byte_acc_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8045914069366290943ull);
    for (int __Vi0 = 0; __Vi0 < 2304; ++__Vi0) {
        vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__4__KET____DOT__u_rx_slots__DOT__mem_r[__Vi0] = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 4006281865622640231ull);
    }
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__4__KET____DOT__u_rx_slots__DOT__wr_maddr_w = VL_SCOPED_RAND_RESET_I(12, __VscopeHash, 17279007275381913887ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__4__KET____DOT__u_rx_slots__DOT__rd_maddr_w = VL_SCOPED_RAND_RESET_I(12, __VscopeHash, 7046938941150520962ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__2__KET____DOT__u_rx_slots__DOT__writing_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 203151333496439598ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__2__KET____DOT__u_rx_slots__DOT__occupied_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 1264933982135688308ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__2__KET____DOT__u_rx_slots__DOT__cur_slot_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 1968089919829221693ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__2__KET____DOT__u_rx_slots__DOT__wr_active_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 69138273503122562ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__2__KET____DOT__u_rx_slots__DOT__wr_closed_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13428091791112872854ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__2__KET____DOT__u_rx_slots__DOT__wr_ptr_r = VL_SCOPED_RAND_RESET_I(10, __VscopeHash, 13279724974667909941ull);
    for (int __Vi0 = 0; __Vi0 < 4; ++__Vi0) {
        vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__2__KET____DOT__u_rx_slots__DOT__len_r[__Vi0] = VL_SCOPED_RAND_RESET_I(10, __VscopeHash, 10990255645276368847ull);
    }
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__2__KET____DOT__u_rx_slots__DOT__ff_valid_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13474969194015149012ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__2__KET____DOT__u_rx_slots__DOT__ff_slot_w = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 1888547970619675846ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__2__KET____DOT__u_rx_slots__DOT__byte_acc_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6522634151910516659ull);
    for (int __Vi0 = 0; __Vi0 < 2304; ++__Vi0) {
        vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__2__KET____DOT__u_rx_slots__DOT__mem_r[__Vi0] = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 8690703838923876750ull);
    }
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__2__KET____DOT__u_rx_slots__DOT__wr_maddr_w = VL_SCOPED_RAND_RESET_I(12, __VscopeHash, 10174442559705650474ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__2__KET____DOT__u_rx_slots__DOT__rd_maddr_w = VL_SCOPED_RAND_RESET_I(12, __VscopeHash, 151916970657551780ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__1__KET____DOT__u_rx_slots__DOT__writing_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 16614558234402319903ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__1__KET____DOT__u_rx_slots__DOT__occupied_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 6421600620524360025ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__1__KET____DOT__u_rx_slots__DOT__cur_slot_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 10759312324851854558ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__1__KET____DOT__u_rx_slots__DOT__wr_active_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7809183358198234367ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__1__KET____DOT__u_rx_slots__DOT__wr_closed_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6079850089612122551ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__1__KET____DOT__u_rx_slots__DOT__wr_ptr_r = VL_SCOPED_RAND_RESET_I(10, __VscopeHash, 13080418407985788114ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__1__KET____DOT__u_rx_slots__DOT__ff_valid_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16477978413136511761ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__1__KET____DOT__u_rx_slots__DOT__ff_slot_w = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 16673198710890532353ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__1__KET____DOT__u_rx_slots__DOT__byte_acc_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8546476971083861706ull);
    for (int __Vi0 = 0; __Vi0 < 2304; ++__Vi0) {
        vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__1__KET____DOT__u_rx_slots__DOT__mem_r[__Vi0] = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 11398156886148025249ull);
    }
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__1__KET____DOT__u_rx_slots__DOT__wr_maddr_w = VL_SCOPED_RAND_RESET_I(12, __VscopeHash, 542814239294558281ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__1__KET____DOT__u_rx_slots__DOT__rd_maddr_w = VL_SCOPED_RAND_RESET_I(12, __VscopeHash, 3026733765093250986ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__0__KET____DOT__u_rx_slots__DOT__writing_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 10929989037808023214ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__0__KET____DOT__u_rx_slots__DOT__occupied_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 4631423860355616695ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__0__KET____DOT__u_rx_slots__DOT__free_mask_w = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 5468505277001180910ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__0__KET____DOT__u_rx_slots__DOT__cur_slot_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 12855531097088482874ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__0__KET____DOT__u_rx_slots__DOT__wr_active_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13992205017888645692ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__0__KET____DOT__u_rx_slots__DOT__wr_closed_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 447252986947117805ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__0__KET____DOT__u_rx_slots__DOT__wr_ptr_r = VL_SCOPED_RAND_RESET_I(10, __VscopeHash, 14257290356227969865ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__0__KET____DOT__u_rx_slots__DOT__ovr_cnt_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 15932077041231480356ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__0__KET____DOT__u_rx_slots__DOT__ff_valid_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2059277679517817156ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__0__KET____DOT__u_rx_slots__DOT__ff_slot_w = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 4241423147486637567ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__0__KET____DOT__u_rx_slots__DOT__byte_acc_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17429647376136799493ull);
    for (int __Vi0 = 0; __Vi0 < 2304; ++__Vi0) {
        vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__0__KET____DOT__u_rx_slots__DOT__mem_r[__Vi0] = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 2592612314483427386ull);
    }
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__0__KET____DOT__u_rx_slots__DOT__wr_maddr_w = VL_SCOPED_RAND_RESET_I(12, __VscopeHash, 18039841719165463787ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__0__KET____DOT__u_rx_slots__DOT__rd_maddr_w = VL_SCOPED_RAND_RESET_I(12, __VscopeHash, 11843427562509853825ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_side_port__DOT__state_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 4206521779429487838ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_side_port__DOT__sel_r = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 11530522066060218483ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_side_port__DOT__fwd_ok_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13700653974969710352ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_side_port__DOT__accept_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10721347440593014902ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_side_port__DOT__sel_rvalid_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8231646147049334610ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_side_port__DOT__sel_rdata_w = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 8292343832503117875ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__arb_st_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 9101721246396058796ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__slot_r = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 4498635239113923030ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__owner_r = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 3851487498061475218ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__start_sent_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12719988796403882761ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__sof_pend_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17572001536088770843ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__pace_nonsol_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7582206252068685860ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__gnt_r = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 16385177880247686133ull);
    for (int __Vi0 = 0; __Vi0 < 8; ++__Vi0) {
        vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__age_r[__Vi0] = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 18301582253119975910ull);
    }
    for (int __Vi0 = 0; __Vi0 < 8; ++__Vi0) {
        vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__cnt_r[__Vi0] = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 14809373652063013944ull);
    }
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__aged_w = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 7798115208618282996ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__pend_r = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 10656354209220061373ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__pend_w = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 6023506135521294057ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__pick_ok_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6319525180114452582ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__pick_w = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 15427290105601663060ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__accept_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5746013383219804287ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__consume_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17004413805818794045ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__eof_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5878057925913043048ull);
    for (int __Vi0 = 0; __Vi0 < 8; ++__Vi0) {
        vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__st_r[__Vi0] = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 9650274946942135168ull);
    }
    for (int __Vi0 = 0; __Vi0 < 8; ++__Vi0) {
        vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__len_r[__Vi0] = VL_SCOPED_RAND_RESET_I(11, __VscopeHash, 2340802394096556132ull);
    }
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__held_r = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 10638814416560507511ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__release_pend_r = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 12559948910996278487ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__alloc_gnt_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14345287198332135203ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__alloc_slot_r = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 16877261865439667027ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__run_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8209146640798125824ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__out_valid_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13981089206145573146ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__out_last_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13239454539384831479ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__cur_slot_r = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 2211852958952964167ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__fetch_idx_r = VL_SCOPED_RAND_RESET_I(11, __VscopeHash, 9682081523772301801ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__pick_ok_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16986809873519342611ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__pick_w = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 17442110602824199066ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__grant_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17211130882035099930ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__commit_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3549713738387709088ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__ser_start_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11952659555023171777ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__rd_en_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13779345522373563356ull);
    for (int __Vi0 = 0; __Vi0 < 3904; ++__Vi0) {
        vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__mem_r[__Vi0] = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 10038608433390220916ull);
    }
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__rd_q_r = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 16866951806149283308ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__wr_madr_w = VL_SCOPED_RAND_RESET_I(12, __VscopeHash, 11479485174107980092ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__rd_madr_w = VL_SCOPED_RAND_RESET_I(12, __VscopeHash, 8436246970863291548ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_release_merge__DOT__pending_r = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 6457577978700827053ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_release_merge__DOT__request_w = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 4633688152139818688ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_release_merge__DOT__available_w = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 3638800139810502899ull);
    for (int __Vi0 = 0; __Vi0 < 16; ++__Vi0) {
        VL_SCOPED_RAND_RESET_W(128, vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__rows_r[__Vi0], __VscopeHash, 9115024697670650718ull);
    }
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__valid_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 10843083786985803169ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__tl_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 7774273470213398478ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__pend_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 16783585101551397329ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__row_eid_w = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 692647590911646331ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__row_mac_w = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 14040762209638490141ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__wr_en_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6704964192738436625ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__wr_ix_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 11777383083058146422ull);
    VL_SCOPED_RAND_RESET_W(128, vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__wr_row_r, __VscopeHash, 13557186798560636364ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__lk_held_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13937143421931354693ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__lk_ctlr_r = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 15103859534326943947ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__pe_sin_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 6190732412057982457ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__pe_sout_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 17453453531680329299ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__pe_avb_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5098948337161878586ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__pe_asp_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 18117051375667700137ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__pe_lock_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1691667791537810591ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__pe_amap_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6758872824870271083ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__amap_remove_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6949649022015996068ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__amap_type_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 10997756514706295163ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__amap_index_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 17755541145235805083ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__amap_count_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 9890055543909568950ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__amap_excl_r = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 15444893169075170702ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__lockx_eid_r = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 12824943053302758564ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__lockx_v_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15601362056363451656ull);
    for (int __Vi0 = 0; __Vi0 < 16; ++__Vi0) {
        vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__cmdq_class_r[__Vi0] = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 8462498183671550576ull);
    }
    for (int __Vi0 = 0; __Vi0 < 16; ++__Vi0) {
        vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__cmdq_type_r[__Vi0] = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 17043831306153504248ull);
    }
    for (int __Vi0 = 0; __Vi0 < 16; ++__Vi0) {
        vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__cmdq_index_r[__Vi0] = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 2561313373783517444ull);
    }
    for (int __Vi0 = 0; __Vi0 < 16; ++__Vi0) {
        vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__cmdq_arg0_r[__Vi0] = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 135039679657630381ull);
    }
    for (int __Vi0 = 0; __Vi0 < 16; ++__Vi0) {
        vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__cmdq_arg1_r[__Vi0] = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 13259256746880531252ull);
    }
    for (int __Vi0 = 0; __Vi0 < 16; ++__Vi0) {
        vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__cmdq_excl_r[__Vi0] = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 6907675833171461510ull);
    }
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__cmdq_wr_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 17562832482828908904ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__cmdq_rd_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 13763370553509029398ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__cmdq_count_r = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 7988224167808647104ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__cmd_class_ok_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8725396141258471274ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__cmd_push_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7887936099420857748ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__ctr_dirty_r = VL_SCOPED_RAND_RESET_I(6, __VscopeHash, 10543780471631240301ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__ctr_pend_r = VL_SCOPED_RAND_RESET_I(6, __VscopeHash, 15451982987170818573ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__ctr_sent_r = VL_SCOPED_RAND_RESET_I(6, __VscopeHash, 15825621379586415342ull);
    for (int __Vi0 = 0; __Vi0 < 6; ++__Vi0) {
        vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__ctr_last_r[__Vi0] = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 2509337063071983142ull);
    }
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__ctr_ev_ok_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9101830116052563767ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__ctr_ev_ix_w = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 5503280646631743835ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__mon_draw_pend_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 2108834410427906429ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__ca_pend_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 3235881520637570940ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__ca_probe_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 18016001784540544060ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__mon_draw_wait_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15807111432680128693ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__mon_draw_ix_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 2425655266125743166ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__mon_pick_ok_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13361092817899984606ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__ca_pick_ok_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4238514450758664449ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__mon_pick_ix_w = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 5037076400208680243ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__ca_pick_ix_w = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 607561029763206964ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__rx_cmd_hit_w = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 2492020875059869407ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__dh_v_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17026919773019308054ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__dh_eid_r = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 13053965471930839194ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__dh_mac_r = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 13940229755077643909ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__dh_seq_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 11491790095868280232ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__n_st_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 15931757185569052427ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__req_done_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14739140444317849724ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__wk_ix_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 15243080489825879693ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__wk_match_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8767264244543793529ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__wk_match_ix_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 16922516510788581117ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__wk_match_seq_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 11064213662491565292ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__wk_free_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1787911749519954801ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__wk_free_ix_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 14639639823268383595ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__hold_eid_r = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 7685414019035030416ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__hold_mac_r = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 3975892753553673011ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__hold_seq_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 4818651627588524729ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__op_tl_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4596908902795927922ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__op_dereg_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 18365755611622805386ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__result_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 13830866285144552274ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__result_q_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 18124325998113153297ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__em_active_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12040463070461493104ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__em_kind_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 15671802438965544291ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__em_dt_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 11219669187193910411ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__em_di_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 7306195361380578273ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__em_arg0_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 2767375666377964976ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__em_arg1_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 7003057903075681776ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__em_excl_r = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 10623696329615909996ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__em_excl_v_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12141833474899062678ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__em_amap_remove_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4146939443766993937ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__em_amap_count_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 16461820305573049103ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__em_dh_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9061456729646940465ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__em_ix_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 6717780284541246580ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__uns_cnt_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 9115426221723050230ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__coalesce_r = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 9571012494287733533ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__deadline_w = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 9650878328317852015ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__rgy_new_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4891186087827175146ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__em_skip_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 18145194793369016306ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__pick_any_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8360117408746226373ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__pick_kind_w = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 416978507951132860ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__pick_dt_w = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 2244594239341406376ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__pick_di_w = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 10773501702765354256ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__pick_arg0_w = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 14392126810641313678ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__pick_arg1_w = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 9072127932906022180ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__pick_cmd_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13135360410197873079ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__pick_ctr_ix_w = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 4330460746438141433ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__pd_any_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12831398145017534928ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__pd_ix_w = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 14764010199864476319ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r = VL_SCOPED_RAND_RESET_I(11, __VscopeHash, 2009604792742241426ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__coalesced_r = VL_SCOPED_RAND_RESET_I(11, __VscopeHash, 7993291850740915914ull);
    for (int __Vi0 = 0; __Vi0 < 11; ++__Vi0) {
        vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r[__Vi0] = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 16759673114524970833ull);
    }
    for (int __Vi0 = 0; __Vi0 < 11; ++__Vi0) {
        vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r[__Vi0] = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 654501378792981787ull);
    }
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__valid_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2946401693474366560ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__sel_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 652769772990411180ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__ptr_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 2603275298639792403ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__deliver_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4832460384937482744ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__delivered_w = VL_SCOPED_RAND_RESET_I(11, __VscopeHash, 2621188081450634061ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__gnt_found_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7728548345585337118ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__gnt_src_w = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 1193857888044396533ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__state_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 5954216302887146608ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__err_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12449456136087434359ull);
    for (int __Vi0 = 0; __Vi0 < 8; ++__Vi0) {
        vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__hdr_r[__Vi0] = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 5807312707327849233ull);
    }
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__hidx_r = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 15513082179918093276ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__bcnt_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 5161613845913672845ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__plen_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 2849812172979815578ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__rec_r = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 1385622564109546057ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__done_seen_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5219627429630826434ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__hdr_plen_w = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 1962010904591836977ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__hdr_ok_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5698892212601729156ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__hs_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 15172682556560145851ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__init_cnt_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 16097460251064396655ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__go_pend_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5803472456665096716ull);
    for (int __Vi0 = 0; __Vi0 < 2; ++__Vi0) {
        VL_SCOPED_RAND_RESET_W(146, vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__shw_ram_r[__Vi0], __VscopeHash, 15414834417775363979ull);
    }
    VL_SCOPED_RAND_RESET_W(146, vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__shw_rdata_r, __VscopeHash, 17076438962525406157ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__wr_en_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7406955278665278953ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__wr_addr_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3717214114216897162ull);
    VL_SCOPED_RAND_RESET_W(146, vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__wr_data_w, __VscopeHash, 9209657149926012373ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__byp_v_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17216715114529789244ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__byp_sink_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14055427263629292830ull);
    VL_SCOPED_RAND_RESET_W(146, vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__byp_data_r, __VscopeHash, 14399711282341253755ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__valid_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 4002212850609588216ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__dirty_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 6079256773193364894ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__touched_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 8432870386847487463ull);
    VL_SCOPED_RAND_RESET_W(384, vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__cap_rec_w, __VscopeHash, 4868951667375560366ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__cap_active_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9874137487736635272ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__c1_v_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4839492065743547598ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__c1_sink_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8161384763673704904ull);
    VL_SCOPED_RAND_RESET_W(146, vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__c1_proj_r, __VscopeHash, 8377121699824114008ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__c1_vld_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6188639301884884534ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__c1_wr_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8083874833267489415ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__go_take_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6947455527237647292ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__rs_k_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11001864523873499973ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__rbcnt_r = VL_SCOPED_RAND_RESET_I(17, __VscopeHash, 10979568626112052443ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__rver_r = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 3967546113178012595ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__rrid_r = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 15460015234407902033ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__rplen_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 4414753659210957424ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__rcrc_rx_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 12813546583761655355ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__rcrc_acc_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 17154498454523559819ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__rvld_q_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8163496331887818164ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__rstarted_q_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6664941833847452860ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__rsw_q_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6333635774084635273ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__ruid_q_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 2174711508665644033ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__rtk_q_r = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 10811507302140511755ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__rctlr_q_r = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 16256098307928642847ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__rrec_ok_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3884351883275532014ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__rp_k_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4652407669655591776ull);
    VL_SCOPED_RAND_RESET_W(146, vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__rp_fields_r, __VscopeHash, 4168202904955286908ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__fl_sink_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12643777771115665067ull);
    VL_SCOPED_RAND_RESET_W(146, vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__fl_fields_r, __VscopeHash, 573782939814194100ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__fl_vld_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10859839579511206931ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__fl_crc_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 18294038682496621365ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__fl_cidx_r = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 4034759163947920114ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__fl_sidx_r = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 12458601591443997742ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__fl_retry_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 14242839285272061990ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__fl_taint_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10490320554903008878ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__fl_any_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4352382884568379577ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__fl_pick_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17344262144884512098ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__deb_open_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 18011858854205082135ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__deb_cnt_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 12866240656857811174ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__fl_arm_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8952922941592271279ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__fsm_rd_req_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4457168004024778885ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__fsm_rd_gnt_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1086546641567541926ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__fsm_wr_gnt_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15227643819166021635ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__rs_torn_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6736265510642956057ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__rs_empty_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12816313919660424296ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__rs_complete_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3004990022956684079ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__fl_giveup_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2959807519477951738ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__alarm_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9429019278032530969ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__done_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10785751417749168493ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__fail_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7081547262667739447ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__any_rec_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4913769550932468598ull);
    for (int __Vi0 = 0; __Vi0 < 2048; ++__Vi0) {
        vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_mrp_strip__DOT__ram_r[__Vi0] = VL_SCOPED_RAND_RESET_I(10, __VscopeHash, 16102300199526076510ull);
    }
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_mrp_strip__DOT__ram_q_r = VL_SCOPED_RAND_RESET_I(10, __VscopeHash, 5410896592884553982ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_mrp_strip__DOT__wr_cmt_r = VL_SCOPED_RAND_RESET_I(12, __VscopeHash, 184606238668961856ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_mrp_strip__DOT__wr_tent_r = VL_SCOPED_RAND_RESET_I(12, __VscopeHash, 7226570573661460132ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_mrp_strip__DOT__rd_ptr_r = VL_SCOPED_RAND_RESET_I(12, __VscopeHash, 8158076141845482817ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_mrp_strip__DOT__hdr_idx_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 16417636416150819692ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_mrp_strip__DOT__et_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 16570397614303696058ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_mrp_strip__DOT__drop_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 18247907237021647855ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_mrp_strip__DOT__out_vld_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8174619666086696582ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_mrp_strip__DOT__out_ent_r = VL_SCOPED_RAND_RESET_I(10, __VscopeHash, 13565662178448628222ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_mrp_strip__DOT__skid_vld_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9428056831671319375ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_mrp_strip__DOT__skid_ent_r = VL_SCOPED_RAND_RESET_I(10, __VscopeHash, 11688937233139859927ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_mrp_strip__DOT__fetch_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4677735292891643502ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_mrp_strip__DOT__avail_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6649475220623954543ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_mrp_strip__DOT__space_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2988358891924636026ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__pstate_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 14217770795802577595ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__offset_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 10404938192302089340ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__w_st_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 3853795728492140985ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__ival_ann_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16082559283254854016ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__send_msg_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 17138152121153420149ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__chain_ann_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12929607260345778466ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__teardown_ph_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 18418778547437237149ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__draw_act_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2496660410541598130ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__draw_req_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11590075303985247689ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__draw_kind_r = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 14888740355114364644ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__bld_slot_r = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 14092286237651573552ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__bld_idx_r = VL_SCOPED_RAND_RESET_I(6, __VscopeHash, 1148409917753016054ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__def_da_r = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 17300915455380341938ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__def_req_start_r = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 5897438834901259107ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__def_req_cnt_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 15284523542388230327ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__def_conf_start_r = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 8594753446730516898ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__def_conf_cnt_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 5446807300946655728ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__arm_v_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15753704259110111495ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__arm_c_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8616846808656289014ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__arm_ann_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 98802186668054981ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__arm_dl_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 8429506790666952902ull);
    for (int __Vi0 = 0; __Vi0 < 2; ++__Vi0) {
        VL_SCOPED_RAND_RESET_W(84, vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__rec_ram_r[__Vi0], __VscopeHash, 2771424252594028409ull);
    }
    VL_SCOPED_RAND_RESET_W(84, vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__rec_q_r, __VscopeHash, 18374640028154906092ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__rec_we_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17488446854252316127ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__rec_waddr_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6399496219017718716ull);
    VL_SCOPED_RAND_RESET_W(84, vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__rec_wdata_w, __VscopeHash, 12837016525171151706ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__rec_re_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4447112634023722453ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__rec_raddr_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16712711096223378667ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__declaring_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 16585780990249879266ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__pe_conflict_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 10489960994238791645ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__pe_pcp_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 7656435199182724635ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__pe_tmr_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 17077310910720972842ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__pe_lsn_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 4946750387546506399ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__pe_init_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 17511855595170796642ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__pe_off_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 8108137895644067375ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__pe_rel_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 5007850317004205834ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__lsn_q_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 6861391856455733557ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__en_q_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 14514840831090202859ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__maap_busy_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4605819149110289397ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__maap_src_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9081586241338373799ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__maap_rel_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8436236632008558921ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__maap_t0_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 12712786165647639901ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__gp_valid_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11297073716493070903ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__gp_src_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14364507806602947276ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__gp_da_r = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 11817520555116245951ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__maap_stale_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 2445059308112676884ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__maap_swallow_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6173237005115770887ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__maap_rsp_live_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14906714669494836608ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__maap_rsp_tmo_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5044890350085058475ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__maap_accept_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 901054422540347440ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__maap_avail_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 571184709594741116ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__state_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 12941678745824596022ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_code_r = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 13348813246078780041ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_src_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15865553532052990119ull);
    VL_SCOPED_RAND_RESET_W(393, vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__txn_r, __VscopeHash, 2050115994582852346ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__fetch_ix_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 3269086957327668606ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__slot_len_r = VL_SCOPED_RAND_RESET_I(10, __VscopeHash, 2107781219091166754ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__pdu_leid_r = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 18373734842824229535ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__pdu_luid_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 5457071885761470300ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__pdu_flags_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 9194817430947825802ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__arm_deadline_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 15650960444389830491ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__mreq_src_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2325601455337094927ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__mreq_rel_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13224177748126016007ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__mreq_tmo_r = VL_SCOPED_RAND_RESET_I(10, __VscopeHash, 15635405149108903224ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__init_ix_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 2013866448632579450ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__maap_tmo_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13044961645091677549ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__disp_kind_w = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 14284089331892536098ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__disp_code_w = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 4882812983722866996ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__disp_src_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16457290099323258993ull);
    VL_SCOPED_RAND_RESET_W(393, vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__txn_in_w, __VscopeHash, 15158427865614925974ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__uid16_w = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 12296705746684707235ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__talker_cmd_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2768998950399369323ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__da_ok_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11120533884327584093ull);
    VL_SCOPED_RAND_RESET_W(84, vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_rec2_w, __VscopeHash, 12156724549839578189ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_we_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8383730315853795168ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_open_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10147349779409269762ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_close_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11346715747517102663ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_arm_fresh_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9057299455860716406ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_cancel_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3593043710349251217ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_initset_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15497280719574773689ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_to_draw_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10582482934155904610ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_to_maap_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6970022004112396969ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ev_maap_rel_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14352479819855666740ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__set_conflict_w = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 3332534137561846086ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__set_tmr_w = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 7898514506110291002ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__set_lsn_w = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 9425118492722719375ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__set_init_w = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 3692962047496817645ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__set_rel_w = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 9124167839629117629ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__clr_disp_w = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 15181857047642042105ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__clr_relq_w = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 15234788388232009758ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__clr_arm_w = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 8937011308586966966ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__xs_r = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 8684263989760631276ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__init_cnt_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 14198942819674182442ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__src_txn_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10008881713328764617ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__src_tmr_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 353086266591265353ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__src_strq_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15251659461553876455ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__msg_x_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 4261771301955430543ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__status_x_r = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 3263555687085181094ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__ctlr_x_r = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 6463019738230077731ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__seq_x_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 7919679957760548027ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__uid16_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 18218683239598712983ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__rxslot_r = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 4503193307871551090ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__sink_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9860170643085499398ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__tkkind_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 2738719528557049694ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__tkfail_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7286624878043397859ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__errflow_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3990220786837084045ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__preL_talker_eid_r = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 13151073698661701735ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__preL_talker_uid_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 5811162188710418364ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__preL_ctlr_eid_r = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 16082651587658726825ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__preL_sw_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17630332287486887701ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__preL_started_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12406911862593362318ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__strtL_val_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5926051505983317451ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__strq_pend_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 711164800520806099ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__strq_busy_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7508811844209946278ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__strq_done_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14612972399077273221ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__strq_fail_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5023268130335306016ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__strq_tmo_r = VL_SCOPED_RAND_RESET_I(13, __VscopeHash, 10359522258004308255ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__strq_sink_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 4746987806892838007ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__strq_val_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 119100797823904456ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__dbg_strq_drop_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 7183348806431733340ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__strt_was_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12814139745163599666ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__bnd_was_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9226743572433081813ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__bind_act_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 397776724364019211ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__tk_eid_f_r = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 12390146340078997140ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__tk_uid_f_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 15431586340644466432ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__flags_f_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 16887235832811558236ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__sid_f_r = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 17159669063564839617ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__da_f_r = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 5878003264006399507ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__vlan_f_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 15551840527055433812ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__f_idx_r = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 10513783255808592194ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__f_cap_idx_r = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 15094337458636434471ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__f_cap_v_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 370695755601159737ull);
    VL_SCOPED_RAND_RESET_W(384, vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__rec_r, __VscopeHash, 17737042343762347135ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__evt_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 15115932260413416944ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__apend_r = VL_SCOPED_RAND_RESET_I(17, __VscopeHash, 7504472300566405085ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__ord_r = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 15717606674128863680ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__cellmut_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2898476433437188333ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__bk_r = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 16038710728975078763ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__bmsg_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 6328841871198895934ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__bstat_r = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 1053889702454101404ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__bidx_r = VL_SCOPED_RAND_RESET_I(6, __VscopeHash, 8068009403256069385ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__bwait_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5949912271558188692ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__bslot_r = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 4052270290709193177ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__probe_ctr_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 15002077224390955775ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__draw_issued_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14435345846403068997ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__pendexp_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 6183964341869934577ull);
    for (int __Vi0 = 0; __Vi0 < 2; ++__Vi0) {
        VL_SCOPED_RAND_RESET_W(384, vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__rec_ram_r[__Vi0], __VscopeHash, 15504512090111252943ull);
    }
    VL_SCOPED_RAND_RESET_W(384, vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__rec_rdata_r, __VscopeHash, 16366718861300829098ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__recwr_en_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9495794895537610656ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__recwr_addr_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2059141257157813033ull);
    for (int __Vi0 = 0; __Vi0 < 128; ++__Vi0) {
        vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__trom_r[__Vi0] = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 9909661938597663196ull);
    }
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__trom_rdata_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 9011064822222188906ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__evt_w = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 13075228413320174004ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__pend_any_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10269035528596502155ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__pend_sink_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9209486014793488644ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__f_cnt_w = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 1676700278830368909ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__res_acts_w = VL_SCOPED_RAND_RESET_I(17, __VscopeHash, 12402074346389034278ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__cur_act_w = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 9376381117939798889ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__b_msg_w = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 13522339146677637836ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__b_status_w = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 15902974356839332730ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__b_sid_w = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 2591873675297476982ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__b_tkeid_w = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 10888917442997455597ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__b_tkuid_w = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 2149768332599111067ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__b_cc_w = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 13432042123285002998ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__b_flags_w = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 1681959217001927674ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__b_vlan_w = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 8538195103004414707ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__b_da_w = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 17335378979267429711ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__link_q_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2783353931936146853ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__enable_q_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6718144066205054797ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__bound_q_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 7721081792735673640ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__link_fall_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1631331781234389742ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__enable_rise_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16371060980319939606ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__enable_fall_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13871138712816610090ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__bound_fall_w = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 7243396163354048353ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__rx_st_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 8734208100117007949ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__rxq_msg_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 15425875738784058016ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__rxq_eid_r = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 6708360001250005115ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__rxq_vt_r = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 16874581424933851359ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__rxq_if_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11636646642013403289ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__rxq_slot_r = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 7264855281449050510ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__rd_ptr_r = VL_SCOPED_RAND_RESET_I(6, __VscopeHash, 15151440968600693133ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__cap_vld_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3788152847187319430ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__cap_idx_r = VL_SCOPED_RAND_RESET_I(6, __VscopeHash, 12348805922032386495ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__rx_aidx_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 4590360016703215681ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__rx_gm_r = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 1776643728473991052ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__rx_dom_r = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 2595123641761418796ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__rx_ifx_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 195857381587510567ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__sink_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15927618175711180350ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__rx_have_slot_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6883147001759410550ull);
    for (int __Vi0 = 0; __Vi0 < 2; ++__Vi0) {
        vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__disc_rec_r[__Vi0] = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 8729992208912089161ull);
    }
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__disc_rec_q_r = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 5292841500957340762ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__rec_wr_en_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 462189933047918812ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__disc_st_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 5320889397907353487ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__gm_dom_ok_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17397424102228065162ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__ev_dep_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5744108959910355165ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__ev_disc_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17233691202022978929ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__st_set_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7443584485822206683ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__st_clr_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16877324426057233037ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__iter_cancel_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12182624923206356688ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__noadp_exp_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16529995178782758799ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__txn_in_valid_q_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13466460043961128376ull);
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__adv_st_r[__Vi0] = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 7596011446548895062ull);
    }
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__adv_startup_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13708896147475114815ull);
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__tpend_r[__Vi0] = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 14637406006215410424ull);
    }
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__tpend_deadline_r[__Vi0] = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 8075146355739975846ull);
    }
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__pend_avail_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12156194899794864252ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__pend_dep_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16028414542216591013ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__adv_exp_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17378271365949749119ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__bld_done_avail_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2891536685326890399ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__bld_take_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 18285195707687150942ull);
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__aidx_r[__Vi0] = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 2960088142161055300ull);
    }
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__draw_act_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9110805619264310266ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__draw_if_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16127981588304630388ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__draw_kind_r = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 12378771775112269629ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__draw_req_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13989640489417433809ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__draw_req_kind_r = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 1537142358551797137ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__draw_need_kind_w = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 11120345414146704046ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__bld_st_r = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 14929030709564074710ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__bld_dep_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16515047105715344302ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__bld_if_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8075463517282538794ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__bld_slot_r = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 16480176253016106287ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__bld_idx_r = VL_SCOPED_RAND_RESET_I(7, __VscopeHash, 4884372900401047662ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__bld_gm_r = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 12079662125608977483ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__bld_dom_r = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 9858328750331053322ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__bld_aidx_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 2157498674284763631ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__pick_vld_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8934895713202096608ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__pick_dep_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4881909499227875647ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__pick_if_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3274424892727725191ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__ucancel_pend_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 3885688181911168913ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__ucancel_issue_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16337051374368716919ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__ucancel_sink_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3695091309707495560ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__iter_port_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9495351654822362294ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__pend_dep_evt_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 11549373682830087852ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__drain_any_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12231448080068521832ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__drain_sink_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17917133432136256296ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__iter_evt_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11454222201466717878ull);
    VL_SCOPED_RAND_RESET_W(393, vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_normalizer__DOT__txn_r, __VscopeHash, 4749845492063411851ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_normalizer__DOT__txn_valid_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 582959952518818152ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_normalizer__DOT__accept_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7546213042617186279ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__fr_st_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 6245904681258032010ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__idx_r = VL_SCOPED_RAND_RESET_I(11, __VscopeHash, 8624326852093517273ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__da_own_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 241031220537174765ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__da_mcast_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13009659229337224043ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__da_maap_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9830333600498162681ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__da_msrp_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16398358466139259489ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__da_mvrp_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 18005654001593124617ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__et_hi_r = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 2902011741297963165ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__vpushed_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4088483520560255584ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__alloc_req_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12729424740392170141ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__slot_held_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8575389540477811324ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__slot_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 4997086161829501000ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__cdl_known_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16988308099029405439ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__subtype_r = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 12072434864444814679ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__msg_type_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 16888284225910022971ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__status_r = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 8579165163645551535ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__cdl_r = VL_SCOPED_RAND_RESET_I(11, __VscopeHash, 12338524621085512003ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__src_mac_r = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 1709848696031042384ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__target_eid_r = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 3761562556388448464ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__ctlr_eid_r = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 9096660556039398860ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__seq_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 10333976761065824882ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__opcode_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 4488370517538212976ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__desc_type_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 6524423166725448502ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__desc_index_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 12555012398253377909ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__tuid_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 4168857079446341121ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__luid_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 12003429432772536655ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__u_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5612760680366057809ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__cr_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 984589365871167581ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__end_pend_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16811006707987224418ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__end_pass_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10767191879956669105ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__abort_pend_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11559763383441770517ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__cp_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 14401019581881764395ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__p1_en_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17250433920740380278ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__p2_en_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13820525912465289501ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__p1_d_r = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 3795127543886025890ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__p2_d_r = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 1624780114398349497ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__p1_l_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8214284068364053783ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__p2_l_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14330174048931575169ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__hdr_protocol_r = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 9821930041465664833ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__hdr_msg_type_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 7546973190172454378ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__hdr_status_r = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 13648142774479077351ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__hdr_cdl_r = VL_SCOPED_RAND_RESET_I(11, __VscopeHash, 11413417505295282734ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__hdr_src_mac_r = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 13382758394506648838ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__hdr_ctlr_eid_r = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 16458796656935991654ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__hdr_target_eid_r = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 9603121099256472374ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__hdr_seq_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 7809868518937484060ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__hdr_opcode_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 10629004901950878756ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__hdr_u_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17038842431811177572ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__hdr_cr_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10414203151238881626ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__hdr_operands_r = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 13177798868023861906ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__hdr_rx_slot_r = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 4193713891994802416ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__cnt_da_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 13785948764178886982ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__cnt_et_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 12177339868808444817ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__cnt_sub_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 17513216891649781941ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__cnt_ver_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 7088548506117496795ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__cnt_len_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 14746163649488164796ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__end_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6910603659813476963ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__pidx_w = VL_SCOPED_RAND_RESET_I(11, __VscopeHash, 14945250803720115537ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__da_own_a_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12374026437766092635ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__da_mcast_a_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13280049328138280197ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__da_maap_a_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1079847166112991526ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__da_msrp_a_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9340297194780230916ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__da_mvrp_a_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2767805371438067856ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__da_1722_a_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9634738727957505768ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__da_mrp_a_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8862490169140686006ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__et_w = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 15059059334134432628ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__slot_now_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4061047136401421068ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__in_budget_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10309010528591357340ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__pdu_byte_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 184286902926280281ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__sub_fail_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11713436386654380366ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__ver_fail_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9960101091224070417ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__fail_now_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6141896236123406563ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__wr_en_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15582362093789645258ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__v1_pass_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8657432197856635348ull);
    for (int __Vi0 = 0; __Vi0 < 64; ++__Vi0) {
        vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__mrp_mem_r[__Vi0] = VL_SCOPED_RAND_RESET_I(9, __VscopeHash, 1847811375677106570ull);
    }
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__wptr_r = VL_SCOPED_RAND_RESET_I(7, __VscopeHash, 13259617910636252406ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__rptr_r = VL_SCOPED_RAND_RESET_I(7, __VscopeHash, 996650578657843001ull);
    for (int __Vi0 = 0; __Vi0 < 16; ++__Vi0) {
        vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__vq_r[__Vi0] = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8654739888195385936ull);
    }
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__vwptr_r = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 8639680209297882046ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__vrptr_r = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 7905826516474018186ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__od_last_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14219059716001208066ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__od_data_r = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 8226326243899999823ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__out_valid_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 845297198526990890ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__out_emit_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9107229532150431163ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__vq_full_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1432305271641272089ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__push_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8516631996906745767ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__vd_push_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14944792098022904151ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__vd_val_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14311952345587728900ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__rd_fire_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3848798789517474472ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__retire_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1748190129642265211ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_ca_builder__DOT__c_st_r = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 14193378413860904374ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_ca_builder__DOT__owner_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 6210747888518996523ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_ca_builder__DOT__ctlr_eid_r = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 12856444050539292281ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_ca_builder__DOT__ctlr_mac_r = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 17383275566065869499ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_ca_builder__DOT__seq_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 10037107432724117161ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_ca_builder__DOT__slot_r = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 6265471257785964959ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_ca_builder__DOT__byte_r = VL_SCOPED_RAND_RESET_I(6, __VscopeHash, 5340035249399371111ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_ca_builder__DOT__alloc_wait_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5451868904605164103ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_ca_builder__DOT__cancel_hit_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17514824593166749458ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__valid_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 7314928309115124174ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__retried_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 9986314717279652070ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__exp_pend_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 13474756187806762774ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__await_tx_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 3733410426696103564ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__accept_pend_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 4432867086192786951ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__cancel_pend_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 6043359471269094377ull);
    for (int __Vi0 = 0; __Vi0 < 16; ++__Vi0) {
        vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__owner_r[__Vi0] = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 17201593125014809355ull);
    }
    for (int __Vi0 = 0; __Vi0 < 16; ++__Vi0) {
        VL_SCOPED_RAND_RESET_W(112, vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__key_r[__Vi0], __VscopeHash, 13752878957547096428ull);
    }
    for (int __Vi0 = 0; __Vi0 < 16; ++__Vi0) {
        vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__seq_r[__Vi0] = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 4990381852444961353ull);
    }
    for (int __Vi0 = 0; __Vi0 < 16; ++__Vi0) {
        vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__tslot_r[__Vi0] = VL_SCOPED_RAND_RESET_I(6, __VscopeHash, 3578547373082222007ull);
    }
    for (int __Vi0 = 0; __Vi0 < 16; ++__Vi0) {
        vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__tout_r[__Vi0] = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 11572469247677136761ull);
    }
    for (int __Vi0 = 0; __Vi0 < 16; ++__Vi0) {
        vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__txs_r[__Vi0] = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 12278904041383376851ull);
    }
    for (int __Vi0 = 0; __Vi0 < 16; ++__Vi0) {
        vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__seq_ctr_r[__Vi0] = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 10488194042096135514ull);
    }
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__free_ok_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3993972728429835434ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__free_ix_w = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 7463516234518045648ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__cancel_work_w = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 10735130154199922696ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__cancel_pend_ok_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17111098157352531278ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__cancel_pend_ix_w = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 6814665725313522594ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__accept_ok_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8355554351789290657ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__accept_pend_ix_w = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 6658350984930225926ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__hit_ok_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 723121770300901597ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__hit_ix_w = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 18084240924712826601ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__cancel_hit_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8750696347454351112ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__cancel_ix_w = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 10177899514351064157ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__accept_hit_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4671766398741055ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__accept_ix_w = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 11311893659041524503ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__pend_ok_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4004871936008544008ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__pend_ix_w = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 5486025692091008955ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__ev_rsp_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11519715534739307163ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__ev_cancel_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3403332449265308789ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__ev_accept_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6321990731416230337ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__ev_exp_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17186171550584774480ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__ev_iss_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17877141692179155704ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_trace__DOT__wr_count_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 12474804334302390711ull);
    for (int __Vi0 = 0; __Vi0 < 256; ++__Vi0) {
        VL_SCOPED_RAND_RESET_W(128, vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_trace__DOT__mem_r[__Vi0], __VscopeHash, 8597075543328687701ull);
    }
    VL_SCOPED_RAND_RESET_W(128, vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_trace__DOT__rd_word_r, __VscopeHash, 14954112543886599064ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_trace__DOT__rd_lane_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 16931442950833276269ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__valid_r = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 1705211641941381761ull);
    for (int __Vi0 = 0; __Vi0 < 8; ++__Vi0) {
        vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__cls_r[__Vi0] = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 13267456505691990964ull);
    }
    for (int __Vi0 = 0; __Vi0 < 8; ++__Vi0) {
        vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__key_r[__Vi0] = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 12651628021201398260ull);
    }
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__barrier_pend_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4098041368853162600ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__ff_valid_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7033126782116303143ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__ff_id_w = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 16004187927845111824ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_r = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 18391036045402078417ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__ctr_r = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 3978065668826062139ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__seeded_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4748811400650290815ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__link_up_q_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 444302652750576195ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__lfsr_next_w = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 7743868641676587031ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__seed_w = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 2541734537032092424ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__kind_r = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 8872729439340791500ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__busy_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15378324759021714839ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__span_w = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 14625384873519606934ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__us_cnt_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 11474385100301186134ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__ms_cnt_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 11006388623056077657ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__now_ms_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 12404228717482010742ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__tick_ms_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12822905185292962968ull);
    for (int __Vi0 = 0; __Vi0 < 61; ++__Vi0) {
        vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__slot_ram_r[__Vi0] = VL_SCOPED_RAND_RESET_Q(40, __VscopeHash, 17676057903791678736ull);
    }
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__sweep_rdata_r = VL_SCOPED_RAND_RESET_Q(40, __VscopeHash, 7964007965145482160ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__sweep_addr_r = VL_SCOPED_RAND_RESET_I(6, __VscopeHash, 8502818446485838982ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__sweep_act_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6792679252779281326ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__sweep_pend_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4230913377359705816ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__chk_valid_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10443040548464718367ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__chk_slot_r = VL_SCOPED_RAND_RESET_I(6, __VscopeHash, 10675338993995837706ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__exp_fire_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4142116195623391079ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__armed_r = VL_SCOPED_RAND_RESET_Q(61, __VscopeHash, 9591285598642566365ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__arm_q_valid_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9299703093707246590ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__arm_q_slot_r = VL_SCOPED_RAND_RESET_I(6, __VscopeHash, 8690389374961866087ull);
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__mapi_pref_r[__Vi0] = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 1688817395975509519ull);
    }
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__mapi_len_r[__Vi0] = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 6288333029338759377ull);
    }
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__mapo_pref_r[__Vi0] = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 9464660826282263510ull);
    }
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__mapo_len_r[__Vi0] = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 14105666258739642251ull);
    }
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__rec_base_w = VL_SCOPED_RAND_RESET_I(18, __VscopeHash, 14639149767070721390ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__rec_len_w = VL_SCOPED_RAND_RESET_I(12, __VscopeHash, 517068223914728582ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__rec_hit_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9121254955308431111ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__b_mapo_w = VL_SCOPED_RAND_RESET_I(18, __VscopeHash, 1746736461724634690ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__img_base_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 15331773508598924225ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__img_len_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 15227148096809908515ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__seq_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 10491385829238550728ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__verdict_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 1752222748208476443ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__img_valid_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17812991068733711557ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__backed_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15585100440129820477ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__stale_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17215334427257218543ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__ever_backed_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8957101294008537974ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__reg_we_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1824720681031505706ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__hb_kick_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10311398303362678284ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__commit_ack_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11037694617346164403ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__commit_start_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13414320256511534118ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__img_live_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17535887749565572794ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__arm_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2323633885954997732ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__attest_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4712160014066782401ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__release_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13472236454487584105ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__reload_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4324579862072950851ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__rebase_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5234925125191895817ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__reload_ok_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12236724512889964246ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__commit_busy_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9200227407356770849ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__cap_open_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13497579223599832466ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__cap_hold_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10051237188471880857ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__cap_valid_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 571705789609016997ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__cap_att_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11550849898544636718ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__ack_ref_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7065421096831619255ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__arm_ref_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11502576007057333214ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__cap_id_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 3797854228354649981ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__hold_r = VL_SCOPED_RAND_RESET_I(6, __VscopeHash, 1942329538368371403ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__dirty_live_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15980456619578449148ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__dirty_cap_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8988053048366785912ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__pend_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6617076795469299087ull);
    VL_SCOPED_RAND_RESET_W(256, vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__open_r, __VscopeHash, 4294376888683793910ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__dirty_img_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13026945183333611410ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__arm_ok_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14956138361222543168ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__ack_ok_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15039394608166906338ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__close_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2901064858007860471ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__void_grant_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 18045858243801758807ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__gnt_opmut_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13912081308908754848ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__rec_close_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2544897649450240271ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__op_region_r = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 4431122850252435466ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__op_mut_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4573384406529927637ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__op_full_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5939504224894031174ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__set_q_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10829354132672636602ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__ld_ok_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2073355871299039270ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__ld_pend_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4713966638734575447ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__rl_ref_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13653784500270740265ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__ld_acc_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15236185818616391466ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__mut_defer_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5310427597453686492ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__pend_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4009921523896137907ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__ms_div_r = VL_SCOPED_RAND_RESET_I(17, __VscopeHash, 14753739419750733960ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__alive_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 6145017484986230722ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__commit_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 6554850040484659551ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__loss_ev_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15635048934677818049ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__backed_n_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10293514592279477687ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__dirty_live_n_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11997143651450447724ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__dirty_cap_n_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9789536235133865525ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__void_hard_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8741597964043418906ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__st_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 7851036459306643047ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__addr_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 17548593208308622905ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__cnt_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 1434702659399532167ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__byte_r = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 10728859527009738055ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__gnt_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 18020731840447235025ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__done_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14962296609031964520ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__err_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5641925380982564461ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__was_write_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3244566229008484903ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__eff_len_w = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 7663341478230697961ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__span_ok_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 60412839515870834ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__wc_valid_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7283049012672235969ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__wc_addr_r = VL_SCOPED_RAND_RESET_I(29, __VscopeHash, 1017687424458621681ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__wc_data_r = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 17129430111873820922ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__wc_hit_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15293055351774741261ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__mut_req_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11407880574965116539ull);
    vlSelf->milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__gnt_now_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13150872266457798525ull);
    for (int __Vi0 = 0; __Vi0 < 512; ++__Vi0) {
        VL_SCOPED_RAND_RESET_W(74, vlSelf->milan_datapath__DOT__pp_shadow__DOT__ctl_fifo__DOT__mem[__Vi0], __VscopeHash, 18085694665017676066ull);
    }
    for (int __Vi0 = 0; __Vi0 < 2; ++__Vi0) {
        VL_SCOPED_RAND_RESET_W(74, vlSelf->milan_datapath__DOT__pp_shadow__DOT__ctl_fifo__DOT__m_axis_pipe_reg[__Vi0], __VscopeHash, 16406675358225914501ull);
    }
    for (int __Vi0 = 0; __Vi0 < 9; ++__Vi0) {
        vlSelf->milan_datapath__DOT__ethernet_counters__DOT__counters[__Vi0] = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 7988988791378497093ull);
    }
    vlSelf->milan_datapath__DOT__ethernet_counters__DOT__rollover_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14981883684186643757ull);
    vlSelf->milan_datapath__DOT__ethernet_counters__DOT____Vcellout__event_counter_gen__BRA__0__KET____DOT__counter_inst__count = 0;
    vlSelf->milan_datapath__DOT__ethernet_counters__DOT____Vcellout__event_counter_gen__BRA__1__KET____DOT__counter_inst__count = 0;
    vlSelf->milan_datapath__DOT__ethernet_counters__DOT____Vcellout__event_counter_gen__BRA__2__KET____DOT__counter_inst__count = 0;
    vlSelf->milan_datapath__DOT__ethernet_counters__DOT____Vcellout__event_counter_gen__BRA__3__KET____DOT__counter_inst__count = 0;
    vlSelf->milan_datapath__DOT__ethernet_counters__DOT____Vcellout__event_counter_gen__BRA__4__KET____DOT__counter_inst__count = 0;
    vlSelf->milan_datapath__DOT__ethernet_counters__DOT____Vcellout__event_counter_gen__BRA__5__KET____DOT__counter_inst__count = 0;
    vlSelf->milan_datapath__DOT__ethernet_counters__DOT____Vcellout__event_counter_gen__BRA__6__KET____DOT__counter_inst__count = 0;
    vlSelf->milan_datapath__DOT__ethernet_counters__DOT____Vcellout__event_counter_gen__BRA__7__KET____DOT__counter_inst__count = 0;
    vlSelf->milan_datapath__DOT__ethernet_counters__DOT____Vcellout__event_counter_gen__BRA__8__KET____DOT__counter_inst__count = 0;
    vlSelf->milan_datapath__DOT__aaf_latency_tap_bank__DOT__aaf_tx_acc_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15649585903221762135ull);
    vlSelf->milan_datapath__DOT__aaf_latency_tap_bank__DOT__aaf_tx_inframe_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13525762549493998000ull);
    vlSelf->milan_datapath__DOT__aaf_latency_tap_bank__DOT__mac_rx_inframe_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11343798644849730236ull);
    vlSelf->milan_datapath__DOT__aaf_latency_tap_bank__DOT__ltap_txmac_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4469834266764611989ull);
    vlSelf->milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__ltap_txp_q_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 12392252541980820821ull);
    vlSelf->milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__ltap_rxp_q_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 2804781832859555512ull);
    vlSelf->milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__cyc_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 10905981909215986137ull);
    vlSelf->milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__active_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 18000252088875312534ull);
    vlSelf->milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__stg_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 3141318676457106143ull);
    vlSelf->milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__prevc_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 9185798217548551066ull);
    vlSelf->milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__epoch_pend_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 2552901448844973066ull);
    vlSelf->milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__epoch_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 13346631629153459251ull);
    vlSelf->milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__to_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 16635967177067751953ull);
    vlSelf->milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__samples_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 9720994278154065597ull);
    vlSelf->milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__timeouts_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 9822142373815838823ull);
    for (int __Vi0 = 0; __Vi0 < 3; ++__Vi0) {
        vlSelf->milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__last_r[__Vi0] = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 14423119810355379048ull);
    }
    for (int __Vi0 = 0; __Vi0 < 3; ++__Vi0) {
        vlSelf->milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__min_r[__Vi0] = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 14964839595840569242ull);
    }
    for (int __Vi0 = 0; __Vi0 < 3; ++__Vi0) {
        vlSelf->milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__max_r[__Vi0] = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 12234981941991708893ull);
    }
    vlSelf->milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__dsat_w = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 11141774580621774251ull);
    vlSelf->milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__didx_w = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 2946077040893553691ull);
    vlSelf->milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__nadv_w = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 3759928423970965800ull);
    vlSelf->milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__nadv0_w = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 4783897208739059296ull);
    vlSelf->milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__active_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 18383410961328432965ull);
    vlSelf->milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__stg_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 7104080215994185476ull);
    vlSelf->milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__prevc_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 9775765075857490465ull);
    vlSelf->milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__epoch_pend_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 7596362075715979780ull);
    vlSelf->milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__epoch_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 17574304916487100989ull);
    vlSelf->milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__to_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 9689235462499786540ull);
    vlSelf->milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__samples_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 12728758397555321427ull);
    vlSelf->milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__timeouts_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 16178254827531417615ull);
    for (int __Vi0 = 0; __Vi0 < 3; ++__Vi0) {
        vlSelf->milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__last_r[__Vi0] = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 5304482821870144011ull);
    }
    for (int __Vi0 = 0; __Vi0 < 3; ++__Vi0) {
        vlSelf->milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__min_r[__Vi0] = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 1355520974836447462ull);
    }
    for (int __Vi0 = 0; __Vi0 < 3; ++__Vi0) {
        vlSelf->milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__max_r[__Vi0] = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 18057055351118720766ull);
    }
    vlSelf->milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__dsat_w = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 16336537211300007718ull);
    vlSelf->milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__didx_w = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 4479851874182427968ull);
    vlSelf->milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__nadv_w = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 18006278022580802221ull);
    vlSelf->milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__nadv0_w = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 13114401531665109136ull);
    vlSelf->milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__pos_r = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 9765631063469914319ull);
    vlSelf->milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__lhold_r = VL_SCOPED_RAND_RESET_I(24, __VscopeHash, 17220224632502900057ull);
    vlSelf->milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__p1_w = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 4015928105186370163ull);
    for (int __Vi0 = 0; __Vi0 < 4; ++__Vi0) {
        vlSelf->milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__stg_r[__Vi0] = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 15626538650372458635ull);
    }
    vlSelf->milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__stg_wp_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 13247234318528579280ull);
    vlSelf->milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__stg_rp_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 14575243297029245807ull);
    vlSelf->milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__stg_cnt_r = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 5717366874026349944ull);
    for (int __Vi0 = 0; __Vi0 < 512; ++__Vi0) {
        vlSelf->milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__fifo_r[__Vi0] = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 297334776200572226ull);
    }
    vlSelf->milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__wptr_r = VL_SCOPED_RAND_RESET_I(10, __VscopeHash, 12899305383254223625ull);
    vlSelf->milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__rptr_r = VL_SCOPED_RAND_RESET_I(10, __VscopeHash, 10345082901790545033ull);
    vlSelf->milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__fill_w = VL_SCOPED_RAND_RESET_I(10, __VscopeHash, 7461485207038989896ull);
    vlSelf->milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__cdc_wen_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14701217712712923670ull);
    vlSelf->milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__cdc_wdata_r = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 721190254482443778ull);
    vlSelf->milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__cdc_wfull_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7794214198742978928ull);
    vlSelf->milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__ms_div_r = VL_SCOPED_RAND_RESET_I(17, __VscopeHash, 14549205714899318864ull);
    vlSelf->milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__conv_ms_r = VL_SCOPED_RAND_RESET_I(7, __VscopeHash, 7720020888755070673ull);
    vlSelf->milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__was_filled_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11562345301486076182ull);
    vlSelf->milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__pushA_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10993484480241482404ull);
    vlSelf->milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__pushB_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16264217931063933185ull);
    vlSelf->milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__pairA_w = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 1346890366976414338ull);
    vlSelf->milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__pairB_w = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 14526895245696190763ull);
    vlSelf->milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__stg_drain_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6811775163955888517ull);
    vlSelf->milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__stg_space_w = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 8640671458113247037ull);
    vlSelf->milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__wA_ok_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6863495994505845597ull);
    vlSelf->milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__wB_ok_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15970572415030042247ull);
    vlSelf->milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__stg_wr_n_w = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 2434175711617030479ull);
    vlSelf->milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__stg_drop_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10827797995250520728ull);
    vlSelf->milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__prefill_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9869767004989633528ull);
    vlSelf->milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__arst_n_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 5765597695171486388ull);
    vlSelf->milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__rd_empty_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17140762555644307664ull);
    vlSelf->milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__rd_pair_w = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 13446133948111077384ull);
    vlSelf->milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__rd_en_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7851982691073516608ull);
    vlSelf->milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__adiv_r = VL_SCOPED_RAND_RESET_I(9, __VscopeHash, 755125253113134100ull);
    vlSelf->milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__shift_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 5141898114419003584ull);
    vlSelf->milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__dbg_sh_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 17675006794609586613ull);
    vlSelf->milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__dbg_frame_a_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 9097434007545026377ull);
    vlSelf->milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__pend_right_r = VL_SCOPED_RAND_RESET_I(24, __VscopeHash, 1592337628700772438ull);
    vlSelf->milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__underrun_a_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 7915059837949334438ull);
    vlSelf->milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__bit_r = VL_SCOPED_RAND_RESET_I(6, __VscopeHash, 8412296246686189179ull);
    vlSelf->milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__under_meta_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 12198055048420856788ull);
    vlSelf->milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__under_sync_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 3907700736420722308ull);
    vlSelf->milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__dbgf_meta_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 4738738567499543276ull);
    vlSelf->milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__dbgf_sync_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 50283463061671655ull);
    vlSelf->milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__u_clr_under_cdc__DOT__src_level = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4158626396930396270ull);
    vlSelf->milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__u_clr_under_cdc__DOT__sync = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 16607369193527480790ull);
    for (int __Vi0 = 0; __Vi0 < 16; ++__Vi0) {
        vlSelf->milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__u_cdc__DOT__mem_r[__Vi0] = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 6622571710003288768ull);
    }
    vlSelf->milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__u_cdc__DOT__wptr_bin_r = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 17481025007313027037ull);
    vlSelf->milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__u_cdc__DOT__wptr_gray_r = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 11610797580783187703ull);
    vlSelf->milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__u_cdc__DOT__rptr_bin_r = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 3461850140231179378ull);
    vlSelf->milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__u_cdc__DOT__rptr_gray_r = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 1789632774265781463ull);
    vlSelf->milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__u_cdc__DOT__rgray_w1_r = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 8156513846963390685ull);
    vlSelf->milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__u_cdc__DOT__rgray_w2_r = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 903452659236422217ull);
    vlSelf->milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__u_cdc__DOT__wgray_r1_r = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 4644718734027076255ull);
    vlSelf->milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__u_cdc__DOT__wgray_r2_r = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 543060870551218166ull);
    vlSelf->milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__u_cdc__DOT__wptr_bin_n = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 17090397731848891693ull);
    vlSelf->milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__u_cdc__DOT__wptr_gray_n = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 13985841412882431879ull);
    vlSelf->milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__u_cdc__DOT__rptr_bin_n = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 6273939600865911900ull);
    vlSelf->milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__u_cdc__DOT__rptr_gray_n = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 16661469293255464872ull);
    vlSelf->milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__arst_sync_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 11619779898570861359ull);
    vlSelf->milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__tick_div_r = VL_SCOPED_RAND_RESET_I(15, __VscopeHash, 6941531551319956634ull);
    vlSelf->milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__tick_a_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8545647611478462754ull);
    vlSelf->milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__locked_sync_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 1745837030565256401ull);
    vlSelf->milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__psbusy_sync_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 15419504392202772199ull);
    vlSelf->milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__psfault_sync_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 14736950254529441852ull);
    vlSelf->milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__ps_busy_ps_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3250579978994282202ull);
    vlSelf->milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__ps_fault_ps_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7542390822911592473ull);
    vlSelf->milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__state_r = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 8001903630719396085ull);
    vlSelf->milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__dstate_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 4091947002557018570ull);
    vlSelf->milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__tick_cnt_r = VL_SCOPED_RAND_RESET_I(10, __VscopeHash, 11111978174438365363ull);
    vlSelf->milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__win_start_r = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 13551802875299335538ull);
    vlSelf->milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__win_valid_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12175314228100954804ull);
    vlSelf->milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__win_skip_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 14384010732966366789ull);
    vlSelf->milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__ew_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 11627751675869233751ull);
    vlSelf->milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__disc_run_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 17785202736916315017ull);
    vlSelf->milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__disc_cnt_r = VL_SCOPED_RAND_RESET_I(6, __VscopeHash, 12495334039247330377ull);
    vlSelf->milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__integ_r = VL_SCOPED_RAND_RESET_I(24, __VscopeHash, 10246020060512661598ull);
    vlSelf->milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__u_cmd_r = VL_SCOPED_RAND_RESET_I(24, __VscopeHash, 11461358087524829170ull);
    vlSelf->milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__lock_cnt_r = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 15038513309621532791ull);
    vlSelf->milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__pp_seq_r = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 3397084741920954052ull);
    vlSelf->milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__pp_run_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11781225111205515651ull);
    vlSelf->milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__pp_d_r = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 18172854647922590050ull);
    vlSelf->milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__pp_spann_r = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 12056569907774400204ull);
    vlSelf->milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__pp_locerr_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 5520118000190301118ull);
    vlSelf->milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__pp_rate_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 12310750090942566639ull);
    vlSelf->milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__pp_isum_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 13531924972631513995ull);
    vlSelf->milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__pp_thr_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3930500975056992225ull);
    vlSelf->milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__pp_ig_r = VL_SCOPED_RAND_RESET_I(24, __VscopeHash, 9911360701222082956ull);
    vlSelf->milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__pp_un_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 14674169965380148901ull);
    vlSelf->milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__pp_ut_r = VL_SCOPED_RAND_RESET_I(24, __VscopeHash, 709789492214545154ull);
    vlSelf->milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__pp_du_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 12089670643531878355ull);
    vlSelf->milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__u_gain_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 13954565267405244904ull);
    vlSelf->milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__acc_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 14800197632174590781ull);
    vlSelf->milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__hs_send_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10343533513370093637ull);
    vlSelf->milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__hs_data_r = VL_SCOPED_RAND_RESET_I(15, __VscopeHash, 11832398884529052294ull);
    vlSelf->milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__ps_hold_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6088439436423558861ull);
    vlSelf->milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__drp_pass_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 590727073402988909ull);
    vlSelf->milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__rd_second_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2620301314913987821ull);
    vlSelf->milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__repairing_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15140463147160262748ull);
    vlSelf->milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__rd_val_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 7449765302757099402ull);
    vlSelf->milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__verified_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10247491543183279472ull);
    vlSelf->milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__mismatch_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 490695811978306810ull);
    vlSelf->milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__drp_fault_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1072024958454834311ull);
    vlSelf->milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__relock_r = VL_SCOPED_RAND_RESET_I(18, __VscopeHash, 7751707712390928800ull);
    vlSelf->milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__rst_settle_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 12598973018361002124ull);
    vlSelf->milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__exp_val_w = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 10113062304904127254ull);
    vlSelf->milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__exp_mask_w = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 18175128700945335004ull);
    vlSelf->milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__ptp_q_r = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 15418384730948276261ull);
    vlSelf->milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__psrst_sync_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 10485604773314952935ull);
    vlSelf->milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__pstate_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 14885225624640812176ull);
    vlSelf->milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__ps_cnt_r = VL_SCOPED_RAND_RESET_I(14, __VscopeHash, 5270052906721326930ull);
    vlSelf->milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__ps_dir_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7318462042179430439ull);
    vlSelf->milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__pend_v_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 117574268076146972ull);
    vlSelf->milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__pend_r = VL_SCOPED_RAND_RESET_I(15, __VscopeHash, 3705898732959895901ull);
    vlSelf->milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__ps_wd_r = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 16253272370252323768ull);
    vlSelf->milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__u_tick_cdc__DOT__src_level = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12737230810038219004ull);
    vlSelf->milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__u_tick_cdc__DOT__sync = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 9790965214494575254ull);
    vlSelf->milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__u_batch_hs__DOT__src_send_d = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2517125027075489853ull);
    vlSelf->milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__u_batch_hs__DOT__req_tog = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7101727235483008596ull);
    vlSelf->milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__u_batch_hs__DOT__data_hold = VL_SCOPED_RAND_RESET_I(15, __VscopeHash, 10323698129609927802ull);
    vlSelf->milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__u_batch_hs__DOT__ack_sync = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 18336191858756470361ull);
    vlSelf->milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__u_batch_hs__DOT__req_sync = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 15315447054756657750ull);
    vlSelf->milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__u_batch_hs__DOT__dest_out_r = VL_SCOPED_RAND_RESET_I(15, __VscopeHash, 13820377244584414907ull);
    vlSelf->milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__u_batch_hs__DOT__dest_req_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4580948918296233594ull);
    vlSelf->milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__u_batch_hs__DOT__ack_tog = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3632286756775668184ull);
    vlSelf->milan_datapath__DOT__crf_tx__DOT__mtt_ofs_r = VL_SCOPED_RAND_RESET_Q(34, __VscopeHash, 8826988803014119865ull);
    vlSelf->milan_datapath__DOT__crf_tx__DOT__mtt_seen_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 5177801273302737312ull);
    vlSelf->milan_datapath__DOT__crf_tx__DOT__mtt_valid_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12750510200722341568ull);
    vlSelf->milan_datapath__DOT__crf_tx__DOT__dv_num_r = VL_SCOPED_RAND_RESET_Q(34, __VscopeHash, 11937209632215440354ull);
    vlSelf->milan_datapath__DOT__crf_tx__DOT__dv_quot_r = VL_SCOPED_RAND_RESET_Q(34, __VscopeHash, 4442301333650302203ull);
    vlSelf->milan_datapath__DOT__crf_tx__DOT__dv_rem_r = VL_SCOPED_RAND_RESET_I(17, __VscopeHash, 13994644653877496318ull);
    vlSelf->milan_datapath__DOT__crf_tx__DOT__dv_div_r = VL_SCOPED_RAND_RESET_I(17, __VscopeHash, 17781593874424760933ull);
    vlSelf->milan_datapath__DOT__crf_tx__DOT__dv_step_r = VL_SCOPED_RAND_RESET_I(6, __VscopeHash, 6254417844417855175ull);
    vlSelf->milan_datapath__DOT__crf_tx__DOT__dv_busy_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10151922770731959112ull);
    vlSelf->milan_datapath__DOT__crf_tx__DOT__dv_pass2_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5970122857489611439ull);
    vlSelf->milan_datapath__DOT__crf_tx__DOT__dv_rsh_w = VL_SCOPED_RAND_RESET_I(17, __VscopeHash, 11543359930188191135ull);
    vlSelf->milan_datapath__DOT__crf_tx__DOT__dv_ge_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16005539691993659150ull);
    vlSelf->milan_datapath__DOT__crf_tx__DOT__arst_n_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 4702644607541866548ull);
    vlSelf->milan_datapath__DOT__crf_tx__DOT__adiv_r = VL_SCOPED_RAND_RESET_I(9, __VscopeHash, 13973974788862635897ull);
    vlSelf->milan_datapath__DOT__crf_tx__DOT__aevt_cnt_r = VL_SCOPED_RAND_RESET_I(7, __VscopeHash, 5324145493602299683ull);
    vlSelf->milan_datapath__DOT__crf_tx__DOT__aevt_p_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7145376842551796687ull);
    vlSelf->milan_datapath__DOT__crf_tx__DOT__ts_r = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 1152980841155199512ull);
    vlSelf->milan_datapath__DOT__crf_tx__DOT__seq_r = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 16085790371680289529ull);
    vlSelf->milan_datapath__DOT__crf_tx__DOT__frame_pend_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17587723922996360482ull);
    vlSelf->milan_datapath__DOT__crf_tx__DOT__tu_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9055541482634606299ull);
    vlSelf->milan_datapath__DOT__crf_tx__DOT__mr_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1559256346447638954ull);
    vlSelf->milan_datapath__DOT__crf_tx__DOT__vln_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2899678594131139957ull);
    vlSelf->milan_datapath__DOT__crf_tx__DOT__vpcp_r = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 2191961353266714310ull);
    vlSelf->milan_datapath__DOT__crf_tx__DOT__vvid_r = VL_SCOPED_RAND_RESET_I(12, __VscopeHash, 3924147351671677240ull);
    for (int __Vi0 = 0; __Vi0 < 28; ++__Vi0) {
        vlSelf->milan_datapath__DOT__crf_tx__DOT__pdu[__Vi0] = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 11444048398030434914ull);
    }
    for (int __Vi0 = 0; __Vi0 < 64; ++__Vi0) {
        vlSelf->milan_datapath__DOT__crf_tx__DOT__fb[__Vi0] = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 3616455940315271579ull);
    }
    vlSelf->milan_datapath__DOT__crf_tx__DOT__st_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14284557797424822327ull);
    vlSelf->milan_datapath__DOT__crf_tx__DOT__beat_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 15700616228807514895ull);
    vlSelf->milan_datapath__DOT__crf_tx__DOT__u_evt_cdc__DOT__src_level = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14022875488956122426ull);
    vlSelf->milan_datapath__DOT__crf_tx__DOT__u_evt_cdc__DOT__sync = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 9616987612383374399ull);
    vlSelf->milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__in_frame = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7847582356564656787ull);
    vlSelf->milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__pass_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15346095915984653831ull);
    vlSelf->milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__sof = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11829716660200141772ull);
    vlSelf->milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__pass_sof = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9653446831909198493ull);
    for (int __Vi0 = 0; __Vi0 < 16; ++__Vi0) {
        vlSelf->milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_valid[__Vi0] = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1672423968018691440ull);
    }
    for (int __Vi0 = 0; __Vi0 < 16; ++__Vi0) {
        vlSelf->milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_key[__Vi0] = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 7528741892787638466ull);
    }
    for (int __Vi0 = 0; __Vi0 < 16; ++__Vi0) {
        vlSelf->milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_mask[__Vi0] = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 2299591252912849714ull);
    }
    for (int __Vi0 = 0; __Vi0 < 16; ++__Vi0) {
        vlSelf->milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_action[__Vi0] = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 10954790848561287945ull);
    }
    vlSelf->milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__hit = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 670122597648584469ull);
    vlSelf->milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__match_any = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2769185763766042543ull);
    vlSelf->milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__match_act = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 9667804316940675262ull);
    vlSelf->milan_datapath__DOT__g_aif_i2s__DOT__aaf_capture__DOT__tarst_n_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 17763864046163534297ull);
    vlSelf->milan_datapath__DOT__g_aif_i2s__DOT__aaf_capture__DOT__tdiv_r = VL_SCOPED_RAND_RESET_I(9, __VscopeHash, 16254683597677923244ull);
    vlSelf->milan_datapath__DOT__g_aif_i2s__DOT__aaf_capture__DOT__tlrck_q_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7614481560933773485ull);
    vlSelf->milan_datapath__DOT__g_aif_i2s__DOT__aaf_capture__DOT__tshift_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 932508622548335593ull);
    vlSelf->milan_datapath__DOT__g_aif_i2s__DOT__aaf_capture__DOT__tsample_l_r = VL_SCOPED_RAND_RESET_I(24, __VscopeHash, 17512906828053488650ull);
    vlSelf->milan_datapath__DOT__g_aif_i2s__DOT__aaf_capture__DOT__cap_l_r = VL_SCOPED_RAND_RESET_I(24, __VscopeHash, 12922677159370532406ull);
    vlSelf->milan_datapath__DOT__g_aif_i2s__DOT__aaf_capture__DOT__cap_r_r = VL_SCOPED_RAND_RESET_I(24, __VscopeHash, 15639297306179102007ull);
    vlSelf->milan_datapath__DOT__g_aif_i2s__DOT__aaf_capture__DOT__cap_wen_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1936056752155945910ull);
    vlSelf->milan_datapath__DOT__g_aif_i2s__DOT__aaf_capture__DOT__cap_full_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12137722084767775211ull);
    vlSelf->milan_datapath__DOT__g_aif_i2s__DOT__aaf_capture__DOT__cap_rempty_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7454548343908278071ull);
    vlSelf->milan_datapath__DOT__g_aif_i2s__DOT__aaf_capture__DOT__cap_pair_w = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 7049021962996478134ull);
    vlSelf->milan_datapath__DOT__g_aif_i2s__DOT__aaf_capture__DOT__cap_ren_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11127873849737890245ull);
    for (int __Vi0 = 0; __Vi0 < 8; ++__Vi0) {
        vlSelf->milan_datapath__DOT__g_aif_i2s__DOT__aaf_capture__DOT__u_tcdc__DOT__mem_r[__Vi0] = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 17146003219840554903ull);
    }
    vlSelf->milan_datapath__DOT__g_aif_i2s__DOT__aaf_capture__DOT__u_tcdc__DOT__wptr_bin_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 620251564782086375ull);
    vlSelf->milan_datapath__DOT__g_aif_i2s__DOT__aaf_capture__DOT__u_tcdc__DOT__wptr_gray_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 14114780467797652053ull);
    vlSelf->milan_datapath__DOT__g_aif_i2s__DOT__aaf_capture__DOT__u_tcdc__DOT__rptr_bin_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 16712187084362300751ull);
    vlSelf->milan_datapath__DOT__g_aif_i2s__DOT__aaf_capture__DOT__u_tcdc__DOT__rptr_gray_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 4767730239873832104ull);
    vlSelf->milan_datapath__DOT__g_aif_i2s__DOT__aaf_capture__DOT__u_tcdc__DOT__rgray_w1_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 350968170436036390ull);
    vlSelf->milan_datapath__DOT__g_aif_i2s__DOT__aaf_capture__DOT__u_tcdc__DOT__rgray_w2_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 10117174497863038128ull);
    vlSelf->milan_datapath__DOT__g_aif_i2s__DOT__aaf_capture__DOT__u_tcdc__DOT__wgray_r1_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 16631005017524974246ull);
    vlSelf->milan_datapath__DOT__g_aif_i2s__DOT__aaf_capture__DOT__u_tcdc__DOT__wgray_r2_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 7947850466803113519ull);
    vlSelf->milan_datapath__DOT__g_aif_i2s__DOT__aaf_capture__DOT__u_tcdc__DOT__wptr_bin_n = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 16258389488733239601ull);
    vlSelf->milan_datapath__DOT__g_aif_i2s__DOT__aaf_capture__DOT__u_tcdc__DOT__wptr_gray_n = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 16012497644458799473ull);
    vlSelf->milan_datapath__DOT__g_aif_i2s__DOT__aaf_capture__DOT__u_tcdc__DOT__rptr_bin_n = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 6417861304610785835ull);
    vlSelf->milan_datapath__DOT__g_aif_i2s__DOT__aaf_capture__DOT__u_tcdc__DOT__rptr_gray_n = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 18165214867400993403ull);
    vlSelf->milan_datapath__DOT__aaf_rx_depkt__DOT__good_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17256738131828586164ull);
    vlSelf->milan_datapath__DOT__aaf_rx_depkt__DOT__in_frame_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13310215683799157150ull);
    vlSelf->milan_datapath__DOT__aaf_rx_depkt__DOT__wv_idx_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 4150956771800167844ull);
    vlSelf->milan_datapath__DOT__aaf_rx_depkt__DOT__tl_idx_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 13057375267745762422ull);
    vlSelf->milan_datapath__DOT__aaf_rx_depkt__DOT__fw_user = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5752005312799155981ull);
    for (int __Vi0 = 0; __Vi0 < 64; ++__Vi0) {
        vlSelf->milan_datapath__DOT__aaf_rx_depkt__DOT__idxq_r[__Vi0] = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 3784084933833027858ull);
    }
    vlSelf->milan_datapath__DOT__aaf_rx_depkt__DOT__idxq_wp_r = VL_SCOPED_RAND_RESET_I(6, __VscopeHash, 5577644233173959075ull);
    vlSelf->milan_datapath__DOT__aaf_rx_depkt__DOT__idxq_rp_r = VL_SCOPED_RAND_RESET_I(6, __VscopeHash, 17074462168683259374ull);
    vlSelf->milan_datapath__DOT__aaf_rx_depkt__DOT__rstate_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 5837267000956981274ull);
    vlSelf->milan_datapath__DOT__aaf_rx_depkt__DOT__rbeat_r = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 17315250115472460349ull);
    vlSelf->milan_datapath__DOT__aaf_rx_depkt__DOT__vlan_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5271510841197838407ull);
    vlSelf->milan_datapath__DOT__aaf_rx_depkt__DOT__remain_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 17432527769314052164ull);
    vlSelf->milan_datapath__DOT__aaf_rx_depkt__DOT__hold_r = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 3648689227113557827ull);
    vlSelf->milan_datapath__DOT__aaf_rx_depkt__DOT__hold_only_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17177073758092427431ull);
    vlSelf->milan_datapath__DOT__aaf_rx_depkt__DOT__emit_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12838129666757485292ull);
    vlSelf->milan_datapath__DOT__aaf_rx_depkt__DOT__pop_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14675545324066737725ull);
    for (int __Vi0 = 0; __Vi0 < 256; ++__Vi0) {
        VL_SCOPED_RAND_RESET_W(74, vlSelf->milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__mem[__Vi0], __VscopeHash, 14837388420136471902ull);
    }
    for (int __Vi0 = 0; __Vi0 < 2; ++__Vi0) {
        VL_SCOPED_RAND_RESET_W(74, vlSelf->milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg[__Vi0], __VscopeHash, 14183867525397544016ull);
    }
    vlSelf->milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_tready_pipe = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15845664245727519107ull);
    vlSelf->milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__state_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 11172897067832704629ull);
    vlSelf->milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tickdiv_r = VL_SCOPED_RAND_RESET_I(17, __VscopeHash, 7989728970043931816ull);
    vlSelf->milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lfsr_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 9957547606533263147ull);
    vlSelf->milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__lfsr_next_w = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 542284071629328248ull);
    vlSelf->milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__offset_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 14797330970465308157ull);
    vlSelf->milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__probe_left_r = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 2153993046585768995ull);
    vlSelf->milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__timer_ms_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 10226546362500914175ull);
    vlSelf->milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__seed_used_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12496182149945137001ull);
    vlSelf->milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rbeat_r = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 13499019565274589756ull);
    vlSelf->milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__is_maap_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13075844088637485733ull);
    vlSelf->milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rx_msg_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 2752225614203899989ull);
    vlSelf->milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rx_req_start_r = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 16713906991442137837ull);
    vlSelf->milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rx_conf_start_r = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 14493160851013244918ull);
    vlSelf->milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rx_req_cnt_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 1307663788517071716ull);
    vlSelf->milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rx_conf_cnt_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 9410149733716856998ull);
    vlSelf->milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rx_done_p = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13251545266174315522ull);
    vlSelf->milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_busy_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3303454394569907374ull);
    vlSelf->milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_msg_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 1301079848489047426ull);
    vlSelf->milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_conf_start_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 2953908247814018391ull);
    vlSelf->milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_conf_cnt_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 9525233757058620095ull);
    vlSelf->milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat_r = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 188553316597498730ull);
    vlSelf->milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__new_off_w = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 14229856282866922033ull);
    vlSelf->milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__xl_in = VL_SCOPED_RAND_RESET_I(24, __VscopeHash, 3246833815323396871ull);
    vlSelf->milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__xr_in = VL_SCOPED_RAND_RESET_I(24, __VscopeHash, 13679864809238892990ull);
    for (int __Vi0 = 0; __Vi0 < 8; ++__Vi0) {
        vlSelf->milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__bfifo_r[__Vi0] = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 16094534049219825673ull);
    }
    vlSelf->milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__bwr_r = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 3660679493284897835ull);
    vlSelf->milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__brd_r = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 11973415886751816670ull);
    vlSelf->milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__bcnt_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 5457512508907291301ull);
    vlSelf->milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__bpop_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10139425757867947312ull);
    vlSelf->milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__xl1_r = VL_SCOPED_RAND_RESET_I(24, __VscopeHash, 1079358788619364180ull);
    vlSelf->milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__xl2_r = VL_SCOPED_RAND_RESET_I(24, __VscopeHash, 6520039323234183374ull);
    vlSelf->milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__yl1_r = VL_SCOPED_RAND_RESET_I(24, __VscopeHash, 12192183913575894170ull);
    vlSelf->milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__yl2_r = VL_SCOPED_RAND_RESET_I(24, __VscopeHash, 7069381669913313442ull);
    vlSelf->milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__xr1_r = VL_SCOPED_RAND_RESET_I(24, __VscopeHash, 8388374678210131653ull);
    vlSelf->milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__xr2_r = VL_SCOPED_RAND_RESET_I(24, __VscopeHash, 1085759031476937101ull);
    vlSelf->milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__yr1_r = VL_SCOPED_RAND_RESET_I(24, __VscopeHash, 17153594281558486633ull);
    vlSelf->milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__yr2_r = VL_SCOPED_RAND_RESET_I(24, __VscopeHash, 12030792037895771617ull);
    vlSelf->milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__step_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 12740560322218139144ull);
    vlSelf->milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__busy_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10781146018636517692ull);
    vlSelf->milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__curl_r = VL_SCOPED_RAND_RESET_I(24, __VscopeHash, 3538385279785576067ull);
    vlSelf->milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__curr_r = VL_SCOPED_RAND_RESET_I(24, __VscopeHash, 15573492843812070809ull);
    vlSelf->milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__acc_r = VL_SCOPED_RAND_RESET_Q(44, __VscopeHash, 669251602262134178ull);
    vlSelf->milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__yl_hold_r = VL_SCOPED_RAND_RESET_I(24, __VscopeHash, 8936756660401357148ull);
    vlSelf->milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__sub_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16089405510922980905ull);
    vlSelf->milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__prod_w = VL_SCOPED_RAND_RESET_Q(41, __VscopeHash, 4827794215717381555ull);
    vlSelf->milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__yfin_w = VL_SCOPED_RAND_RESET_I(24, __VscopeHash, 17965522183166064131ull);
    vlSelf->milan_datapath__DOT__pp_maap_shim__DOT__rsp_valid_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6465726195020922560ull);
    vlSelf->milan_datapath__DOT__pp_maap_shim__DOT__rsp_ok_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8813074980011963651ull);
    vlSelf->milan_datapath__DOT__pp_maap_shim__DOT__rsp_da_r = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 17120168059403126287ull);
    vlSelf->milan_datapath__DOT__pp_maap_shim__DOT__grant_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2391029337861735227ull);
    vlSelf->milan_datapath__DOT__pp_maap_shim__DOT__blk_valid_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17428022316570382328ull);
    vlSelf->milan_datapath__DOT__pp_maap_shim__DOT__blk_addr_r = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 9924426755115987038ull);
    vlSelf->milan_datapath__DOT__pp_maap_shim__DOT__blk_count_r = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 11539093984928834176ull);
    vlSelf->milan_datapath__DOT__pp_maap_shim__DOT__confl_pend_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 7026974943037953144ull);
    vlSelf->milan_datapath__DOT__adp_tx_mux__DOT__locked_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3091492968299740922ull);
    vlSelf->milan_datapath__DOT__adp_tx_mux__DOT__sel_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15300035259290159099ull);
    vlSelf->milan_datapath__DOT__adp_tx_mux__DOT__last_grant_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6266469597484012055ull);
    vlSelf->milan_datapath__DOT__adp_tx_mux__DOT__flush_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3852850512693841886ull);
    vlSelf->milan_datapath__DOT__adp_tx_mux__DOT__to_cnt_r = VL_SCOPED_RAND_RESET_I(18, __VscopeHash, 13983459743081466739ull);
    vlSelf->milan_datapath__DOT__adp_tx_mux__DOT__gsel = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6243220253051098481ull);
    vlSelf->milan_datapath__DOT__adp_tx_mux__DOT__active = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2270741442939387784ull);
    vlSelf->milan_datapath__DOT__adp_tx_mux__DOT__beat_accepted = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8329299471340960092ull);
    vlSelf->milan_datapath__DOT__adp_tx_mux__DOT__src_tvalid_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5648236592384613083ull);
    vlSelf->milan_datapath__DOT__ctl_ifg__DOT__gap_r = VL_SCOPED_RAND_RESET_I(9, __VscopeHash, 3037197690939959602ull);
    vlSelf->milan_datapath__DOT__ctl_ifg__DOT__gapping_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7164260530689217802ull);
    vlSelf->milan_datapath__DOT__ctl_ifg__DOT__beat_acc = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14955978692144943468ull);
    vlSelf->milan_datapath__DOT__crf_dp_mux__DOT__locked_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2056240750540354644ull);
    vlSelf->milan_datapath__DOT__crf_dp_mux__DOT__sel_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5568086125856953443ull);
    vlSelf->milan_datapath__DOT__crf_dp_mux__DOT__last_grant_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 18351354645706085996ull);
    vlSelf->milan_datapath__DOT__crf_dp_mux__DOT__flush_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4761154256828211612ull);
    vlSelf->milan_datapath__DOT__crf_dp_mux__DOT__to_cnt_r = VL_SCOPED_RAND_RESET_I(17, __VscopeHash, 1825756534746855729ull);
    vlSelf->milan_datapath__DOT__crf_dp_mux__DOT__gsel = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7100249991306488364ull);
    vlSelf->milan_datapath__DOT__crf_dp_mux__DOT__active = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6286961003208127014ull);
    vlSelf->milan_datapath__DOT__crf_dp_mux__DOT__beat_accepted = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7701619647540268985ull);
    vlSelf->milan_datapath__DOT__crf_dp_mux__DOT__src_tvalid_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5066394851734785792ull);
    vlSelf->milan_datapath__DOT__ctl_tx_mux__DOT__locked_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3610326048497818135ull);
    vlSelf->milan_datapath__DOT__ctl_tx_mux__DOT__sel_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13184962848309969206ull);
    vlSelf->milan_datapath__DOT__ctl_tx_mux__DOT__last_grant_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5550739806543779914ull);
    vlSelf->milan_datapath__DOT__ctl_tx_mux__DOT__flush_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9354500838508642517ull);
    vlSelf->milan_datapath__DOT__ctl_tx_mux__DOT__to_cnt_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 10719473612023436433ull);
    vlSelf->milan_datapath__DOT__ctl_tx_mux__DOT__gsel = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17745417963012150095ull);
    vlSelf->milan_datapath__DOT__ctl_tx_mux__DOT__active = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8329326523292947328ull);
    vlSelf->milan_datapath__DOT__ctl_tx_mux__DOT__src_tvalid_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15766951250550095212ull);
    for (int __Vi0 = 0; __Vi0 < 10; ++__Vi0) {
        vlSelf->milan_datapath__DOT__chan_map_render__DOT__map_r[__Vi0] = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 10053316931249481898ull);
    }
    vlSelf->milan_datapath__DOT__chan_map_render__DOT__chpos_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 7320026279811759778ull);
    vlSelf->milan_datapath__DOT__chan_map_render__DOT__eff_chans_w = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 15006563009121935262ull);
    vlSelf->milan_datapath__DOT__chan_map_render__DOT__smp0_w = VL_SCOPED_RAND_RESET_I(24, __VscopeHash, 13033066458378869350ull);
    vlSelf->milan_datapath__DOT__chan_map_render__DOT__smp1_w = VL_SCOPED_RAND_RESET_I(24, __VscopeHash, 2340747564916260716ull);
    vlSelf->milan_datapath__DOT__chan_map_render__DOT__ch1_w = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 2563287964740149090ull);
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        for (int __Vi1 = 0; __Vi1 < 8; ++__Vi1) {
            vlSelf->milan_datapath__DOT__chan_map_render__DOT__cur_r[__Vi0][__Vi1] = VL_SCOPED_RAND_RESET_I(24, __VscopeHash, 15950518565320158182ull);
        }
    }
    vlSelf->milan_datapath__DOT__chan_map_render__DOT__map_wr_ok_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9373002482229372779ull);
    vlSelf->milan_datapath__DOT__chan_map_render__DOT__map_seed_w = VL_SCOPED_RAND_RESET_I(24, __VscopeHash, 10301703137156937570ull);
    vlSelf->milan_datapath__DOT__chan_map_render__DOT__avb_ok_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17110842585240415308ull);
    vlSelf->milan_datapath__DOT__chan_map_render__DOT__w0_en_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1629980290258838214ull);
    vlSelf->milan_datapath__DOT__chan_map_render__DOT__w1_en_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17035684146502086057ull);
    vlSelf->milan_datapath__DOT__chan_map_render__DOT__w0_addr_w = VL_SCOPED_RAND_RESET_I(7, __VscopeHash, 7051236067688470580ull);
    vlSelf->milan_datapath__DOT__chan_map_render__DOT__w1_addr_w = VL_SCOPED_RAND_RESET_I(7, __VscopeHash, 17449599142789915687ull);
    for (int __Vi0 = 0; __Vi0 < 10; ++__Vi0) {
        vlSelf->milan_datapath__DOT__chan_map_render__DOT__sel_r[__Vi0] = VL_SCOPED_RAND_RESET_I(24, __VscopeHash, 14519706626061297722ull);
    }
    for (int __Vi0 = 0; __Vi0 < 128; ++__Vi0) {
        vlSelf->milan_datapath__DOT__render_setpoint__DOT__h1_r[__Vi0] = VL_SCOPED_RAND_RESET_I(24, __VscopeHash, 7938915564036964377ull);
    }
    for (int __Vi0 = 0; __Vi0 < 64; ++__Vi0) {
        vlSelf->milan_datapath__DOT__render_setpoint__DOT__h0e_r[__Vi0] = VL_SCOPED_RAND_RESET_I(24, __VscopeHash, 15216632553852028674ull);
    }
    for (int __Vi0 = 0; __Vi0 < 64; ++__Vi0) {
        vlSelf->milan_datapath__DOT__render_setpoint__DOT__h0o_r[__Vi0] = VL_SCOPED_RAND_RESET_I(24, __VscopeHash, 17707505201882375132ull);
    }
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->milan_datapath__DOT__render_setpoint__DOT__wptr_r[__Vi0] = VL_SCOPED_RAND_RESET_I(6, __VscopeHash, 557384753390319676ull);
    }
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->milan_datapath__DOT__render_setpoint__DOT__rptr_r[__Vi0] = VL_SCOPED_RAND_RESET_I(6, __VscopeHash, 8831764667894869129ull);
    }
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->milan_datapath__DOT__render_setpoint__DOT__prefill_r[__Vi0] = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9909413898745517214ull);
    }
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->milan_datapath__DOT__render_setpoint__DOT__pend_r[__Vi0] = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15030614603685792793ull);
    }
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->milan_datapath__DOT__render_setpoint__DOT__dev_ok_r[__Vi0] = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 18236136755639396581ull);
    }
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->milan_datapath__DOT__render_setpoint__DOT__conv_ms_r[__Vi0] = VL_SCOPED_RAND_RESET_I(7, __VscopeHash, 14960642813985833464ull);
    }
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->milan_datapath__DOT__render_setpoint__DOT__converged_r[__Vi0] = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6064766566478180608ull);
    }
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->milan_datapath__DOT__render_setpoint__DOT__chans_q_r[__Vi0] = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 7943923452939940756ull);
    }
    vlSelf->milan_datapath__DOT__render_setpoint__DOT__chpos_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 4438020298215147214ull);
    vlSelf->milan_datapath__DOT__render_setpoint__DOT__evt_drop_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 720044888457874893ull);
    vlSelf->milan_datapath__DOT__render_setpoint__DOT__s_ok_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4175953724872328918ull);
    vlSelf->milan_datapath__DOT__render_setpoint__DOT__chans_q_in_w = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 17282905416290873107ull);
    vlSelf->milan_datapath__DOT__render_setpoint__DOT__wptr_in_w = VL_SCOPED_RAND_RESET_I(6, __VscopeHash, 7732371115899134074ull);
    vlSelf->milan_datapath__DOT__render_setpoint__DOT__c_in_w = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 10807861283495750669ull);
    vlSelf->milan_datapath__DOT__render_setpoint__DOT__ch1_w = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 8464554735620654779ull);
    vlSelf->milan_datapath__DOT__render_setpoint__DOT__pop_take_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6535588364709959747ull);
    vlSelf->milan_datapath__DOT__render_setpoint__DOT__slot_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 10621143902026337499ull);
    vlSelf->milan_datapath__DOT__render_setpoint__DOT__rptr_eff_in_w = VL_SCOPED_RAND_RESET_I(6, __VscopeHash, 2140011682497840220ull);
    vlSelf->milan_datapath__DOT__render_setpoint__DOT__fill_in_w = VL_SCOPED_RAND_RESET_I(6, __VscopeHash, 11218460183688301202ull);
    vlSelf->milan_datapath__DOT__render_setpoint__DOT__drop0_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2094938489711902118ull);
    vlSelf->milan_datapath__DOT__render_setpoint__DOT__row1_w = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 418523058108458557ull);
    vlSelf->milan_datapath__DOT__render_setpoint__DOT__drop1_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13901189419784528467ull);
    vlSelf->milan_datapath__DOT__render_setpoint__DOT__st1_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3048758105684648872ull);
    vlSelf->milan_datapath__DOT__render_setpoint__DOT__ovr0_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1951124693828875637ull);
    vlSelf->milan_datapath__DOT__render_setpoint__DOT__ovr1_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16888417025483043339ull);
    vlSelf->milan_datapath__DOT__render_setpoint__DOT__wptr_nxt_w = VL_SCOPED_RAND_RESET_I(6, __VscopeHash, 15586667022168363986ull);
    vlSelf->milan_datapath__DOT__render_setpoint__DOT__h1_sel0_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 796152348691904582ull);
    vlSelf->milan_datapath__DOT__render_setpoint__DOT__h0e_sel0_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14814315572534894485ull);
    vlSelf->milan_datapath__DOT__render_setpoint__DOT__h0o_sel0_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7056204189517707670ull);
    vlSelf->milan_datapath__DOT__render_setpoint__DOT__sched_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3062859623325195023ull);
    vlSelf->milan_datapath__DOT__render_setpoint__DOT__tick_q_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14401032913093186931ull);
    vlSelf->milan_datapath__DOT__render_setpoint__DOT__tick_d_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17704705281484341684ull);
    vlSelf->milan_datapath__DOT__render_setpoint__DOT__beat_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 12555499573496259400ull);
    vlSelf->milan_datapath__DOT__render_setpoint__DOT__chans_pop_raw_w = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 10680150313373429665ull);
    vlSelf->milan_datapath__DOT__render_setpoint__DOT__rptr_pop_w = VL_SCOPED_RAND_RESET_I(6, __VscopeHash, 2030201135822014224ull);
    vlSelf->milan_datapath__DOT__render_setpoint__DOT__ev_ok_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15636158401312951923ull);
    vlSelf->milan_datapath__DOT__render_setpoint__DOT__ev_row_r = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 13589638940965562759ull);
    vlSelf->milan_datapath__DOT__render_setpoint__DOT__pop_dry_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2825782411762065307ull);
    vlSelf->milan_datapath__DOT__render_setpoint__DOT__rd_row_w = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 16543748740439560237ull);
    vlSelf->milan_datapath__DOT__render_setpoint__DOT__smp_e_w = VL_SCOPED_RAND_RESET_I(24, __VscopeHash, 5650164470269887714ull);
    vlSelf->milan_datapath__DOT__render_setpoint__DOT__smp_o_w = VL_SCOPED_RAND_RESET_I(24, __VscopeHash, 1194870938277938656ull);
    vlSelf->milan_datapath__DOT__render_setpoint__DOT__fill_end_w = VL_SCOPED_RAND_RESET_I(6, __VscopeHash, 1769596492702856471ull);
    vlSelf->milan_datapath__DOT__render_setpoint__DOT__pdu_end_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9517751605835894087ull);
    vlSelf->milan_datapath__DOT__render_setpoint__DOT__ms_div_r = VL_SCOPED_RAND_RESET_I(17, __VscopeHash, 3029488072822363013ull);
    vlSelf->milan_datapath__DOT__render_setpoint__DOT__rail_p_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2204806719876347212ull);
    vlSelf->milan_datapath__DOT__render_setpoint__DOT__recentre_p_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6425078443534762083ull);
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->milan_datapath__DOT__render_setpoint__DOT__fill_s_w[__Vi0] = VL_SCOPED_RAND_RESET_I(6, __VscopeHash, 1100117117908912395ull);
    }
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->milan_datapath__DOT__pcm_route__DOT__route_r[__Vi0] = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 8984510757036864958ull);
    }
    vlSelf->milan_datapath__DOT__avtp_rx_monitor__DOT__mst_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 14622065670122390313ull);
    for (int __Vi0 = 0; __Vi0 < 2; ++__Vi0) {
        VL_SCOPED_RAND_RESET_W(150, vlSelf->milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r[__Vi0], __VscopeHash, 15430697001142611947ull);
    }
    vlSelf->milan_datapath__DOT__avtp_rx_monitor__DOT__pq_cnt_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 17362706939262636967ull);
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->milan_datapath__DOT__avtp_rx_monitor__DOT__tv_cnt_r[__Vi0] = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 16137599970886524405ull);
    }
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->milan_datapath__DOT__avtp_rx_monitor__DOT__tnv_cnt_r[__Vi0] = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 15190712654433800801ull);
    }
    VL_SCOPED_RAND_RESET_W(150, vlSelf->milan_datapath__DOT__avtp_rx_monitor__DOT__cur_r, __VscopeHash, 15685297020129853347ull);
    vlSelf->milan_datapath__DOT__avtp_rx_monitor__DOT__ev_s_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2087811172068529944ull);
    vlSelf->milan_datapath__DOT__avtp_rx_monitor__DOT__fmt_r = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 2792570892404568599ull);
    vlSelf->milan_datapath__DOT__avtp_rx_monitor__DOT__monst_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 13060468068515878231ull);
    vlSelf->milan_datapath__DOT__avtp_rx_monitor__DOT__wrph_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 9909333545390814525ull);
    vlSelf->milan_datapath__DOT__avtp_rx_monitor__DOT__inc_list_r = VL_SCOPED_RAND_RESET_I(12, __VscopeHash, 8811581609622783574ull);
    vlSelf->milan_datapath__DOT__avtp_rx_monitor__DOT__zero_idx_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 1269870397131517630ull);
    vlSelf->milan_datapath__DOT__avtp_rx_monitor__DOT__inc_rd_q_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10083612483744281916ull);
    vlSelf->milan_datapath__DOT__avtp_rx_monitor__DOT__bind_zero_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5437361188095732188ull);
    vlSelf->milan_datapath__DOT__avtp_rx_monitor__DOT__w11_mode_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7497901483064090341ull);
    vlSelf->milan_datapath__DOT__avtp_rx_monitor__DOT__sil_mode_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3854555034230141215ull);
    vlSelf->milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_add_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 5997824553514827741ull);
    vlSelf->milan_datapath__DOT__avtp_rx_monitor__DOT__ddrop_add_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 9023262490013526047ull);
    vlSelf->milan_datapath__DOT__avtp_rx_monitor__DOT__bind_pend_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11712287505304448284ull);
    vlSelf->milan_datapath__DOT__avtp_rx_monitor__DOT__sil_pend_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8862104144150537527ull);
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_pend_r[__Vi0] = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 11662891475857227249ull);
    }
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->milan_datapath__DOT__avtp_rx_monitor__DOT__ddrop_pend_r[__Vi0] = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 6234798159294592240ull);
    }
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->milan_datapath__DOT__avtp_rx_monitor__DOT__iv_seen_r[__Vi0] = VL_SCOPED_RAND_RESET_I(12, __VscopeHash, 1657216877527072578ull);
    }
    vlSelf->milan_datapath__DOT__avtp_rx_monitor__DOT__iv_pend_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14174426712563175089ull);
    vlSelf->milan_datapath__DOT__avtp_rx_monitor__DOT__iv_res_list_r = VL_SCOPED_RAND_RESET_I(12, __VscopeHash, 5551897506219543039ull);
    vlSelf->milan_datapath__DOT__avtp_rx_monitor__DOT__iv_res_s_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11129935078921287851ull);
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->milan_datapath__DOT__avtp_rx_monitor__DOT__frx_acc_r[__Vi0] = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 4752989918826612403ull);
    }
    vlSelf->milan_datapath__DOT__avtp_rx_monitor__DOT__frx_add_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 9870211627585731038ull);
    vlSelf->milan_datapath__DOT__avtp_rx_monitor__DOT__locked_sh_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1865214815742977915ull);
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->milan_datapath__DOT__avtp_rx_monitor__DOT__chans_sh_r[__Vi0] = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 12931490876469748808ull);
    }
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r[__Vi0] = VL_SCOPED_RAND_RESET_I(7, __VscopeHash, 17755078034659646192ull);
    }
    for (int __Vi0 = 0; __Vi0 < 64; ++__Vi0) {
        vlSelf->milan_datapath__DOT__avtp_rx_monitor__DOT__lctx_r[__Vi0] = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 7916785597338757399ull);
    }
    vlSelf->milan_datapath__DOT__avtp_rx_monitor__DOT__ram_we_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15653809701594851254ull);
    vlSelf->milan_datapath__DOT__avtp_rx_monitor__DOT__ram_waddr_w = VL_SCOPED_RAND_RESET_I(6, __VscopeHash, 395929483942599856ull);
    vlSelf->milan_datapath__DOT__avtp_rx_monitor__DOT__ram_raddr_w = VL_SCOPED_RAND_RESET_I(6, __VscopeHash, 3975439784211546110ull);
    vlSelf->milan_datapath__DOT__avtp_rx_monitor__DOT__ram_wdata_w = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 12286988643141797428ull);
    vlSelf->milan_datapath__DOT__avtp_rx_monitor__DOT__ram_q_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 15157742014147402989ull);
    vlSelf->milan_datapath__DOT__avtp_rx_monitor__DOT__ms_div_r = VL_SCOPED_RAND_RESET_I(17, __VscopeHash, 3021355262171967498ull);
    vlSelf->milan_datapath__DOT__avtp_rx_monitor__DOT__ms_tick_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12146398033882798152ull);
    vlSelf->milan_datapath__DOT__avtp_rx_monitor__DOT__iv_div_r = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 8131256921191288803ull);
    vlSelf->milan_datapath__DOT__avtp_rx_monitor__DOT__iv_tick_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7531083333759690026ull);
    vlSelf->milan_datapath__DOT__avtp_rx_monitor__DOT__penq_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5493015344807664390ull);
    VL_SCOPED_RAND_RESET_W(150, vlSelf->milan_datapath__DOT__avtp_rx_monitor__DOT__new_evt_w, __VscopeHash, 518361002865256527ull);
    vlSelf->milan_datapath__DOT__avtp_rx_monitor__DOT__depkt_any_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8115096178605422038ull);
    vlSelf->milan_datapath__DOT__avtp_rx_monitor__DOT__pdisp_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3456729606547324877ull);
    vlSelf->milan_datapath__DOT__avtp_rx_monitor__DOT__pdisp_new_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15042857255433237123ull);
    vlSelf->milan_datapath__DOT__avtp_rx_monitor__DOT__iv_go_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13212019300432514007ull);
    vlSelf->milan_datapath__DOT__avtp_rx_monitor__DOT__ext_rd_go_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2636221605792140609ull);
    vlSelf->milan_datapath__DOT__avtp_rx_monitor__DOT__disp_s_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5860425179636536049ull);
    vlSelf->milan_datapath__DOT__avtp_rx_monitor__DOT__fmt_ok_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4834133345810765451ull);
    vlSelf->milan_datapath__DOT__avtp_rx_monitor__DOT__lost_w = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 10641545219825428915ull);
    vlSelf->milan_datapath__DOT__avtp_rx_monitor__DOT__seq_mm_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8447802588018996438ull);
    vlSelf->milan_datapath__DOT__avtp_rx_monitor__DOT__monst_next_w = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 14094376045547682629ull);
    vlSelf->milan_datapath__DOT__avtp_rx_monitor__DOT__inc_next_w = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 13328925474830464260ull);
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->milan_datapath__DOT__avtp_rx_monitor__DOT__iv_set_w[__Vi0] = VL_SCOPED_RAND_RESET_I(12, __VscopeHash, 11836143326545910709ull);
    }
    vlSelf->milan_datapath__DOT__avtp_rx_monitor__DOT__eng_we_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6579028671195353711ull);
    vlSelf->milan_datapath__DOT__avtp_rx_monitor__DOT__ext_wr_ok_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5004036784858595221ull);
    vlSelf->milan_datapath__DOT__avtp_rx_monitor__DOT__leg_hit_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3915359615882650407ull);
    vlSelf->milan_datapath__DOT__avtp_rx_monitor__DOT__cntw_hit_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6531821003088379339ull);
    vlSelf->milan_datapath__DOT__avtp_rx_monitor__DOT__diag_ridx_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11842843849640638883ull);
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->milan_datapath__DOT__avtp_rx_monitor__DOT__diag_mirror__BRA__0__KET____DOT__col_r[__Vi0] = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 913292693593021891ull);
    }
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->milan_datapath__DOT__avtp_rx_monitor__DOT__diag_mirror__BRA__1__KET____DOT__col_r[__Vi0] = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 10636181827884813106ull);
    }
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->milan_datapath__DOT__avtp_rx_monitor__DOT__diag_mirror__BRA__2__KET____DOT__col_r[__Vi0] = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 4015039950042223651ull);
    }
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->milan_datapath__DOT__avtp_rx_monitor__DOT__diag_mirror__BRA__3__KET____DOT__col_r[__Vi0] = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 10235727983997993540ull);
    }
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->milan_datapath__DOT__avtp_rx_monitor__DOT__diag_mirror__BRA__4__KET____DOT__col_r[__Vi0] = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 5659745578505286953ull);
    }
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->milan_datapath__DOT__avtp_rx_monitor__DOT__diag_mirror__BRA__5__KET____DOT__col_r[__Vi0] = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 679781346148122976ull);
    }
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->milan_datapath__DOT__avtp_rx_monitor__DOT__diag_mirror__BRA__6__KET____DOT__col_r[__Vi0] = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 4990766463432180664ull);
    }
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->milan_datapath__DOT__avtp_rx_monitor__DOT__diag_mirror__BRA__7__KET____DOT__col_r[__Vi0] = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 11021764928368582190ull);
    }
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->milan_datapath__DOT__avtp_rx_monitor__DOT__diag_mirror__BRA__8__KET____DOT__col_r[__Vi0] = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 5522050219562232079ull);
    }
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->milan_datapath__DOT__avtp_rx_monitor__DOT__diag_mirror__BRA__9__KET____DOT__col_r[__Vi0] = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 15621259167364565926ull);
    }
    vlSelf->milan_datapath__DOT__media_grid_align__DOT__tst_r = VL_SCOPED_RAND_RESET_I(13, __VscopeHash, 1698719379293922590ull);
    vlSelf->milan_datapath__DOT__media_grid_align__DOT__ref_r = VL_SCOPED_RAND_RESET_I(13, __VscopeHash, 3535526614550371561ull);
    vlSelf->milan_datapath__DOT__media_grid_align__DOT__slip_r = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 2094927858723150023ull);
    vlSelf->milan_datapath__DOT__media_grid_align__DOT__quiet_r = VL_SCOPED_RAND_RESET_I(14, __VscopeHash, 13519776852699356685ull);
    vlSelf->milan_datapath__DOT__media_grid_align__DOT__engaged_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 991022933485484628ull);
    vlSelf->milan_datapath__DOT__media_grid_align__DOT__tst_next_w = VL_SCOPED_RAND_RESET_I(13, __VscopeHash, 16214125942118120258ull);
    vlSelf->milan_datapath__DOT__media_grid_align__DOT__err_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 15072185903240450609ull);
    vlSelf->milan_datapath__DOT__media_grid_align__DOT__acc_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 1938178437998443643ull);
    vlSelf->milan_datapath__DOT__media_grid_align__DOT__base_w = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 13895051107593726995ull);
    vlSelf->milan_datapath__DOT__media_grid_align__DOT__diff_w = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 10818746702524908842ull);
    vlSelf->milan_datapath__DOT__media_grid_align__DOT__fold_dn_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11659784240529890255ull);
    vlSelf->milan_datapath__DOT__media_grid_align__DOT__fold_up_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9298782087145077363ull);
    vlSelf->milan_datapath__DOT__media_grid_align__DOT__err_w = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 17040977169547476464ull);
    vlSelf->milan_datapath__DOT__crf_rx__DOT__w_hit = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13236602052094429364ull);
    vlSelf->milan_datapath__DOT__crf_rx__DOT__w_fmt_ok = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10522875603045515651ull);
    vlSelf->milan_datapath__DOT__crf_rx__DOT__w_crf_ts = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 11379143846798012241ull);
    for (int __Vi0 = 0; __Vi0 < 256; ++__Vi0) {
        vlSelf->milan_datapath__DOT__crf_rx__DOT__ts_hist_r[__Vi0] = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 5751950040872497243ull);
    }
    vlSelf->milan_datapath__DOT__crf_rx__DOT__hist_old_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 2126901756118269505ull);
    vlSelf->milan_datapath__DOT__crf_rx__DOT__ts_new_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 10365913307368472954ull);
    vlSelf->milan_datapath__DOT__crf_rx__DOT__rate_pend_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15213768936097733128ull);
    vlSelf->milan_datapath__DOT__crf_rx__DOT__hidx_r = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 8347445078272008613ull);
    vlSelf->milan_datapath__DOT__crf_rx__DOT__hfill_r = VL_SCOPED_RAND_RESET_I(9, __VscopeHash, 12685665967167196181ull);
    vlSelf->milan_datapath__DOT__crf_rx__DOT__exp_seq_r = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 11736501980353030304ull);
    vlSelf->milan_datapath__DOT__crf_rx__DOT__have_seq_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9427441939956363762ull);
    vlSelf->milan_datapath__DOT__crf_rx__DOT__settle_r = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 15735112532841544741ull);
    vlSelf->milan_datapath__DOT__crf_rx__DOT__tout_r = VL_SCOPED_RAND_RESET_I(24, __VscopeHash, 11400314798336086975ull);
    vlSelf->milan_datapath__DOT__crf_rx__DOT__prev_mr_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13189660863082724417ull);
    vlSelf->milan_datapath__DOT__crf_rx__DOT__mr_seeded_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13503583124151350882ull);
    vlSelf->milan_datapath__DOT__crf_rx__DOT__en_q = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5273469977982772915ull);
    vlSelf->milan_datapath__DOT__crf_rx__DOT__w_acc = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14028052261861268074ull);
    vlSelf->milan_datapath__DOT__crf_rx__DOT__w_tsd = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 4532899532300187133ull);
    vlSelf->milan_datapath__DOT__crf_rx__DOT__w_ev_uf_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17711043949721621247ull);
    vlSelf->milan_datapath__DOT__crf_rx__DOT__w_ev_sm_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1045043830893538774ull);
    vlSelf->milan_datapath__DOT__crf_rx__DOT__w_ev_mr_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11686232017713281569ull);
    vlSelf->milan_datapath__DOT__crf_rx__DOT__w_ev_tu_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14517631078074677498ull);
    vlSelf->milan_datapath__DOT__crf_rx__DOT__w_ev_lt_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2432399507025224732ull);
    vlSelf->milan_datapath__DOT__crf_rx__DOT__w_ev_et_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 18171265321018570230ull);
    vlSelf->milan_datapath__DOT__crf_rx__DOT__w_ev_si_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5553613729838072406ull);
    vlSelf->milan_datapath__DOT__crf_rx__DOT__w_bind_rise_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4715938103619581086ull);
    vlSelf->milan_datapath__DOT__crf_rx__DOT__iv_div_r = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 7791072445616144646ull);
    vlSelf->milan_datapath__DOT__crf_rx__DOT__iv_tick_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5873808159047111749ull);
    vlSelf->milan_datapath__DOT__crf_rx__DOT__iv_frx_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3872681326030099531ull);
    vlSelf->milan_datapath__DOT__crf_rx__DOT__iv_uf_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11916854116132978333ull);
    vlSelf->milan_datapath__DOT__crf_rx__DOT__iv_sm_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14245653357803398023ull);
    vlSelf->milan_datapath__DOT__crf_rx__DOT__iv_mr_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5477396053363069547ull);
    vlSelf->milan_datapath__DOT__crf_rx__DOT__iv_tu_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8507825207513312276ull);
    vlSelf->milan_datapath__DOT__crf_rx__DOT__iv_lt_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14136597757338471751ull);
    vlSelf->milan_datapath__DOT__crf_rx__DOT__iv_et_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12253632392996223760ull);
    vlSelf->milan_datapath__DOT__avtp_rx_parser__DOT__s_tdata_q = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 12123540848625841582ull);
    vlSelf->milan_datapath__DOT__avtp_rx_parser__DOT__s_tvalid_q = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2205722405258801641ull);
    vlSelf->milan_datapath__DOT__avtp_rx_parser__DOT__s_tready_q = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16601842273036230406ull);
    vlSelf->milan_datapath__DOT__avtp_rx_parser__DOT__s_tlast_q = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11490017988269911512ull);
    vlSelf->milan_datapath__DOT__avtp_rx_parser__DOT__beat_be = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 7415454402184239744ull);
    VL_SCOPED_RAND_RESET_W(448, vlSelf->milan_datapath__DOT__avtp_rx_parser__DOT__hdr, __VscopeHash, 7631136129642521852ull);
    vlSelf->milan_datapath__DOT__avtp_rx_parser__DOT__bytes_in = VL_SCOPED_RAND_RESET_I(7, __VscopeHash, 16871129492222051209ull);
    vlSelf->milan_datapath__DOT__avtp_rx_parser__DOT__in_acc = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2998594054211217415ull);
    vlSelf->milan_datapath__DOT__avtp_rx_parser__DOT__parsed = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14369799751640003813ull);
    vlSelf->milan_datapath__DOT__avtp_rx_parser__DOT__et_off = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 3543618249937577763ull);
    vlSelf->milan_datapath__DOT__avtp_rx_parser__DOT__subtype = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 2877338005700665167ull);
    vlSelf->milan_datapath__DOT__avtp_rx_parser__DOT__b1 = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 15375181611579853452ull);
    vlSelf->milan_datapath__DOT__avtp_rx_parser__DOT__sid = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 7369480024387029132ull);
    vlSelf->milan_datapath__DOT__avtp_rx_parser__DOT__match_hit = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15647204075577153630ull);
    vlSelf->milan_datapath__DOT__avtp_rx_parser__DOT__fire = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6174796174499732474ull);
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->milan_datapath__DOT__stream_table__DOT__ovr_sid_r[__Vi0] = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 5836600025842032663ull);
    }
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->milan_datapath__DOT__stream_table__DOT__ovr_en_r[__Vi0] = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8610899206661485935ull);
    }
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->milan_datapath__DOT__stream_table__DOT__ovr_armed_r[__Vi0] = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5278153249296783299ull);
    }
    vlSelf->milan_datapath__DOT__stream_table__DOT__en_q_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11498123079812195256ull);
    vlSelf->milan_datapath__DOT__talker_diag__DOT__tick_cnt_r = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 7170498985484180712ull);
    vlSelf->milan_datapath__DOT__talker_diag__DOT__tick_p_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5855683744885085915ull);
    for (int __Vi0 = 0; __Vi0 < 2; ++__Vi0) {
        vlSelf->milan_datapath__DOT__talker_diag__DOT__start_r[__Vi0] = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 8537183809594744008ull);
    }
    for (int __Vi0 = 0; __Vi0 < 2; ++__Vi0) {
        vlSelf->milan_datapath__DOT__talker_diag__DOT__stop_r[__Vi0] = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 15466657672989210874ull);
    }
    for (int __Vi0 = 0; __Vi0 < 2; ++__Vi0) {
        vlSelf->milan_datapath__DOT__talker_diag__DOT__mreset_r[__Vi0] = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 5816501462738206896ull);
    }
    for (int __Vi0 = 0; __Vi0 < 2; ++__Vi0) {
        vlSelf->milan_datapath__DOT__talker_diag__DOT__tuiv_r[__Vi0] = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 8643799597278655667ull);
    }
    for (int __Vi0 = 0; __Vi0 < 2; ++__Vi0) {
        vlSelf->milan_datapath__DOT__talker_diag__DOT__ftx_r[__Vi0] = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 12152206246454849272ull);
    }
    vlSelf->milan_datapath__DOT__talker_diag__DOT__seen_f_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 17549255226952657454ull);
    vlSelf->milan_datapath__DOT__talker_diag__DOT__seen_tu_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 16916263998414430998ull);
    vlSelf->milan_datapath__DOT__talker_diag__DOT__seen_mr_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 17281777268225639028ull);
    vlSelf->milan_datapath__DOT__talker_diag__DOT__strm_q_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 16842806567351608481ull);
    vlSelf->milan_datapath__DOT__talker_diag__DOT__mr_q_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 5531972665022936344ull);
    vlSelf->milan_datapath__DOT__talker_diag__DOT__ev_f_w = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 15617580129764803632ull);
    vlSelf->milan_datapath__DOT__talker_diag__DOT__ev_tu_w = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 12202095476604526203ull);
    vlSelf->milan_datapath__DOT__talker_diag__DOT__ev_mr_w = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 644869341168152027ull);
    vlSelf->milan_datapath__DOT__talker_diag__DOT__ridx_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2078712402106711788ull);
    vlSelf->milan_datapath__DOT__media_clock_restart__DOT__tgt_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11730159605993458575ull);
    vlSelf->milan_datapath__DOT__media_clock_restart__DOT__clk_src_q_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 2332101686033378368ull);
    for (int __Vi0 = 0; __Vi0 < 2; ++__Vi0) {
        vlSelf->milan_datapath__DOT__media_clock_restart__DOT__hold_r[__Vi0] = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 2733699533257473304ull);
    }
    vlSelf->milan_datapath__DOT__link_guard__DOT__rx_sync_r = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 15916183860178299118ull);
    vlSelf->milan_datapath__DOT__link_guard__DOT__tx_sync_r = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 7071941923478831061ull);
    vlSelf->milan_datapath__DOT__link_guard__DOT__act_sync_r = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 12671872054067894333ull);
    vlSelf->milan_datapath__DOT__link_guard__DOT__man_reinit_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15084789911786723802ull);
    vlSelf->milan_datapath__DOT__link_guard__DOT__rx_trans_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16495505893704889792ull);
    vlSelf->milan_datapath__DOT__link_guard__DOT__tx_trans_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17606571613770347269ull);
    vlSelf->milan_datapath__DOT__link_guard__DOT__rx_dead_r = VL_SCOPED_RAND_RESET_I(13, __VscopeHash, 12943586142425463810ull);
    vlSelf->milan_datapath__DOT__link_guard__DOT__tx_dead_r = VL_SCOPED_RAND_RESET_I(13, __VscopeHash, 10454050727543716532ull);
    vlSelf->milan_datapath__DOT__link_guard__DOT__rx_alive_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2995488038637301601ull);
    vlSelf->milan_datapath__DOT__link_guard__DOT__tx_alive_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4451929964332348361ull);
    vlSelf->milan_datapath__DOT__link_guard__DOT__rx_armed_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5334664624194689024ull);
    vlSelf->milan_datapath__DOT__link_guard__DOT__tx_armed_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 684872722566134824ull);
    vlSelf->milan_datapath__DOT__link_guard__DOT__act_age_r = VL_SCOPED_RAND_RESET_I(27, __VscopeHash, 2226991931239606812ull);
    vlSelf->milan_datapath__DOT__link_guard__DOT__state_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 13359297620767161239ull);
    vlSelf->milan_datapath__DOT__link_guard__DOT__settle_r = VL_SCOPED_RAND_RESET_I(22, __VscopeHash, 13435235668080576870ull);
    vlSelf->milan_datapath__DOT__link_guard__DOT__bounce_cnt_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 402627201830618389ull);
    vlSelf->milan_datapath__DOT__link_guard__DOT__guard_rst_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2178403524073781789ull);
    vlSelf->milan_datapath__DOT__link_guard__DOT__eth_rst_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17142633955302803513ull);
    vlSelf->milan_datapath__DOT__link_guard__DOT__bounced_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1227313587859577751ull);
    vlSelf->milan_datapath__DOT__link_guard__DOT__both_alive_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13294933488369916783ull);
    VL_SCOPED_RAND_RESET_W(88, vlSelf->milan_datapath__DOT__ts_counter__DOT__acc, __VscopeHash, 15848669679737843233ull);
    vlSelf->milan_datapath__DOT__ts_counter__DOT__tod_snapshot = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 3017743635661798048ull);
    vlSelf->milan_datapath__DOT__ts_counter__DOT__tod_snapshot_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12767843554859708570ull);
    vlSelf->milan_datapath__DOT__ptp_sync__DOT__en_meta = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 792632316048090983ull);
    vlSelf->milan_datapath__DOT__ptp_sync__DOT__en_sync = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8582928589527496273ull);
    vlSelf->milan_datapath__DOT__ptp_sync__DOT__incr_meta = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 1902573894590943951ull);
    vlSelf->milan_datapath__DOT__ptp_sync__DOT__incr_sync = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 11908816039189576919ull);
    vlSelf->milan_datapath__DOT__ptp_sync__DOT__adj_meta = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 17152776304865926639ull);
    vlSelf->milan_datapath__DOT__ptp_sync__DOT__adj_sync = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 7341780836167949889ull);
    vlSelf->milan_datapath__DOT__ptp_sync__DOT__load_tgl = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3326976435052418786ull);
    vlSelf->milan_datapath__DOT__ptp_sync__DOT__adj_tgl = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2231476464460796324ull);
    vlSelf->milan_datapath__DOT__ptp_sync__DOT__snap_tgl = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11556945255514461355ull);
    vlSelf->milan_datapath__DOT__ptp_sync__DOT__load_s = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 7236842466686922883ull);
    vlSelf->milan_datapath__DOT__ptp_sync__DOT__adj_s = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 11988832465336643453ull);
    vlSelf->milan_datapath__DOT__ptp_sync__DOT__snap_s = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 4896056477522210893ull);
    vlSelf->milan_datapath__DOT__ptp_sync__DOT__tod_wr_cap = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 13649410880703236734ull);
    vlSelf->milan_datapath__DOT__ptp_sync__DOT__offset_cap = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 511690286426162166ull);
    vlSelf->milan_datapath__DOT__ptp_sync__DOT__load_pulse_q = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12948232152725840501ull);
    vlSelf->milan_datapath__DOT__ptp_sync__DOT__adj_pulse_q = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9465137292567566842ull);
    vlSelf->milan_datapath__DOT__ptp_sync__DOT__snap_val_ts = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 7703459710492133968ull);
    vlSelf->milan_datapath__DOT__ptp_sync__DOT__snap_tgl_ts = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 526157905251695632ull);
    vlSelf->milan_datapath__DOT__ptp_sync__DOT__snap_ret_s = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 10805604738929053501ull);
    vlSelf->milan_datapath__DOT__ptp_sync__DOT__tod_rd_reg = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 17679027848598062894ull);
    vlSelf->milan_datapath__DOT__ptp_sync__DOT__tod_rd_valid_reg = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17555975567378769612ull);
    vlSelf->milan_datapath__DOT__csr__DOT__b_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13714494621205693037ull);
    vlSelf->milan_datapath__DOT__csr__DOT__r_valid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10503574739617361174ull);
    vlSelf->milan_datapath__DOT__csr__DOT__rd_pend = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14490135098466730862ull);
    vlSelf->milan_datapath__DOT__csr__DOT__rd_pend2 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10974533817742757190ull);
    vlSelf->milan_datapath__DOT__csr__DOT__live_mux_q = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 8733520342253522260ull);
    vlSelf->milan_datapath__DOT__csr__DOT__strm_mux_q = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 13351942126410400712ull);
    vlSelf->milan_datapath__DOT__csr__DOT__shadow_qq = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 11489483537148039968ull);
    vlSelf->milan_datapath__DOT__csr__DOT__live_hit_q = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6138862649735211063ull);
    vlSelf->milan_datapath__DOT__csr__DOT__strm_hit_q = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9100849135778333001ull);
    vlSelf->milan_datapath__DOT__csr__DOT__rd_in_window_q = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6667855123896386864ull);
    vlSelf->milan_datapath__DOT__csr__DOT__r_data = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 12322062386511221102ull);
    vlSelf->milan_datapath__DOT__csr__DOT__rd_addr_q = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 6595945997244090344ull);
    vlSelf->milan_datapath__DOT__csr__DOT__sweep_busy = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1838070856009293287ull);
    vlSelf->milan_datapath__DOT__csr__DOT__sweep_cnt = VL_SCOPED_RAND_RESET_I(10, __VscopeHash, 2597626500227431288ull);
    vlSelf->milan_datapath__DOT__csr__DOT__strm_dir_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2191016090365079151ull);
    vlSelf->milan_datapath__DOT__csr__DOT__strm_idx_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 2473179754331825974ull);
    vlSelf->milan_datapath__DOT__csr__DOT__lctx_wr_p_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7447757951872317670ull);
    vlSelf->milan_datapath__DOT__csr__DOT__lctx_wr_addr_r = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 2616336660015513041ull);
    vlSelf->milan_datapath__DOT__csr__DOT__lctx_wr_data_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 2353885409056742122ull);
    vlSelf->milan_datapath__DOT__csr__DOT__tctx_wr_p_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1560205352452286441ull);
    vlSelf->milan_datapath__DOT__csr__DOT__tctx_wr_addr_r = VL_SCOPED_RAND_RESET_I(7, __VscopeHash, 10201995388155925905ull);
    vlSelf->milan_datapath__DOT__csr__DOT__tctx_wr_data_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 4152439075251573206ull);
    vlSelf->milan_datapath__DOT__csr__DOT__snap_busy_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13401243747251288645ull);
    vlSelf->milan_datapath__DOT__csr__DOT__rds_busy_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10547011445023463007ull);
    vlSelf->milan_datapath__DOT__csr__DOT__rds_dir_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15935505477321121189ull);
    vlSelf->milan_datapath__DOT__csr__DOT__rds_cyc_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 427335538908098653ull);
    vlSelf->milan_datapath__DOT__csr__DOT__rd_is_slow_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15844231368139016641ull);
    vlSelf->milan_datapath__DOT__csr__DOT__rds_valid_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15632904727200795000ull);
    vlSelf->milan_datapath__DOT__csr__DOT__rds_done_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2576900481489799569ull);
    vlSelf->milan_datapath__DOT__csr__DOT__irq_mask = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 2376295935016826797ull);
    vlSelf->milan_datapath__DOT__csr__DOT__irq_status = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 11505584028027618962ull);
    vlSelf->milan_datapath__DOT__csr__DOT__mac_ctrl = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 17018259252392059163ull);
    vlSelf->milan_datapath__DOT__csr__DOT__mac_ifg = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 15121606105290994221ull);
    vlSelf->milan_datapath__DOT__csr__DOT__mac_alo = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 18288736837750982907ull);
    vlSelf->milan_datapath__DOT__csr__DOT__mac_ahi = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 782746863443379205ull);
    vlSelf->milan_datapath__DOT__csr__DOT__mc_lo = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 5831616978633483419ull);
    vlSelf->milan_datapath__DOT__csr__DOT__mc_hi = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 238490697787957232ull);
    vlSelf->milan_datapath__DOT__csr__DOT__phy_rst = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 809839818496205232ull);
    vlSelf->milan_datapath__DOT__csr__DOT__eth_guard = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13469874811738840066ull);
    vlSelf->milan_datapath__DOT__csr__DOT__ptp_ctrl = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 7159777413653490169ull);
    vlSelf->milan_datapath__DOT__csr__DOT__ptp_incr = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 8207339968338810145ull);
    vlSelf->milan_datapath__DOT__csr__DOT__ptp_adj = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 3312056880301096159ull);
    vlSelf->milan_datapath__DOT__csr__DOT__ptp_twlo = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 4730099932413380500ull);
    vlSelf->milan_datapath__DOT__csr__DOT__ptp_twhi = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 12601456620279226798ull);
    vlSelf->milan_datapath__DOT__csr__DOT__ptp_oflo = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 11555497851140061087ull);
    vlSelf->milan_datapath__DOT__csr__DOT__ptp_ofhi = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 138357968536966172ull);
    vlSelf->milan_datapath__DOT__csr__DOT__ptp_tod_rd = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 9518998572414028519ull);
    for (int __Vi0 = 0; __Vi0 < 9; ++__Vi0) {
        vlSelf->milan_datapath__DOT__csr__DOT__stat_snap[__Vi0] = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 12350890656454470542ull);
    }
    vlSelf->milan_datapath__DOT__csr__DOT__stats_rst_p = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10017351510739428585ull);
    vlSelf->milan_datapath__DOT__csr__DOT__i2spb_clru_p = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16683129708530402759ull);
    vlSelf->milan_datapath__DOT__csr__DOT__i2spb_clro_p = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13518283653898073113ull);
    vlSelf->milan_datapath__DOT__csr__DOT__ptp_load_p = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17937085731260552793ull);
    vlSelf->milan_datapath__DOT__csr__DOT__ptp_adj_p = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2650445069227214791ull);
    vlSelf->milan_datapath__DOT__csr__DOT__ptp_snap_p = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6053579945606747085ull);
    vlSelf->milan_datapath__DOT__csr__DOT__adp_ctrl = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 8759610603064104929ull);
    vlSelf->milan_datapath__DOT__csr__DOT__adp_disc_seen_cnt_r = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 9498548670394257550ull);
    vlSelf->milan_datapath__DOT__csr__DOT__aaf_ctrl = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 17912260040090226521ull);
    vlSelf->milan_datapath__DOT__csr__DOT__aaf_dmlo = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 4328653323409169554ull);
    vlSelf->milan_datapath__DOT__csr__DOT__aaf_dmhi = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 2267395976655123260ull);
    vlSelf->milan_datapath__DOT__csr__DOT__acmp_lobs = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 10635196965850591178ull);
    vlSelf->milan_datapath__DOT__csr__DOT__lwsrp_ctrl = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 5759742362018291521ull);
    vlSelf->milan_datapath__DOT__csr__DOT__maap_ctrl = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 11309480783826895116ull);
    vlSelf->milan_datapath__DOT__csr__DOT__link_ctrl = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 17230803420400324052ull);
    vlSelf->milan_datapath__DOT__csr__DOT__lpf_ctrl = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 13320599515544578254ull);
    vlSelf->milan_datapath__DOT__csr__DOT__crf_ctrl = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 4236181310976816398ull);
    vlSelf->milan_datapath__DOT__csr__DOT__crf_sidlo = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 17348827527673671810ull);
    vlSelf->milan_datapath__DOT__csr__DOT__crf_sidhi = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 17064190797701331552ull);
    vlSelf->milan_datapath__DOT__csr__DOT__crft_ctrl = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 4269561266067534930ull);
    vlSelf->milan_datapath__DOT__csr__DOT__crft_sidlo = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 14398692195160633906ull);
    vlSelf->milan_datapath__DOT__csr__DOT__crft_sidhi = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 1401393356969275147ull);
    vlSelf->milan_datapath__DOT__csr__DOT__crft_dmlo = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 14723331479705173299ull);
    vlSelf->milan_datapath__DOT__csr__DOT__crft_dmhi = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 508046437882537176ull);
    vlSelf->milan_datapath__DOT__csr__DOT__tone_ctrl = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 18194934328590750685ull);
    vlSelf->milan_datapath__DOT__csr__DOT__mcsrv_ctrl = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 14319602854640694512ull);
    vlSelf->milan_datapath__DOT__csr__DOT__ltap_en_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14901849583261391137ull);
    vlSelf->milan_datapath__DOT__csr__DOT__ltap_clr_p = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1099971044474508918ull);
    vlSelf->milan_datapath__DOT__csr__DOT__chmap_ctrl = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 15814317113089025199ull);
    vlSelf->milan_datapath__DOT__csr__DOT__chmap_sel = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 289893510951932791ull);
    vlSelf->milan_datapath__DOT__csr__DOT__chmap_word = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 12064112562497560825ull);
    vlSelf->milan_datapath__DOT__csr__DOT__chmap_commits = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 6590000247914501319ull);
    vlSelf->milan_datapath__DOT__csr__DOT__chmap_refused = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 786551900314066785ull);
    vlSelf->milan_datapath__DOT__csr__DOT__chmap_wr_p = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10452850805249207062ull);
    vlSelf->milan_datapath__DOT__csr__DOT__cmrd_busy_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1647126954436129995ull);
    vlSelf->milan_datapath__DOT__csr__DOT__cmrd_flush_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7401261008494427915ull);
    vlSelf->milan_datapath__DOT__csr__DOT__cmrd_valid_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9350041551297280223ull);
    vlSelf->milan_datapath__DOT__csr__DOT__cmrd_to_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1771175108087247947ull);
    vlSelf->milan_datapath__DOT__csr__DOT__cmrd_unsup_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16605521671389585891ull);
    vlSelf->milan_datapath__DOT__csr__DOT__cmrd_armed_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12522474273616277630ull);
    vlSelf->milan_datapath__DOT__csr__DOT__cmrd_side_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11963740656349791237ull);
    vlSelf->milan_datapath__DOT__csr__DOT__cmrd_addr_r = VL_SCOPED_RAND_RESET_I(6, __VscopeHash, 7879796706432343072ull);
    vlSelf->milan_datapath__DOT__csr__DOT__cmrd_data_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 17748678681380318329ull);
    vlSelf->milan_datapath__DOT__csr__DOT__cmrd_wd_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 17809964285985748875ull);
    vlSelf->milan_datapath__DOT__csr__DOT__lwsrp_vid = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 10009375411199016705ull);
    vlSelf->milan_datapath__DOT__csr__DOT__lwsrp_lat = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 15207630477840778715ull);
    vlSelf->milan_datapath__DOT__csr__DOT__adp_eidlo = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 10964907143668503054ull);
    vlSelf->milan_datapath__DOT__csr__DOT__adp_eidhi = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 4151186418388875646ull);
    vlSelf->milan_datapath__DOT__csr__DOT__adp_midlo = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 8662002850644773694ull);
    vlSelf->milan_datapath__DOT__csr__DOT__adp_midhi = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 4966851519894731815ull);
    vlSelf->milan_datapath__DOT__csr__DOT__adp_idx0 = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 10638228031971173045ull);
    vlSelf->milan_datapath__DOT__csr__DOT__tcam_ctrl = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 5605924520227998396ull);
    vlSelf->milan_datapath__DOT__csr__DOT__tcam_klo = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 7050550392683724099ull);
    vlSelf->milan_datapath__DOT__csr__DOT__tcam_khi = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 7126416350406199490ull);
    vlSelf->milan_datapath__DOT__csr__DOT__tcam_mlo = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 16446666664095245209ull);
    vlSelf->milan_datapath__DOT__csr__DOT__tcam_mhi = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 16457401808690757210ull);
    vlSelf->milan_datapath__DOT__csr__DOT__tcam_act = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 17255198050796877158ull);
    vlSelf->milan_datapath__DOT__csr__DOT__tcam_wr_p = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14848887488537196220ull);
    vlSelf->milan_datapath__DOT__csr__DOT__tcam_wr_index = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 577020327276202862ull);
    vlSelf->milan_datapath__DOT__csr__DOT__tcam_wr_valid_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11425649800745150887ull);
    vlSelf->milan_datapath__DOT__csr__DOT__strm_lsn0_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9282533630802940607ull);
    vlSelf->milan_datapath__DOT__csr__DOT__acmp_fresh_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1506875643656530723ull);
    vlSelf->milan_datapath__DOT__csr__DOT__acmp_sid_q_r = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 16677134815942112616ull);
    vlSelf->milan_datapath__DOT__csr__DOT__acmp_dmac_q_r = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 12265674320600836525ull);
    vlSelf->milan_datapath__DOT__csr__DOT__acmp_state_q_r = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 6322528348199834388ull);
    vlSelf->milan_datapath__DOT__csr__DOT__acmp_probing_q_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 5743055432065944602ull);
    vlSelf->milan_datapath__DOT__csr__DOT__acmp_status_q_r = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 10534155452935918122ull);
    vlSelf->milan_datapath__DOT__csr__DOT__acmp_ctlr_q_r = VL_SCOPED_RAND_RESET_Q(64, __VscopeHash, 4518839411219037243ull);
    vlSelf->milan_datapath__DOT__csr__DOT__acmp_flags_q_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 5338870236867212191ull);
    vlSelf->milan_datapath__DOT__csr__DOT__acmp_tuid_q_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 10622876397401828265ull);
    vlSelf->milan_datapath__DOT__csr__DOT__rest_pend_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4517679852334449665ull);
    vlSelf->milan_datapath__DOT__csr__DOT__rest_done_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8796116156453441777ull);
    vlSelf->milan_datapath__DOT__csr__DOT__rest_stat_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 6808364345817571680ull);
    vlSelf->milan_datapath__DOT__csr__DOT__rest_idx_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 6888392363568966134ull);
    for (int __Vi0 = 0; __Vi0 < 12; ++__Vi0) {
        vlSelf->milan_datapath__DOT__csr__DOT__snap_shadow_r[__Vi0] = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 17587902219882628948ull);
    }
    vlSelf->milan_datapath__DOT__csr__DOT__snap_st_r = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 11396009220070497634ull);
    vlSelf->milan_datapath__DOT__csr__DOT__snap_dir_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10087902531055751017ull);
    vlSelf->milan_datapath__DOT__csr__DOT__snap_idx_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 6778552146079125458ull);
    vlSelf->milan_datapath__DOT__csr__DOT__snap_wi_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 10128347099574544739ull);
    vlSelf->milan_datapath__DOT__csr__DOT__snap_cyc_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 13570655677034949205ull);
    vlSelf->milan_datapath__DOT__csr__DOT__snap_word_r = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 9535550438515498905ull);
    vlSelf->milan_datapath__DOT__csr__DOT__snap_req_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9920192665422252616ull);
    vlSelf->milan_datapath__DOT__csr__DOT__snap_rden_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12476638454605304675ull);
    vlSelf->milan_datapath__DOT__csr__DOT__snap_m8_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 13146359122280446010ull);
    vlSelf->milan_datapath__DOT__csr__DOT__rds_word_r = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 7187495083838431147ull);
    vlSelf->milan_datapath__DOT__csr__DOT__rds_idx_r = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 15114061500259906504ull);
    vlSelf->milan_datapath__DOT__csr__DOT__mac_reinit_q = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7107896989702823441ull);
    vlSelf->milan_datapath__DOT__csr__DOT__win_alias_ctrl_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3823672466909055624ull);
    vlSelf->milan_datapath__DOT__csr__DOT__win_alias_dmlo_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10299521400825600779ull);
    vlSelf->milan_datapath__DOT__csr__DOT__win_alias_dmhi_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11007010693916361975ull);
    for (int __Vi0 = 0; __Vi0 < 512; ++__Vi0) {
        vlSelf->milan_datapath__DOT__csr__DOT__shadow_ram[__Vi0] = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 17715787520329520062ull);
    }
    for (int __Vi0 = 0; __Vi0 < 512; ++__Vi0) {
        vlSelf->milan_datapath__DOT__csr__DOT__dflt_rom[__Vi0] = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 574837959447466248ull);
    }
    vlSelf->milan_datapath__DOT__csr__DOT__shadow_q = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 15992117034319299972ull);
    vlSelf->milan_datapath__DOT__csr__DOT__dflt_q = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 9754662354176750976ull);
    vlSelf->milan_datapath__DOT__csr__DOT__shadow_axi_we = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 594599094268029815ull);
    vlSelf->milan_datapath__DOT__csr__DOT__sweep_wr = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6973513038012338370ull);
    vlSelf->milan_datapath__DOT__csr__DOT__pp_rd_hit_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13140496912842398833ull);
    vlSelf->milan_datapath__DOT__csr__DOT__live_mux = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 3971510024697558245ull);
    vlSelf->milan_datapath__DOT__csr__DOT__live_hit = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1751065730186971503ull);
    vlSelf->milan_datapath__DOT__csr__DOT__mac_wire_w = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 7806366114111279884ull);
    vlSelf->milan_datapath__DOT__csr__DOT__strm_mux = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 12629574862558621301ull);
    vlSelf->milan_datapath__DOT__csr__DOT__cmrd_go_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10215571311606879523ull);
    vlSelf->milan_datapath__DOT__csr__DOT__snap_srp9_w = VL_SCOPED_RAND_RESET_I(9, __VscopeHash, 11606304147016669678ull);
    vlSelf->milan_datapath__DOT__csr__DOT__g_pp_csr__DOT__pp_ctrl_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 10899894006989285387ull);
    vlSelf->milan_datapath__DOT__csr__DOT__g_pp_csr__DOT__pp_spaddr_r = VL_SCOPED_RAND_RESET_I(20, __VscopeHash, 8303675070274080080ull);
    vlSelf->milan_datapath__DOT__csr__DOT__g_pp_csr__DOT__pp_sprdata_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 8441076672605357519ull);
    vlSelf->milan_datapath__DOT__csr__DOT__g_pp_csr__DOT__pp_busy_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16702870339680591862ull);
    vlSelf->milan_datapath__DOT__csr__DOT__g_pp_csr__DOT__pp_err_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 363002204724583722ull);
    vlSelf->milan_datapath__DOT__csr__DOT__g_pp_csr__DOT__pp_req_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9567396768690903783ull);
    vlSelf->milan_datapath__DOT__csr__DOT__g_pp_csr__DOT__pp_we_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13421184466471017656ull);
    vlSelf->milan_datapath__DOT__csr__DOT__g_pp_csr__DOT__pp_wdata_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 1678274422872540738ull);
    vlSelf->milan_datapath__DOT__csr__DOT__g_pp_csr__DOT__pp_nvm_sel_r = VL_SCOPED_RAND_RESET_I(6, __VscopeHash, 1674180456631104046ull);
    vlSelf->milan_datapath__DOT__csr__DOT__g_pp_csr__DOT__pp_nvm_we_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11029160951458326063ull);
    vlSelf->milan_datapath__DOT__csr__DOT__g_pp_csr__DOT__pp_nvm_waddr_r = VL_SCOPED_RAND_RESET_I(6, __VscopeHash, 3468095465514337031ull);
    vlSelf->milan_datapath__DOT__csr__DOT__g_pp_csr__DOT__pp_nvm_wdata_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 10012661182320980769ull);
    vlSelf->milan_datapath__DOT__csr__DOT__g_pp_csr__DOT__pp_nvm_rd_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17608790135224629320ull);
    vlSelf->milan_datapath__DOT__ptp_clock_validity__DOT__qdiv_r = VL_SCOPED_RAND_RESET_I(12, __VscopeHash, 1691855097502160009ull);
    vlSelf->milan_datapath__DOT__ptp_clock_validity__DOT__hold_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 6074053983101350171ull);
    vlSelf->milan_datapath__DOT__ptp_clock_validity__DOT__ival_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 15423599261249573040ull);
    vlSelf->milan_datapath__DOT__ptp_clock_validity__DOT__tu_ivals_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 11180446964022865620ull);
    for (int __Vi0 = 0; __Vi0 < 32; ++__Vi0) {
        vlSelf->milan_datapath__DOT__aaf_packetizer__DOT__tctx_r[__Vi0] = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 17871775881516171892ull);
    }
    vlSelf->milan_datapath__DOT__aaf_packetizer__DOT__tram_we_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1899785309538159450ull);
    vlSelf->milan_datapath__DOT__aaf_packetizer__DOT__tram_waddr_w = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 8674119600448016694ull);
    vlSelf->milan_datapath__DOT__aaf_packetizer__DOT__tram_raddr_w = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 12208193128776567302ull);
    vlSelf->milan_datapath__DOT__aaf_packetizer__DOT__tram_wdata_w = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 5963577860569068586ull);
    vlSelf->milan_datapath__DOT__aaf_packetizer__DOT__tram_q_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 16334770945009261429ull);
    for (int __Vi0 = 0; __Vi0 < 128; ++__Vi0) {
        vlSelf->milan_datapath__DOT__aaf_packetizer__DOT__stg_r[__Vi0] = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 7456264598591434293ull);
    }
    vlSelf->milan_datapath__DOT__aaf_packetizer__DOT__stg_we_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15765338554287631209ull);
    vlSelf->milan_datapath__DOT__aaf_packetizer__DOT__stg_q_r = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 4788127773326635489ull);
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->milan_datapath__DOT__aaf_packetizer__DOT__nsamp_r[__Vi0] = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 17771969784989835681ull);
    }
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->milan_datapath__DOT__aaf_packetizer__DOT__wbank_r[__Vi0] = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11217948867763725957ull);
    }
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->milan_datapath__DOT__aaf_packetizer__DOT__pend_r[__Vi0] = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12853281243080674311ull);
    }
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->milan_datapath__DOT__aaf_packetizer__DOT__chans_r[__Vi0] = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 11096691945592641739ull);
    }
    for (int __Vi0 = 0; __Vi0 < 2; ++__Vi0) {
        vlSelf->milan_datapath__DOT__aaf_packetizer__DOT__pbase_w[__Vi0] = VL_SCOPED_RAND_RESET_I(6, __VscopeHash, 6565025543535203189ull);
    }
    vlSelf->milan_datapath__DOT__aaf_packetizer__DOT__pown_v_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14588698973261883580ull);
    vlSelf->milan_datapath__DOT__aaf_packetizer__DOT__pown_o_w = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 6966222693255677569ull);
    vlSelf->milan_datapath__DOT__aaf_packetizer__DOT__own_last_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5072003806064769699ull);
    vlSelf->milan_datapath__DOT__aaf_packetizer__DOT__tsw_pend_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3731182413336555198ull);
    vlSelf->milan_datapath__DOT__aaf_packetizer__DOT__tsw_t_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4168703494689461300ull);
    vlSelf->milan_datapath__DOT__aaf_packetizer__DOT__tsw_val_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 106442723612964873ull);
    vlSelf->milan_datapath__DOT__aaf_packetizer__DOT__est_r = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 3405786319015103622ull);
    vlSelf->milan_datapath__DOT__aaf_packetizer__DOT__et_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4691085994660922745ull);
    vlSelf->milan_datapath__DOT__aaf_packetizer__DOT__ebank_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 821534779399544186ull);
    vlSelf->milan_datapath__DOT__aaf_packetizer__DOT__fph_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 13016944412270609976ull);
    vlSelf->milan_datapath__DOT__aaf_packetizer__DOT__beat_r = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 11335113700708864469ull);
    vlSelf->milan_datapath__DOT__aaf_packetizer__DOT__eiss_r = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 6256100198185193653ull);
    vlSelf->milan_datapath__DOT__aaf_packetizer__DOT__ecap_r = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 11389123144432984513ull);
    vlSelf->milan_datapath__DOT__aaf_packetizer__DOT__esmp_r = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 10322848712792155464ull);
    vlSelf->milan_datapath__DOT__aaf_packetizer__DOT__eo_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 12998868375141184013ull);
    vlSelf->milan_datapath__DOT__aaf_packetizer__DOT__eseq_r = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 8148661617784911198ull);
    vlSelf->milan_datapath__DOT__aaf_packetizer__DOT__ets_r = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 18211812824830942656ull);
    vlSelf->milan_datapath__DOT__aaf_packetizer__DOT__etu_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 212215363238968094ull);
    vlSelf->milan_datapath__DOT__aaf_packetizer__DOT__emr_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10720730203492282912ull);
    vlSelf->milan_datapath__DOT__aaf_packetizer__DOT__edmac_r = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 53299994515341900ull);
    vlSelf->milan_datapath__DOT__aaf_packetizer__DOT__euid_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 16657596977466152150ull);
    vlSelf->milan_datapath__DOT__aaf_packetizer__DOT__evid_r = VL_SCOPED_RAND_RESET_I(12, __VscopeHash, 16795413757673090315ull);
    for (int __Vi0 = 0; __Vi0 < 24; ++__Vi0) {
        vlSelf->milan_datapath__DOT__aaf_packetizer__DOT__buf_l_r[__Vi0] = VL_SCOPED_RAND_RESET_I(24, __VscopeHash, 9494029606082145961ull);
    }
    for (int __Vi0 = 0; __Vi0 < 24; ++__Vi0) {
        vlSelf->milan_datapath__DOT__aaf_packetizer__DOT__buf_r_r[__Vi0] = VL_SCOPED_RAND_RESET_I(24, __VscopeHash, 2090405633593579566ull);
    }
    vlSelf->milan_datapath__DOT__aaf_packetizer__DOT__echn_w = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 5169666477164082641ull);
    vlSelf->milan_datapath__DOT__aaf_packetizer__DOT__eff_dmac_w = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 6710115494411523350ull);
    vlSelf->milan_datapath__DOT__aaf_packetizer__DOT__eff_vid_w = VL_SCOPED_RAND_RESET_I(12, __VscopeHash, 5683696604543584112ull);
    for (int __Vi0 = 0; __Vi0 < 240; ++__Vi0) {
        vlSelf->milan_datapath__DOT__aaf_packetizer__DOT__fb[__Vi0] = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 15647322579175543919ull);
    }
    vlSelf->milan_datapath__DOT__aaf_packetizer__DOT__ext_trd_go_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7816973055398998190ull);
    vlSelf->milan_datapath__DOT__aaf_packetizer__DOT__ext_trd_q_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6896101680176286428ull);
    vlSelf->milan_datapath__DOT__chan_map_capture__DOT__tdm_pair_valid_i = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1165246705320477467ull);
    for (int __Vi0 = 0; __Vi0 < 8; ++__Vi0) {
        vlSelf->milan_datapath__DOT__chan_map_capture__DOT__map_r[__Vi0] = VL_SCOPED_RAND_RESET_I(13, __VscopeHash, 17672175980922143777ull);
    }
    vlSelf->milan_datapath__DOT__chan_map_capture__DOT__loop_mapped_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12868497344440148806ull);
    vlSelf->milan_datapath__DOT__chan_map_capture__DOT__loop_fed_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15316308791018785694ull);
    vlSelf->milan_datapath__DOT__chan_map_capture__DOT__i2s_hold_r = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 7412035743948137912ull);
    for (int __Vi0 = 0; __Vi0 < 4; ++__Vi0) {
        vlSelf->milan_datapath__DOT__chan_map_capture__DOT__tdm_hold_r[__Vi0] = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 162037843714216571ull);
    }
    vlSelf->milan_datapath__DOT__chan_map_capture__DOT__tdm_fed_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 495305766895524811ull);
    vlSelf->milan_datapath__DOT__chan_map_capture__DOT__tdm_frame_pend_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4261642155064925752ull);
    for (int __Vi0 = 0; __Vi0 < 8; ++__Vi0) {
        vlSelf->milan_datapath__DOT__chan_map_capture__DOT__lb_q_r[__Vi0] = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 1428332133724534224ull);
    }
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->milan_datapath__DOT__chan_map_capture__DOT__q_wr_r[__Vi0] = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 17298728824561349025ull);
    }
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->milan_datapath__DOT__chan_map_capture__DOT__q_rd_r[__Vi0] = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 813886602832586031ull);
    }
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r[__Vi0] = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 7232847960997402772ull);
    }
    vlSelf->milan_datapath__DOT__chan_map_capture__DOT__q_fed_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3116155668127286594ull);
    vlSelf->milan_datapath__DOT__chan_map_capture__DOT__q_primed_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16708389086551540033ull);
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r[__Vi0] = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 2102110978853521090ull);
    }
    for (int __Vi0 = 0; __Vi0 < 4; ++__Vi0) {
        vlSelf->milan_datapath__DOT__chan_map_capture__DOT__skid_data_r[__Vi0] = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 8748041923390157654ull);
    }
    for (int __Vi0 = 0; __Vi0 < 4; ++__Vi0) {
        vlSelf->milan_datapath__DOT__chan_map_capture__DOT__skid_addr_r[__Vi0] = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17436753910835527711ull);
    }
    for (int __Vi0 = 0; __Vi0 < 4; ++__Vi0) {
        vlSelf->milan_datapath__DOT__chan_map_capture__DOT__skid_strm_r[__Vi0] = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 9631268522062918851ull);
    }
    vlSelf->milan_datapath__DOT__chan_map_capture__DOT__skid_v_r = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 2918527077089251533ull);
    vlSelf->milan_datapath__DOT__chan_map_capture__DOT__skid_rp_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 16273046127418905713ull);
    vlSelf->milan_datapath__DOT__chan_map_capture__DOT__skid_cnt_r = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 17140546123319360115ull);
    vlSelf->milan_datapath__DOT__chan_map_capture__DOT__push_ram_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10288732629911435511ull);
    vlSelf->milan_datapath__DOT__chan_map_capture__DOT__skid_kill_w = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 4071561021612850768ull);
    vlSelf->milan_datapath__DOT__chan_map_capture__DOT__st_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 617647150233310410ull);
    vlSelf->milan_datapath__DOT__chan_map_capture__DOT__pop_idx_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6713550394578713301ull);
    vlSelf->milan_datapath__DOT__chan_map_capture__DOT__pop_visit_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6385497687219067687ull);
    vlSelf->milan_datapath__DOT__chan_map_capture__DOT__pop_cnt_w = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 7887781413584184122ull);
    vlSelf->milan_datapath__DOT__chan_map_capture__DOT__pop_act_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2580413073170139993ull);
    vlSelf->milan_datapath__DOT__chan_map_capture__DOT__pop_rd_w = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 10860819850146173574ull);
    vlSelf->milan_datapath__DOT__chan_map_capture__DOT__push_same_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16392122523276581737ull);
    vlSelf->milan_datapath__DOT__chan_map_capture__DOT__push_cnt1_w = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 10633173902065854031ull);
    vlSelf->milan_datapath__DOT__chan_map_capture__DOT__push_drop_w = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16855633612322340603ull);
    vlSelf->milan_datapath__DOT__chan_map_capture__DOT__skip_sum_w = VL_SCOPED_RAND_RESET_I(17, __VscopeHash, 18271958241122957847ull);
    vlSelf->milan_datapath__DOT__chan_map_capture__DOT__dup_sum_w = VL_SCOPED_RAND_RESET_I(17, __VscopeHash, 6836999512713769383ull);
    vlSelf->milan_datapath__DOT__chan_map_capture__DOT__q_rdata_r = VL_SCOPED_RAND_RESET_Q(48, __VscopeHash, 16523591104848937275ull);
    vlSelf->milan_datapath__DOT__chan_map_capture__DOT__pop_ret_v_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4703231933506735271ull);
    vlSelf->milan_datapath__DOT__chan_map_capture__DOT__pop_ret_pair_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3713882136506250408ull);
    vlSelf->milan_datapath__DOT__chan_map_capture__DOT__slot_r = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 775011392815299049ull);
    vlSelf->milan_datapath__DOT__chan_map_capture__DOT__tick_pend_r = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4669000913684669080ull);
    vlSelf->milan_datapath__DOT__chan_map_capture__DOT__gap_r = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 3301763615805424823ull);
    vlSelf->milan_datapath__DOT__tone_gen_media__DOT__idx_r = VL_SCOPED_RAND_RESET_I(6, __VscopeHash, 11038296918257059402ull);
    vlSelf->milan_datapath__DOT__media_nco__DOT__cnt_r = VL_SCOPED_RAND_RESET_I(12, __VscopeHash, 11149536716484589554ull);
    vlSelf->milan_datapath__DOT__media_nco__DOT__frac_r = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 11977072428608908816ull);
    vlSelf->milan_datapath__DOT__media_nco__DOT__trim_sel_w = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 10421455893199941521ull);
    vlSelf->milan_datapath__DOT__media_nco__DOT__trim_r = VL_SCOPED_RAND_RESET_I(18, __VscopeHash, 12247305064940818821ull);
    vlSelf->milan_datapath__DOT__media_nco__DOT__sum_w = VL_SCOPED_RAND_RESET_I(18, __VscopeHash, 12873685921185640770ull);
    vlSelf->milan_datapath__DOT__tone_gen__DOT__cnt_r = VL_SCOPED_RAND_RESET_I(9, __VscopeHash, 11721313366426049816ull);
    vlSelf->milan_datapath__DOT__tone_gen__DOT__idx_r = VL_SCOPED_RAND_RESET_I(6, __VscopeHash, 17118182703207828577ull);
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_fp_at_f__12__j = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_fp_at_f__13__j = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_fp_at_f__14__j = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_fp_at_f__15__j = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__pack4_f__16__Vfuncout = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__pack4_f__16__a = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__pack4_f__16__b = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__pack4_f__16__c = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__pack4_f__16__d = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_ev_at_f__17__j = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_ev_at_f__18__j = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_ev_at_f__19__j = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__pack3_f__20__Vfuncout = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__pack3_f__20__a = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__pack3_f__20__b = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__pack3_f__20__c = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__fv_byte_f__21__Vfuncout = 0;
    VL_ZERO_RESET_W(272, vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__fv_byte_f__21__v);
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__fv_byte_f__21__i = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__mac_byte_f__22__Vfuncout = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__mac_byte_f__22__v = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__mac_byte_f__22__i = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__mac_byte_f__23__Vfuncout = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__mac_byte_f__23__v = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__mac_byte_f__23__i = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__byte48_f__69__Vfuncout = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__byte48_f__69__v = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__byte48_f__69__n = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__byte48_f__69__sh = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__byte48_f__70__Vfuncout = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__byte48_f__70__v = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__byte48_f__70__n = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__byte48_f__70__sh = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__byte16_f__71__Vfuncout = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__byte16_f__71__n = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__byte16_f__71__sh = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__byte48_f__72__Vfuncout = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__byte48_f__72__v = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__byte48_f__72__n = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__byte48_f__72__sh = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__byte16_f__73__Vfuncout = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__byte16_f__73__v = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__byte16_f__73__n = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__byte16_f__73__sh = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__byte48_f__74__Vfuncout = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__byte48_f__74__v = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__byte48_f__74__n = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__byte48_f__74__sh = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__byte16_f__75__Vfuncout = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__byte16_f__75__v = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__byte16_f__75__n = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__byte16_f__75__sh = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__76__Vfuncout = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__76__v = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__77__Vfuncout = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__77__v = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__78__Vfuncout = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__78__v = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__79__Vfuncout = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__79__v = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__80__Vfuncout = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__80__v = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__81__Vfuncout = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__81__v = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__82__Vfuncout = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__ffs_f__82__v = 0;
    VL_ZERO_RESET_W(84, vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__fresh_f__84__r);
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__lsn_reg_f__85__s = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__lsn_reg_f__85____VlefCall_0__lsn_state_f = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__lsn_state_f__86__Vfuncout = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__lsn_state_f__86__s = 0;
    VL_ZERO_RESET_W(84, vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__fresh_f__87__r);
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__lsn_reg_f__88__s = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__lsn_reg_f__88____VlefCall_0__lsn_state_f = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__lsn_state_f__89__Vfuncout = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__lsn_state_f__89__s = 0;
    VL_ZERO_RESET_W(84, vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__fresh_f__90__r);
    VL_ZERO_RESET_W(84, vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__fresh_f__91__r);
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__lsn_reg_f__92__s = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__lsn_reg_f__92____VlefCall_0__lsn_state_f = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__lsn_state_f__93__Vfuncout = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__lsn_state_f__93__s = 0;
    VL_ZERO_RESET_W(84, vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__fresh_f__94__r);
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__lsn_reg_f__95__s = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__lsn_reg_f__95____VlefCall_0__lsn_state_f = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__lsn_state_f__96__Vfuncout = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__lsn_state_f__96__s = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__src_sid_f__99__Vfuncout = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__src_sid_f__99__s = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__src_sid_f__100__Vfuncout = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__src_sid_f__100__s = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__src_sid_f__101__Vfuncout = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__src_sid_f__101__s = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__src_sid_f__102__Vfuncout = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__src_sid_f__102__s = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte48_f__111__Vfuncout = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte48_f__111__n = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte48_f__111__sh = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte48_f__112__Vfuncout = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte48_f__112__v = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte48_f__112__n = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte48_f__112__sh = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte16_f__113__Vfuncout = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte16_f__113__n = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte16_f__113__sh = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte64_f__114__Vfuncout = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte64_f__114__v = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte64_f__114__n = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte64_f__114__sh = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte64_f__115__Vfuncout = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte64_f__115__v = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte64_f__115__n = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte64_f__115__sh = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte32_f__116__Vfuncout = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte32_f__116__n = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte32_f__116__sh = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte16_f__117__Vfuncout = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte16_f__117__n = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte16_f__117__sh = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte16_f__118__Vfuncout = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte16_f__118__n = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte16_f__118__sh = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte16_f__119__Vfuncout = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte16_f__119__n = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte16_f__119__sh = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte16_f__120__Vfuncout = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte16_f__120__n = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte16_f__120__sh = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte32_f__121__Vfuncout = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte32_f__121__v = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte32_f__121__n = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte32_f__121__sh = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte64_f__122__Vfuncout = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte64_f__122__v = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte64_f__122__n = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte64_f__122__sh = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte16_f__123__Vfuncout = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte16_f__123__v = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte16_f__123__n = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte16_f__123__sh = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte16_f__124__Vfuncout = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte16_f__124__v = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte16_f__124__n = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte16_f__124__sh = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte16_f__125__Vfuncout = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte16_f__125__v = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte16_f__125__n = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__byte16_f__125__sh = 0;
    vlSelf->__Vfunc_adp_vt_to_ms_f__126__vt = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__mac_byte_f__127__m = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__mac_byte_f__127__i = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__mac_byte_f__127__k = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__mac_byte_f__128__i = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__mac_byte_f__128__k = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__mac_byte_f__129__i = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__mac_byte_f__129__k = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__mac_byte_f__130__i = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__mac_byte_f__130__k = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__mac_byte_f__131__i = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__mac_byte_f__131__k = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132____VlefCall_0__hz_is_lockprot = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__same_key_v = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_conflict__132__other_v = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_is_lockprot__133__Vfuncout = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__hz_is_lockprot__133__c = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__159__Vfuncout = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__159__w = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__aaf_rx_depkt__DOT__fbyte__159__j = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rand_offset__183__rnd = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rand_offset__183__cnt = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rand_offset__183__o = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__ms_settle__232__w = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__ms_settle__233__w = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__234__Vfuncout = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__234__s = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__235__Vfuncout = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__235__s = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__236__Vfuncout = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__236__s = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__237__Vfuncout = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__237__s = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__238__Vfuncout = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__238__s = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__239__Vfuncout = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__239__s = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__240__Vfuncout = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__240__s = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__240__w = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__241__Vfuncout = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__241__s = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__241__w = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__242__Vfuncout = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__242__s = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__243__Vfuncout = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__243__s = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__244__Vfuncout = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__244__s = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__245__Vfuncout = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__245__s = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__246__Vfuncout = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__246__s = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__248__Vfuncout = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__248__s = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__249__Vfuncout = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__249__s = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__250__Vfuncout = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__250__s = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__251__Vfuncout = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__251__s = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__252__s = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__253__s = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__254__Vfuncout = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__254__s = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__254__w = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__255__Vfuncout = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__255__s = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__256__Vfuncout = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__256__s = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__257__Vfuncout = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__257__s = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__258__Vfuncout = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__258__s = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__259__s = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__avtp_rx_monitor__DOT__laddr__259__w = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__csr__DOT__is_plain_rw__301__a = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__302__Vfuncout = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__302__t = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__303__Vfuncout = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__303__t = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__304__Vfuncout = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__304__t = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__307__Vfuncout = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__307__t = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__308__Vfuncout = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__308__t = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__310__Vfuncout = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__310__t = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__310__w = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__311__Vfuncout = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__311__t = 0;
    vlSelf->__Vfunc_milan_datapath__DOT__aaf_packetizer__DOT__taddr__311__w = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_9 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_12 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_15 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_20 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_21 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_22 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_26 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_28 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_30 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_31 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_33 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_34 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_35 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_36 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_37 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_38 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_39 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_40 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_41 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_42 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_45 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_46 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_49 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_50 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_51 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_52 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_53 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_54 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_55 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_56 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_58 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_63 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_64 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_65 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_67 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_68 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_69 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_72 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_73 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_80 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_84 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_86 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_87 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_88 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_89 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_91 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_92 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_93 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_94 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_95 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_97 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_98 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_99 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_100 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_105 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_106 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_112 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_113 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_114 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_115 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_118 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_119 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_121 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_122 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_123 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_124 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_128 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_170 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_171 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_172 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_180 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_182 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_183 = 0;
    VL_ZERO_RESET_W(72, vlSelf->__VdfgRegularize_h6e95ff9d_0_184);
    vlSelf->__VdfgRegularize_h6e95ff9d_0_185 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_186 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_187 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_188 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_189 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_190 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_192 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_193 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_194 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_197 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_198 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_201 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_203 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_204 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_205 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_206 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_207 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_208 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_209 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_211 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_212 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_213 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_214 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_215 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_216 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_217 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_223 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_228 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_229 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_235 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_236 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_237 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_238 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_239 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_240 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_242 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_243 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_244 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_245 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_248 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_251 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_253 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_254 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_259 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_260 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_261 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_263 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_264 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_265 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_266 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_267 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_268 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_269 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_270 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_271 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_272 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_273 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_280 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_281 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_282 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_283 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_284 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_285 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_286 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_291 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_292 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_293 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_294 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_296 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_297 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_298 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_300 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_301 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_302 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_303 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_304 = 0;
    vlSelf->__VdfgRegularize_h6e95ff9d_0_308 = 0;
    vlSelf->__Vdly__milan_datapath__DOT__src_pend_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__src_band_ticks_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__src_eng_ticks_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__bound_hold_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxf_vld_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__rxf_drop_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__hdr_vld_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pf_eid_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pf_st_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pf_idx_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__svc_drop_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__st_tk_vld_r = 0;
    VL_ZERO_RESET_W(154, vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__st_tk_r);
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__st_ls_vld_r = 0;
    VL_ZERO_RESET_W(154, vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__st_ls_r);
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__srp_req_valid_w = 0;
    VL_ZERO_RESET_W(154, vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__inflight_r);
    VL_ZERO_RESET_W(1504, vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__armq_r);
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__arm_drop_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__prng_req_w = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pr_pend_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pr_kind_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__pr_inflight_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_drop_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_pend_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__tkb_st_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__txc_pend_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__txc_locked_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__txc_owner_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__sh_idx_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__sh_st_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__opt_cnt_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__opt_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_idx_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_mfs_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_mif_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__svc_st_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__a_open_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__td_tk_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__td_ls_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__rnd_act_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tm_rr_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__cad_pend_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__cnt_msrp_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__cnt_mvrp_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__waddr_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__bidx_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__st_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__msg_open_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__hold_valid_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_type_r = 0;
    VL_ZERO_RESET_W(272, vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_last_r);
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_len_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__run_open_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__msg_type_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__rd_idx_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__join_pend_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__laown_pend_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__wsrc_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__walk_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__app_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__tpend_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__reg_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vj_pend_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_listener__DOT__vl_pend_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__laown_pend_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__wsrc_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__walk_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__app_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__tpend_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__reg_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__lstn_prev_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vj_pend_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_talker__DOT__vl_pend_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__cidx_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__acc_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__over_acc_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_admission__DOT__aidx_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__rejoin_pend_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__st_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__ridx_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__active_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__scan_ix_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_domain__DOT__rx_pend_prio_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_domain__DOT__rx_pend_vid_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_domain__DOT__rx_pend_v_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_domain__DOT__rejoin_pend_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_domain__DOT__decl_prio_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_domain__DOT__decl_vid_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_decoder__DOT__last_seen_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_decoder__DOT__state_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_decoder__DOT__fp_byte_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_decoder__DOT__idx_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_decoder__DOT__slot_left_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_decoder__DOT__sid_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_decoder__DOT__da_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_decoder__DOT__vid_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_decoder__DOT__pr_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_decoder__DOT__lat_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_decoder__DOT__fcode_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_decoder__DOT__dcid_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_decoder__DOT__dprio_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_decoder__DOT__fv_idx_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_decoder__DOT__tp_rd_byte_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_decoder__DOT__tp_rd_dig_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_decoder__DOT__values_left_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_decoder__DOT__attr_type_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_decoder__DOT__app_msrp_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__adp_stall_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__aecp_stall_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__acmp_stall_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__wr_ptr_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__rd_ptr_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__out_valid_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__cnt_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_acmp_q__DOT__wr_ptr_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_acmp_q__DOT__rd_ptr_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_acmp_q__DOT__out_valid_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_acmp_q__DOT__cnt_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_adp_q__DOT__wr_ptr_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_adp_q__DOT__rd_ptr_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_adp_q__DOT__out_valid_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_adp_q__DOT__cnt_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_maap_q__DOT__wr_ptr_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_maap_q__DOT__rd_ptr_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_maap_q__DOT__out_valid_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_maap_q__DOT__cnt_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_stage_ready_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_stage_assem_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gxr_valid_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gxf_tmo_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_rec_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__echo_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__sent_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__bidx_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__frame_len_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__a_st_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_out_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__pld_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_rd_pos_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_hdr_ix_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_data_head_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_rd_pending_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_data_ix_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_load_data_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_rec_rlen_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__upc_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cfg_ix_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__desc_ty_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__ctrs_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__regun_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__acq_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__lockc_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gstri_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gavb_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gasp_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__eavl_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gcfg_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gsfmt_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gsrate_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gclks_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__ssrate_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__sclks_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__ssfmt_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__ssinfo_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gctrl_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__sctrl_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gname_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__sname_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__scfg_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__setc_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__desc_ix_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__name_ix_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__name_cfg_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_rec_len_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__gdi_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_scan_started_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__pld_cmd_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__rerr_cnt_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__g_sub_end_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__drop_cnt_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__disp_valid_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__walk_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__setval_r = 0;
    VL_ZERO_RESET_W(393, vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__cmd_r);
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_edit_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_remove_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_uns_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__uns_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__tmo_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__st_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__lane_open_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__seal_pend_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__served_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__rvalid_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__roff_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__len_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__sk_valid_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__bix_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__rbusy_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__rreq_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_resp__DOT__wbusy_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__mreq_valid_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__mem_busy_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__beat_ix_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__tmo_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__st_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__miss_cnt_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__desc_len_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__desc_nbase_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__mreq_beats_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__scan_rd_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__heal_pend_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__key_type_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__heal_kind_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__name_load_lane_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__ms_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__rom_q_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__vld_d_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__vld_e_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__uop_e_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__opa_e_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__opb_e_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__opd_e_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__eseq_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__cursor_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__resp_len_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__DOT__wr_ptr_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__DOT__wr_active_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__DOT__occupied_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__4__KET____DOT__u_rx_slots__DOT__wr_ptr_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__4__KET____DOT__u_rx_slots__DOT__wr_active_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__4__KET____DOT__u_rx_slots__DOT__occupied_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__2__KET____DOT__u_rx_slots__DOT__wr_ptr_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__2__KET____DOT__u_rx_slots__DOT__wr_active_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__2__KET____DOT__u_rx_slots__DOT__occupied_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__1__KET____DOT__u_rx_slots__DOT__wr_ptr_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__1__KET____DOT__u_rx_slots__DOT__wr_active_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__1__KET____DOT__u_rx_slots__DOT__occupied_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__0__KET____DOT__u_rx_slots__DOT__wr_ptr_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__0__KET____DOT__u_rx_slots__DOT__wr_active_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__0__KET____DOT__u_rx_slots__DOT__occupied_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__0__KET____DOT__u_rx_slots__DOT__ovr_cnt_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_side_port__DOT__state_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__arb_st_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__owner_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__sof_pend_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__held_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__release_pend_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__run_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__fetch_idx_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__out_valid_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__out_last_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__cmdq_count_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__ctr_dirty_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__ctr_pend_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__mon_draw_pend_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__ca_probe_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__mon_draw_wait_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__mon_draw_ix_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__lk_held_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__lk_ctlr_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__lockx_v_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__n_st_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__dh_v_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__em_active_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__em_ix_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__wk_ix_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__hold_eid_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__hold_mac_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__dh_eid_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__dh_mac_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__dh_seq_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__valid_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__lockx_eid_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__pending_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__done_seen_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__state_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__bcnt_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__hidx_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__plen_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__rec_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__deb_open_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__deb_cnt_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__fl_arm_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__hs_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__fl_retry_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__fl_sink_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__rp_k_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__rs_k_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__rplen_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__rcrc_rx_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__rvld_q_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__mrp_drop_w = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_mrp_strip__DOT__wr_tent_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_mrp_strip__DOT__out_vld_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__draw_req_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__w_st_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_maap__DOT__ival_ann_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__mreq_tmo_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__state_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__slot_len_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__fetch_ix_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__maap_stale_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__f_cap_v_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__xs_r = 0;
    VL_ZERO_RESET_W(384, vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__rec_r);
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__strt_was_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__bnd_was_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__cellmut_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__strq_done_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__ord_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__draw_issued_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__probe_ctr_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__errflow_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__f_idx_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__sink_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__strq_pend_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__strq_busy_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__strq_tmo_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__cap_vld_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__rx_st_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__sink_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__adv_startup_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__draw_req_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__bld_st_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_normalizer__DOT__txn_valid_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__alloc_req_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__abort_pend_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__slot_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__fr_st_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__idx_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__src_mac_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__msg_type_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__status_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__cdl_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__target_eid_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__ctlr_eid_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__seq_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__u_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__cr_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__opcode_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__desc_type_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__desc_index_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__tuid_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__luid_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__subtype_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__cp_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__cnt_len_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__cnt_da_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__cnt_ver_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__cnt_et_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__cnt_sub_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__rptr_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__vrptr_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_ca_builder__DOT__c_st_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_ca_builder__DOT__alloc_wait_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__valid_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__retried_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_trace__DOT__wr_count_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__valid_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__seeded_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__prng_valid_w = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_prng__DOT__busy_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__us_cnt_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__now_ms_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__sweep_addr_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__sweep_pend_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__ms_div_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__commit_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__commit_busy_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__alive_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__cap_open_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__cap_valid_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__cap_hold_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__hold_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__st_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__addr_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__cnt_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__wc_data_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__ld_ok_r = 0;
    VL_ZERO_RESET_W(256, vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__open_r);
    VL_ZERO_RESET_W(256, vlSelf->__VdlyMask__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__open_r);
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__ctl_fifo__DOT__wr_ptr_reg = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__ctl_fifo__DOT__m_axis_tvalid_pipe_reg = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_shadow__DOT__ctl_fifo__DOT__rd_ptr_reg = 0;
    vlSelf->__Vdly__milan_datapath__DOT__ethernet_counters__DOT____Vcellout__event_counter_gen__BRA__8__KET____DOT__counter_inst__count = 0;
    vlSelf->__Vdly__milan_datapath__DOT__ethernet_counters__DOT____Vcellout__event_counter_gen__BRA__7__KET____DOT__counter_inst__count = 0;
    vlSelf->__Vdly__milan_datapath__DOT__ethernet_counters__DOT____Vcellout__event_counter_gen__BRA__6__KET____DOT__counter_inst__count = 0;
    vlSelf->__Vdly__milan_datapath__DOT__ethernet_counters__DOT____Vcellout__event_counter_gen__BRA__5__KET____DOT__counter_inst__count = 0;
    vlSelf->__Vdly__milan_datapath__DOT__ethernet_counters__DOT____Vcellout__event_counter_gen__BRA__4__KET____DOT__counter_inst__count = 0;
    vlSelf->__Vdly__milan_datapath__DOT__ethernet_counters__DOT____Vcellout__event_counter_gen__BRA__3__KET____DOT__counter_inst__count = 0;
    vlSelf->__Vdly__milan_datapath__DOT__ethernet_counters__DOT____Vcellout__event_counter_gen__BRA__2__KET____DOT__counter_inst__count = 0;
    vlSelf->__Vdly__milan_datapath__DOT__ethernet_counters__DOT____Vcellout__event_counter_gen__BRA__1__KET____DOT__counter_inst__count = 0;
    vlSelf->__Vdly__milan_datapath__DOT__ethernet_counters__DOT____Vcellout__event_counter_gen__BRA__0__KET____DOT__counter_inst__count = 0;
    vlSelf->__Vdly__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__cyc_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__active_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__stg_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__samples_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__timeouts_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__active_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__stg_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__samples_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__timeouts_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__wptr_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__was_filled_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__prefill_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__cdc_wen_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__ms_div_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__i2spb_overruns = 0;
    vlSelf->__Vdly__milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__u_clr_under_cdc__DOT__src_level = 0;
    vlSelf->__Vdly__milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__locked_sync_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__psbusy_sync_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__hs_send_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__u_gain_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__state_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__win_skip_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__lock_cnt_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__dstate_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__u_cmd_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__integ_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__acc_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__win_valid_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__disc_run_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__disc_cnt_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__ps_hold_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__rd_second_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__drp_pass_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__repairing_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__tick_cnt_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__pp_d_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__pp_rate_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__pp_run_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__pp_seq_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__u_tick_cdc__DOT__sync = 0;
    vlSelf->__Vdly__milan_datapath__DOT__g_mmcm_servo__DOT__mmcm_servo__DOT__u_batch_hs__DOT__ack_sync = 0;
    vlSelf->__Vdly__milan_datapath__DOT__crf_tx__DOT__u_evt_cdc__DOT__sync = 0;
    vlSelf->__Vdly__milan_datapath__DOT__aaf_rx_depkt__DOT__idxq_rp_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__aaf_rx_depkt__DOT__rbeat_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__aaf_rx_depkt__DOT__vlan_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__aaf_rx_depkt__DOT__remain_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__aaf_rx_depkt__DOT__rstate_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__wr_ptr_reg = 0;
    vlSelf->__Vdly__milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_tvalid_pipe_reg = 0;
    vlSelf->__Vdly__milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__rd_ptr_reg = 0;
    vlSelf->__Vdly__milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__rbeat_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__is_maap_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tickdiv_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__timer_ms_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_beat_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__tx_busy_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__maap_conflicts = 0;
    vlSelf->__Vdly__milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__probe_left_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__offset_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__g_maap__DOT__maap_engine__DOT__state_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__xl1_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__yl1_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__xr1_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__yr1_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__busy_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__step_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__acc_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__yl_hold_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__adp_tx_mux__DOT__locked_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__adp_tx_mux__DOT__sel_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__adp_tx_mux__DOT__flush_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__adp_tx_mux__DOT__to_cnt_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__crf_dp_mux__DOT__locked_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__crf_dp_mux__DOT__sel_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__crf_dp_mux__DOT__flush_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__crf_dp_mux__DOT__to_cnt_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__ctl_tx_mux__DOT__locked_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__ctl_tx_mux__DOT__sel_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__ctl_tx_mux__DOT__flush_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__ctl_tx_mux__DOT__to_cnt_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__render_setpoint__DOT__sched_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__render_setpoint__DOT__slot_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__render_setpoint__DOT__beat_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__render_setpoint__DOT__ms_div_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__ms_div_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__iv_div_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__pq_cnt_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__bind_pend_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__sil_pend_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__mst_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__locked_sh_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__iv_res_list_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__wrph_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__bind_zero_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__zero_idx_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__inc_rd_q_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__inc_list_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__iv_res_s_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__avtprx_accept_idx_w = 0;
    vlSelf->__Vdly__milan_datapath__DOT__avtp_rx_monitor__DOT__ev_s_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__media_grid_align__DOT__quiet_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__media_grid_align__DOT__slip_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__media_grid_align__DOT__acc_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__mnco_servo_trim_w = 0;
    vlSelf->__Vdly__milan_datapath__DOT__crf_rx__DOT__iv_div_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__crf_intrcnt_w = 0;
    vlSelf->__Vdly__milan_datapath__DOT__crf_pducnt_w = 0;
    vlSelf->__Vdly__milan_datapath__DOT__crf_rx__DOT__iv_frx_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__crf_rx__DOT__iv_uf_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__crf_rx__DOT__iv_sm_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__crf_rx__DOT__iv_mr_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__crf_rx__DOT__iv_tu_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__crf_rx__DOT__iv_lt_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__crf_rx__DOT__iv_et_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__crf_rx__DOT__tout_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__crf_locked_w = 0;
    vlSelf->__Vdly__milan_datapath__DOT__crf_rx__DOT__settle_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__crf_rx__DOT__have_seq_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__crf_rx__DOT__hfill_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__crf_rx__DOT__hidx_r = 0;
    VL_ZERO_RESET_W(448, vlSelf->__Vdly__milan_datapath__DOT__avtp_rx_parser__DOT__hdr);
    vlSelf->__Vdly__milan_datapath__DOT__avtp_rx_parser__DOT__bytes_in = 0;
    vlSelf->__Vdly__milan_datapath__DOT__talker_diag__DOT__tick_cnt_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__talker_diag__DOT__seen_f_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__talker_diag__DOT__seen_tu_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__talker_diag__DOT__seen_mr_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__media_clock_restart__DOT__tgt_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__mcr_mr_v_w = 0;
    vlSelf->__Vdly__milan_datapath__DOT__link_guard__DOT__act_sync_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__link_guard__DOT__rx_dead_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__link_guard__DOT__tx_dead_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__link_guard__DOT__act_age_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__link_guard__DOT__state_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__link_guard__DOT__bounced_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__link_guard__DOT__bounce_cnt_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__link_guard__DOT__settle_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__ptp_sync__DOT__load_tgl = 0;
    vlSelf->__Vdly__milan_datapath__DOT__ptp_sync__DOT__adj_tgl = 0;
    vlSelf->__Vdly__milan_datapath__DOT__ptp_sync__DOT__snap_tgl = 0;
    vlSelf->__Vdly__milan_datapath__DOT__ptp_sync__DOT__snap_ret_s = 0;
    vlSelf->__Vdly__milan_datapath__DOT__csr__DOT__sweep_cnt = 0;
    vlSelf->__Vdly__milan_datapath__DOT__csr__DOT__g_pp_csr__DOT__pp_busy_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__csr__DOT__cmrd_busy_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__csr__DOT__cmrd_flush_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__csr__DOT__cmrd_wd_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__csr__DOT__snap_st_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__csr__DOT__snap_req_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__csr__DOT__snap_m8_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__csr__DOT__snap_wi_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__ptp_clock_validity__DOT__qdiv_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__ptp_clock_validity__DOT__hold_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__ptp_clock_validity__DOT__ival_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__aaf_packetizer__DOT__stg_q_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__aaf_packetizer__DOT__tsw_pend_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__aaf_packetizer__DOT__est_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__aaf_packetizer__DOT__eiss_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__aaf_packetizer__DOT__eo_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__aaf_packetizer__DOT__ecap_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__aaf_packetizer__DOT__fph_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__aaf_packetizer__DOT__ext_trd_q_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__chan_map_capture__DOT__skid_cnt_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__chan_map_capture__DOT__skid_rp_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__chan_map_capture__DOT__st_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__chan_map_capture__DOT__slot_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__chan_map_capture__DOT__pop_idx_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__tone_gen_media__DOT__idx_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__media_nco__DOT__cnt_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__g_aif_i2s__DOT__aaf_capture__DOT__tarst_n_r = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_ack_w = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_rdata_w = 0;
    vlSelf->__Vdly__milan_datapath__DOT__pp_err_w = 0;
    vlSelf->__Vdly__milan_datapath__DOT__g_aif_i2s__DOT__aaf_capture__DOT__cap_ren_r = 0;
    VL_ZERO_RESET_W(88, vlSelf->__Vdly__milan_datapath__DOT__ts_counter__DOT__acc);
    vlSelf->__VdlyVal__milan_datapath__DOT__tctx_chans_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__tctx_chans_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__tctx_chans_r__v1 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tf_ram_r__v0 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tf_ram_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tf_ram_r__v0 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tf_ram_r__v1 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tf_ram_r__v1 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tf_ram_r__v1 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tf_q_r__v0 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tf_q_r__v1 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tf_wptr_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tf_wptr_r__v0 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tf_wptr_r__v1 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tf_wptr_r__v1 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tf_wptr_r__v2 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tf_cnt_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tf_rptr_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tf_rptr_r__v1 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tf_rptr_r__v2 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__tf_cnt_r__v3 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__mvrp_ram_r__v0 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__mvrp_ram_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__mvrp_ram_r__v0 = 0;
    VL_ZERO_RESET_W(285, vlSelf->__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__msrp_ram_r__v0);
    vlSelf->__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__msrp_ram_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_encoder__DOT__msrp_ram_r__v0 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__tbl_r__v0 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__tbl_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_vlan__DOT__tbl_r__v0 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_decoder__DOT__tp_ram__v0 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_decoder__DOT__tp_ram__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_srp__DOT__u_decoder__DOT__tp_ram__v0 = 0;
    VL_ZERO_RESET_W(393, vlSelf->__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__mem_r__v0);
    vlSelf->__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__mem_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_aecp_q__DOT__mem_r__v0 = 0;
    VL_ZERO_RESET_W(393, vlSelf->__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_acmp_q__DOT__mem_r__v0);
    vlSelf->__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_acmp_q__DOT__mem_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_acmp_q__DOT__mem_r__v0 = 0;
    VL_ZERO_RESET_W(393, vlSelf->__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_adp_q__DOT__mem_r__v0);
    vlSelf->__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_adp_q__DOT__mem_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_adp_q__DOT__mem_r__v0 = 0;
    VL_ZERO_RESET_W(393, vlSelf->__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_maap_q__DOT__mem_r__v0);
    vlSelf->__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_maap_q__DOT__mem_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_dispatch__DOT__u_maap_q__DOT__mem_r__v0 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_stage_r__v0 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_stage_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__amap_stage_r__v0 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__ptoff_r__v0 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__ptoff_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__ptoff_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__ptoff_r__v1 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__clksrc_r__v0 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__clksrc_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__clksrc_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__clksrc_r__v1 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__rate_r__v0 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__rate_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__rate_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__rate_r__v1 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__fmtout_r__v0 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__fmtout_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__fmtout_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__fmtout_r__v1 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__ident_r__v0 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__ident_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__ident_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__ident_r__v1 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__fmtin_r__v0 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__fmtin_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__fmtin_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_dyn__DOT__fmtin_r__v1 = 0;
    VL_ZERO_RESET_W(128, vlSelf->__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__idx_r__v0);
    vlSelf->__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__idx_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__idx_r__v0 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__line_r__v0 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__line_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__line_r__v0 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__name_r__v0 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__name_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__name_r__v0 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__name_r__v1 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__name_r__v1 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__name_r__v1 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__name_r__v2 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__name_r__v2 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__name_r__v2 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__name_r__v3 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__name_r__v3 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__name_r__v3 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__name_r__v4 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__name_r__v4 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__name_r__v4 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__name_r__v5 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__name_r__v5 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__name_r__v5 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__name_r__v6 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__name_r__v6 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__name_r__v6 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__name_r__v7 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__name_r__v7 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__name_r__v7 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__rf_r__v0 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__rf_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_ucpu__DOT__rf_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__DOT__len_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__DOT__len_r__v1 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__DOT__mem_r__v0 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__DOT__mem_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__5__KET____DOT__u_rx_slots__DOT__mem_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__4__KET____DOT__u_rx_slots__DOT__len_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__4__KET____DOT__u_rx_slots__DOT__len_r__v1 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__4__KET____DOT__u_rx_slots__DOT__mem_r__v0 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__4__KET____DOT__u_rx_slots__DOT__mem_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__4__KET____DOT__u_rx_slots__DOT__mem_r__v0 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__2__KET____DOT__u_rx_slots__DOT__len_r__v0 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__2__KET____DOT__u_rx_slots__DOT__len_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__2__KET____DOT__u_rx_slots__DOT__len_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__2__KET____DOT__u_rx_slots__DOT__len_r__v1 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__2__KET____DOT__u_rx_slots__DOT__mem_r__v0 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__2__KET____DOT__u_rx_slots__DOT__mem_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__2__KET____DOT__u_rx_slots__DOT__mem_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__1__KET____DOT__u_rx_slots__DOT__len_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__1__KET____DOT__u_rx_slots__DOT__len_r__v1 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__1__KET____DOT__u_rx_slots__DOT__mem_r__v0 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__1__KET____DOT__u_rx_slots__DOT__mem_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__1__KET____DOT__u_rx_slots__DOT__mem_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__0__KET____DOT__u_rx_slots__DOT__len_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__0__KET____DOT__u_rx_slots__DOT__len_r__v1 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__0__KET____DOT__u_rx_slots__DOT__mem_r__v0 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__0__KET____DOT__u_rx_slots__DOT__mem_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__g_rx_pool__BRA__0__KET____DOT__u_rx_slots__DOT__mem_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__age_r__v0 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__age_r__v1 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__age_r__v1 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__age_r__v2 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__age_r__v3 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__age_r__v4 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__age_r__v4 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__age_r__v5 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__age_r__v6 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__age_r__v7 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__age_r__v7 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__age_r__v8 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__age_r__v9 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__age_r__v10 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__age_r__v10 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__age_r__v11 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__age_r__v12 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__age_r__v13 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__age_r__v13 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__age_r__v14 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__age_r__v15 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__age_r__v16 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__age_r__v16 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__age_r__v17 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__age_r__v18 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__age_r__v19 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__age_r__v19 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__age_r__v20 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__age_r__v21 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__age_r__v22 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__age_r__v22 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__age_r__v23 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__age_r__v24 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__cnt_r__v0 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__cnt_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__cnt_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_arbiter__DOT__cnt_r__v1 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__st_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__st_r__v0 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__st_r__v1 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__st_r__v1 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__st_r__v2 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__st_r__v2 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__st_r__v3 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__st_r__v3 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__st_r__v4 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__st_r__v4 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__st_r__v5 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__st_r__v5 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__st_r__v6 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__st_r__v6 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__st_r__v7 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__st_r__v8 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__len_r__v0 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__len_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__len_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__len_r__v1 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__mem_r__v0 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__mem_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_tx_slots__DOT__mem_r__v0 = 0;
    VL_ZERO_RESET_W(128, vlSelf->__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__rows_r__v0);
    vlSelf->__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__rows_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__rows_r__v0 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__cmdq_class_r__v0 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__cmdq_class_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__cmdq_class_r__v0 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__cmdq_type_r__v0 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__cmdq_type_r__v0 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__cmdq_index_r__v0 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__cmdq_index_r__v0 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__cmdq_arg0_r__v0 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__cmdq_arg0_r__v0 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__cmdq_arg1_r__v0 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__cmdq_arg1_r__v0 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__cmdq_excl_r__v0 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__cmdq_excl_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__ctr_last_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__ctr_last_r__v1 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__ctr_last_r__v2 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r__v0 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r__v0 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r__v1 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r__v1 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r__v1 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r__v1 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r__v2 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r__v2 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r__v2 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r__v2 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r__v3 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r__v3 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r__v3 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r__v3 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r__v4 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r__v4 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r__v4 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r__v4 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r__v5 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r__v5 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r__v5 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r__v5 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r__v6 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r__v6 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r__v6 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r__v6 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r__v7 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r__v7 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r__v7 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r__v7 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r__v8 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r__v8 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r__v8 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r__v8 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r__v9 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r__v9 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r__v9 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r__v9 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r__v10 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r__v10 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r__v10 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r__v10 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__lost_cnt_r__v11 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_event_router__DOT__payload_r__v11 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__hdr_r__v0 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__hdr_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__hdr_r__v0 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__hdr_r__v1 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__hdr_r__v1 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__hdr_r__v1 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_port__DOT__hdr_r__v2 = 0;
    VL_ZERO_RESET_W(146, vlSelf->__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__shw_ram_r__v0);
    vlSelf->__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__shw_ram_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_nvm_shadow__DOT__shw_ram_r__v0 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_mrp_strip__DOT__ram_r__v0 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_mrp_strip__DOT__ram_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_mrp_strip__DOT__ram_r__v0 = 0;
    VL_ZERO_RESET_W(84, vlSelf->__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__rec_ram_r__v0);
    vlSelf->__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__rec_ram_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_talker__DOT__rec_ram_r__v0 = 0;
    VL_ZERO_RESET_W(384, vlSelf->__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__rec_ram_r__v0);
    vlSelf->__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__rec_ram_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_listener__DOT__rec_ram_r__v0 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__disc_rec_r__v0 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__disc_rec_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__disc_rec_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__tpend_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__adv_st_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__adv_st_r__v1 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__adv_st_r__v2 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__tpend_r__v1 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__adv_st_r__v3 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__tpend_r__v2 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__adv_st_r__v4 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__tpend_deadline_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__tpend_r__v4 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__tpend_deadline_r__v1 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__adv_st_r__v5 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__adv_st_r__v6 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__adv_st_r__v7 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__adv_st_r__v8 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__adv_st_r__v9 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__aidx_r__v0 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__aidx_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__aidx_r__v0 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__aidx_r__v1 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__aidx_r__v1 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_adp__DOT__aidx_r__v2 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__vq_r__v0 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__vq_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__vq_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__vq_r__v1 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__mrp_mem_r__v0 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__mrp_mem_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_rx_validator__DOT__mrp_mem_r__v0 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__owner_r__v0 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__owner_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__owner_r__v0 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__tslot_r__v0 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__tslot_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__tslot_r__v0 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__seq_r__v0 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__seq_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__seq_r__v0 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__seq_ctr_r__v0 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__seq_ctr_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__seq_ctr_r__v1 = 0;
    VL_ZERO_RESET_W(112, vlSelf->__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__key_r__v0);
    vlSelf->__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__key_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__key_r__v0 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__tout_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__tout_r__v0 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__txs_r__v0 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__txs_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_originator__DOT__txs_r__v0 = 0;
    VL_ZERO_RESET_W(128, vlSelf->__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_trace__DOT__mem_r__v0);
    vlSelf->__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_trace__DOT__mem_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_trace__DOT__mem_r__v0 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__cls_r__v0 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__cls_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__cls_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__cls_r__v1 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__key_r__v0 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__key_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__key_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_scoreboard__DOT__key_r__v1 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__slot_ram_r__v0 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__slot_ram_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__slot_ram_r__v0 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__mapi_pref_r__v0 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__mapi_pref_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__mapi_pref_r__v0 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__mapo_pref_r__v0 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__mapo_pref_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__mapo_pref_r__v0 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__mapo_len_r__v0 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__mapo_len_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__mapo_len_r__v0 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__mapi_len_r__v0 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__mapi_len_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__u_nvm__DOT__mapi_len_r__v0 = 0;
    VL_ZERO_RESET_W(74, vlSelf->__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__ctl_fifo__DOT__mem__v0);
    vlSelf->__VdlyDim0__milan_datapath__DOT__pp_shadow__DOT__ctl_fifo__DOT__mem__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__ctl_fifo__DOT__mem__v0 = 0;
    VL_ZERO_RESET_W(74, vlSelf->__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__ctl_fifo__DOT__m_axis_pipe_reg__v0);
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__ctl_fifo__DOT__m_axis_pipe_reg__v0 = 0;
    VL_ZERO_RESET_W(74, vlSelf->__VdlyVal__milan_datapath__DOT__pp_shadow__DOT__ctl_fifo__DOT__m_axis_pipe_reg__v1);
    vlSelf->__VdlySet__milan_datapath__DOT__pp_shadow__DOT__ctl_fifo__DOT__m_axis_pipe_reg__v1 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__last_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__last_r__v3 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__min_r__v3 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__max_r__v3 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__last_r__v4 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__min_r__v4 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__max_r__v4 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__last_r__v5 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__min_r__v5 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__max_r__v5 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__last_r__v6 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__last_r__v7 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__last_r__v8 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__rx_chain__DOT__last_r__v9 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__last_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__last_r__v3 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__min_r__v3 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__max_r__v3 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__last_r__v4 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__min_r__v4 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__max_r__v4 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__last_r__v5 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__min_r__v5 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__max_r__v5 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__last_r__v6 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__last_r__v7 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__last_r__v8 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aaf_latency_tap_bank__DOT__g_ltap__DOT__aaf_latency_taps__DOT__tx_chain__DOT__last_r__v9 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__stg_r__v0 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__stg_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__stg_r__v0 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__stg_r__v1 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__stg_r__v1 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__stg_r__v1 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__fifo_r__v0 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__fifo_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__fifo_r__v0 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__u_cdc__DOT__mem_r__v0 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__u_cdc__DOT__mem_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__g_i2s_player__DOT__i2s_player__DOT__u_cdc__DOT__mem_r__v0 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_mask__v0 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_mask__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_mask__v0 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_valid__v0 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_valid__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_valid__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_valid__v1 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_action__v0 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_action__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_action__v0 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_key__v0 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_key__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__g_rx_filter__DOT__rx_filter__DOT__mac_cam__DOT__ent_key__v0 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__aaf_rx_depkt__DOT__idxq_r__v0 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__aaf_rx_depkt__DOT__idxq_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aaf_rx_depkt__DOT__idxq_r__v0 = 0;
    VL_ZERO_RESET_W(74, vlSelf->__VdlyVal__milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__mem__v0);
    vlSelf->__VdlyDim0__milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__mem__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__mem__v0 = 0;
    VL_ZERO_RESET_W(74, vlSelf->__VdlyVal__milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg__v0);
    vlSelf->__VdlySet__milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg__v0 = 0;
    VL_ZERO_RESET_W(74, vlSelf->__VdlyVal__milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg__v1);
    vlSelf->__VdlySet__milan_datapath__DOT__aaf_rx_depkt__DOT__frame_fifo__DOT__m_axis_pipe_reg__v1 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__bfifo_r__v0 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__bfifo_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__g_pcm_lpf__DOT__pcm_lpf__DOT__bfifo_r__v0 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__map_r__v0 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__chan_map_render__DOT__map_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__chan_map_render__DOT__map_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__chan_map_render__DOT__map_r__v1 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__cur_r__v0 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__chan_map_render__DOT__cur_r__v0 = 0;
    vlSelf->__VdlyDim1__milan_datapath__DOT__chan_map_render__DOT__cur_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__chan_map_render__DOT__cur_r__v0 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__cur_r__v1 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__chan_map_render__DOT__cur_r__v1 = 0;
    vlSelf->__VdlyDim1__milan_datapath__DOT__chan_map_render__DOT__cur_r__v1 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__chan_map_render__DOT__cur_r__v1 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__chan_map_render__DOT__cur_r__v2 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__sel_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__chan_map_render__DOT__sel_r__v0 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__sel_r__v1 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__chan_map_render__DOT__sel_r__v1 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__sel_r__v2 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__chan_map_render__DOT__sel_r__v2 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__sel_r__v3 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__chan_map_render__DOT__sel_r__v3 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__sel_r__v4 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__chan_map_render__DOT__sel_r__v4 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__sel_r__v5 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__chan_map_render__DOT__sel_r__v5 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__sel_r__v6 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__chan_map_render__DOT__sel_r__v6 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__sel_r__v7 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__chan_map_render__DOT__sel_r__v7 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__sel_r__v8 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__chan_map_render__DOT__sel_r__v8 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__sel_r__v9 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__chan_map_render__DOT__sel_r__v9 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__sel_r__v10 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__chan_map_render__DOT__sel_r__v10 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__sel_r__v11 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__chan_map_render__DOT__sel_r__v11 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__sel_r__v12 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__chan_map_render__DOT__sel_r__v12 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__sel_r__v13 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__chan_map_render__DOT__sel_r__v13 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__sel_r__v14 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__chan_map_render__DOT__sel_r__v14 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__sel_r__v15 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__chan_map_render__DOT__sel_r__v15 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__sel_r__v16 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__chan_map_render__DOT__sel_r__v16 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__sel_r__v17 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__chan_map_render__DOT__sel_r__v17 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__sel_r__v18 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__chan_map_render__DOT__sel_r__v18 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__sel_r__v19 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__chan_map_render__DOT__sel_r__v19 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__sel_r__v20 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__chan_map_render__DOT__sel_r__v20 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__sel_r__v21 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__chan_map_render__DOT__sel_r__v21 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__sel_r__v22 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__chan_map_render__DOT__sel_r__v22 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__sel_r__v23 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__chan_map_render__DOT__sel_r__v23 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__sel_r__v24 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__chan_map_render__DOT__sel_r__v24 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__sel_r__v25 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__chan_map_render__DOT__sel_r__v25 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__sel_r__v26 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__chan_map_render__DOT__sel_r__v26 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__sel_r__v27 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__chan_map_render__DOT__sel_r__v27 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__sel_r__v28 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__chan_map_render__DOT__sel_r__v28 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__chan_map_render__DOT__sel_r__v29 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__chan_map_render__DOT__sel_r__v29 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__chan_map_render__DOT__sel_r__v30 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__render_setpoint__DOT__h1_r__v0 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__render_setpoint__DOT__h1_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__render_setpoint__DOT__h1_r__v0 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__render_setpoint__DOT__h0e_r__v0 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__render_setpoint__DOT__h0e_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__render_setpoint__DOT__h0e_r__v0 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__render_setpoint__DOT__h0o_r__v0 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__render_setpoint__DOT__h0o_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__render_setpoint__DOT__h0o_r__v0 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__render_setpoint__DOT__chans_q_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__render_setpoint__DOT__chans_q_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__render_setpoint__DOT__chans_q_r__v1 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__render_setpoint__DOT__prefill_r__v0 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__render_setpoint__DOT__conv_ms_r__v1 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__render_setpoint__DOT__conv_ms_r__v1 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__render_setpoint__DOT__converged_r__v1 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v1 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v1 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__render_setpoint__DOT__prefill_r__v2 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__render_setpoint__DOT__dev_ok_r__v2 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__render_setpoint__DOT__dev_ok_r__v2 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v2 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v2 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__render_setpoint__DOT__prefill_r__v3 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__render_setpoint__DOT__pend_r__v2 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v3 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__render_setpoint__DOT__rptr_r__v3 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__render_setpoint__DOT__dev_ok_r__v6 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__render_setpoint__DOT__wptr_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__render_setpoint__DOT__wptr_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__render_setpoint__DOT__wptr_r__v1 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__pcm_route__DOT__route_r__v0 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__pcm_route__DOT__route_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pcm_route__DOT__route_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__pcm_route__DOT__route_r__v1 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__lctx_r__v0 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__avtp_rx_monitor__DOT__lctx_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__lctx_r__v0 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__diag_mirror__BRA__0__KET____DOT__col_r__v0 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__avtp_rx_monitor__DOT__diag_mirror__BRA__0__KET____DOT__col_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__diag_mirror__BRA__0__KET____DOT__col_r__v0 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__diag_mirror__BRA__1__KET____DOT__col_r__v0 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__avtp_rx_monitor__DOT__diag_mirror__BRA__1__KET____DOT__col_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__diag_mirror__BRA__1__KET____DOT__col_r__v0 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__diag_mirror__BRA__2__KET____DOT__col_r__v0 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__avtp_rx_monitor__DOT__diag_mirror__BRA__2__KET____DOT__col_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__diag_mirror__BRA__2__KET____DOT__col_r__v0 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__diag_mirror__BRA__3__KET____DOT__col_r__v0 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__avtp_rx_monitor__DOT__diag_mirror__BRA__3__KET____DOT__col_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__diag_mirror__BRA__3__KET____DOT__col_r__v0 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__diag_mirror__BRA__4__KET____DOT__col_r__v0 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__avtp_rx_monitor__DOT__diag_mirror__BRA__4__KET____DOT__col_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__diag_mirror__BRA__4__KET____DOT__col_r__v0 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__diag_mirror__BRA__5__KET____DOT__col_r__v0 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__avtp_rx_monitor__DOT__diag_mirror__BRA__5__KET____DOT__col_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__diag_mirror__BRA__5__KET____DOT__col_r__v0 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__diag_mirror__BRA__6__KET____DOT__col_r__v0 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__avtp_rx_monitor__DOT__diag_mirror__BRA__6__KET____DOT__col_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__diag_mirror__BRA__6__KET____DOT__col_r__v0 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__diag_mirror__BRA__7__KET____DOT__col_r__v0 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__avtp_rx_monitor__DOT__diag_mirror__BRA__7__KET____DOT__col_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__diag_mirror__BRA__7__KET____DOT__col_r__v0 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__diag_mirror__BRA__8__KET____DOT__col_r__v0 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__avtp_rx_monitor__DOT__diag_mirror__BRA__8__KET____DOT__col_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__diag_mirror__BRA__8__KET____DOT__col_r__v0 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__diag_mirror__BRA__9__KET____DOT__col_r__v0 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__avtp_rx_monitor__DOT__diag_mirror__BRA__9__KET____DOT__col_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__diag_mirror__BRA__9__KET____DOT__col_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r__v1 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r__v2 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r__v3 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_pend_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__ddrop_pend_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r__v1 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r__v2 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__avtp_rx_monitor__DOT__tv_cnt_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__tv_cnt_r__v0 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__avtp_rx_monitor__DOT__tnv_cnt_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__tnv_cnt_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__dpdu_pend_r__v1 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__ddrop_pend_r__v1 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r__v3 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__tv_cnt_r__v1 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__avtp_rx_monitor__DOT__tv_cnt_r__v1 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__tv_cnt_r__v1 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__avtp_rx_monitor__DOT__tnv_cnt_r__v1 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__avtp_rx_monitor__DOT__tnv_cnt_r__v1 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__tnv_cnt_r__v1 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__chans_sh_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__sil_ms_r__v4 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__iv_seen_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__frx_acc_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__iv_seen_r__v1 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__iv_seen_r__v2 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__frx_acc_r__v2 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r__v5 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__pq_r__v6 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__frx_acc_r__v3 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__avtp_rx_monitor__DOT__chans_sh_r__v1 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__crf_rx__DOT__ts_hist_r__v0 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__crf_rx__DOT__ts_hist_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__crf_rx__DOT__ts_hist_r__v0 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__stream_table__DOT__ovr_sid_r__v0 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__stream_table__DOT__ovr_sid_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__stream_table__DOT__ovr_sid_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__stream_table__DOT__ovr_sid_r__v1 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__stream_table__DOT__ovr_en_r__v0 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__stream_table__DOT__ovr_en_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__stream_table__DOT__ovr_en_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__stream_table__DOT__ovr_en_r__v1 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__stream_table__DOT__ovr_armed_r__v0 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__stream_table__DOT__ovr_armed_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__stream_table__DOT__ovr_armed_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__stream_table__DOT__ovr_armed_r__v1 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__talker_diag__DOT__ftx_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__talker_diag__DOT__ftx_r__v0 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__talker_diag__DOT__tuiv_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__talker_diag__DOT__tuiv_r__v0 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__talker_diag__DOT__mreset_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__talker_diag__DOT__mreset_r__v0 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__talker_diag__DOT__ftx_r__v1 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__talker_diag__DOT__ftx_r__v1 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__talker_diag__DOT__tuiv_r__v1 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__talker_diag__DOT__tuiv_r__v1 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__talker_diag__DOT__mreset_r__v1 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__talker_diag__DOT__mreset_r__v1 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__talker_diag__DOT__start_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__talker_diag__DOT__start_r__v0 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__talker_diag__DOT__stop_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__talker_diag__DOT__stop_r__v0 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__talker_diag__DOT__start_r__v1 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__talker_diag__DOT__start_r__v1 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__talker_diag__DOT__stop_r__v1 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__talker_diag__DOT__stop_r__v1 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__talker_diag__DOT__start_r__v2 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__talker_diag__DOT__mreset_r__v5 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__media_clock_restart__DOT__hold_r__v0 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__media_clock_restart__DOT__hold_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__media_clock_restart__DOT__hold_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__media_clock_restart__DOT__hold_r__v1 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__media_clock_restart__DOT__hold_r__v2 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__media_clock_restart__DOT__hold_r__v3 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__media_clock_restart__DOT__hold_r__v4 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__media_clock_restart__DOT__hold_r__v5 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__stat_snap__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__stat_snap__v0 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__stat_snap__v1 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__stat_snap__v2 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__stat_snap__v3 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__stat_snap__v4 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__stat_snap__v5 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__stat_snap__v6 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__stat_snap__v7 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__stat_snap__v8 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__stat_snap__v9 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__stat_snap__v18 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__csr__DOT__shadow_ram__v0 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__csr__DOT__shadow_ram__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__shadow_ram__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__snap_shadow_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__snap_shadow_r__v1 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__snap_shadow_r__v2 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__snap_shadow_r__v4 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__snap_shadow_r__v5 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__snap_shadow_r__v17 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__snap_shadow_r__v29 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__snap_shadow_r__v39 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__snap_shadow_r__v40 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__csr__DOT__snap_shadow_r__v51 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__aaf_packetizer__DOT__tctx_r__v0 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__aaf_packetizer__DOT__tctx_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aaf_packetizer__DOT__tctx_r__v0 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__aaf_packetizer__DOT__stg_r__v0 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__aaf_packetizer__DOT__stg_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aaf_packetizer__DOT__stg_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aaf_packetizer__DOT__pend_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aaf_packetizer__DOT__buf_l_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aaf_packetizer__DOT__buf_r_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aaf_packetizer__DOT__wbank_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aaf_packetizer__DOT__nsamp_r__v1 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aaf_packetizer__DOT__nsamp_r__v2 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aaf_packetizer__DOT__wbank_r__v1 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aaf_packetizer__DOT__buf_l_r__v1 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aaf_packetizer__DOT__buf_l_r__v2 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__aaf_packetizer__DOT__chans_r__v0 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__aaf_packetizer__DOT__chans_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aaf_packetizer__DOT__chans_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__aaf_packetizer__DOT__chans_r__v1 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__chan_map_capture__DOT__map_r__v0 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__chan_map_capture__DOT__map_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__map_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__map_r__v1 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__chan_map_capture__DOT__tdm_hold_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__tdm_hold_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__tdm_hold_r__v1 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__chan_map_capture__DOT__q_rd_r__v0 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__chan_map_capture__DOT__q_rd_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__q_rd_r__v0 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__chan_map_capture__DOT__q_rd_r__v1 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__chan_map_capture__DOT__q_rd_r__v1 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__q_rd_r__v1 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__q_rd_r__v2 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__q_rd_r__v3 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__chan_map_capture__DOT__lb_q_r__v0 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__chan_map_capture__DOT__lb_q_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__lb_q_r__v0 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r__v0 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r__v0 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r__v1 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r__v1 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r__v1 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r__v2 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__q_cnt_r__v3 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__chan_map_capture__DOT__q_wr_r__v0 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__chan_map_capture__DOT__q_wr_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__q_wr_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__q_wr_r__v1 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__q_wr_r__v2 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r__v0 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r__v1 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__chan_map_capture__DOT__lb_hold_r__v2 = 0;
    vlSelf->__VdlyVal__milan_datapath__DOT__g_aif_i2s__DOT__aaf_capture__DOT__u_tcdc__DOT__mem_r__v0 = 0;
    vlSelf->__VdlyDim0__milan_datapath__DOT__g_aif_i2s__DOT__aaf_capture__DOT__u_tcdc__DOT__mem_r__v0 = 0;
    vlSelf->__VdlySet__milan_datapath__DOT__g_aif_i2s__DOT__aaf_capture__DOT__u_tcdc__DOT__mem_r__v0 = 0;
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->__VstlTriggered[__Vi0] = 0;
    }
    for (int __Vi0 = 0; __Vi0 < 3; ++__Vi0) {
        vlSelf->__VicoTriggered[__Vi0] = 0;
    }
    vlSelf->__Vtrigprevexpr___TOP__i_desc_mem_req_ready__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__i_desc_mem_rsp_valid__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__i_desc_mem_rsp_data__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__i_desc_mem_rsp_last__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__i_desc_mem_rsp_err__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__i_resp_mem_req_ready__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__i_resp_mem_rsp_valid__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__i_resp_mem_rsp_data__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__i_resp_mem_rsp_last__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__i_resp_mem_rsp_err__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__i_resp_mem_wr_ready__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__i_resp_mem_wr_done__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__i_resp_mem_wr_err__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__i_nvm_mem_req_ready__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__i_nvm_mem_rsp_valid__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__i_nvm_mem_rsp_data__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__i_nvm_mem_rsp_last__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__i_nvm_mem_rsp_err__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__i_nvm_mem_wr_ready__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__i_nvm_mem_wr_done__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__i_nvm_mem_wr_err__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__axis_clk__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__clk_audio_i__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__clk_tdm_i__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__axis_resetn__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__gtx_clk__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__gtx_resetn__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__s_axi_awaddr__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__s_axi_awvalid__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__s_axi_wdata__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__s_axi_wstrb__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__s_axi_wvalid__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__s_axi_bready__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__s_axi_araddr__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__s_axi_arvalid__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__s_axi_rready__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__i2s_sdout_i__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__tdm_bclk_i__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__tdm_fsync_i__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__tdm_data_i__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__m_axis_mac_tx_tready__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__s_axis_mac_rx_tdata__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__s_axis_mac_rx_tkeep__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__s_axis_mac_rx_tvalid__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__s_axis_mac_rx_tlast__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__i_mac_speed__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__i_link_up__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__i_full_duplex__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__i_ethrx_tgl__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__i_ethtx_tgl__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__i_ethact_tgl__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__i_gptp_txrec_valid__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__i_gptp_txrec_kind__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__i_gptp_txrec_oidx__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__i_gptp_txrec_gen__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__i_gptp_txrec_type__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__i_gptp_txrec_seq__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__i_gptp_txrec_delta__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__i_gptp_txrec_abort__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__i_gptp_txseal_ack__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__i_mac_events__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__i_mac_events_cap__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__i_ps_clk__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__i_mmcm_drp_do__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__i_mmcm_drp_rdy__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__i_mmcm_locked__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__i_mmcm_ps_done__0 = 0;
    vlSelf->__VicoDidInit = 0;
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->__VactTriggered[__Vi0] = 0;
    }
    vlSelf->__Vtrigprevexpr___TOP__axis_clk__1 = 0;
    vlSelf->__Vtrigprevexpr___TOP__clk_audio_i__1 = 0;
    vlSelf->__Vtrigprevexpr___TOP__axis_resetn__1 = 0;
    vlSelf->__Vtrigprevexpr___TOP__i_ps_clk__1 = 0;
    vlSelf->__Vtrigprevexpr___TOP__gtx_clk__1 = 0;
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->__VnbaTriggered[__Vi0] = 0;
    }
}
